#!/usr/bin/env python3
"""
Time logging automation script for task time registration.
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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import (NoSuchElementException, 
                                        TimeoutException, 
                                        ElementNotInteractableException,
                                        StaleElementReferenceException)
import logging

class TimeLogger:
    """Time logging automation class."""
    
    def __init__(self, headless=False, timeout=30):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self):
        """Setup Chrome WebDriver."""
        options = Options()
        if self.headless:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, self.timeout)
        self.logger.info("Chrome browser initialized successfully")
    
    def log_time(self, task_url, hours, description, date=None):
        """
        Log time for a task.
        
        Args:
            task_url (str): URL of the task page
            hours (str): Hours to log (e.g., "2")
            description (str): Description of the work
            date (str): Date in YYYY-MM-DD format (optional)
        """
        try:
            self.driver.get(task_url)
            self.logger.info(f"Loaded task page: {task_url}")
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            # Take initial screenshot
            self.take_screenshot('initial_page.png')
            
            # Try to find and click time logging button
            time_logged = self._find_and_click_time_button()
            
            if time_logged:
                # Fill time logging form
                self._fill_time_form(hours, description, date)
                
                # Submit the form
                self._submit_time_form()
                
                return True
            else:
                self.logger.error("Could not find time logging button")
                return False
                
        except Exception as e:
            self.logger.error(f"Error logging time: {str(e)}")
            return False
    
    def _find_and_click_time_button(self):
        """Find and click the time logging button."""
        # Try different selectors for time logging buttons
        button_selectors = [
            'button:contains("Log Time")',
            'button:contains("Add Time")',
            'button:contains("记录时间")',
            'button:contains("登记工时")',
            'button:contains("工时登记")',
            '.log-time',
            '.add-time',
            '.time-log',
            '[title*="time"]',
            '[title*="Time"]',
            '[title*="工时"]',
            'a:contains("Time")',
            'a:contains("时间")',
            'a:contains("工时")'
        ]
        
        for selector in button_selectors:
            try:
                # Wait for button to be clickable
                button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                button.click()
                self.logger.info(f"Clicked time logging button: {selector}")
                
                # Wait for form to appear
                time.sleep(2)
                return True
                
            except:
                continue
        
        # Try to find by text content using XPath
        xpath_selectors = [
            '//button[contains(text(), "Time")]',
            '//button[contains(text(), "时间")]',
            '//button[contains(text(), "工时")]',
            '//a[contains(text(), "Time")]',
            '//a[contains(text(), "时间")]',
            '//a[contains(text(), "工时")]'
        ]
        
        for xpath in xpath_selectors:
            try:
                button = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                button.click()
                self.logger.info(f"Clicked time logging button with XPath: {xpath}")
                
                # Wait for form to appear
                time.sleep(2)
                return True
                
            except:
                continue
        
        return False
    
    def _fill_time_form(self, hours, description, date=None):
        """Fill the time logging form."""
        try:
            # Try to find hours input field
            hours_selectors = [
                'input[name*="hour"]',
                'input[name*="time"]',
                'input[name*="duration"]',
                'input[name*="工时"]',
                'input[name*="小时"]',
                'input[placeholder*="hour"]',
                'input[placeholder*="time"]',
                'input[placeholder*="duration"]',
                'input[placeholder*="工时"]',
                'input[placeholder*="小时"]',
                '#hours',
                '#time',
                '#duration',
                '.hours',
                '.time',
                '.duration'
            ]
            
            hours_filled = False
            for selector in hours_selectors:
                try:
                    hours_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    hours_input.clear()
                    hours_input.send_keys(hours)
                    self.logger.info(f"Filled hours: {hours}")
                    hours_filled = True
                    break
                except:
                    continue
            
            if not hours_filled:
                self.logger.warning("Could not find hours input field")
            
            # Try to find description textarea
            desc_selectors = [
                'textarea[name*="description"]',
                'textarea[name*="comment"]',
                'textarea[name*="note"]',
                'textarea[name*="描述"]',
                'textarea[name*="备注"]',
                'textarea[placeholder*="description"]',
                'textarea[placeholder*="comment"]',
                'textarea[placeholder*="note"]',
                'textarea[placeholder*="描述"]',
                'textarea[placeholder*="备注"]',
                '#description',
                '#comment',
                '#note',
                '.description',
                '.comment',
                '.note'
            ]
            
            desc_filled = False
            for selector in desc_selectors:
                try:
                    desc_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    desc_input.clear()
                    desc_input.send_keys(description)
                    self.logger.info(f"Filled description: {description}")
                    desc_filled = True
                    break
                except:
                    continue
            
            if not desc_filled:
                self.logger.warning("Could not find description textarea")
            
            # Try to find date input if provided
            if date:
                date_selectors = [
                    'input[name*="date"]',
                    'input[name*="Date"]',
                    'input[name*="日期"]',
                    'input[placeholder*="date"]',
                    'input[placeholder*="Date"]',
                    'input[placeholder*="日期"]',
                    '#date',
                    '#Date',
                    '.date'
                ]
                
                date_filled = False
                for selector in date_selectors:
                    try:
                        date_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        date_input.clear()
                        date_input.send_keys(date)
                        self.logger.info(f"Filled date: {date}")
                        date_filled = True
                        break
                    except:
                        continue
                
                if not date_filled:
                    self.logger.warning("Could not find date input field")
            
            # Take screenshot after filling form
            self.take_screenshot('filled_form.png')
            
        except Exception as e:
            self.logger.error(f"Error filling time form: {str(e)}")
    
    def _submit_time_form(self):
        """Submit the time logging form."""
        try:
            # Try to find submit button
            submit_selectors = [
                'input[type="submit"]',
                'button[type="submit"]',
                'input[value*="submit"]',
                'input[value*="Submit"]',
                'input[value*="保存"]',
                'input[value*="提交"]',
                'button:contains("Submit")',
                'button:contains("保存")',
                'button:contains("提交")',
                '.submit',
                '#submit',
                '.save',
                '.save-button'
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    submit_button.click()
                    self.logger.info("Clicked submit button")
                    
                    # Wait for submission to complete
                    time.sleep(3)
                    return True
                    
                except:
                    continue
            
            self.logger.warning("Could not find submit button")
            return False
            
        except Exception as e:
            self.logger.error(f"Error submitting time form: {str(e)}")
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
    parser = argparse.ArgumentParser(description='Automatically log time for tasks')
    parser.add_argument('--url', required=True, help='URL of the task page')
    parser.add_argument('--hours', required=True, help='Hours to log (e.g., "2")')
    parser.add_argument('--description', required=True, help='Description of the work')
    parser.add_argument('--date', help='Date in YYYY-MM-DD format (optional)')
    parser.add_argument('--headless', action='store_true', 
                       help='Run browser in headless mode')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Timeout in seconds (default: 30)')
    parser.add_argument('--screenshot', action='store_true',
                       help='Take screenshots during the process')
    
    args = parser.parse_args()
    
    # Initialize time logger
    logger = TimeLogger(headless=args.headless, timeout=args.timeout)
    
    try:
        # Setup driver
        logger.setup_driver()
        
        # Log time
        success = logger.log_time(
            task_url=args.url,
            hours=args.hours,
            description=args.description,
            date=args.date
        )
        
        if success:
            print("Time logged successfully!")
            if args.screenshot:
                logger.take_screenshot('final_page.png')
                print("Final screenshot saved!")
        else:
            print("Failed to log time")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        logger.close()

if __name__ == '__main__':
    main()