#!/usr/bin/env python3
"""导出TCA分析数据到Excel。需认证。"""
import argparse
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Export TCA analysis to Excel")
    parser.add_argument("--symbol", type=str, default=None, help="Trading pair symbol")
    parser.add_argument("--category", type=str, default=None, help="spot, perp, or perp_cm")
    parser.add_argument("--apikey", type=str, default=None, help="ApiKey id list, comma-separated")
    parser.add_argument("--start-time", type=int, default=None, help="Start timestamp in milliseconds")
    parser.add_argument("--end-time", type=int, default=None, help="End timestamp in milliseconds")
    parser.add_argument("--output", type=str, default=None, help="Output file path")
    args = parser.parse_args()

    try:
        from _client import get_client
        import pandas as pd

        client = get_client()
        params = {}
        if args.symbol is not None:
            params["symbol"] = args.symbol
        if args.category is not None:
            params["category"] = args.category
        if args.apikey is not None:
            params["apikey"] = args.apikey
        if args.start_time is not None:
            params["startTime"] = args.start_time
        if args.end_time is not None:
            params["endTime"] = args.end_time

        items = client.get_tca_analysis(**params)

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
            output_path = workspace / f"tca_analysis_{timestamp}.xlsx"

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
