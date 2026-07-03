"""
Phase Manager - 单元测试
test_phase_manager.py

覆盖 schemas / file_manager / gate_keeper / summary_generator / hil_renderer / PhaseManager
"""

import os
import sys
import json
import tempfile
import shutil
import unittest
from pathlib import Path

# 确保可以 import phase_manager
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from phase_manager import (
    PhaseManager,
    PhaseFileManager,
    PhaseGateKeeper,
    PhaseSummaryGenerator,
    PhaseHILRenderer,
)
from phase_manager.schemas import (
    PhaseSummary,
    GateResult,
    PhaseTransition,
    calculate_content_hash,
    calculate_word_count,
    extract_chapter_count,
    now_iso,
    CONTENT_TYPE_INTEGRATED,
    CONTENT_TYPE_REVIEW,
    CONTENT_TYPE_SUMMARY,
    STATUS_COMPLETED,
    STATUS_MODIFIED,
)


# ============================================================================
# 测试基类
# ============================================================================

class TestBase(unittest.TestCase):
    """测试基类，提供临时工作区"""

    @classmethod
    def setUpClass(cls):
        import time
        cls.paper_name = f"test_paper_{int(time.time())}"
        cls.workspace = tempfile.mkdtemp(prefix="pm_test_")
        cls.pm = PhaseManager(cls.paper_name, cls.workspace)
        cls.fm = cls.pm.fm

    @classmethod
    def tearDownClass(cls):
        # 清理临时目录
        shutil.rmtree(cls.workspace, ignore_errors=True)


# ============================================================================
# schemas 辅助函数测试
# ============================================================================

class TestSchemasHelpers(TestBase):
    """测试 schemas.py 中的辅助函数"""

    def test_calculate_content_hash(self):
        """相同内容产生相同 hash"""
        h1 = calculate_content_hash("hello")
        h2 = calculate_content_hash("hello")
        self.assertEqual(h1, h2)

    def test_calculate_content_hash_different(self):
        """不同内容产生不同 hash"""
        h1 = calculate_content_hash("hello")
        h2 = calculate_content_hash("world")
        self.assertNotEqual(h1, h2)

    def test_calculate_word_count_empty(self):
        self.assertEqual(0, calculate_word_count(""))

    def test_calculate_word_count_chinese(self):
        """中文字符计数"""
        # 5个汉字
        text = "你好世界"
        count = calculate_word_count(text)
        self.assertGreaterEqual(count, 4)  # 简单实现可能计入标点

    def test_calculate_word_count_mixed(self):
        """中英混合计数"""
        text = "Hello世界123"
        count = calculate_word_count(text)
        self.assertGreaterEqual(count, 2)  # 至少中文部分

    def test_extract_chapter_count_empty(self):
        self.assertEqual(0, extract_chapter_count(""))

    def test_extract_chapter_count_single(self):
        """提取单个章节"""
        text = "# 第1章 概述\n\n内容"
        count = extract_chapter_count(text)
        self.assertEqual(1, count)

    def test_extract_chapter_count_multiple(self):
        """提取多个章节"""
        text = """# 第1章 概述
# 第2章 理论
## 第3章 分析
### 第4章 策略
# 第5章 实施
# 第6章 保障
# 第7章 结论
"""
        count = extract_chapter_count(text)
        self.assertEqual(6, count)

    def test_now_iso_format(self):
        """now_iso 返回 ISO 格式"""
        ts = now_iso()
        self.assertIn("T", ts)
        self.assertIn("+08:00", ts)


# ============================================================================
# PhaseFileManager 测试
# ============================================================================

