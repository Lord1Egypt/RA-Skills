#!/usr/bin/env python3
"""A股分析报告生成器 — 统一入口

用法:
  python3 scripts/report.py stock 600519           # 个股分析 + 生成报告
  python3 scripts/report.py market                  # 市场分析 + 生成报告
  python3 scripts/report.py stock 600519 --json     # 同时输出 JSON
  python3 scripts/report.py stock 600519 -o ./out   # 自定义输出目录
"""
import argparse
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.index import analyze_stock, analyze_market, _dataclass_to_dict


def main():
    parser = argparse.ArgumentParser(
        prog="report",
        description="A股分析报告生成器",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    stock_parser = sub.add_parser("stock", help="个股分析报告")
    stock_parser.add_argument("code", help="股票代码，如 600519")
    stock_parser.add_argument("-o", "--output-dir", default=None, help="报告输出目录 (默认: reports/)")
    stock_parser.add_argument("--json", action="store_true", help="同时输出 JSON 到控制台")

    market_parser = sub.add_parser("market", help="市场分析报告")
    market_parser.add_argument("-o", "--output-dir", default=None, help="报告输出目录 (默认: reports/)")
    market_parser.add_argument("--json", action="store_true", help="同时输出 JSON 到控制台")

    args = parser.parse_args()

    if args.command == "stock":
        result = asyncio.run(analyze_stock(args.code, save=True, output_dir=args.output_dir))
    else:
        result = asyncio.run(analyze_market(save=True, output_dir=args.output_dir))

    if args.json:
        print(json.dumps(_dataclass_to_dict(result), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
