#!/usr/bin/env python3
"""
Slickdeals Deal Search - Search Slickdeals.net for deals, coupons, and promo codes.
"""

import argparse
import json
import re
import urllib.parse
import urllib.request
import urllib.error
from html.parser import HTMLParser
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Deal:
    title: str
    price: str
    original_price: Optional[str]
    discount: Optional[str]
    store: str
    score: str
    comments: int
    expired: bool
    url: str


class SlickdealsParser(HTMLParser):
    """Parse Slickdeals search results."""
    
    def __init__(self):
        super().__init__()
        self.deals: List[Deal] = []
        self.current_deal = None
        self.in_deal = False
        self.current_field = None
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Deal container
        if 'class' in attrs_dict and 'dealRow' in attrs_dict.get('class', ''):
            self.in_deal = True
            self.current_deal = {
                'title': '',
                'price': '',
                'original_price': None,
                'discount': None,
                'store': '',
                'score': '0',
                'comments': 0,
                'expired': False,
                'url': ''
            }
    
    def handle_endtag(self, tag):
        if tag == 'div' and self.in_deal:
            self.in_deal = False
            if self.current_deal and self.current_deal.get('title'):
                self.deals.append(Deal(**self.current_deal))
            self.current_deal = None
    
    def handle_data(self, data):
        if self.in_deal and self.current_deal:
            data = data.strip()
            if data and 'expired' in data.lower():
                self.current_deal['expired'] = True


def search_deals(query: str, limit: int = 10) -> List[Deal]:
    """Search Slickdeals for deals matching query."""
    
    encoded_query = urllib.parse.quote(query)
    url = f"https://slickdeals.net/newsearch.php?q={encoded_query}&searcharea=deals&searchin=first"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except urllib.error.URLError as e:
        print(f"Error fetching deals: {e}")
        return []
    
    # Simple regex-based extraction (more reliable than HTML parsing for this site)
    deals = []
    
    # Find deal titles and prices
    title_pattern = r'Found by[^>]*>.*?</a>\s*\$?([\d,.]+)?\s*(\$[\d,.]+)?\s*(\d+% off)?'
    
    # Look for deal blocks
    deal_blocks = re.findall(
        r'<div[^>]*class="[^"]*dealRow[^"]*"[^>]*>(.*?)</div>',
        html,
        re.DOTALL | re.IGNORECASE
    )
    
    # Alternative: parse from the text content
    lines = html.split('\n')
    current_title = None
    current_price = None
    current_store = None
    expired = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Check for expiration
        if 'expired' in line.lower():
            expired = True
        
        # Check for deal title (Found by pattern)
        if 'Found by' in line:
            # Extract title from nearby content
            title_match = re.search(r'([^<]+)(?:<[^>]+>)*\s*\$?[\d,.]+', line)
            if title_match:
                current_title = title_match.group(1).strip()
        
        # Check for price
        price_match = re.search(r'\$?([\d,.]+)\s*(\$[\d,.]+)?\s*(\d+% off)?', line)
        if price_match and current_title:
            current_price = price_match.group(0)
        
        # Check for store
        store_match = re.search(r'(Amazon|Best Buy|Walmart|Newegg|Target|Steam|Epic|GameStop|Nintendo|PlayStation|Xbox)', line, re.I)
        if store_match:
            current_store = store_match.group(1)
    
    # Use a simpler approach: parse visible deals from the HTML
    # Look for patterns like: "Title $XX $YY 50% off Store"
    
    deal_pattern = re.compile(
        r'([^<>\n]{10,100}?)\s*\$?([\d,.]+)\s*(?:\$[\d,.]+)?\s*(\d+% off)?\s*(Amazon|Best Buy|Walmart|Newegg|Target|Steam|Epic|GameStop|Nintendo|PlayStation|Xbox)?',
        re.IGNORECASE
    )
    
    # Extract deals from the raw text
    visible_text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    visible_text = re.sub(r'<style[^>]*>.*?</style>', '', visible_text, flags=re.DOTALL)
    visible_text = re.sub(r'<[^>]+>', ' ', visible_text)
    
    # Find deals with price patterns
    lines = visible_text.split('\n')
    for line in lines:
        line = ' '.join(line.split())  # Normalize whitespace
        if '$' in line and len(line) > 20 and len(line) < 500:
            # Check if it looks like a deal
            if any(store in line for store in ['Amazon', 'Best Buy', 'Walmart', 'Newegg', 'Target', 'Steam']):
                deals.append(line)
                if len(deals) >= limit:
                    break
    
    return deals[:limit]


def format_deals(deals: List, output_format: str = 'text') -> str:
    """Format deals for output."""
    
    if output_format == 'json':
        return json.dumps(deals, indent=2)
    
    if not deals:
        return "No deals found."
    
    output = []
    output.append("| Deal | Price | Store |")
    output.append("|------|-------|-------|")
    
    for deal in deals[:10]:
        if isinstance(deal, str):
            output.append(f"| {deal[:80]}... | - | - |" if len(deal) > 80 else f"| {deal} | - | - |")
        else:
            output.append(f"| {deal.title[:50]} | {deal.price} | {deal.store} |")
    
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Search Slickdeals for deals'
    )
    parser.add_argument('query', help='Search query')
    parser.add_argument('-l', '--limit', type=int, default=10, help='Max results')
    parser.add_argument('-j', '--json', action='store_true', help='JSON output')
    parser.add_argument('-c', '--category', help='Category filter (video-games, electronics, etc.)')
    
    args = parser.parse_args()
    
    deals = search_deals(args.query, args.limit)
    output = format_deals(deals, 'json' if args.json else 'text')
    print(output)


if __name__ == '__main__':
    main()