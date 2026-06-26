import logging
import random
from .utils import random_delay

class ContentDiscovery:
    def __init__(self, page, keywords):
        self.page = page
        self.keywords = keywords
        self.selectors = {
            "captcha_box": "captcha-verify-container-main-page",
            "captcha_close_button": "#captcha_close_button"
        }

    def discover_video_link(self):
        keyword = random.choice(self.keywords)
        logging.info(f"Discovering content for tag: {keyword}...")
        try:
            search_url = f"https://www.tiktok.com/tag/{keyword}"
            self.page.goto(search_url, wait_until="networkidle")
            random_delay(3, 5)
            # check if captcha is exists
            captcha_sel = f"#{self.selectors.get('captcha_box', 'captcha-verify-container-main-page')}"
            if self.page.locator(captcha_sel).count() > 0 or self.page.locator(".captcha-verify-container").count() > 0:
                logging.warning("Captcha detected! Reloading browser with new user agent in incognito mode...")
                # close captcha
                self.page.click(self.selectors["captcha_close_button"])
                logging.info("Captcha closed.")
                random_delay(2, 4)
            
            # Find the first video link
            video_selector = 'a[href*="/video/"]'
            video_link = self.page.get_attribute(video_selector, "href")
            
            if video_link:
                logging.info(f"Discovered video link: {video_link}")
                return video_link
            else:
                logging.warning("No video link found.")
                return None
        except Exception as e:
            logging.error(f"Error discovering content: {e}")
            return None
