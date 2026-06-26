#!/usr/bin/env python3
"""
spec-engine compare — 对比两个 spec 版本的差异。

用法:
    python compare.py <旧spec> <新spec> [--json]

输出:
    - 新增的 section
    - 删除的 section
    - 修改的 section（显示内容差异）
"""

import argparse
import json
import os
import re
import sys
from difflib import unified_diff


def read_spec(filepath):
    """读取 spec 文件，自动去除 BOM。"""
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"[ERROR] 文件编码错误: {filepath}", file=sys.stderr)
        sys.exit(1)


def parse_sections(text):
    """
    将 markdown 文本解析为 sections dict。
    返回: {标题: 完整section文本(含##标题)}
    """
    sections = {}
    # 匹配 ## 标题和内容
    lines = text.split("\n")
    current_title = None
    current_content = []

    for line in lines:
        h2_match = re.match(r"^##\s+(.+)$", line)
        h1_match = re.match(r"^#\s+(.+)$", line)

        if h1_match:
            # 一级标题作为特殊 section
            if current_title:
                sections[current_title] = "\n".join(current_content).strip()
            current_title = "__title__"
            current_content = [line]
        elif h2_match:
            if current_title:
                sections[current_title] = "\n".join(current_content).strip()
            raw_title = h2_match.group(1).strip()
            # 清理编号前缀，保留原始标题作 key
            clean_title = re.sub(r"^\d+[.、]?\s*", "", raw_title).strip()
            current_title = clean_title
            current_content = [line]
        else:
            current_content.append(line)

    # 最后一个 section
    if current_title:
        sections[current_title] = "\n".join(current_content).strip()

    return sections


def compare_specs(old_text, new_text):
    """
    对比两个 spec，返回差异信息。
    返回: {
        "added": [section_names],
        "removed": [section_names],
        "modified": [{"section": name, "diff": diff_text}],
        "unchanged": [section_names],
    }
    """
    old_sections = parse_sections(old_text)
    new_sections = parse_sections(new_text)

    old_keys = set(old_sections.keys())
    new_keys = set(new_sections.keys())

    added = sorted(new_keys - old_keys)
    removed = sorted(old_keys - new_keys)
    common = old_keys & new_keys

    modified = []
    unchanged = []

    for key in sorted(common):
        if old_sections[key] == new_sections[key]:
            unchanged.append(key)
        else:
            # 生成 unified diff
            old_lines = old_sections[key].splitlines(keepends=True)
            new_lines = new_sections[key].splitlines(keepends=True)
            diff = list(unified_diff(
                old_lines, new_lines,
                fromfile=f"旧版/{key}",
                tofile=f"新版/{key}",
                lineterm=""
            ))
            modified.append({
                "section": key,
                "diff": "\n".join(diff),
            })

    return {
        "added": added,
        "removed": removed,
        "modified": modified,
        "unchanged": unchanged,
    }


def print_report(old_file, new_file, result):
    """打印对比报告。"""
    print(f"\nSpec 对比报告")
    print(f"  旧版: {old_file}")
    print(f"  新版: {new_file}")
    print()

    if not result["added"] and not result["removed"] and not result["modified"]:
        print("  [OK] 两个版本完全相同")
        return

    # 新增
    if result["added"]:
        print(f"  [ADDED] 新增 section ({len(result['added'])}个):")
        for name in result["added"]:
            print(f"     + {name}")
        print()

    # 删除
    if result["removed"]:
        print(f"  [REMOVED] 删除 section ({len(result['removed'])}个):")
        for name in result["removed"]:
            print(f"     - {name}")
        print()

    # 修改
    if result["modified"]:
        print(f"  [MODIFIED] 修改 section ({len(result['modified'])}个):")
        for item in result["modified"]:
            print(f"\n  --- {item['section']} ---")
            print(item["diff"])
        print()

    # 未变
    if result["unchanged"]:
        print(f"  [UNCHANGED] 未变 section ({len(result['unchanged'])}个):")
        for name in result["unchanged"]:
            print(f"     {name}")
        print()


def print_json_report(old_file, new_file, result):
    """以 JSON 格式输出报告。"""
    report = {
        "old_file": old_file,
        "new_file": new_file,
        "added": result["added"],
        "removed": result["removed"],
        "modified": result["modified"],
        "unchanged": result["unchanged"],
        "summary": {
            "added_count": len(result["added"]),
            "removed_count": len(result["removed"]),
            "modified_count": len(result["modified"]),
            "unchanged_count": len(result["unchanged"]),
        }
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="spec-engine compare — 对比两个 spec 版本差异"
    )
    parser.add_argument("old_spec", help="旧版 spec 文件路径")
    parser.add_argument("new_spec", help="新版 spec 文件路径")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 格式输出")
    args = parser.parse_args()

    old_text = read_spec(args.old_spec)
    new_text = read_spec(args.new_spec)

    result = compare_specs(old_text, new_text)

    if args.json:
        print_json_report(args.old_spec, args.new_spec, result)
    else:
        print_report(args.old_spec, args.new_spec, result)


if __name__ == "__main__":
    main()
