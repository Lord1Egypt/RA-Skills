#!/usr/bin/env python3
"""Fetch insider transactions and institutional holders for a stock ticker."""
import argparse
import json
import sys


def df_to_records(df):
    """Convert a DataFrame to a list of dicts, handling NaN and Timestamps."""
    if df is None or df.empty:
        return []
    records = []
    for _, row in df.iterrows():
        record = {}
        for col in df.columns:
            val = row[col]
            if hasattr(val, "isoformat"):
                record[col] = val.isoformat()
            elif isinstance(val, float) and (val != val):  # NaN check
                record[col] = None
            else:
                record[col] = val
        records.append(record)
    return records


def main():
    parser = argparse.ArgumentParser(description="Fetch insider transactions and institutional holders.")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--limit", type=int, default=20, help="Max insider transactions to show (default: 20)")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run with: uv run --with yfinance", file=sys.stderr)
        sys.exit(1)

    ticker = args.ticker.upper()
    t = yf.Ticker(ticker)

    # Insider transactions
    insider_tx = []
    try:
        it = t.insider_transactions
        if it is not None and not it.empty:
            insider_tx = df_to_records(it.head(args.limit))
    except Exception:
        pass

    # Insider purchases (summary)
    insider_purchases = []
    try:
        ip = t.insider_purchases
        if ip is not None and not ip.empty:
            insider_purchases = df_to_records(ip)
    except Exception:
        pass

    # Institutional holders
    institutional = []
    try:
        ih = t.institutional_holders
        if ih is not None and not ih.empty:
            institutional = df_to_records(ih.head(args.limit))
    except Exception:
        pass

    # Major holders summary
    major_holders = []
    try:
        mh = t.major_holders
        if mh is not None and not mh.empty:
            for _, row in mh.iterrows():
                major_holders.append({"value": str(row.iloc[0]), "description": str(row.iloc[1])})
    except Exception:
        pass

    result = {
        "ticker": ticker,
        "major_holders": major_holders,
        "insider_transactions": insider_tx,
        "insider_purchases_summary": insider_purchases,
        "top_institutional_holders": institutional,
    }

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
