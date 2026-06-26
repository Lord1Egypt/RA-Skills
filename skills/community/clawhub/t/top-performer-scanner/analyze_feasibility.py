#!/usr/bin/env python3
"""
Analyze Feasibility of Stock Selection Filters

Tests whether common momentum/breakout filters would have caught the top-performing
stocks before their major runs. Compares strict, strong, and broad filter configurations
to help calibrate scanner thresholds without excluding future multibaggers.
"""

import argparse
import warnings

import pandas as pd
import yfinance as yf

warnings.filterwarnings("ignore")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Test stock selection filters against known top performers."
    )
    parser.add_argument(
        "--tickers",
        type=str,
        default="APP,PLTR,NVDA,CVNA",
        help="Comma-separated list of tickers to analyze (default: APP,PLTR,NVDA,CVNA)",
    )
    parser.add_argument(
        "--start",
        type=str,
        default="2023-01-01",
        help="Start date for analysis (default: 2023-01-01)",
    )
    parser.add_argument(
        "--end",
        type=str,
        default="2026-01-31",
        help="End date for analysis (default: 2026-01-31)",
    )
    parser.add_argument(
        "--strict-turnover",
        type=float,
        default=200_000_000,
        help="Daily dollar volume threshold for strict/strong filters (default: 200000000)",
    )
    parser.add_argument(
        "--loose-turnover",
        type=float,
        default=50_000_000,
        help="Daily dollar volume threshold for broad filter (default: 50000000)",
    )
    parser.add_argument(
        "--strong-threshold",
        type=float,
        default=0.015,
        help="Minimum intraday return (close/open - 1) for strong filter (default: 0.015)",
    )
    parser.add_argument(
        "--high-lookback",
        type=int,
        default=60,
        help="Lookback period in trading days for rolling high (default: 60)",
    )
    parser.add_argument(
        "--high-pct",
        type=float,
        default=0.95,
        help="Percentage of 60-day high that close must exceed (default: 0.95)",
    )
    return parser.parse_args()


def analyze_ticker(ticker, df_close, df_open, df_high, df_low, df_volume, args):
    """Run all three filter configurations on a single ticker."""
    try:
        close = df_close[ticker].dropna()
        opn = df_open[ticker].dropna()
        high = df_high[ticker].dropna()
        low = df_low[ticker].dropna()
        volume = df_volume[ticker].dropna()
    except KeyError:
        print(f"  {ticker}: No data available, skipping.")
        return None

    # Align all series to a common index
    common_idx = close.index.intersection(opn.index).intersection(volume.index)
    close = close.loc[common_idx]
    opn = opn.loc[common_idx]
    high = high.loc[common_idx]
    low = low.loc[common_idx]
    volume = volume.loc[common_idx]

    if len(close) < args.high_lookback:
        print(f"  {ticker}: Insufficient data ({len(close)} days), skipping.")
        return None

    # Derived signals
    rolling_high = high.rolling(args.high_lookback).max()
    near_high = close >= (rolling_high * args.high_pct)
    up_today = close > opn
    dollar_volume = close * volume
    intraday_return = (close / opn) - 1

    # Strict filter: near 60d high + up today + high turnover
    strict_mask = near_high & up_today & (dollar_volume >= args.strict_turnover)

    # Strong filter: near 60d high + strong intraday return + high turnover
    strong_mask = (
        near_high
        & (intraday_return >= args.strong_threshold)
        & (dollar_volume >= args.strict_turnover)
    )

    # Broad filter: near 60d high + up today + loose turnover
    broad_mask = near_high & up_today & (dollar_volume >= args.loose_turnover)

    total_days = len(close) - args.high_lookback  # exclude warmup period
    strict_count = strict_mask.sum()
    strong_count = strong_mask.sum()
    broad_count = broad_mask.sum()

    # Overall return for the period
    overall_return = (close.iloc[-1] / close.iloc[0] - 1) * 100

    return {
        "ticker": ticker,
        "total_days": total_days,
        "overall_return_pct": round(overall_return, 1),
        "strict_triggers": int(strict_count),
        "strong_triggers": int(strong_count),
        "broad_triggers": int(broad_count),
        "strict_pct": round(strict_count / total_days * 100, 1) if total_days > 0 else 0,
        "strong_pct": round(strong_count / total_days * 100, 1) if total_days > 0 else 0,
        "broad_pct": round(broad_count / total_days * 100, 1) if total_days > 0 else 0,
    }


