import logging
import time
from datetime import datetime

class Scheduler:
    def __init__(self, target_time_hm):
        self.target_time_hm = target_time_hm

    def wait_until_target_time(self):
        target_hour, target_minute = self.target_time_hm
        logging.info(f"Waiting until {target_hour:02d}:{target_minute:02d} to run...")
        
        while True:
            now = datetime.now()
            if now.hour == target_hour and now.minute == target_minute:
                logging.info("Target time reached. Starting execution.")
                break
            time.sleep(30) # Check every 30 seconds
