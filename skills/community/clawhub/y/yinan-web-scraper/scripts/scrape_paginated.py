#!/usr/bin/env python3
"""
Paginated Web Scraper
Extract data from multiple pages with pagination.

Usage:
    python scrape_paginated.py --url "https://example.com?page={page}" --pages 10 --fields "title=h1" --output data.csv
"""

import argparse
import csv
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Import from scrape_page.py
sys.path.insert(0, str(Path(__file__).parent))
from scrape_page import parse_fields, scrape_page, save_data, run_agent_browser

def scrape_paginated(url_pattern, pages, fields, output_path, output_format='csv', delay=2):
    """Scrape multiple pages with pagination."""
    all_data = []
    
    for page_num in range(1, pages + 1):
        print(f"\n{'='*50}")
        print(f"Scraping page {page_num}/{pages}...")
        print(f"{'='*50}")
        
        # Generate URL for this page
        if '{page}' in url_pattern:
            url = url_pattern.replace('{page}', str(page_num))
        elif '{0}' in url_pattern:
            url = url_pattern.replace('{0}', str(page_num))
        else:
            # Try appending ?page=N
            separator = '&' if '?' in url_pattern else '?'
            url = f"{url_pattern}{separator}page={page_num}"
        
        print(f"URL: {url}")
        
        # Scrape this page
        data = scrape_page(url, fields, wait_time=2)
        
        if data:
            data['_page'] = page_num
            all_data.append(data)
            print(f"✓ Page {page_num} scraped successfully")
        else:
            print(f"✗ Page {page_num} failed")
            # Continue anyway, don't stop on single page failure
        
        # Delay before next page (be polite to servers)
        if page_num < pages:
            print(f"Waiting {delay}s before next page...")
            time.sleep(delay)
    
    # Save all data
    if all_data:
        save_data(all_data, output_path, output_format)
        print(f"\n✅ Scraped {len(all_data)} pages successfully!")
    else:
        print("\n❌ No data scraped!")
    
    return all_data

def scrape_with_next_button(url, fields, output_path, output_format='csv', next_selector=None, max_pages=50, delay=2):
    """Scrape by clicking 'next page' button."""
    all_data = []
    page_num = 1
    
    print(f"Opening initial page: {url}")
    stdout, stderr, code = run_agent_browser(["open", url])
    if code != 0:
        print(f"Error opening page: {stderr}")
        return []
    
    while page_num <= max_pages:
        print(f"\n{'='*50}")
        print(f"Scraping page {page_num}...")
        print(f"{'='*50}")
        
        # Wait for page load
        time.sleep(2)
        
        # Scrape this page
        data = scrape_page(url, fields, wait_time=0)  # Already waited
        
        if data:
            data['_page'] = page_num
            all_data.append(data)
            print(f"✓ Page {page_num} scraped successfully")
        else:
            print(f"✗ Page {page_num} failed")
            break  # Stop if we can't scrape
        
        # Try to click next button
        print(f"Looking for next button: {next_selector}")
        stdout, stderr, code = run_agent_browser(["is", "visible", next_selector])
        
        if code == 0 and stdout.strip().lower() == 'true':
            print(f"Clicking next button...")
            stdout, stderr, code = run_agent_browser(["click", next_selector])
            if code != 0:
                print(f"Error clicking next: {stderr}")
                break
            page_num += 1
            time.sleep(delay)
        else:
            print("No more pages (next button not found)")
            break
    
    # Save all data
    if all_data:
        save_data(all_data, output_path, output_format)
        print(f"\n✅ Scraped {len(all_data)} pages successfully!")
    else:
        print("\n❌ No data scraped!")
    
    return all_data

def main():
    parser = argparse.ArgumentParser(description='Scrape paginated web pages')
    parser.add_argument('--url', required=True, 
                        help='Target URL (use {page} for page number placeholder)')
    parser.add_argument('--pages', type=int, default=10,
                        help='Number of pages to scrape (default: 10)')
    parser.add_argument('--fields', required=True,
                        help='Field definitions (name=selector,name2=selector2)')
    parser.add_argument('--output', required=True,
                        help='Output file path')
    parser.add_argument('--format', choices=['csv', 'json', 'xlsx'], default='csv',
                        help='Output format (default: csv)')
    parser.add_argument('--delay', type=int, default=2,
                        help='Delay between pages in seconds (default: 2)')
    parser.add_argument('--next-selector',
                        help='CSS selector for "next page" button (alternative to URL pattern)')
    args = parser.parse_args()
    
    # Parse fields
    fields = parse_fields(args.fields)
    print(f"Fields to extract: {list(fields.keys())}")
    print()
    
    # Scrape
    if args.next_selector:
        # Use next button method
        data = scrape_with_next_button(
            args.url, fields, args.output, args.format,
            args.next_selector, args.pages, args.delay
        )
    else:
        # Use URL pattern method
        data = scrape_paginated(
            args.url, args.pages, fields, args.output, args.format, args.delay
        )
    
    return 0 if data else 1

if __name__ == '__main__':
    sys.exit(main())
