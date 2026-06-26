#!/usr/bin/env python3
"""获取 LTP 账户持仓信息"""
import sys
import json
import argparse
from _client import get_client


def main():
    parser = argparse.ArgumentParser(description="获取 LTP 账户持仓信息")
    parser.add_argument("--binding-id", type=str, required=True, help="交易所 API 的 id（来自 list_exchange_apis）")
    parser.add_argument("--sym", type=str, help="交易对筛选，如 BTCUSDT")
    args = parser.parse_args()

    try:
        client = get_client()
        if args.sym:
            result = client.get_ltp_position(args.binding_id, sym=args.sym)
        else:
            result = client.get_ltp_position(args.binding_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
