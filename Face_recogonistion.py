import cv2
import csv 
import datetime 
 


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Trainer/trainer.yml')
cascadePath = 'haarcascade_frontalface_default.xml'
faceCascade=cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX 

id = 2
name=['','daksh' ] 


cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(3,640)
cam.set(4,480)

minW=0.1*cam.get(3)
minH=0.1*cam.get(4)

def attendence(name):
    with open ('Attendance.csv','r+') as f:
        saved=False
        mydataList=f.readlines()
        nameList=[]
        for line in mydataList:
            entry = line.split(',')
            nameList.append(entry[0]) 

        if name not in nameList:
            time_now= datetime.datetime.now()
            tstr=time_now.strftime('%H:%M:%S')
            dstr=time_now.strftime('%d/%m/%y')
            cv2.putText(img,"Attendance Marked ", (x+10,y-30), font,1, (255,50,25) ,2)
            f.writelines(f'{name},{tstr},{dstr}')
            saved=True

            if name in nameList:
                cam.release()
            f.close()
            
        if saved == True:
            cam.release()
            f.close()

while True:
    ret, img=cam.read()
    converted_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces=faceCascade.detectMultiScale(
        converted_img,scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW),int(minH) )
        ,
    )
    detect=False;

    for (x,y,w,h)in faces:

        cv2.rectangle(img,(x,y), (x+w,y+h) , (0,255,0), 2 )

        id,accuracy= recognizer.predict(converted_img[y:y+h , x:x+w ] ) 

        if ( accuracy<100 ):
            id= name[id]
            accuracy="  {0}%".format(round(100- accuracy))
            attendence(name[1])
            detect=True
            
            
        else:
            id="unknown"
            accuracy ="  {0}%".format(round( 100-accuracy ) )
        
        cv2.putText(img,str(id), (x+10,y-65 ), font,1, (255,50,25) ,2  )
        cv2.putText(img,str(accuracy), (x+5,y-5 ), font,1, (255,20,255) ,1 )
        if detect == True:
                break;

    cv2.imshow('camera',img)

    k=cv2.waitKey(10) &0xff
    if k== 27:
        break

print("Recogonistion Done")
cam.release()
cam.distroyAllWindows()

