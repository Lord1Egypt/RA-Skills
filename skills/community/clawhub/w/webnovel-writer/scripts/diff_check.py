#!/usr/bin/env python3
"""章节差异检测 - 对比修改前后的章节，只显示差异和新增问题

用法:
    diff_check <旧目录> <新目录> [--outline <大纲>] [--dict <设定词典>]
"""

import difflib
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional

SCRIPTS_DIR = Path(__file__).parent


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _write(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def pair_chapters(old_dir: str, new_dir: str) -> List[Tuple[str, str, int, Optional[str]]]:
    """配对两个目录的章节文件，返回 [(old_path, new_path, 章号, 标题), ...]"""
    old_files = {}
    new_files = {}

    for f in Path(old_dir).glob("*.md"):
        m = re.search(r"第(\d+)", f.name)
        if m:
            old_files[int(m.group(1))] = (str(f), f.name)

    for f in Path(new_dir).glob("*.md"):
        m = re.search(r"第(\d+)", f.name)
        if m:
            new_files[int(m.group(1))] = (str(f), f.name)

    all_nums = sorted(set(old_files.keys()) | set(new_files.keys()))
    pairs = []
    for num in all_nums:
        old = old_files.get(num)
        new = new_files.get(num)
        old_path = old[0] if old else None
        new_path = new[0] if new else None
        title = (new or old)[1] if (new or old) else ""
        pairs.append((old_path, new_path, num, title))

    return pairs


def text_diff(old_text: str, new_text: str) -> dict:
    """生成文本差异"""
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)

    diff = list(difflib.unified_diff(old_lines, new_lines,
                                      fromfile="旧版", tofile="新版", n=1))

    added = sum(1 for l in diff if l.startswith("+") and not l.startswith("+++"))
    removed = sum(1 for l in diff if l.startswith("-") and not l.startswith("---"))

    return {
        "diff_lines": len(diff),
        "added_lines": added,
        "removed_lines": removed,
        "diff_text": "".join(diff),
    }


def analyze_modifications(old_text: str, new_text: str) -> List[dict]:
    """分析修改内容，找出可能引入的新问题"""
    issues = []

    diff = text_diff(old_text, new_text)
    if diff["diff_lines"] == 0:
        return issues

    # 1. 检查新增段落是否与上下文重复
    new_lines_set = set(new_text.splitlines())
    old_lines_set = set(old_text.splitlines())
    added_lines = new_lines_set - old_lines_set
    long_adds = [l for l in added_lines if len(l) >= 15]

    if long_adds:
        # 检查新增行之间是否互相重复
        from collections import Counter
        add_counts = Counter(long_adds)
        for line, count in add_counts.items():
            if count >= 2:
                issues.append({
                    "type": "新增重复",
                    "severity": "medium",
                    "detail": f"新增内容中重复出现: 「{line[:50]}…」",
                    "suggestion": "删除重复段落",
                })

    # 2. 检查新增内容的AI味
    ai_patterns = [
        r"不禁[了]?", r"缓缓[地]?", r"淡淡[地]?", r"微微[了]?",
        r"缓缓而[来]", r"不禁感慨", r"心中一[动震凛]",
        r"仿佛[被]?", r"竟然[不]?",
    ]
    for line in long_adds:
        for pat in ai_patterns:
            if re.search(pat, line):
                issues.append({
                    "type": "AI味",
                    "severity": "low",
                    "detail": f"新增内容含AI高频词: 「{line[:50]}…」",
                    "suggestion": f"替换「{pat}」相关表述",
                })
                break

    # 3. 检查新增对话标签
    added_text = "\n".join(added_lines)
    dialogue_patterns = re.findall(r'[："]\s*\w+\s*(说|道|笑|问|答|喊|叫|吼|吼)', added_text)
    if len(dialogue_patterns) > 5:
        unique_tags = set(dialogue_patterns)
        if len(unique_tags) <= 2:
            issues.append({
                "type": "对话标签单调",
                "severity": "low",
                "detail": f"新增{len(dialogue_patterns)}处对话，只用{len(unique_tags)}种标签: {unique_tags}",
                "suggestion": "丰富对话表达方式",
            })

    # 4. 检查是否引入了前后不一致（简单字面检查）
    old_names = set(re.findall(r"[\u4e00-\u9fff]{2,4}(?:说|道|想|看|走|来|去|笑|哭|叫|喊)", old_text))
    new_names = set(re.findall(r"[\u4e00-\u9fff]{2,4}(?:说|道|想|看|走|来|去|笑|哭|叫|喊)", new_text))
    removed_names = old_names - new_names
    if removed_names:
        for name in list(removed_names)[:3]:
            issues.append({
                "type": "名称变化",
                "severity": "info",
                "detail": f"旧版有「{name}」，新版消失",
                "suggestion": "确认是否为有意修改",
            })

    # 5. 字数变化过大警告
    old_len = len(old_text)
    new_len = len(new_text)
    change_pct = (new_len - old_len) / max(old_len, 1) * 100
    if abs(change_pct) > 30:
        direction = "增加" if change_pct > 0 else "减少"
        issues.append({
            "type": "字数变化",
            "severity": "info",
            "detail": f"字数{direction} {abs(change_pct):.0f}%（{old_len}→{new_len}字）",
            "suggestion": "确认修改幅度是否合理" if abs(change_pct) > 50 else "",
        })

    return issues


