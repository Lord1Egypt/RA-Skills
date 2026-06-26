#!/usr/bin/env python3
"""
Coinglass Hyperliquid Module

Provides Hyperliquid-specific data: whale alerts, whale positions,
positions by coin, user positions, and position distribution.
"""

import sys
import json
import argparse
from typing import Dict, Any, List, Optional

from ._api import cg_request


def get_whale_alerts() -> Optional[List[Dict[str, Any]]]:
    """Get Hyperliquid whale position alerts (large position changes)."""
    return cg_request("api/hyperliquid/whale-alert")


def get_whale_positions() -> Optional[List[Dict[str, Any]]]:
    """Get current Hyperliquid whale positions."""
    return cg_request("api/hyperliquid/whale-position")


def get_positions_by_coin(
    symbol: str = "BTC"
) -> Optional[List[Dict[str, Any]]]:
    """
    Get Hyperliquid positions aggregated by coin.

    Args:
        symbol: Coin symbol (BTC, ETH, SOL, etc.)
    """
    return cg_request(
        "api/hyperliquid/position",
        params={"symbol": symbol}
    )


def get_user_positions(
    address: str = ""
) -> Optional[List[Dict[str, Any]]]:
    """
    Get positions for a specific Hyperliquid wallet.

    Args:
        address: Wallet address to query.
    """
    params = {}
    if address:
        params["address"] = address
    return cg_request(
        "api/hyperliquid/user-position",
        params=params or None
    )


def get_position_distribution(
    symbol: str = "BTC"
) -> Optional[Dict[str, Any]]:
    """
    Get wallet position distribution for a coin on Hyperliquid.

    Args:
        symbol: Coin symbol (BTC, ETH, SOL, etc.)
    """
    return cg_request(
        "api/hyperliquid/wallet/position-distribution",
        params={"symbol": symbol}
    )


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Coinglass Hyperliquid Tools"
    )
    parser.add_argument("action", choices=[
        "alerts", "whales", "coin", "user", "distribution"
    ])
    parser.add_argument("--symbol", "-s", default="BTC")
    parser.add_argument("--address", "-a", default="")
    args = parser.parse_args()

    actions = {
        "alerts": get_whale_alerts,
        "whales": get_whale_positions,
        "coin": lambda: get_positions_by_coin(args.symbol),
        "user": lambda: get_user_positions(args.address),
        "distribution": lambda: get_position_distribution(args.symbol),
    }

    try:
        result = actions[args.action]()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
