#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_loop_self_check.py - loop_self_check.py 单元测试

由 scripts/tests/__init__.py 拆分而来（修复 P2-2）。
覆盖 check_chapter_completeness / check_mixed_chapter_format /
check_inline_bold / check_references / check_merge_residue /
check_chapter_keywords / run_checks 12 个函数。
"""

import os
import sys
import unittest

# 路径修正：本文件 = scripts/tests/test_loop_self_check.py
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(TESTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)

# 导入测试目标模块
import loop_self_check as lsc


class TestLoopSelfCheck(unittest.TestCase):
    """测试 Guardrails 校验函数"""

    def test_chapter_completeness_7(self):
        """章节完整性：7章齐全"""
        content = "\n".join(f"# 第{i}章 章节{i}" for i in range(1, 8))
        ok, msg = lsc.check_chapter_completeness(content)
        self.assertTrue(ok, msg)

    def test_chapter_completeness_missing(self):
        """章节完整性：缺章"""
        content = "# 第1章\n# 第2章\n# 第3章"
        ok, msg = lsc.check_chapter_completeness(content)
        self.assertFalse(ok, msg)

    def test_mixed_format_detected(self):
        """检测混合格式 ## 第X章"""
        content = "## 第1章 绪论"
        ok, msg = lsc.check_mixed_chapter_format(content)
        self.assertFalse(ok, msg)

    def test_mixed_format_clean(self):
        """正确格式 # 第X章"""
        content = "# 第1章 绪论"
        ok, msg = lsc.check_mixed_chapter_format(content)
        self.assertTrue(ok, msg)

    def test_inline_bold_detected(self):
        """检测正文加粗"""
        content = "这是正文，有一个**加粗**术语。"
        ok, msg = lsc.check_inline_bold(content)
        self.assertFalse(ok, msg)

    def test_inline_bold_title_ignored(self):
        """标题行的加粗被忽略"""
        content = "# 第1章 这是标题"
        ok, msg = lsc.check_inline_bold(content)
        self.assertTrue(ok, msg)

    def test_references_exist(self):
        """参考文献存在"""
        content = "正文内容\n## 参考文献\n[1] 测试"
        ok, msg = lsc.check_references(content)
        self.assertTrue(ok, msg)

    def test_references_missing(self):
        """参考文献缺失检测"""
        content = "正文内容，没有参考文献标题"
        ok, msg = lsc.check_references(content)
        self.assertFalse(ok, msg)

    def test_merge_residue_detected(self):
        """合并残留检测"""
        content = "正文\n===END===\n更多内容"
        ok, msg = lsc.check_merge_residue(content)
        self.assertFalse(ok, msg)

    def test_chapter_keywords_ok(self):
        """核心章节关键词存在"""
        content = (
            "# 第5章 战略选择\n"
            "本章讨论差异化竞争战略和QSPM矩阵。\n"
            "# 第6章 实施保障\n"
            "本章讨论组织保障和实施措施。\n"
            "# 第7章 结论\n"
        )
        ok, msg = lsc.check_chapter_keywords(content)
        self.assertTrue(ok, msg)

    def test_chapter_keywords_missing(self):
        """核心章节关键词缺失"""
        content = (
            "# 第5章 其他内容\n"
            "本章没有关键词。\n"
            "# 第6章 其他内容\n"
            "本章也没有关键词。\n"
        )
        ok, msg = lsc.check_chapter_keywords(content)
        self.assertFalse(ok, msg)

    def test_run_checks_all_pass(self):
        """运行全部校验，大部分通过"""
        content_lines = []
        for i in range(1, 8):
            content_lines.append(f"# 第{i}章 章节{i}")
            for j in range(100):
                content_lines.append(f"这是第{i}章的正文内容第{j}行，包含引用（张三，2020）。")
            # 第5章需要包含战略选择关键词
            if i == 5:
                content_lines.append("本章核心是竞争战略的差异化与集中化选择，使用QSPM矩阵。")
            # 第6章需要包含实施保障关键词
            if i == 6:
                content_lines.append("本章讨论组织保障和KPI考核体系的实施措施。")
        content_lines.append("## 参考文献")
        content_lines.append("[1] 张三. 测试研究. 2020")
        content = '\n'.join(content_lines)
        report = lsc.run_checks(content)
        self.assertTrue(report["all_passed"], f"失败项: {report['results']}")


if __name__ == "__main__":
    unittest.main(verbosity=2)