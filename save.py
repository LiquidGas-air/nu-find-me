import face_recognition as fc
import pickle
import os

def save_enc(path):
    path = os.path.splitext(path[0])
    with open(f"{path}.pickle", "rb") as file:
        known = pickle.loads(file.read())[0]
    unknown = fc.load_image_file("temp.jpg")
    unknown = fc.face_encodings(unknown)[0]
    known[0].append(unknown)
    print(known)

