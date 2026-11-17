#!/usr/bin/env python3
"""Validate test-prompts.json and print a capability coverage summary."""

import argparse
import datetime
import json
from collections import Counter
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompts", required=True)
    parser.add_argument("--output", required=False)
    args = parser.parse_args()

    data = json.loads(Path(args.prompts).read_text(encoding="utf-8"))
    cases = data.get("test_cases", [])
    types = Counter(case.get("type", "unknown") for case in cases)
    notes = Counter(case.get("notes", "unknown") for case in cases)

    lines = [
        f"# 能力覆盖矩阵（{datetime.date.today().isoformat()}）",
        "",
        f"- test_cases: {len(cases)}",
        "",
        "## 类型分布",
        "",
        "| 类型 | 数量 |",
        "|---|---|",
    ]
    for key, count in sorted(types.items()):
        lines.append(f"| {key} | {count} |")

    lines += ["", "## 触发领域分布", "", "| 领域 | 数量 |", "|---|---|"]
    for key, count in sorted(notes.items(), key=lambda x: -x[1]):
        lines.append(f"| {key} | {count} |")

    report = "\n".join(lines) + "\n"
    print(report)
    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"output: {args.output}")


if __name__ == "__main__":
    main()
