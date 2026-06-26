#!/usr/bin/env python3
"""
Symbol search — skill script wrapper.

Usage:
  python search.py "QUERY" [OPTIONS]

Options:
  --type TYPE          stock|crypto|forex|futures|index|bond|cfd
  --exchange EXCHANGE  Filter by exchange (BINANCE, NASDAQ, etc.)
  --limit N            Max results (default: 20)
  --mock               Use fixture data
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.lib.errors import handle_error, EXIT_OK
from scripts.lib.formatter import print_search_results


def main() -> int:
    parser = argparse.ArgumentParser(description="Search TradingView for symbols")
    parser.add_argument("query", help="Search term")
    parser.add_argument("--type", dest="symbol_type", default="", help="Asset type filter")
    parser.add_argument("--exchange", "-e", default="", help="Exchange filter")
    parser.add_argument("--limit", "-n", type=int, default=20, help="Max results")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()

    if args.mock:
        fixture_path = _SKILL_DIR / "fixtures"
        import json
        # Try to find a matching fixture
        safe = args.query.lower().replace(" ", "_")
        for name in [f"search_{safe}.json", f"search_{safe}_{args.symbol_type}.json", "search_default.json"]:
            p = fixture_path / name
            if p.is_file():
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print_search_results(data.get("results", []))
                return EXIT_OK
        print(f"WARNING: No search fixture for '{args.query}'", file=sys.stderr)
        print_search_results([])
        return EXIT_OK

    try:
        import tvfetch
        results = tvfetch.search(
            query=args.query,
            exchange=args.exchange,
            symbol_type=args.symbol_type,
            limit=args.limit,
        )
    except Exception as exc:
        return handle_error(exc)

    result_dicts = [
        {
            "symbol": r.symbol,
            "description": r.description,
            "exchange": r.exchange,
            "type": r.type,
            "currency": r.currency,
        }
        for r in results
    ]
    print_search_results(result_dicts)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
