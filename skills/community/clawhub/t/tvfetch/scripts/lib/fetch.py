#!/usr/bin/env python3
"""
Fetch historical OHLCV data — skill script wrapper.

Usage:
  python fetch.py SYMBOL TIMEFRAME BARS [OPTIONS]

Options:
  --output PATH        Save to file (format auto-detected from extension)
  --format FMT         csv|json|parquet|freqtrade
  --no-cache           Bypass SQLite cache
  --fallback-only      Skip TradingView, use Yahoo/CCXT
  --mock               Use fixture data
  --json-output        Machine-readable JSON to stdout
  --token TOKEN        Auth token override
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Add skill root to path so tvfetch is importable
_SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.lib.config import get_config
from scripts.lib.validators import resolve_symbol, validate_timeframe, parse_bars, check_bar_limit_warning
from scripts.lib.errors import handle_error, EXIT_OK
from scripts.lib.formatter import print_fetch_result, print_json_output, print_warning
from scripts.lib.mock import load_fixture


def _detect_gaps(df, timeframe: str) -> list[str]:
    """Detect unexpected gaps in the data (ignoring weekends for stock timeframes)."""
    import pandas as pd

    if len(df) < 2:
        return []

    tf_seconds = {
        "1": 60, "3": 180, "5": 300, "10": 600, "15": 900,
        "30": 1800, "45": 2700, "60": 3600, "120": 7200,
        "180": 10800, "240": 14400, "1D": 86400, "1W": 604800, "1M": 2592000,
    }
    expected = tf_seconds.get(timeframe, 86400)
    # Allow 3x tolerance (accounts for weekends, holidays)
    threshold = expected * 3

    gaps = []
    for i in range(1, len(df)):
        delta = (df.index[i] - df.index[i - 1]).total_seconds()
        if delta > threshold:
            gap_bars = int(delta / expected) - 1
            if gap_bars > 5:  # Only report significant gaps
                gaps.append(
                    f"Gap: {df.index[i-1].strftime('%Y-%m-%d %H:%M')} to "
                    f"{df.index[i].strftime('%Y-%m-%d %H:%M')} (~{gap_bars} bars missing)"
                )
    return gaps


def _validate_ohlcv(df) -> list[str]:
    """Run data quality checks. Returns list of warning strings."""
    warnings = []

    # High < Low check
    invalid = df[df["high"] < df["low"]]
    if not invalid.empty:
        warnings.append(f"{len(invalid)} bars have high < low (possible data corruption)")

    # Excessive zero-volume bars (>10%)
    zero_vol = df[df["volume"] == 0]
    if len(zero_vol) > len(df) * 0.1:
        warnings.append(f"{len(zero_vol)} bars have zero volume ({len(zero_vol)/len(df)*100:.0f}%)")

    # Price spike detection (close > 3x previous close)
    if len(df) >= 2:
        ratios = df["close"] / df["close"].shift(1)
        spikes = ratios[(ratios > 3) | (ratios < 0.33)]
        if not spikes.empty:
            warnings.append(f"{len(spikes)} possible price spike(s) detected")

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch historical OHLCV data")
    parser.add_argument("symbol", help="Symbol (EXCHANGE:TICKER or alias)")
    parser.add_argument("timeframe", nargs="?", default="1D", help="Timeframe (default: 1D)")
    parser.add_argument("bars", nargs="?", default="500", help="Bar count (default: 500)")
    parser.add_argument("--output", "-o", help="Save to file")
    parser.add_argument("--format", dest="fmt", help="Export format: csv|json|parquet|freqtrade")
    parser.add_argument("--no-cache", action="store_true", help="Bypass cache")
    parser.add_argument("--fallback-only", action="store_true", help="Skip TV, use Yahoo/CCXT")
    parser.add_argument("--mock", action="store_true", help="Use fixture data")
    parser.add_argument("--json-output", action="store_true", help="Machine-readable JSON")
    parser.add_argument("--token", help="Auth token override")
    parser.add_argument("--adjustment", default="splits", help="splits|dividends|none")
    parser.add_argument("--extended", action="store_true", help="Extended session (pre/post market)")
    args = parser.parse_args()

    try:
        symbol = resolve_symbol(args.symbol)
        timeframe = validate_timeframe(args.timeframe)
        bars = parse_bars(args.bars)
    except ValueError as exc:
        return handle_error(exc, args.symbol, args.timeframe)

    cfg = get_config(cli_token=args.token)

    if args.mock or cfg.mock_mode:
        cfg = cfg  # keep config but use mock
        result = load_fixture(symbol, timeframe, bars)
        if result is None:
            print(f"WARNING: No fixture found for {symbol}/{timeframe}/{bars}. Using empty result.", file=sys.stderr)
            from tvfetch.models import FetchResult
            result = FetchResult(symbol=symbol, timeframe=timeframe, bars=[], source="mock", auth_mode="anonymous")
    else:
        # Check bar limit warning
        warning = check_bar_limit_warning(timeframe, bars, cfg.is_anonymous)
        if warning:
            print_warning(warning)

        try:
            if args.fallback_only:
                from tvfetch.fallback import fetch_with_fallback
                result = fetch_with_fallback(symbol, timeframe, bars)
            else:
                from tvfetch.historical import fetch as _tv_fetch
                result = _tv_fetch(
                    symbol=symbol,
                    timeframe=timeframe,
                    bars=bars,
                    auth_token=cfg.auth_token,
                    adjustment=args.adjustment,
                    extended_session=args.extended,
                    use_cache=not args.no_cache,
                )
        except Exception as exc:
            return handle_error(exc, symbol, timeframe)

    df = result.df

    # Data quality checks
    warnings = []
    if not df.empty:
        warnings.extend(_validate_ohlcv(df))
        gap_warnings = _detect_gaps(df, timeframe)
        if gap_warnings:
            warnings.append(f"{len(gap_warnings)} gap(s) detected (likely market holidays/weekends)")

    # Output
    if args.output:
        _save_to_file(result, args.output, args.fmt)
        print(f"Saved {len(result):,} bars to {args.output}")
        return EXIT_OK

    if args.json_output:
        print_json_output({
            "symbol": result.symbol,
            "timeframe": result.timeframe,
            "bars": len(result),
            "source": result.source,
            "auth_mode": result.auth_mode,
            "date_from": df.index[0].isoformat() if not df.empty else None,
            "date_to": df.index[-1].isoformat() if not df.empty else None,
            "latest_close": float(df.iloc[-1]["close"]) if not df.empty else None,
        })
        return EXIT_OK

    print_fetch_result(
        symbol=result.symbol,
        timeframe=result.timeframe,
        df=df,
        source=result.source,
        auth_mode=result.auth_mode,
        warnings=warnings,
    )
    return EXIT_OK


def _save_to_file(result, output: str, fmt: str | None) -> None:
    """Save FetchResult to file. Format auto-detected from extension if not specified."""
    from tvfetch import exporters

    path = Path(output)
    fmt = fmt or path.suffix.lstrip(".")

    if fmt == "freqtrade":
        candles = exporters.to_freqtrade(result)
        with open(output, "w", encoding="utf-8") as f:
            json.dump(candles, f, indent=2)
    elif fmt == "parquet":
        exporters.to_parquet(result, output)
    elif fmt == "json":
        exporters.to_json(result, output)
    else:
        exporters.to_csv(result, output)


if __name__ == "__main__":
    sys.exit(main())
