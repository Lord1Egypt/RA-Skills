#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1.5 集成测试 - InvoiceAnalyzerWithLLM

测试策略：
- T1 mock 数据在 test/mock_emails.py
- T2 使用 unittest + unittest.mock.patch 模拟 LLM 调用
- T3 语法 + 导入验证
- T4 SKILL.md 更新（见 SKILL.md 末尾）
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# 确保项目根在 path
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

try:
    from test.mock_emails import MOCK_EMAILS
except ImportError:
    # 当作为 __main__ 直接运行时，test/ 不在包路径中
    import mock_emails as _me
    MOCK_EMAILS = _me.MOCK_EMAILS

# 延迟导入，容忍 InvoiceAnalyzer 不可用
InvoiceAnalyzer = None
InvoiceAnalyzerWithLLM = None
try:
    from invoice_analyzer import InvoiceAnalyzer
except ImportError:
    pass

try:
    from invoice_analyzer_v9 import InvoiceAnalyzerWithLLM, LLMAnalysisResult
except ImportError:
    InvoiceAnalyzerWithLLM = None


class TestKnownPlatforms(unittest.TestCase):
    """已知平台置信度 ≥ 0.7，不触发 LLM"""

    @classmethod
    def setUpClass(cls):
        if InvoiceAnalyzerWithLLM is None:
            raise unittest.SkipTest("invoice_analyzer_v9 not available")
        # 不设置 MINIMAX_API_KEY → 纯硬编码模式
        cls.env_backup = os.environ.get("MINIMAX_API_KEY")
        if "MINIMAX_API_KEY" in os.environ:
            del os.environ["MINIMAX_API_KEY"]

    @classmethod
    def tearDownClass(cls):
        if cls.env_backup is not None:
            os.environ["MINIMAX_API_KEY"] = cls.env_backup
        elif "MINIMAX_API_KEY" in os.environ:
            del os.environ["MINIMAX_API_KEY"]

    def test_heyun_international(self):
        """和运国际税务平台"""
        email = MOCK_EMAILS[0]
        analyzer = InvoiceAnalyzerWithLLM()
        result = analyzer.analyze(email.subject, email.text, email.html, email.has_attachments)
        self.assertEqual(result.invoice_type.value, email.expected_type)
        self.assertGreaterEqual(result.confidence, email.expected_confidence_min)

    def test_nuonuo(self):
        """诺诺网"""
        email = MOCK_EMAILS[1]
        analyzer = InvoiceAnalyzerWithLLM()
        result = analyzer.analyze(email.subject, email.text, email.html, email.has_attachments)
        self.assertEqual(result.invoice_type.value, email.expected_type)
        self.assertGreaterEqual(result.confidence, email.expected_confidence_min)

    def test_cnooc(self):
        """中海油批量"""
        email = MOCK_EMAILS[2]
        analyzer = InvoiceAnalyzerWithLLM()
        result = analyzer.analyze(email.subject, email.text, email.html, email.has_attachments)
        self.assertEqual(result.invoice_type.value, email.expected_type)
        self.assertGreaterEqual(result.confidence, email.expected_confidence_min)


class TestUnknownPlatformTriggersLLM(unittest.TestCase):
    """未知平台触发 LLM fallback（mock LLM 返回）"""

    @classmethod
    def setUpClass(cls):
        if InvoiceAnalyzerWithLLM is None:
            raise unittest.SkipTest("invoice_analyzer_v9 not available")
        cls.env_backup = os.environ.get("MINIMAX_API_KEY")
        os.environ["MINIMAX_API_KEY"] = "mock-api-key-for-test"

    @classmethod
    def tearDownClass(cls):
        if cls.env_backup is not None:
            os.environ["MINIMAX_API_KEY"] = cls.env_backup
        elif "MINIMAX_API_KEY" in os.environ:
            del os.environ["MINIMAX_API_KEY"]

    @patch("invoice_analyzer_v9.LLMInvoiceAnalyzer")
    def test_unknown_triggers_llm(self, mock_llm_class):
        """未知平台应触发 LLM"""
        email = MOCK_EMAILS[3]  # 顺捷云

        # Mock LLM 返回
        mock_result = MagicMock()
        mock_result.invoice_type.value = "direct_pdf_link"
        mock_result.strategy.value = "browser_simple"
        mock_result.confidence = 0.85
        mock_result.urls = ["https://shunjeyun.com/invoice/abc123"]
        mock_result.notes = "LLM分析：顺捷云平台，直接PDF链接"
        mock_result.selectors = []
        mock_result.platform_name = "顺捷云"
        mock_result.llm_used = True
        mock_result.reasoning = "识别为顺捷云平台"

        mock_llm_instance = MagicMock()
        mock_llm_instance.analyze.return_value = mock_result
        mock_llm_class.return_value = mock_llm_instance

        analyzer = InvoiceAnalyzerWithLLM()
        # 确认 base 是 unknown → 触发 LLM
        base = InvoiceAnalyzer().analyze(email.subject, email.text, email.html, email.has_attachments)
        self.assertEqual(base.invoice_type.value, "unknown")

        result = analyzer.analyze(email.subject, email.text, email.html, email.has_attachments)

        # LLM 应该被调用（unknown 类型无论 confidence 都触发 LLM）
        mock_llm_instance.analyze.assert_called_once()
        # 结果应该是 LLM 返回的（置信度更高）
        self.assertGreater(result.confidence, base.confidence)
        self.assertTrue(result.llm_used)


