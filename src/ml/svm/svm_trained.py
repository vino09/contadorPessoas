import numpy as np
import cv2
import Pessoa
import time
from matplotlib import pyplot as plt
import math


#Fonte de video
#cap = cv2.VideoCapture(0) # Descomente para usar a camera.
#cap = cv2.VideoCapture("C:\\Users\\Bruno\\Documents\\GitHub\\Contador\\peopleCounter.avi") #Captura um video
cap = cv2.VideoCapture("C:\\Users\\Bruno\\Documents\\GitHub\\Contador\\d.mp4") #Captura um video
#cap = cv2.VideoCapture("C:\\Users\\Bruno\\Documents\\GitHub\\Contador\\bus.avi") #Captura um video


fgbg = cv2.createBackgroundSubtractorMOG2(500,detectShadows = True)

#Elementos estruturantes para filtros morfoogicos
kernelOp = np.ones((3,3),np.uint8)
kernelOp2 = np.ones((5,5),np.uint8)
kernelOp3 = np.ones((8, 8), np.uint8)
kernelCl = np.ones((11,11),np.uint8)
kernelCl2 = np.ones((8, 8), np.uint8)

# Metodo GET para pegar width e height do frame
w = cap.get(3)
h = cap.get(4)

x_meio = int(w / 2)
y_meio = int(h / 2)

frameArea = h * w
print("Area do Frame:", frameArea)
areaTH = frameArea / 225
print ('Area Threshold', areaTH)  # Area de contorno usada para detectar uma pessoa

count = 0

svm = cv2.ml.SVM_load('svm_data.dat')
#print(svm.getSupportVectors())

list_P = []
list_N = []
list = []

while(cap.isOpened()):
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    fgmask2 = fgbg.apply(frame)

    # Binarização para eliminar sombras (color gris)
    try:

        fgmask = cv2.GaussianBlur(fgmask, (3, 3), 0)
        fgmask2 = cv2.GaussianBlur(fgmask2, (3, 3), 0)

        ret, imBin = cv2.threshold(fgmask, 128, 255, cv2.THRESH_BINARY)
        ret, imBin2 = cv2.threshold(fgmask2, 128, 255, cv2.THRESH_BINARY)

        # Opening (erode->dilate) para remover o ruído.
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp3)
        mask2 = cv2.morphologyEx(imBin2, cv2.MORPH_OPEN, kernelOp3)

        # Closing (dilate -> erode) para juntar regiões brancas.
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelCl2)
        mask2 = cv2.morphologyEx(mask2, cv2.MORPH_CLOSE, kernelCl2)
    except:
        print('EOF')

    # RETR_EXTERNAL returns only extreme outer flags. All child contours are left behind.
    _, contours0, hierarchy = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    _center = [314.67404, 231.52438]
    for cnt in contours0:
        area = cv2.contourArea(cnt)
        # cv2.drawContours(frame, cnt, -1, (0,0,255), 3, 8)
        if area > areaTH:
            #print(cnt.tolist())
            #print(len(cnt))
            #print(type(cnt))
            #####################
            #   RASTREAMENTO    #
            #####################

            # Falta agregar condições para multiplas pessoas, saídas e entradas da tela

            M = cv2.moments(cnt)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])

            b = np.float32(cv2.HuMoments(M)).reshape(-1, 7)
            #print(len(b))
            #print(b)
            a = svm.predict(b)
            #print(str(a[1]))
            if(str(a[1]) == "[[0.]]"):
               print(a)


            list.append((cx, cy))

            dist = math.hypot(_center[0] - cx, _center[1] - cy)

            #print(dist)

            if(dist < 200):
                count +=1

            x, y, w, h = cv2.boundingRect(cnt)

            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Frame', frame)
    cv2.imshow('Debug', mask)

    # preisonar ESC para sair
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    # END while(cap.isOpened())

    #################
    #   LIMPEZA     #
    #################

cap.release()
cv2.destroyAllWindows()
