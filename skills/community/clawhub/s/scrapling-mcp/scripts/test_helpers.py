"""Offline regression checks; no browser, network or Scrapling install required.

Run: python -m unittest discover -s openclaw-skill-scrapling-mcp/scripts -p "test_*.py"
"""

import argparse
import contextlib
import io
import json
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

import scrapling_scrape as scrape
import scrapling_smoke_test as smoke


def response(status=200, html="<title>Fixture</title>"):
    page = types.SimpleNamespace(status=status, url="https://fixture.invalid/", html_content=html)
    page.css = lambda _: types.SimpleNamespace(get=lambda: "Fixture")
    return page


class SmokeTests(unittest.TestCase):
    def run_smoke(self, page=None, error=None, arguments=()):
        fetch = MagicMock(return_value=page or response(), side_effect=error)
        output = io.StringIO()
        with patch.object(smoke, "_pick_fetcher", return_value=("Fixture", fetch)), \
                contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            code = smoke.main(["https://fixture.invalid/", *arguments])
        return code, output.getvalue(), fetch

    def test_fetch_failure_is_unsuccessful(self):
        code, output, _ = self.run_smoke(error=TimeoutError("fixture timeout"))
        self.assertEqual(code, 1)
        self.assertIn("TimeoutError", output)

    def test_http_error_is_unsuccessful(self):
        self.assertEqual(self.run_smoke(page=response(status=503))[0], 1)

    def test_keywords_warn_without_failing_accessible_pages(self):
        for html in (
            '<html><h1>Contact us</h1><script src="https://challenges.cloudflare.com/turnstile/v0/api.js"></script></html>',
            '<article>This tutorial explains CAPTCHA integration.</article>',
        ):
            with self.subTest(html=html):
                code, output, _ = self.run_smoke(page=response(html=html))
                self.assertEqual(code, 0)
                self.assertIn("possible_block_indicator:", output)

    def test_strict_indicator_mode_is_unsuccessful(self):
        for html in (
            '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js"></script>',
            '<h1>CAPTCHA</h1>',
            '<h1>Access denied</h1>',
        ):
            with self.subTest(html=html):
                code, _, _ = self.run_smoke(page=response(html=html), arguments=("--fail-on-indicator",))
                self.assertEqual(code, 1)

    def test_generic_next_data_survives_attribute_order_and_empty_object(self):
        data = {"props": {"pageProps": {"title": "Unrelated English content"}}}
        html = "<script type='application/json' nonce='fixture' id='__NEXT_DATA__'>" + json.dumps(data) + "</script>"
        self.assertEqual(smoke._extract_next_data(html), data)
        code, output, _ = self.run_smoke(page=response(html=html), arguments=("--extract", "next_data"))
        self.assertEqual(code, 0)
        self.assertIn("Unrelated English content", output)
        self.assertEqual(smoke._extract_next_data('<script id="__NEXT_DATA__">{}</script>'), {})

    def test_missing_or_malformed_requested_data_fails(self):
        for html in ("<html>No embedded JSON</html>", '<script id="__NEXT_DATA__">bad json</script>'):
            with self.subTest(html=html):
                self.assertEqual(self.run_smoke(page=response(html=html), arguments=("--extract", "next_data"))[0], 1)

    def test_headful_and_browser_timeout_forwarded(self):
        code, _, fetch = self.run_smoke(arguments=("--fetcher", "stealthy", "--no-headless", "--timeout", "2"))
        self.assertEqual(code, 0)
        self.assertFalse(fetch.call_args.kwargs["headless"])
        self.assertEqual(fetch.call_args.kwargs["timeout"], 2000)

    def test_mixed_batch_remains_unsuccessful(self):
        fetch = MagicMock(side_effect=[TimeoutError("fixture"), response()])
        with patch.object(smoke, "_pick_fetcher", return_value=("Fixture", fetch)), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(smoke.main(["https://fixture.invalid/a", "https://fixture.invalid/b"]), 1)
        self.assertEqual(fetch.call_count, 2)


class ScrapeTests(unittest.TestCase):
    def args(self, **overrides):
        values = dict(
            mode="fetcher", url="https://fixture.invalid/", timeout=3,
            adaptive=False, auto_save=False, headless=True,
            network_idle=False, solve_cloudflare=False,
        )
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_http_import_does_not_require_browser_session_and_enables_storage(self):
        fetchers = types.ModuleType("scrapling.fetchers")
        session_class = MagicMock()
        expected = response()
        session_class.return_value.__enter__.return_value.get.return_value = expected
        # Deliberately supply no StealthySession (and no removed DynamicSession).
        fetchers.FetcherSession = session_class
        with patch.dict(sys.modules, {"scrapling.fetchers": fetchers}):
            self.assertIs(scrape._fetch(self.args(auto_save=True)), expected)
        self.assertTrue(session_class.call_args.kwargs["selector_config"]["adaptive"])
        self.assertEqual(session_class.return_value.__enter__.return_value.get.call_args.kwargs["timeout"], 3)

    def test_browser_settings_go_to_the_correct_scope(self):
        fetchers = types.ModuleType("scrapling.fetchers")
        session_class = MagicMock()
        fetchers.StealthySession = session_class
        with patch.dict(sys.modules, {"scrapling.fetchers": fetchers}):
            scrape._fetch(self.args(mode="stealthy", headless=False, network_idle=True, solve_cloudflare=True))
        self.assertFalse(session_class.call_args.kwargs["headless"])
        self.assertNotIn("solve_cloudflare", session_class.call_args.kwargs)
        call = session_class.return_value.__enter__.return_value.fetch.call_args
        self.assertEqual(call.kwargs["timeout"], 3000)
        self.assertTrue(call.kwargs["network_idle"])
        self.assertTrue(call.kwargs["solve_cloudflare"])

    def test_selection_errors_are_not_silently_retried_without_adaptive(self):
        page = response()
        page.css = MagicMock(side_effect=TypeError("selection fixture"))
        with self.assertRaises(TypeError):
            scrape._select(page, css="h1", xpath=None, adaptive=True, auto_save=True)
        self.assertEqual(page.css.call_count, 1)

    def test_extraction_failure_returns_nonzero(self):
        with patch.object(scrape, "_fetch", side_effect=TimeoutError("fixture")), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(scrape.main(["--url", "https://fixture.invalid/", "--css", "h1"]), 1)


if __name__ == "__main__":
    unittest.main()
