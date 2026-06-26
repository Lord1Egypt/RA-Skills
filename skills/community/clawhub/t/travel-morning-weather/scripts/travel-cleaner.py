#!/usr/bin/env python3
"""
travel-cleaner.py — 过期行程自动清理

清理 memory/travel-plan.json 中日期早于今天的记录。
与晨报 cron 结合，每天自动运行。

用法：
    python3 travel-cleaner.py [--dry-run] [--verbose]
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta

DATA_PATH = os.path.expanduser("~/.openclaw/workspace/memory/travel-plan.json")


def main():
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv

    if not os.path.exists(DATA_PATH):
        if verbose:
            print(f"⚠️  文件不存在: {DATA_PATH}")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    today = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    daily = data.get("daily_locations", {})
    original_count = len(daily)
    cleaned = {
        date: loc for date, loc in daily.items() if date >= today
    }
    removed_count = original_count - len(cleaned)

    if removed_count == 0:
        if verbose:
            print(f"✅ 无过期记录（今天: {today}，共 {original_count} 条）")
        return

    data["daily_locations"] = cleaned

    if not dry_run:
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        if verbose:
            print(f"🧹 清理了 {removed_count} 条过期记录（今天: {today}）")
    else:
        print(f"[dry-run] 将清理 {removed_count} 条过期记录（今天: {today}）")


if __name__ == "__main__":
    main()
