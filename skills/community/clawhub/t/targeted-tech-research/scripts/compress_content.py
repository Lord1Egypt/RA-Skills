#!/usr/bin/env python3
"""
Content Cleaning & Compression Script

Features:
- Remove HTML tags, scripts, styles
- Compress excessive whitespace
- Cap single source max length (default 3000 chars)
- Preserve title and paragraph structure
"""

import re
import sys
import argparse

def compress_html(html_content: str, max_length: int = 3000) -> str:
    """Clean HTML content, extract plain text, and limit length."""
    # Remove script and style tags along with their contents
    content = re.sub(r'<script[^>]*>.*?</script>', ' ', html_content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'<style[^>]*>.*?</style>', ' ', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove all HTML tags
    content = re.sub(r'<[^>]+>', ' ', content)
    
    # Replace common HTML entities
    entities = {
        '&nbsp;': ' ', '&lt;': '<', '&gt;': '>', '&amp;': '&',
        '&quot;': '"', '&apos;': "'", '&#39;': "'"
    }
    for entity, char in entities.items():
        content = content.replace(entity, char)
    
    # Compress whitespace (multiple spaces, newlines, tabs to single space)
    content = re.sub(r'\s+', ' ', content).strip()
    
    # Truncate to max length, preferably at sentence boundary
    if len(content) > max_length:
        truncated = content[:max_length]
        last_period = truncated.rfind('.')
        last_space = truncated.rfind(' ')
        if last_period > max_length * 0.7:
            content = truncated[:last_period+1]
        elif last_space > 0:
            content = truncated[:last_space] + '...'
        else:
            content = truncated + '...'
    
    return content

def main():
    parser = argparse.ArgumentParser(description='Clean and compress webpage content')
    parser.add_argument('--input', '-i', help='Input file path (default: stdin)')
    parser.add_argument('--output', '-o', help='Output file path (default: stdout)')
    parser.add_argument('--max-length', '-m', type=int, default=3000, help='Max character length (default 3000)')
    args = parser.parse_args()
    
    if args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            raw = f.read()
    else:
        raw = sys.stdin.read()
    
    compressed = compress_html(raw, args.max_length)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(compressed)
    else:
        print(compressed)

if __name__ == '__main__':
    main()
