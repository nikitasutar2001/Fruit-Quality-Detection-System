import cv2
import numpy as np
#import time
from copy import deepcopy
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
#The name of the image file to annotate
#i=time.strftime("%d-%m-%y_%H-%M-%S")
#capture image
#camera = cv2.VideoCapture(0)
#return_value, image = camera.read()
#cv2.imwrite(i+'.jpeg', image)
#del(camera)
#image = cv2.imread("raw14.jpeg") 
#image = cv2.imread("red.png") 
#image = cv2.imread("med.png") 
image=cv2.imread("HP000 (28).jpg") 
frame=image
edge_img=deepcopy(image)
 # finds edges in the input image and
# marks them in the output map edges
edged = cv2.Canny(edge_img,50,100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
 
# find contours in the edge map
cnts, h = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

max_contA=cv2.contourArea(cnts[0])
max_cont=max(cnts,key=cv2.contourArea)

for i in range(len(cnts)):
    	x,y,w,h=cv2.boundingRect(max_cont)
    	cv2.rectangle(edge_img,(x,y),(x+w,y+h),(0,0,255), 2)
croppedk=frame[y:y+h,x:x+w]

# Display the fruit 
cv2.imshow('Input Image',edge_img)

frame=edge_img

# converting BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# define range of red color in HSV
lower_red = np.array([170,50,50])
upper_red = np.array([180,255,255])
     
# create a red HSV colour boundary and 
# threshold HSV image
redmask = cv2.inRange(hsv, lower_red, upper_red) 
#redmask=redmask1+redmask2 

maskOpen=cv2.morphologyEx(redmask,cv2.MORPH_OPEN,kernelOpen)
maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)

maskFinal=maskClose
cv2.imshow('Red Mask:',maskFinal)
cnt_r=0
for r in redmask:
	    cnt_r=cnt_r+list(r).count(255)
print ("Redness: ",cnt_r)

# define range of yellow color in HSV
lower_yellow=np.array([25,50,70])
upper_yellow=np.array([35,255,255])

# create a yellow HSV colour boundary and 
# threshold HSV image
yellowmask = cv2.inRange(hsv, lower_yellow, upper_yellow)
cv2.imshow('Yellow Mask:', yellowmask)
cnt_y=0
for y in yellowmask:
	cnt_y=cnt_y+list(y).count(255)
print ("Yellowness: ",cnt_y)


# define range of green color in HSV
lower_green=np.array([25,52,72])
upper_green=np.array([102,255,255])

# create a yellow HSV colour boundary and 
# threshold HSV image
greenmask = cv2.inRange(hsv, lower_green, upper_green)
cv2.imshow('Green Mask:',greenmask)
cnt_g=0
for g in greenmask:
	cnt_g=cnt_g+list(g).count(255)
print ("Greenness: ",cnt_g)

#Calculate ripeness
tot_area=cnt_r+cnt_y+cnt_g
rperc=cnt_r/tot_area
yperc=cnt_y/tot_area
gperc=cnt_g/tot_area

#Adjust the limits for your fruit
glimit=0.5
ylimit=0.8

if gperc>glimit:
	print ("Unripe")
elif yperc>ylimit:
	print ("Overripe")
else:
	print ("Ripe")
# Wait for any key to close
cv2.waitKey(0)
cv2.destroyAllWindows() 
