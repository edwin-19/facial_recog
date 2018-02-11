# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 23:05:06 2017

@author: Edwin
"""
import sqlite3
import cv2
import numpy as np
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os
import csv
from time import gmtime, strftime

def sendEmail(message,count):
    ImgFileName = "C:\\Users\\Edwin\\Documents\\Python Projects\\Facial Recognition\\Unknown\\Unknown User-" + str(count) +".jpg"
    
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Unknown User'
    msg['From'] = 'edwin4v@gmail.com'
    msg['To'] = '0111774@gmail.com'
    
    text = MIMEText(message)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)
    
    mail = smtplib.SMTP ('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('edwin4v@gmail.com','cheong16')
    mail.sendmail("edwin4v@gmail.com","0111774@gmail.com", msg.as_string())
    mail.quit()

def writeToCSV(name,time):
    count = 1
    myData = [
        ["Name", "Time"],
        [name,time]
    ]
    
    myFile = open('example2.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(myData)
    
    print("Writing complete")
    count += 1

def takePicture(color, count):
    cv2.imwrite("Unknown/Unknown User-" + str(count) +".jpg", color) 
   
def getProfile(id):
    conn = sqlite3.connect("FaceDatabase.db")
    try:
        if conn:
            command = "SELECT * FROM People WHERE ID = ?"
            cursor = conn.execute(command, str(id))
            profile = None
            
            for row in cursor:
                profile = row
            
            conn.close()
            return profile
            
    except sqlite3.ProgrammingError as ex:
        print("Error: " + str(ex))

def faceRecognizer():
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load('trainer/trainer.yml')
    
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    cap = cv2.VideoCapture(0)
    
    count = 1
    
    while 1:
        ret, im = cap.read()
        
        gray = 0
        if ret is True:
            gray =  cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        else:
            continue
        faces = face_cascade.detectMultiScale(gray, 1.2, 5, minSize=(100, 100), flags = cv2.CASCADE_SCALE_IMAGE)
        
        for (x,y,w,h) in faces:
             cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 3)
             roi_color = im[y:y+h, x:x+w]
             
             id = recognizer.predict(gray[y:y+h,x:x+w])
             print(id)
             
             profile = getProfile(id[0])
             
             cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,255,0), -1)
             if id[1] > 50:
                 if profile != None:
                    cv2.putText(im,"ID: " + str(profile[0]),(x,y-50),font,2, (255,255,255), 3); #label faces
                    cv2.putText(im, "Name: "+ str(profile[1]),(x,y-10),font,2, (255,255,255), 3); #label faces
                    cv2.putText(im, "Age: " + str(profile[2]),(x,y+h+80),font,2, (255,255,255), 3); #label faces
                    cv2.putText(im,"Rel: " +str(profile[4]),(x,y+h+130),font,2, (255,255,255), 3); #label faces
                    print(count)
                    if count > 1:
                        currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        takePicture(roi_color,count)
                        writeToCSV(profile[1], currentTime)
                    
                    count += 1
             elif id[1] < 50: 
                 id = "Unknown"   
                 cv2.putText(im, str(id), (x,y-40), font, 2, (255,255,255), 3)
                 
                 
                 
                 #takePicture(roi_color,count)
                 #sendEmail("Unknonwn User",count)
                 count += 1
                 
             #cv2.putText(im, str(id), (x,y-40), font, 2, (255,255,255), 3)
             
        cv2.imshow('Facial Detection', im)
    
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
             
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    faceRecognizer()
    