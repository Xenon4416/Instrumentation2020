import serial
import time
from datetime import datetime
import cv2
faceCascade = cv2.CascadeClassifier('ffd.xml')
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height
xHist = 0
xHistCur = 0
takeSample = True

# ard = serial.Serial("COM6", 9600, timeout=1)
# try:
#     ard = serial.Serial("COM6", 9600, timeout=1)
# except:
#     print('Please check the port')

file = open('Dat.txt', 'a') # TODO: Edit Dat.txt to Data.txt
while True:
    # image processing
    ret, img = cap.read()
    # img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x, y, w, h) in faces:
        if xHist == 0:
            xHist = x
        # temp = str(ard.readline())
        # if temp != "b''" and takeSample:
        #     temp = temp.split('\\')[0][2:]
        #     now = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        #     if temp == 'Entry' and xHist-x > 0:
        #         now += ' 1'
        #     elif temp == 'Exit' and xHist-x < 0:
        #         now += ' 0'
        #     print(now, file=file)
        #     takeSample = False
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = img[y:y + h, x:x + w]
        xHistCur = x
    if faces == ():
        xHist = 0
        takeSample = True
    cv2.imshow('video', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break
    time.sleep(0.1)
cap.release()
cv2.destroyAllWindows()