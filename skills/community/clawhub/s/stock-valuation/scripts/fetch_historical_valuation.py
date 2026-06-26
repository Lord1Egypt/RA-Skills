#!/usr/bin/env python3
"""Fetch 5-year historical PE ratio using quarterly earnings and price data.
For full 5-year history, run with: uv run --with yfinance --with lxml
"""
import argparse
import json
import sys
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Fetch 5-year PE history for a stock ticker.")
    parser.add_argument("ticker", help="Stock ticker symbol")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run with: uv run --with yfinance", file=sys.stderr)
        sys.exit(1)

    ticker = args.ticker.upper()
    t = yf.Ticker(ticker)

    # Get 5 years of price history
    hist = t.history(period="5y")
    if hist.empty:
        print(json.dumps({"error": f"No price history for {ticker}"}))
        sys.exit(1)

    # Try get_earnings_dates first (needs lxml, gives ~5yr of quarterly EPS)
    quarterly_eps = []  # list of (date, reported_eps)
    try:
        ed = t.get_earnings_dates(limit=24)
        if ed is not None and not ed.empty and "Reported EPS" in ed.columns:
            for dt_idx, row in ed.iterrows():
                eps = row["Reported EPS"]
                if eps is not None and not (isinstance(eps, float) and eps != eps):
                    dt = dt_idx
                    if hasattr(dt, "to_pydatetime"):
                        dt = dt.to_pydatetime()
                    quarterly_eps.append((dt, float(eps)))
            # Sort ascending by date
            quarterly_eps.sort(key=lambda x: x[0])
    except Exception:
        pass

    # Fallback: use quarterly_income_stmt (typically only ~5 quarters)
    if len(quarterly_eps) < 4:
        quarterly_eps = []
        earnings = t.quarterly_income_stmt
        if earnings is not None and not earnings.empty:
            for label in ["Diluted EPS", "Basic EPS"]:
                if label in earnings.index:
                    eps_row = earnings.loc[label].dropna().sort_index()
                    for dt, val in eps_row.items():
                        quarterly_eps.append((dt, float(val)))
                    break

    if len(quarterly_eps) < 4:
        print(json.dumps({"error": f"Insufficient EPS data for {ticker} (need 4+ quarters, got {len(quarterly_eps)})"}))
        sys.exit(1)

    # Build trailing-12-month EPS at each quarter end, then compute PE
    pe_history = []
    # Normalize hist index to tz-naive for comparison
    import pandas as pd
    if hist.index.tzinfo is not None or (hasattr(hist.index, "tz") and hist.index.tz is not None):
        hist_naive = hist.index.tz_localize(None)
    else:
        hist_naive = hist.index

    for i in range(3, len(quarterly_eps)):
        ttm_eps = sum(quarterly_eps[j][1] for j in range(i - 3, i + 1))
        if ttm_eps <= 0:
            continue

        quarter_date = quarterly_eps[i][0]
        # Convert to naive datetime for comparison
        if hasattr(quarter_date, "to_pydatetime"):
            quarter_date = quarter_date.to_pydatetime()
        if hasattr(quarter_date, "tzinfo") and quarter_date.tzinfo is not None:
            quarter_date = quarter_date.replace(tzinfo=None)
        target = pd.Timestamp(quarter_date)

        mask = hist_naive <= target
        if not mask.any():
            continue

        import numpy as np
        indices = np.where(mask)[0]
        price = float(hist.iloc[indices[-1]]["Close"])
        pe = price / ttm_eps

        pe_history.append({
            "date": str(target.date()),
            "price": round(price, 2),
            "ttm_eps": round(ttm_eps, 2),
            "pe_ratio": round(pe, 2),
        })

    if not pe_history:
        print(json.dumps({"error": "Could not compute PE history"}))
        sys.exit(1)

    pe_values = [p["pe_ratio"] for p in pe_history]
    current_pe = pe_values[-1]

    # Percentile: what % of historical PEs are below current
    below = sum(1 for p in pe_values if p < current_pe)
    percentile = round(below / len(pe_values) * 100, 1)

    result = {
        "ticker": ticker,
        "current_pe": current_pe,
        "pe_5yr_avg": round(sum(pe_values) / len(pe_values), 2),
        "pe_5yr_min": round(min(pe_values), 2),
        "pe_5yr_max": round(max(pe_values), 2),
        "pe_5yr_median": round(sorted(pe_values)[len(pe_values) // 2], 2),
        "current_percentile": percentile,
        "num_quarters": len(pe_history),
        "pe_history": pe_history,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
