from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel = KeyboardButton("Cancel")

img_one_set = KeyboardButton("/one")
img_multiple_set = KeyboardButton("/multiple")
setting_img = ReplyKeyboardMarkup(resize_keyboard=True).add(img_one_set, img_multiple_set)

encoding_add = KeyboardButton("/yes")
encoding_not_add = KeyboardButton("/no")
setting_encoding = ReplyKeyboardMarkup(resize_keyboard=True).add(encoding_add, encoding_not_add)