class TestPhaseFileManager(TestBase):
    """测试文件生命周期管理"""

    def test_get_file_path(self):
        """路径计算正确"""
        path = self.fm.get_file_path(3, CONTENT_TYPE_INTEGRATED)
        self.assertIn("_phase3_integrated.md", path)
        # 文件应该在 workspace 目录下
        self.assertTrue(path.startswith(self.workspace))

    def test_get_file_path_review(self):
        path = self.fm.get_file_path(3, CONTENT_TYPE_REVIEW)
        self.assertIn("_phase3_review.json", path)
        self.assertTrue(path.startswith(self.workspace))

    def test_save_and_load_roundtrip(self):
        """保存后读取，内容一致"""
        content = "# 第1章 测试\n\n这是测试内容。"
        result = self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, content)
        self.assertTrue(result["ok"])
        self.assertTrue(result["changed"])

        loaded = self.fm.load_content(3, CONTENT_TYPE_INTEGRATED)
        self.assertEqual(content, loaded)

    def test_save_no_change(self):
        """内容无变化时不创建备份"""
        content = "# 第1章 测试\n\n内容A"
        self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, content)

        # 再次保存相同内容
        result = self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, content)
        self.assertTrue(result["ok"])
        self.assertFalse(result["changed"])
        self.assertIsNone(result["backup_path"])

    def test_backup_on_overwrite(self):
        """覆盖写入时自动备份"""
        content_v1 = "# 第1章 V1\n\n版本1"
        self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, content_v1)

        content_v2 = "# 第1章 V2\n\n版本2"
        result = self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, content_v2)

        self.assertTrue(result["ok"])
        self.assertTrue(result["changed"])
        self.assertIsNotNone(result["backup_path"])
        self.assertTrue(os.path.exists(result["backup_path"]))

        # 验证备份是旧内容
        with open(result["backup_path"], "r", encoding="utf-8") as f:
            backup_content = f.read()
        self.assertEqual(content_v1, backup_content)

    def test_backup_exists(self):
        """检测备份是否存在"""
        content_v1 = "# V1"
        self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, content_v1)

        self.assertFalse(self.fm.backup_exists(3, CONTENT_TYPE_INTEGRATED))

        self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, "# V2")
        self.assertTrue(self.fm.backup_exists(3, CONTENT_TYPE_INTEGRATED))

    def test_restore_backup(self):
        """恢复备份版本"""
        self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, "# V1")
        self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, "# V2")

        restore_result = self.fm.restore_backup(3, CONTENT_TYPE_INTEGRATED)
        self.assertTrue(restore_result["ok"])

        content = self.fm.load_content(3, CONTENT_TYPE_INTEGRATED)
        self.assertEqual("# V1", content)

    def test_freshness_check(self):
        """文件新鲜度检测"""
        self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, "# 测试")

        # 新保存的文件应该是新鲜的
        self.assertTrue(self.fm.is_fresh(3, CONTENT_TYPE_INTEGRATED))

    def test_validate_before_read_missing(self):
        """文件不存在时校验失败"""
        result = self.fm.validate_before_read(99, CONTENT_TYPE_INTEGRATED)
        self.assertFalse(result["ok"])
        self.assertIn("不存在", result["error"])

    def test_save_summary_and_load(self):
        """Summary 文件保存和读取"""
        summary_data = {
            "phase": 3,
            "status": "completed",
            "word_count": 1000,
        }
        self.assertTrue(self.fm.save_summary(3, summary_data))

        loaded = self.fm.load_summary(3)
        self.assertIsNotNone(loaded)
        self.assertEqual(3, loaded["phase"])
        self.assertEqual("completed", loaded["status"])

    def test_save_transition_and_load(self):
        """流转记录保存和读取"""
        transition = {
            "from_phase": 2,
            "to_phase": 3,
            "triggered_by": "user_confirm",
        }
        self.assertTrue(self.fm.save_transition(transition))

        # 验证最新一条记录正确（不依赖总数，因为测试间可能有残留）
        last = self.fm.get_last_transition()
        self.assertEqual(2, last["from_phase"])
        self.assertEqual(3, last["to_phase"])

    def test_get_last_transition(self):
        """获取最近一次流转"""
        self.fm.save_transition({"from_phase": 1, "to_phase": 2, "triggered_by": "auto"})
        self.fm.save_transition({"from_phase": 2, "to_phase": 3, "triggered_by": "user_confirm"})

        last = self.fm.get_last_transition()
        self.assertEqual(3, last["to_phase"])

    def test_cleanup_intermediate(self):
        """清理中间文件"""
        # 创建一些临时文件
        self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, "# 正式文件")
        tmp_path = os.path.join(self.workspace, "_phase3_integrated.md.tmp")
        with open(tmp_path, "w") as f:
            f.write("tmp")

        # 清理
        result = self.fm.cleanup_intermediate(3)
        self.assertTrue(result["ok"])
        self.assertTrue(tmp_path in result["deleted"])

        # 正式文件应该还在
        self.assertIsNotNone(self.fm.load_content(3, CONTENT_TYPE_INTEGRATED))

    def test_concurrent_write_protection(self):
        """并发写入保护（简化测试：锁文件创建）"""
        self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, "# V1")
        # 第二次写入应该成功（因为锁会被释放）
        result = self.fm.save_content(3, CONTENT_TYPE_INTEGRATED, "# V2")
        self.assertTrue(result["ok"])


# ============================================================================
# GateKeeper 测试
# ============================================================================

class TestGateKeeper(TestBase):
    """测试门禁校验"""

    def test_pre_phase_check_phase2_without_phase1(self):
        """Phase 1 未完成时，Phase 2 准入应该失败"""
        gate = self.pm.gk.pre_enter_check(2)
        self.assertFalse(gate.passed)
        self.assertTrue(len(gate.blocking_issues) > 0)

    def test_pre_phase_check_unknown_phase(self):
        """未知 Phase 的准入检查"""
        gate = self.pm.gk.pre_enter_check(99)
        self.assertFalse(gate.passed)


