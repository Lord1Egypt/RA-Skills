#!/usr/bin/env python3
"""获取 Hyperliquid 永续合约持仓。需认证。"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Get Hyperliquid perpetual positions")
    parser.add_argument("--binding-id", type=str, required=True, help="Exchange API Key binding UUID")
    args = parser.parse_args()

    try:
        from _client import get_client
        client = get_client()

        result = client.get_hyperliquid_positions(binding_id=args.binding_id)

        print(json.dumps(result, ensure_ascii=False, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
