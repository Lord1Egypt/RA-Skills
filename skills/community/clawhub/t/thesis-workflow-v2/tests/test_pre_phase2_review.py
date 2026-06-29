#!/usr/bin/env python3
"""
tests/test_pre_phase2_review.py

验证 pre_phase2_review 及辅助函数的行为：
  1. _find_nodes 正确从 outline 提取节点列表
  2. 覆盖率统计正确
  3. 菜单选项 1/2/3/4/5 都能正确处理
  4. outline 不存在时返回错误
  5. 节点为空时返回错误
"""

import sys
import unittest
import unittest.mock

sys.path.insert(0, "scripts")

from orchestrator_v2 import (
    pre_phase2_review,
    _find_nodes,
    _print_with_hint,
    _print_without_hint,
    _edit_node_hint,
)


class TestFindNodes(unittest.TestCase):

    def test_finds_top_level_nodes(self):
        """正确找到顶层 nodes 列表"""
        outline = {
            "outline": {
                "outline_tree": {
                    "nodes": [
                        {"id": "1", "title": "绪论", "level": 1},
                        {"id": "2", "title": "理论", "level": 1},
                    ]
                }
            }
        }
        nodes = _find_nodes(outline)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0]["id"], "1")

    def test_finds_nested_nodes(self):
        """outline 结构嵌套时也能找到"""
        outline = {
            "outline": {
                "data": {
                    "outline_tree": {
                        "nodes": [
                            {"id": "1", "title": "绪论", "level": 1},
                            {"id": "3", "title": "外部环境", "level": 1},
                        ]
                    }
                }
            }
        }
        nodes = _find_nodes(outline)
        self.assertEqual(len(nodes), 2)

    def test_returns_none_when_not_found(self):
        """找不到 nodes 时返回 None"""
        self.assertIsNone(_find_nodes({}))
        self.assertIsNone(_find_nodes({"foo": "bar"}))


class TestPrePhase2ReviewMocked(unittest.TestCase):

    @unittest.mock.patch("orchestrator_v2.outline_load")
    def test_outline_missing_returns_error(self, mock_load):
        """大纲不存在时返回错误"""
        mock_load.return_value = None
        result = pre_phase2_review("不存在的论文")
        self.assertFalse(result.get("ok"))
        self.assertIn("error", result)

    @unittest.mock.patch("orchestrator_v2.outline_load")
    def test_nodes_empty_returns_error(self, mock_load):
        """节点为空时返回错误"""
        mock_load.return_value = {"outline": {"outline_tree": {"nodes": []}}}
        result = pre_phase2_review("某论文")
        self.assertFalse(result.get("ok"))
        self.assertIn("error", result)

    @unittest.mock.patch("builtins.input")
    @unittest.mock.patch("orchestrator_v2.outline_load")
    def test_continue_action_on_option4(self, mock_load, mock_input):
        """用户选4时返回 continue"""
        mock_load.return_value = {
            "outline": {
                "outline_tree": {
                    "nodes": [
                        {"id": "1", "title": "绪论", "level": 1},
                        {"id": "1.1", "title": "选题背景", "level": 2,
                         "parent_id": "1", "content_hint": "南京大学MBA",
                         "research_keywords": []},
                    ]
                }
            }
        }
        mock_input.return_value = "4"

        result = pre_phase2_review("测试论文")

        self.assertTrue(result.get("ok"))
        self.assertEqual(result.get("action"), "continue")
        self.assertIn("stats", result)

    @unittest.mock.patch("builtins.input")
    @unittest.mock.patch("orchestrator_v2.outline_load")
    def test_exit_action_on_option5(self, mock_load, mock_input):
        """用户选5时返回 exit"""
        mock_load.return_value = {
            "outline": {
                "outline_tree": {
                    "nodes": [
                        {"id": "1", "title": "绪论", "level": 1},
                    ]
                }
            }
        }
        mock_load.return_value = {
            "outline": {
                "outline_tree": {
                    "nodes": [{"id": "1", "title": "绪论", "level": 1}]
                }
            }
        }
        mock_input.return_value = "5"

        result = pre_phase2_review("测试论文")

        self.assertTrue(result.get("ok"))
        self.assertEqual(result.get("action"), "exit")

    @unittest.mock.patch("builtins.input")
    @unittest.mock.patch("orchestrator_v2.outline_load")
    def test_exit_on_eoferror(self, mock_load, mock_input):
        """Ctrl+D 时优雅退出"""
        mock_load.return_value = {
            "outline": {
                "outline_tree": {
                    "nodes": [{"id": "1", "title": "绪论", "level": 1}]
                }
            }
        }
        mock_input.side_effect = EOFError()

        result = pre_phase2_review("测试论文")

        self.assertTrue(result.get("ok"))
        self.assertEqual(result.get("action"), "exit")

    @unittest.mock.patch("builtins.input")
    @unittest.mock.patch("orchestrator_v2.outline_load")
    def test_invalid_option_reprompts(self, mock_load, mock_input):
        """无效选项重新提示"""
        mock_load.return_value = {
            "outline": {
                "outline_tree": {
                    "nodes": [{"id": "1", "title": "绪论", "level": 1}]
                }
            }
        }
        mock_input.side_effect = ["9", "5"]  # 先输入9无效，再输入5退出

        result = pre_phase2_review("测试论文")

        self.assertTrue(result.get("ok"))
        self.assertEqual(result.get("action"), "exit")


