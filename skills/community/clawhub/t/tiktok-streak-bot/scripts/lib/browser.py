import logging
from playwright.sync_api import sync_playwright

class BrowserManager:
    def __init__(self, headless=True, user_agent=None):
        self.headless = headless
        self.user_agent = user_agent
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        logging.info("Starting browser...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        
        context_args = {}
        if self.user_agent:
            context_args['user_agent'] = self.user_agent
            
        self.context = self.browser.new_context(**context_args)
        self.page = self.context.new_page()
        return self.page

    def stop(self):
        logging.info("Stopping browser...")
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def navigate(self, url):
        logging.info(f"Navigating to {url}...")
        self.page.goto(url, wait_until="networkidle")
