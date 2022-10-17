import logging
from aiogram import Bot, Dispatcher, executor, types
import face_recognition as fc
from search import searching_match
from searches import searching_matches
import aiogram.utils.markdown as md
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
import buttons as nav
from save import save_enc

API_TOKEN = '5722537089:AAHApqnTQMfVgU_C2jpQ0tacwNI9GC_RNF4'
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    method = State()
    img_settings = State()
    img_single = State()
    img_multiple = State()
    name = State()
    save = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await Form.img_settings.set()
    global answer
    answer = await message.answer("How many profiles to output? \none or multiple?", reply_markup=nav.setting_img)

# @dp.message_handler(regexp='(^cat[s]?$|puss)')
# async def cats(message: types.Message):
#     with open('data/cats.jpg', 'rb') as photo:
#         '''
#         # Old fashioned way:
#         await bot.send_photo(
#             message.chat.id,
#             photo,
#             caption='Cats are here 😺',
#             reply_to_message_id=message.message_id,
#         )
#         '''
#
#         await message.reply_photo(photo, caption='Cats are here 😺')

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()


# @dp.message_handler(state=Form.method, commands=["by_img"])
# async def method_set(message: types.Message,  state: FSMContext):
#     await Form.img_settings.set()
#
#     await message.answer("How many profiles to output? \none or multiple?")


@dp.message_handler(state=Form.img_settings, commands=["one", "multiple"])
async def multiple_one(message: types.Message,  state: FSMContext):
    try:
        await bot.delete_message(chat_id=answer.chat.id, message_id=answer.message_id)
    except:
        pass
    if message.text == "/one":
        await Form.img_single.set()
    elif message.text == "/multiple":
        await Form.img_multiple.set()

    await message.answer("Awaiting photo of single person...")
    logging.info(await state.get_state())


@dp.message_handler(state=Form.img_single, content_types=['photo'])
async def receive_photo_of_target(message, state: FSMContext):
    global answer
    global results
    is_there = int()
    results = list()
    await message.photo[-1].download('temp.jpg')
    try:
        img = fc.face_encodings(fc.load_image_file("temp.jpg"))[0]
    except:
        await Form.img_settings.set()
        await bot.send_message(chat_id=message.chat.id, text="Invalid image, repeat", reply_markup=nav.setting_img)
        return
    waiting = await bot.send_message(message.chat.id, text="PROCESSING...")

    for result in searching_match(img, tolerance=0.4):
        if type(result) == list:
            results.append(result)
            is_there += 1
    if is_there == 0:
        await message.answer("No such person known.")
        await Form.img_settings.set()
        answer = await message.answer("How many profiles to output? \none or multiple?", reply_markup=nav.setting_img)
        return

    await bot.send_message(message.chat.id, text="Here are some results:")
    for result in results:
        with open(result[0], "r") as txt, open(result[1], "rb") as persona:
            txt = txt.read()
            await message.reply_photo(persona, caption=txt)
    await bot.delete_message(chat_id=waiting.chat.id, message_id=waiting.message_id)

    await Form.save.set()

    await bot.send_message(message.chat.id, text="If you found a needed person, \nwould you like to add his/her photo to gallery for better search results next time?", reply_markup=nav.setting_encoding)


@dp.message_handler(state=Form.img_multiple, content_types=['photo'])
async def receive_photo_of_targets(message, state: FSMContext):
    global answer
    global results
    is_there = int()
    results = list()
    await message.photo[-1].download('temp.jpg')
    try:
        img = fc.face_encodings(fc.load_image_file("temp.jpg"))[0]
    except:
        await Form.img_settings.set()
        await bot.send_message(chat_id=message.chat.id, text="Invalid image, repeat", reply_markup=nav.setting_img)
        return
    waiting = await bot.send_message(message.chat.id, text="PROCESSING...")

    for result in searching_matches(img, tolerance=0.4):
        if type(result) == list:
            results.append(result)
            is_there += 1
    if is_there == 0:
        await message.answer("No such person known.")
        await Form.img_settings.set()
        answer = await message.answer("How many profiles to output? \none or multiple?", reply_markup=nav.setting_img)
        return

    await bot.send_message(message.chat.id, text="Here are some results:")
    for result in results:
        with open(result[0], "r") as txt, open(result[1], "rb") as persona:
            txt = txt.read()
            await message.reply_photo(persona, caption=txt)
    await bot.delete_message(chat_id=waiting.chat.id, message_id=waiting.message_id)

    await Form.save.set()

    await bot.send_message(message.chat.id, text="If you found a needed person, \nwould you like to add his/her photo to gallery for better search results next time?", reply_markup=nav.setting_encoding)


@dp.message_handler(state=Form.save, commands=["yes", "no"])
async def save(message, state: FSMContext):
    global answer
    if message.text == "/yes":
        # save_enc(results[0])
        await Form.img_settings.set()
        answer = await message.answer("How many profiles to output? \none or multiple?", reply_markup=nav.setting_img)

    elif message.text == "/no":
        await Form.img_settings.set()
        answer = await message.answer("How many profiles to output? \none or multiple?", reply_markup=nav.setting_img)

# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#
#     await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
