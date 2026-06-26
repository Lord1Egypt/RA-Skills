# tokenview_balance_checker API client

"""Utility to fetch token balances from Tokenview API for multiple chains.
Supported chains: BTC, ETH, BSC, TRON.
The client provides a simple `get_balance(address, chain)` function returning the balance as a string.
"""

#!/usr/bin/env python3
import os
import sys
import json
import argparse
import requests

# {lowercase-coin-abbr}/{address}?apikey={apikey}
BASE_URL = "https://services.tokenview.io/vipapi/addr/b"

# Mapping of chain identifiers to Tokenview API endpoints
CHAIN_ENDPOINTS = {
    "btc": "btc",
    "eth": "eth",
    "bsc": "bsc",
    "tron": "trx",
}

def get_balance(address: str, chain: str = "btc") -> str:
    api_key = os.environ.get("TOKENVIEW_API_KEY")
    if not api_key:
        print(json.dumps({"code": -1, "msg": "API Key not configured", "data": "NONE"}))
        sys.exit(1)
    if not address:
        print(json.dumps({"code": -2, "msg": "Address is required", "data": "NONE"}))
        sys.exit(1)
    """Fetch the balance for a given address on a specified chain.

    Args:
        address: The wallet address.
        chain: One of "btc", "eth", "bsc", "tron". If None, auto‑detect.

    Returns:
        Balance as a string. Raises ValueError for unsupported chain or request errors.
    """
    if chain is None:
        # Auto‑detect chain from address pattern
        if address.startswith('0x'):
            # Could be ETH or BSC; default to eth
            chain = 'eth'
        elif address.startswith('T'):
            chain = 'tron'
        elif address.isdigit():
            # Simple heuristic: numeric address likely BTC (legacy)
            chain = 'btc'
        else:
            # Fallback: try eth format detection (checksum address length)
            if len(address) == 42:
                chain = 'eth'
            else:
                raise ValueError(f"Unable to auto‑detect chain for address: {address}")
    else:
        chain = chain.lower()

    if chain not in CHAIN_ENDPOINTS:
        raise ValueError(f"Unsupported chain: {chain}. Supported: {list(CHAIN_ENDPOINTS)}")

    coin = CHAIN_ENDPOINTS.get(chain)
        
    url = f"{BASE_URL}/{coin}/{address}?apikey={api_key}"  # e.g. https://services.tokenview.io/vipapi/addr/b/eth/0x... 
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # 成功格式
        if data.get("code") == 1 and (str(data.get("msg")).lower() == "成功" or str(data.get("msg")).lower() == "success"):
            balance = data.get("data")
            coin_display = chain.upper()
            print(json.dumps({"code": 1, "msg": "成功", "data": f"{balance} {coin_display}"}))
        else:
            # 使用 API 返回的错误字段格式
            print(json.dumps({"code": data.get("code", 1), "msg": str(data.get("msg", "")), "data": data.get("data", "NONE")}))

    except requests.exceptions.RequestException as e:
        print(json.dumps({"code": -3, "msg": f"Network error: {e}", "data": "NONE"}))
        sys.exit(1)
    except json.JSONDecodeError:
        print(json.dumps({"code": -4, "msg": "Failed to parse API response", "data": "NONE"}))
        sys.exit(1)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Query Tokenview balance for an address.")
    p.add_argument("address", help="Blockchain address to query.")
    p.add_argument("--coin", default="btc", help="Coin abbreviation (default: btc).")
    args = p.parse_args()
    get_balance(args.address, args.coin)