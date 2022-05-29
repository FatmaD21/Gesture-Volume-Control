import math

import cv2
import time
import numpy as np
#import prevt as prevt

import HandTrackingModule as htm
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities , IAudioEndpointVolume


#######################
camera_width,camera_ht=640,480
######################

cap=cv2.VideoCapture(0)
cap.set(3,camera_width)
cap.set(4,camera_ht)
prevt =0

hdobj = htm.handdetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_ , CLSCTX_ALL , None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()

volRange=volume.GetVolumeRange()
#print(volRange)

minVol=volRange[0]
maxVol=volRange[1]
vol=0
volBar=400
volPer=0



while True:
    success, Image=cap.read()
    Image = hdobj.findHands(Image)
    lmList=hdobj.findPosition(Image,draw=False)
    if len(lmList)!=0:
        print(lmList[4],lmList[8])

        x1,y1=lmList[4][1],lmList[4][2]
        x2 ,y2 = lmList[8][1], lmList[8][2]
        cx,cy=(x1+x2)//2,(y1+y2)//2

        cv2.circle(Image, (x1,y1),15,(0,100,0),cv2.FILLED)
        cv2.circle(Image, (x2, y2), 15, (255,255,0), cv2.FILLED)
        cv2.line(Image,(x1,y1),(x2,y2),(255,255,0),3)
        cv2.circle(Image, (x2, y2), 15, (0,100,0), cv2.FILLED)

        length=math.hypot(x2-x1,y2-y1)
       # print(length)


        # hand range 50 to 300
        #vol range -65 to 0

        vol=np.interp(length,[50,300],[minVol,maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)





    cv2.rectangle(Image,(50,150),(85,400),(255,0,0),3)
    cv2.rectangle(Image, (50,int(volBar)), (85, 400), (255,0,0), cv2.FILLED)
    cv2.putText(Image, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)

    currentt=time.time()
    fps=1/(currentt-prevt)
    prevt=currentt

   # cv2.putText(Image,f'FPS:{int(fps)}',(30,115),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.putText(Image, 'Place your hand near camera', (56, 35), cv2.FONT_HERSHEY_COMPLEX, 1, (86,55,230), 3)

    cv2.imshow("Img", Image)
    cv2.waitKey(1)
