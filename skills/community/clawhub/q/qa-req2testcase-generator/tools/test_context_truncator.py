#!/usr/bin/env python3
"""
context_truncator.py 单元测试

覆盖范围：
  1. TokenCounter: 文本/JSON/字段token计数
  2. TruncationExecutor: 各优先级字段截断逻辑
  3. ContextTruncator: 单点截断、批量截断、预算估算
  4. TruncationReportFormatter: 报告格式化
  5. 集成测试: 大批量模拟数据截断

覆盖率目标: ≥80%
"""

import json
import math
import sys
import os
import unittest
from copy import deepcopy

# 将当前目录加入路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from context_truncator import (
    TokenCounter,
    TruncationExecutor,
    ContextTruncator,
    TruncationReportFormatter,
    FIELD_PRIORITY,
    MODEL_CONTEXT_WINDOWS,
    TRUNCATION_STRATEGIES,
    smart_truncate_for_batch,
)


# ============================================================
# 辅助函数：生成模拟测试点
# ============================================================

def make_test_point(
    tp_id="TP-001",
    title="测试点标题",
    description="这是一个测试点的描述",
    has_operations=True,
    has_exception=True,
    has_ui=True,
    num_operations=6,
    num_exceptions=5,
    num_fields=3,
) -> dict:
    """生成模拟的P5测试点"""
    tp = {
        "id": tp_id,
        "title": title,
        "description": description,
        "category": "main_flow",
        "priority": "P0",
        "priority_reason": "核心业务流程",
        "is_smoke_candidate": True,
        "status": "active",
        "page_path": {
            "full_path": "首页 → 营销管理 → 协同分润 → 债券投顾",
            "hierarchy": ["首页", "营销管理", "协同分润", "债券投顾"],
            "entry_method": "菜单导航",
            "url_pattern": "/marketing/cooperative-sharing/bond-advisor",
            "source": "PRD §3.1",
        },
    }

    if has_operations:
        ops = []
        for i in range(1, num_operations + 1):
            ops.append({
                "step": i,
                "action_type": "click" if i % 2 == 0 else "input",
                "description": f"第{i}步操作描述：执行某个具体操作",
                "target_element": f"目标元素{i}",
                "data_value": f"测试值{i}",
                "expected_anchor": f"第{i}步的预期结果：显示具体UI状态变化",
            })
        tp["operations_chain"] = ops

    if has_ui:
        tp["ui_elements"] = {
            "buttons": [
                {"name": "新增分润", "location": "页面右上角", "style": "primary"},
                {"name": "提交审批", "location": "弹窗底部", "style": "primary"},
                {"name": "暂存", "location": "弹窗底部", "style": "default"},
            ],
            "inputs": [
                {"name": "创收比例(%)", "type": "number_input", "required": True},
                {"name": "分润说明", "type": "text_input", "required": False, "max_length": 200},
            ],
            "selectors": [
                {"name": "协办单位", "type": "dropdown", "required": True},
            ],
            "popups": [
                {"name": "分润申请弹窗", "type": "modal", "trigger": "点击新增分润"},
            ],
            "lists": [
                {"name": "分润列表", "columns": ["协办单位", "创收比例", "状态"]},
            ],
            "messages": [
                {"name": "提交成功提示", "type": "toast", "color": "green"},
            ],
        }

    tp["field_specs"] = []
    for i in range(1, num_fields + 1):
        tp["field_specs"].append({
            "field_name": f"字段{i}",
            "field_type": "text" if i % 2 == 0 else "number",
            "required": i == 1,
            "validation_rules": [f"规则{i}-1", f"规则{i}-2"],
        })

    tp["business_rules"] = [
        {"rule_id": "BR-001", "rule_name": "必填校验", "description": "必填字段不能为空",
         "violation_behavior": "红色边框+错误提示"},
        {"rule_id": "BR-002", "rule_name": "范围校验", "description": "数值在0-100之间",
         "violation_behavior": "输入框红色边框"},
    ]

    if has_exception:
        tp["exception_scenarios"] = []
        for i in range(1, num_exceptions + 1):
            tp["exception_scenarios"].append({
                "scenario_id": f"EX-{i:03d}",
                "type": "invalid_value",
                "description": f"异常场景{i}的描述，包含详细的预期行为说明",
                "expected_behavior": f"系统应拦截并提示具体错误信息{i}",
                "pci_ref": f"PCI-{i:03d}",
                "pci_status": "已确认",
            })

    tp["precondition"] = {
        "account": {
            "role": "营销管理员",
            "account_id": "test_mkt01",
            "permissions": ["查看", "发起"],
            "status": "正常启用",
        },
        "data_preparation": [
            "预置1条分润记录",
            "协办单位「测试证券」已存在",
        ],
        "environment": {
            "system": "CRM系统",
            "module": "协同分润",
            "browser": "Chrome最新版",
        },
    }

    tp["requirement_completeness"] = {
        "D1_page_path": {"status": "clear", "score": 5},
        "D2_field_specs": {"status": "partial", "score": 3},
        "D3_business_flow": {"status": "partial", "score": 3},
        "D4_exception_handling": {"status": "missing", "score": 1},
        "D5_data_specs": {"status": "partial", "score": 3},
        "overall_level": "L1",
    }

    tp["related_roles"] = ["营销管理员", "审批人"]
    tp["related_rules"] = ["BR-001", "BR-002"]
    tp["source_scenario"] = "REQ-001-M01-F01-S01"
    tp["field_target"] = {}
    tp["test_data_matrix"] = []
    tp["meta"] = {
        "p5_model": "kimi-k2.5",
        "p5_generated_at": "2026-05-15T14:30:00+08:00",
    }

    return tp


