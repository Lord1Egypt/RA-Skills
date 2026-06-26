#!/usr/bin/env python3
"""
Coinglass Whale Transfer Module

Provides on-chain whale transfer data including:
- Large transfers (minimum $10M) across major blockchains
- Bitcoin, Ethereum, Tron, Ripple, Dogecoin, Litecoin, Polygon,
  Algorand, Bitcoin Cash, Solana
- Past 6 months of data
"""

import sys
import json
import argparse
from typing import Dict, Any, Optional

from ._api import cg_request


def get_whale_transfers() -> Optional[Dict[str, Any]]:
    """
    Get large on-chain transfers (minimum $10M) across major blockchains.

    Returns:
        List of whale transfers with transaction hash, asset, amount,
        exchange, transfer type (1=inflow, 2=outflow, 3=internal),
        addresses, and timestamp.

    Raises:
        CoinglassError: On API failure with actionable error message.
    """
    return cg_request("api/chain/v2/whale-transfer")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Coinglass Whale Transfer Tool"
    )
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output as JSON")
    parser.parse_args()

    try:
        result = get_whale_transfers()
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
