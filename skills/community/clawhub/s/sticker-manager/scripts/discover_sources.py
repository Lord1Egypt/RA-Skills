#!/usr/bin/env python3
"""Discover sticker sources from various channels."""
from __future__ import annotations
import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests

from common import get_lang, SUPPORTED_EXTS

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
DEFAULT_TIMEOUT = 30
DEFAULT_MAX_SIZE = 10 * 1024 * 1024  # 10MB

MESSAGES_DISCOVER: Dict[str, Dict[str, str]] = {
    "discover_title": {"zh": "🔍 发现表情包来源:", "en": "🔍 Discovering sticker sources:"},
    "discover_url_success": {"zh": "  ✓ URL: {url} ({size_kb}KB)", "en": "  ✓ URL: {url} ({size_kb}KB)"},
    "discover_url_fail": {"zh": "  ✗ URL 失败: {url} ({error})", "en": "  ✗ URL failed: {url} ({error})"},
    "discover_dir_found": {"zh": "  ✓ 目录: {path} ({count} 个文件)", "en": "  ✓ Directory: {path} ({count} files)"},
    "discover_dir_empty": {"zh": "  ✗ 目录为空: {path}", "en": "  ✗ Directory empty: {path}"},
    "discover_page_found": {"zh": "  ✓ 页面: {url} ({count} 张图片)", "en": "  ✓ Page: {url} ({count} images)"},
    "discover_page_no_images": {"zh": "  ✗ 页面无图片: {url}", "en": "  ✗ No images found on page: {url}"},
    "discover_output": {"zh": "\n📝 发现结果已保存到: {path}", "en": "\n📝 Discovery results saved to: {path}"},
    "discover_summary": {"zh": "\n📊 汇总: {urls} 个URL, {dirs} 个目录, {pages} 个页面, 共 {total} 个来源", "en": "\n📊 Summary: {urls} URLs, {dirs} directories, {pages} pages, {total} total sources"},
    "discover_no_sources": {"zh": "未发现有效来源", "en": "No valid sources discovered"},
    "import_url_help": {"zh": "URL 格式: https://example.com/image.gif", "en": "URL format: https://example.com/image.gif"},
    "import_dir_help": {"zh": "目录格式: /path/to/stickers/", "en": "Directory format: /path/to/stickers/"},
    "import_page_help": {"zh": "页面格式: https://example.com/gallery (抓取静态页面图片)", "en": "Page format: https://example.com/gallery (scrape static page images)"},
}


def t_discover(key: str, lang: str, **kwargs) -> str:
    entry = MESSAGES_DISCOVER.get(key, {})
    template = entry.get(lang) or entry.get('en') or key
    return template.format(**kwargs)


def is_image_url(url: str) -> bool:
    """Check if URL points to a supported image format."""
    parsed = urlparse(url)
    ext = os.path.splitext(parsed.path)[1].lower()
    return ext in SUPPORTED_EXTS


def is_image_file(path: Path) -> bool:
    """Check if file has a supported image extension."""
    return path.suffix.lower() in SUPPORTED_EXTS


