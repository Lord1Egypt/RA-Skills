#!/usr/bin/env python3
"""
update-travel-plan.py — 行程数据更新

添加或更新 memory/travel-plan.json 中的行程记录。
支持日期范围展开为逐日记录。

用法：
    python3 update-travel-plan.py --start 2026-05-10 --end 2026-05-12 --location "Paris, France"
    python3 update-travel-plan.py --date 2026-05-15 --location "Lyon, France"
    python3 update-travel-plan.py --remove 2026-05-10
    python3 update-travel-plan.py --set-default "Your City, Country"
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta

DATA_PATH = os.path.expanduser("~/.openclaw/workspace/memory/travel-plan.json")


def ensure_data_exists():
    """确保 travel-plan.json 存在，不存在则创建默认文件。"""
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    data = {"default_location": "Your City, Country", "daily_locations": {}}
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data


def save_data(data):
    """保存数据到 travel-plan.json。"""
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def date_range(start, end):
    """生成日期范围内的所有日期（含起止日期）。"""
    current = start
    while current <= end:
        yield current.strftime("%Y-%m-%d")
        current += timedelta(days=1)


def main():
    parser = argparse.ArgumentParser(description="更新行程数据")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--start",
        help="行程开始日期 (YYYY-MM-DD)",
    )
    group.add_argument(
        "--date",
        help="单个日期 (YYYY-MM-DD)",
    )
    group.add_argument(
        "--remove",
        help="删除指定日期 (YYYY-MM-DD) 或日期范围 (YYYY-MM-DD:YYYY-MM-DD)",
    )
    group.add_argument(
        "--set-default",
        help="设置默认地点",
    )

    parser.add_argument("--end", help="行程结束日期 (YYYY-MM-DD)")
    parser.add_argument("--location", help="地点 (City, Country)")

    args = parser.parse_args()

    data = ensure_data_exists()

    # 设置默认地点
    if args.set_default:
        old = data.get("default_location", "")
        data["default_location"] = args.set_default
        save_data(data)
        print(f"✅ 默认地点: {old} → {args.set_default}")
        return

    # 删除日期
    if args.remove:
        if ":" in args.remove:
            start_str, end_str = args.remove.split(":", 1)
            dates = list(
                date_range(
                    datetime.strptime(start_str, "%Y-%m-%d"),
                    datetime.strptime(end_str, "%Y-%m-%d"),
                )
            )
        else:
            dates = [args.remove]
        removed = []
        for d in dates:
            if d in data["daily_locations"]:
                del data["daily_locations"][d]
                removed.append(d)
        save_data(data)
        if removed:
            print(f"🗑️  已删除: {', '.join(removed)}")
        else:
            print(f"ℹ️  无匹配日期可删除")
        return

    # 添加/更新行程
    if not args.location:
        print("❌ --location 参数必填")
        sys.exit(1)

    if args.date:
        dates = [args.date]
    elif args.start:
        end_date = (
            datetime.strptime(args.end, "%Y-%m-%d")
            if args.end
            else datetime.strptime(args.start, "%Y-%m-%d")
        )
        dates = list(
            date_range(datetime.strptime(args.start, "%Y-%m-%d"), end_date)
        )
    else:
        print("❌ 必须指定 --date 或 --start")
        sys.exit(1)

    for d in dates:
        data["daily_locations"][d] = args.location

    save_data(data)
    print(f"✅ 已记录: {len(dates)} 天 → {args.location}")
    if len(dates) <= 5:
        print(f"   日期: {', '.join(dates)}")
    else:
        print(f"   日期: {dates[0]} 至 {dates[-1]}")


if __name__ == "__main__":
    main()
