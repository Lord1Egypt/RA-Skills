#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# R-12 审计锚点
import os
DEFAULT_DATA_DIR_RAW = "skills/.standardization/triphasic-execution/data/"
"""
Cron Helper — 经验教训登记册定时更新钩子
========================================
配合 cron/automation 使用，定时检查未解决问题并生成登记册。

用法:
  python cron_helper.py                    # 默认：检查 + 合并
  python cron_helper.py --check-only       # 只检查不合并
  python cron_helper.py --auto-update      # 检查 + 合并（带提醒）
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# ============================================================================
# 路径配置
# ============================================================================
_SKILL_DIR = Path(__file__).resolve().parent.parent

def _find_standardization_dir() -> Path:
    p = _SKILL_DIR.resolve()
    for parent in [p] + list(p.parents):
        if parent.name == "skills" and parent.parent.name != "skills":
            return parent / ".standardization" / _SKILL_DIR.name
    return _SKILL_DIR.parent / ".standardization" / _SKILL_DIR.name

_DEFAULT_HOME = _find_standardization_dir()
_TRIPHASIC_HOME = Path(os.environ.get("TRIPHASIC_HOME", str(_DEFAULT_HOME)))


def get_home() -> Path:
    home = _TRIPHASIC_HOME
    home.mkdir(parents=True, exist_ok=True)
    return home


def get_logger_script() -> Path:
    return Path(__file__).parent / "problem_logger.py"


# ============================================================================
# 命令实现
# ============================================================================
def check_unresolved() -> list[tuple[str, str]]:
    """检查未解决的问题"""
    logger = get_logger_script()
    result = subprocess.run(
        [sys.executable, str(logger), "--home", str(get_home()), "list", "--recent", "100"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"❌ 获取问题列表失败：{result.stderr}")
        return []

    unresolved = []
    for line in result.stdout.split("\n"):
        if "❌" in line:
            parts = line.strip().split("|")
            if len(parts) >= 2:
                num = parts[0].strip()
                scene = parts[1].strip()
                unresolved.append((num, scene))

    return unresolved


def merge_to_lessons() -> int:
    """合并到经验教训登记册"""
    logger = get_logger_script()
    print("🔨 生成经验教训登记册...")
    result = subprocess.run(
        [sys.executable, str(logger), "--home", str(get_home()), "merge-to-lessons"],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("✅ 登记册生成完成")
        return 0
    else:
        print(f"❌ 生成失败：{result.stderr}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Cron Helper — 经验教训登记册定时更新钩子",
    )
    parser.add_argument("--home", type=str, default=None, help="覆盖 TRIPHASIC_HOME")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check-only", action="store_true", help="只检查不合并")
    group.add_argument("--auto-update", action="store_true", help="检查 + 合并（带提醒）")

    args = parser.parse_args()

    if args.home:
        global _TRIPHASIC_HOME
        _TRIPHASIC_HOME = Path(args.home).expanduser().resolve()

    if args.check_only:
        unresolved = check_unresolved()
        if unresolved:
            print(f"⚠️  发现 {len(unresolved)} 个未解决问题")
            return 1
        else:
            print("✅ 所有问题均已解决")
            return 0
    elif args.auto_update:
        unresolved = check_unresolved()
        if unresolved:
            print(f"⚠️  发现 {len(unresolved)} 个未解决问题（需人工补充原因/解决方案）")
        merge_to_lessons()
        return 0
    else:
        print("🔍 [Step 1/2] 检查未解决的问题...")
        unresolved = check_unresolved()
        if unresolved:
            print(f"⚠️  发现 {len(unresolved)} 个未解决问题（跳过自动补充，需人工介入）\n")
        else:
            print("✅ 所有问题均已解决\n")

        print("🔨 [Step 2/2] 生成经验教训登记册...")
        return merge_to_lessons()


if __name__ == "__main__":
    sys.exit(main())
