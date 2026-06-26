#!/usr/bin/env python3
"""
Web scraper using Scrapling as fallback when URL prefix services fail.
"""

import sys
from scrapling import Fetcher

def scrape(url: str) -> str:
    """Scrape a webpage and return content as markdown-like text."""
    fetcher = Fetcher(auto_match=None)
    page = fetcher.fetch(url)
    
    # Get main content
    body = page.css_first('body')
    if not body:
        return ""
    
    # Extract text with structure
    lines = []
    for element in body.walk():
        tag = element.tag.lower() if element.tag else ""
        text = element.text.strip() if element.text else ""
        
        if not text:
            continue
            
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            lines.append(f"\n{'#' * level} {text}\n")
        elif tag == 'p':
            lines.append(f"\n{text}\n")
        elif tag == 'li':
            lines.append(f"- {text}")
        elif tag in ('strong', 'b'):
            lines.append(f"**{text}**")
        elif tag in ('em', 'i'):
            lines.append(f"*{text}*")
        elif tag == 'code':
            lines.append(f"`{text}`")
        elif tag == 'a':
            href = element.attrib.get('href', '')
            lines.append(f"[{text}]({href})")
        else:
            lines.append(text)
    
    return '\n'.join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape.py <url>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"# Scraped from: {url}\n", file=sys.stderr)
    
    try:
        content = scrape(url)
        print(content)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
