#!/usr/bin/env python3
"""查询TCA分析数据。需认证。"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Get TCA analysis data")
    parser.add_argument("--symbol", type=str, default=None, help="Trading pair symbol")
    parser.add_argument("--category", type=str, default=None, help="spot, perp, or perp_cm")
    parser.add_argument("--apikey", type=str, default=None, help="ApiKey id list, comma-separated")
    parser.add_argument("--start-time", type=int, default=None, help="Start timestamp in milliseconds")
    parser.add_argument("--end-time", type=int, default=None, help="End timestamp in milliseconds")
    args = parser.parse_args()
    try:
        from _client import get_client
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
        result = client.get_tca_analysis(**params)
        print(json.dumps(result, ensure_ascii=False, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
