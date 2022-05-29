import cv2
import mediapipe as mp
import time



class handdetector():
    def __init__(self, mode=False, maxHands=2, modComplexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modComplexity = modComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modComplexity, self.detectionCon, self.trackCon)
        self.pic = mp.solutions.drawing_utils



    def findHands(self, Image, draw=True):         #bgr to rgb for hands of mediapipe
        rgb = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
        self.pframe = self.hands.process(rgb)
        if self.pframe.multi_hand_landmarks:
            for lms in self.pframe.multi_hand_landmarks:
                if draw:
                    self.pic.draw_landmarks(Image, lms, self.mpHands.HAND_CONNECTIONS)
        return Image

    def findPosition(self, Image, handNo=0, draw=True):
        lmList = []
        if self.pframe.multi_hand_landmarks:
            focushand = self.pframe.multi_hand_landmarks[handNo]
            for id, lm in enumerate(focushand.landmark):
                # print(id,lm)
                h, w, channel = Image.shape
                cx, cy = int(lm.x *w), int(lm.y*h )
                # print(id,cx,cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(Image, (cx, cy), 7, (240, 1, 0), cv2.FILLED)
        return lmList


def main():
    prevt = 0
    currentt = 0
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    hdobj = handdetector()
    while True:
        success, Image = cap.read()
        Image = hdobj.findHands(Image)

        lmList = hdobj.findPosition(Image)
        if len(lmList) != 0:
            print(lmList[4])

        currentt = time.time()
        fps = 1 / (currentt - prevt)
        prevt = currentt
        cv2.putText(Image, str(int(fps)), (10, 70), cv2.FONT_ITALIC, 3, (255, 0, 255), 3)
        cv2.imshow("image", Image)
        cv2.waitKey(1)



