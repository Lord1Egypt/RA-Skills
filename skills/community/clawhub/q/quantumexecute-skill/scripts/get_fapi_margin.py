#!/usr/bin/env python3
"""获取普通账户可用保证金"""
import sys
import json
import argparse
from _client import get_client

def main():
    parser = argparse.ArgumentParser(description="获取普通账户可用保证金")
    parser.add_argument("--binding-id", type=str, required=True, help="交易所 API 的 id（来自 list_exchange_apis）")
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.get_margin_balance(args.binding_id)

        if "balances" in result:
            result["balances"] = [b for b in result["balances"] if float(b.get("walletBalance", 0)) != 0]

        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
