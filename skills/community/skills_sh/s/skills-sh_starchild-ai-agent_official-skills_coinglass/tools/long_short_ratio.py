#!/usr/bin/env python3
"""
Coinglass Long/Short Ratio Module

Provides aggregate long/short position ratio data across exchanges.
Ratio > 1 means more longs; < 1 means more shorts.
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional, List

from ._api import cg_request


def get_long_short_ratio(
    symbol: str = "BTC",
    interval: str = "h4"
) -> Optional[Dict[str, Any]]:
    """
    Get long/short ratio data across exchanges.

    Args:
        symbol: Coin symbol (BTC, ETH, etc.)
        interval: Time interval (h1, h4, h12, h24).

    Returns:
        Dict with exchange-level long/short data.

    Raises:
        CoinglassError: On API failure.
    """
    data = cg_request(
        "long_short", params={"symbol": symbol, "time_type": interval},
        version="v2"
    )

    # v2 returns wrapped data — may need to handle both list and dict
    return data


def get_exchange_ratio(
    symbol: str = "BTC",
    exchange: str = "Binance",
    interval: str = "h4"
) -> Optional[Dict[str, Any]]:
    """
    Get long/short ratio for a specific exchange.

    Args:
        symbol: Coin symbol.
        exchange: Exchange name.
        interval: Time interval.

    Returns:
        Dict with ratio, longPercent, shortPercent for the exchange.
        None if exchange not found in data.
    """
    data = get_long_short_ratio(symbol, interval)
    if not data:
        return None

    # Data may be a list of exchange entries
    entries = data if isinstance(data, list) else [data]
    for entry in entries:
        if entry.get("exchangeName", "").lower() == exchange.lower():
            long_pct = entry.get("longRate", 0)
            short_pct = entry.get("shortRate", 0)
            ratio = long_pct / short_pct if short_pct else 0
            return {
                "symbol": symbol.upper(),
                "exchange": entry.get("exchangeName"),
                "long_percent": long_pct * 100,
                "short_percent": short_pct * 100,
                "ratio": ratio,
            }
    return None


def get_sentiment(
    symbol: str = "BTC",
    interval: str = "h4"
) -> Optional[Dict[str, Any]]:
    """
    Get aggregated market sentiment from long/short ratios.

    Args:
        symbol: Coin symbol.
        interval: Time interval.

    Returns:
        Dict with avg ratio, sentiment label, and per-exchange breakdown.
    """
    data = get_long_short_ratio(symbol, interval)
    if not data:
        return None

    entries = data if isinstance(data, list) else [data]
    ratios = []
    for entry in entries:
        long_r = entry.get("longRate", 0)
        short_r = entry.get("shortRate", 0)
        if short_r:
            ratios.append({
                "exchange": entry.get("exchangeName", ""),
                "ratio": long_r / short_r,
            })

    if not ratios:
        return None

    avg_ratio = sum(r["ratio"] for r in ratios) / len(ratios)
    if avg_ratio > 1.2:
        sentiment = "Very Bullish"
    elif avg_ratio > 1.0:
        sentiment = "Bullish"
    elif avg_ratio > 0.8:
        sentiment = "Bearish"
    else:
        sentiment = "Very Bearish"

    return {
        "symbol": symbol.upper(),
        "avg_ratio": avg_ratio,
        "sentiment": sentiment,
        "exchanges": ratios,
    }


def compare_exchanges(
    symbol: str = "BTC",
    interval: str = "h4"
) -> Optional[List[Dict[str, Any]]]:
    """
    Compare long/short ratios across all exchanges.

    Returns:
        Sorted list of exchanges by ratio (most bullish first).
    """
    data = get_long_short_ratio(symbol, interval)
    if not data:
        return None

    entries = data if isinstance(data, list) else [data]
    results = []
    for entry in entries:
        long_r = entry.get("longRate", 0)
        short_r = entry.get("shortRate", 0)
        ratio = long_r / short_r if short_r else 0
        results.append({
            "exchange": entry.get("exchangeName", ""),
            "ratio": round(ratio, 4),
            "long_percent": round(long_r * 100, 2),
            "short_percent": round(short_r * 100, 2),
        })

    results.sort(key=lambda x: x["ratio"], reverse=True)
    return results if results else None


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Coinglass Long/Short Ratio Tools"
    )
    parser.add_argument("--symbol", "-s", default="BTC")
    parser.add_argument("--exchange", "-e", default=None)
    parser.add_argument("--interval", "-i", default="h4")
    parser.add_argument("--sentiment", action="store_true",
                        help="Show sentiment analysis")
    parser.add_argument("--compare", action="store_true",
                        help="Compare across exchanges")
    args = parser.parse_args()

    try:
        if args.sentiment:
            result = get_sentiment(args.symbol, args.interval)
        elif args.compare:
            result = compare_exchanges(args.symbol, args.interval)
        elif args.exchange:
            result = get_exchange_ratio(
                args.symbol, args.exchange, args.interval
            )
        else:
            result = get_long_short_ratio(args.symbol, args.interval)

        if result:
            print(json.dumps(result, indent=2))
        else:
            print("No data found", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
