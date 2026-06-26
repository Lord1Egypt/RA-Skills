#!/usr/bin/env python3
"""
sitemap_gen.py — Crawl a website and generate an XML sitemap.

Usage:
    python3 sitemap_gen.py https://example.com
    python3 sitemap_gen.py https://example.com --max-pages 500 --output sitemap.xml
    python3 sitemap_gen.py https://example.com --max-depth 3 --delay 0.5
"""

import argparse
import sys
import time
import xml.etree.ElementTree as ET
from collections import deque
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

try:
    import requests
except ImportError:
    print("ERROR: 'requests' is required. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: 'beautifulsoup4' is required. Install with: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)


def normalize_url(url: str) -> str:
    """Normalize a URL by removing fragments and trailing slashes."""
    parsed = urlparse(url)
    # Remove fragment, normalize path
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.scheme}://{parsed.netloc}{path}"


def is_same_domain(url: str, base_domain: str) -> bool:
    """Check if URL belongs to the same domain."""
    parsed = urlparse(url)
    return parsed.netloc == base_domain or parsed.netloc == ""


def should_skip(url: str) -> bool:
    """Skip non-HTML resources and common junk paths."""
    skip_extensions = {
        ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico",
        ".css", ".js", ".pdf", ".zip", ".tar", ".gz", ".mp3", ".mp4",
        ".avi", ".mov", ".woff", ".woff2", ".ttf", ".eot", ".map",
    }
    parsed = urlparse(url)
    path_lower = parsed.path.lower()
    return any(path_lower.endswith(ext) for ext in skip_extensions)


def crawl(start_url: str, max_pages: int, max_depth: int, delay: float, timeout: int, verbose: bool):
    """BFS crawl from start_url, return set of discovered URLs."""
    parsed_start = urlparse(start_url)
    base_domain = parsed_start.netloc
    visited = set()
    queue = deque()
    start_normalized = normalize_url(start_url)
    queue.append((start_normalized, 0))
    visited.add(start_normalized)

    headers = {
        "User-Agent": "SitemapGenerator/1.0 (compatible; OpenClaw skill)",
        "Accept": "text/html,application/xhtml+xml",
    }

    while queue and len(visited) <= max_pages:
        url, depth = queue.popleft()

        if verbose:
            print(f"  [{len(visited):>4}] depth={depth} {url}", file=sys.stderr)

        try:
            resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type:
                continue
            resp.raise_for_status()
        except Exception as e:
            if verbose:
                print(f"  SKIP {url}: {e}", file=sys.stderr)
            continue

        if depth >= max_depth:
            continue

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            full_url = urljoin(url, href)
            normalized = normalize_url(full_url)

            if not normalized.startswith(("http://", "https://")):
                continue
            if not is_same_domain(normalized, base_domain):
                continue
            if should_skip(normalized):
                continue
            if normalized in visited:
                continue
            if len(visited) >= max_pages:
                break

            visited.add(normalized)
            queue.append((normalized, depth + 1))

        if delay > 0:
            time.sleep(delay)

    return visited


def generate_sitemap(urls: set, output_path: str, changefreq: str, priority: str):
    """Generate an XML sitemap from a set of URLs."""
    urlset = ET.Element("urlset")
    urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    for url in sorted(urls):
        url_elem = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url_elem, "loc")
        loc.text = url
        lastmod = ET.SubElement(url_elem, "lastmod")
        lastmod.text = now
        if changefreq:
            freq = ET.SubElement(url_elem, "changefreq")
            freq.text = changefreq
        if priority:
            prio = ET.SubElement(url_elem, "priority")
            prio.text = priority

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")

    if output_path == "-":
        ET.indent(tree, space="  ")
        tree.write(sys.stdout.buffer, encoding="UTF-8", xml_declaration=True)
        print()  # newline
    else:
        tree.write(output_path, encoding="UTF-8", xml_declaration=True)
        print(f"Sitemap written to {output_path} ({len(urls)} URLs)", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Crawl a website and generate an XML sitemap.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s https://example.com
  %(prog)s https://example.com --max-pages 500 --output sitemap.xml
  %(prog)s https://example.com --max-depth 3 --delay 0.5 --verbose
  %(prog)s https://example.com --changefreq weekly --priority 0.8
""",
    )
    parser.add_argument("url", help="Starting URL to crawl")
    parser.add_argument("--output", "-o", default="sitemap.xml", help="Output file (default: sitemap.xml, use - for stdout)")
    parser.add_argument("--max-pages", type=int, default=200, help="Maximum pages to crawl (default: 200)")
    parser.add_argument("--max-depth", type=int, default=5, help="Maximum link depth (default: 5)")
    parser.add_argument("--delay", type=float, default=0.2, help="Delay between requests in seconds (default: 0.2)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    parser.add_argument("--changefreq", choices=["always", "hourly", "daily", "weekly", "monthly", "yearly", "never"], default="weekly", help="Change frequency hint (default: weekly)")
    parser.add_argument("--priority", default="0.5", help="Priority hint 0.0-1.0 (default: 0.5)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print progress to stderr")

    args = parser.parse_args()

    # Validate URL
    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        print("ERROR: Invalid URL. Include scheme (https://example.com)", file=sys.stderr)
        sys.exit(1)

    print(f"Crawling {args.url} (max {args.max_pages} pages, depth {args.max_depth})...", file=sys.stderr)
    urls = crawl(args.url, args.max_pages, args.max_depth, args.delay, args.timeout, args.verbose)
    print(f"Found {len(urls)} pages.", file=sys.stderr)

    generate_sitemap(urls, args.output, args.changefreq, args.priority)


if __name__ == "__main__":
    main()
