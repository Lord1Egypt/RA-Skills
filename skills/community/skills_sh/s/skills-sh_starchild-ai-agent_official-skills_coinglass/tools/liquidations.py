#!/usr/bin/env python3
"""
Coinglass Liquidations Module

Provides liquidation data across exchanges: individual liquidations
and aggregated (long/short) liquidation summaries.
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional

from ._api import cg_request


def get_liquidations(
    symbol: str = "BTC",
    time_type: str = "h24"
) -> Optional[Dict[str, Any]]:
    """
    Get liquidation data across exchanges.

    Args:
        symbol: Coin symbol (BTC, ETH, SOL, etc.)
        time_type: Time window (h1, h4, h12, h24).

    Returns:
        Dict with liquidation data: long/short amounts, counts.

    Raises:
        CoinglassError: On API failure.
    """
    # Map h-format to API format
    range_map = {"h1": "1h", "h4": "4h", "h12": "12h", "h24": "24h"}
    v4_range = range_map.get(time_type, time_type)
    params = {"symbol": symbol.upper(), "range": v4_range}
    return cg_request(
        "api/futures/liquidation/exchange-list", params=params
    )


def get_liquidation_aggregated(
    symbol: str = "BTC",
    time_type: str = "h24"
) -> Optional[Dict[str, Any]]:
    """
    Get aggregated liquidation summary (total longs vs shorts).

    Args:
        symbol: Coin symbol.
        interval: Time interval.

    Returns:
        Dict with total long/short liquidations and ratio.
    """
    data = get_liquidations(symbol, time_type)
    if not data:
        return None

    # Aggregate across exchanges
    entries = data if isinstance(data, list) else [data]
    total_long = 0
    total_short = 0
    for entry in entries:
        total_long += entry.get("longLiquidationUsd", 0) or 0
        total_short += entry.get("shortLiquidationUsd", 0) or 0

    total = total_long + total_short
    return {
        "symbol": symbol.upper(),
        "interval": time_type,
        "total_long_usd": total_long,
        "total_short_usd": total_short,
        "total_usd": total,
        "long_ratio": total_long / total if total else 0,
        "short_ratio": total_short / total if total else 0,
        "dominant": "long" if total_long > total_short else "short",
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Coinglass Liquidation Tools"
    )
    parser.add_argument("--symbol", "-s", default="BTC")
    parser.add_argument("--interval", "-i", default="h4")
    parser.add_argument("--exchange", "-e", default=None)
    parser.add_argument("--aggregated", "-a", action="store_true",
                        help="Show aggregated summary")
    args = parser.parse_args()

    try:
        if args.aggregated:
            result = get_liquidation_aggregated(
                args.symbol, args.interval
            )
        else:
            result = get_liquidations(
                args.symbol, args.interval
            )

        if result:
            print(json.dumps(result, indent=2))
        else:
            print("No data found", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