def make_large_test_point(tp_id="TP-LARGE", num_exceptions=20, num_operations=15) -> dict:
    """生成大型测试点（模拟信息密集的需求）"""
    return make_test_point(
        tp_id=tp_id,
        title="大型测试点-包含大量异常场景和操作步骤",
        description="这是一个模拟大型需求的测试点，包含大量异常场景、操作步骤、UI元素和字段规格。"
                    "主要验证动态截断策略在高信息密度场景下的表现。",
        num_exceptions=num_exceptions,
        num_operations=num_operations,
        num_fields=8,
    )


# ============================================================
# TokenCounter 测试
# ============================================================

class TestTokenCounter(unittest.TestCase):
    """Token计数器测试"""

    def test_empty_text(self):
        """空文本token数为0"""
        self.assertEqual(TokenCounter.count_text(""), 0)
        self.assertEqual(TokenCounter.count_text(None), 0)

    def test_chinese_text(self):
        """中文文本token计数"""
        # "测试用例" = 4个中文字符 × 1.5 = 6 tokens
        result = TokenCounter.count_text("测试用例")
        self.assertGreater(result, 0)
        # 估算范围：4-8 tokens
        self.assertLessEqual(result, 10)

    def test_english_text(self):
        """英文文本token计数"""
        result = TokenCounter.count_text("hello world test")
        self.assertGreater(result, 0)
        # 3个英文单词 × 1.3 ≈ 4
        self.assertLessEqual(result, 8)

    def test_mixed_text(self):
        """中英混合文本"""
        text = "验证新增分润组Submit按钮的功能"
        result = TokenCounter.count_text(text)
        self.assertGreater(result, 5)

    def test_json_string(self):
        """JSON字符串token计数"""
        json_str = '{"id": "TP-001", "title": "测试点"}'
        result = TokenCounter.count_text(json_str)
        self.assertGreater(result, 5)

    def test_count_json_dict(self):
        """JSON对象token计数"""
        obj = {"id": "TP-001", "name": "测试"}
        result = TokenCounter.count_json(obj)
        self.assertGreater(result, 3)

    def test_count_json_list(self):
        """JSON列表token计数"""
        obj = [1, 2, 3, "测试"]
        result = TokenCounter.count_json(obj)
        self.assertGreater(result, 2)

    def test_count_json_none(self):
        """None值token数为0"""
        self.assertEqual(TokenCounter.count_json(None), 0)

    def test_count_json_number(self):
        """数字token计数"""
        self.assertGreater(TokenCounter.count_json(42), 0)
        self.assertGreater(TokenCounter.count_json(3.14), 0)

    def test_count_field(self):
        """字段token计数（含字段名开销）"""
        result = TokenCounter.count_field("title", "测试点标题")
        self.assertGreater(result, 3)

    def test_count_test_point(self):
        """完整测试点token计数"""
        tp = make_test_point()
        result = TokenCounter.count_test_point(tp)
        self.assertIn("__total__", result)
        self.assertGreater(result["__total__"], 50)
        # 每个字段都应该有计数
        for key in ["id", "title", "description"]:
            self.assertIn(key, result)
            self.assertGreater(result[key], 0)

    def test_larger_text_more_tokens(self):
        """更长的文本应有更多tokens"""
        short = TokenCounter.count_text("短文本")
        long = TokenCounter.count_text("这是一个很长的测试文本，包含多个中文字符和English words混合的内容")
        self.assertGreater(long, short)

    def test_count_text_deterministic(self):
        """相同文本多次计数结果一致"""
        text = "验证测试点的token计数稳定性"
        r1 = TokenCounter.count_text(text)
        r2 = TokenCounter.count_text(text)
        self.assertEqual(r1, r2)


