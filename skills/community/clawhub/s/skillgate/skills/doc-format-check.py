#!/usr/bin/env python3
"""
doc-format-check — 文档格式检查 skill。
检查 Markdown 文档的格式问题。
"""
import re
import sys
from pathlib import Path


def check_markdown(filepath: str) -> list:
    """检查 Markdown 文档格式。"""
    findings = []

    content = Path(filepath).read_text(encoding="utf-8")
    lines = content.split("\n")

    # 检查 1：标题层级是不是跳级
    prev_level = 0
    for i, line in enumerate(lines, 1):
        match = re.match(r"^(#+)\s", line)
        if match:
            level = len(match.group(1))
            if prev_level > 0 and level > prev_level + 1:
                findings.append({
                    "line": i,
                    "severity": "MEDIUM",
                    "message": f"标题层级跳级：从 H{prev_level} 跳到 H{level}"
                })
            prev_level = level

    # 检查 2：列表格式是不是统一
    has_dash = any(re.match(r"^-\s", line) for line in lines)
    has_star = any(re.match(r"^\*\s", line) for line in lines)
    if has_dash and has_star:
        findings.append({
            "line": 0,
            "severity": "LOW",
            "message": "列表格式不统一——有的用 -，有的用 *"
        })

    # 检查 3：代码块是不是闭合
    code_block_count = sum(1 for line in lines if line.strip().startswith("```"))
    if code_block_count % 2 != 0:
        findings.append({
            "line": 0,
            "severity": "HIGH",
            "message": "代码块没闭合——``` 数量是奇数"
        })

    return findings


def main():
    if len(sys.argv) < 2:
        print("用法: python doc_format_check.py <markdown文件>")
        sys.exit(1)

    filepath = sys.argv[1]
    findings = check_markdown(filepath)

    if not findings:
        print("✅ 文档格式没问题")
        sys.exit(0)

    print(f"发现 {len(findings)} 个问题：")
    for f in findings:
        print(f"  [{f['severity']}] 行 {f['line']}: {f['message']}")

    sys.exit(1 if any(f["severity"] == "HIGH" for f in findings) else 0)


if __name__ == "__main__":
    main()
