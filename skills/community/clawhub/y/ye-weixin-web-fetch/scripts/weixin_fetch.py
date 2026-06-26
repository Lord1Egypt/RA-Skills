#!/usr/bin/env python3
"""
Fetch complete content from WeChat public account articles (mp.weixin.qq.com)
Specialized version that handles WeChat's anti-bot checks and content extraction
"""

import httpx
import argparse
import json
import re
import html
from typing import Tuple, Optional
from urllib.parse import urlparse
from readability import Document

# User-Agent that simulates a real browser
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
MAX_REDIRECTS = 5
MAX_CHARS = 50000


def strip_tags(text: str) -> str:
    """Remove HTML tags and decode entities."""
    text = re.sub(r'<script[\s\S]*?</script>', '', text, flags=re.I)
    text = re.sub(r'<style[\s\S]*?</style>', '', text, flags=re.I)
    text = re.sub(r'<[^>]+>', '', text)
    return html.unescape(text).strip()


def normalize(text: str) -> str:
    """Normalize whitespace."""
    text = re.sub(r'[ \t]+', ' ', text)
    return re.sub(r'\n{3,}', '\n\n', text).strip()


def validate_url(url: str) -> Tuple[bool, str]:
    """Validate URL: must be http(s) with valid domain."""
    try:
        p = urlparse(url)
        if p.scheme not in ('http', 'https'):
            return False, f"Only http/https allowed, got '{p.scheme or 'none'}'"
        if not p.netloc:
            return False, "Missing domain"
        return True, ""
    except Exception as e:
        return False, str(e)


def html_to_markdown(html_content: str) -> str:
    """Convert HTML to markdown."""
    # Convert links, headings, lists before stripping tags
    text = re.sub(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([\s\S]*?)</a>',
                  lambda m: f'[{strip_tags(m[2])}]({m[1]})', html_content, flags=re.I)
    text = re.sub(r'<h([1-6])[^>]*>([\s\S]*?)</h\1>',
                  lambda m: f'\n{"#" * int(m[1])} {strip_tags(m[2])}\n', text, flags=re.I)
    text = re.sub(r'<li[^>]*>([\s\S]*?)</li>', lambda m: f'\n- {strip_tags(m[1])}', text, flags=re.I)
    text = re.sub(r'</(p|div|section|article|p)>', '\n\n', text, flags=re.I)
    text = re.sub(r'<(br|hr)\s*/?>', '\n', text, flags=re.I)
    return normalize(strip_tags(text))


def extract_author(html_content: str) -> Optional[str]:
    """Extract author information from WeChat article."""
    # Common patterns for WeChat author
    patterns = [
        r'<meta[^>]+name=["\']author["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+property=["\']og:author["\'][^>]+content=["\']([^"\']+)["\']',
        r'id=["\']js_name["\'][^>]*>([^<]+)</',
        r'class=["\']rich_media_meta rich_media_meta_text["\'][^>]*>([^<]+)</',
        r'作者[:：]\s*([^<\n]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, html_content, re.I)
        if match:
            author = match.group(1).strip()
            if author and len(author) < 100:
                return author
    return None


def extract_weixin_content(html_content: str) -> str:
    """Special extraction for WeChat articles - finds the main content div."""
    # WeChat stores the main content in #js_content or .rich_media_content
    match = re.search(
        r'<div[^>]+class=["\'][^"\']*rich_media_content[^"\']*["\'][^>]*id=["\']js_content["\'][^>]*>([\s\S]*?)</div\s*>',
        html_content,
        re.I
    )
    if not match:
        # Try without id constraint
        match = re.search(
            r'<div[^>]+class=["\'][^"\']*rich_media_content[^"\']*["\'][^>]*>([\s\S]*?)</div\s*>',
            html_content,
            re.I
        )
    
    if match:
        return match.group(1)
    return None


def fetch_weixin_article(url: str, max_chars: int = MAX_CHARS) -> dict:
    """Fetch a WeChat article and extract clean content."""
    is_valid, error_msg = validate_url(url)
    if not is_valid:
        return {"error": f"URL validation failed: {error_msg}", "url": url, "blocked": False}

    # WeChat specific headers - simulate real browser
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
    }

    try:
        with httpx.Client(
            follow_redirects=True,
            max_redirects=MAX_REDIRECTS,
            timeout=30.0
        ) as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()

        html_content = response.text
        final_url = str(response.url)
        status_code = response.status_code

        # Check if it's completely blocked (only QR code visible)
        qr_block = "微信扫一扫" in html_content and "使用小程序" in html_content

        # Extract title
        title_match = re.search(r'<title>([^<]+)</title>', html_content, re.I)
        title = title_match.group(1).strip() if title_match else None

        # Special WeChat content extraction - directly extract rich_media_content
        weixin_content_html = extract_weixin_content(html_content)
        author = extract_author(html_content)

        if weixin_content_html:
            # We found the WeChat content div, use that instead of Readability
            content_markdown = html_to_markdown(weixin_content_html)
            extractor = "weixin-direct"
        else:
            # Fallback to Readability
            doc = Document(html_content)
            if not title:
                title = doc.title() if doc.title() != "[no-title]" else None
            content_html = doc.summary()
            content_markdown = html_to_markdown(content_html)
            extractor = "readability"

        # Check if we only got the QR code despite extracting content
        if len(content_markdown.strip()) < 200 and ("微信扫一扫" in content_markdown or "使用小程序" in content_markdown):
            return {
                "error": "需要微信扫码登录",
                "message": "该文章需要在微信客户端内访问，外部访问会被拦截。请在微信中打开文章后复制完整内容发给我，或者使用浏览器登录微信网页版后再试。",
                "url": url,
                "blocked": True
            }

        # Truncate if needed
        truncated = len(content_markdown) > max_chars
        if truncated:
            content_markdown = content_markdown[:max_chars]

        result = {
            "url": url,
            "final_url": final_url,
            "status": status_code,
            "title": title,
            "author": author,
            "content": content_markdown,
            "length": len(content_markdown),
            "truncated": truncated,
            "blocked": False,
            "extractor": extractor
        }

        return result

    except Exception as e:
        return {"error": str(e), "url": url, "blocked": False}


def main():
    parser = argparse.ArgumentParser(description='Fetch content from WeChat public account articles.')
    parser.add_argument('url', help='URL of the WeChat article (mp.weixin.qq.com)')
    parser.add_argument('--max-chars', type=int, default=MAX_CHARS, help='Maximum characters to return')
    args = parser.parse_args()

    result = fetch_weixin_article(args.url, args.max_chars)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
