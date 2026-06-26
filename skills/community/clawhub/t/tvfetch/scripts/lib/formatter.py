"""
Centralized output formatting for tvfetch skill scripts.

All output uses tagged sections that SKILL.md's STEP 4 can parse:
  === SECTION_NAME === ... === END ===

Claude reads these tags and formats a clean user response from them.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from typing import Any

import pandas as pd


def print_fetch_result(
    symbol: str,
    timeframe: str,
    df: pd.DataFrame,
    source: str,
    auth_mode: str,
    warnings: list[str] | None = None,
    max_rows: int = 20,
) -> None:
    """Print tagged fetch result block."""
    print("=== FETCH RESULT ===")
    print(f"SYMBOL: {symbol}")
    print(f"TIMEFRAME: {timeframe}")
    print(f"BARS: {len(df)}")
    print(f"SOURCE: {source}")
    print(f"AUTH_MODE: {auth_mode}")

    if not df.empty:
        print(f"DATE_FROM: {df.index[0].strftime('%Y-%m-%d')}")
        print(f"DATE_TO: {df.index[-1].strftime('%Y-%m-%d')}")

        latest = df.iloc[-1]
        print(f"LATEST_OPEN: {latest['open']:.4f}")
        print(f"LATEST_HIGH: {latest['high']:.4f}")
        print(f"LATEST_LOW: {latest['low']:.4f}")
        print(f"LATEST_CLOSE: {latest['close']:.4f}")
        print(f"LATEST_VOLUME: {latest['volume']:.2f}")

        if len(df) >= 2:
            prev_close = df.iloc[-2]["close"]
            change_pct = (latest["close"] - prev_close) / prev_close * 100
            print(f"PREV_CLOSE: {prev_close:.4f}")
            print(f"CHANGE_PCT: {change_pct:+.2f}%")

    if warnings:
        for w in warnings:
            print(f"WARNING: {w}")

    if not df.empty:
        print("=== DATA TABLE ===")
        display = df.tail(max_rows)
        # Print header
        print(f"{'Datetime (UTC)':<22} {'Open':>12} {'High':>12} {'Low':>12} {'Close':>12} {'Volume':>14}")
        print("-" * 88)
        for idx, row in display.iterrows():
            dt_str = idx.strftime("%Y-%m-%d %H:%M")
            print(
                f"{dt_str:<22} {row['open']:>12.4f} {row['high']:>12.4f} "
                f"{row['low']:>12.4f} {row['close']:>12.4f} {row['volume']:>14.2f}"
            )
        if len(df) > max_rows:
            print(f"... ({len(df) - max_rows} earlier bars not shown)")

    print("=== END ===")


def print_analysis_result(stats: dict[str, Any]) -> None:
    """Print tagged analysis result block."""
    print("=== ANALYSIS RESULT ===")
    for key, val in stats.items():
        if isinstance(val, float):
            print(f"{key}: {val:.4f}")
        elif isinstance(val, datetime):
            print(f"{key}: {val.strftime('%Y-%m-%d')}")
        elif isinstance(val, bool):
            print(f"{key}: {'true' if val else 'false'}")
        else:
            print(f"{key}: {val}")
    print("=== END ===")


def print_compare_result(table: str, stats: dict[str, Any]) -> None:
    """Print tagged comparison result block."""
    print("=== COMPARISON ===")
    for key, val in stats.items():
        if isinstance(val, float):
            print(f"{key}: {val:.4f}")
        else:
            print(f"{key}: {val}")
    print("=== TABLE ===")
    print(table)
    print("=== END ===")


def print_search_results(results: list[dict]) -> None:
    """Print tagged search results block."""
    print("=== SEARCH RESULTS ===")
    print(f"COUNT: {len(results)}")
    print(f"{'Symbol':<30} {'Description':<40} {'Exchange':<12} {'Type':<10} {'Currency':<8}")
    print("-" * 104)
    for r in results:
        print(
            f"{r['symbol']:<30} {r['description']:<40} {r['exchange']:<12} "
            f"{r['type']:<10} {r['currency']:<8}"
        )
    print("=== END ===")


def print_indicator_result(
    symbol: str,
    timeframe: str,
    latest_close: float,
    indicators: dict[str, Any],
    signals: list[str],
) -> None:
    """Print tagged indicator result block."""
    print("=== INDICATORS ===")
    print(f"SYMBOL: {symbol}")
    print(f"TIMEFRAME: {timeframe}")
    print(f"LATEST_CLOSE: {latest_close:.4f}")

    for name, val in indicators.items():
        if isinstance(val, float):
            print(f"{name}: {val:.4f}")
        else:
            print(f"{name}: {val}")

    if signals:
        print("=== SIGNALS ===")
        for sig in signals:
            print(sig)

    print("=== END ===")


def print_stream_summary(
    symbols: list[str],
    duration: float,
    update_count: int,
    session_stats: dict[str, Any],
) -> None:
    """Print tagged stream summary block."""
    print("=== STREAM SUMMARY ===")
    print(f"SYMBOLS: {', '.join(symbols)}")
    print(f"DURATION: {duration:.1f}s")
    print(f"UPDATES: {update_count}")

    for sym, stats in session_stats.items():
        print(f"--- {sym} ---")
        for key, val in stats.items():
            if isinstance(val, float):
                print(f"  {key}: {val:.4f}")
            else:
                print(f"  {key}: {val}")

    print("=== END ===")


def print_json_output(data: dict) -> None:
    """Print machine-readable JSON for agent mode."""
    print(json.dumps(data, indent=2, default=str))


def print_warning(msg: str) -> None:
    """Print a warning that Claude will pass through to user."""
    print(f"WARNING: {msg}")


def print_progress(current: int, total: int) -> None:
    """Print progress line for large fetches."""
    print(f"PROGRESS: {current}/{total} bars")
