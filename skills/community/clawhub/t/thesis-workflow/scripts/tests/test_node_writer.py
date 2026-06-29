#!/usr/bin/env python3
"""
test_node_writer.py - NodeWriter 单元测试
"""

import sys
import os
import unittest

# 将 scripts/ 目录加入路径（与 test_context_builder.py 相同方式）
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from test_context_builder import setup_mock_state

from node_writer import (
    build_writing_prompt,
    extract_key_conclusion,
    extract_key_conclusion_from_response,
    count_chinese_chars,
    count_words,
    validate_content,
    write_node,
    write_node_with_llm,
)


class TestExtractKeyConclusion(unittest.TestCase):
    """测试 key_conclusion 提取"""

    def test_因此标记(self):
        text = "行业发展迅速，市场规模持续扩大。因此，本文认为互联网分发业务正处于高速增长期，具有广阔的发展前景。"
        result = extract_key_conclusion(text)
        self.assertTrue("因此" in result or "本文认为" in result)
        self.assertLessEqual(len(result), 200)

    def test_综合标记(self):
        text = "综上，可以得出以下结论：行业发展呈现快速增长态势。"
        result = extract_key_conclusion(text)
        self.assertTrue(len(result) > 0)  # 综上匹配到即有结论

    def test_本章小结(self):
        text = "本章小结：本节通过对研究背景的系统分析，明确了该领域的基本特征。"
        result = extract_key_conclusion(text)
        self.assertIn("本章小结", result) or self.assertIn("本节", result)

    def test_无标记取末尾段(self):
        text = "这是一个普通段落，没有任何结论标记词。这是另一个段落，继续讨论相关内容。"
        result = extract_key_conclusion(text)
        self.assertTrue(len(result) > 0)

    def test_空内容(self):
        result = extract_key_conclusion("")
        self.assertEqual(result, "")

    def test_标签提取(self):
        text = "这是正文内容。<key_conclusion>本节核心结论是：行业发展呈现快速增长态势。</key_conclusion> 后续内容。"
        result = extract_key_conclusion_from_response(text)
        self.assertIn("核心结论", result)
        self.assertIn("行业发展", result)

    def test_纯文本提取(self):
        text = "本研究旨在探讨互联网分发业务的竞争战略选择。综上所述，该行业面临机遇与挑战并存的局面。"
        result = extract_key_conclusion_from_response(text)
        self.assertTrue(len(result) > 0)


class TestWordCount(unittest.TestCase):
    """测试字数统计"""

    def test_纯中文(self):
        text = "这是一个测试内容，共包含二十个汉字。"
        self.assertEqual(count_chinese_chars(text), 16)

    def test_中英混合(self):
        text = "AI人工智能技术发展迅速，machine learning算法不断进步。"  # 16中+2英
        chars = count_chinese_chars(text)
        words = count_words(text)
        self.assertGreaterEqual(chars, 16)
        self.assertGreaterEqual(words, chars + 2)

    def test_纯标点(self):
        text = "，。、；？！"
        self.assertEqual(count_chinese_chars(text), 0)


class TestValidateContent(unittest.TestCase):
    """测试内容质量检查"""

    def test_正常内容(self):
        text = "这是一个正常的段落内容，包含足够的文字用于学术论文写作。" * 5
        ok, msg = validate_content(text)
        self.assertTrue(ok)

    def test_内容过短(self):
        text = "太短了"
        ok, msg = validate_content(text, min_words=50)
        self.assertFalse(ok)
        self.assertTrue(len(msg) > 0)  # 有错误信息即可

    def test_空内容(self):
        ok, msg = validate_content("")
        self.assertFalse(ok)


class TestWriteNode(unittest.TestCase):
    """测试 write_node 主入口"""

    def setUp(self):
        self.paper_name = setup_mock_state()

    def test_有效节点(self):
        result = write_node(self.paper_name, "1.1")
        self.assertTrue(result["ok"])
        self.assertEqual(result["node_id"], "1.1")
        self.assertIn("prompt", result)
        self.assertIn("写作任务", result["prompt"])

    def test_无效节点(self):
        result = write_node(self.paper_name, "不存在")
        self.assertFalse(result["ok"])
        self.assertIn("不存在", result["error"])

    def test_节点有标题(self):
        result = write_node(self.paper_name, "ch1")
        self.assertTrue(result["ok"])
        self.assertIn("绪论", result["title"])

    def test_prompt包含必要信息(self):
        result = write_node(self.paper_name, "1.1")
        prompt = result["prompt"]
        self.assertIn("1.1", prompt)
        self.assertIn("字数", prompt)


class TestWriteNodeWithLLM(unittest.TestCase):
    """测试 write_node_with_llm（带 mock LLM）"""

    def setUp(self):
        self.paper_name = setup_mock_state()

    def test_mock_llm成功(self):
        """Mock LLM 返回带标签的完整内容"""
        mock_response = """# 1.1 研究背景

本研究聚焦于互联网分发业务的市场现状与竞争格局。随着移动互联网的高速发展，该领域呈现出新的特征。

## 主要内容

1. 市场规模持续扩大
2. 竞争格局日趋激烈
3. 技术创新推动行业变革

<key_conclusion>本节通过分析得出：互联网分发业务市场规模大、增速快，但竞争日趋激烈，企业需差异化竞争。</key_conclusion>"""

        def mock_llm(prompt: str) -> str:
            return mock_response

        result = write_node_with_llm(self.paper_name, "1.1", mock_llm)
        self.assertTrue(result["ok"])
        self.assertIn("市场规模", result["content"])
        self.assertIn("互联网分发业务", result["key_conclusion"])
        self.assertGreater(result["word_count"], 50)
        self.assertTrue(result.get("state_updated", False))

    def test_mock_llm无标签(self):
        """Mock LLM 返回无标签内容，使用回退提取"""
        mock_response = """# 1.1 研究背景

行业发展迅速。因此，行业呈现快速增长态势。"""

        def mock_llm(prompt: str) -> str:
            return mock_response

        result = write_node_with_llm(self.paper_name, "1.1", mock_llm)
        self.assertTrue(result["ok"])
        self.assertIn("因此", result["key_conclusion"])

    def test_mock_llm失败(self):
        """LLM 调用异常"""
        def failing_llm(prompt: str) -> str:
            raise RuntimeError("API Error")

        result = write_node_with_llm(self.paper_name, "1.1", failing_llm)
        self.assertFalse(result["ok"])
        self.assertIn("失败", result["error"])


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print("🏁 开始 NodeWriter 测试\n")

    # unittest 方式运行
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
