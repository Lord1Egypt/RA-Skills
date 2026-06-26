#!/usr/bin/env python3
"""Fetch options chain for nearest expiry. Put/call ratio, IV, unusual volume."""
import argparse
import json
import sys


def chain_to_records(chain):
    """Convert options chain DataFrame to list of dicts."""
    if chain is None or chain.empty:
        return []
    records = []
    for _, row in chain.iterrows():
        record = {}
        for col in chain.columns:
            val = row[col]
            if hasattr(val, "isoformat"):
                record[col] = val.isoformat()
            elif isinstance(val, float) and (val != val):
                record[col] = None
            elif isinstance(val, bool):
                record[col] = val
            else:
                try:
                    record[col] = float(val) if isinstance(val, (int, float)) else val
                except (TypeError, ValueError):
                    record[col] = str(val)
        records.append(record)
    return records


def main():
    parser = argparse.ArgumentParser(description="Fetch options chain for nearest expiry date.")
    parser.add_argument("ticker", help="Stock ticker symbol")
    parser.add_argument("--expiry-index", type=int, default=0, help="Index of expiry date to use (0=nearest)")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run with: uv run --with yfinance", file=sys.stderr)
        sys.exit(1)

    ticker = args.ticker.upper()
    t = yf.Ticker(ticker)

    # Get available expiry dates
    try:
        expirations = t.options
    except Exception as e:
        print(json.dumps({"error": f"Could not fetch options: {e}"}))
        sys.exit(1)

    if not expirations:
        print(json.dumps({"error": f"No options data available for {ticker}"}))
        sys.exit(1)

    idx = min(args.expiry_index, len(expirations) - 1)
    expiry = expirations[idx]
    chain = t.option_chain(expiry)

    calls = chain.calls
    puts = chain.puts

    # Aggregate stats
    total_call_volume = int(calls["volume"].sum()) if "volume" in calls.columns else 0
    total_put_volume = int(puts["volume"].sum()) if "volume" in puts.columns else 0
    total_call_oi = int(calls["openInterest"].sum()) if "openInterest" in calls.columns else 0
    total_put_oi = int(puts["openInterest"].sum()) if "openInterest" in puts.columns else 0

    put_call_volume_ratio = round(total_put_volume / total_call_volume, 4) if total_call_volume > 0 else None
    put_call_oi_ratio = round(total_put_oi / total_call_oi, 4) if total_call_oi > 0 else None

    # Average IV
    avg_call_iv = round(float(calls["impliedVolatility"].mean()), 4) if "impliedVolatility" in calls.columns else None
    avg_put_iv = round(float(puts["impliedVolatility"].mean()), 4) if "impliedVolatility" in puts.columns else None

    # Unusual volume: options where volume > 2x open interest and volume > 100
    unusual = []
    for side, df, label in [(calls, calls, "call"), (puts, puts, "put")]:
        if "volume" in df.columns and "openInterest" in df.columns:
            for _, row in df.iterrows():
                vol = row.get("volume", 0) or 0
                oi = row.get("openInterest", 0) or 0
                if vol > 100 and oi > 0 and vol > 2 * oi:
                    unusual.append({
                        "type": label,
                        "strike": float(row["strike"]),
                        "volume": int(vol),
                        "openInterest": int(oi),
                        "vol_oi_ratio": round(vol / oi, 2),
                        "impliedVolatility": round(float(row.get("impliedVolatility", 0)), 4),
                    })

    unusual.sort(key=lambda x: x["vol_oi_ratio"], reverse=True)

    result = {
        "ticker": ticker,
        "expiry": expiry,
        "available_expiries": list(expirations[:5]),
        "summary": {
            "total_call_volume": total_call_volume,
            "total_put_volume": total_put_volume,
            "total_call_oi": total_call_oi,
            "total_put_oi": total_put_oi,
            "put_call_volume_ratio": put_call_volume_ratio,
            "put_call_oi_ratio": put_call_oi_ratio,
            "avg_call_iv": avg_call_iv,
            "avg_put_iv": avg_put_iv,
        },
        "unusual_volume": unusual[:10],
        "calls_count": len(calls),
        "puts_count": len(puts),
    }

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
