# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 22:28:27 2017

@author: Edwin
"""

import cv2, os
import numpy as np 
from PIL import Image

recognizer = cv2.face.createLBPHFaceRecognizer()
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def get_image_and_labels(path):
    
    # Get all file path
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
    
    faceSamples = []
    
    ids = [] 
    
    for imagePath in imagePaths:
        PIL_img = Image.open(imagePath).convert('L')
        
        img_numpy = np.array(PIL_img, 'uint8')
        
        # Get the image id
        id = int(os.path.split(imagePath)[1].split(".")[0].replace("face-", ""))
        print(id)
        
        faces = face_cascade.detectMultiScale(img_numpy)
        
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)
            cv2.imshow("Adding faces to traning set...", img_numpy[y: y + h, x: x + w])
            cv2.waitKey(10)
            
    return faceSamples, ids

faces, ids = get_image_and_labels('dataSet')
cv2.imshow('test',faces[1])
cv2.waitKey(1)

recognizer.train(faces, np.array(ids))
recognizer.save('trainer/trainer.yml')
cv2.destroyAllWindows()