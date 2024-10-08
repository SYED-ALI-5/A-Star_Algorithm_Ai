from datetime import datetime
import dlib
import face_recognition
import cv2
import numpy as np

print('Capturing...\nPress enter when ready!')

class FaceRecognizer:
    def __init__(self):
        self.known_faces = []
        self.names = []
        self.ages = []
        
    def add_face(self, image_path, name, age):
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        self.known_faces.append(encoding)
        self.names.append(name)
        self.ages.append(age)

    def recognize_face(self, frame):
        faces = self.detect_faces(frame)

        for face in faces:
            top, right, bottom, left = face
            face_encoding = face_recognition.face_encodings(frame, [(top, right, bottom, left)])

            if len(face_encoding) > 0:
                face_encoding = face_encoding[0]
                face_compare = face_recognition.compare_faces(self.known_faces, face_encoding)
                distance = face_recognition.face_distance(self.known_faces, face_encoding)
                best_match_index = np.argmin(distance)

                if face_compare[best_match_index]:
                    name = self.names[best_match_index]
                    age = self.ages[best_match_index]
                    return name, age

        return None, None

    def detect_faces(self, frame):
        detector = dlib.get_frontal_face_detector()
        faces = detector(frame)
        face_locations = [(face.top(), face.right(), face.bottom(), face.left()) for face in faces]
        return face_locations

    def capture(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Camera failed!")
            return None

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Camera failed!")
                break

            faces = self.detect_faces(frame)

            for face in faces:
                top, right, bottom, left = face
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 100, 255), 2)

            cv2.imshow('Camera', frame)

            k = cv2.waitKey(10)

            if k % 256 == 13:
                print('Captured...')
                break

        cap.release()
        cv2.destroyAllWindows()

        return frame

class Watchman:
    def __init__(self):
        self.house_warden = None
        self.time = 22

    def set_house_warden(self, name, age):
        self.house_warden = {'name': name, 'age': age}

    def check_permission(self, name, age):
        current_time = datetime.now().time().hour
        if name not in face_recognizer.names or age not in face_recognizer.ages:
            print("You are an outsider. Please ask the house warden for permission.")
            self.ask_warden_permission()
        elif self.house_warden is None:
            print("House warden not defined. Please provide house warden details to proceed.")
            n = input('Name:')
            a = input('Age:')
            self.set_house_warden(n, a)
        elif name == self.house_warden['name']:
            print(f"Welcome, {name}!")
            choice = input('Sir what you want to do?\n1. Just pass\n2. Allow guest entry\n3. Change closing time\n')
            if choice == '1':
                self.allow_entry()
            elif choice == '2':
                frame = face_recognizer.capture()
                if frame is not None:
                    self.allow_entry()
            elif choice == '3':
                self.time = int(input(f"Current closing time: {self.time}\nEnter new closing time: "))
        elif age < 13:
            self.check_teenager_permission(age, current_time)
        elif name in face_recognizer.names and age in face_recognizer.ages:
            self.allow_entry()
        else:
            print("You are an outsider. Please ask the house warden for permission.")


    def check_teenager_permission(self, age, current_time):
        if current_time >= self.time:  
            print(f"It's past {self.time} . Please ask the house warden for permission to enter.")
            self.ask_warden_permission()
        else:
            print("You are a teenager, but it's not past 10 PM. You can enter.")
            self.allow_entry()
   
    def allow_entry(self):
        print("Entry allowed.")
        exit()

    def ask_warden_permission(self):
        print('Capturing Warden')
        captured_frame = face_recognizer.capture()
        if captured_frame is not None:
            name, age = face_recognizer.recognize_face(captured_frame)
            if name == self.house_warden:
                print('Warden detected')
                self.allow_entry()
            else:
                print('Warden not recognized!\nPermission denied.')
                exit()

face_recognizer = FaceRecognizer()

# Replace with your Image Path
face_recognizer.add_face('E:/TECNO/D CAMRA/Ahmad.jpg', 'Syed Ahmad Ali', 21)
face_recognizer.add_face('E:/TECNO/D CAMRA/IMG_20220303_155444_765.jpg', 'Athar', 19)
face_recognizer.add_face('E:/TECNO/D CAMRA/Baghwaan.jpg', 'Syed Ali Hamza', 17)
face_recognizer.add_face('E:/TECNO/D CAMRA/PICTURE/IMG_3696.JPG', 'Mustafa', 22)

captured_frame = face_recognizer.capture()

if captured_frame is not None:
    name, age = face_recognizer.recognize_face(captured_frame)
    
    if name is not None and age is not None:
        print(f"Detected: {name}, Age: {age}")

    watchman = Watchman()
    watchman.set_house_warden("Ajmal",53)
    watchman.check_permission(name,age)