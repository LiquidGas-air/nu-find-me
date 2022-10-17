import face_recognition as fc
import pickle
import os


def searching_matches(face, tolerance, multiple = False):
    path = os.path.join(os.getcwd(), "NU")

    root = os.scandir(path)
    possible_people = []
    for folder in root:
        path_dir = os.path.join(path, folder.name)
        folder = os.scandir(folder)
        for profile in folder:
            profile_dir = os.path.join(path_dir, profile.name)
            profile = os.scandir(profile)
            for img in profile:
                if os.path.splitext(img)[1] == ".png":
                    img_dir = os.path.join(profile_dir, img.name)
                    with open(f"{os.path.splitext(img)[0]}.pickle", "rb") as file:
                        enc = file.read()
                        enc = pickle.loads(enc)
                        # print(f"{os.path.splitext(img)[0]}.pickle")
                        # print(enc[0][0])
                        if len(enc[0]):
                            enc = enc[0][0]
                        else:
                            break
                        results = fc.face_distance([enc], face)
                        if results[0] < tolerance:
                            possible_people.append([os.path.splitext(img)[0], results[0]])
                            # print(results[0])
                            # yield [f"{os.path.splitext(img)[0]}.txt", f"{os.path.splitext(img)[0]}.png"]

    if len(possible_people) == 0:
        return
    best_fit = possible_people[0]
    real_output = []
    for i in range(0,3):
        for possible_person in possible_people:
            if possible_person[1] < best_fit[1]:
                best_fit = possible_person
        possible_people.remove(best_fit)
        real_output.append(best_fit)
        if len(possible_people) == 0:
            break
        best_fit=possible_people[0]

    for i in real_output:
        yield [f"{i[0]}.txt", f"{i[0]}.png"]

