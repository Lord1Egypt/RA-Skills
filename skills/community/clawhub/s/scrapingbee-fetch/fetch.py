#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests",
#     "python-dotenv"
# ]
# ///

import argparse
import requests
import sys
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Get the API key from environment variables
API_KEY = os.environ.get("SCRAPINGBEE_API_KEY")

def fetch_url(url, render_js=True, country_code=None, wait=3000, block_ads=True, premium_proxy=False):
    if not API_KEY:
        print("Error: SCRAPINGBEE_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    print(f"Fetching {url} via ScrapingBee...", file=sys.stderr)
    
    extract_rules = {
        "title": {
            "selector": "h1",
            "output": "text",
        },
        "text": {
            "selector": "body",
            "output": "text_relevant",
            "clean": False,
        }
    }
    
    params = {
        "api_key": API_KEY,
        "url": url,
        "render_js": "true" if render_js else "false",
        "wait": wait,
        "block_ads": "true" if block_ads else "false",
        "premium_proxy": "true" if premium_proxy else "false",
        "extract_rules": json.dumps(extract_rules)
    }
    
    if country_code:
        params["country_code"] = country_code
    
    if "google" in url.lower():
        params["custom_google"] = "true"
        
    try:
        response = requests.get("https://app.scrapingbee.com/api/v1/", params=params, timeout=60)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}", file=sys.stderr)
            sys.exit(1)
            
        data = response.json()
        
        title = data.get("title", "No title found")
        text = data.get("text", "No text found")
        
        # Fix encoding issues from ScrapingBee JSON response
        if isinstance(title, str):
            try:
                title = title.encode('windows-1251').decode('utf-8')
            except:
                pass
        if isinstance(text, str):
            try:
                text = text.encode('windows-1251').decode('utf-8')
            except:
                pass
                
        print(f"# {title}\n")
        print(text)
        
    except Exception as e:
        print(f"Exception occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch URL using ScrapingBee")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--no-render-js", action="store_true", help="Disable JavaScript rendering")
    parser.add_argument("--country-code", type=str, help="Country code for proxy (e.g., us, uk, ru)")
    parser.add_argument("--wait", type=int, default=3000, help="Wait time in milliseconds before extracting content (default: 3000)")
    parser.add_argument("--no-block-ads", action="store_true", help="Disable ad blocking")
    parser.add_argument("--premium-proxy", action="store_true", help="Use premium proxy")
    
    args = parser.parse_args()
    
    fetch_url(
        url=args.url,
        render_js=not args.no_render_js,
        country_code=args.country_code,
        wait=args.wait,
        block_ads=not args.no_block_ads,
        premium_proxy=args.premium_proxy
    )
