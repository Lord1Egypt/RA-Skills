#!/usr/bin/env python3
"""解析 .dev/plan.md 中的 todo list，输出进度

Usage:
  python3 progress.py [plan_path]
  python3 progress.py .dev/plan.md
"""

import argparse
import re
import sys
from pathlib import Path


def parse_progress(plan_path: str = ".dev/plan.md"):
    path = Path(plan_path)
    if not path.exists():
        print(f"❌ 文件不存在: {path}")
        sys.exit(1)

    content = path.read_text()
    lines = content.split("\n")

    total = 0
    done = 0
    current_phase = ""
    phases = {}

    for line in lines:
        # 检测阶段标题
        phase_match = re.match(r"^###\s+(.+)", line)
        if phase_match:
            current_phase = phase_match.group(1).strip()
            if current_phase not in phases:
                phases[current_phase] = {"total": 0, "done": 0}

        # 检测 checkbox
        todo_match = re.match(r"^\s*-\s*\[([ xX])\]\s*(.+)", line)
        if todo_match:
            total += 1
            is_done = todo_match.group(1).lower() == "x"
            if is_done:
                done += 1
            if current_phase:
                phases[current_phase]["total"] += 1
                if is_done:
                    phases[current_phase]["done"] += 1

    if total == 0:
        print("📋 plan.md 中没有找到任务清单")
        return

    pct = (done / total) * 100

    # 进度条
    bar_len = 30
    filled = int(bar_len * done / total)
    bar = "█" * filled + "░" * (bar_len - filled)

    print(f"\n📊 实施进度: {done}/{total} ({pct:.0f}%)")
    print(f"   [{bar}]")

    if phases:
        print(f"\n{'阶段':<25} {'进度':>10}")
        print("-" * 38)
        for phase, stats in phases.items():
            p_pct = (stats["done"] / stats["total"] * 100) if stats["total"] > 0 else 0
            status = "✅" if stats["done"] == stats["total"] else "🔧"
            print(f"   {status} {phase:<22} {stats['done']}/{stats['total']} ({p_pct:.0f}%)")

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="解析 plan.md 进度")
    parser.add_argument("plan_path", nargs="?", default=".dev/plan.md", help="plan.md 文件路径")
    args = parser.parse_args()
    parse_progress(args.plan_path)