class TestLLMWinsWhenBetter(unittest.TestCase):
    """LLM 置信度更高时使用 LLM 结果"""

    @classmethod
    def setUpClass(cls):
        if InvoiceAnalyzerWithLLM is None:
            raise unittest.SkipTest("invoice_analyzer_v9 not available")
        cls.env_backup = os.environ.get("MINIMAX_API_KEY")
        os.environ["MINIMAX_API_KEY"] = "mock-api-key-for-test"

    @classmethod
    def tearDownClass(cls):
        if cls.env_backup is not None:
            os.environ["MINIMAX_API_KEY"] = cls.env_backup
        elif "MINIMAX_API_KEY" in os.environ:
            del os.environ["MINIMAX_API_KEY"]

    @patch("invoice_analyzer_v9.LLMInvoiceAnalyzer")
    def test_llm_wins(self, mock_llm_class):
        """LLM 置信度 > 硬编码 → 使用 LLM"""
        email = MOCK_EMAILS[3]  # 顺捷云

        base = InvoiceAnalyzer().analyze(email.subject, email.text, email.html, email.has_attachments)

        mock_result = MagicMock()
        mock_result.invoice_type.value = "direct_pdf_link"
        mock_result.strategy.value = "direct_download"
        mock_result.confidence = 0.95  # 远高于 base
        mock_result.urls = ["https://shunjeyun.com/invoice/abc123"]
        mock_result.notes = "LLM识别成功"
        mock_result.selectors = []
        mock_result.platform_name = "顺捷云"
        mock_result.llm_used = True
        mock_result.reasoning = ""

        mock_llm_instance = MagicMock()
        mock_llm_instance.analyze.return_value = mock_result
        mock_llm_class.return_value = mock_llm_instance

        analyzer = InvoiceAnalyzerWithLLM()
        result = analyzer.analyze(email.subject, email.text, email.html, email.has_attachments)

        self.assertEqual(result.confidence, 0.95)
        self.assertTrue(result.llm_used)


class TestFallbackPreservesBaseResult(unittest.TestCase):
    """LLM 失败时保留硬编码结果"""

    @classmethod
    def setUpClass(cls):
        if InvoiceAnalyzerWithLLM is None:
            raise unittest.SkipTest("invoice_analyzer_v9 not available")
        cls.env_backup = os.environ.get("MINIMAX_API_KEY")
        os.environ["MINIMAX_API_KEY"] = "mock-api-key-for-test"

    @classmethod
    def tearDownClass(cls):
        if cls.env_backup is not None:
            os.environ["MINIMAX_API_KEY"] = cls.env_backup
        elif "MINIMAX_API_KEY" in os.environ:
            del os.environ["MINIMAX_API_KEY"]

    @patch("invoice_analyzer_v9.LLMInvoiceAnalyzer")
    def test_llm_fails_preserves_base(self, mock_llm_class):
        """LLM 抛出异常时，保留硬编码 base_result"""
        email = MOCK_EMAILS[3]  # 顺捷云

        base = InvoiceAnalyzer().analyze(email.subject, email.text, email.html, email.has_attachments)

        # LLM 抛出异常
        mock_llm_instance = MagicMock()
        mock_llm_instance.analyze.side_effect = RuntimeError("LLM API 错误")
        mock_llm_class.return_value = mock_llm_instance

        analyzer = InvoiceAnalyzerWithLLM()
        result = analyzer.analyze(email.subject, email.text, email.html, email.has_attachments)

        # 结果应该是 base 的，不是 LLM 的
        self.assertEqual(result.confidence, base.confidence)
        self.assertEqual(result.invoice_type.value, base.invoice_type.value)


class TestNonInvoiceSkip(unittest.TestCase):
    """非发票邮件 → skip"""

    @classmethod
    def setUpClass(cls):
        if InvoiceAnalyzerWithLLM is None:
            raise unittest.SkipTest("invoice_analyzer_v9 not available")
        cls.env_backup = os.environ.get("MINIMAX_API_KEY")
        if "MINIMAX_API_KEY" in os.environ:
            del os.environ["MINIMAX_API_KEY"]

    @classmethod
    def tearDownClass(cls):
        if cls.env_backup is not None:
            os.environ["MINIMAX_API_KEY"] = cls.env_backup

    def test_non_invoice_unknown(self):
        """订单确认邮件 → unknown 类型，跳过"""
        email = MOCK_EMAILS[4]
        analyzer = InvoiceAnalyzerWithLLM()
        result = analyzer.analyze(email.subject, email.text, email.html, email.has_attachments)
        # 应该是 unknown（base analyzer 识别不了 → 触发 LLM 或直接返回 unknown）
        self.assertEqual(result.invoice_type.value, email.expected_type)


if __name__ == "__main__":
    unittest.main(verbosity=2)
