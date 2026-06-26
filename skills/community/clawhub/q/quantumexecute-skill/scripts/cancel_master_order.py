#!/usr/bin/env python3
"""取消指定主订单。需认证。"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Cancel master order")
    parser.add_argument("--master-order-id", type=str, required=True, help="Master order ID to cancel")
    parser.add_argument("--reason", type=str, default=None, help="Cancel reason (optional)")
    args = parser.parse_args()
    try:
        from _client import get_client
        client = get_client()
        params = {"masterOrderId": args.master_order_id}
        if args.reason is not None:
            params["reason"] = args.reason
        result = client.cancel_master_order(**params)
        print(json.dumps(result, ensure_ascii=False, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
