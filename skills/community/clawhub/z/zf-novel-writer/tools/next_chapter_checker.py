#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
下一章预告检查工具
检查下一章预告是否超过20字且不剧透
"""

import sys
import re

def parse_next_chapter_preview(content):
    """解析下一章预告"""
    # 查找下一章预告部分（支持空行）
    patterns = [
        r'下章预告\s*\n\s*(.+)',      # 新增：匹配"下章预告\n内容"
        r'下章预告[：:]\s*(.+)',       # 新增：匹配"下章预告：内容"
        r'下一章[：:预告]*(.+)',       # 原有：匹配"下一章：内容"
        r'下一章[：:]\s*(.+)',         # 原有：匹配"下一章：内容"
        r'预告[：:]\s*(.+)'            # 原有：匹配"预告：内容"
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1).strip()

    return None

def check_hook_teaser(preview_text):
    """检查hook是否只说一半、不说破"""
    issues = []

    # 检查是否说了完整的结果（把话说破）
    full_reveal_patterns = [
        r'最终.{0,5}成功',
        r'最终.{0,5}失败',
        r'最后.{0,3}了',
        r'果然.{0,5}了',
        r'原来.{0,5}是',
        r'竟然.{0,5}了',
        r'决定.{0,5}了',
        r'已经.{0,5}了'
    ]

    for pattern in full_reveal_patterns:
        if re.search(pattern, preview_text):
            issues.append("[ERROR] 把话说破：包含完整结果描述，应该只说一半留悬念")
            break

    # 检查是否泄露核心信息
    info_leak_patterns = [
        r'是.{0,3}的儿子',
        r'是.{0,3}的父亲',
        r'就是.{0,5}',
        r'背后.{0,3}是',
        r'真正.{0,3}是'
    ]

    for pattern in info_leak_patterns:
        if re.search(pattern, preview_text):
            issues.append("[ERROR] 泄露核心信息：直接揭示了身份或真相")
            break

    # 检查是否是完整的陈述句（把话说死）
    # 完整的陈述句通常以句号结尾，且没有省略号
    if preview_text.endswith('。') and '...' not in preview_text and '…' not in preview_text:
        # 检查是否包含疑问词（如果有疑问词，可能是疑问句）
        question_words = ['谁', '什么', '哪里', '怎么', '为什么', '是否', '能否', '会不会']
        has_question = any(word in preview_text for word in question_words)
        if not has_question:
            issues.append("[ERROR] 把话说死：完整陈述句结尾，建议改为疑问句或省略号")

    return issues

def validate_preview(preview_text):
    """验证预告"""
    issues = []
    warnings = []

    if not preview_text:
        issues.append("[ERROR] 未找到下一章预告")
        return issues, warnings

    # 检查字数（30字限制）
    char_count = len(preview_text)
    if char_count > 30:
        issues.append(f"[ERROR] 预告过长：{char_count}字（应≤30字）")

    # 检查是否剧透（包含明确的结局描述）
    spoiler_keywords = ["结局", "破产", "后悔", "跪舔", "成功", "收购", "成为", "首富"]
    for keyword in spoiler_keywords:
        if keyword in preview_text:
            warnings.append(f"[WARN] 可能剧透：包含关键词'{keyword}'")

    # 检查是否有悬念（应该包含省略号、疑问号或未完成的句子）
    suspense_patterns = ["...", "…", "？", "?", "突然", "竟然", "没想到"]
    has_suspense = any(pattern in preview_text for pattern in suspense_patterns)
    if not has_suspense:
        warnings.append("[WARN] 缺乏悬念：建议添加省略号、疑问句或意外转折")

    # ⭐ 新增：检查hook是否只说一半、不说破
    hook_issues = check_hook_teaser(preview_text)
    issues.extend(hook_issues)

    return issues, warnings

def print_report(file_path):
    """打印报告"""
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("=" * 60)
    print(f"[下一章预告检查] {file_path}")
    print("=" * 60)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        print("[ERROR] 无法读取文件")
        return

    preview = parse_next_chapter_preview(content)
    issues, warnings = validate_preview(preview)

    # 显示预告内容
    if preview:
        print(f"\n[下一章预告]")
        print(f"  内容：{preview}")
        print(f"  字数：{len(preview)}字")
    else:
        print(f"\n[下一章预告]")
        print(f"  未找到")

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
        print("[OK] 下一章预告检查通过！")
    elif issues:
        print("[ERROR] 下一章预告不符合要求")
    else:
        print("[WARN] 下一章预告需要改进")
    print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("用法：python next_chapter_checker.py <章节文件路径>")
        print("示例：python next_chapter_checker.py chapter-1_xxx.txt")
        return

    file_path = sys.argv[1]
    print_report(file_path)

if __name__ == '__main__':
    main()
