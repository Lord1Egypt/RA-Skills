#!/usr/bin/env python3
"""Generate a regression-evaluation tracking file from test-prompts.json."""

import argparse
import datetime
import json
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", required=True)
    parser.add_argument("--out", required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    data = json.loads(Path(args.prompts).read_text(encoding="utf-8"))
    cases = data.get("test_cases", [])
    today = datetime.date.today().isoformat()
    lines = [
        f"# 回归测试记录 - {today}",
        "",
        "本文件用于记录同一批 test-prompts 的真实执行结果。每次模型、协议或技能包变化后，重新跑一遍并填写状态。",
        "",
        "| ID | 类型 | 状态 | 提示词摘要 | 期望行为摘要 | 实际结果/备注 |",
        "|---|---|---|---|---|---|",
    ]
    for case in cases:
        pid = case.get("id", "")
        ctype = case.get("type", "")
        prompt = case.get("prompt", "").replace("|", "/")[:60]
        expected = case.get("expected_behavior", "").replace("|", "/")[:60]
        lines.append(f"| {pid} | {ctype} | 待测 | {prompt} | {expected} | |")
    lines.append("")
    text = "\n".join(lines)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print("OUTPUT", out)
    print("CASES", len(cases))


if __name__ == "__main__":
    main()