# ============================================================
# TruncationExecutor 测试
# ============================================================

class TestTruncationExecutor(unittest.TestCase):
    """截断执行器测试"""

    def setUp(self):
        self.executor = TruncationExecutor()

    def test_p0_field_not_truncated(self):
        """P0字段不截断"""
        value, log = self.executor.truncate_field("id", "TP-001", "P0")
        self.assertEqual(value, "TP-001")
        self.assertEqual(log["action"], "kept")

    def test_p1_field_not_truncated(self):
        """P1字段不截断"""
        value, log = self.executor.truncate_field("page_path", {"full_path": "A→B"}, "P1")
        self.assertEqual(value, {"full_path": "A→B"})
        self.assertEqual(log["action"], "kept")

    def test_p3_field_fully_truncated(self):
        """P3字段完全截断"""
        original = [{"scenario": "异常1"}, {"scenario": "异常2"}]
        value, log = self.executor.truncate_field("exception_scenarios", original, "P3")
        self.assertEqual(value, "[已截断-详见完整P5输出]")
        self.assertEqual(log["action"], "replaced")
        self.assertLess(log["truncated_tokens"], log["original_tokens"])

    def test_p2_list_truncated(self):
        """P2列表字段截断到前N项"""
        original = ["规则1", "规则2", "规则3", "规则4"]
        value, log = self.executor.truncate_field("related_rules", original, "P2")
        # 默认保留1项 + 占位符
        self.assertEqual(len(value), 2)  # 1项 + 1个占位符
        self.assertEqual(log["action"], "list_truncated")

    def test_p2_short_list_not_truncated(self):
        """P2短列表不截断"""
        original = ["规则1"]
        value, log = self.executor.truncate_field("related_rules", original, "P2")
        self.assertEqual(value, original)
        self.assertEqual(log["action"], "kept")

    def test_p2_long_text_truncated(self):
        """P2长文本截断"""
        original = "A" * 200
        value, log = self.executor.truncate_field("priority_reason", original, "P2")
        self.assertIn("已截断", value)
        self.assertLess(len(value), len(original))

    def test_p2_short_text_not_truncated(self):
        """P2短文本不截断"""
        original = "核心业务流程"
        value, log = self.executor.truncate_field("priority_reason", original, "P2")
        self.assertEqual(value, original)

    def test_p2_empty_not_truncated(self):
        """空值不截断"""
        for empty_val in [None, "", [], {}]:
            value, log = self.executor.truncate_field("test", empty_val, "P2")
            self.assertEqual(log["action"], "kept")

    def test_p2_dict_compacted(self):
        """P2字典类型压缩"""
        original = {
            "short": "abc",
            "long_field": "A" * 100,
            "long_list": [1, 2, 3, 4, 5],
        }
        value, log = self.executor.truncate_field("test_dict", original, "P2")
        self.assertIsInstance(value, dict)
        self.assertEqual(log["action"], "dict_compacted")

    def test_p2_basic_type_not_truncated(self):
        """P2基础类型（bool/int/float）不截断"""
        for val in [True, 42, 3.14]:
            value, log = self.executor.truncate_field("test", val, "P2")
            self.assertEqual(value, val)

    def test_unknown_priority_not_truncated(self):
        """未知优先级不截断"""
        value, log = self.executor.truncate_field("custom_field", "value", "P99")
        self.assertEqual(value, "value")

    def test_log_has_required_fields(self):
        """截断日志包含必要字段"""
        _, log = self.executor.truncate_field("exception_scenarios", [1, 2, 3], "P3")
        for key in ["field", "priority", "original_type", "action", "original_tokens", "truncated_tokens"]:
            self.assertIn(key, log)


