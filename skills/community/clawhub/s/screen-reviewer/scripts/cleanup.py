#!/usr/bin/env python3
"""
自动清理模块 — 删除 N 天前的原始截图目录
日志和报告永久保留。
"""

import os
import sys
import shutil
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import load_config, DATA_DIR


def cleanup_old_screenshots(keep_days: int = None):
    """
    删除 keep_days 天前的截图文件夹。
    截图按日期存放在 screenshots/YYYY-MM-DD/ 下。
    """
    config = load_config()
    if keep_days is None:
        keep_days = config["cleanup"]["keep_days"]

    screenshots_dir = os.path.join(DATA_DIR, "screenshots")
    if not os.path.isdir(screenshots_dir):
        return

    cutoff = (datetime.now() - timedelta(days=keep_days)).strftime("%Y-%m-%d")
    removed = 0

    for name in os.listdir(screenshots_dir):
        full_path = os.path.join(screenshots_dir, name)
        if not os.path.isdir(full_path):
            continue
        # 文件夹名就是日期 YYYY-MM-DD
        if name < cutoff:
            shutil.rmtree(full_path, ignore_errors=True)
            removed += 1
            print(f"[cleanup] 已删除: {name}/")

    if removed:
        print(f"[cleanup] 共清理 {removed} 个过期截图目录")
    else:
        print(f"[cleanup] 无需清理（保留最近 {keep_days} 天）")


if __name__ == "__main__":
    days = int(sys.argv[1]) if len(sys.argv) > 1 else None
    cleanup_old_screenshots(days)
