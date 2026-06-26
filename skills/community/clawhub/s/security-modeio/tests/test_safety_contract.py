#!/usr/bin/env python3

import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import call, patch

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = REPO_ROOT / "security"
SCRIPT_PATH = REPO_ROOT / "security" / "scripts" / "safety.py"

sys.path.insert(0, str(PACKAGE_ROOT))
from modeio_guardrail.cli import safety as guardrail_safety  # noqa: E402


class _DummyResponse:
    def __init__(self, *, status_code=200, payload=None, raise_error=None):
        self.status_code = status_code
        self._payload = {} if payload is None else payload
        self._raise_error = raise_error

    def raise_for_status(self):
        if self._raise_error is not None:
            raise self._raise_error

    def json(self):
        if isinstance(self._payload, Exception):
            raise self._payload
        return self._payload


class TestSafetyContract(unittest.TestCase):
    def _run_cli(self, args, env=None):
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH)] + args,
            capture_output=True,
            text=True,
            env=merged_env,
        )

    def _run_main(self, args):
        out = StringIO()
        err = StringIO()
        exit_code = 0
        with (
            patch.object(sys, "argv", ["safety.py", *args]),
            redirect_stdout(out),
            redirect_stderr(err),
        ):
            try:
                guardrail_safety.main()
            except SystemExit as exc:
                code = exc.code if isinstance(exc.code, int) else 1
                exit_code = code
        return exit_code, out.getvalue(), err.getvalue()

    def test_success_envelope_shape(self):
        payload = guardrail_safety._success_envelope({"approved": True})
        self.assertTrue(payload["success"])
        self.assertEqual(payload["tool"], "security")
        self.assertEqual(payload["mode"], "api")
        self.assertEqual(payload["data"]["approved"], True)

    def test_error_envelope_shape(self):
        payload = guardrail_safety._error_envelope(
            error_type="network_error",
            message="request failed",
            status_code=503,
        )
        self.assertFalse(payload["success"])
        self.assertEqual(payload["tool"], "security")
        self.assertEqual(payload["mode"], "api")
        self.assertEqual(payload["error"]["type"], "network_error")
        self.assertEqual(payload["error"]["status_code"], 503)

    def test_json_validation_error_for_empty_input(self):
        result = self._run_cli(["--input", "   ", "--json"])
        self.assertEqual(result.returncode, 1)

        payload = json.loads(result.stdout)
        self.assertFalse(payload["success"])
        self.assertEqual(payload["error"]["type"], "validation_error")

    def test_json_network_error_envelope(self):
        result = self._run_cli(
            ["--input", "Delete all log files in production", "--json"],
            env={"SAFETY_API_URL": "http://127.0.0.1:9"},
        )
        self.assertEqual(result.returncode, 1)

        payload = json.loads(result.stdout)
        self.assertFalse(payload["success"])
        self.assertEqual(payload["tool"], "security")
        self.assertIn(payload["error"]["type"], ("network_error", "dependency_error"))
        if payload["error"]["type"] == "dependency_error":
            self.assertIn("requests package is required", payload["error"]["message"])

    def test_post_with_retry_retries_503_then_succeeds(self):
        first = _DummyResponse(status_code=503)
        second = _DummyResponse(status_code=200)
        with patch.object(
            guardrail_safety.requests, "post", side_effect=[first, second]
        ) as mock_post:
            with patch.object(guardrail_safety.time, "sleep") as mock_sleep:
                result = guardrail_safety._post_with_retry(
                    "https://example.com", json_payload={"instruction": "x"}
                )

        self.assertIs(result, second)
        self.assertEqual(mock_post.call_count, 2)
        mock_sleep.assert_called_once_with(1.0)

    def test_post_with_retry_retries_connection_error_then_succeeds(self):
        conn_error = guardrail_safety.requests.ConnectionError("connection failed")
        ok = _DummyResponse(status_code=200)

        with patch.object(
            guardrail_safety.requests, "post", side_effect=[conn_error, ok]
        ) as mock_post:
            with patch.object(guardrail_safety.time, "sleep") as mock_sleep:
                result = guardrail_safety._post_with_retry(
                    "https://example.com", json_payload={"instruction": "x"}
                )

        self.assertIs(result, ok)
        self.assertEqual(mock_post.call_count, 2)
        mock_sleep.assert_called_once_with(1.0)

    def test_post_with_retry_timeout_exhausted_raises(self):
        timeout_error = guardrail_safety.requests.Timeout("timed out")
        with patch.object(
            guardrail_safety.requests,
            "post",
            side_effect=[timeout_error, timeout_error, timeout_error],
        ) as mock_post:
            with patch.object(guardrail_safety.time, "sleep") as mock_sleep:
                with self.assertRaises(guardrail_safety.requests.Timeout):
                    guardrail_safety._post_with_retry(
                        "https://example.com", json_payload={"instruction": "x"}
                    )

        self.assertEqual(mock_post.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)
        mock_sleep.assert_has_calls([call(1.0), call(2.0)])

    def test_detect_safety_passes_context_and_target(self):
        response = _DummyResponse(payload={"approved": True})
        with patch.object(
            guardrail_safety, "_post_with_retry", return_value=response
        ) as mock_post:
            payload = guardrail_safety.detect_safety(
                "DROP TABLE users", context="production", target="db.users"
            )

        self.assertTrue(payload["approved"])
        mock_post.assert_called_once_with(
            guardrail_safety.URL,
            json_payload={
                "instruction": "DROP TABLE users",
                "context": "production",
                "target": "db.users",
            },
        )

    def test_detect_safety_omits_empty_optional_fields(self):
        response = _DummyResponse(payload={"approved": True})
        with patch.object(
            guardrail_safety, "_post_with_retry", return_value=response
        ) as mock_post:
            payload = guardrail_safety.detect_safety("ls -la")

        self.assertTrue(payload["approved"])
        kwargs = mock_post.call_args.kwargs
        self.assertEqual(kwargs["json_payload"], {"instruction": "ls -la"})

    def test_main_json_http_error_is_classified_as_api_error(self):
        http_error = guardrail_safety.requests.HTTPError("upstream 503")
        response = guardrail_safety.requests.Response()
        response.status_code = 503
        http_error.response = response

        with patch.object(guardrail_safety, "detect_safety", side_effect=http_error):
            code, stdout, _ = self._run_main(["--input", "DROP TABLE users", "--json"])

        self.assertEqual(code, 1)
        payload = json.loads(stdout)
        self.assertEqual(payload["error"]["type"], "api_error")
        self.assertEqual(payload["error"]["status_code"], 503)

    def test_main_json_missing_dependency_is_classified_as_dependency_error(self):
        dependency_error = guardrail_safety.requests.RequestException(
            "requests package is required for backend-backed safety checks."
        )

        with patch.object(
            guardrail_safety, "_is_requests_dependency_error", return_value=True
        ):
            with patch.object(
                guardrail_safety, "detect_safety", side_effect=dependency_error
            ):
                code, stdout, _ = self._run_main(
                    ["--input", "DROP TABLE users", "--json"]
                )

        self.assertEqual(code, 1)
        payload = json.loads(stdout)
        self.assertEqual(payload["error"]["type"], "dependency_error")
        self.assertIn("requests package is required", payload["error"]["message"])

    def test_main_json_invalid_payload_type_is_api_error(self):
        with patch.object(guardrail_safety, "detect_safety", return_value=["bad"]):
            code, stdout, _ = self._run_main(["--input", "DROP TABLE users", "--json"])

        self.assertEqual(code, 1)
        payload = json.loads(stdout)
        self.assertEqual(payload["error"]["type"], "api_error")
        self.assertEqual(payload["error"]["details"]["receivedType"], "list")

    def test_main_json_invalid_json_error_is_api_error(self):
        with patch.object(
            guardrail_safety, "detect_safety", side_effect=ValueError("bad json")
        ):
            code, stdout, _ = self._run_main(["--input", "DROP TABLE users", "--json"])

        self.assertEqual(code, 1)
        payload = json.loads(stdout)
        self.assertEqual(payload["error"]["type"], "api_error")

    def test_main_json_normalizes_null_approved_to_false(self):
        with patch(
            "modeio_guardrail.cli.safety.detect_safety",
            return_value={
                "approved": None,
                "risk_level": "medium",
                "recommendation": "review",
            },
        ):
            code, stdout, _ = self._run_main(["--input", "rm -rf /tmp/cache", "--json"])

        self.assertEqual(code, 0)
        payload = json.loads(stdout)
        self.assertTrue(payload["success"])
        self.assertEqual(payload["data"]["approved"], False)
        self.assertEqual(payload["data"]["risk_level"], "medium")

    def test_main_json_backend_error_field_is_api_error(self):
        with patch(
            "modeio_guardrail.cli.safety.detect_safety",
            return_value={
                "error": "blocked by policy",
                "approved": False,
                "risk_level": "high",
            },
        ):
            code, stdout, _ = self._run_main(["--input", "rm -rf /", "--json"])

        self.assertEqual(code, 1)
        payload = json.loads(stdout)
        self.assertEqual(payload["error"]["type"], "api_error")
        self.assertEqual(payload["error"]["details"]["risk_level"], "high")

    def test_main_non_json_success_prints_status_and_payload(self):
        with patch(
            "modeio_guardrail.cli.safety.detect_safety",
            return_value={
                "approved": True,
                "risk_level": "low",
                "recommendation": "ok",
            },
        ):
            code, stdout, stderr = self._run_main(["--input", "ls"])

        self.assertEqual(code, 0)
        self.assertIn("Status: success", stderr)
        self.assertIn('"approved": true', stdout)

    def test_main_non_json_api_error_prints_error_and_details(self):
        with patch(
            "modeio_guardrail.cli.safety.detect_safety",
            return_value={
                "error": "blocked",
                "approved": False,
                "risk_level": "critical",
            },
        ):
            code, stdout, stderr = self._run_main(["--input", "DROP TABLE users"])

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("Error: blocked", stderr)
        self.assertIn('"risk_level": "critical"', stderr)


if __name__ == "__main__":
    unittest.main()