class TestCoverageStats(unittest.TestCase):

    @unittest.mock.patch("builtins.input")
    @unittest.mock.patch("orchestrator_v2.outline_load")
    def test_coverage_stats_accurate(self, mock_load, mock_input):
        """统计覆盖率正确"""
        mock_load.return_value = {
            "outline": {
                "outline_tree": {
                    "nodes": [
                        {"id": "1", "title": "绪论", "level": 1},
                        {"id": "2", "title": "理论基础", "level": 1},
                        {"id": "1.1", "title": "选题背景", "level": 2,
                         "parent_id": "1", "content_hint": "有内容",
                         "research_keywords": []},
                        {"id": "1.2", "title": "研究问题", "level": 2,
                         "parent_id": "1", "content_hint": "", "research_keywords": []},
                    ]
                }
            }
        }
        mock_input.return_value = "4"

        result = pre_phase2_review("测试论文")

        stats = result.get("stats", {})
        self.assertEqual(stats.get("total"), 2)  # 2个level2节点
        self.assertEqual(stats.get("with_hint"), 1)  # 1个有hint
        self.assertEqual(stats.get("coverage_pct"), 50)


class TestEditNodeHint(unittest.TestCase):

    @unittest.mock.patch("builtins.input")
    @unittest.mock.patch("orchestrator_v2.outline_update_status")
    def test_updates_hint_successfully(self, mock_update, mock_input):
        """成功更新节点归因"""
        nodes = [
            {"id": "3.1", "title": "外部环境分析", "level": 2,
             "content_hint": "旧内容", "research_keywords": []},
        ]
        mock_input.side_effect = ["3.1", "A公司差异化战略定位"]
        mock_update.return_value = True

        _edit_node_hint("测试论文", nodes)

        mock_update.assert_called_once()
        call_args = mock_update.call_args
        self.assertEqual(call_args[1].get("content_hint"), "A公司差异化战略定位")

    @unittest.mock.patch("builtins.input")
    def test_empty_input_cancels(self, mock_input):
        """直接回车取消编辑"""
        nodes = [{"id": "3.1", "title": "外部环境", "level": 2,
                  "content_hint": "", "research_keywords": []}]
        mock_input.return_value = ""

        # 不抛异常
        _edit_node_hint("测试论文", nodes)

    @unittest.mock.patch("builtins.input")
    def test_invalid_node_id_reports_error(self, mock_input):
        """不存在的节点ID报错"""
        nodes = [{"id": "3.1", "title": "外部环境", "level": 2,
                  "content_hint": "", "research_keywords": []}]
        mock_input.side_effect = ["9.9", ""]  # 无效ID然后取消

        import io, sys
        buf = io.StringIO()
        with unittest.mock.patch("sys.stdout", buf):
            _edit_node_hint("测试论文", nodes)
        output = buf.getvalue()
        self.assertIn("不存在", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
