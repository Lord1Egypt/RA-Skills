#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_b1_bypass_scarcity.py - 修复 B-1 的回归测试

覆盖：
1. write_single_node(bypass_scarcity=True) 跳过 scarcity 检查
2. write_single_node(bypass_scarcity=False) 正常检查并返回 needs_user_input
3. orchestrate_phase2 收到 needs_user_input action 时单独处理（不进 pending_review）
"""

import os
import sys
import unittest

# 路径修正：本文件 = scripts/tests/test_b1_bypass_scarcity.py
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.dirname(TESTS_DIR)
sys.path.insert(0, SCRIPTS_DIR)
sys.path.insert(0, TESTS_DIR)

from orchestrator_v2 import (
    write_single_node, orchestrate_phase2,
    check_info_scarcity, apply_user_decision,
    load_orchestrate_state, init_orchestrate_state
)
from state_manager_v2 import outline_load, outline_update_status


TEST_PAPER = "test_b1_bypass"


def setup_outline_with_scarcity():
    """构造一个会触发 HIL 的场景：
    - ch1（首章 L1）：content_hint 已填，但 user_hints 空，bridge 空（首章 L1 bridge 允许空）
    - 1.1（章节首 L2）：content_hint 已填，user_hints 空，bridge 空（章节首 L2 bridge 仍检查）
    """
    nodes = [
        {"id": "ch1", "level": 1, "title": "绪论", "parent_id": None,
         "children_ids": ["1.1"], "prev_sibling_id": None, "next_sibling_id": None,
         "writing_status": "pending"},
        {"id": "1.1", "level": 2, "title": "研究背景", "parent_id": "ch1",
         "children_ids": [], "prev_sibling_id": None, "next_sibling_id": None,
         "writing_status": "pending"},
    ]
    # 直接构造 outline_state（用 save_content_hints_to_outline 之类不直接支持节点 status）
    from state_manager_v2 import outline_save
    from outline_parser import insert_chapter_summary_nodes
    outline = {"outline_tree": {"metadata": {"paper_title": "test"}, "nodes": nodes}}
    outline_with_summary = insert_chapter_summary_nodes(outline)
    outline_save(TEST_PAPER, outline_with_summary)

    # 填 content_hint 让某些字段非空
    outline_update_status(TEST_PAPER, "1.1", "pending",
                          content_hint="用户已填的提示文本")


def cleanup():
    """清理测试状态"""
    import shutil
    paper_dir = os.path.join(os.path.expanduser("~/.openclaw/workspace"), TEST_PAPER)
    if os.path.exists(paper_dir):
        shutil.rmtree(paper_dir)


def mock_llm(prompt: str) -> str:
    """Mock LLM：返回带 key_conclusion 标记的最小内容"""
    return """# 章节内容

这是 mock LLM 生成的内容。

## 小结

