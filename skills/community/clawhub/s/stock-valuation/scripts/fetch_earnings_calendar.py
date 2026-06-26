#!/usr/bin/env python3
"""Fetch next earnings date and days until earnings for a stock ticker."""
import argparse
import json
import sys
from datetime import datetime, timezone


def main():
    parser = argparse.ArgumentParser(description="Fetch next earnings date and days until.")
    parser.add_argument("ticker", help="Stock ticker symbol")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run with: uv run --with yfinance", file=sys.stderr)
        sys.exit(1)

    ticker = args.ticker.upper()
    t = yf.Ticker(ticker)

    # Get earnings dates
    earnings_dates = None
    try:
        ed = t.earnings_dates
        if ed is not None and not ed.empty:
            earnings_dates = ed
    except Exception:
        pass

    # Also check calendar
    calendar_data = {}
    try:
        cal = t.calendar
        if cal is not None:
            if isinstance(cal, dict):
                calendar_data = {k: str(v) if hasattr(v, "isoformat") else v for k, v in cal.items()}
            elif hasattr(cal, "to_dict"):
                calendar_data = {str(k): str(v) for k, v in cal.to_dict().items()}
    except Exception:
        pass

    now = datetime.now(timezone.utc)
    next_earnings = None
    days_until = None
    upcoming = []
    past = []

    if earnings_dates is not None:
        for dt_idx in earnings_dates.index:
            dt = dt_idx
            if hasattr(dt, "to_pydatetime"):
                dt = dt.to_pydatetime()
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)

            row_data = {}
            for col in earnings_dates.columns:
                val = earnings_dates.loc[dt_idx, col]
                if hasattr(val, "isoformat"):
                    row_data[col] = val.isoformat()
                elif isinstance(val, float) and val != val:
                    row_data[col] = None
                else:
                    row_data[col] = val

            entry = {"date": dt.strftime("%Y-%m-%d %H:%M:%S %Z"), **row_data}

            if dt >= now:
                upcoming.append((dt, entry))
            else:
                past.append(entry)

    # Sort upcoming by date ascending
    upcoming.sort(key=lambda x: x[0])

    if upcoming:
        next_dt, next_entry = upcoming[0]
        next_earnings = next_entry["date"]
        days_until = (next_dt - now).days

    # Fallback: parse next earnings from calendar if earnings_dates failed
    if next_earnings is None and calendar_data:
        cal_dates = calendar_data.get("Earnings Date")
        if cal_dates:
            if isinstance(cal_dates, list):
                cal_dates = cal_dates[0]
            try:
                next_dt = datetime.strptime(str(cal_dates)[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
                next_earnings = str(cal_dates)
                days_until = (next_dt - now).days
            except (ValueError, TypeError):
                pass

    result = {
        "ticker": ticker,
        "next_earnings_date": next_earnings,
        "days_until_earnings": days_until,
        "upcoming_earnings": [e for _, e in upcoming[:4]],
        "recent_earnings": past[:4],
        "calendar": calendar_data,
    }

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
