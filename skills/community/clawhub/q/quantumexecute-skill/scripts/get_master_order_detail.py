#!/usr/bin/env python3
"""获取指定母单详情。需认证。"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Get master order detail by masterOrderId")
    parser.add_argument("--master-order-id", type=str, required=True, help="Master order ID")
    args = parser.parse_args()
    try:
        from _client import get_client
        client = get_client()
        result = client.get_master_order_detail(masterOrderId=args.master_order_id)
        print(json.dumps(result, ensure_ascii=False, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
