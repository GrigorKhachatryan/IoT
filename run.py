import cv2
import numpy as np
import os
import time
import requests

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX
status = False
# iniciate id counter
id = 0
id_camera = 'Камера №2'

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['unknown','Grigor']

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video widht
cam.set(4, 480)  # set video height

# Define min window size to be recognized as a face
minW = 0.1 * cam.get(3)
minH = 0.1 * cam.get(4)

def minus_time(start,stop):
    start = start.split(':')
    stop = stop.split(':')
    result = []
    H = int(stop[0])-int(start[0])
    M = int(stop[1])-int(start[1])
    S = int(stop[2])-int(start[2])
    if S < 0:
        M -= 1
        S += 60
    if M < 0:
        H -= 1
        M += 60

    result.extend([str(H), str(M), str(S)])
    return ':'.join(result)


while True:
    ret, img = cam.read()
    # img = cv2.flip(img, -1)  # Flip vertically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    if len(faces) == 0 and status is True:
        status = False
        times = minus_time(start,time.strftime("%H:%M:%S"))
        info = f'Пользователь {id} покинул территорию , Присутствововал {times}'
        param = {'message': info,
                 'camera': id_camera,
                 'date': time.strftime("%Y-%m-%d %H:%M:%S")}
        a = requests.get('http://localhost:5000/up/iot', params=param )


    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 40):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))

        cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
        cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        if status is False:
            start = time.strftime("%H:%M:%S")
            info = f'Пользователь {id} зашел на территорию'
            param = {'message': info,
                     'camera': id_camera,
                     'date': time.strftime("%Y-%m-%d %H:%M:%S")}
            a = requests.get('http://localhost:5000/up/iot', params=param )
            status = True

    cv2.imshow('camera', img)

    k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()