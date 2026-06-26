#!/usr/bin/env python3
"""SaffronAI ETF tracker fetcher.

- Fetches CSV from https://www.saffronai.in/api/etf-data via curl (avoids Python SSL issues).
- Converts to JSON.
- Supports filtering by symbol.

Usage:
  saffronai_etf.py fetch [--format json|csv]
  saffronai_etf.py get <SYMBOL...> [--format json|csv]
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
import sys
from typing import Iterable

URL = "https://www.saffronai.in/api/etf-data"


def fetch_csv_text() -> str:
    # Use curl for resilience and to align with OpenClaw skill expectations.
    # -sS: silent but show errors
    # --fail: non-2xx => exit non-zero
    res = subprocess.run(
        ["curl", "-sS", "--fail", URL],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return res.stdout


def parse_csv(text: str) -> list[dict]:
    # Normalize newlines and parse.
    buf = io.StringIO(text)
    reader = csv.DictReader(buf)
    rows: list[dict] = []
    for r in reader:
        # Keep raw strings; strip whitespace.
        rows.append({k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()})
    return rows


def filter_by_symbols(rows: Iterable[dict], symbols: list[str]) -> list[dict]:
    wanted = {s.upper() for s in symbols}
    out: list[dict] = []
    for r in rows:
        sym = (r.get("symbol") or "").upper()
        if sym in wanted:
            out.append(r)
    # Preserve input order of symbols if possible
    order = {s.upper(): i for i, s in enumerate(symbols)}
    out.sort(key=lambda r: order.get((r.get("symbol") or "").upper(), 10**9))
    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_fetch = sub.add_parser("fetch", help="Fetch full ETF snapshot")
    ap_fetch.add_argument("--format", choices=["json", "csv"], default="json")

    ap_get = sub.add_parser("get", help="Get one or more ETF symbols")
    ap_get.add_argument("symbols", nargs="+", help="e.g. NIFTYBEES GOLDBEES")
    ap_get.add_argument("--format", choices=["json", "csv"], default="json")

    args = ap.parse_args(argv)

    csv_text = fetch_csv_text()

    if getattr(args, "format", "json") == "csv":
        # For get: filter still applies, so we need to re-emit a CSV.
        if args.cmd == "fetch":
            sys.stdout.write(csv_text)
            return 0

        rows = parse_csv(csv_text)
        rows = filter_by_symbols(rows, args.symbols)
        if not rows:
            sys.stdout.write("")
            return 0
        # Emit CSV with original headers (DictReader preserves fieldnames)
        fieldnames = list(rows[0].keys())
        w = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
        return 0

    # JSON output
    rows = parse_csv(csv_text)
    if args.cmd == "get":
        rows = filter_by_symbols(rows, args.symbols)

    json.dump({"ok": True, "source": URL, "count": len(rows), "data": rows}, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv[1:]))
    except subprocess.CalledProcessError as e:
        msg = e.stderr.strip() if isinstance(e.stderr, str) else "curl failed"
        json.dump({"ok": False, "error": {"message": "fetch_failed", "details": msg}}, sys.stdout)
        sys.stdout.write("\n")
        raise SystemExit(1)
