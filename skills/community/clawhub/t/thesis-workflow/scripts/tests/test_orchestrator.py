#!/usr/bin/env python3
"""
test_orchestrator.py - Orchestrator V2 单元测试
"""

import sys
import os
import unittest
from unittest.mock import patch

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'scripts'))

from test_context_builder import setup_mock_state

from orchestrator_v2 import (
    load_orchestrate_state,
    save_orchestrate_state,
    init_orchestrate_state,
    update_progress,
    get_next_writing_node,
    orchestrate_phase1,
    confirm_phase1,
    handle_review_decision,
    orchestrate,
)


class TestOrchestrateState(unittest.TestCase):
    """编排状态管理测试"""

    def setUp(self):
        self.paper_name = setup_mock_state()

    def test_init_state(self):
        state = init_orchestrate_state(self.paper_name)
        self.assertEqual(state["paper_name"], self.paper_name)
        self.assertEqual(state["phase"], "phase1")
        self.assertFalse(state["phase1_confirmed"])
        self.assertEqual(len(state["completed_nodes"]), 0)

    def test_save_and_load(self):
        state = init_orchestrate_state(self.paper_name)
        state["completed_nodes"].append("1.1")

        saved = save_orchestrate_state(self.paper_name, state)
        self.assertTrue(saved)

        loaded = load_orchestrate_state(self.paper_name)
        self.assertEqual(loaded["paper_name"], self.paper_name)
        self.assertIn("1.1", loaded["completed_nodes"])

    def test_update_progress(self):
        state = init_orchestrate_state(self.paper_name)
        state["completed_nodes"] = ["1.1", "1.2"]
        state["pending_review"] = ["1.3"]
        state["failed_nodes"] = ["1.4"]

        state = update_progress(state)

        self.assertEqual(state["progress"]["completed"], 2)
        self.assertEqual(state["progress"]["pending"], 1)
        self.assertEqual(state["progress"]["failed"], 1)


class TestPhase1(unittest.TestCase):
    """Phase 1 测试"""

    def setUp(self):
        self.paper_name = setup_mock_state()
        init_orchestrate_state(self.paper_name)

    def test_phase1_initial(self):
        result = orchestrate_phase1(self.paper_name)
        self.assertTrue(result["ok"])
        self.assertEqual(result["phase"], "phase1")
        self.assertFalse(result["confirmed"])

    def test_confirm_phase1(self):
        result = confirm_phase1(self.paper_name)
        self.assertTrue(result["ok"])
        # Step 11 拍板 #1 强制：confirm_phase1 后不进 phase2，需走 Phase 1.3
        self.assertEqual(result["phase"], "phase1")
        self.assertEqual(result["phase1_3_status"], "pending")

    def test_phase1_already_confirmed(self):
        confirm_phase1(self.paper_name)
        result = orchestrate_phase1(self.paper_name)
        self.assertTrue(result["ok"])
        self.assertTrue(result.get("confirmed", False))


class TestGetNextNode(unittest.TestCase):
    """节点调度测试"""

    def setUp(self):
        self.paper_name = setup_mock_state()
        init_orchestrate_state(self.paper_name)
        confirm_phase1(self.paper_name)

    def test_first_node(self):
        state = load_orchestrate_state(self.paper_name)
        state["current_node_id"] = None
        next_node = get_next_writing_node(self.paper_name, state)
        self.assertIsNotNone(next_node)

    def test_skip_completed(self):
        state = load_orchestrate_state(self.paper_name)
        state["completed_nodes"] = ["1.1"]
        state["current_node_id"] = "1.1"
        next_node = get_next_writing_node(self.paper_name, state)
        self.assertNotEqual(next_node, "1.1")


class TestReviewDecision(unittest.TestCase):
    """评审决策处理测试"""

    def setUp(self):
        self.paper_name = setup_mock_state()
        init_orchestrate_state(self.paper_name)
        confirm_phase1(self.paper_name)
        # Step 11: 走完 Phase 1.3 才能进 phase2（手动跳过以保持原有测试环境）
        from orchestrator_v2 import skip_phase1_3
        skip_phase1_3(self.paper_name)

        # 模拟节点进入待确认
        state = load_orchestrate_state(self.paper_name)
        state["pending_review"].append("1.1")
        save_orchestrate_state(self.paper_name, state)

    def test_continue_decision(self):
        result = handle_review_decision(self.paper_name, "1.1", "continue")
        self.assertTrue(result["ok"])
        self.assertEqual(result["decision"], "continue")
        self.assertIn("1.1", result["next_node_id"] or "")

    def test_skip_decision(self):
        result = handle_review_decision(self.paper_name, "1.1", "skip")
        self.assertTrue(result["ok"])
        self.assertEqual(result["decision"], "skip")

        state = load_orchestrate_state(self.paper_name)
        self.assertIn("1.1", state["failed_nodes"])

    def test_rewrite_decision(self):
        result = handle_review_decision(self.paper_name, "1.1", "rewrite")
        self.assertTrue(result["ok"])
        self.assertEqual(result["decision"], "rewrite")

        state = load_orchestrate_state(self.paper_name)
        self.assertNotIn("1.1", state["pending_review"])
        self.assertNotIn("1.1", state["completed_nodes"])


class TestOrchestrate(unittest.TestCase):
    """主入口测试"""

    def setUp(self):
        self.paper_name = setup_mock_state()
        init_orchestrate_state(self.paper_name)

    def test_auto_phase_detection(self):
        # 初始应为 phase1
        result = orchestrate(self.paper_name)
        self.assertEqual(result["phase"], "phase1")

    def test_explicit_phase(self):
        result = orchestrate(self.paper_name, phase="phase1")
        self.assertTrue(result["ok"])
        self.assertEqual(result["phase"], "phase1")

    def test_phase2_requires_llm(self):
        confirm_phase1(self.paper_name)
        result = orchestrate(self.paper_name, phase="phase2")
        self.assertFalse(result["ok"])
        self.assertIn("llm_func", result["error"])


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print("🏁 开始 Orchestrator V2 测试\n")

    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n============================================================")
    print("测试结果汇总")
    print("============================================================")

    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total - failures - errors

    print(f"  总计: {total}")
    print(f"  ✅ 通过: {passed}")
    if failures:
        print(f"  ❌ 失败: {failures}")
    if errors:
        print(f"  💥 错误: {errors}")

    if failures == 0 and errors == 0:
        print("\n🎉 全部测试通过")
    else:
        print("\n⚠️ 部分测试失败")
        exit(1)
