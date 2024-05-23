import time
import logging, logging.handlers
import ctypes
import subprocess
import sys
import configparser
import locker

config = configparser.ConfigParser()
config.read('config.ini')
LOG_FILENAME = '..\logs\LockAway_logs.out'
logger = logging.getLogger(__name__)  
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=5, backupCount=0)
logger.addHandler(handler)

def main() -> None:
    if not sys.platform.startswith('win32'):
        logger.error('Incompatible OS')
        quit()
    
    time_limit = int(config['CONFIG']['LockoutInterval'])
    locker.run(time_limit,"haarcascade_frontalface_default.xml")


if __name__ == "__main__":
    main()