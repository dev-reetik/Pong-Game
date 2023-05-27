import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
import pygame 
from pygame import mixer

mixer.init()

#load the file
mixer.music.load("music.mp3")

#set volume
mixer.music.set_volume(1.0)
mixer.music.play()
print("MAKE YOUR FINGERS READY TO FOR DOING SOME WORKOUT !!")


cap = cv2.VideoCapture(0)
cap.set(3,1200)
cap.set(4,720)

imgBackground = cv2.imread('Background.png')
imgBall = cv2.imread('Resources/Ball.png', cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread('Resources/bat1.png', cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread('Resources/bat2.png', cv2.IMREAD_UNCHANGED)



detector = HandDetector(detectionCon=0.8, maxHands=2)


ballpos = [100,100]
speedx = 15
speedy = 15

while True:
   res, img = cap.read()
   hands, img = detector.findHands(img) 
   img = np.fliplr(img)
   img = cv2.addWeighted(img,0.3,imgBackground,0.8,0)
   if hands:
      for hand in hands:
         x, y, w, h = hand['bbox']
         h1, w1, _ = imgBat1.shape
         h1, w1, _ = imgBat2.shape
         y1 = y - h1//2
         y1 = np.clip(y1, 20 ,415)
         
         
         if hand ["type"] == "Left":
            img = cvzone.overlayPNG (img,imgBat1,(60,y1) ) 
            if 60 < ballpos[0]<60+w1 and y1 < ballpos[1]< y1+h1:
               speedx= -speedx

         if hand ["type"] == "Right":
            img = cvzone.overlayPNG (img,imgBat2,(1195,y1) ) 
            if 1195-50 < ballpos[0]<1195 and y1 < ballpos[1]< y1+h1:
               speedx= -speedx

   if ballpos[1] >= 500 or ballpos[1] <= 10:
      speedy = -speedy
   if ballpos[1] == imgBat2.shape:
            speedx = -speedx  
            
   ballpos[0] += speedx
   ballpos[1] += speedy
   img = cvzone.overlayPNG (img,imgBall,ballpos)

   cv2.imshow("Image", img)

   cv2.waitKey(1)