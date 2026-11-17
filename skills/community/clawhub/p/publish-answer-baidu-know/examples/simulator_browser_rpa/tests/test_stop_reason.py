# -*- coding: utf-8 -*-
"""RPA 失败结果与 artifacts 单元测试。"""
from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from service.adapter import BatchItem, SimulatorBrowserRpaAdapter
from service.adapter.base import BatchSubmitResult


class TestBatchSubmitFailureResult(unittest.IsolatedAsyncioTestCase):
    @patch("service.adapter.simulator_rpa.release_lease")
    @patch("service.adapter.simulator_rpa.submit_batch_rpa", new_callable=AsyncMock)
    @patch("service.adapter.simulator_rpa.pick_web_account")
    @patch("service.adapter.simulator_rpa.find_chrome_executable", return_value="C:/Chrome/chrome.exe")
    async def test_rpa_error_converts_to_failed_result(
        self,
        _chrome: MagicMock,
        mock_pick: MagicMock,
        mock_rpa: AsyncMock,
        _release: MagicMock,
    ) -> None:
        mock_pick.return_value = {
            "profile_dir": "/tmp/profile",
            "lease_token": "tok",
        }
        mock_rpa.return_value = BatchSubmitResult(
            ok=False,
            batch_id=None,
            submitted_count=0,
            submitted_amount=0.0,
            error_msg="登录第一步失败：timeout",
            artifacts={"adapter": "simulator_rpa", "screenshot": "/tmp/art/x.png"},
        )

        adapter = SimulatorBrowserRpaAdapter(artifacts_dir="/tmp/art")
        items = [BatchItem(row_index=1, name="A", account="1", amount=1.0)]
        result = await adapter.submit_batch("acct-demo-001", items)

        self.assertFalse(result.ok)
        self.assertIn("登录第一步失败", result.error_msg or "")
        self.assertEqual(result.artifacts.get("adapter"), "simulator_rpa")
        self.assertEqual(result.artifacts.get("screenshot"), "/tmp/art/x.png")

    @patch("service.adapter.simulator_rpa.release_lease")
    @patch("service.adapter.simulator_rpa.submit_batch_rpa", new_callable=AsyncMock)
    @patch("service.adapter.simulator_rpa.pick_web_account")
    @patch("service.adapter.simulator_rpa.find_chrome_executable", return_value="C:/Chrome/chrome.exe")
    async def test_unexpected_error_includes_adapter_name(
        self,
        _chrome: MagicMock,
        mock_pick: MagicMock,
        mock_rpa: AsyncMock,
        _release: MagicMock,
    ) -> None:
        mock_pick.return_value = {
            "profile_dir": "/tmp/profile",
            "lease_token": "tok",
        }
        mock_rpa.side_effect = RuntimeError("boom")

        adapter = SimulatorBrowserRpaAdapter(artifacts_dir=None)
        items = [BatchItem(row_index=1, name="A", account="1", amount=1.0)]
        result = await adapter.submit_batch("acct-demo-001", items)

        self.assertFalse(result.ok)
        self.assertIn("未预期异常", result.error_msg or "")
        self.assertEqual(result.artifacts.get("adapter"), "simulator_rpa")
        self.assertNotIn("screenshot", result.artifacts)


if __name__ == "__main__":
    unittest.main()
