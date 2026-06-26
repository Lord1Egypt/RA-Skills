#!/usr/bin/env python3
"""导出子单成交记录到Excel。需认证。"""
import argparse
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Export order fills to Excel")
    parser.add_argument("--page", type=int, default=None, help="Page number")
    parser.add_argument("--page-size", type=int, default=None, help="Page size")
    parser.add_argument("--master-order-id", type=str, default=None, help="Master order ID")
    parser.add_argument("--sub-order-id", type=str, default=None, help="Sub order ID")
    parser.add_argument("--order-id", type=str, default=None, help="Order ID (exchange order ID)")
    parser.add_argument("--symbol", type=str, default=None, help="Trading pair symbol")
    parser.add_argument("--status", type=str, default=None, help="PLACED,FILLED,CANCELLED,REJECTED etc")
    parser.add_argument("--start-time", type=str, default=None, help="Start time ISO8601")
    parser.add_argument("--end-time", type=str, default=None, help="End time ISO8601")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    args = parser.parse_args()

    try:
        from _client import get_client
        import pandas as pd

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
        items = result.get("items", [])

        if not items:
            print(json.dumps({"success": False, "error": "No data found"}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        df = pd.DataFrame(items)

        workspace = Path.home() / "workspace"
        workspace.mkdir(exist_ok=True)

        if args.output:
            output_path = Path(args.output)
        else:
            # 使用当前时间作为文件名
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = workspace / f"order_fills_{timestamp}.xlsx"

        df.to_excel(output_path, index=False, engine='openpyxl')

        print(json.dumps({
            "success": True,
            "file_path": str(output_path),
            "total_records": len(items)
        }, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
