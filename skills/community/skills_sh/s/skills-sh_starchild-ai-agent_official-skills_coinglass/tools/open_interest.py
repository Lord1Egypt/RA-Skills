#!/usr/bin/env python3
"""
Coinglass Open Interest Module

Fetch aggregate open interest data across major cryptocurrency exchanges.
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional, List

from ._api import cg_request

# MCP Tool Schema
MCP_OPEN_INTEREST_SCHEMA = {
    "name": "cg_open_interest",
    "title": "Coinglass Open Interest",
    "description": (
        "Get aggregate open interest across exchanges for a symbol."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "symbol": {
                "type": "string",
                "description": "Symbol (BTC, ETH, SOL, etc.)"
            },
            "interval": {
                "type": "string",
                "description": "Time interval: 0 (all), h1, h4, h12, h24",
                "default": "0",
                "enum": ["0", "h1", "h4", "h12", "h24"]
            }
        },
        "required": ["symbol"],
        "additionalProperties": False
    }
}


def get_open_interest(
    symbol: str = "BTC",
    interval: str = "0"
) -> Optional[Dict[str, Any]]:
    """
    Get aggregate open interest across exchanges for a symbol.

    Uses v2 API for basic OI data.

    Args:
        symbol: Coin symbol (BTC, ETH, SOL, etc.)
        interval: Time interval (0=all, h1, h4, h12, h24).

    Returns:
        Dict with open interest data by exchange.

    Raises:
        CoinglassError: On API failure.
    """
    return cg_request(
        "open_interest",
        params={"symbol": symbol, "interval": interval},
        version="v2"
    )


def get_open_interest_history(
    symbol: str = "BTC",
    interval: str = "h4",
    exchange: Optional[str] = None
) -> Optional[List[Dict[str, Any]]]:
    """
    Get open interest history (aggregated across exchanges).

    Uses v4 API for historical data.

    Args:
        symbol: Coin symbol.
        interval: Time interval (h1, h4, h12, h24).
        exchange: Optional exchange filter.

    Returns:
        List of historical OI data points.
    """
    params = {"symbol": symbol, "interval": interval}
    if exchange:
        params["exchange"] = exchange
    return cg_request(
        "api/futures/open-interest/aggregated-history",
        params=params
    )


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Coinglass Open Interest Tools"
    )
    parser.add_argument("--symbol", "-s", default="BTC")
    parser.add_argument("--interval", "-i", default="h4")
    parser.add_argument("--exchange", "-e", default=None)
    parser.add_argument("--history", action="store_true",
                        help="Show OI history")
    parser.add_argument("--json", "-j", action="store_true")
    args = parser.parse_args()

    try:
        if args.history:
            result = get_open_interest_history(
                args.symbol, args.interval, args.exchange
            )
        else:
            result = get_open_interest(args.symbol, args.interval)

        if result:
            print(json.dumps(result, indent=2))
        else:
            print("No data found", file=sys.stderr)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
