import logging
import random
from datetime import datetime
from .utils import random_delay
from .sender import MessageSender
from .discovery import ContentDiscovery

class StreakManager:
    def __init__(self, page, config, state_manager, usernames):
        self.page = page
        self.config = config
        self.state_manager = state_manager
        self.usernames = usernames
        self.sender = MessageSender(page)
        self.discovery = ContentDiscovery(page, config.get("keywords", []))

    def run(self):
        today = datetime.now().strftime("%Y-%m-%d")
        processed_count = 0
        daily_limit = self.config.get("daily_limit", 10)
        
        for username in self.usernames:
            if processed_count >= daily_limit:
                logging.info(f"Daily limit of {daily_limit} reached. Stopping.")
                break
            
            # Check if already processed today
            last_sent = self.state_manager.get_last_sent(username)
            if last_sent == today:
                logging.info(f"Skipping {username}, already processed today.")
                continue
            
            # Determine message
            message = self.get_message()
            if not message:
                logging.warning(f"No message generated for {username}. Skipping.")
                continue
            
            # Send message
            if self.sender.find_user_chat(username):
                if self.sender.send_message(message):
                    logging.info(f"Successfully sent message to {username}.")
                    self.state_manager.update_state(username, today)
                    processed_count += 1
                    random_delay(5, 15) # Delay between users
                else:
                    logging.warning(f"Failed to send message to {username}.")
            else:
                logging.warning(f"Could not find chat for {username}.")
            
            random_delay(2, 5)
        
        logging.info(f"Run complete. Processed {processed_count} users.")

    def get_message(self):
        if self.config.get("enable_discovery", False):
            video_link = self.discovery.discover_video_link()
            if video_link:
                return "https://www.tiktok.com" + video_link
        
        # Default to text message
        texts = self.config.get("texts", ["."])
        return random.choice(texts)