<key_conclusion>本节论述清晰，结论明确。</key_conclusion>
"""


class TestBypassScarcity(unittest.TestCase):
    """修复 B-1: write_single_node 加 bypass_scarcity 参数"""

    def setUp(self):
        cleanup()
        setup_outline_with_scarcity()

    def tearDown(self):
        cleanup()

    def test_bypass_scarcity_true_skips_check(self):
        """测试 1：bypass_scarcity=True 时跳过 scarcity 检查，直接生成内容"""
        # 1.1 节点：content_hint 填了，但 user_hints 和 bridge 缺失 → scarcity needs_user_input
        sc = check_info_scarcity(TEST_PAPER, "1.1")
        self.assertEqual(sc["action"], "needs_user_input", "前置条件：1.1 应触发 HIL")

        # 调用 write_single_node with bypass_scarcity=True
        result = write_single_node(TEST_PAPER, "1.1", mock_llm, bypass_scarcity=True)
        self.assertTrue(result["ok"])
        # 不应该返回 needs_user_input，应该继续执行（completed 或 pending_review）
        self.assertIn(result["action"], ["completed", "pending_review"],
                      f"bypass_scarcity=True 应跳过检查，但 got action={result['action']}")

        # 节点 content 应被写入
        from state_manager_v2 import outline_get_node
        node = outline_get_node(TEST_PAPER, "1.1")
        self.assertEqual(node.get("writing_status"), "completed")
        self.assertTrue(len(node.get("content", "")) > 0,
                        f"content 应被写入，实际长度={len(node.get('content', ''))}")

    def test_bypass_scarcity_false_returns_needs_user_input(self):
        """测试 2：bypass_scarcity=False（默认）时正常检查，返回 needs_user_input"""
        sc = check_info_scarcity(TEST_PAPER, "1.1")
        self.assertEqual(sc["action"], "needs_user_input", "前置条件：1.1 应触发 HIL")

        result = write_single_node(TEST_PAPER, "1.1", mock_llm, bypass_scarcity=False)
        self.assertTrue(result["ok"])
        self.assertEqual(result["action"], "needs_user_input",
                         f"默认应返回 needs_user_input，但 got {result['action']}")
        self.assertIn("scarcity_info", result)

    def test_apply_user_decision_then_bypass(self):
        """测试 3：apply_user_decision 后 bypass_scarcity=True 能正常写作（B-1 修复主路径）"""
        # 第一次：触发 HIL
        r1 = write_single_node(TEST_PAPER, "1.1", mock_llm)
        self.assertEqual(r1["action"], "needs_user_input")

        # 用户决策 2（AI 自行生成）
        r_dec = apply_user_decision(TEST_PAPER, "1.1", "2")
        self.assertEqual(r_dec["action"], "proceed")

        # 第二次：bypass_scarcity=True → 跳过检查，正常生成
        r2 = write_single_node(TEST_PAPER, "1.1", mock_llm, bypass_scarcity=True)
        self.assertIn(r2["action"], ["completed", "pending_review"],
                      f"决策后 bypass_scarcity=True 应能继续写作，但 got action={r2['action']}")

        # 节点应完成
        from state_manager_v2 import outline_get_node
        node = outline_get_node(TEST_PAPER, "1.1")
        self.assertEqual(node.get("writing_status"), "completed")


class TestOrchestratePhase2HIL(unittest.TestCase):
    """修复 B-1: orchestrate_phase2 处理 needs_user_input action"""

    def setUp(self):
        cleanup()
        setup_outline_with_scarcity()
        init_orchestrate_state(TEST_PAPER)
        # 标记 phase1 + phase1_3 确认（破坏性变更要求）
        state = load_orchestrate_state(TEST_PAPER)
        state["phase1_confirmed"] = True
        state["phase1_3_status"] = "confirmed"
        state["phase"] = "phase2"
        from orchestrator_v2 import save_orchestrate_state
        save_orchestrate_state(TEST_PAPER, state)

    def tearDown(self):
        cleanup()

    def test_orchestrate_phase2_returns_needs_user_input(self):
        """测试 4：orchestrate_phase2 收到 needs_user_input 时单独返回，不进 pending_review"""
        # orchestrate_phase2 调用 write_single_node
        result = orchestrate_phase2(TEST_PAPER, llm_func=mock_llm)

        # 应该返回 needs_user_input action，而不是 wait_for_user
        self.assertTrue(result.get("ok"))
        self.assertEqual(result.get("action"), "needs_user_input",
                         f"应返回 needs_user_input，但 got {result.get('action')}")

        # 检查 pending_review 列表不应该包含 1.1（这是 HIL 不是评审）
        state = load_orchestrate_state(TEST_PAPER)
        self.assertNotIn("1.1", state.get("pending_review", []),
                         "needs_user_input 不应进入 pending_review")

        # completed_nodes 也不应包含 1.1
        self.assertNotIn("1.1", state.get("completed_nodes", []),
                         "1.1 还未真正完成，不应进 completed_nodes")


if __name__ == "__main__":
    unittest.main(verbosity=2)