# -*- coding: utf-8 -*-
"""adapter 工厂 dispatch 单元测试。"""
from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from service.adapter import (
    BatchItem,
    MockBatchAdapter,
    SimulatorBrowserRpaAdapter,
    select_adapter,
)


class TestAdapterDispatch(unittest.TestCase):
    def test_default_returns_simulator_rpa(self) -> None:
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("OPENCLAW_TEST_TARGET", None)
            adapter = select_adapter()
            self.assertIsInstance(adapter, SimulatorBrowserRpaAdapter)

    def test_unit_returns_mock(self) -> None:
        with patch.dict(os.environ, {"OPENCLAW_TEST_TARGET": "unit"}):
            self.assertIsInstance(select_adapter(), MockBatchAdapter)

    def test_mock_returns_mock(self) -> None:
        with patch.dict(os.environ, {"OPENCLAW_TEST_TARGET": "mock"}):
            self.assertIsInstance(select_adapter(), MockBatchAdapter)

    def test_simulator_rpa_returns_simulator(self) -> None:
        with patch.dict(os.environ, {"OPENCLAW_TEST_TARGET": "simulator_rpa"}):
            self.assertIsInstance(select_adapter(), SimulatorBrowserRpaAdapter)

    def test_real_rpa_falls_back_to_mock(self) -> None:
        with patch.dict(os.environ, {"OPENCLAW_TEST_TARGET": "real_rpa"}):
            self.assertIsInstance(select_adapter(), MockBatchAdapter)

    def test_unknown_target_falls_back_simulator_rpa(self) -> None:
        with patch.dict(os.environ, {"OPENCLAW_TEST_TARGET": "simulator_api"}):
            self.assertIsInstance(select_adapter(), SimulatorBrowserRpaAdapter)


class TestMockAdapter(unittest.IsolatedAsyncioTestCase):
    async def test_mock_success(self) -> None:
        items = [
            BatchItem(row_index=1, name="Alice", account="1001", amount=10.5),
            BatchItem(row_index=2, name="Bob", account="1002", amount=20.0),
        ]
        result = await MockBatchAdapter().submit_batch("acct-demo-001", items)
        self.assertTrue(result.ok)
        self.assertEqual(result.submitted_count, 2)
        self.assertEqual(result.submitted_amount, 30.5)
        self.assertTrue((result.batch_id or "").startswith("MOCK-"))

    async def test_mock_empty_items(self) -> None:
        result = await MockBatchAdapter().submit_batch("acct-demo-001", [])
        self.assertFalse(result.ok)
        self.assertEqual(result.error_msg, "items 为空")


if __name__ == "__main__":
    unittest.main()
