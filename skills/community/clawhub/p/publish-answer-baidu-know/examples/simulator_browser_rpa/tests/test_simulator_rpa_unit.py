# -*- coding: utf-8 -*-
"""SimulatorBrowserRpaAdapter 单元测试（不启动真实浏览器）。"""
from __future__ import annotations

import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from service.adapter import BatchItem, SimulatorBrowserRpaAdapter
from service.browser_session import CHROME_LAUNCH_ARGS
from service.simulator_playwright import RpaError


class TestSimulatorRpaUnit(unittest.IsolatedAsyncioTestCase):
    async def test_submit_batch_empty_items(self) -> None:
        adapter = SimulatorBrowserRpaAdapter()
        result = await adapter.submit_batch("acct-demo-001", [])
        self.assertFalse(result.ok)
        self.assertIn("items", result.error_msg or "")

    @patch("service.adapter.simulator_rpa.find_chrome_executable", return_value=None)
    async def test_no_chrome_returns_error_without_launch(self, _chrome: MagicMock) -> None:
        adapter = SimulatorBrowserRpaAdapter()
        items = [BatchItem(row_index=1, name="A", account="1", amount=1.0)]
        result = await adapter.submit_batch("acct-demo-001", items)
        self.assertFalse(result.ok)
        msg = result.error_msg or ""
        self.assertTrue("Chrome" in msg or "Edge" in msg or "浏览器" in msg)

    def test_chrome_launch_args_must_not_contain_url(self) -> None:
        for arg in CHROME_LAUNCH_ARGS:
            lowered = arg.lower()
            self.assertFalse(lowered.startswith("http://"))
            self.assertFalse(lowered.startswith("https://"))
            self.assertFalse(lowered.startswith("file://"))

    @patch("service.adapter.simulator_rpa.submit_batch_rpa", new_callable=AsyncMock)
    @patch("service.adapter.simulator_rpa.pick_web_account")
    @patch("service.adapter.simulator_rpa.find_chrome_executable", return_value="C:/Chrome/chrome.exe")
    async def test_adapter_delegates_to_playwright_with_account_url(
        self,
        _chrome: MagicMock,
        mock_pick: MagicMock,
        mock_rpa: AsyncMock,
    ) -> None:
        from service.adapter.base import BatchSubmitResult

        mock_pick.return_value = {
            "login_id": "demo001",
            "profile_dir": "/tmp/profile",
            "url": "file:///demo/demo_app.html",
            "lease_token": "tok-1",
        }
        mock_rpa.return_value = BatchSubmitResult(
            ok=False,
            batch_id=None,
            submitted_count=0,
            submitted_amount=0.0,
            error_msg="login fail",
            artifacts={"adapter": "simulator_rpa"},
        )

        adapter = SimulatorBrowserRpaAdapter(artifacts_dir="/tmp/art")
        items = [BatchItem(row_index=1, name="A", account="1", amount=1.0)]
        result = await adapter.submit_batch("acct-demo-001", items)

        self.assertFalse(result.ok)
        mock_rpa.assert_awaited_once()
        call_kwargs = mock_rpa.call_args.kwargs
        self.assertEqual(call_kwargs["base_url"], "file:///demo/demo_app.html")
        for arg in CHROME_LAUNCH_ARGS:
            self.assertNotIn(arg, call_kwargs["base_url"])

    @patch("service.simulator_playwright.start_browser_session", new_callable=AsyncMock)
    async def test_playwright_opens_url_via_goto_not_launch_args(self, mock_start: AsyncMock) -> None:
        from service.simulator_playwright import submit_batch_rpa

        page = AsyncMock()
        page.goto = AsyncMock()
        mock_start.return_value = (MagicMock(), MagicMock(), page)

        account = {"profile_dir": "/tmp/p", "login_id": "demo001"}
        items = [BatchItem(row_index=1, name="A", account="1", amount=1.0)]

        with patch(
            "service.simulator_playwright._wait_portal_gate",
            new_callable=AsyncMock,
            return_value=None,
        ):
            with patch(
                "service.simulator_playwright._login",
                new_callable=AsyncMock,
                side_effect=RpaError("login fail"),
            ):
                with patch(
                    "service.simulator_playwright.find_chrome_executable",
                    return_value="C:/Chrome/chrome.exe",
                ):
                    with patch(
                        "service.simulator_playwright.close_browser_session",
                        new_callable=AsyncMock,
                    ):
                        result = await submit_batch_rpa(
                            account,
                            target="acct-demo-001",
                            items=items,
                            base_url="file:///demo/demo_app.html",
                            artifacts_dir=None,
                        )

        self.assertFalse(result.ok)
        page.goto.assert_awaited_once()
        goto_url = page.goto.call_args[0][0]
        self.assertEqual(goto_url, "file:///demo/demo_app.html")
        for arg in CHROME_LAUNCH_ARGS:
            self.assertNotIn(arg, goto_url)

    async def test_safe_screenshot_without_artifacts_dir(self) -> None:
        from service.simulator_playwright import _safe_screenshot

        page = AsyncMock()
        self.assertIsNone(await _safe_screenshot(page, None, "tag"))


class TestSyncHelpers(unittest.TestCase):
    def test_asyncio_run_smoke(self) -> None:
        async def _noop() -> bool:
            return True

        self.assertTrue(asyncio.run(_noop()))


if __name__ == "__main__":
    unittest.main()
