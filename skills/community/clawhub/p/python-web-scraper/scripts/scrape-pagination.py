#!/usr/bin/env python3
"""
scrape-pagination.py — Scrape paginated websites
Usage: python3 scrape-pagination.py <url> [--page-param page] [--max-pages 10]

Handles:
- URL-based pagination (?page=2, /page/2/)
- "Next" link detection
- Concurrent (but rate-limited) page fetches
"""

import argparse
import json
import sys
import time
from urllib.parse import urljoin, urlparse, parse_qs, urlencode

import requests
from bs4 import BeautifulSoup


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def fetch(url, timeout=15):
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
        resp.raise_for_status()
        return resp
    except requests.RequestException as e:
        print(f"❌ {url}: {e}", file=sys.stderr)
        return None


def find_next_link(soup, base_url):
    """Find 'next' link from common patterns."""
    for sel in [
        "a.next", "a[rel=next]", "a:has(> .next)", "a.pagination__next",
        "a:contains('Next')", "a:contains('next')",
        "a:contains('›')", "a:contains('»')",
    ]:
        el = soup.select_one(sel)
        if el and el.get("href"):
            return urljoin(base_url, el["href"])
    return None


def scrape_page(soup, selector, attr=None, base_url=None):
    items = []
    for el in soup.select(selector):
        if attr:
            val = el.get(attr)
            if val and base_url:
                val = urljoin(base_url, val)
            items.append(val)
        else:
            items.append(el.get_text(strip=True))
    return items


def main():
    parser = argparse.ArgumentParser(description="Scrape paginated websites.")
    parser.add_argument("url", help="Starting URL")
    parser.add_argument("--selector", "-s", default="h2 a", help="CSS selector for items")
    parser.add_argument("--attr", help="Attribute to extract instead of text")
    parser.add_argument("--max-pages", "-n", type=int, default=10, help="Maximum pages to scrape")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between pages (seconds)")
    parser.add_argument("--page-param", help="Query param for page number (e.g., 'page')")
    parser.add_argument("--output", "-o", default="-", help="Output file ('-' for stdout)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    parser.add_argument("--start-page", type=int, default=1, help="Starting page number")
    args = parser.parse_args()

    all_items = []
    page_num = args.start_page
    current_url = args.url

    if args.page_param:
        # URL-based pagination
        for i in range(args.max_pages):
            parsed = list(urlparse(args.url))
            qs = parse_qs(parsed[4])
            qs[args.page_param] = [str(page_num)]
            parsed[4] = urlencode(qs, doseq=True)
            url = parsed[0] + "://" + parsed[1] + parsed[2] + "?" + parsed[4]
            # Simple case: just append param
            url = args.url + ("" if "?" in args.url else "?")
            url += f"{args.page_param}={page_num}"

            print(f"📄 Page {page_num}: {url}", file=sys.stderr)
            resp = fetch(url)
            if not resp:
                break
            soup = BeautifulSoup(resp.text, "html.parser")
            items = scrape_page(soup, args.selector, args.attr, base_url=url)
            if not items:
                print("⏹️  No more items found.", file=sys.stderr)
                break
            all_items.extend(items)
            print(f"  → {len(items)} items (total: {len(all_items)})", file=sys.stderr)
            page_num += 1
            time.sleep(args.delay)
    else:
        # Next-link based pagination
        for i in range(args.max_pages):
            print(f"📄 Page {i+1}: {current_url}", file=sys.stderr)
            resp = fetch(current_url)
            if not resp:
                break
            soup = BeautifulSoup(resp.text, "html.parser")
            items = scrape_page(soup, args.selector, args.attr, base_url=current_url)
            all_items.extend(items)
            print(f"  → {len(items)} items (total: {len(all_items)})", file=sys.stderr)

            next_url = find_next_link(soup, current_url)
            if not next_url or next_url == current_url:
                print("⏹️  No next link found.", file=sys.stderr)
                break
            current_url = next_url
            time.sleep(args.delay)

    # Output
    output = json.dumps(all_items, indent=2 if args.pretty else None, ensure_ascii=False)
    if args.output == "-":
        print(output)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Wrote {len(all_items)} items to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
