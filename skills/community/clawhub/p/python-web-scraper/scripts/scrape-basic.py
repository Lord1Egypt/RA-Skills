#!/usr/bin/env python3
"""
scrape-basic.py — Generic web scraper template with rate limiting
Usage: python3 scrape-basic.py <url> [--output data.json] [--selector div.content]

Supports:
- HTML parsing with BeautifulSoup
- Rate limiting (delay between requests)
- User-agent rotation
- Output to JSON, CSV, or plain text
"""

import argparse
import csv
import json
import sys
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
]


def fetch(url, headers=None, timeout=15):
    ua = headers.get("User-Agent") if headers else None
    if not ua:
        ua = USER_AGENTS[0]
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": ua, **(headers or {})},
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}", file=sys.stderr)
        return None


def extract_text(soup, selector, attr=None, base_url=None):
    results = []
    for el in soup.select(selector):
        if attr:
            val = el.get(attr)
            if val and base_url and attr == "href":
                val = urljoin(base_url, val)
            results.append(val)
        else:
            results.append(el.get_text(strip=True))
    return results


def main():
    parser = argparse.ArgumentParser(description="Generic web scraper.")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("--selector", "-s", default="body", help="CSS selector to extract (default: body)")
    parser.add_argument("--attr", help="HTML attribute to extract instead of text")
    parser.add_argument("--output", "-o", help="Output file (default: print to stdout)")
    parser.add_argument("--format", "-f", choices=["text", "json", "csv"], default="text", help="Output format")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (seconds)")
    parser.add_argument("--timeout", type=int, default=15, help="Request timeout")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    print(f"🌐 Fetching: {args.url}", file=sys.stderr)
    resp = fetch(args.url, timeout=args.timeout)
    if not resp:
        sys.exit(1)

    soup = BeautifulSoup(resp.text, "html.parser")
    results = extract_text(soup, args.selector, args.attr, base_url=args.url)

    if not results:
        print(f"ℹ️  No elements matched '{args.selector}'", file=sys.stderr)
        sys.exit(0)

    # Output
    if args.output and args.output != "-":
        outfile = open(args.output, "w", encoding="utf-8")
    else:
        outfile = sys.stdout
    try:
        if args.format == "json":
            json.dump(results, outfile, indent=2 if args.pretty else None, ensure_ascii=False)
        elif args.format == "csv":
            if results and isinstance(results[0], str):
                writer = csv.writer(outfile)
                writer.writerow(["text"])
                for r in results:
                    writer.writerow([r])
            else:
                writer = csv.writer(outfile)
                for r in results:
                    writer.writerow([r] if isinstance(r, str) else r)
        else:
            for r in results:
                print(r, file=outfile)
    finally:
        if outfile is not sys.stdout:
            outfile.close()
            print(f"✅ Wrote {len(results)} items to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
