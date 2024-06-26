import time
import logging, logging.handlers
import ctypes
import subprocess
import sys
import cv2
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
LOG_FILENAME = '..\logs\LockAway_logs.out'
logger = logging.getLogger(__name__)  
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=5, backupCount=0)
logger.addHandler(handler)

face_classifier = cv2.CascadeClassifier(
cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
def main() -> None:
    if not sys.platform.startswith('win32'):
        logger.error('Incompatible OS')
        quit()
    run()

def run():
    video_capture = cv2.VideoCapture(0)
    start = time.time()
    time_limit = int(config['CONFIG']['LockoutInterval'])
    while True:
        current_interval = time.time() - start
        print(current_interval)

        result, frame = video_capture.read()  # read frames from the video
        if result is False:
            break  # terminate the loop if the frame is not read successfully

        # if screen is already locked then skip
        if curr_user_desktop_locked():
            start = time.time()
            current_interval = 0
            print('Locked')
            continue

        # if face is on screen,set interval to 0 start timer again
        if detect_face(frame):
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

def detect_face(frame) -> bool:
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    if len(faces) > 0:
        return True
    return False


if __name__ == "__main__":
    main()