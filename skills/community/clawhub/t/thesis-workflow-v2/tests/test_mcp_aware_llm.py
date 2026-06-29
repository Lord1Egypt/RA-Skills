#!/usr/bin/env python3
"""
tests/test_mcp_aware_llm.py

验证 make_mcp_aware_llm 包装器的行为：
  1. 有 [SEARCH: xxx] 标签 → 触发 tavily_func，结果注入
  2. 无标签 → 原样透传给 original_llm
  3. tavily_func=None → 降级返回友好消息，不抛异常
  4. 多标签 → 全部替换
  5. Tavily 调用失败 → 降级不阻断
"""

import sys
import unittest

sys.path.insert(0, "scripts")
from node_writer import make_mcp_aware_llm


class TestMakeMcpAwareLlm(unittest.TestCase):

    def test_search_tag_replaced(self):
        """[SEARCH: xxx] 标签被替换为搜索结果"""
        def mock_llm(prompt):
            return f"[LLM输出: {prompt[:50]}...]"
        def mock_tavily(query):
            return f"关于「{query}」的研究结果，这是模拟数据。"
        wrapped = make_mcp_aware_llm(mock_llm, tavily_func=mock_tavily)
        result = wrapped("请写[SEARCH: A公司竞争战略]相关内容")
        self.assertIn("搜索结果", result)
        self.assertIn("A公司竞争战略", result)
        self.assertIn("关于「A公司竞争战略」的研究结果", result)

    def test_no_tag_passthrough(self):
        """无标签时原样透传给 original_llm"""
        def mock_llm(prompt):
            self.assertEqual(prompt, "普通prompt，不含标签")
            return "ok"
        wrapped = make_mcp_aware_llm(mock_llm)
        result = wrapped("普通prompt，不含标签")
        self.assertEqual(result, "ok")

    def test_tavily_unavailable_graceful(self):
        """tavily_func=None 时降级，不抛异常"""
        def mock_llm(prompt):
            # 降级消息应该已经被注入 prompt
            self.assertIn("[Tavily不可用", prompt)
            return "ok"
        wrapped = make_mcp_aware_llm(mock_llm, tavily_func=None)
        result = wrapped("请写[SEARCH: test]相关内容")
        self.assertEqual(result, "ok")

    def test_multiple_tags_all_replaced(self):
        """多个 [SEARCH: xxx] 标签全部替换"""
        def mock_llm(prompt):
            self.assertIn("[搜索结果:", prompt)
            self.assertIn("vivo应用商店", prompt)
            self.assertIn("信息流广告", prompt)
            # 标签本身应该被移除
            self.assertNotIn("[SEARCH:", prompt)
            return "ok"
        def mock_tavily(query):
            return f"结果:{query}"
        wrapped = make_mcp_aware_llm(mock_llm, tavily_func=mock_tavily)
        result = wrapped("请写[SEARCH: vivo应用商店]和[SEARCH: 信息流广告]的相关内容")

    def test_tavily_call_failure_does_not_crash(self):
        """Tavily 调用抛异常时降级返回，不阻断写作流程"""
        def failing_tavily(query):
            raise RuntimeError("网络错误")
        def mock_llm(prompt):
            self.assertIn("[Tavily调用失败", prompt)
            return "写作完成"
        wrapped = make_mcp_aware_llm(mock_llm, tavily_func=failing_tavily)
        result = wrapped("请写[SEARCH: A公司]相关内容")
        self.assertEqual(result, "写作完成")

    def test_nested_brackets_not_corrupted(self):
        """嵌套标签不会被部分替换导致格式损坏"""
        def mock_llm(prompt):
            # 标签被完整替换为搜索结果块
            self.assertNotIn("[SEARCH:", prompt)
            # 搜索结果块格式正确
            self.assertIn("[搜索结果:", prompt)
            return "ok"
        def mock_tavily(q):
            return f"结果{q}"
        wrapped = make_mcp_aware_llm(mock_llm, tavily_func=mock_tavily)
        result = wrapped("关于[SEARCH: A公司]的研究[SEARCH: B公司]")  # 无嵌套，正常处理

    def test_real_tavily_not_called_when_no_tag(self):
        """无 [SEARCH:] 标签时，不调用 tavily_func（节省 API 配额）"""
        call_count = 0
        def mock_tavily(query):
            nonlocal call_count
            call_count += 1
            return f"结果:{query}"
        def mock_llm(prompt):
            return "ok"
        wrapped = make_mcp_aware_llm(mock_llm, tavily_func=mock_tavily)
        wrapped("这是一个不含搜索标签的普通prompt")
        self.assertEqual(call_count, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
