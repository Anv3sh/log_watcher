# log the current time every 5 secs into the log file
import datetime
import pytz
import time


FILE = "test.log"

def logger(filename=FILE):
    with open(filename,"a") as f:
        while True:
            current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            print(current_time)
            f.write(f"Logged at {current_time}.\n")
            f.flush() # to force write before closing the file
            time.sleep(10)
            
logger("test.log")