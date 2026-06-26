#!/usr/bin/env python3
"""
Web scraping automation script using Selenium and BeautifulSoup.
"""

import sys
import argparse
import time
import json
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import FirefoxOptions
from selenium.webdriver.edge.options import EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import (NoSuchElementException, 
                                        TimeoutException,
                                        WebDriverException)
import logging

class WebScraper:
    """Web scraping automation class."""
    
    def __init__(self, browser='chrome', headless=True, timeout=30):
        self.browser = browser.lower()
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        self.soup = None
        
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
            options = FirefoxOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--width=1920')
            options.add_argument('--height=1080')
        elif self.browser == 'edge':
            options = EdgeOptions()
            if self.headless:
                options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--window-size=1920,1080')
        else:
            raise ValueError(f"Unsupported browser: {self.browser}")
        
        return options
    
    def scrape_page(self, url, selectors=None, wait_for=None):
        """
        Scrape data from a webpage.
        
        Args:
            url (str): URL to scrape
            selectors (dict): Dictionary of data_name -> CSS selector pairs
            wait_for (str): CSS selector to wait for before scraping
        """
        try:
            self.driver.get(url)
            self.logger.info(f"Loaded page: {url}")
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            # Wait for specific element if provided
            if wait_for:
                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, wait_for)))
            
            # Get page source and parse with BeautifulSoup
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Scrape data using selectors
            if selectors:
                data = self._scrape_with_selectors(selectors)
            else:
                data = self._scrape_all_text()
            
            return data
            
        except Exception as e:
            self.logger.error(f"Error scraping page: {str(e)}")
            return None
    
    def _scrape_with_selectors(self, selectors):
        """Scrape data using CSS selectors."""
        data = {}
        
        for data_name, selector in selectors.items():
            try:
                elements = self.soup.select(selector)
                
                if elements:
                    if len(elements) == 1:
                        data[data_name] = self._extract_element_text(elements[0])
                    else:
                        data[data_name] = [self._extract_element_text(el) for el in elements]
                else:
                    data[data_name] = None
                    
            except Exception as e:
                self.logger.warning(f"Error scraping {data_name}: {str(e)}")
                data[data_name] = None
        
        return data
    
    def _extract_element_text(self, element):
        """Extract text from an element."""
        text = element.get_text(strip=True)
        
        # Extract specific attributes if needed
        if element.name == 'a':
            href = element.get('href')
            if href:
                text = f"{text} ({href})"
        
        if element.name in ['img', 'source']:
            src = element.get('src') or element.get('data-src')
            if src:
                text = f"[Image: {src}]"
        
        return text
    
    def _scrape_all_text(self):
        """Scrape all text content from the page."""
        text_content = self.soup.get_text(strip=True)
        return {'all_text': text_content}
    
    def scrape_table(self, table_selector, output_file=None, format='csv'):
        """
        Scrape data from an HTML table.
        
        Args:
            table_selector (str): CSS selector for the table
            output_file (str): Output file path
            format (str): Output format ('csv' or 'json')
        """
        try:
            table = self.soup.select_one(table_selector)
            if not table:
                raise NoSuchElementException(f"Table not found with selector: {table_selector}")
            
            # Extract table headers
            headers = []
            header_row = table.select_one('thead tr') or table.select_one('tr')
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.select('th, td')]
            
            # Extract table rows
            rows = []
            for row in table.select('tr'):
                if row == header_row:
                    continue  # Skip header row
                
                cells = [td.get_text(strip=True) for td in row.select('td, th')]
                if cells:  # Only add non-empty rows
                    rows.append(cells)
            
            # Create DataFrame
            df = pd.DataFrame(rows, columns=headers if headers else None)
            
            # Save to file if requested
            if output_file:
                if format == 'csv':
                    df.to_csv(output_file, index=False)
                elif format == 'json':
                    df.to_json(output_file, orient='records', indent=2)
                
                self.logger.info(f"Table data saved to {output_file}")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Error scraping table: {str(e)}")
            return None
    
    def scrape_links(self, link_selector=None, output_file=None):
        """
        Scrape links from the page.
        
        Args:
            link_selector (str): CSS selector for links (default: all links)
            output_file (str): Output file path
        """
        try:
            if link_selector:
                links = self.soup.select(link_selector)
            else:
                links = self.soup.select('a[href]')
            
            link_data = []
            for link in links:
                href = link.get('href')
                text = link.get_text(strip=True)
                
                if href and text:
                    link_data.append({
                        'text': text,
                        'url': href,
                        'full_url': self._make_absolute_url(href)
                    })
            
            # Save to file if requested
            if output_file:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(link_data, f, indent=2, ensure_ascii=False)
                self.logger.info(f"Links saved to {output_file}")
            
            return link_data
            
        except Exception as e:
            self.logger.error(f"Error scraping links: {str(e)}")
            return None
    
    def _make_absolute_url(self, url):
        """Convert relative URL to absolute URL."""
        if url.startswith(('http://', 'https://')):
            return url
        else:
            # This is a simplified version - in production, you'd use urllib.parse
            return url
    
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
    parser = argparse.ArgumentParser(description='Automatically scrape web pages')
    parser.add_argument('--url', required=True, help='URL to scrape')
    parser.add_argument('--browser', default='chrome', choices=['chrome', 'firefox', 'edge'],
                       help='Browser to use (default: chrome)')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='Run browser in headless mode')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Timeout in seconds (default: 30)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', choices=['csv', 'json', 'txt'], default='csv',
                       help='Output format (default: csv)')
    parser.add_argument('--screenshot', action='store_true',
                       help='Take screenshot of the page')
    parser.add_argument('--wait-for', help='CSS selector to wait for before scraping')
    
    # Selectors for specific data extraction
    parser.add_argument('--title-selector', default='title',
                       help='CSS selector for page title')
    parser.add_argument('--content-selector', 
                       help='CSS selector for main content')
    parser.add_argument('--table-selector', 
                       help='CSS selector for table to scrape')
    parser.add_argument('--link-selector', 
                       help='CSS selector for links to scrape')
    
    args = parser.parse_args()
    
    # Initialize web scraper
    scraper = WebScraper(browser=args.browser, headless=args.headless, timeout=args.timeout)
    
    try:
        # Setup driver
        scraper.setup_driver()
        
        # Define selectors
        selectors = {}
        if args.title_selector:
            selectors['title'] = args.title_selector
        if args.content_selector:
            selectors['content'] = args.content_selector
        
        # Scrape page
        data = scraper.scrape_page(
            url=args.url,
            selectors=selectors,
            wait_for=args.wait_for
        )
        
        if data:
            print("Scraping completed successfully!")
            
            # Process table if specified
            if args.table_selector:
                table_data = scraper.scrape_table(
                    table_selector=args.table_selector,
                    output_file=args.output,
                    format=args.format
                )
                if table_data is not None:
                    print(f"Table scraped with {len(table_data)} rows")
            
            # Process links if specified
            elif args.link_selector:
                link_data = scraper.scrape_links(
                    link_selector=args.link_selector,
                    output_file=args.output
                )
                if link_data:
                    print(f"Found {len(link_data)} links")
            
            # Process general data
            elif data:
                if args.output:
                    if args.format == 'json':
                        with open(args.output, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                    elif args.format == 'csv':
                        df = pd.DataFrame([data])
                        df.to_csv(args.output, index=False)
                    elif args.format == 'txt':
                        with open(args.output, 'w', encoding='utf-8') as f:
                            for key, value in data.items():
                                f.write(f"{key}: {value}\n")
                    
                    print(f"Data saved to {args.output}")
                else:
                    print("Scraped data:")
                    for key, value in data.items():
                        print(f"{key}: {value}")
            
            # Take screenshot if requested
            if args.screenshot:
                scraper.take_screenshot()
                print("Screenshot saved!")
        else:
            print("Failed to scrape page")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        scraper.close()

if __name__ == '__main__':
    main()