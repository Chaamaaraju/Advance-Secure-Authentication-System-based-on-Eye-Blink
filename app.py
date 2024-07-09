from flask_socketio import SocketIO, send, join_room
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for
import os
#import StockPrice as SP
import re

import pandas as pd
import numpy as np
import requests
import MySQLdb
import cv2
from PIL import Image, ImageTk

import pingenerate as pingen
import random as r
import pyotp
import time 

print(cv2.__version__)

mydb = MySQLdb.connect(host='localhost',user='root',passwd='root',db='banking')
conn = mydb.cursor()

recognizer = cv2.face.LBPHFaceRecognizer_create()

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale=1
fontColor=(255,255,255)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
clientid=0
data=[]
data1=[]

otp="0000"
totp = pyotp.TOTP('base32secret3232')

def otpgen():
        otp=""
        for i in range(4):
                otp+=str(r.randint(1,9))
        print ("Your One Time Password is ")
        print (otp)
        return otp
        
@app.route('/')
#loading login page or main chat page
def index():
        if not session.get('logged_in'):
                return render_template("login.html")
        else:
                return render_template('main.html')


@app.route('/registerpage',methods=['POST'])
def reg_page():
    return render_template("register.html")
@app.route('/forgetpasspage',methods=['POST'])
def fpass_page():
    return render_template("forgetpass.html")
        
@app.route('/loginpage',methods=['POST'])
def log_page():
    return render_template("login.html")
    

    
    
@app.route('/AddClient',methods=['POST'])
def main_page():
        cid=request.form['cid']
        name=request.form['name']
        fathername=request.form['fname']
        email=request.form['email']
        mob=request.form['mob']
        address=request.form['address']
        city=request.form['city']
        state=request.form['state']
        pnum=request.form['pnum']
        anum=request.form['anum']
        cmd="SELECT * FROM client WHERE cid='"+cid+"'"
        print(cmd)
        conn.execute(cmd)
        cursor=conn.fetchall()
        isRecordExist=0
        for row in cursor:
                isRecordExist=1
        if(isRecordExist==1):
                print("Client Id Already Exists")
                return render_template("main.html",message="Client ID Already Exists")
        else:
                print("insert")
                cmd="INSERT INTO client Values('"+str(cid)+"','"+str(name)+"','"+str(fathername)+"','"+str(email)+"','"+str(mob)+"','"+str(address)+"','"+str(city)+"','"+str(state)+"','"+str(pnum)+"','"+str(anum)+"')"
                print(cmd)
                print("Inserted Successfully")
                conn.execute(cmd)
                mydb.commit()
                return render_template("main.html",message="Inserted SuccesFully")

@app.route('/UpdateClient',methods=['POST'])
def UpdateClient():
        cid=request.form['cid']
        name=request.form['name']
        fathername=request.form['fname']
        email=request.form['email']
        mob=request.form['mob']
        address=request.form['address']
        city=request.form['city']
        state=request.form['state']
        pnum=request.form['pnum']
        anum=request.form['anum']
        cmd="update client set cid='"+str(cid)+"',name='"+str(name)+"',fathername='"+str(fathername)+"',email='"+str(email)+"',mobile='"+str(mob)+"',address='"+str(address)+"',city='"+str(city)+"',state='"+str(state)+"',pnum='"+str(pnum)+"',anum='"+str(anum)+"' where cid='"+str(cid)+"'"
        print(cmd)
        conn.execute(cmd)
        mydb.commit()
        print("Update Successfully")
        return render_template("ViewClient.html",message="Update SuccesFully")
   

@app.route('/ViewClient',methods=['POST'])
def ViewClient():
        cid=request.form['cid']
        cmd="SELECT * FROM client WHERE cid='"+str(cid)+"'"
        conn.execute(cmd)
        cursor=conn.fetchall()
        print("length",len(cursor))
        if len(cursor)>0:
                results=[]
                for row in cursor:
                        print(row)
                results.append(row[0])
                results.append(row[1])
                results.append(row[2])
                results.append(row[3])
                results.append(row[4])
                results.append(row[5])
                results.append(row[6])
                results.append(row[7])
                results.append(row[8])
                results.append(row[9])
                print("length of row",len(row))
        
                return render_template("ViewClient.html",results=results)
        else:
                return render_template("ViewClient.html",message="No Records Found")
                

