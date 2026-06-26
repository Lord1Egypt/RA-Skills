#!/usr/bin/env python3
"""
Skill Radar — 扫描、洞察、优化你的 AI 技能生态

子命令:
  usage      使用价值评估（分析各 Skill 实际使用情况）
  status     Missing/Ready 状态检查
  versions   版本更新检查
  recommend  基于历史对话的智能推荐
  all        完整报告（以上四项）
"""

import sys
from pathlib import Path

# 确保能导入同目录的模块
sys.path.insert(0, str(Path(__file__).parent))

from usage_analyzer import check_usage
from checks import check_status, check_versions
from report import check_recommend, generate_summary


def print_usage():
    usage = """
📡 Skill Radar

用法: python3 health_check.py <command>

命令:
  usage      使用价值评估（分析各 Skill 实际使用情况）
  status     Missing/Ready 状态检查
  versions   版本更新检查
  recommend  基于历史对话的智能推荐
  all        完整报告（以上四项）

示例:
  python3 health_check.py all
  python3 health_check.py usage > usage.md
"""
    print(usage)


def main():
    if len(sys.argv) < 2:
        cmd = "all"
    else:
        cmd = sys.argv[1].lower().strip()

    commands = {
        "usage": check_usage,
        "status": check_status,
        "versions": check_versions,
        "recommend": check_recommend,
        "all": None,
    }

    if cmd not in commands:
        print_usage()
        sys.exit(1)

    if cmd == "all":
        reports = []
        reports.append(generate_summary())
        reports.append(check_status())
        reports.append("\n\n---\n\n")
        reports.append(check_usage())
        reports.append("\n\n---\n\n")
        reports.append(check_recommend())
        reports.append("\n\n---\n\n")
        reports.append(check_versions())
        print("".join(reports))
    else:
        print(commands[cmd]())


if __name__ == "__main__":
    main()
