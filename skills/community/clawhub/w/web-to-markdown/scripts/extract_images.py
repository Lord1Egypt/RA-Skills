#!/usr/bin/env python3
"""
Extract image URLs from any website.
"""

import argparse
import os
import re
import sys

try:
    import requests
except ImportError:
    print("Please install requests: pip install requests", file=sys.stderr)
    sys.exit(1)


def fetch_page(url: str) -> str:
    """Fetch page content using r.jina.ai."""
    fetch_url = f"https://r.jina.ai/{url}"
    try:
        response = requests.get(fetch_url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching page: {e}", file=sys.stderr)
        return ""


def extract_image_urls(content: str) -> list[str]:
    """Extract all image URLs from page content."""
    # Match various image URL patterns
    patterns = [
        r'https://[^\s\)"\'<>]+\.(?:jpg|jpeg|png|gif|webp|avif)(?:\?[^\s\)"\'<>]*)?',
        r'https://[^\s\)"\'<>]+/img/[^\s\)"\'<>]+',
        r'https://[^\s\)"\'<>]+/images/[^\s\)"\'<>]+',
        r'https://[^\s\)"\'<>]+/photos/[^\s\)"\'<>]+',
    ]
    
    urls = []
    for pattern in patterns:
        urls.extend(re.findall(pattern, content, re.IGNORECASE))
    
    # Deduplicate while preserving order
    seen = set()
    unique_urls = []
    for url in urls:
        # Clean URL (remove trailing punctuation)
        url = url.rstrip('.,;:\'">)')
        if url not in seen and not url.endswith(')'):  # Avoid markdown links
            seen.add(url)
            unique_urls.append(url)
    
    return unique_urls


def main():
    parser = argparse.ArgumentParser(description='Extract image URLs from web pages')
    parser.add_argument('url', help='Web page URL')
    parser.add_argument('--output', '-o', help='Output file for URLs (default: stdout)')
    parser.add_argument('--limit', '-l', type=int, default=0,
                        help='Maximum number of URLs to extract (0 = unlimited)')
    
    args = parser.parse_args()
    
    # Fetch page content
    print(f"Fetching: {args.url}", file=sys.stderr)
    content = fetch_page(args.url)
    
    if not content:
        print("Failed to fetch page content", file=sys.stderr)
        sys.exit(1)
    
    # Extract image URLs
    urls = extract_image_urls(content)
    
    if not urls:
        print("No images found", file=sys.stderr)
        sys.exit(1)
    
    # Limit
    if args.limit > 0:
        urls = urls[:args.limit]
    
    # Output
    output = '\n'.join(urls)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Saved {len(urls)} URLs to {args.output}", file=sys.stderr)
    else:
        print(output)
    
    print(f"Found {len(urls)} images", file=sys.stderr)


if __name__ == "__main__":
    main()
