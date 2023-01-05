from array import array
import numpy as np
from PIL import Image
import os
import cv2

path ="samples"

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def img_lables(path):
    
    imagepaths=[os.path.join(path,f) for f in os.listdir(path)  ]
    facesample=[]
    ids=[]

    for imagepath in imagepaths:

        gray_img=Image.open(imagepath).convert( "L" )
        img_arr=np.array(gray_img,'uint8') # convert image to an array

        id = int(os.path.split(imagepath) [-1].split(".") [1] )
        faces= detector.detectMultiScale(img_arr)

        for (x,y,w,h) in faces:
            facesample.append(img_arr[y:y+h,x:x+w] )
            ids.append(id)
         
    return facesample,ids
    
print(" Face Training success ")

faces,id = img_lables(path)
recognizer.train(faces,np.array(id))

recognizer.write('Trainer/trainer.yml')

print("done  now we can recognize your face ")