# ============================================================================
# SummaryGenerator 测试
# ============================================================================

class TestSummaryGenerator(TestBase):
    """测试摘要生成"""

    def test_generate_phase_summary(self):
        """生成 PhaseSummary"""
        # 使用真实的多章节内容（7章）
        content = """# 第1章 概述

本文研究...。

# 第2章 理论

理论背景...

# 第3章 分析

分析内容...

# 第4章 战略

战略选择...

# 第5章 实施

实施计划...

# 第6章 保障

保障措施...

# 第7章 结论

研究结论...
"""
        result = self.pm.sg.generate_phase_summary(
            phase=3,
            file_content=content,
            status=STATUS_COMPLETED,
        )

        self.assertIsInstance(result, PhaseSummary)
        self.assertEqual(3, result.phase)
        self.assertEqual(STATUS_COMPLETED, result.status)
        self.assertGreater(result.word_count, 0)
        self.assertEqual(7, result.chapter_count)

    def test_generate_phase_summary_from_file(self):
        """从已保存的文件生成 summary"""
        self.pm.save_phase_output(3, CONTENT_TYPE_INTEGRATED, "# 测试内容" * 50)

        summary = self.pm.sg.get_summary(3)
        self.assertIsNotNone(summary)
        self.assertEqual(3, summary.phase)

    def test_key_metrics_phase2(self):
        """Phase 2 的 key_metrics"""
        content = "# 论文\n" + "内容\n" * 100
        summary = self.pm.sg.generate_phase_summary(
            phase=2,
            phase_result={"nodes": {"1.1": {"status": "completed"}, "1.2": {"status": "completed"}}},
            file_content=content,
        )

        metrics = summary.key_metrics
        self.assertIn("nodes_total", metrics)
        self.assertIn("nodes_completed", metrics)

    def test_key_metrics_phase3(self):
        """Phase 3 的 key_metrics"""
        content = "# 论文\n" + "内容\n" * 100
        review_data = {"summary": {"p0_issues": 0, "p1_issues": 2, "guardrails_passed": True}}

        summary = self.pm.sg.generate_phase_summary(
            phase=3,
            phase_result={"review_report": review_data},
            file_content=content,
        )

        metrics = summary.key_metrics
        self.assertEqual(0, metrics["p0_issues"])
        self.assertEqual(2, metrics["p1_issues"])


# ============================================================================
# HILRenderer 测试
# ============================================================================

class TestHILRenderer(TestBase):
    """测试 HIL 消息渲染"""

    def test_render_hil_message_basic(self):
        """基本 HIL 消息渲染"""
        self.pm.save_phase_output(3, CONTENT_TYPE_INTEGRATED, "# 测试\n" * 50)

        summary = self.pm.sg.get_summary(3)
        msg = self.pm.hr.render_hil_message(phase=3, summary=summary, next_phase=4)

        self.assertIn("整合", msg)  # PHASE_NAMES[3] = "整合"
        self.assertIn("文件", msg)  # 包含文件路径提示
        self.assertNotIn("# 第1章", msg)  # 不应该包含正文

    def test_render_hil_message_no_summary(self):
        """无 summary 时的消息"""
        # 用一个不存在的 phase，会走到 else 分支
        msg = self.pm.hr.render_hil_message(phase=3, summary=None)
        self.assertIn("文件", msg)  # 应该提示文件路径

    def test_render_gate_failure(self):
        """门禁失败消息"""
        gate = GateResult(passed=False, phase=3, checks={})
        gate.add_blocking_issue("字数不足")
        gate.add_blocking_issue("章节不全")

        msg = self.pm.hr.render_gate_failure(3, gate)
        self.assertIn("门禁未通过", msg)
        self.assertIn("字数不足", msg)

    def test_render_all_phases_status(self):
        """所有 Phase 状态渲染"""
        msg = self.pm.hr.render_all_phases_status()
        self.assertIn("进度总览", msg)
        self.assertIn("Phase 1", msg)

    def test_render_user_modification_warning(self):
        """用户修改警告"""
        msg = self.pm.hr.render_user_modification_warning(
            phase=3,
            old_hash="abc123",
            new_hash="def456",
        )
        self.assertIn("修改", msg)
        self.assertIn("abc123", msg)


# ============================================================================
# PhaseManager Facade 测试
# ============================================================================