def main():
    args = parse_args()
    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]

    print(f"Downloading data for {len(tickers)} tickers: {', '.join(tickers)}")
    print(f"Date range: {args.start} to {args.end}")
    print(f"Strict turnover threshold: ${args.strict_turnover:,.0f}")
    print(f"Loose turnover threshold:  ${args.loose_turnover:,.0f}")
    print(f"Strong intraday threshold: {args.strong_threshold:.1%}")
    print(f"Rolling high lookback:     {args.high_lookback} days")
    print(f"Near-high percentage:      {args.high_pct:.0%}")
    print()

    data = yf.download(tickers, start=args.start, end=args.end, progress=False, threads=True)

    df_close = data["Close"]
    df_open = data["Open"]
    df_high = data["High"]
    df_low = data["Low"]
    df_volume = data["Volume"]

    # If only one ticker, yfinance returns a Series instead of DataFrame
    if len(tickers) == 1:
        ticker = tickers[0]
        df_close = pd.DataFrame({ticker: df_close})
        df_open = pd.DataFrame({ticker: df_open})
        df_high = pd.DataFrame({ticker: df_high})
        df_low = pd.DataFrame({ticker: df_low})
        df_volume = pd.DataFrame({ticker: df_volume})

    print("=" * 90)
    print("FILTER FEASIBILITY ANALYSIS")
    print("=" * 90)
    print()
    print("Filter definitions:")
    print(f"  Strict : Close >= {args.high_pct:.0%} of {args.high_lookback}d high + up today + "
          f"dollar volume >= ${args.strict_turnover/1e6:.0f}M")
    print(f"  Strong : Close >= {args.high_pct:.0%} of {args.high_lookback}d high + "
          f"intraday return >= {args.strong_threshold:.1%} + "
          f"dollar volume >= ${args.strict_turnover/1e6:.0f}M")
    print(f"  Broad  : Close >= {args.high_pct:.0%} of {args.high_lookback}d high + up today + "
          f"dollar volume >= ${args.loose_turnover/1e6:.0f}M")
    print()

    results = []
    for ticker in tickers:
        result = analyze_ticker(ticker, df_close, df_open, df_high, df_low, df_volume, args)
        if result is not None:
            results.append(result)

    # Print results table
    header = (
        f"{'Ticker':<8} {'Return':>8} {'Days':>6} "
        f"{'Strict':>8} {'Strong':>8} {'Broad':>8} "
        f"{'Strict%':>8} {'Strong%':>8} {'Broad%':>8}"
    )
    print(header)
    print("-" * len(header))

    for r in results:
        print(
            f"{r['ticker']:<8} "
            f"{r['overall_return_pct']:>7.1f}% "
            f"{r['total_days']:>6} "
            f"{r['strict_triggers']:>8} "
            f"{r['strong_triggers']:>8} "
            f"{r['broad_triggers']:>8} "
            f"{r['strict_pct']:>7.1f}% "
            f"{r['strong_pct']:>7.1f}% "
            f"{r['broad_pct']:>7.1f}%"
        )

    print()
    print("Interpretation:")
    print("  - If Strict triggers = 0, the filter is too tight and would miss this performer.")
    print("  - If Broad triggers >> Strict, consider relaxing turnover thresholds.")
    print("  - Higher trigger % means the filter catches the stock on more trading days.")

    if results:
        avg_strict = sum(r["strict_triggers"] for r in results) / len(results)
        avg_broad = sum(r["broad_triggers"] for r in results) / len(results)
        print(f"\n  Average Strict triggers per ticker: {avg_strict:.1f}")
        print(f"  Average Broad triggers per ticker:  {avg_broad:.1f}")
        if avg_strict > 0:
            print(f"  Broad/Strict ratio: {avg_broad / avg_strict:.1f}x")


if __name__ == "__main__":
    main()