def fetch_url_info(url: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[Dict]:
    """Fetch URL and return info dict if it's a valid image."""
    try:
        head = requests.head(url, headers={'User-Agent': DEFAULT_USER_AGENT}, timeout=timeout, allow_redirects=True)
        content_type = head.headers.get('Content-Type', '')
        if not any(ct in content_type for ct in ['image/', 'application/octet-stream']):
            # Try GET if HEAD doesn't give content type
            pass
        if head.status_code == 200:
            size = int(head.headers.get('Content-Length', 0))
            return {'url': url, 'size': size, 'status': 'ok'}
    except Exception:
        pass
    
    # Try GET request
    try:
        r = requests.get(url, headers={'User-Agent': DEFAULT_USER_AGENT}, timeout=timeout, stream=True)
        if r.status_code == 200:
            # Read just enough to get size estimate
            size = int(r.headers.get('Content-Length', 0))
            return {'url': url, 'size': size, 'status': 'ok'}
    except Exception as e:
        return {'url': url, 'size': 0, 'status': 'error', 'error': str(e)}
    return None


def scan_directory(directory: str, recursive: bool = True) -> List[Dict]:
    """Scan a directory for image files."""
    results = []
    base = Path(directory).expanduser()
    if not base.exists():
        return results
    
    if recursive:
        pattern = '**/*'
    else:
        pattern = '*'
    
    for f in base.glob(pattern):
        if f.is_file() and is_image_file(f):
            results.append({
                'path': str(f),
                'name': f.name,
                'size': f.stat().st_size,
                'status': 'ok'
            })
    return results


def scrape_page_images(url: str, timeout: int = DEFAULT_TIMEOUT) -> List[Dict]:
    """Scrape static page for image URLs."""
    results = []
    try:
        r = requests.get(url, headers={'User-Agent': DEFAULT_USER_AGENT}, timeout=timeout)
        r.raise_for_status()
        
        # Find image URLs in img tags
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        matches = re.findall(img_pattern, r.text)
        
        for match in matches:
            # Convert relative to absolute URL
            img_url = urljoin(url, match)
            if is_image_url(img_url):
                results.append({'url': img_url, 'status': 'pending'})
        
        # Also look for background-image URLs in style attributes
        bg_pattern = r'background-image:\s*url\(["\']?([^"\')\s]+)["\']?\)'
        bg_matches = re.findall(bg_pattern, r.text)
        for match in bg_matches:
            img_url = urljoin(url, match)
            if is_image_url(img_url):
                results.append({'url': img_url, 'status': 'pending'})
                
    except Exception as e:
        return [{'url': url, 'status': 'error', 'error': str(e)}]
    
    return results


def discover_from_urls(urls: List[str], lang: str, fetch_urls: bool = False) -> List[Dict]:
    """Discover image sources from URL list."""
    results = []
    for url in urls:
        if fetch_urls:
            info = fetch_url_info(url)
            if info and info.get('status') == 'ok':
                size_kb = info['size'] // 1024
                print(t_discover('discover_url_success', lang, url=url, size_kb=size_kb))
                results.append(info)
            else:
                error = info.get('error', 'unknown') if info else 'fetch failed'
                print(t_discover('discover_url_fail', lang, url=url, error=error))
            continue

        pending = {'url': url, 'size': 0, 'status': 'pending'}
        print(t_discover('discover_url_success', lang, url=url, size_kb=0))
        results.append(pending)
    return results


def discover_from_directories(directories: List[str], recursive: bool, lang: str) -> List[Dict]:
    """Discover image sources from local directories."""
    results = []
    for d in directories:
        files = scan_directory(d, recursive=recursive)
        if files:
            print(t_discover('discover_dir_found', lang, path=d, count=len(files)))
            results.extend(files)
        else:
            print(t_discover('discover_dir_empty', lang, path=d))
    return results


def discover_from_pages(pages: List[str], lang: str) -> List[Dict]:
    """Discover image sources from web pages."""
    results = []
    for page in pages:
        images = scrape_page_images(page)
        valid_images = [item for item in images if item.get('status') != 'error']
        if valid_images:
            print(t_discover('discover_page_found', lang, url=page, count=len(valid_images)))
            results.extend(valid_images)
        elif images:
            error = images[0].get('error', 'fetch failed')
            print(t_discover('discover_url_fail', lang, url=page, error=error))
        else:
            print(t_discover('discover_page_no_images', lang, url=page))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description='Discover sticker sources from URLs, directories, and web pages.')
    parser.add_argument('sources', nargs='*', help='URLs, directories, or page URLs to discover')
    parser.add_argument('--urls-file', help='File containing URLs (one per line)')
    parser.add_argument('--dirs-file', help='File containing directories (one per line)')
    parser.add_argument('--pages-file', help='File containing page URLs to scrape (one per line)')
    parser.add_argument('--output', '-o', help='Output JSON file for discovered sources')
    parser.add_argument('--recursive', '-r', action='store_true', default=True, help='Scan directories recursively (default: True)')
    parser.add_argument('--no-recursive', action='store_false', dest='recursive', help='Do not scan directories recursively')
    parser.add_argument('--lang')
    parser.add_argument('--fetch-urls', action='store_true', help='Actually fetch URL content to verify (slower)')
    args = parser.parse_args()

    lang = get_lang(args.lang)
    
    urls = []
    dirs = []
    pages = []
    
    # Parse command line sources
    for source in args.sources:
        expanded = os.path.expanduser(source)
        if source.startswith('http://') or source.startswith('https://'):
            if is_image_url(source):
                urls.append(source)
            else:
                pages.append(source)
        elif os.path.isdir(expanded):
            dirs.append(expanded)
        elif os.path.isfile(expanded):
            # Single file - treat as URL file
            with open(expanded, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if line.startswith('http'):
                            urls.append(line)
                        elif os.path.isdir(os.path.expanduser(line)):
                            dirs.append(os.path.expanduser(line))
    
    # Load from files
    if args.urls_file:
        for line in Path(args.urls_file).read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and (line.startswith('http')):
                urls.append(line)
    
    if args.dirs_file:
        for line in Path(args.dirs_file).read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                expanded = os.path.expanduser(line)
                if os.path.isdir(expanded):
                    dirs.append(expanded)
    
    if args.pages_file:
        for line in Path(args.pages_file).read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and (line.startswith('http')):
                pages.append(line)
    
    print(t_discover('discover_title', lang))
    
    all_results = []
    
    # Discover from URLs
    url_results = discover_from_urls(urls, lang, fetch_urls=args.fetch_urls) if urls else []
    all_results.extend(url_results)
    
    # Discover from directories
    dir_results = discover_from_directories(dirs, args.recursive, lang) if dirs else []
    all_results.extend(dir_results)
    
    # Discover from pages
    page_results = discover_from_pages(pages, lang) if pages else []
    all_results.extend(page_results)
    
    # Summary
    total = len(all_results)
    if total == 0:
        print(t_discover('discover_no_sources', lang))
        return 1
    
    print(t_discover('discover_summary', lang, 
        urls=len(url_results), 
        dirs=len(dir_results), 
        pages=len(page_results), 
        total=total))
    
    # Output
    output_data = {
        'urls': url_results,
        'directories': dir_results,
        'pages': page_results,
        'total': total,
    }
    
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(t_discover('discover_output', lang, path=args.output))
    else:
        print('\n' + json.dumps(output_data, ensure_ascii=False, indent=2))
    
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
