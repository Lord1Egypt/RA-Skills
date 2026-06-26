#!/usr/bin/env python3
"""获取 Binance 现货账户余额（普通账户和PM账户通用）"""
import sys
import json
import argparse
from _client import get_client

def main():
    parser = argparse.ArgumentParser(description="获取 Binance 现货账户余额")
    parser.add_argument("--binding-id", type=str, required=True, help="交易所 API 的 id（来自 list_exchange_apis）")
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.get_account_balance(args.binding_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
