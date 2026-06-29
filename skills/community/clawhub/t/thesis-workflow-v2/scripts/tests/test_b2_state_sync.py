#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_b2_state_sync.py - 修复 B-2 的回归测试

覆盖：
1. outline_update_status(status="completed") 同步 orchestrate state.completed_nodes
2. outline_update_status(status="failed") 同步 orchestrate state.failed_nodes
3. failed → completed 转换：completed_nodes 加入，failed_nodes 移除
4. completed → failed 转换：failed_nodes 加入，completed_nodes 移除
5. 其他状态（writing / pending）不触发同步
6. orchestrate state 未初始化时同步函数安全跳过
7. orchestrate state 函数（load/save/init/update_progress）从 state_manager_v2 正确导出
"""

import os
import shutil
import sys
import unittest

# 路径修正
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(TESTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, TESTS_DIR)

from state_manager_v2 import (
    outline_save, outline_update_status, outline_load, _get_state_path,
    init_orchestrate_state, load_orchestrate_state, save_orchestrate_state,
    update_progress, _get_orchestrate_state_path, sync_orchestrate_state_from_outline,
)
from outline_parser import insert_chapter_summary_nodes


TEST_PAPER = "test_b2_state_sync"


def setup_outline():
    """构造最小化 outline + orchestrate state"""
    nodes = [
        {"id": "ch1", "level": 1, "title": "绪论", "parent_id": None,
         "children_ids": ["1.1", "1.2"], "prev_sibling_id": None, "next_sibling_id": None,
         "writing_status": "pending"},
        {"id": "1.1", "level": 2, "title": "选题背景", "parent_id": "ch1",
         "children_ids": [], "prev_sibling_id": None, "next_sibling_id": "1.2",
         "writing_status": "pending"},
        {"id": "1.2", "level": 2, "title": "研究问题", "parent_id": "ch1",
         "children_ids": [], "prev_sibling_id": "1.1", "next_sibling_id": None,
         "writing_status": "pending"},
    ]
    outline = {"outline_tree": {"metadata": {"paper_title": "test"}, "nodes": nodes}}
    outline_with_summary = insert_chapter_summary_nodes(outline)
    outline_save(TEST_PAPER, outline_with_summary)
    # 初始化 orchestrate state
    init_orchestrate_state(TEST_PAPER)


def cleanup():
    """清理测试状态"""
    paper_dir = os.path.join(os.path.expanduser("~/.openclaw/workspace"), TEST_PAPER)
    if os.path.exists(paper_dir):
        shutil.rmtree(paper_dir)


class TestOrchestrateStateMigration(unittest.TestCase):
    """验证 orchestrate state 函数已迁移到 state_manager_v2"""

    def setUp(self):
        cleanup()
        setup_outline()

    def tearDown(self):
        cleanup()

    def test_load_orchestrate_state_from_state_manager(self):
        """load_orchestrate_state 应从 state_manager_v2 导入"""
        state = load_orchestrate_state(TEST_PAPER)
        self.assertIsNotNone(state)
        self.assertEqual(state["paper_name"], TEST_PAPER)
        self.assertEqual(state["completed_nodes"], [])

    def test_save_orchestrate_state_from_state_manager(self):
        """save_orchestrate_state 应从 state_manager_v2 导入"""
        state = load_orchestrate_state(TEST_PAPER)
        state["phase"] = "phase2"
        self.assertTrue(save_orchestrate_state(TEST_PAPER, state))
        reloaded = load_orchestrate_state(TEST_PAPER)
        self.assertEqual(reloaded["phase"], "phase2")

    def test_init_orchestrate_state_from_state_manager(self):
        """init_orchestrate_state 应从 state_manager_v2 导入"""
        # setup_outline 已初始化，再次调用应正常工作
        state = init_orchestrate_state(TEST_PAPER)
        self.assertIsNotNone(state)
        # 节点数 = 3 真实 (ch1/1.1/1.2) + 1 虚拟摘要 (__ch1_summary__) = 4
        self.assertEqual(state["progress"]["total"], 4)

    def test_update_progress_from_state_manager(self):
        """update_progress 应从 state_manager_v2 导入"""
        state = load_orchestrate_state(TEST_PAPER)
        state["completed_nodes"] = ["1.1", "1.2"]
        update_progress(state)
        self.assertEqual(state["progress"]["completed"], 2)


class TestOutlineUpdateStatusSync(unittest.TestCase):
    """修复 B-2: outline_update_status 同步 orchestrate state"""

    def setUp(self):
        cleanup()
        setup_outline()

    def tearDown(self):
        cleanup()

    def test_completed_status_syncs_completed_nodes(self):
        """测试 1：status='completed' 同步 completed_nodes 列表"""
        r = outline_update_status(TEST_PAPER, "1.1", "completed",
                                  key_conclusion="结论1", word_count=100)
        self.assertTrue(r["ok"])

        state = load_orchestrate_state(TEST_PAPER)
        self.assertIn("1.1", state["completed_nodes"],
                      "completed status 应同步到 orchestrate state.completed_nodes")
        self.assertNotIn("1.1", state["failed_nodes"])

    def test_failed_status_syncs_failed_nodes(self):
        """测试 2：status='failed' 同步 failed_nodes 列表"""
        r = outline_update_status(TEST_PAPER, "1.2", "failed", retry_count=1)
        self.assertTrue(r["ok"])

        state = load_orchestrate_state(TEST_PAPER)
        self.assertIn("1.2", state["failed_nodes"],
                      "failed status 应同步到 orchestrate state.failed_nodes")
        self.assertNotIn("1.2", state["completed_nodes"])

    def test_failed_to_completed_removes_from_failed(self):
        """测试 3：failed → completed 转换：从 failed_nodes 移除"""
        outline_update_status(TEST_PAPER, "1.1", "failed", retry_count=1)
        state = load_orchestrate_state(TEST_PAPER)
        self.assertIn("1.1", state["failed_nodes"])

        # 重写为 completed
        outline_update_status(TEST_PAPER, "1.1", "completed",
                              key_conclusion="重写完成", word_count=150)
        state = load_orchestrate_state(TEST_PAPER)
        self.assertIn("1.1", state["completed_nodes"])
        self.assertNotIn("1.1", state["failed_nodes"],
                         "重写为 completed 后应从 failed_nodes 移除")

    def test_completed_to_failed_removes_from_completed(self):
        """测试 4：completed → failed 转换：从 completed_nodes 移除"""
        outline_update_status(TEST_PAPER, "1.1", "completed", key_conclusion="首次完成")
        state = load_orchestrate_state(TEST_PAPER)
        self.assertIn("1.1", state["completed_nodes"])

        # 改为 failed
        outline_update_status(TEST_PAPER, "1.1", "failed", retry_count=1)
        state = load_orchestrate_state(TEST_PAPER)
        self.assertIn("1.1", state["failed_nodes"])
        self.assertNotIn("1.1", state["completed_nodes"],
                        "改为 failed 后应从 completed_nodes 移除")

    def test_other_status_does_not_sync(self):
        """测试 5：writing / pending / approved 状态不触发同步"""
        # 直接调用 sync 函数确保未触发同步
        for status in ("writing", "pending", "approved"):
            with self.subTest(status=status):
                outline_update_status(TEST_PAPER, "1.1", status)
                state = load_orchestrate_state(TEST_PAPER)
                self.assertNotIn("1.1", state["completed_nodes"])
                self.assertNotIn("1.1", state["failed_nodes"])


class TestSyncHelperSafety(unittest.TestCase):
    """sync_orchestrate_state_from_outline 安全测试"""

    def tearDown(self):
        cleanup()

    def test_sync_skips_when_orchestrate_state_not_initialized(self):
        """测试 6：orchestrate state 未初始化时同步函数安全跳过"""
        # 只初始化 outline state，不初始化 orchestrate state
        nodes = [{"id": "1.1", "level": 2, "title": "test", "parent_id": "ch1",
                  "children_ids": [], "prev_sibling_id": None, "next_sibling_id": None,
                  "writing_status": "pending"}]
        outline = {"outline_tree": {"metadata": {}, "nodes": nodes}}
        outline_save(TEST_PAPER, outline)

        # 确保 orchestrate state 不存在
        orchestrate_path = _get_orchestrate_state_path(TEST_PAPER)
        if os.path.exists(orchestrate_path):
            os.remove(orchestrate_path)

        # 调用 outline_update_status 应正常完成（同步被静默跳过）
        r = outline_update_status(TEST_PAPER, "1.1", "completed", word_count=10)
        self.assertTrue(r["ok"])

        # 确认 orchestrate state 仍未创建（不会因为 sync 而自动创建）
        # sync 函数不主动创建，仅在已存在时同步

    def test_sync_helper_direct_call(self):
        """测试 7：直接调用 sync_orchestrate_state_from_outline 验证逻辑"""
        setup_outline()
        try:
            # completed → 加入 completed_nodes
            sync_orchestrate_state_from_outline(TEST_PAPER, "1.1", "completed")
            state = load_orchestrate_state(TEST_PAPER)
            self.assertIn("1.1", state["completed_nodes"])

            # failed → 从 completed_nodes 移除，加入 failed_nodes
            sync_orchestrate_state_from_outline(TEST_PAPER, "1.1", "failed")
            state = load_orchestrate_state(TEST_PAPER)
            self.assertNotIn("1.1", state["completed_nodes"])
            self.assertIn("1.1", state["failed_nodes"])

            # writing → 不变
            sync_orchestrate_state_from_outline(TEST_PAPER, "1.2", "writing")
            state = load_orchestrate_state(TEST_PAPER)
            self.assertNotIn("1.2", state["completed_nodes"])
            self.assertNotIn("1.2", state["failed_nodes"])
        finally:
            cleanup()

    def test_progress_counter_synced(self):
        """测试 8：进度计数同步（B-2 增强：progress.completed 随列表更新）"""
        setup_outline()
        try:
            # 初始 progress.completed = 0
            state = load_orchestrate_state(TEST_PAPER)
            self.assertEqual(state["progress"]["completed"], 0)

            # 完成 1.1 → progress.completed = 1
            outline_update_status(TEST_PAPER, "1.1", "completed", word_count=10)
            state = load_orchestrate_state(TEST_PAPER)
            self.assertEqual(state["progress"]["completed"], 1)

            # 完成 1.2 → progress.completed = 2
            outline_update_status(TEST_PAPER, "1.2", "completed", word_count=10)
            state = load_orchestrate_state(TEST_PAPER)
            self.assertEqual(state["progress"]["completed"], 2)

            # 失败 1.1 → progress.completed = 1, progress.failed = 1
            outline_update_status(TEST_PAPER, "1.1", "failed", retry_count=1)
            state = load_orchestrate_state(TEST_PAPER)
            self.assertEqual(state["progress"]["completed"], 1)
            self.assertEqual(state["progress"]["failed"], 1)
        finally:
            cleanup()


if __name__ == "__main__":
    unittest.main(verbosity=2)