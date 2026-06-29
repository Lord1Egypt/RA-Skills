#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_state_manager.py - state_manager.py 单元测试

由 scripts/tests/__init__.py 拆分而来（修复 P2-2）。
覆盖 create_state / load_state / update_phase / update_chapter /
all_chapters_exist / increment_retry / is_retry_exceeded /
format_state_summary / resolve_paper_name 9 个方法。
"""

import os
import sys
import tempfile
import unittest

# 路径修正：本文件 = scripts/tests/test_state_manager.py
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(TESTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)

# 导入测试目标模块
import state_manager as sm


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


if __name__ == "__main__":
    unittest.main(verbosity=2)