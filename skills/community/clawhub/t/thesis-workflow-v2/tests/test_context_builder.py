#!/usr/bin/env python3
"""
tests/test_context_builder.py

验证 context_builder 的方案B+C集成：
  1. build_prompt_package 返回 research_context 字段
  2. build_prompt_package_text 正确渲染研究背景和标签说明
  3. research_tools 异常时 research_context 为空（不阻断）
"""

import sys
import unittest
import unittest.mock

sys.path.insert(0, "scripts")

# 先 import 一次（不在 mock patch 范围内）
import context_builder
import state_manager_v2
import research_tools


def _mock_context(node_id="3.1", title="外部环境分析", hint="A公司主营应用分发"):
    return {
        "current_node": {
            "id": node_id,
            "title": title,
            "level": 2,
            "num": node_id,
            "content_hint": hint,
        },
        "parent_node": {
            "id": node_id.split(".")[0],
            "title": "外部环境",
            "level": 1
        }
    }


class TestResearchContextInjection(unittest.TestCase):

    @unittest.mock.patch("context_builder.outline_get_context")
    @unittest.mock.patch("context_builder.outline_load")
    @unittest.mock.patch("research_tools.research_enrich_from_outline")
    def test_package_has_research_context_key(self, mock_enrich, mock_load, mock_ctx):
        """build_prompt_package 返回的 package 含 research_context 字段"""
        mock_ctx.return_value = _mock_context()
        mock_load.return_value = {"chapter_hints": {}}
        mock_enrich.return_value = "[开题报告]\nA公司主营应用分发"

        pkg = context_builder.build_prompt_package("测试论文", "3.1")

        self.assertTrue(pkg.get("ok"), f"pkg error: {pkg.get('error')}")
        self.assertIn("research_context", pkg)

    @unittest.mock.patch("context_builder.outline_get_context")
    @unittest.mock.patch("context_builder.outline_load")
    @unittest.mock.patch("research_tools.research_enrich_from_outline")
    def test_research_context_value_from_outline(self, mock_enrich, mock_load, mock_ctx):
        """research_context 正确从 outline 提取"""
        mock_ctx.return_value = _mock_context()
        mock_load.return_value = {"chapter_hints": {}}
        mock_enrich.return_value = "[开题报告]\nA公司差异化战略"

        pkg = context_builder.build_prompt_package("测试论文", "3.1")

        self.assertEqual(pkg["research_context"], "[开题报告]\nA公司差异化战略")

    @unittest.mock.patch("context_builder.outline_get_context")
    @unittest.mock.patch("context_builder.outline_load")
    @unittest.mock.patch("research_tools.research_enrich_from_outline",
                         side_effect=RuntimeError("网络错误"))
    def test_research_tools_failure_returns_empty(self, mock_enrich, mock_load, mock_ctx):
        """research_tools 抛异常时，research_context 为空，不阻断"""
        mock_ctx.return_value = _mock_context()
        mock_load.return_value = {"chapter_hints": {}}

        pkg = context_builder.build_prompt_package("测试论文", "3.1")

        self.assertTrue(pkg.get("ok"), f"pkg error: {pkg.get('error')}")
        self.assertEqual(pkg.get("research_context", ""), "")


class TestPromptTextSearchTags(unittest.TestCase):

    @unittest.mock.patch("context_builder.outline_get_context")
    @unittest.mock.patch("context_builder.outline_load")
    @unittest.mock.patch("research_tools.research_enrich_from_outline")
    def test_search_tag_instruction_rendered(self, mock_enrich, mock_load, mock_ctx):
        """build_prompt_package_text 输出含方案B触发标签说明"""
        mock_ctx.return_value = _mock_context()
        mock_load.return_value = {"chapter_hints": {}}
        mock_enrich.return_value = ""

        pkg = context_builder.build_prompt_package("测试论文", "3.1")
        text = context_builder.build_prompt_package_text(pkg)

        self.assertIn("[SEARCH:", text)
        self.assertIn("Tavily", text)

    @unittest.mock.patch("context_builder.outline_get_context")
    @unittest.mock.patch("context_builder.outline_load")
    @unittest.mock.patch("research_tools.research_enrich_from_outline")
    def test_research_context_rendered_in_text(self, mock_enrich, mock_load, mock_ctx):
        """research_context 内容正确渲染到 prompt 文本"""
        mock_ctx.return_value = _mock_context()
        mock_load.return_value = {"chapter_hints": {}}
        mock_enrich.return_value = "[开题报告]\nA公司差异化战略定位"

        pkg = context_builder.build_prompt_package("测试论文", "3.1")
        text = context_builder.build_prompt_package_text(pkg)

        self.assertIn("A公司差异化战略定位", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
