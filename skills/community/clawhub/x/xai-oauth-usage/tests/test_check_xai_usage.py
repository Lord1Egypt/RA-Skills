from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
import urllib.error
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import Any
from unittest.mock import patch


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "check_xai_usage.py"
SPEC = importlib.util.spec_from_file_location("check_xai_usage", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load check_xai_usage.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class FakeResponse:
    def __init__(self, payload: dict[str, Any], status: int = 200) -> None:
        self.status = status
        self._body = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self._body


class FakeOpener:
    def __init__(self, result: FakeResponse | Exception) -> None:
        self.result = result
        self.request: Any = None

    def open(self, request: Any, timeout: float) -> FakeResponse:
        self.request = request
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class XaiOauthUsageTests(unittest.TestCase):
    def test_reads_only_xai_oauth_access_token(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            auth_file = Path(temp_dir) / "auth.json"
            auth_file.write_text(
                json.dumps(
                    {
                        "providers": {
                            "xai-oauth": {
                                "tokens": {
                                    "access_token": "secret-access-token",
                                    "refresh_token": "secret-refresh-token",
                                }
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            token = MODULE.read_access_token(auth_file)

        self.assertEqual(token, "secret-access-token")

    def test_fetch_usage_returns_sanitized_summary(self) -> None:
        payload = {
            "config": {
                "currentPeriod": {
                    "type": "weekly",
                    "start": "2099-01-01T00:00:00Z",
                    "end": "2099-01-08T00:00:00Z",
                },
                "creditUsagePercent": 75,
                "isUnifiedBillingUser": True,
                "productUsage": [{"product": "GrokBuild", "usagePercent": 80}],
            }
        }
        opener = FakeOpener(FakeResponse(payload))

        with patch.object(MODULE.urllib.request, "build_opener", return_value=opener):
            result = MODULE.fetch_usage("secret-access-token", timeout=3)

        self.assertEqual(opener.request.full_url, MODULE.ENDPOINT)
        self.assertEqual(opener.request.get_header("Authorization"), "Bearer secret-access-token")
        self.assertEqual(
            opener.request.get_header("X-grok-client-identifier"),
            "hermes-xai-usage-checker",
        )
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["used_percent"], 75.0)
        self.assertEqual(result["remaining_percent"], 25.0)
        self.assertEqual(result["source_host"], "cli-chat-proxy.grok.com")
        self.assertEqual(result["product_usage"], [{"product": "GrokBuild", "usage_percent": 80.0}])
        self.assertNotIn("secret", json.dumps(result))
        self.assertFalse(any("token" in key.lower() for key in result))

    def test_credential_rejection_does_not_retry(self) -> None:
        error = urllib.error.HTTPError(MODULE.ENDPOINT, 403, "Forbidden", {}, None)
        opener = FakeOpener(error)

        try:
            with patch.object(MODULE.urllib.request, "build_opener", return_value=opener):
                with self.assertRaises(MODULE.UsageError) as raised:
                    MODULE.fetch_usage("secret-access-token", timeout=3)
        finally:
            error.close()

        self.assertEqual(raised.exception.http_status, 403)
        self.assertIn("no reauthentication", str(raised.exception))
        self.assertNotIn("secret-access-token", str(raised.exception))

    def test_redirects_are_refused(self) -> None:
        handler = MODULE.NoRedirect()
        self.assertIsNone(handler.redirect_request(None, None, 302, "Found", {}, "https://example.com"))

    def test_language_environment_overrides_hermes_config(self) -> None:
        with (
            patch.dict(MODULE.os.environ, {"HERMES_LANGUAGE": "ja-JP"}, clear=True),
            patch.object(MODULE.shutil, "which") as which,
        ):
            language = MODULE.detect_language()

        self.assertEqual(language, "ja")
        which.assert_not_called()

    def test_language_uses_hermes_config(self) -> None:
        completed = MODULE.subprocess.CompletedProcess(
            ["/usr/local/bin/hermes", "config", "get", "display.language"],
            0,
            stdout="japanese\n",
            stderr="",
        )
        with (
            patch.dict(MODULE.os.environ, {}, clear=True),
            patch.object(MODULE.shutil, "which", return_value="/usr/local/bin/hermes"),
            patch.object(MODULE.subprocess, "run", return_value=completed) as run,
        ):
            language = MODULE.detect_language()

        self.assertEqual(language, "ja")
        run.assert_called_once_with(
            ["/usr/local/bin/hermes", "config", "get", "display.language"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )

    def test_language_defaults_to_english(self) -> None:
        cases = ["en", "fr", "unknown", ""]
        for value in cases:
            with self.subTest(value=value):
                completed = MODULE.subprocess.CompletedProcess(
                    ["hermes", "config", "get", "display.language"],
                    0,
                    stdout=value,
                    stderr="",
                )
                with (
                    patch.dict(MODULE.os.environ, {}, clear=True),
                    patch.object(MODULE.shutil, "which", return_value="hermes"),
                    patch.object(MODULE.subprocess, "run", return_value=completed),
                ):
                    self.assertEqual(MODULE.detect_language(), "en")

        with (
            patch.dict(MODULE.os.environ, {}, clear=True),
            patch.object(MODULE.shutil, "which", return_value="hermes"),
            patch.object(MODULE.subprocess, "run", side_effect=MODULE.subprocess.TimeoutExpired("hermes", 3)),
        ):
            self.assertEqual(MODULE.detect_language(), "en")

        failed = MODULE.subprocess.CompletedProcess(
            ["hermes", "config", "get", "display.language"],
            1,
            stdout="ja",
            stderr="config error",
        )
        with (
            patch.dict(MODULE.os.environ, {}, clear=True),
            patch.object(MODULE.shutil, "which", return_value="hermes"),
            patch.object(MODULE.subprocess, "run", return_value=failed),
        ):
            self.assertEqual(MODULE.detect_language(), "en")

    def test_human_output_follows_language(self) -> None:
        result = {
            "used_percent": 75.0,
            "remaining_percent": 25.0,
            "period_end_jst": "2099-01-08T09:00:00+09:00",
            "remaining_seconds": 7380,
            "product_usage": [{"product": "GrokBuild", "usage_percent": 80.0}],
        }

        japanese = io.StringIO()
        with redirect_stdout(japanese):
            MODULE.print_human(result, "ja")
        self.assertEqual(
            japanese.getvalue(),
            "xAI OAuth 利用枠\n"
            "週間利用率: 75.0%（残り 25.0%）\n"
            "リセット: 2099-01-08T09:00:00+09:00\n"
            "残り時間: 2時間3分\n"
            "内訳:\n"
            "- GrokBuild: 80.0%\n",
        )

        english = io.StringIO()
        with redirect_stdout(english):
            MODULE.print_human(result, "en")
        self.assertEqual(
            english.getvalue(),
            "xAI OAuth Usage\n"
            "Weekly usage: 75.0% (25.0% remaining)\n"
            "Reset: 2099-01-08T09:00:00+09:00\n"
            "Time remaining: 2h 3m\n"
            "Breakdown:\n"
            "- GrokBuild: 80.0%\n",
        )

    def test_human_error_follows_language_and_json_stays_english(self) -> None:
        args = MODULE.argparse.Namespace(
            auth_file=Path("missing.json"), timeout=3.0, as_json=False
        )
        error = MODULE.UsageError(
            "xai-oauth access token is not configured",
            "xai-oauth access tokenが設定されていません",
        )

        stderr = io.StringIO()
        with (
            patch.object(MODULE, "parse_args", return_value=args),
            patch.object(MODULE, "detect_language", return_value="ja"),
            patch.object(MODULE, "read_access_token", side_effect=error),
            redirect_stderr(stderr),
        ):
            self.assertEqual(MODULE.main(), 1)
        self.assertEqual(
            stderr.getvalue(),
            "xAI OAuth利用枠を確認できません: xai-oauth access tokenが設定されていません\n",
        )

        stderr = io.StringIO()
        with (
            patch.object(MODULE, "parse_args", return_value=args),
            patch.object(MODULE, "detect_language", return_value="en"),
            patch.object(MODULE, "read_access_token", side_effect=error),
            redirect_stderr(stderr),
        ):
            self.assertEqual(MODULE.main(), 1)
        self.assertEqual(
            stderr.getvalue(),
            "Could not check xAI OAuth usage: xai-oauth access token is not configured\n",
        )

        args.as_json = True
        stdout = io.StringIO()
        with (
            patch.object(MODULE, "parse_args", return_value=args),
            patch.object(MODULE, "detect_language") as detect_language,
            patch.object(MODULE, "read_access_token", side_effect=error),
            redirect_stdout(stdout),
        ):
            self.assertEqual(MODULE.main(), 1)
        detect_language.assert_not_called()
        self.assertEqual(json.loads(stdout.getvalue())["error"], str(error))


if __name__ == "__main__":
    unittest.main()
