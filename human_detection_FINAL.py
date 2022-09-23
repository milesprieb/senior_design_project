from ast import Continue
import cv2
import serial,time
import numpy as np

#Set pixel color values of target
lowerbound = np.array([0, 60, 240])
upperbound = np.array([60, 100, 255])

def testColorMask(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    targetImg = cv2.inRange(hsv, lowerbound, upperbound)

    cv2.imshow('target color', targetImg)

    #Test if any pixels are white (meaning they're the target color)
    # return np.any(targetImg == 255)
    num = cv2.countNonZero(targetImg)
    print(num)

    if num > 15:
        return True
    else:
        return False

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
cap=cv2.VideoCapture(1)
#fourcc= cv2.VideoWriter_fourcc(*'XVID')
ArduinoSerial=serial.Serial('com5',9600,timeout=0.1)
fourcc= cv2.VideoWriter_fourcc(*'XVID')
out= cv2.VideoWriter('human_detection_noadjustments.avi',fourcc,10.0,(640,480))
time.sleep(1)
i = 0
tmp = 0
while cap.isOpened():
    ret, frame= cap.read()
    frame=cv2.flip(frame,1)  #mirror the image
    #frame1 = frame.copy()
    if frame is None:
        print("Wrong path")
    else:
        frame = cv2.resize(frame, (640, 480))
    #print(frame.shape)
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    human, weights = hog.detectMultiScale(frame,winStride=(8,8))  #detect the human
    human  = np.array([[x, y, x + w, y + h] for (x, y, w, h) in human])
    #print(human)
    #print(type(human))
    #print(human.size)

    if (len(human) == 0): 
        tmp += 1
        if (tmp == 20):
            string = 'F'
            ArduinoSerial.flush()
            ArduinoSerial.write(string.encode('utf-8'))
            tmp = 0
            print("NO HUMAN")
    else:
        #print("HUMAN")

        #Only search in detected box of our image
        box = frame[human[0][1]:human[0][3], human[0][0]:human[0][2]]

        if testColorMask(box):
            string= ('X' + str(human[0][0]+human[0][2]//2)  + 'Y' + str(human[0][1]+human[0][3]//2))
            #print(string)
            ArduinoSerial.flush()
            ArduinoSerial.write(string.encode('utf-8'))

        #plot the center of the face
        cv2.circle(human,(human[0][0]+human[0][2]//2,human[0][1]+human[0][3]//2),2,(0,255,0),2)
        #plot the roi
        cv2.rectangle(frame, (human[0][0], human[0][1]), (human[0][2], human[0][3]), (0, 255, 0), 2)
        tmp = 0

    ArduinoSerial.flush()    

    #plot the squared region in the center of the screen
    cv2.rectangle(frame,(640//2-30,480//2-30),
                 (640//2+30,480//2+30),
                  (255,255,255),3)
    out.write(frame)
    cv2.imshow('img',frame)
    #cv2.imwrite('output_img.mp4',frame)

    #for testing purpose
    read= str(ArduinoSerial.readline(ArduinoSerial.inWaiting()))
    print('data from arduino:'+ read)

    # press q to Quit
    if cv2.waitKey(10)&0xFF== ord('q'):
        string = 'F'
        ArduinoSerial.flush()
        ArduinoSerial.write(string.encode('utf-8'))
        break
cap.release()
cv2.destroyAllWindows()