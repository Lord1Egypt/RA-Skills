#!/usr/bin/env python3
"""查询成交记录。需认证。"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Get order fills")
    parser.add_argument("--page", type=int, default=None, help="Page number")
    parser.add_argument("--page-size", type=int, default=None, help="Page size")
    parser.add_argument("--master-order-id", type=str, default=None, help="Master order ID")
    parser.add_argument("--sub-order-id", type=str, default=None, help="Sub order ID")
    parser.add_argument("--order-id", type=str, default=None, help="Order ID (exchange order ID)")
    parser.add_argument("--symbol", type=str, default=None, help="Trading pair symbol")
    parser.add_argument("--status", type=str, default=None, help="PLACED,FILLED,CANCELLED,REJECTED etc, comma-separated")
    parser.add_argument("--start-time", type=str, default=None, help="Start time ISO8601")
    parser.add_argument("--end-time", type=str, default=None, help="End time ISO8601")
    args = parser.parse_args()
    try:
        from _client import get_client
        client = get_client()
        params = {}
        if args.page is not None:
            params["page"] = args.page
        if args.page_size is not None:
            params["pageSize"] = args.page_size
        if args.master_order_id is not None:
            params["masterOrderId"] = args.master_order_id
        if args.sub_order_id is not None:
            params["subOrderId"] = args.sub_order_id
        if args.order_id is not None:
            params["orderId"] = args.order_id
        if args.symbol is not None:
            params["symbol"] = args.symbol
        if args.status is not None:
            params["status"] = args.status
        if args.start_time is not None:
            params["startTime"] = args.start_time
        if args.end_time is not None:
            params["endTime"] = args.end_time
        result = client.get_order_fills(**params)
        print(json.dumps(result, ensure_ascii=False, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
