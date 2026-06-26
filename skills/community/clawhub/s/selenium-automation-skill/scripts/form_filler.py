#!/usr/bin/env python3
"""
Form filling automation script using Selenium.
Supports various input types and form submission.
"""

import sys
import argparse
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.options import ArgOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import (NoSuchElementException, 
                                        TimeoutException, 
                                        ElementNotInteractableException,
                                        StaleElementReferenceException)
import logging

class FormFiller:
    """Form filling automation class."""
    
    def __init__(self, browser='chrome', headless=False, timeout=30):
        self.browser = browser.lower()
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup WebDriver based on browser type."""
        options = self._get_browser_options()
        
        if self.browser == 'chrome':
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        elif self.browser == 'firefox':
            service = Service(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=options)
        elif self.browser == 'edge':
            service = Service(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service, options=options)
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")
        
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.logger.info(f"Browser {self.browser} initialized successfully")
    
    def _get_browser_options(self):
        """Get browser-specific options."""
        if self.browser == 'chrome':
            options = Options()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
        elif self.browser == 'firefox':
            options = ArgOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--width=1920')
            options.add_argument('--height=1080')
        elif self.browser == 'edge':
            options = ArgOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")
        
        return options
    
    def fill_form(self, url, form_data, submit=True, submit_button=None):
        """
        Fill a form with provided data.
        
        Args:
            url (str): URL of the form page
            form_data (dict): Dictionary of field_name -> value pairs
            submit (bool): Whether to submit the form after filling
            submit_button (str): CSS selector or ID of submit button
        """
        try:
            self.driver.get(url)
            self.logger.info(f"Loaded page: {url}")
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            # Fill each field
            for field_name, value in form_data.items():
                self._fill_field(field_name, value)
            
            self.logger.info("Form filled successfully")
            
            # Submit form if requested
            if submit:
                self._submit_form(submit_button)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error filling form: {str(e)}")
            return False
    
    def _fill_field(self, field_name, value):
        """Fill a single field."""
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            try:
                # Try multiple locator strategies
                element = self._find_element(field_name)
                
                if element:
                    # Clear existing value
                    element.clear()
                    
                    # Type new value
                    element.send_keys(value)
                    self.logger.info(f"Filled field '{field_name}' with '{value}'")
                    return
                
            except (NoSuchElementException, ElementNotInteractableException) as e:
                attempts += 1
                self.logger.warning(f"Attempt {attempts} failed for field '{field_name}': {str(e)}")
                if attempts < max_attempts:
                    time.sleep(1)  # Wait before retry
            
            except StaleElementReferenceException:
                attempts += 1
                self.logger.warning(f"Stale element reference for field '{field_name}', retrying...")
                if attempts < max_attempts:
                    time.sleep(1)
        
        raise NoSuchElementException(f"Could not find or interact with field: {field_name}")
    
    def _find_element(self, field_name):
        """Find an element using multiple strategies."""
        strategies = [
            (By.ID, field_name),
            (By.NAME, field_name),
            (By.CSS_SELECTOR, f"[name='{field_name}']"),
            (By.CSS_SELECTOR, f"#{field_name}"),
            (By.XPATH, f"//*[@name='{field_name}']"),
            (By.XPATH, f"//*[@id='{field_name}']"),
            (By.CSS_SELECTOR, f"[placeholder*='{field_name}']"),
            (By.CSS_SELECTOR, f"[aria-label*='{field_name}']"),
            (By.CSS_SELECTOR, f"[title*='{field_name}']"),
        ]
        
        for by, value in strategies:
            try:
                element = self.wait.until(EC.presence_of_element_located((by, value)))
                if element.is_displayed() and element.is_enabled():
                    return element
            except:
                continue
        
        return None
    
    def _submit_form(self, submit_button=None):
        """Submit the form."""
        try:
            if submit_button:
                # Use specific submit button
                button = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, submit_button) if submit_button.startswith('.') else (By.ID, submit_button)
                ))
            else:
                # Try common submit button selectors
                button_selectors = [
                    'input[type="submit"]',
                    'button[type="submit"]',
                    'input[value*="submit"]',
                    'input[value*="Submit"]',
                    'button:contains("Submit")',
                    '.submit',
                    '#submit'
                ]
                
                button = None
                for selector in button_selectors:
                    try:
                        button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                        if button:
                            break
                    except:
                        continue
            
            if button:
                button.click()
                self.logger.info("Form submitted successfully")
                
                # Wait for page to load after submission
                time.sleep(2)
                return True
            else:
                self.logger.warning("No submit button found")
                return False
                
        except Exception as e:
            self.logger.error(f"Error submitting form: {str(e)}")
            return False
    
    def take_screenshot(self, filename='screenshot.png'):
        """Take a screenshot of the current page."""
        try:
            self.driver.save_screenshot(filename)
            self.logger.info(f"Screenshot saved as {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {str(e)}")
            return False
    
    def close(self):
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description='Automatically fill web forms')
    parser.add_argument('--url', required=True, help='URL of the form page')
    parser.add_argument('--browser', default='chrome', choices=['chrome', 'firefox', 'edge'],
                       help='Browser to use (default: chrome)')
    parser.add_argument('--headless', action='store_true', 
                       help='Run browser in headless mode')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Timeout in seconds (default: 30)')
    parser.add_argument('--screenshot', action='store_true',
                       help='Take screenshot after filling form')
    parser.add_argument('--no-submit', action='store_true',
                       help='Do not submit the form after filling')
    parser.add_argument('--submit-button', help='CSS selector or ID of submit button')
    
    # Form data arguments
    parser.add_argument('--username', help='Username field value')
    parser.add_argument('--password', help='Password field value')
    parser.add_argument('--email', help='Email field value')
    parser.add_argument('--name', help='Name field value')
    parser.add_argument('--message', help='Message field value')
    parser.add_argument('--phone', help='Phone field value')
    parser.add_argument('--company', help='Company field value')
    
    args = parser.parse_args()
    
    # Build form data dictionary
    form_data = {}
    for field in ['username', 'password', 'email', 'name', 'message', 'phone', 'company']:
        value = getattr(args, field)
        if value:
            form_data[field] = value
    
    if not form_data:
        print("Error: No form data provided. Use --username, --password, etc.")
        sys.exit(1)
    
    # Initialize form filler
    filler = FormFiller(browser=args.browser, headless=args.headless, timeout=args.timeout)
    
    try:
        # Setup driver
        filler.setup_driver()
        
        # Fill form
        success = filler.fill_form(
            url=args.url,
            form_data=form_data,
            submit=not args.no_submit,
            submit_button=args.submit_button
        )
        
        if success:
            print("Form filled successfully!")
            
            if args.screenshot:
                filler.take_screenshot()
                print("Screenshot saved!")
        else:
            print("Failed to fill form")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        filler.close()

if __name__ == '__main__':
    main()