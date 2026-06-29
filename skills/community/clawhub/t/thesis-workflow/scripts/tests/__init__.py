#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MBA Thesis Workflow - 单元测试
测试覆盖：state_manager.py / loop_self_check.py / md2docx_strict.py 关键函数
"""

import os
import sys
import tempfile
import unittest

# 路径修正：__file__ = scripts/tests/__init__.py
TEST_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(TEST_FILE)))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'scripts')
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, PROJECT_ROOT)

# 导入测试目标模块
import state_manager as sm
import md2docx_strict as md2d
import loop_self_check as lsc


# ==================== Test State Manager ====================

class TestStateManager(unittest.TestCase):
    """测试状态文件管理器"""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.paper = "测试论文_A公司"
        self.state = sm.create_state(
            self.paper,
            version="v1.0",
            planned_chapters=["chapter1_2_7", "chapter3_4", "chapter5_6"],
            workspace=self.tmpdir,
        )
        self.path = sm.state_path_for(self.paper, self.tmpdir)

    def tearDown(self):
        sm.delete_state(self.paper, self.tmpdir)

    def test_create_state(self):
        """测试创建状态文件"""
        self.assertTrue(os.path.exists(self.path))
        self.assertEqual(self.state["paper"], self.paper)
        self.assertEqual(self.state["phase"], "Phase 1")
        self.assertEqual(len(self.state["planned_chapters"]), 3)

    def test_load_state(self):
        """测试加载状态文件"""
        loaded = sm.load_state(self.paper, self.tmpdir)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["paper"], self.paper)

    def test_update_phase(self):
        """测试更新 Phase"""
        sm.update_phase(self.state, "Phase 2")
        self.assertEqual(self.state["phase"], "Phase 2")

    def test_update_chapter(self):
        """测试更新章节状态"""
        sm.update_chapter(self.state, "chapter3_4",
                          status="completed", file_path="/tmp/test.md", lines=500)
        ch = self.state["chapters"]["chapter3_4"]
        self.assertEqual(ch["status"], "completed")
        self.assertEqual(ch["lines"], 500)

    def test_all_chapters_pass(self):
        """测试章节完整性检测"""
        self.assertFalse(sm.all_chapters_exist(self.state))
        for ch in self.state["planned_chapters"]:
            sm.update_chapter(self.state, ch, status="completed")
        self.assertTrue(sm.all_chapters_exist(self.state))

    def test_increment_retry(self):
        """测试重试计数"""
        rnd = sm.increment_retry(self.state, "review_loop")
        self.assertEqual(rnd, 1)
        rnd = sm.increment_retry(self.state, "review_loop")
        self.assertEqual(rnd, 2)
        self.assertFalse(sm.is_retry_exceeded(self.state, "review_loop"))
        sm.increment_retry(self.state, "review_loop")
        self.assertTrue(sm.is_retry_exceeded(self.state, "review_loop"))

    def test_state_summary(self):
        """测试状态摘要生成"""
        summary = sm.format_state_summary(self.state)
        self.assertIn("Phase 1", summary)
        self.assertIn("0/3", summary)

    def test_resolve_paper_name(self):
        """测试论文名推断"""
        cases = [
            ("论文_A公司_v1.0_H_chapter3_4.md", "论文_A公司"),
            ("论文_A公司_v2.0_integrated.md", "论文_A公司"),
            ("thesis_v2_final.md", "thesis_final"),
        ]
        for path, expected in cases:
            result = sm.resolve_paper_name(path)
            self.assertEqual(result, expected, f"输入: {path}")


# ==================== Test Loop Self-Check ====================

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


# ==================== Test md2docx_strict ====================

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


# ==================== main ====================

if __name__ == "__main__":
    unittest.main(verbosity=2)