# ============================================================
# ContextTruncator 测试
# ============================================================

class TestContextTruncator(unittest.TestCase):
    """核心截断器测试"""

    def test_default_config(self):
        """默认配置初始化"""
        truncator = ContextTruncator()
        self.assertEqual(truncator.context_window, MODEL_CONTEXT_WINDOWS["default"])
        self.assertGreater(truncator.available_budget, 0)

    def test_custom_config(self):
        """自定义配置初始化"""
        truncator = ContextTruncator(
            model_context_window=64000,
            reserved_for_system=2000,
            reserved_for_output=4000,
            safety_margin=0.9,
        )
        self.assertEqual(truncator.context_window, 64000)
        expected = int((64000 - 2000 - 4000) * 0.9)
        self.assertEqual(truncator.available_budget, expected)

    def test_model_name_lookup(self):
        """通过模型名自动选择窗口大小"""
        for model_name, expected_window in MODEL_CONTEXT_WINDOWS.items():
            if model_name == "default":
                continue
            truncator = ContextTruncator(model_name=model_name)
            self.assertEqual(truncator.context_window, expected_window,
                             f"模型{model_name}窗口大小不匹配")

    def test_available_budget_calculation(self):
        """可用预算计算正确"""
        truncator = ContextTruncator(model_context_window=100000)
        # (100000 - 4000 - 8000) * 0.85 = 75060
        expected = int(88000 * 0.85)
        self.assertEqual(truncator.available_budget, expected)

    def test_no_truncation_needed(self):
        """测试点不需要截断"""
        truncator = ContextTruncator(model_context_window=128000)
        # 简单测试点，远小于预算
        tp = {"id": "TP-001", "title": "简单测试点", "description": "描述"}
        result, log = truncator.truncate_test_point(tp)
        self.assertFalse(log["truncation_needed"])
        self.assertEqual(result, tp)

    def test_truncation_reduces_tokens(self):
        """截断后token数减少"""
        truncator = ContextTruncator(model_context_window=128000)
        # 设置极低的目标预算强制截断
        tp = make_test_point(has_exception=True, num_exceptions=10)
        result, log = truncator.truncate_test_point(tp, target_budget=200)
        self.assertTrue(log["truncation_needed"])
        self.assertLessEqual(log["final_tokens"], log["original_tokens"])
        self.assertGreater(log["tokens_saved"], 0)

    def test_p3_truncated_before_p2(self):
        """P3字段在P2之前被截断"""
        truncator = ContextTruncator(model_context_window=128000)
        tp = make_test_point(has_exception=True, num_exceptions=10, has_ui=True)
        _, log = truncator.truncate_test_point(tp, target_budget=500)

        # 检查截断顺序：P3应比P2先被截断
        truncated_fields = log["fields_affected"]
        p3_fields = [f for f in truncated_fields
                     if FIELD_PRIORITY.get(f, {}).get("level") == "P3"]
        p2_fields = [f for f in truncated_fields
                     if FIELD_PRIORITY.get(f, {}).get("level") == "P2"]

        # 如果P2被截断了，P3应该也被截断了
        if p2_fields:
            self.assertTrue(len(p3_fields) > 0,
                            "P2被截断但P3没有被截断，优先级顺序错误")

    def test_p0_p1_never_truncated(self):
        """P0和P1字段永不截断"""
        truncator = ContextTruncator(model_context_window=128000)
        tp = make_test_point()
        # 设置极低预算
        result, _ = truncator.truncate_test_point(tp, target_budget=100)

        # P0/P1字段应保留
        p0_p1_fields = [f for f, info in FIELD_PRIORITY.items()
                        if info["level"] in ("P0", "P1")]
        for field in p0_p1_fields:
            if field in tp:
                self.assertIn(field, result,
                              f"P0/P1字段 {field} 被错误移除")

    def test_original_not_modified(self):
        """截断不修改原始数据"""
        truncator = ContextTruncator(model_context_window=128000)
        tp = make_test_point()
        original_copy = deepcopy(tp)
        truncator.truncate_test_point(tp, target_budget=200)
        self.assertEqual(tp, original_copy, "原始数据被修改")

    def test_batch_truncation(self):
        """批量截断功能"""
        truncator = ContextTruncator(model_context_window=128000)
        tps = [make_test_point(tp_id=f"TP-{i:03d}") for i in range(5)]
        results, batch_log = truncator.truncate_batch(tps)

        self.assertEqual(len(results), 5)
        self.assertEqual(batch_log["total_points"], 5)
        self.assertIn("truncated_count", batch_log)
        self.assertIn("total_tokens_saved", batch_log)

    def test_batch_dynamic_budget_adjustment(self):
        """批量截断动态预算调整"""
        truncator = ContextTruncator(model_context_window=128000)
        # 创建5个大小不同的测试点
        tps = [
            make_test_point(tp_id=f"TP-{i}", num_exceptions=i * 3)
            for i in range(1, 6)
        ]
        results, batch_log = truncator.truncate_batch(tps)
        self.assertEqual(len(results), 5)

    def test_empty_batch(self):
        """空列表处理"""
        truncator = ContextTruncator()
        results, log = truncator.truncate_batch([])
        self.assertEqual(results, [])
        self.assertIn("error", log)

    def test_estimate_batch_tokens(self):
        """批量token估算"""
        truncator = ContextTruncator(model_context_window=128000)
        tps = [make_test_point(tp_id=f"TP-{i}") for i in range(3)]
        estimate = truncator.estimate_batch_tokens(tps)

        self.assertGreater(estimate["total_tokens"], 0)
        self.assertIn("per_field_avg", estimate)
        self.assertIn("priority_distribution", estimate)
        self.assertIn("recommended_batch_size", estimate)
        self.assertGreater(estimate["recommended_batch_size"], 0)

    def test_estimate_empty_batch(self):
        """空批量估算"""
        truncator = ContextTruncator()
        estimate = truncator.estimate_batch_tokens([])
        self.assertEqual(estimate["total_tokens"], 0)

    def test_stats_tracking(self):
        """截断统计跟踪"""
        truncator = ContextTruncator()
        tp = make_test_point()
        truncator.truncate_test_point(tp, target_budget=200)
        stats = truncator.get_truncation_stats()
        self.assertIn("total_truncations", stats)
        self.assertIn("tokens_saved", stats)

    def test_reset_stats(self):
        """重置统计"""
        truncator = ContextTruncator()
        tp = make_test_point()
        truncator.truncate_test_point(tp, target_budget=200)
        truncator.reset_stats()
        stats = truncator.get_truncation_stats()
        self.assertEqual(stats["total_truncations"], 0)


