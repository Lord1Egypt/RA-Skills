#!/usr/bin/env python3
"""
OpenClaw / 通用 AI Skill 入口脚本。

提供统一入口，便于 AI skill 框架通过单个命令调用：
- config: 配置 V2EX API Key 与监控节点
- run: 执行一次监控并生成报告
- report: 输出最近一次生成的 Markdown 报告
"""

import argparse
import sys
from pathlib import Path

import v2ex_monitor


BASE_DIR = Path(__file__).resolve().parent
REPORT_FILE = BASE_DIR / "v2ex_hourly_report.md"


def cmd_config(args):
    class ConfigArgs:
        nodes = args.nodes
        apikey = args.apikey

    v2ex_monitor.cmd_config(ConfigArgs)


def cmd_run(args):
    v2ex_monitor.run_monitor()


def cmd_report(args):
    if not REPORT_FILE.exists():
        print("尚未生成报告，请先执行 run 子命令。")
        sys.exit(1)

    print(REPORT_FILE.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="V2EX Monitor Skill 统一入口")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    config_parser = subparsers.add_parser("config", help="配置 API Key 和监控节点")
    config_parser.add_argument("--nodes", help="监控节点，用逗号分隔，例如 python,linux,programmer")
    config_parser.add_argument("--apikey", help="V2EX API Key")
    config_parser.set_defaults(func=cmd_config)

    run_parser = subparsers.add_parser("run", help="运行一次监控并生成报告")
    run_parser.set_defaults(func=cmd_run)

    report_parser = subparsers.add_parser("report", help="输出最近一次生成的报告")
    report_parser.set_defaults(func=cmd_report)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        return

    try:
        args.func(args)
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()