@app.route('/StartCamera',methods=['POST'])
def StartCamera():
        cid=request.form['cid']
        print("cid",cid)
        sampleNum=0
        cam = cv2.VideoCapture(0)
    
    
        while True:
                ret, frame = cam.read()
                if ret == True:
                        #cv2.imwrite("static/data/"+cid +".jpg", frame)
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = faceCascade.detectMultiScale(
                            frame,
                            scaleFactor=1.1,
                            minNeighbors=5,
                            minSize=(30, 30)
                            #flags=cv2.cv.CV_HAAR_SCALE_IMAGE
                        )
                        for (x,y,w,h) in faces:
                                x1=x-60
                                y1=y-60
                                w1=x+w+40
                                h1=y+h+40
                                crop_img = frame[x1:h1,y1:w1]
                                try:
                                        cv2.imwrite("static/data/"+cid +".jpg", crop_img)
                                except:
                                        pass
                                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                                sampleNum=sampleNum+1
                                print(cid +'.'+ str(sampleNum))
                                cv2.imwrite("dataSet/User."+cid +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                                
                                #cv2.imshow('frame',img)
                # Display the resulting frame
                cv2.imshow('Video', frame)
                if cv2.waitKey(1)==ord('q'):
                        break
        cam.release()
        cv2.destroyAllWindows()
        
        return render_template("register.html",message="Snap Taken SuccesFully")


@app.route('/Training',methods=['POST'])
def train():
    print("Train Images")
    #path=request.form['path']
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    def getImagesAndLabels(path):
        print(path)
        imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
        
        faceSamples=[]
        
        Ids=[]
        
        for imagePath in imagePaths:
            pilImage=Image.open(imagePath).convert('L')
            imageNp=np.array(pilImage,'uint8')
            Id=int(os.path.split(imagePath)[-1].split(".")[1])
            faces=faceCascade.detectMultiScale(imageNp)
            for (x,y,w,h) in faces:
                faceSamples.append(imageNp[y:y+h,x:x+w])
                Ids.append(Id)
        return faceSamples,Ids
    
    
    faces,Ids = getImagesAndLabels("dataset")
    recognizer.train(faces, np.array(Ids))
    recognizer.write('trainer/trainer.yml')
    res = "Image Train is Finished"
    return render_template("login.html",message="Training SuccesFully Finished")


def getProfile(Id):
        data=[]
        cmd="SELECT * FROM login WHERE cid="+str(Id)
        #print(cmd)
        conn.execute(cmd)

        cursor=conn.fetchall()
        #print(cursor)
        profile=None
        for row in cursor:
                #print(row)
                
                profile=row[1]

        print("data value",data)
        
        
        conn.close
        return profile
        
        
def find_faces(image_path):

        recognizer.read('trainer/trainer.yml')
        image = cv2.imread(image_path)
        # Make a copy to prevent us from modifying the original
        color_img = image.copy()
        filename = os.path.basename(image_path)
        # OpenCV works best with gray images
        gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)
        # Use OpenCV's built-in Haar classifier
        faces=faceCascade.detectMultiScale(gray_img, 1.2,5)
        print('Number of faces found: {faces}'.format(faces=len(faces)))
        if len(faces)==0:
                return 0
        else:
                for (x, y, w, h) in faces:
                        #cv2.rectangle(color_img, (x, y), (x+width, y+height), (0, 255, 0), 2)
                        cv2.rectangle(color_img,(x,y),(x+w,y+h),(225,0,0),2)
                        Id, conf = recognizer.predict(gray_img[y:y+h,x:x+w])
                        print(Id)
                        print(conf)
                        if(20<conf and conf<80):
                                #data1=data
                                profile=getProfile(Id)
                                print("cliend id",Id)
                                print("Name",profile)                   
                                cv2.putText(color_img,str(Id), (x,y+h),font, fontScale, fontColor)
                                cv2.putText(color_img,str(profile), (x,y+h+30),font, fontScale, fontColor)
        
                                clientid=Id
                                #print("clientid",clientid)
                        else:
                                Id=0
                                #profile=getProfile(Id)
                                cv2.putText(color_img,'0', (x,y+h),font, fontScale, fontColor)
                                cv2.putText(color_img,'UNKNOWN', (x,y+h+30),font, fontScale, fontColor)
                        cv2.imshow(filename, color_img)
                        if cv2.waitKey(1)==ord('q'):
                                return Id
                        else:
                                return 0
        
