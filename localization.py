# code for image segmentation and detection
#by tamilselvan
#02,July 2018

#importing necessary libraries.
import cv2
import numpy as np
import os
import time
from PIL import Image
from matplotlib import pyplot as plt
import csv

#for writing into csv file.
f = open('Sample-Output.csv','w')
f.write('FileName,GCPLocation\n')

i=0
flag=0
count=1
def blurring(flag,file,chuck_gray,chuck):
    chuck_bw = cv2.threshold(chuck_gray, 230, 255, cv2.THRESH_BINARY)[1]
    chuck_bw, contours, hierarchy = cv2.findContours(chuck_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    try:
        cnt = contours[0]
        contours=None
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        hull = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull)
        area = cv2.contourArea(cnt)
        save(flag,file,chuck,cx,cy,cnt,defects)
    except:
        return 0


def save(flag,file,chuck,cx,cy,cnt,defects):
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        sstart = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        #when the centroid and the contours's edge are set apart by 3 pixels, the contour edge is calculated as the GCP
        if np.abs(far[0]-cx)<= 3 and np.abs(far[1]-cy)<= 3:
          cv2.line(chuck,sstart,end,[0,255,0],2)
          cv2.circle(chuck,far,2,[0,0,255],-1)
          flag=flag+1
    if(flag>=1):
        cv2.imwrite(path_to_save+str(pt)+file, chuck)
    else:
        #it will execute the same save operation but with the minimum distance between centroid and countour's edges as 4
        extreme(flag,file,chuck,cx,cy,cnt,defects,chuck_gray)

def extreme(flag,file,chuck,cx,cy,cnt,defects,chuck_gray):
    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        sstart = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])
        print(far,cx,cy,flag)
        if np.abs(far[0]-cx)<= 4 and np.abs(far[1]-cy) <= 4:
          cv2.line(chuck,sstart,end,[0,255,0],2)
          cv2.circle(chuck,far,2,[0,0,255],-1)
        #to save the chucks to a path
        cv2.imwrite(path_to_save+str(pt)+file, chuck)

#declaring the paths       
path = 'dataset/'
template_path= 'template/'
path_to_chucks = 'chucks/'
path_to_save= 'GCP_marked/'
files = os.listdir(path)
templates=os.listdir(template_path)
#looping across every images in the file.
for file in files:
    img_rgb= cv2.imread(path+file)
    height,width,_=img_rgb.shape
    counter=0
    pt_prev=(0,0)
    c=0
    f.write(file+',[')
    #looping across the every possible templates
    for temp  in templates:
        start = time.time()
        template = cv2.imread(template_path+temp,0)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        #loc will have the points which has matching templates
        for pt in zip(*loc[::-1]):
            #to remove away chucks that are close to each other and to avoid repeation
           if(pt[0]-pt_prev[0])>=10 and (pt[1]-pt_prev[1])>=10:
              chuck= img_rgb[pt[1]:(pt[1] + h), pt[0]:(pt[0] + w)]
              # to use bilaterial filtering to smoothening the chuck
              chuck= cv2.bilateralFilter(chuck,10,75,75)
              chuck_gray =cv2.cvtColor(chuck, cv2.COLOR_BGR2GRAY)
              chuck_bw = cv2.threshold(chuck_gray, 190, 255, cv2.THRESH_BINARY)[1]
              #to remove complete black image and to remove very small chucks
              if cv2.countNonZero(chuck_bw) == 0 or (chuck_bw.shape[0]<=26 and chuck_bw.shape[1]<=26):
                  continue
              else:
                  flag=0
                  #to normalize black and white image and to smoothen image by gaussian filter
                  cv2.normalize(chuck_bw, chuck_bw, 0, 255, cv2.NORM_MINMAX)
                  blur = cv2.GaussianBlur(chuck_bw,(5,5),0)
                  smooth = cv2.addWeighted(blur,1.5,chuck_bw,-0.5,0)
                  #to find the contours in the chucks
                  chuck_bw, contours, hierarchy = cv2.findContours(smooth, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                  cnt = contours[0]
                  contours=None
                  M = cv2.moments(cnt)
                  cx = int(M['m10']/M['m00'])
                  cy = int(M['m01']/M['m00'])
                  hull = cv2.convexHull(cnt,returnPoints = False)
                  defects = cv2.convexityDefects(cnt,hull)
                  #to find the area of the contours so that it will remove  false positives
                  area = cv2.contourArea(cnt)
                  #if the area of image is more than or less than the desired area it is set to further blurring operations 
                  if int(area)<=100 or int(area)>=1000 :
                    flag=blurring(flag,file,chuck_gray,chuck)

                  else:
                  #if found that image is of desired area, it given into a function where GCP is calculated
                    flag=save(flag,file,chuck,cx,cy,cnt,defects)

                  #it marks the chucks on the raw image
                  cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
              pt_prev=pt
              f.write('['+str(pt[0])+','+str(pt[1])+'],')
              c=c+1
        counter=counter+1
        finish=time.time()
        #to print the execution time to the console
        print(str(count)+'-'+str(file)+" -mask count "+str(counter)+" took =  "+str(finish-start)+' sec')
    if c==0:
      f.write('NIL')
    f.write(']\n')
    cv2.imwrite(path_to_chucks+file, img_rgb)
    count=count+1


