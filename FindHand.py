"""import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
prevt = 0
currentt = 0
cap = cv2.VideoCapture(0)
hdobj = htm.handdetector()
while True:
    success,Image = cap.read()
    Image = hdobj.findHands(Image)
    lmList= hdobj.findPosition(Image)
    if len(lmList)!=0:
        print(lmList[4])
    currentt = time.time()
    fps = 1 / (currentt - prevt)
    prevt = currentt
    cv2.putText(Image, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 3)
    cv2.imshow("image", Image)
    cv2.waitKey(1)"""