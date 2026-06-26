import random
import time
import logging

def random_delay(min_delay=1, max_delay=5):
    delay = random.uniform(min_delay, max_delay)
    logging.debug(f"Sleeping for {delay:.2f} seconds...")
    time.sleep(delay)

def setup_logging(log_file=None):
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file, encoding='utf-8'))
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