# ============================================================
# TruncationReportFormatter 测试
# ============================================================

class TestTruncationReportFormatter(unittest.TestCase):
    """报告格式化测试"""

    def test_format_point_log_no_truncation(self):
        """无需截断的日志格式化"""
        log = {
            "tp_id": "TP-001",
            "original_tokens": 100,
            "target_budget": 200,
            "final_tokens": 100,
            "tokens_saved": 0,
            "truncation_needed": False,
            "fields_affected": [],
            "truncation_steps": [],
        }
        report = TruncationReportFormatter.format_point_log(log)
        self.assertIn("TP-001", report)
        self.assertIn("无需截断", report)

    def test_format_point_log_with_truncation(self):
        """有截断的日志格式化"""
        log = {
            "tp_id": "TP-002",
            "original_tokens": 500,
            "target_budget": 200,
            "final_tokens": 180,
            "tokens_saved": 320,
            "truncation_needed": True,
            "fields_affected": ["exception_scenarios", "ui_elements"],
            "truncation_steps": [
                {
                    "field": "exception_scenarios",
                    "priority": "P3",
                    "action": "replaced",
                    "reason": "P3字段完全截断",
                    "original_tokens": 200,
                    "truncated_tokens": 10,
                },
            ],
        }
        report = TruncationReportFormatter.format_point_log(log)
        self.assertIn("TP-002", report)
        self.assertIn("exception_scenarios", report)
        self.assertIn("已截断", report)

    def test_format_batch_log(self):
        """批量日志格式化"""
        batch_log = {
            "total_points": 10,
            "per_point_budget": 1000,
            "truncated_count": 3,
            "total_tokens_saved": 1500,
            "summary": {
                "fields_truncated_count": {
                    "exception_scenarios": 3,
                    "ui_elements": 2,
                },
                "by_priority": {
                    "P3": {"count": 5, "tokens_saved": 1200},
                },
            },
            "point_logs": [],
        }
        report = TruncationReportFormatter.format_batch_log(batch_log)
        self.assertIn("10", report)
        self.assertIn("exception_scenarios", report)

    def test_format_estimate(self):
        """估算报告格式化"""
        estimate = {
            "total_tokens": 50000,
            "context_window": 128000,
            "available_budget": 98600,
            "utilization": 50.7,
            "fits_in_context": True,
            "recommended_batch_size": 25,
            "priority_distribution": {
                "P0": {"tokens": 5000, "percentage": 10.0},
                "P1": {"tokens": 20000, "percentage": 40.0},
                "P2": {"tokens": 15000, "percentage": 30.0},
                "P3": {"tokens": 10000, "percentage": 20.0},
            },
        }
        report = TruncationReportFormatter.format_estimate(estimate)
        self.assertIn("50000", report)
        self.assertIn("P0", report)


