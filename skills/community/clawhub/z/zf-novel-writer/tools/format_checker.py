#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
格式检查工具
检查章节文件格式是否符合要求
"""

import re
import sys
from pathlib import Path


def check_format(file_path):
    """
    检查章节文件格式

    Args:
        file_path: 章节文件路径

    Returns:
        dict: {'issues': [], 'warnings': []}
    """
    result = {'issues': [], 'warnings': []}

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        result['issues'].append(f"无法读取文件: {e}")
        return result

    # 检查1: 是否有章节标题（已禁用 - 根据新写作规范，章节不需要标题）
    # if not re.search(r'^第\d+章\s+.+', content, re.MULTILINE):
    #     result['issues'].append("缺少章节标题（格式：第X章 标题）")

    # 检查2: 是否有正文内容
    body = re.sub(r'^第\d+章\s+.+\n*', '', content, count=1).strip()
    if len(body) < 100:
        result['issues'].append("正文内容过短（<100字）")

    # 检查3: 对话引号是否匹配
    quote_count = content.count('"')
    if quote_count % 2 != 0:
        result['warnings'].append(f"双引号数量为奇数（{quote_count}个），可能有未闭合的引号")

    # 检查4: 允许段落间空行，但不应过多
    empty_lines = len(re.findall(r'\n\s*\n', content))
    if empty_lines > 200:
        result['warnings'].append(f"空行过多（{empty_lines}处），建议减少到150以内")
    elif empty_lines > 150:
        result['issues'].append(f"空行略多（{empty_lines}处），建议优化段落结构")

    # 检查5: 是否有财务总结
    if '当前余额' not in content and '财务总结' not in content:
        result['warnings'].append("缺少财务总结部分")

    # 检查6: 是否有下一章预告
    if '下一章预告' not in content:
        result['warnings'].append("缺少下一章预告部分")

    # 检查7: 是否有系统提示
    if '系统' not in content and '返还' not in content:
        result['warnings'].append("可能缺少系统相关内容")

    # 检查8: 格式一致性
    lines = content.split('\n')
    dialogue_lines = [line for line in lines if '"' in line]
    if dialogue_lines:
        # 检查对话格式是否一致（是否有说话人标注）
        has_speaker = any(re.search(r'说[：:]', line) or re.search(r'[问道答][：:]', line) for line in dialogue_lines)
        if has_speaker and len(dialogue_lines) > 5:
            # 有说话人标注，检查是否所有对话都有
            without_speaker = [line for line in dialogue_lines
                             if not re.search(r'说[：:]', line)
                             and not re.search(r'[问道答][：:]', line)
                             and not line.strip().startswith('"')]
            if len(without_speaker) > len(dialogue_lines) * 0.5:
                result['warnings'].append("部分对话缺少说话人标注")

    return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python format_checker.py <章节文件>")
        print("示例: python format_checker.py chapter-1_xxx.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"文件不存在: {file_path}")
        sys.exit(1)

    result = check_format(file_path)

    print("=" * 60)
    print("格式检查报告")
    print("=" * 60)

    if result['issues']:
        print(f"\n发现 {len(result['issues'])} 个格式错误:")
        for i, issue in enumerate(result['issues'], 1):
            print(f"  {i}. {issue}")
    else:
        print("\n未发现格式错误")

    if result['warnings']:
        print(f"\n发现 {len(result['warnings'])} 个格式警告:")
        for i, warning in enumerate(result['warnings'], 1):
            print(f"  {i}. {warning}")

    print("=" * 60)

    if result['issues']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
