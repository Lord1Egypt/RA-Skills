#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_md2docx_strict.py - md2docx_strict.py 单元测试

由 scripts/tests/__init__.py 拆分而来（修复 P2-2）。
覆盖 _is_tbl_sep / _strip_bold / _find_review_report /
_check_report_passed 5 个函数。
"""

import os
import sys
import tempfile
import unittest

# 路径修正：本文件 = scripts/tests/test_md2docx_strict.py
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(TESTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)

# 导入测试目标模块
import md2docx_strict as md2d


class TestMd2DocxStrict(unittest.TestCase):
    """测试 Word 转换脚本的关键函数"""

    def test_is_tbl_sep(self):
        """表头分隔行识别"""
        self.assertTrue(md2d._is_tbl_sep("| :--- | :---: | ---: |"))
        self.assertTrue(md2d._is_tbl_sep("| --- | --- |"))
        self.assertFalse(md2d._is_tbl_sep("| a | b | c |"))
        self.assertFalse(md2d._is_tbl_sep(""))

    def test_strip_bold(self):
        """加粗标记清除"""
        self.assertEqual(md2d._strip_bold("普通文字"), "普通文字")
        self.assertEqual(md2d._strip_bold("**加粗**文字"), "加粗文字")
        self.assertEqual(md2d._strip_bold("前**中**后"), "前中后")
        self.assertEqual(md2d._strip_bold("**全行加粗**"), "全行加粗")

    def test_find_review_report_no_dir(self):
        """审核报告查找：空目录"""
        tmpdir = tempfile.mkdtemp()
        fake_md = os.path.join(tmpdir, "论文_A公司_v4.0.md")
        # 没有审核报告
        result = md2d._find_review_report(fake_md)
        self.assertIsNone(result)

    def test_check_report_passed_grade(self):
        """审核报告解析：结构化评分"""
        tmpdir = tempfile.mkdtemp()
        report = os.path.join(tmpdir, "审核报告_v1.md")
        with open(report, 'w', encoding='utf-8') as f:
            f.write("评级：通过\n其他内容")
        self.assertTrue(md2d._check_report_passed(report))
        with open(report, 'w', encoding='utf-8') as f:
            f.write("评级：不通过\n其他内容")
        self.assertFalse(md2d._check_report_passed(report))

    def test_check_report_passed_emoji(self):
        """审核报告解析：emoji 回退"""
        tmpdir = tempfile.mkdtemp()
        report = os.path.join(tmpdir, "审核报告_v1.md")
        with open(report, 'w', encoding='utf-8') as f:
            f.write("✅ 通过\n其他内容")
        self.assertTrue(md2d._check_report_passed(report))


if __name__ == "__main__":
    unittest.main(verbosity=2)