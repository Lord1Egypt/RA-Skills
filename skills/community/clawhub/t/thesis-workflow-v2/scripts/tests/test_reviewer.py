#!/usr/bin/env python3
"""
test_reviewer.py - Reviewer 单元测试
"""

import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_context_builder import setup_mock_state

from reviewer import (
    program_check,
    build_review_prompt,
    review_node_prompt,
    parse_review_response,
    review_node,
)


class TestProgramCheck(unittest.TestCase):
    """第一层：程序兜底检查"""

    def test_正常内容(self):
        content = "这是一个正常的段落内容。" * 20
        result = program_check(content, "1.1")
        self.assertTrue(result["passed"])

    def test_空内容(self):
        result = program_check("", "1.1")
        self.assertFalse(result["passed"])
        self.assertIn("为空", result["reason"])

    def test_字数极少(self):
        result = program_check("太短", "1.1")
        self.assertFalse(result["passed"])

    def test_乱码检测(self):
        content = "正常内容\x00\x01\x02异常字符"
        result = program_check(content, "1.1")
        self.assertFalse(result["passed"])
        self.assertIn("乱码", result["reason"])

    def test_连续重复字符(self):
        content = "AAAAAAAAAAAAAAAAAAAAAAAAAAB"  # 连续A
        result = program_check(content, "1.1")
        self.assertFalse(result["passed"])
        self.assertIn("重复", result["reason"])


class TestBuildReviewPrompt(unittest.TestCase):
    """Prompt 构建测试"""

    def setUp(self):
        self.paper_name = setup_mock_state()

    def test_prompt包含必要元素(self):
        node = {
            "id": "1.1",
            "title": "1.1 研究背景",
            "content": "这是研究背景内容。" * 20,
            "word_count_range": (600, 1500)
        }
        prompt = build_review_prompt(
            "1.1", "1.1 研究背景", node["content"],
            word_count_range=(600, 1500)
        )
        self.assertIn("1.1 研究背景", prompt)
        self.assertIn("逻辑性", prompt)
        self.assertIn("流畅性", prompt)
        self.assertIn("600", prompt)
        self.assertIn("1500", prompt)
        self.assertIn('"quality":', prompt)

    def test_prompt包含bridge(self):
        prompt = build_review_prompt(
            "1.1", "1.1 研究背景", "内容",
            bridge_paragraph="在前文中已阐明..."
        )
        self.assertIn("前文衔接", prompt)
        self.assertIn("在前文中已阐明", prompt)


class TestReviewNodePrompt(unittest.TestCase):
    """review_node_prompt 函数测试"""

    def setUp(self):
        self.paper_name = setup_mock_state()

    def test_返回prompt(self):
        prompt = review_node_prompt(self.paper_name, "1.1")
        self.assertIsNotNone(prompt)
        self.assertIn("评审节点", prompt)

    def test_无效节点返回None(self):
        prompt = review_node_prompt(self.paper_name, "不存在")
        self.assertIsNone(prompt)


class TestParseReviewResponse(unittest.TestCase):
    """解析 AI 评审响应"""

    def test_标准JSON格式(self):
        response = '''{
  "quality": "high",
  "summary": "内容质量优秀",
  "strengths": ["逻辑清晰"],
  "weaknesses": [],
  "suggestions": []
}'''
        result = parse_review_response(response)
        self.assertTrue(result["ok"])
        self.assertEqual(result["quality"], "high")

    def test_markdown代码块格式(self):
        response = '''```json
{
  "quality": "medium",
  "summary": "有小幅优化空间",
  "strengths": ["结构完整"],
  "weaknesses": ["过渡不够自然"],
  "suggestions": ["建议增加过渡句"]
}
```'''
        result = parse_review_response(response)
        self.assertTrue(result["ok"])
        self.assertEqual(result["quality"], "medium")

    def test_解析失败(self):
        response = "这不是有效的 JSON 格式"
        result = parse_review_response(response)
        self.assertFalse(result["ok"])
        self.assertIn("解析失败", result["error"])


class TestReviewNode(unittest.TestCase):
    """完整评审流程测试（含 mock LLM）"""

    def setUp(self):
        self.paper_name = setup_mock_state()
        self.mock_node = {
            "id": "1.1",
            "title": "1.1 研究背景",
            "content": "这是研究背景的测试内容。" * 30,
            "bridge_paragraph": "在前文中已阐明行业背景",
            "word_count_range": (600, 1500),
            "writing_status": "completed"
        }

    def test_程序兜底_空内容(self):
        def mock_llm(prompt):
            return '{"quality": "high"}'

        result = review_node(self.paper_name, "1.1", mock_llm)
        self.assertTrue(result["ok"])

    def test_AI评审_high质量(self):
        mock_response = '''{
  "quality": "high",
  "summary": "内容质量优秀，逻辑清晰，衔接自然",
  "strengths": ["论证充分", "过渡自然"],
  "weaknesses": [],
  "suggestions": []
}'''

        def mock_llm(prompt):
            return mock_response

        with patch('reviewer.outline_get_node', return_value=self.mock_node):
            result = review_node(self.paper_name, "1.1", mock_llm)

        self.assertTrue(result["ok"])
        self.assertTrue(result["passed"])
        self.assertEqual(result["quality"], "high")

    def test_AI评审_medium质量(self):
        mock_response = '''{
  "quality": "medium",
  "summary": "内容基本合格，有小幅优化空间",
  "strengths": ["结构完整"],
  "weaknesses": ["过渡不够自然"],
  "suggestions": ["建议增加过渡句"]
}'''

        def mock_llm(prompt):
            return mock_response

        with patch('reviewer.outline_get_node', return_value=self.mock_node):
            result = review_node(self.paper_name, "1.1", mock_llm)

        self.assertTrue(result["ok"])
        self.assertTrue(result["passed"])

    def test_AI评审_low质量(self):
        mock_response = '''{
  "quality": "low",
  "summary": "内容存在明显问题",
  "strengths": [],
  "weaknesses": ["逻辑混乱", "论据不足", "衔接断裂"],
  "suggestions": ["重新组织逻辑结构", "补充数据支撑"]
}'''

        def mock_llm(prompt):
            return mock_response

        with patch('reviewer.outline_get_node', return_value=self.mock_node):
            result = review_node(self.paper_name, "1.1", mock_llm)

        self.assertTrue(result["ok"])
        self.assertFalse(result["passed"])

    def test_LLM调用失败(self):
        def failing_llm(prompt):
            raise RuntimeError("API Error")

        with patch('reviewer.outline_get_node', return_value=self.mock_node):
            result = review_node(self.paper_name, "1.1", failing_llm)

        self.assertFalse(result["ok"])
        self.assertIn("失败", result["error"])


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print("🏁 开始 Reviewer 测试\n")

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
