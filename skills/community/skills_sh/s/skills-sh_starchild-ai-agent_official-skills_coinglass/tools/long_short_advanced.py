#!/usr/bin/env python3
"""
Coinglass Long/Short Advanced Module

Provides advanced long/short data: global account ratio,
top trader ratios, taker buy/sell by exchange, net positions.
"""

import sys
import json
import argparse
from typing import Dict, Any, List, Optional

from ._api import cg_request


def _to_pair(symbol: str) -> str:
    """Convert symbol to trading pair (BTC → BTCUSDT)."""
    s = symbol.upper()
    return s if s.endswith("USDT") else f"{s}USDT"


# Exchange name normalization for consistent API calls
_EXCHANGE_ALIASES = {
    "binance": "Binance", "okx": "OKX", "bybit": "Bybit",
    "bitget": "Bitget", "gate": "Gate", "bitmex": "Bitmex",
    "dydx": "dYdX", "kraken": "Kraken", "coinex": "CoinEx",
}


def _normalize_exchange(name: str) -> str:
    """Normalize exchange name to Coinglass format."""
    return _EXCHANGE_ALIASES.get(name.lower(), name)


def get_global_account_ratio(
    symbol: str = "BTC",
    exchange: str = "Binance",
    interval: str = "1h"
) -> Optional[List[Dict[str, Any]]]:
    """
    Get global long/short account ratio history.

    Args:
        symbol: Coin symbol.
        interval: Time interval (h1, h4, h12, h24).
        exchange: Optional exchange filter.
    """
    params = {
        "symbol": _to_pair(symbol),
        "exchange": _normalize_exchange(exchange),
        "interval": interval,
    }
    return cg_request(
        "api/futures/global-long-short-account-ratio/history",
        params=params
    )


def get_top_account_ratio(
    symbol: str = "BTC",
    exchange: str = "Binance",
    interval: str = "1h"
) -> Optional[List[Dict[str, Any]]]:
    """
    Get top trader long/short account ratio history.

    Args:
        symbol: Coin symbol.
        interval: Time interval.
        exchange: Optional exchange filter.
    """
    params = {
        "symbol": _to_pair(symbol),
        "exchange": _normalize_exchange(exchange),
        "interval": interval,
    }
    return cg_request(
        "api/futures/top-long-short-account-ratio/history",
        params=params
    )


def get_top_position_ratio(
    symbol: str = "BTC",
    exchange: str = "Binance",
    interval: str = "1h"
) -> Optional[List[Dict[str, Any]]]:
    """
    Get top trader long/short position ratio history.

    Args:
        symbol: Coin symbol.
        interval: Time interval.
        exchange: Optional exchange filter.
    """
    params = {
        "symbol": _to_pair(symbol),
        "exchange": _normalize_exchange(exchange),
        "interval": interval,
    }
    return cg_request(
        "api/futures/top-long-short-position-ratio/history",
        params=params
    )


def get_taker_buysell_exchanges(
    symbol: str = "BTC",
    range_type: str = "4h"
) -> Optional[List[Dict[str, Any]]]:
    """
    Get taker buy/sell volume by exchange.

    Args:
        symbol: Coin symbol.
    """
    return cg_request(
        "api/futures/taker-buy-sell-volume/exchange-list",
        params={"symbol": symbol, "range": range_type}
    )


def get_net_position(
    symbol: str = "BTC",
    exchange: str = "Binance",
    interval: str = "1h"
) -> Optional[List[Dict[str, Any]]]:
    """
    Get net position history (v1).

    Args:
        symbol: Coin symbol.
        interval: Time interval.
        exchange: Optional exchange filter.
    """
    params = {
        "symbol": _to_pair(symbol),
        "exchange": _normalize_exchange(exchange),
        "interval": interval,
    }
    return cg_request(
        "api/futures/net-position/history", params=params
    )


def get_net_position_v2(
    symbol: str = "BTC",
    exchange: str = "Binance",
    interval: str = "1h"
) -> Optional[List[Dict[str, Any]]]:
    """
    Get net position history (v2 — more exchanges).

    Args:
        symbol: Coin symbol.
        interval: Time interval.
        exchange: Optional exchange filter.
    """
    params = {
        "symbol": _to_pair(symbol),
        "exchange": _normalize_exchange(exchange),
        "interval": interval,
    }
    return cg_request(
        "api/futures/v2/net-position/history", params=params
    )


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Coinglass Long/Short Advanced Tools"
    )
    parser.add_argument("action", choices=[
        "global", "top-account", "top-position",
        "taker", "net", "net-v2"
    ])
    parser.add_argument("--symbol", "-s", default="BTC")
    parser.add_argument("--exchange", "-e", default=None)
    parser.add_argument("--interval", "-i", default="h4")
    args = parser.parse_args()

    actions = {
        "global": lambda: get_global_account_ratio(
            args.symbol, args.exchange or "Binance", args.interval
        ),
        "top-account": lambda: get_top_account_ratio(
            args.symbol, args.exchange or "Binance", args.interval
        ),
        "top-position": lambda: get_top_position_ratio(
            args.symbol, args.exchange or "Binance", args.interval
        ),
        "taker": lambda: get_taker_buysell_exchanges(args.symbol),
        "net": lambda: get_net_position(
            args.symbol, args.exchange or "Binance", args.interval
        ),
        "net-v2": lambda: get_net_position_v2(
            args.symbol, args.exchange or "Binance", args.interval
        ),
    }

    try:
        result = actions[args.action]()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
