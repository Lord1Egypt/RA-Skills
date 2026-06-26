#!/usr/bin/env python3
"""Create a compact multi-ticker Yahoo Finance market brief."""

from __future__ import annotations

import argparse
import gzip
import html
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.request import Request, urlopen


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Encoding": "identity",
}


@dataclass
class Snapshot:
    symbol: str
    title: str
    price: str
    change: str
    change_pct_value: float
    change_pct_text: str
    market_time: str


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


def parse_percent(raw: str) -> float:
    cleaned = raw.replace("(", "").replace(")", "").replace("%", "").replace("+", "").replace(",", "").strip()
    return float(cleaned or 0)


def parse_title(page: str, fallback_symbol: str) -> str:
    title = extract(r"<title>(.*?)</title>", page)
    title = title.replace(" - Yahoo Finance", "").replace("Stock Price, News, Quote & History", "").strip(" |")
    return title or fallback_symbol.upper()


def load_symbols(args_symbols: list[str], file_path: str | None) -> list[str]:
    symbols = [item.upper() for item in args_symbols]
    if file_path:
        path = Path(file_path).expanduser()
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip().upper()
            if line and not line.startswith("#"):
                symbols.append(line)
    seen = set()
    unique = []
    for symbol in symbols:
        if symbol not in seen:
            seen.add(symbol)
            unique.append(symbol)
    return unique


def fetch_snapshot(symbol: str) -> Snapshot:
    page = fetch_html(symbol)
    change_pct_text = extract(r'data-testid="qsp-price-change-percent">\s*([^<]+)', page) or "(0.00%)"
    return Snapshot(
        symbol=symbol,
        title=parse_title(page, symbol),
        price=extract(r'data-testid="qsp-price">\s*([^<]+)', page) or "?",
        change=extract(r'data-testid="qsp-price-change">\s*([^<]+)', page) or "?",
        change_pct_value=parse_percent(change_pct_text),
        change_pct_text=change_pct_text,
        market_time=extract(r'<div slot="marketTimeNotice"[^>]*>\s*<span[^>]*>([^<]+)', page),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("symbols", nargs="*", help="tickers to include")
    parser.add_argument("--file", help="optional file with one symbol per line")
    args = parser.parse_args()

    symbols = load_symbols(args.symbols, args.file)
    if not symbols:
        print("Provide at least one symbol or --file.", file=sys.stderr)
        return 1

    snapshots: list[Snapshot] = []
    failures: list[str] = []
    for symbol in symbols:
        try:
            snapshots.append(fetch_snapshot(symbol))
        except Exception as exc:
            failures.append(f"{symbol}: {exc}")

    if not snapshots:
        print("No quotes could be fetched.", file=sys.stderr)
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    movers = sorted(snapshots, key=lambda item: item.change_pct_value, reverse=True)
    avg_move = statistics.mean(item.change_pct_value for item in snapshots)

    print("Yahoo Market Brief")
    if snapshots[0].market_time:
        print(f"Market state: {snapshots[0].market_time}")
    print(f"Universe: {', '.join(item.symbol for item in snapshots)}")
    print(f"Average move: {avg_move:+.2f}%")
    print()

    print("Ranked movers")
    for item in movers:
        print(f"- {item.symbol}: {item.price} | {item.change} {item.change_pct_text} | {item.title}")

    print()
    print("Leaders")
    for item in movers[: min(3, len(movers))]:
        print(f"- {item.symbol}: {item.change_pct_text}")

    print()
    print("Laggards")
    for item in list(reversed(movers[-min(3, len(movers)) :])):
        print(f"- {item.symbol}: {item.change_pct_text}")

    if failures:
        print()
        print("Failures")
        for failure in failures:
            print(f"- {failure}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
