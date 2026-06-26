#!/usr/bin/env python3
"""
Coinglass ETF Module (Non-Bitcoin)

Provides ETF data for Ethereum, Solana, XRP, and HK listings.
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional, List

from ._api import cg_request


def get_eth_etf_flows() -> Optional[List[Dict[str, Any]]]:
    """Get Ethereum ETF flow history (inflows/outflows)."""
    return cg_request("api/etf/ethereum/flow-history")


def get_eth_etf_list() -> Optional[List[Dict[str, Any]]]:
    """Get list of all Ethereum ETFs with details."""
    return cg_request("api/etf/ethereum/list")


def get_eth_etf_premium_discount() -> Optional[List[Dict[str, Any]]]:
    """Get Ethereum ETF premium/discount history."""
    return cg_request("api/etf/ethereum/premium-discount/history")


def get_sol_etf_flows() -> Optional[List[Dict[str, Any]]]:
    """Get Solana ETF flow history."""
    return cg_request("api/etf/solana/flow-history")


def get_sol_etf_list() -> Optional[List[Dict[str, Any]]]:
    """Get list of all Solana ETFs."""
    return cg_request("api/etf/solana/list")


def get_xrp_etf_flows() -> Optional[List[Dict[str, Any]]]:
    """Get XRP ETF flow history."""
    return cg_request("api/etf/xrp/flow-history")


def get_xrp_etf_list() -> Optional[List[Dict[str, Any]]]:
    """Get list of all XRP ETFs."""
    return cg_request("api/etf/xrp/list")


def get_hk_eth_etf_flows() -> Optional[List[Dict[str, Any]]]:
    """Get Hong Kong Ethereum ETF flows."""
    return cg_request("api/hk-etf/ethereum/flow-history")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Coinglass ETF Tools")
    parser.add_argument("action", choices=[
        "eth-flows", "eth-list", "sol-flows", "xrp-flows"
    ])
    parser.add_argument("--json", "-j", action="store_true")
    args = parser.parse_args()

    actions = {
        "eth-flows": get_eth_etf_flows,
        "eth-list": get_eth_etf_list,
        "sol-flows": get_sol_etf_flows,
        "xrp-flows": get_xrp_etf_flows,
    }

    try:
        result = actions[args.action]()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
