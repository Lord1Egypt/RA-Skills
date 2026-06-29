#!/usr/bin/env python3
"""
test_run_workflow.py - v2.0.6 真实入口 CLI 回归测试

测试覆盖：
  - P0-1: skip_phase1_3 拦截（入口层 + 函数层）
  - P0-2: run_workflow.py CLI 可启动
  - P0-3: 走 v2.0.4 推荐调用模式（write_single_node + apply_user_decision）
  - P1-1: B-2 幂等修复
  - P1-2: 独立 Reviewer 警告
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR.parent))

WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace"))
TEST_PAPER = "test_run_workflow_v206"


def cleanup():
    """清理测试状态"""
    import shutil
    paper_dir = WORKSPACE / TEST_PAPER
    if paper_dir.exists():
        shutil.rmtree(paper_dir)


def setup_minimal_outline():
    """设置最小 outline（2 节点测试用）"""
    from orchestrator_v2 import orchestrate
    from outline_parser import build_outline_tree

    # 用 text 模式初始化（注意：不能含 markdown # 格式，纯文本）
    outline_text = """第1章 绪论
1.1 研究背景
1.2 研究意义
第2章 理论基础
2.1 战略管理理论
"""
    r = orchestrate(TEST_PAPER, action="phase1_1_init",
                    input_type="text", input_data=outline_text)
    return r


def mock_llm_factory(content="这是 LLM 生成的内容。<key_conclusion>关键结论：测试通过</key_conclusion>"):
    """生成 mock LLM 函数"""
    def mock_llm(prompt: str) -> str:
        return content
    return mock_llm


class TestSkipPhase1_3Enforcement(unittest.TestCase):
    """P0-1: skip_phase1_3 拦截"""

    def setUp(self):
        cleanup()
        setup_minimal_outline()

    def tearDown(self):
        cleanup()

    def test_orchestrate_action_phase1_3_skip_blocked(self):
        """入口层：orchestrate(action='phase1_3_skip') 必须被拦截"""
        from orchestrator_v2 import orchestrate
        r = orchestrate(TEST_PAPER, action="phase1_3_skip")
        self.assertFalse(r["ok"], "v2.0.6 修复后 phase1_3_skip 必须被拦截")
        self.assertIn("拍板 #1", r["error"])
        self.assertEqual(r["blocked_action"], "phase1_3_skip")
        self.assertEqual(r["required_action"], "phase1_3_submit")

    def test_skip_phase1_3_requires_reason(self):
        """函数层：skip_phase1_3() 不传 reason 必须报错"""
        from orchestrator_v2 import skip_phase1_3
        r = skip_phase1_3(TEST_PAPER)
        self.assertFalse(r["ok"])
        self.assertIn("reason", r["error"])

    def test_skip_phase1_3_requires_operator(self):
        """函数层：skip_phase1_3() 不传 operator 必须报错"""
        from orchestrator_v2 import skip_phase1_3
        r = skip_phase1_3(TEST_PAPER, reason="调试")
        self.assertFalse(r["ok"])
        self.assertIn("operator", r["error"])

    def test_skip_phase1_3_with_audit_succeeds(self):
        """函数层：传 reason + operator 成功 + audit log"""
        from orchestrator_v2 import skip_phase1_3
        from state_manager_v2 import load_orchestrate_state
        r = skip_phase1_3(TEST_PAPER, reason="测试", operator="test_run_workflow.py")
        self.assertTrue(r["ok"])
        state = load_orchestrate_state(TEST_PAPER)
        audit = state.get("audit_log", [])
        self.assertGreater(len(audit), 0)
        self.assertEqual(audit[-1]["action"], "phase1_3_skip")

    def test_skip_phase1_3_env_guard(self):
        """函数层：MBA_THESIS_PRODUCTION=1 必须报错"""
        from orchestrator_v2 import skip_phase1_3
        with patch.dict(os.environ, {"MBA_THESIS_PRODUCTION": "1"}):
            r = skip_phase1_3(TEST_PAPER, reason="测试", operator="test")
            self.assertFalse(r["ok"])
            self.assertIn("MBA_THESIS_PRODUCTION", r["error"])


class TestRunWorkflowCLI(unittest.TestCase):
    """P0-2: run_workflow.py CLI"""

    def test_cli_help(self):
        """CLI --help 可用"""
        import subprocess
        r = subprocess.run(
            ["python3", str(SCRIPT_DIR.parent / "run_workflow.py"), "--help"],
            capture_output=True, text=True
        )
        self.assertEqual(r.returncode, 0)
        self.assertIn("thesis-workflow v2", r.stdout)
        self.assertIn("v2.0.6", r.stdout)

    def test_cli_status_no_state(self):
        """CLI --status：状态文件不存在时报错"""
        cleanup()
        import subprocess
        r = subprocess.run(
            ["python3", str(SCRIPT_DIR.parent / "run_workflow.py"),
             TEST_PAPER, "--status"],
            capture_output=True, text=True
        )
        self.assertEqual(r.returncode, 0)
        self.assertIn("状态文件不存在", r.stdout)


class TestB2Idempotent(unittest.TestCase):
    """P1-1: B-2 幂等修复"""

    def setUp(self):
        cleanup()
        setup_minimal_outline()

    def tearDown(self):
        cleanup()

    def test_outline_update_status_idempotent(self):
        """已 completed 节点拒绝覆盖 content（默认）"""
        from state_manager_v2 import outline_update_status, outline_load

        # 先完成一个节点
        outline_update_status(TEST_PAPER, "1.1", "completed",
                            content="原始内容", key_conclusion="原始结论")

        # 再尝试覆盖（应该失败）
        r = outline_update_status(TEST_PAPER, "1.1", "completed",
                                content="覆盖内容", key_conclusion="新结论")
        self.assertFalse(r["ok"], "B-2 修复后必须拒绝覆盖 completed 节点 content")
        self.assertIn("v2.0.6", r["error"])
        self.assertEqual(r["current_status"], "completed")

    def test_outline_update_status_force_overrides(self):
        """force=True 可以强制覆盖（调试用）"""
        from state_manager_v2 import outline_update_status, outline_load

        outline_update_status(TEST_PAPER, "1.1", "completed",
                            content="原始内容", key_conclusion="原始结论")

        # force=True
        r = outline_update_status(TEST_PAPER, "1.1", "completed",
                                content="覆盖内容", key_conclusion="新结论",
                                force=True)
        self.assertTrue(r["ok"], "force=True 应允许覆盖")

    def test_outline_update_status_writing_allows_overwrite(self):
        """writing 状态可以更新 content（写作中）"""
        from state_manager_v2 import outline_update_status

        outline_update_status(TEST_PAPER, "1.1", "writing")
        r = outline_update_status(TEST_PAPER, "1.1", "writing",
                                content="写作中内容")
        self.assertTrue(r["ok"])


class TestIndependentReviewer(unittest.TestCase):
    """P1-2: 独立 Reviewer 警告"""

    def setUp(self):
        cleanup()
        setup_minimal_outline()
        # 跳过 Phase 1.3 让测试可以进 Phase 2
        from orchestrator_v2 import skip_phase1_3
        skip_phase1_3(TEST_PAPER, reason="测试", operator="test_run_workflow.py")

    def tearDown(self):
        cleanup()

    def test_no_reviewer_func_emits_warning(self):
        """不传 reviewer_func 必须发警告"""
        from orchestrator_v2 import write_single_node
        import warnings
        mock = mock_llm_factory()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            r = write_single_node(TEST_PAPER, "1.1", mock, bypass_scarcity=True)
            warning_msgs = [str(warning.message) for warning in w]
            self.assertTrue(any("P1-2" in msg for msg in warning_msgs),
                          f"必须发 P1-2 警告，实际 warnings: {warning_msgs}")

    def test_same_reviewer_llm_emits_warning(self):
        """reviewer_func == llm_func 必须发警告"""
        from orchestrator_v2 import write_single_node
        import warnings
        mock = mock_llm_factory()

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            r = write_single_node(TEST_PAPER, "1.1", mock, reviewer_func=mock, bypass_scarcity=True)
            warning_msgs = [str(warning.message) for warning in w]
            self.assertTrue(any("P1-2" in msg for msg in warning_msgs))

    def test_different_reviewer_no_warning(self):
        """reviewer_func != llm_func 不发警告"""
        from orchestrator_v2 import write_single_node
        import warnings
        mock_writer = mock_llm_factory()
        mock_reviewer = mock_llm_factory('{"quality": "high", "summary": "ok", "weaknesses": [], "suggestions": []}')

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            r = write_single_node(TEST_PAPER, "1.1", mock_writer,
                                reviewer_func=mock_reviewer, bypass_scarcity=True)
            warning_msgs = [str(warning.message) for warning in w]
            self.assertFalse(any("P1-2" in msg for msg in warning_msgs),
                           f"独立 reviewer 不应发 P1-2 警告: {warning_msgs}")


class TestEndToEndWorkflow(unittest.TestCase):
    """端到端：完整流程跑通"""

    def setUp(self):
        cleanup()
        setup_minimal_outline()
        from orchestrator_v2 import skip_phase1_3
        skip_phase1_3(TEST_PAPER, reason="测试", operator="test_run_workflow.py")

    def tearDown(self):
        cleanup()

    def test_v2_recommended_calling_pattern(self):
        """v2.0.4 推荐调用模式：write_single_node + apply_user_decision + bypass_scarcity"""
        from orchestrator_v2 import write_single_node, apply_user_decision
        from state_manager_v2 import load_orchestrate_state

        mock_writer = mock_llm_factory()
        mock_reviewer = mock_llm_factory('{"quality": "high", "summary": "ok", "weaknesses": [], "suggestions": []}')

        # 直接调 write_single_node（已 skip_phase1_3，content_hint 为空可能触发 needs_user_input）
        # 但有 bypass_scarcity=False，先看是否会触发 HIL
        import warnings
        warnings.simplefilter("ignore")  # 忽略 P1-2 警告
        r1 = write_single_node(TEST_PAPER, "1.1", mock_writer,
                            reviewer_func=mock_reviewer, bypass_scarcity=False)

        # info_scarcity 检查可能返回 needs_user_input（因为 skip 后 content_hint 为空）
        if r1.get("action") == "needs_user_input":
            # 走 v2.0.4 推荐路径：apply_user_decision("2") + bypass_scarcity=True
            apply_user_decision(TEST_PAPER, "1.1", "2")
            r2 = write_single_node(TEST_PAPER, "1.1", mock_writer,
                                 reviewer_func=mock_reviewer, bypass_scarcity=True)
            # 应该 completed 或 pending_review
            self.assertIn(r2.get("action"), ["completed", "pending_review"])
        elif r1.get("action") == "completed":
            pass  # OK
        else:
            self.fail(f"意外 action: {r1.get('action')}")


if __name__ == "__main__":
    unittest.main()