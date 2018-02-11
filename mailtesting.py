# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 13:09:57 2017

@author: Edwin
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import os
from time import sleep

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