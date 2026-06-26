#!/usr/bin/env python3
"""Resolve Yahoo Finance symbols and show related headlines."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SEARCH_URL = "https://query1.finance.yahoo.com/v1/finance/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Accept-Encoding": "identity",
}


def fetch_json(query: str, quotes: int, news: int) -> dict[str, Any]:
    params = urlencode(
        {
            "q": query,
            "quotesCount": quotes,
            "newsCount": news,
            "enableFuzzyQuery": "false",
            "enableCb": "false",
        }
    )
    req = Request(f"{SEARCH_URL}?{params}", headers=HEADERS)
    with urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="company name, ticker, ETF, or theme")
    parser.add_argument("--quotes", type=int, default=5, help="max quote matches")
    parser.add_argument("--news", type=int, default=3, help="max news items")
    args = parser.parse_args()

    try:
        payload = fetch_json(args.query, args.quotes, args.news)
    except Exception as exc:
        print(f"Yahoo search failed: {exc}", file=sys.stderr)
        return 1

    quotes = payload.get("quotes", [])
    news = payload.get("news", [])

    print(f"Yahoo Search: {args.query}")
    print()

    if quotes:
        print("Symbol matches")
        for item in quotes[: args.quotes]:
            name = item.get("shortname") or item.get("longname") or "(no name)"
            symbol = item.get("symbol", "?")
            kind = item.get("typeDisp") or item.get("quoteType") or "unknown"
            exch = item.get("exchDisp") or item.get("exchange") or "unknown"
            sector = item.get("sectorDisp") or item.get("sector") or ""
            sector_text = f" | {sector}" if sector else ""
            print(f"- {symbol}: {name} [{kind} | {exch}{sector_text}]")
    else:
        print("No symbol matches returned.")

    if news:
        print()
        print("Related headlines")
        for item in news[: args.news]:
            title = item.get("title") or "(untitled)"
            publisher = item.get("publisher") or item.get("provider") or "unknown"
            link = item.get("link") or ""
            print(f"- {title} [{publisher}]")
            if link:
                print(f"  {link}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
