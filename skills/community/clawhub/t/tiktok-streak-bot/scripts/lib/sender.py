import logging
import random
from .utils import random_delay

class MessageSender:
    def __init__(self, page):
        self.page = page
        self.selectors = {
            "search_input": 'input[type="search"], input[type="text"]',
            "chat_item": 'div[data-e2e="chat-item"]',
            "message_box": 'div[contenteditable="true"]',
            "send_button": 'button[data-e2e="chat-send"]',
            "user_message_button": "a.link-a11y-focus:nth-child(2) > div:nth-child(1) > button:nth-child(1)",
            "captcha_box": "captcha-verify-container-main-page",
            "captcha_close_button": "#captcha_close_button"
        }

    def find_user_chat(self, username):
        logging.info(f"Searching for user: {username}...")
        try:
            self.page.goto(f"https://www.tiktok.com/@{username}", wait_until="networkidle")
            random_delay(2, 4)
            
            # Check if captcha box is exists
            captcha_sel = f"#{self.selectors.get('captcha_box', 'captcha-verify-container-main-page')}"
            if self.page.locator(captcha_sel).count() > 0 or self.page.locator(".captcha-verify-container").count() > 0:
                logging.warning("Captcha detected! Reloading browser with new user agent in incognito mode...")
                
                # close captcha
                self.page.click(self.selectors["captcha_close_button"])
                logging.info("Captcha closed.")
                random_delay(2, 4)
            
            # click message button with force to bypass TUXModal-overlay
            self.page.click(self.selectors["user_message_button"], force=True)
            random_delay(2, 4)
            
            # Wait for message box to confirm redirection to chat
            # Usually the URL changes to /messages?user_id=...
            if self.page.locator(self.selectors["message_box"]).is_visible():
                return True
            else:
                logging.warning(f"Could not reach chat for {username}.")
                return False
        except Exception as e:
            logging.error(f"Error finding chat for {username}: {e}")
            return False

    def send_message(self, message):
        logging.info(f"Sending message: {message}...")
        try:
            self.page.fill(self.selectors["message_box"], message)
            random_delay(0.5, 1.5)
            self.page.keyboard.press("Enter")
            random_delay(1, 2)
            return True
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            return False
