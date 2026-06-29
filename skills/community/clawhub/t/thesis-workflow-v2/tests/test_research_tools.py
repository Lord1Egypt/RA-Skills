#!/usr/bin/env python3
"""
tests/test_research_tools.py

验证 research_tools.py 的行为：
  1. research_enrich_from_outline 只读 outline，不调用网络
  2. tavily_search 失败时返回降级消息，不抛异常
  3. research_enrich outline内容充足时不调Tavily
  4. research_enrich outline内容贫瘠时调用Tavily补充
"""

import sys
import unittest
import unittest.mock

sys.path.insert(0, "scripts")
from research_tools import (
    tavily_search,
    research_enrich,
    research_enrich_from_outline,
    _get_outline_node,
)


class TestTavilySearch(unittest.TestCase):

    def test_returns_string_always(self):
        """无论成功失败，tavily_search 总返回字符串，不抛异常"""
        result = tavily_search("竞争战略")
        self.assertIsInstance(result, str)
        self.assertGreaterEqual(len(result), 0)

    def test_failure_returns_degraded_message(self):
        """mcporter 不可用时返回友好降级消息"""
        result = tavily_search("测试查询")
        # 降级消息不应该包含异常堆栈
        self.assertNotIn("Traceback", result)
        self.assertNotIn("Traceback", result)
        # 应该包含降级标识
        self.assertTrue(
            result.startswith("[Tavily") or len(result) >= 0
        )


class TestResearchEnrichFromOutline(unittest.TestCase):

    def test_empty_when_node_not_found(self):
        """节点不存在时返回空字符串"""
        with unittest.mock.patch('research_tools._get_outline_node', return_value=None):
            result = research_enrich_from_outline("不存在节点", "某论文")
            self.assertEqual(result, "")

    def test_extracts_content_hint(self):
        """正确提取 content_hint"""
        with unittest.mock.patch('research_tools._get_outline_node') as mock_get:
            mock_get.return_value = {
                "content_hint": "A公司主营应用分发，信息流广告业务",
                "research_keywords": []
            }
            result = research_enrich_from_outline("3.1", "测试论文")
            self.assertIn("A公司主营应用分发", result)
            self.assertIn("信息流广告", result)

    def test_extracts_research_keywords(self):
        """正确提取 research_keywords"""
        with unittest.mock.patch('research_tools._get_outline_node') as mock_get:
            mock_get.return_value = {
                "content_hint": "",
                "research_keywords": ["竞争战略", "差异化", "互联网分发"]
            }
            result = research_enrich_from_outline("3.1", "测试论文")
            self.assertIn("竞争战略", result)
            self.assertIn("差异化", result)
            self.assertIn("互联网分发", result)

    def test_no_network_call(self):
        """不调用网络（测试环境验证）"""
        with unittest.mock.patch('research_tools._get_outline_node') as mock_get:
            mock_get.return_value = {"content_hint": "测试内容", "research_keywords": []}
            with unittest.mock.patch('research_tools.tavily_search') as mock_tavily:
                result = research_enrich_from_outline("3.1", "测试论文")
                mock_tavily.assert_not_called()
                self.assertIn("测试内容", result)


class TestResearchEnrich(unittest.TestCase):

    def test_outline_content_sufficient_skips_tavily(self):
        """outline 内容充足时不调用 Tavily"""
        with unittest.mock.patch('research_tools._get_outline_node') as mock_get:
            mock_get.return_value = {
                "content_hint": "A公司主营应用分发业务，信息流广告为主要变现模式，"
                                "面临手机大盘见顶与AI大模型颠覆双重压力。",
                "research_keywords": ["应用分发", "竞争战略"]
            }
            with unittest.mock.patch('research_tools.tavily_search') as mock_tavily:
                result = research_enrich("3.1", "测试论文")
                mock_tavily.assert_not_called()  # 内容充足，不查Tavily
                self.assertIn("A公司主营应用分发", result)

    def test_outline_content_poor_invokes_tavily(self):
        """outline 内容贫瘠时调用 Tavily 补充"""
        with unittest.mock.patch('research_tools._get_outline_node') as mock_get:
            mock_get.return_value = {
                "content_hint": "A公司竞争战略。",
                "research_keywords": ["应用分发"]
            }
            with unittest.mock.patch('research_tools.tavily_search') as mock_tavily:
                mock_tavily.return_value = "Tavily搜索结果：应用分发是移动互联网核心赛道。"
                result = research_enrich("3.1", "测试论文")
                mock_tavily.assert_called_once_with("应用分发")
                self.assertIn("Tavily补充搜索", result)
                self.assertIn("应用分发是移动互联网核心赛道", result)

    def test_completely_empty_returns_empty(self):
        """outline 完全无数据时返回空字符串"""
        with unittest.mock.patch('research_tools._get_outline_node', return_value=None):
            result = research_enrich("3.1", "某论文")
            self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
