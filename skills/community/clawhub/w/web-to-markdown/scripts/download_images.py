#!/usr/bin/env python3
"""
Download images from any website. Supports Pinterest size conversion and smart filtering.
"""

import argparse
import os
import re
import sys
import urllib.parse
from pathlib import Path

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
        # Clean URL
        url = url.rstrip('.,;:\'">)')
        if url not in seen and not url.endswith(')'):
            seen.add(url)
            unique_urls.append(url)
    
    return unique_urls


def convert_pinterest_size(url: str, size: str) -> str:
    """Convert Pinterest image URL to specified size."""
    if 'pinimg.com' not in url:
        return url
    
    size_pattern = r'/(\d+x|originals)/'
    return re.sub(size_pattern, f'/{size}/', url)


def is_valid_image(url: str, min_size: int = 0) -> bool:
    """Check if URL points to a valid image (optionally by size)."""
    # Skip common small images (icons, avatars, etc.)
    skip_patterns = [
        r'/avatar',
        r'/icon',
        r'/logo',
        r'/favicon',
        r'/emoji',
        r'/smiley',
        r'/button',
        r'/badge',
        r'/spinner',
        r'/loading',
        r'/blank\.',
        r'/pixel\.',
        r'/1x1',
        r'/spinner',
    ]
    
    for pattern in skip_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return False
    
    # Check file size if min_size specified
    if min_size > 0:
        try:
            resp = requests.head(url, timeout=10, allow_redirects=True)
            content_length = int(resp.headers.get('content-length', 0))
            if content_length > 0 and content_length < min_size:
                return False
        except:
            pass
    
    return True


def get_filename(url: str, index: int) -> str:
    """Generate filename from URL."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    filename = os.path.basename(path)
    
    if not filename or '.' not in filename:
        # Generate filename from URL hash
        ext = '.jpg'
        for e in ['.png', '.gif', '.webp', '.avif']:
            if e in url.lower():
                ext = e
                break
        filename = f"image_{index:03d}{ext}"
    
    return filename


def download_image(url: str, output_dir: Path, index: int) -> bool:
    """Download a single image."""
    try:
        filename = get_filename(url, index)
        output_path = output_dir / filename
        
        # Skip if exists
        if output_path.exists():
            print(f"  Skip (exists): {filename}")
            return True
        
        print(f"  Downloading: {url[:60]}...")
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"  Saved: {output_path}")
        return True
    
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='Download images from web pages')
    parser.add_argument('url', help='Web page URL')
    parser.add_argument('--output', '-o', default='~/.openclaw/images',
                        help='Output directory (default: ~/.openclaw/images)')
    parser.add_argument('--limit', '-l', type=int, default=50,
                        help='Maximum number of images to download (default: 50)')
    parser.add_argument('--min-size', '-m', type=int, default=10240,
                        help='Minimum file size in bytes (default: 10240 = 10KB, 0 to disable)')
    parser.add_argument('--ext', '-e', type=str, default='',
                        help='Only download specific extension (jpg/png/gif/webp)')
    parser.add_argument('--size', '-s', default='originals',
                        choices=['originals', '236x', '564x'],
                        help='Image size for Pinterest (default: originals)')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(os.path.expanduser(args.output))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Detect Pinterest
    is_pinterest = 'pinterest.com' in args.url
    
    # Fetch page content
    print(f"Fetching: {args.url}")
    content = fetch_page(args.url)
    
    if not content:
        print("Failed to fetch page content", file=sys.stderr)
        sys.exit(1)
    
    # Extract image URLs
    urls = extract_image_urls(content)
    
    if not urls:
        print("No images found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(urls)} images")
    
    # Convert Pinterest size
    if is_pinterest:
        urls = [convert_pinterest_size(url, args.size) for url in urls]
    
    # Filter by extension
    if args.ext:
        ext = args.ext.lower().lstrip('.')
        urls = [u for u in urls if f'.{ext}' in u.lower()]
        print(f"Filtered to {len(urls)} {args.ext} images")
    
    # Filter valid images
    if args.min_size > 0:
        print("Checking image sizes...")
        valid_urls = []
        for url in urls:
            if is_valid_image(url, args.min_size):
                valid_urls.append(url)
        urls = valid_urls
        print(f"Filtered to {len(urls)} valid images (>{args.min_size} bytes)")
    else:
        urls = [u for u in urls if is_valid_image(u, 0)]
    
    # Limit
    urls = urls[:args.limit]
    
    if not urls:
        print("No valid images to download", file=sys.stderr)
        sys.exit(1)
    
    # Download
    print(f"\nDownloading {len(urls)} images to {output_dir}...")
    success = 0
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}]")
        if download_image(url, output_dir, i):
            success += 1
    
    print(f"\n✓ Downloaded {success}/{len(urls)} images to {output_dir}")


if __name__ == "__main__":
    main()
