#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主角性格一致性检查工具
检查主角是否符合设定：霸气、有恩必报、有仇必报、绝不圣母
"""

import sys
import re

# 主角性格设定
PROTAGONIST_RULES = {
    "禁止词语": ["算了吧", "算了", "原谅", "原谅他", "原谅她", "原谅他们", "算了算了"],
    "必备特质": ["冷笑", "嘲讽", "愤怒", "报仇", "滚", "配吗"],
    "口头禅": ["很好", "滚", "配吗", "有意思", "玩玩"],
    "禁止行为": ["忍气吞声超过500字", "圣母心态", "软弱犹豫", "原谅反派"],
    # 新增：主角不蠢货检查
    "禁止财务行为": [
        "刷爆信用卡",
        "透支.*?(无法|还不|还不上|困难)",
        "借.*?高利贷",
        "陷入绝境",
        "无脑消费",
        "立刻.*?买.*?不"
    ],
    "理智行为": [
        "冷静.*?思考",
        "先.*?计划",
        "想.*?再做",
        "观察.*?决定",
        "制定.*?计划"
    ]
}

def parse_chapter_content(file_path):
    """解析章节内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        return None

def check_protagonist_character(content):
    """检查主角性格"""
    issues = []
    warnings = []

    # 检查禁止词语
    for forbidden_word in PROTAGONIST_RULES["禁止词语"]:
        if forbidden_word in content:
            count = content.count(forbidden_word)
            issues.append(f"[ERROR] 发现禁止词语：'{forbidden_word}'出现{count}次")

    # 检查必备特质（至少要有一些）
    found_traits = []
    for trait in PROTAGONIST_RULES["必备特质"]:
        if trait in content:
            found_traits.append(trait)

    if len(found_traits) < 3:
        warnings.append(f"[WARN] 主角性格不够鲜明，只发现了{len(found_traits)}个必备特质：{found_traits}")

    # 检查口头禅
    found_catchphrases = []
    for catchphrase in PROTAGONIST_RULES["口头禅"]:
        if catchphrase in content:
            found_catchphrases.append(catchphrase)

    if not found_catchphrases:
        warnings.append("[WARN] 未发现主角口头禅")

    # 检查软弱表现（搜索软弱相关的描述）
    weak_patterns = [
        r'陈安.*?(犹豫|怯懦|害怕|恐惧|发抖|退缩)',
        r'他.*?(不敢|不能|算了|忍忍|忍气吞声)'
    ]

    for pattern in weak_patterns:
        matches = re.findall(pattern, content)
        if matches:
            warnings.append(f"[WARN] 发现软弱表现：{matches[0]}（共{len(matches)}处）")

    # 新增：检查主角是否"蠢货"（财务愚蠢行为）
    for stupid_pattern in PROTAGONIST_RULES["禁止财务行为"]:
        matches = re.findall(stupid_pattern, content)
        if matches:
            issues.append(f"[ERROR] 主角太蠢了！发现愚蠢财务行为：'{matches[0]}'（共{len(matches)}处）")

    # 新增：检查主角是否有理智行为
    rational_count = 0
    for rational_pattern in PROTAGONIST_RULES["理智行为"]:
        if re.search(rational_pattern, content):
            rational_count += 1

    if rational_count == 0:
        warnings.append("[WARN] 主角缺乏理智行为，像无头苍蝇乱撞")

    return issues, warnings

def print_report(file_path):
    """打印报告"""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 60)
    print(f"[主角性格检查] {file_path}")
    print("=" * 60)

    content = parse_chapter_content(file_path)

    if not content:
        print("[ERROR] 无法读取文件")
        return

    issues, warnings = check_protagonist_character(content)

    # 显示问题
    if issues:
        print(f"\n[必须修复]")
        for issue in issues:
            print(f"  {issue}")

    # 显示警告
    if warnings:
        print(f"\n[建议修复]")
        for warning in warnings:
            print(f"  {warning}")

    # 显示结果
    print("\n" + "=" * 60)
    if not issues and not warnings:
        print("[OK] 主角性格检查通过！")
    elif issues:
        print("[ERROR] 主角性格不符合设定")
    else:
        print("[WARN] 主角性格需要加强")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("用法：python protagonist_checker.py <章节文件路径>")
        print("示例：python protagonist_checker.py chapter-1_xxx.txt")
        return

    file_path = sys.argv[1]
    print_report(file_path)

if __name__ == '__main__':
    main()
