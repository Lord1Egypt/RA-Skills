# -*- coding: utf-8 -*-
"""人工验证检测单元测试（DOM 精准检测，不依赖真实浏览器）。"""
from __future__ import annotations

import asyncio
import time
import unittest

from service.human_verification import (
    HumanVerificationWaitResult,
    detect_human_verification,
    detect_human_verification_from_text,
    wait_human_verification_if_present,
    wait_save_login_countdown_if_present,
)


SLIDER_HTML = """
<div class="vc-captcha-verify slide">
  <div class="captcha_verify_bar--title">请完成下列验证后继续</div>
  <div class="captcha-slider-tips">按住左边按钮拖动完成上方拼图</div>
</div>
"""

SMS_HTML = """
<div class="second-verify-panel">
  <div class="uc-ui-verify_sms-input">
    <div class="uc-ui-verify-new_header-title">短信验证</div>
    <input placeholder="手机号" />
    <input placeholder="请输入验证码" />
    <button>获取验证码</button>
  </div>
</div>
"""

SEARCH_RESULTS_HTML = """
<div id="search-result-container">
  <div data-result-item="1">RPA 滑块验证码识别教程</div>
  <div data-result-item="2">短信验证码自动化</div>
</div>
"""


class MockLocator:
    def __init__(self, selector: str, visible: set[str], texts: dict[str, str]) -> None:
        self._selector = selector
        self._visible = visible
        self._texts = texts

    @property
    def first(self) -> MockLocator:
        return self

    async def is_visible(self, timeout: int = 500) -> bool:
        return self._selector in self._visible

    async def inner_text(self, timeout: int = 1000) -> str:
        return self._texts.get(self._selector, "")

    async def count(self) -> int:
        return 1 if self._selector in self._visible else 0


class MockPage:
    def __init__(self, visible: set[str], texts: dict[str, str] | None = None) -> None:
        self._visible = visible
        self._texts = texts or {}

    def locator(self, selector: str) -> MockLocator:
        return MockLocator(selector, self._visible, self._texts)


class TestHumanVerificationFromText(unittest.TestCase):
    def test_slider_dom_detect(self) -> None:
        state = detect_human_verification_from_text(SLIDER_HTML)
        self.assertTrue(state.present)
        self.assertEqual(state.kind, "slider")
        self.assertTrue(state.selector)

    def test_sms_dom_detect(self) -> None:
        state = detect_human_verification_from_text(SMS_HTML)
        self.assertTrue(state.present)
        self.assertEqual(state.kind, "sms")
        self.assertTrue(state.selector)

    def test_search_results_not_misclassified(self) -> None:
        state = detect_human_verification_from_text(SEARCH_RESULTS_HTML)
        self.assertFalse(state.present)

    def test_body_keywords_without_dom_not_misclassified(self) -> None:
        text = "RPA 滑块验证码识别教程\n短信验证码自动化"
        state = detect_human_verification_from_text(text)
        self.assertFalse(state.present)


class TestHumanVerificationDomDetect(unittest.TestCase):
    def test_slider_dom_visible(self) -> None:
        page = MockPage(
            {".vc-captcha-verify.slide"},
            {".vc-captcha-verify.slide": "请完成下列验证后继续"},
        )
        state = asyncio.run(detect_human_verification(page))
        self.assertTrue(state.present)
        self.assertEqual(state.kind, "slider")
        self.assertEqual(state.selector, ".vc-captcha-verify.slide")

    def test_sms_dom_visible(self) -> None:
        page = MockPage(
            {".second-verify-panel"},
            {".second-verify-panel": "短信验证 获取验证码"},
        )
        state = asyncio.run(detect_human_verification(page))
        self.assertTrue(state.present)
        self.assertEqual(state.kind, "sms")

    def test_no_verification_when_empty(self) -> None:
        page = MockPage(set())
        state = asyncio.run(detect_human_verification(page))
        self.assertFalse(state.present)


class TestSaveLoginCountdown(unittest.TestCase):
    def test_wait_not_present_no_delay(self) -> None:
        page = MockPage(set())
        start = time.monotonic()
        result = asyncio.run(wait_save_login_countdown_if_present(page, timeout_sec=8))
        elapsed = time.monotonic() - start
        self.assertFalse(result)
        self.assertLess(elapsed, 1.0)


class TestHumanVerificationWait(unittest.TestCase):
    def test_wait_timeout_slider_dom(self) -> None:
        page = MockPage(
            {".vc-captcha-verify.slide"},
            {".vc-captcha-verify.slide": "请完成下列验证后继续"},
        )
        result = asyncio.run(
            wait_human_verification_if_present(page, wait_sec=1, stage="search_verification")
        )
        self.assertIsInstance(result, HumanVerificationWaitResult)
        self.assertTrue(result.timed_out)
        self.assertEqual(result.code, "SLIDER_VERIFICATION_TIMEOUT")
        self.assertIn("滑块验证码未在 1 秒内完成", result.message)
        self.assertEqual(result.stage, "search_verification")

    def test_wait_timeout_sms_dom(self) -> None:
        page = MockPage(
            {".second-verify-panel"},
            {".second-verify-panel": "短信验证 获取验证码"},
        )
        result = asyncio.run(
            wait_human_verification_if_present(page, wait_sec=1, stage="login_check")
        )
        self.assertIsInstance(result, HumanVerificationWaitResult)
        self.assertTrue(result.timed_out)
        self.assertEqual(result.code, "SMS_VERIFICATION_TIMEOUT")
        self.assertEqual(result.stage, "login_check")

    def test_collect_no_verification_immediate_none(self) -> None:
        page = MockPage(set())
        start = time.monotonic()
        err = asyncio.run(wait_human_verification_if_present(page, wait_sec=180, stage="collect"))
        elapsed = time.monotonic() - start
        self.assertIsNone(err)
        self.assertLess(elapsed, 1.0)


if __name__ == "__main__":
    unittest.main()
