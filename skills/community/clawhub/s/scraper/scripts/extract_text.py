#!/usr/bin/env python3
import argparse
import re
import urllib.request
from html import unescape

def strip_html(html):
    html = re.sub(r'(?is)<script.*?>.*?</script>', ' ', html)
    html = re.sub(r'(?is)<style.*?>.*?</style>', ' ', html)
    html = re.sub(r'(?i)<br\\s*/?>', '\\n', html)
    html = re.sub(r'(?i)</p>', '\\n', html)
    text = re.sub(r'(?s)<.*?>', ' ', html)
    text = unescape(text)
    text = re.sub(r'\r', '', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def main():
    parser = argparse.ArgumentParser(description="Extract readable text from a public page")
    parser.add_argument("--url", required=True, help="Public URL to fetch and clean")
    args = parser.parse_args()

    req = urllib.request.Request(
        args.url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; ScraperSkill/1.0)"
        }
    )

    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    text = strip_html(html)
    print(text[:4000])

if __name__ == "__main__":
    main()
