#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节综合检查器
检查章节的基础结构、格式、完整性
"""

import re
import os
from pathlib import Path


class ChapterChecker:
    """章节检查器类"""

    def __init__(self, file_path=None):
        """
        初始化检查器

        Args:
            file_path: 章节文件路径
        """
        self.file_path = file_path
        self.content = None
        self.issues = []
        self.warnings = []

        # 自动加载文件内容
        if file_path:
            self.load_file(file_path)

    def load_file(self, file_path=None):
        """
        加载章节文件

        Args:
            file_path: 章节文件路径（可选，默认使用初始化时的路径）

        Returns:
            bool: 是否成功加载
        """
        if file_path:
            self.file_path = file_path

        if not self.file_path:
            self.issues.append("未指定文件路径")
            return False

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except Exception as e:
            self.issues.append(f"无法读取文件: {e}")
            return False

    def check_structure(self):
        """
        检查章节基础结构

        Returns:
            tuple: (issues, warnings)
        """
        issues = []
        warnings = []

        if not self.content:
            return ["内容为空"], []

        # 注意：根据提示词要求，章节不需要标题
        # 检查标题格式（已禁用）
        # if not re.search(r'^第\d+章\s+.+', self.content, re.MULTILINE):
        #     issues.append("缺少章节标题（格式：第X章 标题）")

        # 检查是否有正文内容（直接检查原始内容）
        if len(self.content.strip()) < 100:
            issues.append("正文内容过短")

        # 检查是否有财务总结
        if '财务总结' not in self.content and '当前余额' not in self.content:
            warnings.append("缺少财务总结部分")

        # 下一章预告检查（已禁用 - 根据SKILL.md要求，不需要下章预告）
        # SKILL.md明确规定：不要写"下章预告"、"本章完"等元叙事元素

        return issues, warnings

    def check_format(self):
        """
        检查章节格式

        Returns:
            tuple: (issues, warnings)
        """
        issues = []
        warnings = []

        if not self.content:
            return ["内容为空"], []

        # 检查是否有空行过多
        empty_line_blocks = re.findall(r'\n\s*\n\s*\n+', self.content)
        if len(empty_line_blocks) > 20:
            warnings.append(f"空行过多（{len(empty_line_blocks)}处）")

        # 检查对话引号是否匹配
        single_quotes = self.content.count('"')
        if single_quotes % 2 != 0:
            warnings.append("对话引号数量为奇数，可能有未闭合的引号")

        # 检查是否有全角标点混用
        chinese_comma_in_english = re.findall(r'[a-zA-Z][，][a-zA-Z]', self.content)
        if chinese_comma_in_english:
            warnings.append(f"发现{len(chinese_comma_in_english)}处英文中混用中文逗号")

        return issues, warnings

    def check_word_count(self, min_words=3000, max_words=3500):
        """
        检查字数（与 word_count_tool.py 方法完全一致）

        Args:
            min_words: 最小字数
            max_words: 最大字数

        Returns:
            tuple: (word_count, issues, warnings)
        """
        issues = []
        warnings = []

        if not self.content:
            return 0, ["内容为空"], []

        # ⚠️ 修复：移除【变量更新】部分（与 word_count_tool.py 保持一致）
        body = self.content
        if '【变量更新】' in body:
            body = body.split('【变量更新】')[0]

        # 移除多余换行
        body = re.sub(r'\n+', '\n', body)
        body = body.strip()

        # 统计字数（中文字符+英文单词）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', body))
        english_words = len(re.findall(r'[a-zA-Z]+', body))
        word_count = chinese_chars + english_words

        if word_count < min_words:
            issues.append(f"字数不足：{word_count}字（要求≥{min_words}字）")
        elif word_count > max_words:
            issues.append(f"字数过多：{word_count}字（要求≤{max_words}字，超出{word_count - max_words}字）")

        return word_count, issues, warnings

    def check_all(self):
        """
        运行所有检查

        Returns:
            dict: 检查结果
        """
        all_issues = []
        all_warnings = []

        # 结构检查
        issues, warnings = self.check_structure()
        all_issues.extend(issues)
        all_warnings.extend(warnings)

        # 格式检查
        issues, warnings = self.check_format()
        all_issues.extend(issues)
        all_warnings.extend(warnings)

        # 字数检查
        word_count, issues, warnings = self.check_word_count()
        all_issues.extend(issues)
        all_warnings.extend(warnings)

        return {
            'word_count': word_count,
            'issues': all_issues,
            'warnings': all_warnings,
            'passed': len(all_issues) == 0
        }


def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法: python chapter_checker.py <章节文件>")
        print("示例: python chapter_checker.py chapter-1_xxx.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        sys.exit(1)

    checker = ChapterChecker(file_path)
    if not checker.load_file():
        print("无法加载文件")
        sys.exit(1)

    result = checker.check_all()

    print("=" * 60)
    print("章节检查报告")
    print("=" * 60)
    print(f"文件: {file_path}")
    print(f"字数: {result['word_count']}")

    if result['issues']:
        print(f"\n发现 {len(result['issues'])} 个问题:")
        for i, issue in enumerate(result['issues'], 1):
            print(f"  {i}. {issue}")

    if result['warnings']:
        print(f"\n发现 {len(result['warnings'])} 个警告:")
        for i, warning in enumerate(result['warnings'], 1):
            print(f"  {i}. {warning}")

    if result['passed']:
        print("\n检查通过！")
        sys.exit(0)
    else:
        print(f"\n检查失败，发现 {len(result['issues'])} 个问题")
        sys.exit(1)


if __name__ == '__main__':
    main()

