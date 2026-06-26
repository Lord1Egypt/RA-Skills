#!/usr/bin/env python3
"""获取 PM 账户 U 本位合约持仓"""
import sys
import json
import argparse
from _client import get_client

def main():
    parser = argparse.ArgumentParser(description="获取 PM 账户 U 本位合约持仓")
    parser.add_argument("--binding-id", type=str, required=True, help="交易所 API 的 id（来自 list_exchange_apis）")
    parser.add_argument("--symbol", type=str, help="交易对筛选，如 BTCUSDT")
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.get_um_account(args.binding_id)

        if "positions" in result:
            if args.symbol:
                # 指定交易对时，返回该交易对信息（即使持仓为0）
                result["positions"] = [p for p in result["positions"] if p.get("symbol") == args.symbol]
            else:
                # 不指定交易对时，只返回持仓不为0的
                result["positions"] = [p for p in result["positions"] if float(p.get("positionAmt", 0)) != 0]

        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