def generate_report(pairs: List, old_dir: str, new_dir: str, output: str = None) -> str:
    """生成完整的差异报告"""
    lines = []
    lines.append("# 章节差异检测报告\n")
    lines.append(f"旧目录: `{old_dir}`\n")
    lines.append(f"新目录: `{new_dir}`\n")

    total_issues = 0
    changed = 0
    added_chapters = 0
    removed_chapters = 0

    for old_path, new_path, num, title in pairs:
        if old_path and new_path:
            old_text = _read(old_path)
            new_text = _read(new_path)
            if old_text == new_text:
                continue

            changed += 1
            diff = text_diff(old_text, new_text)
            mods = analyze_modifications(old_text, new_text)

            lines.append(f"## 第{num:03d}章: {title}")
            lines.append(f"- 变更: +{diff['added_lines']}行 / -{diff['removed_lines']}行\n")

            if diff["diff_text"]:
                lines.append("<details><summary>查看差异</summary>\n")
                lines.append("```diff")
                lines.append(diff["diff_text"])
                lines.append("```\n")
                lines.append("</details>\n")

            if mods:
                total_issues += len(mods)
                lines.append("**发现的问题:**\n")
                for m in mods:
                    marker = "⚠️" if m["severity"] == "medium" else "💡"
                    lines.append(f"- {marker} [{m['type']}] {m['detail']}")
                    if m["suggestion"]:
                        lines.append(f"  → {m['suggestion']}")
                lines.append("")

        elif new_path and not old_path:
            added_chapters += 1
            lines.append(f"## 第{num:03d}章: {title} 🆕 新增章节\n")
        elif old_path and not new_path:
            removed_chapters += 1
            lines.append(f"## 第{num:03d}章: {title} ❌ 删除章节\n")

    # 汇总
    lines.insert(3, f"\n| 统计 | 数量 |")
    lines.insert(4, f"|------|------|")
    lines.insert(5, f"| 对比章节 | {len(pairs)} |")
    lines.insert(6, f"| 有变更 | {changed} |")
    lines.insert(7, f"| 新增章节 | {added_chapters} |")
    lines.insert(8, f"| 删除章节 | {removed_chapters} |")
    lines.insert(9, f"| 发现问题 | {total_issues} |")

    report = "\n".join(lines)

    if output:
        _write(output, report)
        print(f"✅ 报告已保存: {output}")
    else:
        print(report)

    return report


def main():
    if len(sys.argv) < 3:
        print("📖 章节差异检测")
        print("用法: diff_check <旧目录> <新目录> [--output <报告路径>]")
        print("  对比修改前后的章节，只显示差异和新增问题")
        sys.exit(0)

    old_dir = sys.argv[1]
    new_dir = sys.argv[2]
    output = None

    for i, arg in enumerate(sys.argv):
        if arg == "--output" and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]

    if not Path(old_dir).is_dir():
        print(f"❌ 目录不存在: {old_dir}")
        sys.exit(1)
    if not Path(new_dir).is_dir():
        print(f"❌ 目录不存在: {new_dir}")
        sys.exit(1)

    pairs = pair_chapters(old_dir, new_dir)
    if not pairs:
        print("❌ 未找到章节文件")
        sys.exit(1)

    print(f"🔍 对比 {len(pairs)} 章...\n")
    generate_report(pairs, old_dir, new_dir, output)


if __name__ == "__main__":
    main()
