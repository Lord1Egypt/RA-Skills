#!/usr/bin/env python3
"""查询当前用户绑定的交易所 API 列表。需认证。"""
import argparse
import json
import sys
import os

# Allow importing _client from same directory when run from project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def _mask_api_key(value):
    if not isinstance(value, str):
        return value
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}{'*' * (len(value) - 8)}{value[-4:]}"

def _mask_result(result):
    if not isinstance(result, dict):
        return result
    items = result.get("items")
    if not isinstance(items, list):
        return result
    masked_items = []
    for item in items:
        if isinstance(item, dict) and "apiKey" in item:
            item = dict(item)
            item["apiKey"] = _mask_api_key(item.get("apiKey"))
        masked_items.append(item)
    result = dict(result)
    result["items"] = masked_items
    return result

def main():
    parser = argparse.ArgumentParser(description="List exchange APIs")
    parser.add_argument("--page", type=int, default=None, help="Page number")
    parser.add_argument("--page-size", type=int, default=None, help="Page size")
    parser.add_argument("--exchange", type=str, default=None, help="Filter by exchange: Binance, OKX, LTP, Deribit, Hyperliquid")
    args = parser.parse_args()
    try:
        from _client import get_client
        client = get_client()
        params = {}
        if args.page is not None:
            params["page"] = args.page
        if args.page_size is not None:
            params["pageSize"] = args.page_size
        if args.exchange is not None:
            params["exchange"] = args.exchange
        result = client.list_exchange_apis(**params)
        result = _mask_result(result)
        print(json.dumps(result, ensure_ascii=False, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
