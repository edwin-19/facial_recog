import cv2
import sqlite3

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

def insertNewUser(id,name, age, relationship):
    p_id = id
    p_name = name
    p_age = age
    #p_gender = gender
    p_relations = relationship
    
    conn = sqlite3.connect("FaceDatabase.db")
    try:
        if conn:
            command = "SELECT * FROM People WHERE ID = ?" 
            cursor = conn.execute(command, p_id)
               
            isRecordExsist = 0 
            for row in cursor:
                isRecordExsist = 1
               
            if isRecordExsist is True:
                command = "UPDATE People SET Name="+str(p_name)+" WHERE ID="+str(p_id)
            else:
                command="INSERT INTO People(ID,Name,Age,Relationship) Values(?,?,?,?)"
            
            conn.execute(command, (p_id, p_name, p_age, p_relations))
            conn.commit()
            conn.close()
        
    except sqlite3.ProgrammingError as ex:
        print("Error: " + str(ex))
       
    
def faceDetect(face_id):
    cap = cv2.VideoCapture(0)
    count = 0 
    
    while 1:
        ret, img = cap.read()
        gray = 0
        
        if ret is True:
            gray =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            continue
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for(x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            
            count+=1
            cv2.imwrite("dataSet/face-" + str(face_id) + "." + str(count) + ".jpg", roi_gray)
                
        if count > 20:
            cap.release()
            cv2.destroyAllWindows()
            break
        
        cv2.imshow('facial', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    """
    cap.release()
    cv2.destroyAllWindows()"""

p_id = input("Please enter ID: ")
p_name = input("Please enter your name:")
p_age = input("Enter age: ")
p_relationship = input("Enter your relationship:")

insertNewUser(p_id, p_name, p_age, p_relationship)
faceDetect(p_id)