# ============================================================
# 集成测试：大批量模拟数据
# ============================================================

class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_100_test_points_truncation(self):
        """100条测试点大批量截断"""
        truncator = ContextTruncator(model_context_window=128000)
        tps = [
            make_test_point(
                tp_id=f"TP-{i:03d}",
                num_exceptions=3 + (i % 5),
                num_operations=4 + (i % 3),
            )
            for i in range(100)
        ]

        # 估算
        estimate = truncator.estimate_batch_tokens(tps)
        self.assertGreater(estimate["total_tokens"], 0)

        # 批量截断
        results, batch_log = truncator.truncate_batch(tps)

        self.assertEqual(len(results), 100)
        self.assertEqual(batch_log["total_points"], 100)

        # 所有结果应为dict
        for result in results:
            self.assertIsInstance(result, dict)
            # P0字段不应被移除
            self.assertIn("id", result)

    def test_large_test_point_truncation(self):
        """大型测试点（高信息密度）截断"""
        truncator = ContextTruncator(model_context_window=128000)
        tp = make_large_test_point(num_exceptions=30, num_operations=20)

        # 估算
        estimate = truncator.estimate_batch_tokens([tp])
        original_tokens = estimate["total_tokens"]

        # 设置较低预算强制截断
        result, log = truncator.truncate_test_point(tp, target_budget=1000)

        self.assertTrue(log["truncation_needed"])
        self.assertLess(log["final_tokens"], original_tokens)
        self.assertGreater(log["tokens_saved"], 0)

        # 核心字段仍存在
        self.assertIn("id", result)
        self.assertIn("title", result)

    def test_smart_truncate_convenience_function(self):
        """便捷函数测试"""
        tps = [make_test_point(tp_id=f"TP-{i}") for i in range(5)]
        results, report = smart_truncate_for_batch(
            tps, model_name="deepseek-v4-pro"
        )
        self.assertEqual(len(results), 5)
        self.assertIn("Token估算报告", report)

    def test_overflow_scenario(self):
        """上下文溢出场景模拟"""
        # 模拟小窗口模型
        truncator = ContextTruncator(
            model_context_window=8000,  # 极小窗口
            reserved_for_system=2000,
            reserved_for_output=2000,
        )
        tp = make_test_point(num_exceptions=10, num_operations=8)

        # 估算应该显示不fit
        estimate = truncator.estimate_batch_tokens([tp])
        # 即使不溢出，截断也应正常工作
        result, log = truncator.truncate_test_point(tp)
        self.assertIsInstance(result, dict)

    def test_priority_distribution_correct(self):
        """优先级Token分布正确"""
        truncator = ContextTruncator()
        tp = make_test_point()
        estimate = truncator.estimate_batch_tokens([tp])
        dist = estimate.get("priority_distribution", {})

        # 应包含所有存在的优先级
        for level in ["P0", "P1", "P2", "P3"]:
            if level in dist:
                self.assertIn("tokens", dist[level])
                self.assertIn("percentage", dist[level])
                self.assertGreater(dist[level]["tokens"], 0)

    def test_multiple_truncations_accumulate_stats(self):
        """多次截断累积统计"""
        truncator = ContextTruncator()
        for i in range(5):
            tp = make_test_point(tp_id=f"TP-{i}", num_exceptions=5)
            truncator.truncate_test_point(tp, target_budget=300)

        stats = truncator.get_truncation_stats()
        self.assertGreater(stats["total_truncations"], 0)


