import cv2
import os

import imutils
template_path= 'others/'
files = os.listdir(template_path)
counter=1
for template in files:
    image=cv2.imread(template_path+template,0)
    image=cv2.resize(image,(2000,2000))
    cv2.imwrite(template_path1+str(counter)+'.jpg',rotated)
         '''   for i in range (0,20,2):
        image=cv2.resize(image,(20+i,20+i))

        for angle in range(0,360,60):
            rotated = imutils.rotate(image, angle)
            cv2.imwrite(template_path1+str(counter)+'.jpg',rotated)
            counter=counter+1
            print(counter)'''
