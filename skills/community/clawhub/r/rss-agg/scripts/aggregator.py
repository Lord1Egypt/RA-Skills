#!/usr/bin/env python3
"""
RSS/Atom Feed Aggregator
Parse and aggregate multiple feeds with filtering
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError
import ssl
import xml.etree.ElementTree as ET


def parse_date(date_str):
    """Try to parse various date formats."""
    formats = [
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def fetch_feed(url):
    """Fetch and parse a single feed."""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = Request(url, headers={
            'User-Agent': 'RSS-Aggregator/1.0'
        })
        with urlopen(req, timeout=30, context=ctx) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
        
        # Parse XML
        root = ET.fromstring(content)
        
        # Determine feed type
        if 'atom' in root.tag.lower():
            return parse_atom(root, url)
        else:
            return parse_rss(root, url)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []


def parse_rss(root, feed_url):
    """Parse RSS feed."""
    items = []
    channel = root.find('channel')
    feed_title = channel.find('title').text if channel is not None and channel.find('title') is not None else feed_url
    
    for item in root.findall('.//item'):
        title = item.find('title').text if item.find('title') is not None else ""
        link = item.find('link').text if item.find('link') is not None else ""
        desc = item.find('description').text if item.find('description') is not None else ""
        pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ""
        
        # Clean HTML from description
        desc = re.sub(r'<[^>]+>', '', desc) if desc else ""
        
        items.append({
            'title': title.strip() if title else "",
            'link': link.strip() if link else "",
            'description': desc.strip()[:500] if desc else "",
            'pubDate': pub_date,
            'feed': feed_title
        })
    return items


def parse_atom(root, feed_url):
    """Parse Atom feed."""
    items = []
    feed_title = root.find('title').text if root.find('title') is not None else feed_url
    
    for entry in root.findall('.//entry'):
        title = entry.find('title').text if entry.find('title') is not None else ""
        link = ""
        link_elem = entry.find('link')
        if link_elem is not None:
            link = link_elem.get('href', '')
        
        desc = ""
        if entry.find('content') is not None:
            desc = entry.find('content').text or ""
        elif entry.find('summary') is not None:
            desc = entry.find('summary').text or ""
        
        desc = re.sub(r'<[^>]+>', '', desc) if desc else ""
        
        pub_date = ""
        if entry.find('published') is not None:
            pub_date = entry.find('published').text
        elif entry.find('updated') is not None:
            pub_date = entry.find('updated').text
        
        items.append({
            'title': title.strip() if title else "",
            'link': link.strip() if link else "",
            'description': desc.strip()[:500] if desc else "",
            'pubDate': pub_date,
            'feed': feed_title
        })
    return items


def filter_items(items, keyword=None, since=None, limit=None):
    """Filter items by keyword and date."""
    filtered = items
    
    if keyword:
        kw = keyword.lower()
        filtered = [i for i in filtered if kw in (i['title'] + i['description']).lower()]
    
    if since:
        since_date = parse_date(since)
        if since_date:
            filtered = [i for i in filtered if parse_date(i['pubDate']) and parse_date(i['pubDate']) >= since_date]
    
    # Sort by date (newest first)
    filtered.sort(key=lambda x: parse_date(x['pubDate']) or datetime.min, reverse=True)
    
    if limit:
        filtered = filtered[:limit]
    
    return filtered


def format_output(items, fmt='json'):
    """Format items for output."""
    if fmt == 'json':
        return json.dumps(items, indent=2, ensure_ascii=False)
    elif fmt == 'html':
        html = ['<html><body><h1>RSS Digest</h1><ul>']
        for item in items:
            html.append(f'<li><a href="{item["link"]}">{item["title"]}</a> ({item["feed"]})</li>')
        html.append('</ul></body></html>')
        return '\n'.join(html)
    elif fmt == 'markdown':
        md = ['# RSS Digest\n']
        for item in items:
            md.append(f'## [{item["title"]}]({item["link"]})')
            md.append(f'_{item["feed"]} | {item["pubDate"]}_\n')
            if item['description']:
                md.append(f'{item["description"]}\n')
            md.append('')
        return '\n'.join(md)
    else:
        return json.dumps(items, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description='RSS/Atom Feed Aggregator')
    parser.add_argument('--feeds', help='File with feed URLs (one per line)')
    parser.add_argument('--url', action='append', help='Single feed URL (can repeat)')
    parser.add_argument('--output', help='Output file')
    parser.add_argument('--format', choices=['json', 'html', 'markdown'], default='json')
    parser.add_argument('--limit', type=int, help='Maximum items to return')
    parser.add_argument('--keyword', help='Filter by keyword in title/description')
    parser.add_argument('--since', help='Only items after this date (ISO format)')
    
    args = parser.parse_args()
    
    # Collect feed URLs
    urls = []
    if args.url:
        urls.extend(args.url)
    if args.feeds:
        with open(args.feeds) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    urls.append(line)
    
    if not urls:
        print("Error: No feeds specified")
        return 1
    
    # Fetch all feeds
    all_items = []
    for url in urls:
        print(f"Fetching: {url}")
        items = fetch_feed(url)
        all_items.extend(items)
        print(f"  Found {len(items)} items")
    
    # Filter
    filtered = filter_items(all_items, args.keyword, args.since, args.limit)
    print(f"Total: {len(all_items)} items, {len(filtered)} after filtering")
    
    # Output
    output = format_output(filtered, args.format)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Saved to {args.output}")
    else:
        print(output)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
