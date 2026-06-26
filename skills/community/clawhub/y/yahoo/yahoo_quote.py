#!/usr/bin/env python3
"""Fetch a Yahoo Finance quote page and print key quote statistics."""

from __future__ import annotations

import argparse
import gzip
import html
import re
import sys
from urllib.request import Request, urlopen


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Encoding": "identity",
}


def fetch_html(symbol: str) -> str:
    req = Request(f"https://finance.yahoo.com/quote/{symbol}", headers=HEADERS)
    with urlopen(req, timeout=20) as response:
        payload = response.read()
        encoding = (response.info().get("Content-Encoding") or "").lower()
    if encoding == "gzip" or payload[:2] == b"\x1f\x8b":
        payload = gzip.decompress(payload)
    return payload.decode("utf-8", "replace")


def extract(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.S)
    if not match:
        return ""
    return " ".join(html.unescape(match.group(1)).split())


def strip_tags(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw)
    return " ".join(html.unescape(text).split())


def parse_stats(page: str) -> list[tuple[str, str]]:
    block = re.search(r'<div data-testid="quote-statistics".*?<ul[^>]*>(.*?)</ul>', page, re.S)
    if not block:
        return []
    items = re.findall(
        r'<li[^>]*>\s*<span class="label[^"]*"[^>]*title="([^"]+)"[^>]*>.*?</span>\s*<span class="value[^"]*">(.*?)</span>\s*</li>',
        block.group(1),
        re.S,
    )
    return [(label, strip_tags(value)) for label, value in items]


def parse_title(page: str, fallback_symbol: str) -> str:
    title = extract(r"<title>(.*?)</title>", page)
    title = title.replace(" - Yahoo Finance", "").replace("Stock Price, News, Quote & History", "").strip(" |")
    if title and title != "Yahoo Finance":
        return title
    return fallback_symbol.upper()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbol", help="ticker or Yahoo symbol, e.g. AAPL or BTC-USD")
    args = parser.parse_args()

    try:
        page = fetch_html(args.symbol.upper())
    except Exception as exc:
        print(f"Yahoo quote fetch failed: {exc}", file=sys.stderr)
        return 1

    title = parse_title(page, args.symbol)
    price = extract(r'data-testid="qsp-price">\s*([^<]+)', page)
    change = extract(r'data-testid="qsp-price-change">\s*([^<]+)', page)
    change_pct = extract(r'data-testid="qsp-price-change-percent">\s*([^<]+)', page)
    market_time = extract(r'<div slot="marketTimeNotice"[^>]*>\s*<span[^>]*>([^<]+)', page)
    stats = parse_stats(page)

    print(title)
    if price:
        print(f"Price: {price}")
    if change or change_pct:
        print(f"Move: {change} {change_pct}".strip())
    if market_time:
        print(f"Market state: {market_time}")

    if stats:
        print()
        print("Key statistics")
        for label, value in stats[:10]:
            print(f"- {label}: {value}")
    else:
        print()
        print("No statistics parsed from the Yahoo quote page.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
