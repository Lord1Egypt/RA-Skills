#!/usr/bin/env python3
"""
record_step.py — 录制单个测试执行步骤
将每步操作记录到 session JSON 文件中，供后续生成脚本和报告使用。

用法:
    python record_step.py \
        --session <session_file.json> \
        --step-num <步骤编号> \
        --description "操作描述" \
        --command "agent-browser 执行的命令" \
        --screenshot <截图路径(可选)> \
        --status <passed|failed|skipped> \
        [--selector "CSS或XPath选择器"] \
        [--input-value "输入的值"] \
        [--url "当前URL"]
"""

import argparse
import json
import os
import sys
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="录制测试步骤到 session 文件")
    parser.add_argument("--session",      required=True,  help="session JSON 文件路径")
    parser.add_argument("--step-num",     required=True,  type=int, help="步骤编号（从1开始）")
    parser.add_argument("--description",  required=True,  help="步骤描述")
    parser.add_argument("--command",      required=True,  help="执行的 agent-browser 命令")
    parser.add_argument("--screenshot",   default="",     help="截图文件路径")
    parser.add_argument("--status",       default="passed", choices=["passed", "failed", "skipped"],
                        help="步骤执行状态")
    parser.add_argument("--selector",     default="",     help="目标元素选择器")
    parser.add_argument("--input-value",  default="",     help="输入的值（如有）")
    parser.add_argument("--url",          default="",     help="执行时的页面 URL")
    parser.add_argument("--error-msg",    default="",     help="失败时的错误信息")
    return parser.parse_args()


def load_session(path: str) -> dict:
    """加载或初始化 session 数据。"""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "created_at": datetime.now().isoformat(),
        "steps": []
    }


def save_session(path: str, data: dict):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    args = parse_args()

    session = load_session(args.session)

    step = {
        "step_num":    args.step_num,
        "description": args.description,
        "command":     args.command,
        "status":      args.status,
        "selector":    args.selector,
        "input_value": args.input_value,
        "url":         args.url,
        "screenshot":  args.screenshot,
        "error_msg":   args.error_msg,
        "timestamp":   datetime.now().isoformat()
    }

    # 如果已有同编号步骤则覆盖，否则追加
    existing_indices = [i for i, s in enumerate(session["steps"]) if s["step_num"] == args.step_num]
    if existing_indices:
        session["steps"][existing_indices[0]] = step
    else:
        session["steps"].append(step)

    # 按步骤编号排序
    session["steps"].sort(key=lambda s: s["step_num"])
    session["updated_at"] = datetime.now().isoformat()

    save_session(args.session, session)
    print(f"✅ Step {args.step_num} recorded → {args.session}")


if __name__ == "__main__":
    main()
