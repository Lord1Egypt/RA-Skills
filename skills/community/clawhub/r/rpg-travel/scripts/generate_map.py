#!/usr/bin/env python3
"""RPG Travel — 冒险地图生成器（主入口）"""

import json
import sys
import argparse
from pathlib import Path

import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import TripData, OUTPUT_DIR
from html_generator import generate_html
from text_generator import generate_text_taskbook


def main():
    parser = argparse.ArgumentParser(description="RPG Travel 冒险地图生成器")
    parser.add_argument("--data", type=str, help="JSON 数据文件路径")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读取 JSON")
    parser.add_argument("--text-only", action="store_true", help="只生成文本任务书")
    parser.add_argument("--html-only", action="store_true", help="只生成 HTML 冒险地图")
    parser.add_argument(
        "--output-dir", type=str, default=None, help="输出目录（默认当前目录）"
    )
    args = parser.parse_args()

    if args.data:
        with open(args.data, "r", encoding="utf-8") as f:
            raw = json.load(f)
    elif args.stdin:
        raw = json.load(sys.stdin)
    else:
        print("错误：需要 --data 或 --stdin 参数", file=sys.stderr)
        sys.exit(1)

    data = TripData(raw)

    errors = data.validate()
    if errors:
        print("数据校验失败：", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    out_dir = Path(args.output_dir) if args.output_dir else OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    if not args.html_only:
        taskbook = generate_text_taskbook(data)
        taskbook_file = (
            out_dir / f"{data.game_name}-任务书-{data.date_range or '待定'}.txt"
        )
        taskbook_file.write_text(taskbook, encoding="utf-8")
        print(f"✅ 任务书已生成：{taskbook_file}")

    if not args.text_only:
        html = generate_html(data)
        html_file = (
            out_dir / f"{data.game_name}-冒险地图-{data.date_range or '待定'}.html"
        )
        html_file.write_text(html, encoding="utf-8")
        print(f"✅ 冒险地图已生成：{html_file}")

    print("🎉 生成完成！")


if __name__ == "__main__":
    main()