# ============================================================
# 边界测试
# ============================================================

class TestEdgeCases(unittest.TestCase):
    """边界情况测试"""

    def test_zero_budget(self):
        """零预算处理"""
        truncator = ContextTruncator(model_context_window=128000)
        tp = {"id": "TP-001", "title": "测试"}
        result, log = truncator.truncate_test_point(tp, target_budget=0)
        self.assertIsInstance(result, dict)

    def test_very_small_budget(self):
        """极小预算（仅够P0字段）"""
        truncator = ContextTruncator(model_context_window=128000)
        tp = make_test_point()
        result, log = truncator.truncate_test_point(tp, target_budget=10)
        self.assertIsInstance(result, dict)
        # P0字段应保留
        self.assertIn("id", result)

    def test_single_test_point_batch(self):
        """单条测试点批量截断"""
        truncator = ContextTruncator()
        tps = [make_test_point()]
        results, log = truncator.truncate_batch(tps)
        self.assertEqual(len(results), 1)

    def test_all_empty_fields(self):
        """所有字段为空"""
        truncator = ContextTruncator()
        tp = {
            "id": "",
            "title": "",
            "description": "",
            "operations_chain": [],
            "exception_scenarios": [],
            "ui_elements": {},
        }
        result, log = truncator.truncate_test_point(tp)
        self.assertIsInstance(result, dict)

    def test_unicode_content(self):
        """Unicode内容（emoji、特殊字符）"""
        truncator = ContextTruncator()
        tp = {
            "id": "TP-001",
            "title": "测试⚠️特殊字符🎉",
            "description": "包含emoji和特殊符号：©️®️™️",
            "exception_scenarios": [{"desc": "异常⚠️场景"}],
        }
        result, log = truncator.truncate_test_point(tp, target_budget=100)
        self.assertIsInstance(result, dict)

    def test_deeply_nested_json(self):
        """深度嵌套JSON"""
        truncator = ContextTruncator()
        tp = make_test_point()
        # 在exception_scenarios中添加深度嵌套
        tp["exception_scenarios"] = [
            {
                "scenario_id": "EX-001",
                "nested": {
                    "level1": {
                        "level2": {
                            "level3": {
                                "data": "深层嵌套数据" * 50
                            }
                        }
                    }
                }
            }
        ]
        result, log = truncator.truncate_test_point(tp, target_budget=200)
        self.assertIsInstance(result, dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
