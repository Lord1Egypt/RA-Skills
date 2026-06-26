#!/usr/bin/env python3
"""
Cache management — skill script wrapper.

Usage:
  python cache_mgr.py stats                    Show cache contents
  python cache_mgr.py clear [--symbol SYM] [--all]  Clear cache
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.lib.config import get_config


def main() -> int:
    parser = argparse.ArgumentParser(description="Cache management")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("stats", help="Show cache contents")

    clear_p = sub.add_parser("clear", help="Clear cache")
    clear_p.add_argument("--symbol", help="Clear only this symbol")
    clear_p.add_argument("--timeframe", help="Clear only this timeframe")
    clear_p.add_argument("--all", action="store_true", help="Clear everything")

    args = parser.parse_args()

    cfg = get_config()

    from tvfetch.cache import Cache
    cache = Cache(path=cfg.cache_path)

    if args.command == "stats":
        df = cache.stats()
        print("=== CACHE STATS ===")
        print(f"PATH: {cfg.cache_path}")
        print(f"SIZE: {cache.size_mb():.2f} MB")
        print(f"ENTRIES: {len(df)}")
        if df.empty:
            print("(empty)")
        else:
            print(f"\n{'Symbol':<25} {'TF':<6} {'Bars':>8} {'Oldest':<12} {'Newest':<12} {'Fetched':<20}")
            print("-" * 90)
            for _, row in df.iterrows():
                print(
                    f"{row['symbol']:<25} {row['timeframe']:<6} {row['bars']:>8} "
                    f"{row['oldest']:<12} {row['newest']:<12} {row['fetched_at']:<20}"
                )
        print("=== END ===")

    elif args.command == "clear":
        if not args.all and not args.symbol:
            print("Specify --symbol SYMBOL or --all to clear.", file=sys.stderr)
            return 1
        deleted = cache.clear(symbol=args.symbol, timeframe=args.timeframe)
        print(f"Deleted {deleted:,} cached bar rows.")

    else:
        parser.print_help()
        return 1

    cache.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