@app.route('/Detect',methods=['POST'])
def detection():
    print("detection")
    clientid=0
    
    cam = cv2.VideoCapture(0)
    while True:
        return_value, image = cam.read()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(image,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
        for (x,y,w,h) in faces:
                cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.imshow('Video', image)
                cv2.imwrite('image.png', image)
                print("Newdata ",data)

                r=find_faces('image.png')
                print("r value",r)
                #r=int(r)
                if r!= "":
                        if r>0:
                                cam.release()
                                cv2.destroyAllWindows()
                                print("Now r value",r)
                                cmd="SELECT * FROM login WHERE cid="+str(r)
                                conn.execute(cmd)
                                cursor=conn.fetchall()
                                print(cursor)
                                results=[]
                                for row in cursor:
                                        print(row)
                                results.append(row[0])
                                results.append(row[1])
                                results.append(row[2])
                                results.append(row[3])
                                results.append(row[4])

                                print(results)                                          

                                return render_template("login.html",results=results)
                else:
                        if r>0:
                                cam.release()
                                cv2.destroyAllWindows()
                                print("now r value",r)
                                cmd="SELECT * FROM client WHERE cid="+str(r)
                                conn.execute(cmd)
                                cursor=conn.fetchall()
                                print(cursor)
                                results=[]
                                for row in cursor:
                                        print(row)
                                results.append(row[0])
                                results.append(row[1])
                                results.append(row[2])
                                results.append(row[3])
                                results.append(row[4])
                                print(results)                                          

                                return render_template("login.html",results=results)
                        
    

@app.route('/Addpin',methods=['POST'])
def addpin():
        print("addpin")
        cid=request.form['cid']
        pin1=request.form['pin']
        results=[]
        
        pin=str(pin1)+pingen.process()
        print(pin)
        print("len",len(str(pin)))
        while len(pin)<4:
                pin=str(pin)+pingen.process()
                print(pin)
                #render_template("login.html",results=results,pin=pin)
                
        results.append(cid)
        print(results)
        return render_template("login.html",results=results,pin=pin)
    
@app.route('/register',methods=['POST'])
def reg():
        name=request.form['name']
        cid=request.form['cid']
        pin=request.form['pin']
        email=request.form['emailid']
        mobile=request.form['mobile']
        cmd="SELECT * FROM login WHERE cid='"+cid+"'"
        print(cmd)
        conn.execute(cmd)
        cursor=conn.fetchall()
        isRecordExist=0
        for row in cursor:
                isRecordExist=1
        if(isRecordExist==1):
                print("Username Already Exists")
                return render_template("register.html",message="Client id Already Exists")
        else:
                print("insert")
                cmd="INSERT INTO login Values('"+str(cid)+"','"+str(name)+"','"+str(pin)+"','"+str(email)+"','"+str(mobile)+"')"
                print(cmd)
                print("Inserted Successfully")
                conn.execute(cmd)
                mydb.commit()
                return render_template("register.html",message="Inserted SuccesFully")
@app.route('/changepin',methods=['POST'])
def upatepin():
        #name=request.form['name']
        cid=request.form['cid']
        pin=request.form['pin']
        cpin=request.form['cpin']
        #mobile=request.form['mobile']
        cmd="SELECT * FROM login WHERE cid='"+cid+"'"
        print(cmd)
        conn.execute(cmd)
        cursor=conn.fetchall()
        isRecordExist=0
        for row in cursor:
                isRecordExist=1
        if(isRecordExist==1):
                print("Username Already Exists")
                cmd="UPDATE login SET pin='"+str(pin)+"'WHERE cid='"+cid+"'"
                print(cmd)
                print("Inserted Successfully")
                
                conn.execute(cmd)
                mydb.commit()
                return render_template("login.html",message="PIN Updated")
                
        else:
                return render_template("forgetpass.html",message="Client id not Exist")

    
@app.route('/login1',methods=['POST'])
def log_in1():
        global otp
        otpvalue=request.form['otp']
        print(otp)
        print(otpvalue)
        if otp==otpvalue:
                session['logged_in'] = True
                session['cid'] = request.form['cid']
                return redirect(url_for('index'))
        else:
                return render_template("login.html",message="Check OTP Value")
@app.route('/fpass1',methods=['POST'])
def fpass_in1():
        global otp
        otpvalue=request.form['otp']
        print(otp)
        print(otpvalue)
        if otp==otpvalue:
                results=[]
                #session['logged_in'] = True
                session['cid'] = request.form['cid']
                cid=request.form['cid']
                results.append(cid)
                return render_template("changepin.html",results=results)
        else:
                return render_template("forgetpass.html",message="Check OTP Value")
                

    
@app.route('/login',methods=['POST'])
def log_in():
        global otp
        #complete login if name is not an empty string or doesnt corss with any names currently used across sessions
        if request.form['cid'] != None and request.form['cid'] != "" and request.form['pin'] != None and request.form['pin'] != "":
                cid=request.form['cid']
                pin=request.form['pin']
                cmd="SELECT cid,pin,mobile FROM login WHERE cid='"+cid+"' and pin='"+pin+"'"
                print(cmd)
                conn.execute(cmd)
                cursor=conn.fetchall()
                isRecordExist=0
                for row in cursor:
                        isRecordExist=1
                        
                if(isRecordExist==1):
                        mobile=row[2]
                        results=[]
                        results.append(cid)
                        results.append(pin)
                        print(otp)
                        otp=totp.now()
                        print(otp)
                        url = "https://www.fast2sms.com/dev/bulk"
                        print(mobile)
                        
                        msg="Your Otp Number Is " + otp
                        payload = "sender_id=FSTSMS&message="+msg+"&language=english&route=p&numbers="+mobile
                        headers = {'authorization':"bM9ryo3h6E0DdJjikwWq5FIncGY1TVK4Og7sZQHRALNz8XufltTsiAp0g72WNrYO3aewR41DVztHbu5d",'Content-Type': "application/x-www-form-urlencoded",'Cache-Control': "no-cache",}
                        response = requests.request("POST", url, data=payload, headers=headers)
                        print(response.text)

                        #time.sleep(30)
                        #session['logged_in'] = True
                        # cross check names and see if name exists in current session
                        #session['cid'] = request.form['cid']
                        #return redirect(url_for('index'))
                        return render_template("otp.html",results=results)
                else:
                        return render_template("login.html",message="Check Rollnumber and Pin Number")

        return redirect(url_for('index'))
@app.route('/fpass',methods=['POST'])
def fpass_in():
        global otp
        #complete login if name is not an empty string or doesnt corss with any names currently used across sessions
        if request.form['name'] != None and request.form['name'] != "" and request.form['cid'] != None and request.form['cid'] != "":
                cid=request.form['name']
                pin=request.form['cid']
                cmd="SELECT cid,pin,mobile FROM login WHERE cid='"+pin+"'"
                print(cmd)
                conn.execute(cmd)
                cursor=conn.fetchall()
                isRecordExist=0
                for row in cursor:
                        isRecordExist=1
                        
                if(isRecordExist==1):
                        mobile=row[2]
                        results=[]
                        results.append(cid)
                        results.append(pin)
                        print(otp)
                        otp=totp.now()
                        print(otp)
                        url = "https://www.fast2sms.com/dev/bulk"
                        print(mobile)
                        
                        msg="Your Otp Number Is " + otp
                        payload = "sender_id=FSTSMS&message="+msg+"&language=english&route=p&numbers="+mobile
                        headers = {'authorization':"bM9ryo3h6E0DdJjikwWq5FIncGY1TVK4Og7sZQHRALNz8XufltTsiAp0g72WNrYO3aewR41DVztHbu5d",'Content-Type': "application/x-www-form-urlencoded",'Cache-Control': "no-cache",}
                        response = requests.request("POST", url, data=payload, headers=headers)
                        print(response.text)

                        #time.sleep(30)
                        #session['logged_in'] = True
                        # cross check names and see if name exists in current session
                        #session['cid'] = request.form['cid']
                        #return redirect(url_for('index'))
                        return render_template("otp1.html",results=results)
                else:
                        return render_template("forgetpass.html",message="Check Rollnumber and Pin Number")

        return redirect(url_for('index'))
        
@app.route("/logout")
def log_out():
    session.clear()
    return redirect(url_for('index'))
    
@app.route("/AddClient")
def addClient():
    return render_template("main.html")

@app.route("/TrainingPage")
def TrainingPage():
    return render_template("Training.html")
   
@app.route("/ViewClientPage")
def ViewClientPage():
    return render_template("ViewClient.html")
  
@app.route("/ReportPage")
def ReportPage():
        sql="select * from client"
        conn.execute(sql)
        results = conn.fetchall()
        return render_template("Report.html",result=results)  
        
    
# /////////socket io config ///////////////
#when message is recieved from the client    
@socketio.on('message')
def handleMessage(msg):
    print("Message recieved: " + msg)
 
# socket-io error handling
@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    pass


  
  
if __name__ == '__main__':
    socketio.run(app,debug=True,host='127.0.0.1', port=4000)
