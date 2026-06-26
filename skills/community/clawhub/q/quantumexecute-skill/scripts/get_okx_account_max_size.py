#!/usr/bin/env python3
"""获取 OKX 账户最大可下单量"""
import sys
import json
import argparse
from _client import get_client


def main():
    parser = argparse.ArgumentParser(description="获取 OKX 账户最大可下单量")
    parser.add_argument("--binding-id", type=str, required=True, help="交易所 API 的 id（来自 list_exchange_apis）")
    parser.add_argument("--inst-id", type=str, required=True, help="产品 ID，如 BTC-USDT-SWAP")
    parser.add_argument("--td-mode", type=str, required=True, help="交易模式：cross / isolated / cash")
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.get_okx_account_max_size(args.binding_id, args.inst_id, args.td_mode)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
