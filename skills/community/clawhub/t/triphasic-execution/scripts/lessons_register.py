#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# R-12 审计锚点
import os
DEFAULT_DATA_DIR_RAW = "skills/.standardization/triphasic-execution/data/"
"""
Lessons Register — 经验教训登记册汇总与优化
============================================
独立命令触发经验教训登记册生成，支持增量检测和统计。

用法:
  python lessons_register.py generate        # 生成登记册
  python lessons_register.py diff            # 查看与上次生成的差异
  python lessons_register.py stats           # 统计信息
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter

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


def get_problems_jsonl() -> Path:
    return get_home() / ".problem_logs" / "problems.jsonl"


def get_lessons_md() -> Path:
    return get_home() / "LESSONS_REGISTER.md"


def get_logger_script() -> Path:
    """获取 problem_logger.py 路径"""
    return Path(__file__).parent / "problem_logger.py"


# ============================================================================
# 命令实现
# ============================================================================
def cmd_generate(args):
    """生成经验教训登记册"""
    print("=" * 60)
    print("📚 经验教训登记册生成器")
    print("=" * 60)
    print()

    logger = get_logger_script()
    result = subprocess.run(
        [sys.executable, str(logger), "merge-to-lessons", "--home", str(get_home())],
        capture_output=False,
        text=True,
    )

    print()
    if result.returncode == 0:
        print("✅ 登记册生成完成")
        print(f"📍 文件位置：{get_lessons_md()}")
    else:
        print("❌ 生成失败，请检查错误信息")

    return result.returncode


def cmd_diff(args):
    """查看与上次生成的差异（需要 git）"""
    lessons = get_lessons_md()
    if not lessons.exists():
        print("❌ LESSONS_REGISTER.md 不存在，先运行 generate 命令")
        return 1

    result = subprocess.run(
        ["git", "diff", str(lessons)],
        cwd=str(get_home()),
        capture_output=True,
        text=True,
    )

    if result.returncode == 0 and not result.stdout.strip():
        print("✅ 无未提交的更改")
    elif result.stdout.strip():
        print("📊 与上次提交的差异:\n")
        print(result.stdout)
    else:
        print("❌ git diff 执行失败（可能不在 git repo 中）")
        return 1

    return 0


def cmd_stats(args):
    """统计信息"""
    log = get_problems_jsonl()
    if not log.exists():
        print("📭 暂无问题记录")
        return 0

    problems = []
    with open(log, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    problems.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    total = len(problems)
    resolved = len([p for p in problems if p["status"] == "已解决"])
    unresolved = total - resolved
    rate = (resolved / total * 100) if total > 0 else 0

    now = datetime.now()
    recent_7d = len([p for p in problems if _parse_ts(p.get("timestamp", "")) > now - timedelta(days=7)])
    recent_30d = len([p for p in problems if _parse_ts(p.get("timestamp", "")) > now - timedelta(days=30)])

    print("=" * 60)
    print("📊 经验教训统计")
    print("=" * 60)
    print(f"\n总问题数：       {total}")
    print(f"已解决：         {resolved} ({rate:.1f}%)")
    print(f"未解决：         {unresolved}")
    print(f"\n时间分布:")
    print(f"  - 最近 7 天：   {recent_7d} 条")
    print(f"  - 最近 30 天：  {recent_30d} 条")

    scenes = Counter(p.get("scene", "未知") for p in problems)
    top = scenes.most_common(5)
    if top:
        print(f"\nTop 5 问题场景:")
        for i, (scene, count) in enumerate(top, 1):
            print(f"  {i}. {scene}: {count} 次")

    print()
    return 0


def _parse_ts(ts: str) -> datetime:
    """解析时间戳字符串"""
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            continue
    return datetime.min


def main():
    parser = argparse.ArgumentParser(
        description="Lessons Register — 经验教训登记册汇总与优化",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python lessons_register.py generate
  python lessons_register.py diff
  python lessons_register.py stats

环境变量:
  TRIPHASIC_HOME  数据目录（默认 ~/.workbuddy/triphasic/）
        """,
    )

    parser.add_argument("--home", type=str, default=None, help="覆盖 TRIPHASIC_HOME")

    subparsers = parser.add_subparsers(dest="command", help="子命令")
    subparsers.add_parser("generate", help="生成经验教训登记册")
    subparsers.add_parser("diff", help="查看与上次生成的差异")
    subparsers.add_parser("stats", help="统计信息")

    args = parser.parse_args()

    if args.home:
        global _TRIPHASIC_HOME
        _TRIPHASIC_HOME = Path(args.home).expanduser().resolve()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "generate":
        return cmd_generate(args)
    elif args.command == "diff":
        return cmd_diff(args)
    elif args.command == "stats":
        return cmd_stats(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
