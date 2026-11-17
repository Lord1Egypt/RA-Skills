#!/usr/bin/env python3
"""
租车网点查询 CLI

用法:
  python scripts/car_stores.py 乌鲁木齐                    # 双平台查询
  python scripts/car_stores.py 乌鲁木齐 --source zuche     # 仅神州
  python scripts/car_stores.py 乌鲁木齐 --source ehi       # 仅一嗨
  python scripts/car_stores.py 乌鲁木齐 --json              # JSON 输出
"""

from __future__ import annotations

import argparse
import json
import sys

# 确保项目根目录在 sys.path 中
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vendor.car_rental import get_stores, StoreInfo


def format_markdown(result: dict) -> str:
    """格式化为 Markdown 表格输出"""
    lines = []

    source_labels = {"zuche": "神州租车", "ehi": "一嗨租车"}

    for src in ["zuche", "ehi"]:
        if src not in result:
            continue

        stores = result[src]
        label = source_labels.get(src, src)
        error_key = f"{src}_error"

        if not stores and error_key in result:
            lines.append(f"## {label}\n\n⚠️ 查询失败: {result[error_key]}\n")
            continue

        lines.append(f"## {label}（{len(stores)} 个网点）\n")

        if src == "zuche":
            lines.append("| # | 网点 | 区域 | 地址 | 电话 | 营业时间 | 自助 | 机场 | 高铁 |")
            lines.append("|---|------|------|------|------|---------|------|------|------|")
            for i, s in enumerate(stores, 1):
                lines.append(
                    f"| {i} | {s.name} | {s.district or '-'} | {s.address} | "
                    f"{s.phone or '-'} | {s.work_time or '-'} | "
                    f"{'✓' if s.is_self_service else '-'} | "
                    f"{'✓' if s.is_airport else '-'} | "
                    f"{'✓' if s.is_train_station else '-'} |"
                )
        else:
            lines.append("| # | 网点 | 地址 | 电话 | 营业时间 | 机场 | 高铁 |")
            lines.append("|---|------|------|------|---------|------|------|")
            for i, s in enumerate(stores, 1):
                lines.append(
                    f"| {i} | {s.name} | {s.address} | "
                    f"{s.phone or '-'} | {s.work_time or '-'} | "
                    f"{'✓' if s.is_airport else '-'} | "
                    f"{'✓' if s.is_train_station else '-'} |"
                )

        lines.append("")

    return "\n".join(lines)


def format_json(result: dict) -> str:
    """格式化为 JSON 输出"""
    output = {}
    for key, value in result.items():
        if isinstance(value, list):
            output[key] = [s.to_dict() if isinstance(s, StoreInfo) else s for s in value]
        else:
            output[key] = value
    return json.dumps(output, ensure_ascii=False, indent=2)


def _available_cities_hint() -> str:
    """城市查不到时，给出神州租车的可用城市列表（网络失败则跳过）"""
    try:
        from vendor.car_rental.zuche import _get_city_list
        return "可用城市: " + "、".join(sorted(_get_city_list()))
    except Exception:
        return ""


def main():
    parser = argparse.ArgumentParser(description="租车网点查询")
    parser.add_argument("city", help="城市名（中文，如 乌鲁木齐）")
    parser.add_argument(
        "--source",
        choices=["zuche", "ehi"],
        default=None,
        help="指定平台（默认双平台查询）",
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    result = get_stores(args.city, source=args.source)

    # get_stores 不抛异常，单平台失败降级为 "{src}_error"；全部失败才退出
    errors = [(k, v) for k, v in result.items() if isinstance(v, str)]
    queried = [args.source] if args.source else ["zuche", "ehi"]
    if errors and all(not result.get(src) for src in queried):
        for k, msg in errors:
            print(f"❌ {k.removesuffix('_error')}: {msg}", file=sys.stderr)
        hint = _available_cities_hint()
        if hint:
            print(hint, file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(format_json(result))
    else:
        print(format_markdown(result))


if __name__ == "__main__":
    main()
