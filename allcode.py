from asyncore import write
from cgitb import text
from tkinter.font import names
from turtle import width
from typing import Text
from unicodedata import name
import cv2

from array import array
import numpy as np
from PIL import Image
import os
import csv 
import datetime 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import csv 
import datetime 
import time

def face_scanning(rollno):

                #face_generator py
 cam= cv2.VideoCapture(0)
 cam.set(3,640) #width
 cam.set(4,480) #height
 
 detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 
 count=0
 
 while True:
     ret,img=cam.read()
     converted_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
     faces=detector.detectMultiScale(converted_img,1.3,5)
     for (x,y,w,h) in faces:
         cv2.rectangle(img,(x,y), (x+w, y+h) , (255,0,0), 2 )
         count+=1
 
         cv2.imwrite("samples/faces." + str(rollno)+ "."+ str(count)
         + ".jpg",converted_img[y:y+h,x:x+w] )
 
         cv2.imshow("image",img)  #used to show image on screen
     if cv2.waitKey(20) & 0xFF == ord('q'):
         break
     elif count >= 50:
         break
 print("Face Has been Scanned Successfully ...")
 cv2.destroyAllWindows()
 cam.release() 
 trainer_faces(rollno)

        
def trainer_faces(rollno):
    
    path ="samples"
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
     
    def img_lables(path):
         columns = ['SERIAL NO.', '', 'ID', '', 'NAME']
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
     
    print("Done  now we can recognize your face ")
    

def attendance_recogonistion(name,rollno):

 
 recognizer = cv2.face.LBPHFaceRecognizer_create()
 recognizer.read('Trainer/trainer.yml')
 cascadePath = 'haarcascade_frontalface_default.xml'
 faceCascade=cv2.CascadeClassifier(cascadePath)
 
 font = cv2.FONT_HERSHEY_SIMPLEX 
 

 
 
 cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)
 cam.set(3,640)
 cam.set(4,480)
 
 minW=0.1*cam.get(3)
 minH=0.1*cam.get(4)
 
 def attendence(name):
     with open ('StudentDetail/Attendance.csv','r+') as f:
         saved=False
         fobj=csv.writer(f)
         fobj.writerow(['Name','Time','Date'])
         mydataList=f.readlines()
         nameList=[]
         alldetails=[]
         for line in mydataList:
             entry = line.split(',')
             nameList.append(entry[0])
 
         if name not in nameList:
             time_now= datetime.datetime.now()
             tstr=time_now.strftime('%H:%M:%S')
             dstr=time_now.strftime('%d/%m/%y')
             alldetails=[name,tstr,dstr]
             fobj.writerow(alldetails)
             cv2.putText(img,"Attendance Marked ", (x+10,y-30), font,1, (255,50,25) ,2)
             saved= True
           
             if saved == True:
              cam.release()
              f.close()
             #time.sleep(10)
 
             if name in nameList:
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
             
             accuracy="  {0}%".format(round(100- accuracy))
             attendence(name)
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
 




 
def clear():
    txt.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)

def clear2():
    txt2.delete(0, 'end')
    res = "1)Take Images  >>>  2)Save Profile"
    message1.configure(text=res)


window =tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Attendance System")
window.configure(background='#262523')




frame1 = tk.Frame(window, bg="#00aeff")
frame1.place(relx=0.11, rely=0.17, relwidth=0.39, relheight=0.80)

frame2 = tk.Frame(window, bg="#00aeff")
frame2.place(relx=0.51, rely=0.17, relwidth=0.38, relheight=0.80)

message3 = tk.Label(window, text="Face Recognition Based Attendance System" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

head2 = tk.Label(frame2, text="                       For New Registrations                       ", fg="black",bg="#3ece48" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=0)

head1 = tk.Label(frame1, text="                       For Already Registered                       ", fg="black",bg="#3ece48" ,font=('times', 17, ' bold ') )
head1.place(x=0,y=0)

lbl = tk.Label(frame2, text="Enter ID",width=20  ,height=1  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold ') )
lbl.place(x=80, y=55)

txt = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold '))
txt.place(x=30, y=88)

lbl2 = tk.Label(frame2, text="Enter Name",width=20  ,fg="black"  ,bg="#00aeff" ,font=('times', 17, ' bold '))
lbl2.place(x=80, y=140)

txt2 = tk.Entry(frame2,width=32 ,fg="black",font=('times', 15, ' bold ')  )
txt2.place(x=30, y=173)

message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="#00aeff" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
message1.place(x=7, y=230)

message = tk.Label(frame2, text="" ,bg="#00aeff" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=7, y=450)

lbl3 = tk.Label(frame1, text="Attendance",width=20  ,fg="black"  ,bg="#00aeff"  ,height=1 ,font=('times', 17, ' bold '))
lbl3.place(x=100, y=115)

res=0
exists = os.path.isfile("StudentDetail\Attendance.csv")
if exists:
    with open("StudentDetail\Attendance.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        for l in reader1:
            res = res + 1
    res = (res // 2) - 1
    csvFile1.close()
else:
    res = 0
message.configure(text='Total Registrations till now  : '+str(res))


################## TREEVIEW ATTENDANCE TABLE ####################

tv= ttk.Treeview(frame1,height =13,columns = ('name','time','date'))
tv.column('#0',width=82)
tv.column('name',width=130)
tv.column('time',width=133)
tv.column('date',width=133)

tv.grid(row=2,column=0,padx=(0,0),pady=(150,0),columnspan=4)

tv.heading('#0',text ='ID')
tv.heading('name',text ='Name')
tv.heading('time',text ='Time')
tv.heading('date',text ='Date')


def display_csv_data():
    with open('StudentDetail/Attendance.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            name = row['Name']
            time = row['Time']
            date = row['Date']
            tv.insert("", 0, values=(name,time,date))

###################### SCROLLBAR ################################

scroll=ttk.Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(150,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)

def get():
    rollno_get=txt.get()
    name_get=txt2.get()
    face_scanning(rollno_get)
    
def name_():
    name_get=txt2.get()
    rollno_get=txt.get()
    attendance_recogonistion(name_get,rollno_get)
    


    
clearButton = tk.Button(frame2, text="Clear", command=clear  ,fg="black"  ,bg="#ea2a2a"  ,width=11 ,activebackground = "white" ,font=('times', 11, ' bold '))
clearButton.place(x=335, y=86)
clearButton2 = tk.Button(frame2, text="Clear", command=clear2  ,fg="black"  ,bg="#ea2a2a"  ,width=11 , activebackground = "white" ,font=('times', 11, ' bold '))
clearButton2.place(x=335, y=172)    

takeImg = tk.Button(frame2, text="Take Images",command= get, fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
takeImg.place(x=30, y=300)

saveprofile = tk.Button(frame2, text="Save Profile",command=name_, fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
saveprofile.place(x=30, y=350)

markattendance = tk.Button(frame2, text="read Profile",command=display_csv_data, fg="white"  ,bg="blue"  ,width=34  ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
markattendance.place(x=30, y=400)

window.mainloop()



