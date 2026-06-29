#!/usr/bin/env python3
"""
Extract clean article content from a URL.
Removes ads, navigation, and clutter - returns just the article text.
"""

import sys
import json
import re
import urllib.request
import urllib.parse
from html.parser import HTMLParser
from datetime import datetime

class ArticleExtractor:
    def __init__(self, url):
        self.url = url
        self.title = ""
        self.content = ""
        self.author = ""
        self.date = ""
        
    def fetch(self):
        """Fetch the HTML content from URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            req = urllib.request.Request(self.url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Error fetching URL: {e}", file=sys.stderr)
            return None
    
    def extract(self):
        """Extract article content from HTML."""
        html = self.fetch()
        if not html:
            return None
            
        # Simple extraction - look for common article containers
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Extract title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE)
        if title_match:
            self.title = self._clean_text(title_match.group(1))
        
        # Try to find main content
        # Look for article, main, or content divs
        content_patterns = [
            r'<article[^>]*>(.*?)</article>',
            r'<main[^>]*>(.*?)</main>',
            r'<div[^>]*class=["\'][^"\']*(?:content|article|post)[^"\']*["\'][^>]*>(.*?)</div>',
            r'<div[^>]*id=["\'][^"\']*(?:content|article|post)[^"\']*["\'][^>]*>(.*?)</div>',
        ]
        
        for pattern in content_patterns:
            match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
            if match:
                self.content = self._html_to_text(match.group(1))
                break
        
        # Fallback: extract all paragraph text
        if not self.content:
            paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL | re.IGNORECASE)
            self.content = '\n\n'.join([self._html_to_text(p) for p in paragraphs if len(p) > 50])
        
        # Extract author if available
        author_patterns = [
            r'(?:author|by)["\']?\s*[:\-]?\s*["\']?([^"\'<>,]+)',
            r'class=["\'][^"\']*author[^"\']*["\'][^>]*>([^<]+)',
        ]
        for pattern in author_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                self.author = self._clean_text(match.group(1))
                break
        
        return {
            'title': self.title or 'Untitled',
            'content': self.content,
            'author': self.author,
            'url': self.url,
            'date': datetime.now().isoformat(),
            'word_count': len(self.content.split())
        }
    
    def _html_to_text(self, html):
        """Convert HTML to plain text."""
        # Remove remaining tags
        text = re.sub(r'<[^>]+>', ' ', html)
        # Decode common entities
        text = text.replace('&nbsp;', ' ')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _clean_text(self, text):
        """Clean up extracted text."""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: extract_article.py <url>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    extractor = ArticleExtractor(url)
    result = extractor.extract()
    
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({'error': 'Failed to extract article'}), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
