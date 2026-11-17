from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "fetch_weread.py"
TEMPLATE = ROOT / "templates" / "dashboard.html"


def load_fetch_module():
    spec = importlib.util.spec_from_file_location("fetch_weread", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load fetch_weread.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class GatewayContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_fetch_module()

    def test_gateway_is_fixed_https_endpoint(self) -> None:
        self.assertEqual(
            self.module.GATEWAY_URL,
            "https://i.weread.qq.com/api/agent/gateway",
        )

    def test_opener_disables_redirects_and_environment_proxies(self) -> None:
        with patch(
            "urllib.request.getproxies",
            return_value={"https": "http://proxy.invalid"},
        ):
            opener = self.module.build_opener()
        proxy_handlers = [
            handler
            for handler in opener.handlers
            if handler.__class__.__name__ == "ProxyHandler"
        ]
        redirect_handlers = [
            handler
            for handler in opener.handlers
            if isinstance(handler, self.module.NoRedirectHandler)
        ]
        # ProxyHandler({}) deliberately installs no proxy handler and prevents
        # build_opener() from adding its environment-derived default.
        self.assertEqual(proxy_handlers, [])
        self.assertEqual(len(redirect_handlers), 1)

    def test_search_uses_documented_gateway_shape(self) -> None:
        with patch.object(self.module, "fetch_gateway", return_value={}) as fetch:
            self.module.fetch_command("wrk-test", "search", "系统思考")
        fetch.assert_called_once_with(
            "wrk-test",
            "/store/search",
            keyword="系统思考",
            count="10",
        )

    def test_command_stops_before_reading_credentials_without_confirmation(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "shelf"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("请求已停止", result.stderr)


class DashboardTemplateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = TEMPLATE.read_text(encoding="utf-8")

    def test_template_has_one_json_placeholder(self) -> None:
        placeholder = "{{DASHBOARD_DATA_JSON_ESCAPED_FOR_HTML}}"
        self.assertEqual(self.html.count(placeholder), 1)
        self.assertIn('type="application/json"', self.html)

    def test_external_content_is_not_rendered_as_html(self) -> None:
        self.assertIn(".textContent", self.html)
        self.assertNotIn("innerHTML", self.html)
        self.assertNotIn("insertAdjacentHTML", self.html)
        self.assertNotIn("document.write", self.html)

    def test_template_has_no_remote_assets(self) -> None:
        self.assertNotIn("http://", self.html)
        self.assertNotIn("https://", self.html)


if __name__ == "__main__":
    unittest.main()
