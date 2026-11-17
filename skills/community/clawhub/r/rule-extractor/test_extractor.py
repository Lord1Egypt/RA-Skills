"""
规则提取器测试用例
"""
import os
import sys
import json
import tempfile
import unittest

# 添加 scripts 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))

from extractor import RuleExtractor, Rule
from formatter import RuleFormatter


class TestRuleExtractor(unittest.TestCase):
    """测试规则提取器"""

    def setUp(self):
        self.extractor = RuleExtractor()

    def test_extract_avoid_rules_from_traces(self):
        """测试从 traces 提取 avoid 规则"""
        traces = [
            {"operation_name": "file_write", "status": "error", "error_type": "encoding_error"},
            {"operation_name": "file_write", "status": "error", "error_type": "encoding_error"},
            {"operation_name": "api_call", "status": "error", "error_type": "timeout"},
            {"operation_name": "file_read", "status": "success"},
        ]

        rules = self.extractor.extract_from_traces(traces)
        avoid_rules = [r for r in rules if r.category == "avoid"]

        # 应该有 avoid 规则
        self.assertGreater(len(avoid_rules), 0)

        # file_write 应该有最高的置信度（2/3 = 67%）
        file_write_rule = next((r for r in avoid_rules if r.pattern == "file_write"), None)
        self.assertIsNotNone(file_write_rule)
        self.assertEqual(file_write_rule.confidence, 0.67)
        self.assertEqual(file_write_rule.source_count, 2)

    def test_extract_prefer_rules_from_traces(self):
        """测试从 traces 提取 prefer 规则"""
        traces = [
            {"operation_name": "async_await", "status": "success"},
            {"operation_name": "async_await", "status": "success"},
            {"operation_name": "async_await", "status": "success"},
            {"operation_name": "pathlib", "status": "success"},
            {"operation_name": "file_write", "status": "error"},
        ]

        rules = self.extractor.extract_from_traces(traces)
        prefer_rules = [r for r in rules if r.category == "prefer"]

        # 应该有 prefer 规则
        self.assertGreater(len(prefer_rules), 0)

        # async_await 应该有最高的置信度（3/4 = 75%）
        async_rule = next((r for r in prefer_rules if r.pattern == "async_await"), None)
        self.assertIsNotNone(async_rule)
        self.assertEqual(async_rule.confidence, 0.75)
        self.assertEqual(async_rule.source_count, 3)

    def test_extract_from_learnings(self):
        """测试从 .learnings/ 目录提取规则"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建测试学习文件
            with open(os.path.join(tmpdir, "encoding_error.md"), "w", encoding="utf-8") as f:
                f.write("# 文件编码错误处理\n\n应该使用 utf-8 编码...")

            with open(os.path.join(tmpdir, "async_pattern.md"), "w", encoding="utf-8") as f:
                f.write("# 异步操作最佳实践\n\n使用 async/await...")

            rules = self.extractor.extract_from_learnings(tmpdir)

            # 应该有2条规则
            self.assertEqual(len(rules), 2)

            # encoding_error 应该是 avoid（标题包含"错误"）
            encoding_rule = next((r for r in rules if "encoding" in r.rule_id), None)
            self.assertIsNotNone(encoding_rule)
            self.assertEqual(encoding_rule.category, "avoid")
            self.assertEqual(encoding_rule.confidence, 0.8)

            # async_pattern 应该是 prefer
            async_rule = next((r for r in rules if "async" in r.rule_id), None)
            self.assertIsNotNone(async_rule)
            self.assertEqual(async_rule.category, "prefer")

    def test_confidence_threshold(self):
        """测试置信度阈值"""
        # 创建错误率低于10%的情况
        traces = [
            {"operation_name": "rare_error", "status": "error"},
            {"operation_name": "op1", "status": "error"},
            {"operation_name": "op2", "status": "error"},
            {"operation_name": "op3", "status": "error"},
            {"operation_name": "op4", "status": "error"},
            {"operation_name": "op5", "status": "error"},
            {"operation_name": "op6", "status": "error"},
            {"operation_name": "op7", "status": "error"},
            {"operation_name": "op8", "status": "error"},
            {"operation_name": "op9", "status": "error"},
            {"operation_name": "op10", "status": "error"},
        ]

        rules = self.extractor.extract_from_traces(traces)
        avoid_rules = [r for r in rules if r.category == "avoid"]

        # rare_error 只有 1/11 = 9%，低于10%阈值，不应该被提取
        rare_rule = next((r for r in avoid_rules if r.pattern == "rare_error"), None)
        self.assertIsNone(rare_rule)


class TestRuleFormatter(unittest.TestCase):
    """测试规则格式化器"""

    def setUp(self):
        self.formatter = RuleFormatter()
        self.sample_rules = [
            Rule(rule_id="avoid_file_write", category="avoid", description="避免在 file_write 中出现编码错误",
                 pattern="file_write", confidence=0.85, source_count=10),
            Rule(rule_id="avoid_api_call", category="avoid", description="避免在 api_call 中出现超时错误",
                 pattern="api_call", confidence=0.72, source_count=8),
            Rule(rule_id="prefer_async_await", category="prefer", description="优先使用 async/await 处理异步操作",
                 pattern="async_await", confidence=0.90, source_count=15),
            Rule(rule_id="prefer_pathlib", category="prefer", description="优先使用 pathlib 处理文件路径",
                 pattern="pathlib", confidence=0.78, source_count=12),
        ]

    def test_format_as_prompt(self):
        """测试格式化为 System Prompt"""
        prompt = self.formatter.format_as_prompt(self.sample_rules)

        # 检查基本结构
        self.assertIn("【历史经验规则（请遵循）】", prompt)
        self.assertIn("## 避免操作", prompt)
        self.assertIn("## 推荐做法", prompt)

        # 检查规则内容
        self.assertIn("避免在 file_write 中出现编码错误", prompt)
        self.assertIn("优先使用 async/await 处理异步操作", prompt)

        # 检查置信度格式
        self.assertIn("85%", prompt)
        self.assertIn("90%", prompt)

    def test_format_as_json(self):
        """测试格式化为 JSON"""
        json_str = self.formatter.format_as_json(self.sample_rules)
        data = json.loads(json_str)

        # 检查数量
        self.assertEqual(len(data), 4)

        # 检查字段
        first_rule = data[0]
        self.assertIn("rule_id", first_rule)
        self.assertIn("category", first_rule)
        self.assertIn("description", first_rule)
        self.assertIn("confidence", first_rule)
        self.assertIn("source_count", first_rule)

    def test_format_as_markdown(self):
        """测试格式化为 Markdown"""
        md = self.formatter.format_as_markdown(self.sample_rules)

        # 检查标题
        self.assertIn("# 自动提取的规则", md)
        self.assertIn("## 避免操作", md)
        self.assertIn("## 推荐做法", md)

        # 检查表格
        self.assertIn("| 规则ID | 描述 | 置信度 | 来源数 |", md)
        self.assertIn("| avoid_file_write |", md)

    def test_empty_rules(self):
        """测试空规则列表"""
        prompt = self.formatter.format_as_prompt([])
        self.assertEqual(prompt, "")

    def test_sorting_by_confidence(self):
        """测试按置信度排序"""
        prompt = self.formatter.format_as_prompt(self.sample_rules)

        # avoid 规则中，file_write (85%) 应该在 api_call (72%) 前面
        file_write_pos = prompt.find("file_write")
        api_call_pos = prompt.find("api_call")
        self.assertLess(file_write_pos, api_call_pos)


if __name__ == "__main__":
    unittest.main()
