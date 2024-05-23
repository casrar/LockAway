import time
import logging, logging.handlers
import ctypes
import subprocess
import cv2
from FacialRecognizer import FacialRecognizer

def run(time_limit: int, cascade: str):
    video_capture = cv2.VideoCapture(0)
    start = time.time()
    classifier = cv2.CascadeClassifier(
        cv2.data.haarcascades + cascade)
    fr = FacialRecognizer(classifier)
    while True:
        current_interval = time.time() - start
        result, frame = video_capture.read()  # read frames from the video
        if result is False:
            break  # terminate the loop if the frame is not read successfully

        # if screen is already locked then skip
        if curr_user_desktop_locked():
            start = time.time()
            current_interval = 0
            continue

        # if face is on screen,set interval to 0 start timer again
        if fr.detect_facial_presence(frame):
            start = time.time()
            current_interval = 0
            continue

        # once face leaves screen, start timer
        if current_interval > time_limit:
            start = time.time()
            current_interval = 0
            ctypes.windll.user32.LockWorkStation()

    video_capture.release()
    cv2.destroyAllWindows()

def curr_user_desktop_locked() -> bool:  
    process_name='LogonUI.exe'
    callall='TASKLIST'
    outputall=subprocess.check_output(callall)
    outputstringall=str(outputall)
    if process_name in outputstringall:
        return True
    return False