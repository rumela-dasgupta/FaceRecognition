# import libraries 
from deepface import DeepFace 
import cv2 
from datetime import datetime 
import pickle 
 
 
 
def train(): 
    d={} 
    l=[] 
    fin=open("v.dat","ab") 
    cam = cv2.VideoCapture(0) 
    c=input("Enter visitor serial no:") 
    name=input("Enter name:") 
    no=input("Enter contact number:") 
    purpose=input("Enter purpose of visit:") 
    l.extend([name,no,purpose]) 
    now = datetime.now() 
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S") 
    l.append(dt_string) 
    for i in range(4,7): 
        t="f"+str(c)+str(i)+".png" 
        print("Capturing image... when you are ready press Q") 
        while(True): 
            result, image = cam.read() 
            cv2.imshow(name+str(i), image) 
            if cv2.waitKey(20) & 0xFF==ord('q'): 
                break 
                
        cv2.imwrite(t,image) 
        cv2.waitKey(0) 
        cv2.destroyWindow(name+str(i)) 
        l.append(t) 
    d[c]=l 
    pickle.dump(d,fin) 
    fin.close() 
    cam.release() 
    for i in range(4,7): 
        image=cv2.imread(d[c][i]) 
        cv2.imshow(name+str(i), image) 
        cv2.waitKey(0) 
        cv2.destroyWindow(name+str(i)) 
    cam.release()     
 
def RECOGNITION(): 
    try: 
        fout=open("v.dat","rb") 
        d={} 
        cam = cv2.VideoCapture(0) 
        print("Visitor") 
        print("Capturing image... when you are ready press Q") 
        while(True): 
            result, image = cam.read() 
            cv2.imshow("Visitor", image) 
            if cv2.waitKey(20) & 0xFF==ord('q'): 
                break 
     
     
        cv2.imwrite("Visitor.png",image) 
        cv2.waitKey(0) 
        cv2.destroyWindow("Visitor") 
        img1=image 
        tp=0 
        try: 
            while True: 
                d=pickle.load(fout) 
                tp=0 
                for k,v in d.items(): 
                    tp=0 
                    for i in range(4,7): 
                        img2=cv2.imread(v[i]) 
                        result=DeepFace.verify(img1,img2) 
                        if(result['distance']<0.1): 
                            tp=1 
                            raise EOFError 
        except EOFError: 
            fout.close() 
            if tp==1: 
                print("VISITOR - REVISITING") 
                print("Visitor's name:", v[0]) 
                print("Visitor's contact number:", v[1]) 
                print("Prior purpose of visit:", v[2]) 
                print("Previous visit on and at", v[3])      
            else: 
                print("FIRST TIME VISIT") 
                print("Accepting data and capturing image...") 
                cam.release() 
                 
    except FileNotFoundError: 
                train() 
         
     
############MAIN############### 
while True:  
    RECOGNITION() 
    ch=input("Any more visitors?  Y/N") 
    if ch.upper()=="N": 
        break