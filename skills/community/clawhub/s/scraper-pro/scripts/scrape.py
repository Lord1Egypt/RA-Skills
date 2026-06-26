#!/usr/bin/env python3
"""
Data Scraper - Extract structured data from websites
"""

import argparse
import json
import os
import re
import sys
import ssl
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError


def fetch_page(url, wait=0):
    """Fetch a web page."""
    import time
    if wait:
        time.sleep(wait)
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urlopen(req, timeout=30, context=ctx) as resp:
            return resp.read().decode('utf-8', errors='ignore')
    except URLError as e:
        print(f"Error fetching {url}: {e}")
        return None


def parse_html_simple(html, selector):
    """Simple HTML parsing with regex (basic CSS-like selectors)."""
    results = []
    
    # Handle tag.class or tag#id selectors
    match = re.match(r'^(\w+)?([\.#])(\w+)$', selector)
    if match:
        tag, sep, name = match.groups()
        
        if sep == '.':  # Class
            pattern = rf'<(\w+)[^>]*class="[^"]*\b{name}\b[^"]*"[^>]*>(.*?)</\1>'
            for m in re.finditer(pattern, html, re.DOTALL):
                text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                if text:
                    results.append(text)
        elif sep == '#':  # ID
            pattern = rf'<(\w+)[^>]*id="{name}"[^>]*>(.*?)</\1>'
            m = re.search(pattern, html, re.DOTALL)
            if m:
                text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
                if text:
                    results.append(text)
    
    # Handle tag::attr selectors
    attr_match = re.match(r'^(\w+)::(attr\([^)]+\))$', selector)
    if attr_match:
        tag, attr_expr = attr_match.groups()
        attr_name = re.search(r'attr\(([^)]+)\)', attr_expr).group(1)
        pattern = rf'<{tag}[^>]*({attr_name}="([^"]*)")[^>]*>'
        for m in re.finditer(pattern, html):
            if m.group(2):
                results.append(m.group(2))
    
    # Handle ::text selector
    if selector.endswith('::text'):
        tag = selector.split('::')[0] or '\w+'
        pattern = rf'<{tag}[^>]*>(.*?)</{tag}>'
        for m in re.finditer(pattern, html, re.DOTALL):
            text = m.group(1).strip()
            if text and not text.startswith('<'):
                results.append(text)
    
    return results


def scrape(args):
    """Main scraping logic."""
    print(f"Scraping: {args.url}")
    
    html = fetch_page(args.url, args.wait)
    if not html:
        return 1
    
    if args.selector:
        data = parse_html_simple(html, args.selector)
    else:
        # Just get the raw content
        data = [html[:1000]]  # First 1000 chars
    
    print(f"Found {len(data)} items")
    
    # Output
    if args.output:
        if args.format == 'json':
            with open(args.output, 'w') as f:
                json.dump(data, f, indent=2)
        elif args.format == 'csv':
            with open(args.output, 'w') as f:
                f.write('\n'.join(data))
        elif args.format == 'markdown':
            with open(args.output, 'w') as f:
                for i, item in enumerate(data, 1):
                    f.write(f"{i}. {item}\n")
        print(f"Saved to: {args.output}")
    else:
        for item in data[:args.limit]:
            print(item)
    
    return 0


def main():
    parser = argparse.ArgumentParser(description='Data Scraper')
    parser.add_argument('--url', required=True, help='URL to scrape')
    parser.add_argument('--selector', help='CSS selector for extraction')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', default='json', choices=['json', 'csv', 'markdown'], help='Output format')
    parser.add_argument('--limit', type=int, default=100, help='Maximum items')
    parser.add_argument('--wait', type=int, default=0, help='Wait between requests (seconds)')
    
    args = parser.parse_args()
    return scrape(args)


if __name__ == '__main__':
    sys.exit(main())
