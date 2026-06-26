#!/usr/bin/env python3
"""
Multi-symbol comparison: correlation, relative performance, beta, Sharpe.

Usage:
  python compare.py SYM1 SYM2 ... --timeframe TF --bars N [--mock]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.lib.config import get_config
from scripts.lib.validators import resolve_symbol, validate_timeframe, parse_bars, TIMEFRAME_LABELS
from scripts.lib.errors import handle_error, EXIT_OK
from scripts.lib.formatter import print_compare_result
from scripts.lib.mock import load_fixture

BARS_PER_YEAR = {
    "1": 525600, "5": 105120, "15": 35040, "60": 8760,
    "240": 2190, "1D": 252, "1W": 52, "1M": 12,
}


def compare(dfs: dict[str, pd.DataFrame], timeframe: str) -> tuple[str, dict]:
    """
    Compare multiple symbols. Returns (table_string, stats_dict).
    dfs: {symbol: DataFrame} with OHLCV columns and datetime index.
    """
    bpy = BARS_PER_YEAR.get(timeframe, 252)
    symbols = list(dfs.keys())

    # Align all close series on common dates
    closes = pd.DataFrame({sym: dfs[sym]["close"] for sym in symbols})
    closes = closes.dropna()

    if len(closes) < 2:
        return "Insufficient overlapping data for comparison.", {}

    returns = closes.pct_change().dropna()

    stats = {}
    stats["SYMBOLS"] = ", ".join(symbols)
    stats["TIMEFRAME"] = TIMEFRAME_LABELS.get(timeframe, timeframe)
    stats["BARS"] = len(closes)
    stats["DATE_FROM"] = closes.index[0].strftime("%Y-%m-%d")
    stats["DATE_TO"] = closes.index[-1].strftime("%Y-%m-%d")

    # Per-symbol stats
    per_sym = {}
    for sym in symbols:
        s = closes[sym]
        r = returns[sym]
        total_ret = (s.iloc[-1] / s.iloc[0] - 1) * 100
        daily_vol = float(r.std()) * 100
        ann_vol = daily_vol * np.sqrt(bpy)
        period_years = len(s) / bpy if bpy > 0 else 1
        ann_ret = ((1 + total_ret / 100) ** (1 / period_years) - 1) * 100 if period_years > 0 else 0
        sharpe = ann_ret / ann_vol if ann_vol > 0 else 0
        rolling_max = s.cummax()
        dd = ((s - rolling_max) / rolling_max * 100).min()

        per_sym[sym] = {
            "period_return": round(total_ret, 2),
            "ann_return": round(ann_ret, 2),
            "ann_volatility": round(ann_vol, 2),
            "sharpe": round(sharpe, 2),
            "max_drawdown": round(dd, 2),
        }

    # Correlation matrix
    corr = returns.corr()

    # Beta (each symbol vs first as benchmark)
    benchmark = symbols[0]
    betas = {}
    for sym in symbols[1:]:
        cov = returns[sym].cov(returns[benchmark])
        var = returns[benchmark].var()
        betas[f"BETA_{sym}_vs_{benchmark}"] = round(cov / var, 3) if var > 0 else 0.0

    # Build table string
    header = f"{'Metric':<20}" + "".join(f"{sym:>16}" for sym in symbols)
    rows = [header, "-" * (20 + 16 * len(symbols))]

    metrics = ["period_return", "ann_return", "ann_volatility", "sharpe", "max_drawdown"]
    labels = ["Period Return %", "Ann. Return %", "Ann. Volatility %", "Sharpe Ratio", "Max Drawdown %"]
    for label, metric in zip(labels, metrics):
        vals = "".join(f"{per_sym[sym][metric]:>16.2f}" for sym in symbols)
        rows.append(f"{label:<20}{vals}")

    rows.append("")
    rows.append("Correlation Matrix:")
    rows.append(f"{'':>16}" + "".join(f"{sym:>16}" for sym in symbols))
    for sym1 in symbols:
        vals = "".join(f"{corr.loc[sym1, sym2]:>16.3f}" for sym2 in symbols)
        rows.append(f"{sym1:>16}{vals}")

    if betas:
        rows.append("")
        for key, val in betas.items():
            rows.append(f"{key}: {val}")

    table = "\n".join(rows)

    # Combine all stats
    all_stats = {**stats}
    for sym, s in per_sym.items():
        for k, v in s.items():
            all_stats[f"{sym}_{k}"] = v
    for k, v in betas.items():
        all_stats[k] = v

    return table, all_stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare multiple symbols")
    parser.add_argument("symbols", nargs="+", help="2+ symbols to compare")
    parser.add_argument("--timeframe", "-t", default="1D")
    parser.add_argument("--bars", "-n", default="500")
    parser.add_argument("--token", help="Auth token")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()

    if len(args.symbols) < 2:
        print("ERROR_TYPE: ValueError", file=sys.stderr)
        print("ERROR_MESSAGE: Need at least 2 symbols to compare", file=sys.stderr)
        return 1

    try:
        symbols = [resolve_symbol(s) for s in args.symbols]
        timeframe = validate_timeframe(args.timeframe)
        bars = parse_bars(args.bars)
    except ValueError as exc:
        return handle_error(exc)

    cfg = get_config(cli_token=args.token)

    # Fetch data for all symbols
    dfs: dict[str, pd.DataFrame] = {}
    if args.mock or cfg.mock_mode:
        for sym in symbols:
            result = load_fixture(sym, timeframe, bars)
            if result and result.bars:
                dfs[sym] = result.df
    else:
        try:
            import tvfetch
            results = tvfetch.fetch_multi(symbols, timeframe, bars, auth_token=cfg.auth_token)
            for sym, result in results.items():
                if result.bars:
                    dfs[sym] = result.df
        except Exception as exc:
            return handle_error(exc)

    if len(dfs) < 2:
        print("ERROR_TYPE: InsufficientData", file=sys.stderr)
        print(f"ERROR_MESSAGE: Need data for at least 2 symbols, got {len(dfs)}", file=sys.stderr)
        return 1

    table, stats = compare(dfs, timeframe)
    print_compare_result(table, stats)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
