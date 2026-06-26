#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.index import analyze_stock, _dataclass_to_dict


def main():
    parser = argparse.ArgumentParser(description="A股个股分析")
    parser.add_argument("code", nargs="?", default="600519", help="股票代码 (默认: 600519)")
    parser.add_argument("--save", action="store_true", help="保存 Markdown 报告到 reports/ 目录")
    parser.add_argument("--output-dir", default=None, help="自定义报告输出目录")
    args = parser.parse_args()

    result = asyncio.run(analyze_stock(args.code, save=args.save, output_dir=args.output_dir))
    print(json.dumps(_dataclass_to_dict(result), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
