#!/usr/bin/env python3
"""Prompt 质量检查工具。"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import List

STYLE_KEYWORDS = {
    "photorealistic", "realistic", "anime", "illustration", "cinematic",
    "vintage", "retro", "showa", "cyberpunk", "concept art", "watercolor",
    "oil painting", "ghibli", "comic", "digital painting", "film grain",
}

QUALITY_KEYWORDS = {
    "masterpiece", "best quality", "high detail", "ultra detailed",
    "8k", "sharp focus", "highly detailed",
}

COMMON_SUBJECT_HINTS = {
    "girl", "boy", "woman", "man", "cat", "dog", "robot", "city",
    "street", "building", "car", "portrait", "character", "person",
    "landscape", "forest", "mountain", "flower", "temple", "warrior",
}

CONTRADICTIONS = [
    ("realistic", "anime"),
    ("photorealistic", "illustration"),
    ("vintage", "modern"),
]

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
WEIGHT_RE = re.compile(r"\(([^()]+?):\s*([0-9]+(?:\.[0-9]+)?)\)")


def word_count(text: str) -> int:
    return len(WORD_RE.findall(text))


def has_subject(text: str) -> bool:
    lower = text.lower()
    tokens = set(WORD_RE.findall(lower))
    if any(t in tokens for t in COMMON_SUBJECT_HINTS):
        return True
    # 宽松回退：出现 a/an/the + 单词，视作有主体描述
    return bool(re.search(r"\b(a|an|the)\s+[a-z][a-z0-9_-]{2,}\b", lower))


def has_style(text: str) -> bool:
    lower = text.lower()
    return any(k in lower for k in STYLE_KEYWORDS)


def has_quality(text: str) -> bool:
    lower = text.lower()
    return any(k in lower for k in QUALITY_KEYWORDS)


def check_parentheses_balance(text: str) -> bool:
    depth = 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def check_weight_format(text: str) -> List[str]:
    issues: List[str] = []
    if not check_parentheses_balance(text):
        issues.append("括号不匹配")
        return issues

    # 检测疑似加权但格式错误的片段
    suspect = re.findall(r"\([^()]*:[^()]*\)", text)
    for s in suspect:
        if not WEIGHT_RE.fullmatch(s):
            issues.append(f"权重格式可能错误: {s}")

    # 检测权重范围
    for m in WEIGHT_RE.finditer(text):
        value = float(m.group(2))
        if value <= 0 or value > 2.0:
            issues.append(f"权重值超出建议范围(0,2]: {m.group(0)}")

    return issues


def check_contradictions(text: str) -> List[str]:
    lower = text.lower()
    issues: List[str] = []
    for a, b in CONTRADICTIONS:
        if a in lower and b in lower:
            issues.append(f"存在潜在风格冲突: {a} vs {b}")
    return issues


def run_check(prompt: str) -> dict:
    issues: List[str] = []
    warnings: List[str] = []

    wc = word_count(prompt)
    if wc < 50:
        issues.append(f"长度过短: {wc} 词（建议 50-300 词）")
    elif wc > 300:
        issues.append(f"长度过长: {wc} 词（建议 50-300 词）")

    if not has_subject(prompt):
        issues.append("缺少明确主体描述（subject）")

    if not has_style(prompt):
        issues.append("缺少风格关键词（style）")

    if not has_quality(prompt):
        warnings.append("缺少常见质量词（如 masterpiece / best quality / high detail）")

    issues.extend(check_weight_format(prompt))
    issues.extend(check_contradictions(prompt))

    status = "PASS" if not issues else "WARN"
    return {
        "status": status,
        "word_count": wc,
        "issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Prompt 质量检查工具")
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="检查 prompt 文本")
    p_check.add_argument("prompt", help="待检查的 prompt 文本")

    args = parser.parse_args()

    if args.command == "check":
        result = run_check(args.prompt)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "PASS" else 1

    print(json.dumps({"status": "WARN", "issues": ["未知命令"]}, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    sys.exit(main())
