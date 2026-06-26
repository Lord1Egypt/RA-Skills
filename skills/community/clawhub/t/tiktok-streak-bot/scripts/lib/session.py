import json
import logging
import os

class SessionManager:
    def __init__(self, context, cookies_path):
        self.context = context
        self.cookies_path = cookies_path

    def load_cookies(self):
        if os.path.exists(self.cookies_path):
            logging.info(f"Loading cookies from {self.cookies_path}...")
            with open(self.cookies_path, 'r', encoding='utf-8') as f:
                cookies = json.load(f)

            sanitized_cookies = []
            for cookie in cookies:
                sanitized_cookie = {}
                for key in ['name', 'value', 'url', 'domain', 'path', 'httpOnly', 'secure']:
                    if key in cookie:
                        sanitized_cookie[key] = cookie[key]
                if 'expirationDate' in cookie:
                    sanitized_cookie['expires'] = cookie['expirationDate']
                if cookie.get('sameSite'):
                    val = cookie['sameSite'].lower()
                    if val == 'no_restriction':
                        sanitized_cookie['sameSite'] = 'None'
                    elif val in ['strict', 'lax', 'none']:
                        sanitized_cookie['sameSite'] = val.capitalize()

                if 'url' in sanitized_cookie and not sanitized_cookie['url']:
                    del sanitized_cookie['url']
                if 'domain' in sanitized_cookie and not sanitized_cookie['domain']:
                    del sanitized_cookie['domain']

                if 'domain' not in sanitized_cookie and 'url' not in sanitized_cookie:
                    continue
                
                if 'domain' in sanitized_cookie and 'url' in sanitized_cookie:
                    del sanitized_cookie['url']

                sanitized_cookies.append(sanitized_cookie)

            self.context.add_cookies(sanitized_cookies)
            return True
        else:
            logging.warning(f"Cookies file not found at {self.cookies_path}.")
            return False

    def save_cookies(self):
        logging.info(f"Saving cookies to {self.cookies_path}...")
        cookies = self.context.cookies()
        with open(self.cookies_path, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=4)
