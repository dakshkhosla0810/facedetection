import cv2
cam= cv2.VideoCapture(0)
cam.set(3,640) #width
cam.set(4,480) #height

detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

faceid=input("ENter userId:")
count=0

while True:
    ret,img=cam.read()
    converted_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(converted_img,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y), (x+w, y+h) , (255,0,0), 2 )
        count+=1

        cv2.imwrite("samples/faces." + str(faceid)+ "."+ str(count)
        + ".jpg",converted_img[y:y+h,x:x+w] )

        cv2.imshow("image",img)  #used to show image on screen
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        break
    elif count >= 50:
        break
print("Face Has been Scanned Successfully ...")
cam.realease()
cv2.destroyAllWindows()

