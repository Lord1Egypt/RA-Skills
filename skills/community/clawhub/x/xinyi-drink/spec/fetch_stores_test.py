from __future__ import annotations

import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import fetch_stores


class FetchStoresScriptTest(unittest.TestCase):
    @patch.object(
        fetch_stores,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_fetch_stores_outputs_table_text(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        response = urlopen_mock.return_value.__enter__.return_value
        response.read.return_value = (
            '{"data":{"stores":[{"name":"幂茶幂咖望京店","address":"北京市朝阳区望京街9号",'
            '"facilities":"外摆区，休息区，宠物友好。",'
            '"storeMobile":"010-12345678",'
            '"businessStatus":1,"operatingStatus":1,"realtimeState":1,'
            '"labels":[{"name":"休息区"}],"makingCupCount":4,"makingCupMinutes":18,'
            '"storeType":2,"supportUnattendedMode":1}]}}'
        ).encode("utf-8")

        stdout = io.StringIO()

        with patch("sys.stdout", stdout):
            exit_code = fetch_stores.main()

        output = stdout.getvalue()

        self.assertEqual(exit_code, 0)
        self.assertIn("## 门店列表", output)
        self.assertIn("幂茶幂咖望京店", output)
        self.assertIn("010-12345678", output)
        self.assertIn("宠物友好", output)
        self.assertIn("外摆区，休息区，宠物友好。", output)
        self.assertIn("休息区", output)
        self.assertIn("Box 门店", output)
        self.assertIn("支持无人模式", output)
        self.assertNotIn('"stores"', output)

    @patch.object(
        fetch_stores,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen")
    def test_fetch_stores_outputs_debug_logs_to_stderr(
        self,
        urlopen_mock,
        _load_config_mock,
    ) -> None:
        response = urlopen_mock.return_value.__enter__.return_value
        response.read.return_value = '{"data":{"stores":[]}}'.encode("utf-8")

        stdout = io.StringIO()
        stderr = io.StringIO()

        with patch.object(
            sys,
            "argv",
            ["fetch_stores.py", "--debug"],
        ), patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            exit_code = fetch_stores.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("DEBUG fetch_stores: fetching stores from http://127.0.0.1:8020/skill/xinyi/stores", stderr.getvalue())
        self.assertIn("## 门店列表", stdout.getvalue())

    @patch.object(
        fetch_stores,
        "load_config",
        return_value={
            "apiBaseUrl": "http://127.0.0.1:8020",
            "timeoutSeconds": 5,
        },
    )
    @patch("urllib.request.urlopen", side_effect=OSError("connection refused"))
    def test_fetch_stores_outputs_graceful_fallback_when_request_fails(
        self,
        _urlopen_mock,
        _load_config_mock,
    ) -> None:
        stdout = io.StringIO()

        with patch("sys.stdout", stdout):
            exit_code = fetch_stores.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("## 实时数据状态", stdout.getvalue())
        self.assertIn("门店实时数据暂时没拿到：网络请求失败", stdout.getvalue())
        self.assertIn("不要编造门店名、地址、电话或排队信息", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
