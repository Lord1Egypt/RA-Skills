#!/usr/bin/env python3
"""Detect user feedback signals from plain text.

Usage:
    python scripts/detect_feedback_signal.py --text "你又忘了同步更新设计稿"

Output:
    A JSON object with `matched`, `matched_keywords`, and `additional_context`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys


PATTERNS = [
    r"不是这样",
    r"别这样做",
    r"你搞错",
    r"搞错了",
    r"你错了",
    r"不对",
    r"不应该",
    r"你漏了",
    r"你忘了",
    r"你又忘",
    r"改一下",
    r"不合理",
    r"理解错",
    r"我说的不是",
    r"为什么没",
    r"没有执行",
    r"没有生效",
    r"每次都",
    r"我不是让你",
    r"不要再",
    r"别再",
    r"停下",
    r"先不要",
    r"that(?:'s| is) not (?:right|what i asked)",
    r"not like this",
    r"don't do it this way",
    r"you forgot again",
    r"you forgot",
    r"this is wrong",
    r"that's wrong",
    r"you are wrong",
    r"you missed",
    r"why (?:didn't|did not) you",
    r"this isn't what i meant",
    r"i didn't ask you to do that",
    r"stop doing this",
    r"don't do that again",
]


def detect(text: str) -> dict[str, object]:
    matched = []
    for pattern in PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            matched.append(pattern)

    payload = {
        "matched": bool(matched),
        "matched_keywords": matched,
        "additional_context": "",
    }

    if matched:
        payload["additional_context"] = (
            "检测到用户修正/反馈信号 / Detected corrective feedback. "
            "请在处理完当前请求后派发 feedback-observer，"
            "记录 feedback 到 .claude/feedback/ 目录。"
        )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect feedback signals.")
    parser.add_argument("--text", required=True, help="User message text")
    args = parser.parse_args()

    result = detect(args.text.strip())
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
