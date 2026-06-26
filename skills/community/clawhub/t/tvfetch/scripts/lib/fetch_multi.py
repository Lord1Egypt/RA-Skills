#!/usr/bin/env python3
"""
Multi-symbol fetch — single WebSocket connection for performance.

Usage:
  python fetch_multi.py SYM1 SYM2 ... --timeframe TF --bars N [--output-dir DIR]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.lib.config import get_config
from scripts.lib.validators import resolve_symbol, validate_timeframe, parse_bars
from scripts.lib.errors import handle_error, EXIT_OK
from scripts.lib.formatter import print_fetch_result, print_warning


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch multiple symbols over single connection")
    parser.add_argument("symbols", nargs="+", help="Symbols (EXCHANGE:TICKER or aliases)")
    parser.add_argument("--timeframe", "-t", default="1D")
    parser.add_argument("--bars", "-n", default="500")
    parser.add_argument("--output-dir", help="Save each symbol to a CSV in this directory")
    parser.add_argument("--token", help="Auth token override")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()

    try:
        symbols = [resolve_symbol(s) for s in args.symbols]
        timeframe = validate_timeframe(args.timeframe)
        bars = parse_bars(args.bars)
    except ValueError as exc:
        return handle_error(exc)

    if len(symbols) > 10:
        print_warning("Maximum 10 symbols per call. Truncating to first 10.")
        symbols = symbols[:10]

    cfg = get_config(cli_token=args.token)

    if args.mock or cfg.mock_mode:
        from scripts.lib.mock import load_fixture
        results = {}
        for sym in symbols:
            result = load_fixture(sym, timeframe, bars)
            if result:
                results[sym] = result
    else:
        try:
            import tvfetch
            results = tvfetch.fetch_multi(
                symbols=symbols,
                timeframe=timeframe,
                bars=bars,
                auth_token=cfg.auth_token,
                use_cache=not args.no_cache,
            )
        except Exception as exc:
            return handle_error(exc)

    # Output
    for sym, result in results.items():
        df = result.df

        if args.output_dir:
            out_dir = Path(args.output_dir)
            out_dir.mkdir(parents=True, exist_ok=True)
            safe_name = sym.replace(":", "_")
            path = out_dir / f"{safe_name}_{timeframe}.csv"
            result.to_csv(str(path))
            print(f"Saved {sym}: {len(result):,} bars -> {path}")
        else:
            print_fetch_result(
                symbol=result.symbol,
                timeframe=result.timeframe,
                df=df,
                source=result.source,
                auth_mode=result.auth_mode,
                max_rows=5,  # fewer rows per symbol in multi mode
            )
            print()  # blank line between symbols

    # Summary
    total_bars = sum(len(r) for r in results.values())
    failed = [s for s in symbols if s not in results or len(results[s]) == 0]
    print(f"=== MULTI FETCH SUMMARY ===")
    print(f"SYMBOLS: {len(results)}/{len(symbols)} succeeded")
    print(f"TOTAL_BARS: {total_bars:,}")
    if failed:
        print(f"FAILED: {', '.join(failed)}")
    print("=== END ===")

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
