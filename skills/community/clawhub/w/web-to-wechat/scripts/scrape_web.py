#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrape_web.py — Extract article content from any URL and output clean Markdown.

Supports: WeChat articles, news sites, tech blogs, generic web pages.
Auto-detects site type and uses appropriate selectors.

Usage:
    python scrape_web.py --url "https://example.com/article" --output article.md
    python scrape_web.py --url "https://mp.weixin.qq.com/s/xxx" --output article.md
    python scrape_web.py --url "https://example.com" --output article.md --selector ".article-body"

Dependencies: requests, beautifulsoup4, html2text (auto-installed)
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urljoin

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, Exception):
        pass

try:
    import requests
except ImportError:
    print("[INFO] Installing requests...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("[INFO] Installing beautifulsoup4...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "beautifulsoup4", "-q"])
    from bs4 import BeautifulSoup

try:
    import html2text
except ImportError:
    print("[INFO] Installing html2text...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "html2text", "-q"])
    import html2text


# ── Site-specific selectors for precise extraction ──
SITE_SELECTORS = {
    "mp.weixin.qq.com": {
        "title": "#activity-name",
        "author": "#js_name",
        "content": "#js_content",
        "publish_date": "#publish_time",
        "cover": 'meta[property="og:image"]',
    },
    "toutiao.com": {
        "title": "h1",
        "author": 'a[href*="user"]',
        "content": ".article-content",
        "publish_date": "time",
    },
    "zhihu.com": {
        "title": "h1",
        "author": ".AuthorInfo-name",
        "content": ".RichText",
        "publish_date": ".ContentItem-time",
    },
    "juejin.cn": {
        "title": "h1",
        "author": ".username",
        "content": ".article-content",
        "publish_date": ".time",
    },
    "csdn.net": {
        "title": "h1",
        "author": ".follow-nickName",
        "content": "#content_views",
        "publish_date": ".time",
    },
    "medium.com": {
        "title": "h1",
        "author": 'meta[name="author"]',
        "content": "article",
        "publish_date": "time",
    },
}

GENERIC_SELECTORS = [
    "article",
    '[role="main"]',
    ".post-content",
    ".article-content",
    ".entry-content",
    ".content",
    "main",
    ".main-content",
    "#content",
    ".post",
    ".story-body",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


def detect_site(url: str) -> str:
    """Detect the site domain and return matching key."""
    domain = urlparse(url).hostname or ""
    for site in SITE_SELECTORS:
        if site in domain:
            return site
    return "generic"


def fetch_page(url: str, timeout: int = 30) -> tuple:
    """Fetch page HTML and return (html_text, response)."""
    print(f"[FETCH] Fetching: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()
        # Detect encoding
        if resp.encoding and resp.encoding.lower() == "iso-8859-1":
            resp.encoding = resp.apparent_encoding
        html = resp.text
        print(f"[OK] Fetched {len(html)} bytes, encoding: {resp.encoding}")
        return html, resp
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out after {timeout}s")
        return "", None
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error: {e}")
        return "", None
    except Exception as e:
        print(f"[ERROR] Fetch failed: {e}")
        return "", None


def extract_content(html: str, url: str, custom_selector: str = "") -> dict:
    """Extract title, author, content, and metadata from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    site = detect_site(url)
    result = {
        "title": "",
        "author": "",
        "publish_date": "",
        "content_html": "",
        "cover_url": "",
        "source_url": url,
    }

    selectors = SITE_SELECTORS.get(site, {})

    # Title
    if custom_selector:
        pass  # custom_selector is for content only
    title_el = soup.select_one(selectors.get("title", "h1")) if selectors else soup.find("h1")
    if not title_el:
        title_el = soup.find("title")
    if title_el:
        result["title"] = title_el.get_text(strip=True)

    # og:title fallback
    if not result["title"]:
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            result["title"] = og_title["content"]

    # Author
    author_sel = selectors.get("author", "")
    if author_sel:
        author_el = soup.select_one(author_sel)
        if author_el:
            result["author"] = author_el.get_text(strip=True)
    if not result["author"]:
        meta_author = soup.find("meta", attrs={"name": "author"})
        if meta_author and meta_author.get("content"):
            result["author"] = meta_author["content"]

    # Publish date
    date_sel = selectors.get("publish_date", "")
    if date_sel:
        date_el = soup.select_one(date_sel)
        if date_el:
            result["publish_date"] = date_el.get_text(strip=True)
    if not result["publish_date"]:
        meta_date = soup.find("meta", attrs={"property": "article:published_time"})
        if meta_date and meta_date.get("content"):
            result["publish_date"] = meta_date["content"][:10]

    # Cover image (og:image)
    cover_sel = selectors.get("cover", 'meta[property="og:image"]')
    cover_el = soup.select_one(cover_sel) if cover_sel else soup.find("meta", property="og:image")
    if cover_el:
        cover_url = cover_el.get("content", "")
        if cover_url and not cover_url.startswith("http"):
            cover_url = urljoin(url, cover_url)
        result["cover_url"] = cover_url

    # Content
    content_el = None
    if custom_selector:
        content_el = soup.select_one(custom_selector)
        if not content_el:
            print(f"[WARN] Custom selector '{custom_selector}' not found, falling back to auto-detect")

    if not content_el and selectors.get("content"):
        content_el = soup.select_one(selectors["content"])

    if not content_el:
        for sel in GENERIC_SELECTORS:
            content_el = soup.select_one(sel)
            if content_el:
                # Verify it has enough content (>200 chars of text)
                text_len = len(content_el.get_text(strip=True))
                if text_len > 200:
                    break
                content_el = None

    if not content_el:
        content_el = soup.find("body")

    if content_el:
        # Remove ads, scripts, nav, footer, sidebar elements
        for tag in content_el.find_all(["script", "style", "nav", "footer", "aside",
                                         "iframe", "noscript", "form"]):
            tag.decompose()
        for cls in ["sidebar", "footer", "nav", "ad", "advertisement", "comment",
                     "comments", "related", "recommend"]:
            for el in content_el.find_all(class_=re.compile(cls, re.I)):
                el.decompose()

        # Fix relative image URLs
        for img in content_el.find_all("img"):
            src = img.get("src") or img.get("data-src") or ""
            if src and not src.startswith("http") and not src.startswith("data:"):
                img["src"] = urljoin(url, src)
            elif img.get("data-src") and not img.get("src"):
                img["src"] = img["data-src"]

        # Remove lazy-load attributes
        for img in content_el.find_all("img"):
            for attr in ["data-src", "data-original", "data-lazy-src"]:
                if img.has_attr(attr):
                    del img[attr]

        result["content_html"] = str(content_el)
        print(f"[OK] Extracted content: {len(result['content_html'])} chars HTML")
    else:
        print("[ERROR] Could not find any content element")

    return result


def html_to_markdown(content_html: str) -> str:
    """Convert HTML content to clean Markdown."""
    h = html2text.HTML2Text()
    h.body_width = 0  # Don't wrap lines
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.unicode_snob = True
    h.skip_internal_links = True
    h.inline_links = True
    h.mark_code = False
    h.wrap_links = False
    h.wrap_list_items = False

    md = h.handle(content_html)

    # Clean up excessive blank lines
    md = re.sub(r'\n{3,}', '\n\n', md)
    # Clean up trailing whitespace
    md = '\n'.join(line.rstrip() for line in md.splitlines())

    return md.strip()


def build_markdown(result: dict) -> str:
    """Build final Markdown with metadata frontmatter."""
    md_parts = []

    # Title as H1
    if result["title"]:
        md_parts.append(f"# {result['title']}")

    # Metadata line
    meta_parts = []
    if result["author"]:
        meta_parts.append(f"**作者：** {result['author']}")
    if result["publish_date"]:
        meta_parts.append(f"**发布时间：** {result['publish_date']}")
    if result["source_url"]:
        meta_parts.append(f"**来源：** [原文链接]({result['source_url']})")
    if meta_parts:
        md_parts.append(" | ".join(meta_parts))

    md_parts.append("")  # blank line before content

    # Content
    content_md = html_to_markdown(result["content_html"])
    md_parts.append(content_md)

    return "\n\n".join(md_parts)


def main():
    parser = argparse.ArgumentParser(
        description="Scrape web content and convert to clean Markdown",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scrape_web.py --url "https://example.com/article" --output article.md
  python scrape_web.py --url "https://mp.weixin.qq.com/s/xxx" --output article.md
  python scrape_web.py --url "https://example.com" --selector ".article-body" --output article.md

Supported sites:
  WeChat articles, Toutiao, Zhihu, Juejin, CSDN, Medium, and any generic website.
        """,
    )
    parser.add_argument("--url", required=True, help="URL to scrape")
    parser.add_argument("--output", required=True, help="Output Markdown file path")
    parser.add_argument("--selector", default="", help="Custom CSS selector for content (optional)")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds (default: 30)")
    parser.add_argument("--json", action="store_true", help="Output as JSON instead of Markdown")

    args = parser.parse_args()

    # Fetch page
    html, resp = fetch_page(args.url, args.timeout)
    if not html:
        print("[ERROR] Failed to fetch page. Check the URL and try again.")
        sys.exit(1)

    # Extract content
    result = extract_content(html, args.url, args.selector)

    if not result["content_html"]:
        print("[ERROR] Could not extract any content from the page.")
        sys.exit(1)

    # Output
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    if args.json:
        import json
        result["markdown"] = build_markdown(result)
        del result["content_html"]  # Don't include raw HTML in JSON
        out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[DONE] JSON output: {args.output}")
    else:
        md = build_markdown(result)
        out.write_text(md, encoding="utf-8")
        print(f"[DONE] Markdown output: {args.output}")

    print(f"[INFO] Title: {result['title']}")
    print(f"[INFO] Author: {result['author'] or 'unknown'}")
    print(f"[INFO] Date: {result['publish_date'] or 'unknown'}")
    if result["cover_url"]:
        print(f"[INFO] Cover: {result['cover_url']}")
    print(f"[INFO] Content: {len(result['content_html'])} chars HTML → {len(build_markdown(result))} chars Markdown")


if __name__ == "__main__":
    main()