class TestPhaseManager(TestBase):
    """测试 PhaseManager Facade"""

    def test_save_and_load_integrated(self):
        """save_integrated / load_integrated 往返"""
        content = "# 第1章 测试\n\n测试内容"
        save_result = self.pm.save_integrated(3, content)
        self.assertTrue(save_result["ok"])

        loaded = self.pm.load_integrated(3)
        self.assertEqual(content, loaded)

    def test_save_and_load_review(self):
        """save_review / load_review 往返"""
        review_data = {
            "summary": {"p0_issues": 0, "p1_issues": 1},
            "details": [{"node": "1.1", "issue": "格式不规范"}],
        }
        save_result = self.pm.save_review(3, review_data)
        self.assertTrue(save_result["ok"])

        loaded = self.pm.load_review(3)
        self.assertIsNotNone(loaded)
        self.assertEqual(0, loaded["summary"]["p0_issues"])

    def test_save_phase_output_returns_summary(self):
        """save_phase_output 返回 PhaseSummary"""
        result = self.pm.save_phase_output(
            phase=3,
            content_type=CONTENT_TYPE_INTEGRATED,
            content="# 测试",
        )
        self.assertTrue(result["ok"])
        self.assertIsInstance(result["summary"], PhaseSummary)

    def test_generate_hil_message_integration(self):
        """生成 HIL 消息（集成测试）"""
        # 保存内容
        self.pm.save_integrated(3, "# 测试内容\n" * 50)

        # 生成 HIL
        msg = self.pm.generate_hil_message(phase=3, next_phase=4)
        self.assertIsInstance(msg, str)
        self.assertGreater(len(msg), 50)
        self.assertIn("文件", msg)

    def test_pre_phase_check_integration(self):
        """门禁检查（集成测试）"""
        # Phase 1 未完成时，Phase 2 应该被拦截
        gate = self.pm.pre_phase_check(2)
        self.assertFalse(gate.passed)

    def test_get_phase_status(self):
        """获取 Phase 状态"""
        status = self.pm.get_phase_status(3)
        self.assertIn("exists", status)
        self.assertIn("status", status)
        # 初始时可能存在 summary 文件（如果 workspace 复用）

        # 保存后再查
        self.pm.save_integrated(3, "# 测试")
        status = self.pm.get_phase_status(3)
        self.assertTrue(status["exists"])

    def test_get_all_phase_status(self):
        """获取所有 Phase 状态"""
        statuses = self.pm.get_all_phase_status()
        self.assertEqual(6, len(statuses))  # Phase 1-5 + 3.5

    def test_record_transition(self):
        """记录流转"""
        result = self.pm.record_transition(
            from_phase=2,
            to_phase=3,
            triggered_by="user_confirm",
        )
        self.assertTrue(result["ok"])

        last = self.pm.get_last_transition()
        self.assertEqual(2, last["from_phase"])
        self.assertEqual(3, last["to_phase"])

    def test_check_user_modification_no_change(self):
        """检测用户修改（无修改）"""
        self.pm.save_integrated(3, "# V1")
        modified = self.pm.check_user_modification(3)
        self.assertFalse(modified)

    def test_check_user_modification_with_change(self):
        """检测用户修改（有修改）"""
        self.pm.save_integrated(3, "# V1")

        # 模拟用户修改文件
        file_path = self.pm.fm.get_file_path(3, CONTENT_TYPE_INTEGRATED)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# V2 修改后")

        modified = self.pm.check_user_modification(3)
        self.assertTrue(modified)

    def test_update_summary_after_modification(self):
        """用户修改后更新 summary"""
        self.pm.save_integrated(3, "# 原始内容")

        # 用户修改
        file_path = self.pm.fm.get_file_path(3, CONTENT_TYPE_INTEGRATED)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# 修改后内容")

        # 更新 summary
        new_summary = self.pm.update_summary_after_modification(3)
        self.assertIsNotNone(new_summary)
        self.assertEqual(STATUS_MODIFIED, new_summary.status)

    def test_cleanup_phase(self):
        """清理 Phase 中间文件"""
        self.pm.save_integrated(3, "# 正式")
        tmp_path = os.path.join(self.workspace, "_phase3_integrated.md.tmp")
        with open(tmp_path, "w") as f:
            f.write("temp")

        result = self.pm.cleanup_phase(3)
        self.assertTrue(result["ok"])
        self.assertTrue(tmp_path in result["deleted"])

    def test_restore_backup_facade(self):
        """通过 Facade 恢复备份"""
        self.pm.save_integrated(3, "# V1")
        self.pm.save_integrated(3, "# V2")

        result = self.pm.restore_backup(3)
        self.assertTrue(result["ok"])

        content = self.pm.load_integrated(3)
        self.assertEqual("# V1", content)


# ============================================================================
# 运行测试
# ============================================================================

if __name__ == "__main__":
    unittest.main(verbosity=2)