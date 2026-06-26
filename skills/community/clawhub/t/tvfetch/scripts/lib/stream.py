#!/usr/bin/env python3
"""
Live price streaming — skill script wrapper.

Usage:
  python stream.py SYM1 SYM2 ... [OPTIONS]

Options:
  --timeframe TF       Bar timeframe (default: 1)
  --duration N         Seconds to stream (default: 10)
  --alert-above PRICE  Alert when price exceeds threshold
  --alert-below PRICE  Alert when price falls below threshold
  --alert-change-pct P Alert on N% move
  --token TOKEN        Auth token override
  --mock               Use fixture data
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.lib.config import get_config
from scripts.lib.validators import resolve_symbol, validate_timeframe
from scripts.lib.errors import handle_error, EXIT_OK
from scripts.lib.formatter import print_stream_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Stream live prices")
    parser.add_argument("symbols", nargs="+", help="Symbols")
    parser.add_argument("--timeframe", "-t", default="1")
    parser.add_argument("--duration", "-d", type=float, default=10.0, help="Seconds (default: 10)")
    parser.add_argument("--alert-above", type=float, help="Alert when price > threshold")
    parser.add_argument("--alert-below", type=float, help="Alert when price < threshold")
    parser.add_argument("--alert-change-pct", type=float, help="Alert on N% move")
    parser.add_argument("--token", help="Auth token override")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()

    try:
        symbols = [resolve_symbol(s) for s in args.symbols]
        timeframe = validate_timeframe(args.timeframe)
    except ValueError as exc:
        return handle_error(exc)

    cfg = get_config(cli_token=args.token)

    if args.mock or cfg.mock_mode:
        # Mock mode: print synthetic updates
        print("=== STREAM (MOCK) ===")
        for i in range(min(5, int(args.duration))):
            for sym in symbols:
                print(f"  {sym}: 50000.{i:04d} (mock)")
            time.sleep(0.1)
        print_stream_summary(symbols, args.duration, len(symbols) * 5, {})
        return EXIT_OK

    # Real streaming
    updates: list = []
    first_prices: dict[str, float] = {}
    session_highs: dict[str, float] = {}
    session_lows: dict[str, float] = {}
    last_prices: dict[str, float] = {}
    count = [0]

    def on_bar(bar) -> None:
        count[0] += 1
        sym = bar.symbol
        updates.append(bar)

        if sym not in first_prices:
            first_prices[sym] = bar.close

        session_highs[sym] = max(session_highs.get(sym, bar.high), bar.high)
        session_lows[sym] = min(session_lows.get(sym, bar.low), bar.low)
        last_prices[sym] = bar.close

        # Direction indicator
        prev = last_prices.get(sym, bar.close)
        direction = "+" if bar.close >= prev else "-"

        ts = bar.timestamp.strftime("%H:%M:%S")
        print(
            f"  {sym:<25} {bar.close:>12.4f}  {bar.change_pct:>+8.2f}%"
            f"  vol={bar.volume:>12.2f}  {ts} [{direction}]"
        )

        # Alert checks
        if args.alert_above and bar.close > args.alert_above:
            print(f"ALERT_ABOVE: {sym} crossed {args.alert_above:.4f} at {ts} (current: {bar.close:.4f})")
        if args.alert_below and bar.close < args.alert_below:
            print(f"ALERT_BELOW: {sym} fell below {args.alert_below:.4f} at {ts} (current: {bar.close:.4f})")
        if args.alert_change_pct and abs(bar.change_pct) > args.alert_change_pct:
            print(f"ALERT_CHANGE: {sym} moved {bar.change_pct:+.2f}% (threshold: {args.alert_change_pct}%)")

    try:
        import tvfetch
        print(f"Streaming {', '.join(symbols)} for {args.duration:.0f}s...")
        print(f"{'Symbol':<25} {'Price':>12}  {'Change':>9}  {'Volume':>14}  Time")
        print("-" * 75)

        tvfetch.stream(
            symbols=symbols,
            on_update=on_bar,
            timeframe=timeframe,
            auth_token=cfg.auth_token,
            duration=args.duration,
        )
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        return handle_error(exc)

    # Build session stats
    session_stats = {}
    for sym in symbols:
        stats = {}
        if sym in last_prices:
            stats["LAST_PRICE"] = last_prices[sym]
        if sym in session_highs:
            stats["SESSION_HIGH"] = session_highs[sym]
        if sym in session_lows:
            stats["SESSION_LOW"] = session_lows[sym]
        if sym in first_prices and sym in last_prices:
            change = (last_prices[sym] - first_prices[sym]) / first_prices[sym] * 100
            stats["SESSION_CHANGE_PCT"] = change

        # VWAP approximation
        sym_updates = [u for u in updates if u.symbol == sym and u.volume > 0]
        if sym_updates:
            total_pv = sum(u.close * u.volume for u in sym_updates)
            total_v = sum(u.volume for u in sym_updates)
            if total_v > 0:
                stats["APPROX_VWAP"] = total_pv / total_v

        stats["UPDATE_COUNT"] = sum(1 for u in updates if u.symbol == sym)
        session_stats[sym] = stats

    print_stream_summary(symbols, args.duration, count[0], session_stats)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
