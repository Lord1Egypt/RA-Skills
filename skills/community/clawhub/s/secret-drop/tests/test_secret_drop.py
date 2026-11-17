"""Automated test suite for openclaw-secret-drop."""

from __future__ import annotations

import base64
import contextlib
import io
import json
import os
import socket
import stat
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from secret_drop.dotenv_file import format_assignment, upsert_env_file, write_secret_file
from secret_drop.errors import SecretDropError
from secret_drop.net import _is_private_ip, assert_public_https, resolve_public_https
from secret_drop.cli import main as cli_main
from secret_drop.providers.pwpush import retrieve as pwpush_retrieve
from secret_drop.providers.registry import detect_provider
from secret_drop.providers.share import create_push
from secret_drop.providers.snappwd import retrieve as snappwd_retrieve
from secret_drop.redact import host_of, redact_text, sanitize_url
from secret_drop.sources import read_dotenv_value, read_secret_source

_BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def _b58encode(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(_BASE58[r])
    res = "".join(reversed(res))
    pad = 0
    for byte in b:
        if byte == 0:
            pad += 1
        else:
            break
    return "1" * pad + res


class RedactTests(unittest.TestCase):
    def test_sanitize_url_strips_fragment_and_query_secrets(self) -> None:
        url = "https://example.com/p/token?passphrase=supersecret#fragmentkey123"
        clean = sanitize_url(url)
        self.assertNotIn("supersecret", clean)
        self.assertNotIn("fragmentkey123", clean)
        self.assertEqual(clean, "https://example.com/p/[redacted-token]")

    def test_redact_text_replaces_secret_and_fragment(self) -> None:
        raw = "error fetching https://snappwd.io/g/sp-123#mykey: sk-proj-12345 failed"
        safe = redact_text(raw, secret="sk-proj-12345", url="https://snappwd.io/g/sp-123#mykey")
        self.assertNotIn("sk-proj-12345", safe)
        self.assertNotIn("mykey", safe)
        self.assertIn("[redacted-secret]", safe)

    def test_host_of_normalizes(self) -> None:
        self.assertEqual(host_of("https://PWPUSH.com/p/abc"), "pwpush.com")

    def test_redacts_provider_path_token_from_url_and_error_text(self) -> None:
        token = "kngc42l6azicpqj5hbu"
        url = f"https://pwpush.com/p/{token}"
        raw = f"Invalid token prefix {token}; request failed for {url}"
        safe = redact_text(raw, url=url)
        self.assertNotIn(token, safe)
        self.assertIn("/p/[redacted-token]", safe)


class NetSecurityTests(unittest.TestCase):
    def test_rejects_non_https(self) -> None:
        with self.assertRaises(SecretDropError):
            assert_public_https("http://pwpush.com/p/test")

    def test_rejects_localhost_by_default(self) -> None:
        with self.assertRaises(SecretDropError):
            assert_public_https("https://localhost/p/test")

    def test_allows_private_host_when_explicitly_authorized(self) -> None:
        assert_public_https("https://localhost/p/test", allow_private=True)

    def test_rejects_ipv4_mapped_private_ipv6(self) -> None:
        self.assertTrue(_is_private_ip("::ffff:127.0.0.1"))
        self.assertFalse(_is_private_ip("::ffff:8.8.8.8"))

    @patch("secret_drop.net.socket.getaddrinfo")
    def test_rejects_mixed_public_and_private_dns_records(self, getaddrinfo) -> None:
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443)),
            (socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("fd00::1", 443, 0, 0)),
        ]
        with self.assertRaises(SecretDropError):
            resolve_public_https("https://example.com/p/test")

    @patch("secret_drop.net.socket.getaddrinfo")
    def test_pins_first_address_only_after_all_records_pass(self, getaddrinfo) -> None:
        getaddrinfo.return_value = [
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443)),
            (socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("2606:2800:220:1:248:1893:25c8:1946", 443, 0, 0)),
        ]
        _host, _port, _path, connect_ip = resolve_public_https(
            "https://example.com/p/test"
        )
        self.assertEqual(connect_ip, "93.184.216.34")


class DotenvWriterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.env_file = Path(self.temp_dir.name) / ".env"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_atomic_append_and_replace_maintains_mode_0600(self) -> None:
        upsert_env_file(self.env_file, "KEY_ONE", "value_1")
        self.assertEqual(stat.S_IMODE(self.env_file.stat().st_mode), 0o600)
        self.assertIn("KEY_ONE=value_1", self.env_file.read_text())

        upsert_env_file(self.env_file, "KEY_ONE", "value_2_updated")
        self.assertEqual(stat.S_IMODE(self.env_file.stat().st_mode), 0o600)
        content = self.env_file.read_text()
        self.assertIn("KEY_ONE=value_2_updated", content)
        self.assertNotIn("value_1", content)

    def test_refuses_symlink_target_or_directory(self) -> None:
        symlink = Path(self.temp_dir.name) / "symlink.env"
        real = Path(self.temp_dir.name) / "real.env"
        real.write_text("FOO=bar\n")
        symlink.symlink_to(real)
        with self.assertRaises(SecretDropError):
            upsert_env_file(symlink, "KEY", "val")
        with self.assertRaises(SecretDropError):
            write_secret_file(symlink, "val")

    def test_rechecks_for_symlink_immediately_before_replace(self) -> None:
        victim = Path(self.temp_dir.name) / "victim.env"
        victim.write_text("SAFE=unchanged\n")
        self.env_file.write_text("KEY=old\n")

        from secret_drop import dotenv_file

        real_check = dotenv_file._assert_safe_replace_target

        def inject_symlink(path: Path, *, destination: str) -> None:
            path.unlink()
            path.symlink_to(victim)
            real_check(path, destination=destination)

        with patch(
            "secret_drop.dotenv_file._assert_safe_replace_target",
            side_effect=inject_symlink,
        ):
            with self.assertRaises(SecretDropError):
                upsert_env_file(self.env_file, "KEY", "new")

        self.assertEqual(victim.read_text(), "SAFE=unchanged\n")
        self.assertTrue(self.env_file.is_symlink())
        self.assertEqual(list(Path(self.temp_dir.name).glob(".secret-drop-*.tmp")), [])

    def test_quotes_special_characters(self) -> None:
        line = format_assignment("COMPLEX", 'secret "quoted" with spaces')
        self.assertEqual(line, 'COMPLEX="secret \\"quoted\\" with spaces"\n')

    def test_write_file_creates_mode_0600(self) -> None:
        target = Path(self.temp_dir.name) / "secret.key"
        write_secret_file(target, "raw_secret_data")
        self.assertEqual(stat.S_IMODE(target.stat().st_mode), 0o600)
        self.assertEqual(target.read_text(), "raw_secret_data")

    def test_write_file_refuses_overwrite_without_replace_flag(self) -> None:
        target = Path(self.temp_dir.name) / "existing.key"
        target.write_text("initial")
        with self.assertRaises(SecretDropError):
            write_secret_file(target, "new")
        write_secret_file(target, "new", replace=True)
        self.assertEqual(target.read_text(), "new")


class SecretSourceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_reads_named_dotenv_value_without_printing_it(self) -> None:
        path = self.root / ".env"
        path.write_text(
            "PLAIN=value-one\n"
            "export QUOTED=\"secret with spaces\\nsecond line\"\n",
            encoding="utf-8",
        )
        self.assertEqual(read_dotenv_value(path, "PLAIN"), "value-one")
        self.assertEqual(
            read_dotenv_value(path, "QUOTED"),
            "secret with spaces\nsecond line",
        )

    def test_rejects_symlink_secret_source(self) -> None:
        target = self.root / "secret.txt"
        target.write_text("hidden-secret", encoding="utf-8")
        link = self.root / "secret-link.txt"
        link.symlink_to(target)
        with self.assertRaises(SecretDropError):
            read_secret_source(source="file", path=str(link), name=None)

    def test_reads_raw_file_exactly(self) -> None:
        target = self.root / "secret.txt"
        target.write_text("raw-secret-value", encoding="utf-8")
        self.assertEqual(
            read_secret_source(source="file", path=str(target), name=None),
            "raw-secret-value",
        )


class ProviderAdapterTests(unittest.TestCase):
    def test_detect_provider(self) -> None:
        self.assertEqual(detect_provider("https://pwpush.com/p/abcd1234"), "pwpush")
        self.assertEqual(detect_provider("https://snappwd.io/g/sp-1234#key5678"), "snappwd")

    def test_unknown_self_host_requires_explicit_provider(self) -> None:
        with self.assertRaises(SecretDropError):
            detect_provider("https://secrets.example.com/p/abcd1234")

    @patch("secret_drop.providers.pwpush.request_json")
    def test_pwpush_retrieves_payload(self, mock_json) -> None:
        mock_json.return_value = (200, {"payload": "secret-value-from-pwpush"}, b"")
        val = pwpush_retrieve("https://pwpush.com/p/testtoken123", allow_private=True)
        self.assertEqual(val, "secret-value-from-pwpush")
        mock_json.assert_called_once()
        self.assertEqual(mock_json.call_args[0][0], "https://pwpush.com/p/testtoken123.json")

    @patch("secret_drop.providers.pwpush.request_json")
    def test_pwpush_accepts_retrieval_step_url(self, mock_json) -> None:
        mock_json.return_value = (200, {"payload": "secret-value-from-pwpush"}, b"")
        value = pwpush_retrieve(
            "https://eu.pwpush.com/p/testtoken123/r", allow_private=True
        )
        self.assertEqual(value, "secret-value-from-pwpush")
        self.assertEqual(
            mock_json.call_args[0][0],
            "https://eu.pwpush.com/p/testtoken123.json",
        )

    @patch("secret_drop.providers.pwpush.request_json")
    def test_pwpush_completes_retrieval_step(self, mock_json) -> None:
        mock_json.side_effect = [
            (200, {"retrieval_step": True, "payload": None}, b""),
            (200, {"status": "previewed"}, b""),
            (200, {"retrieval_step": True, "payload": "final-secret"}, b""),
        ]
        value = pwpush_retrieve("https://pwpush.com/p/testtoken123", allow_private=True)
        self.assertEqual(value, "final-secret")
        self.assertEqual(mock_json.call_count, 3)
        self.assertEqual(
            mock_json.call_args_list[1][0][0],
            "https://pwpush.com/p/testtoken123/preview.json",
        )

    @patch("secret_drop.providers.snappwd.request_json")
    def test_snappwd_decrypts_v2_payload(self, mock_json) -> None:
        raw_key = os.urandom(32)
        b58_key = _b58encode(raw_key)
        iv = os.urandom(12)
        aesgcm = AESGCM(raw_key)
        ciphertext = aesgcm.encrypt(iv, b"snappwd-plain-text", None)
        versioned = bytes([2]) + iv + ciphertext
        b64_payload = base64.b64encode(versioned).decode("ascii")

        mock_json.return_value = (200, {"encryptedSecret": b64_payload}, b"")
        url = f"https://snappwd.io/g/sp-uuid123#{b58_key}"
        val = snappwd_retrieve(url, allow_private=True)
        self.assertEqual(val, "snappwd-plain-text")

    @patch("secret_drop.providers.share.request_json")
    def test_pwpush_creates_one_view_link(self, mock_json) -> None:
        secret = "outbound-secret-value"
        mock_json.return_value = (
            201,
            {
                "url_token": "synthetic-token-123",
                "html_url": "https://eu.pwpush.com/p/synthetic-token-123/r",
                "expire_after_views": 1,
                "expire_after_days": 1,
                "retrieval_step": True,
            },
            b"",
        )
        result = create_push(secret)
        self.assertEqual(result["url"], "https://eu.pwpush.com/p/synthetic-token-123/r")
        self.assertEqual(result["expire_views"], 1)
        self.assertEqual(result["expire_days"], 1)
        self.assertTrue(result["retrieval_step"])
        request_kwargs = mock_json.call_args.kwargs
        self.assertFalse(request_kwargs["allow_redirects"])
        request_payload = json.loads(request_kwargs["data"].decode("utf-8"))
        self.assertEqual(request_payload["password"]["payload"], secret)
        self.assertEqual(request_payload["password"]["expire_after_views"], 1)
        self.assertEqual(request_payload["password"]["expire_after_days"], 1)
        self.assertTrue(request_payload["password"]["retrieval_step"])
        self.assertNotIn(secret, json.dumps(result))

    @patch("secret_drop.providers.share.request_json")
    def test_pwpush_rejects_invalid_response_token(self, mock_json) -> None:
        mock_json.return_value = (
            201,
            {
                "url_token": "../../bad",
                "html_url": "https://pwpush.com/p/bad/r",
                "expire_after_views": 1,
                "expire_after_days": 1,
                "retrieval_step": True,
            },
            b"",
        )
        with self.assertRaises(SecretDropError):
            create_push("outbound-secret-value")

    @patch("secret_drop.providers.share.request_json")
    def test_pwpush_rejects_missing_retrieval_step_url(self, mock_json) -> None:
        mock_json.return_value = (
            201,
            {
                "url_token": "synthetic-token-123",
                "expire_after_views": 1,
                "expire_after_days": 1,
                "retrieval_step": True,
            },
            b"",
        )
        with self.assertRaises(SecretDropError):
            create_push("outbound-secret-value")

    @patch("secret_drop.providers.share.request_json")
    def test_pwpush_rejects_non_one_view_response(self, mock_json) -> None:
        mock_json.return_value = (
            201,
            {
                "url_token": "synthetic-token-123",
                "html_url": "https://pwpush.com/p/synthetic-token-123/r",
                "expire_after_views": 2,
                "expire_after_days": 1,
                "retrieval_step": True,
            },
            b"",
        )
        with self.assertRaises(SecretDropError):
            create_push("outbound-secret-value")

    @patch("secret_drop.providers.share.request_json")
    def test_pwpush_rejects_foreign_share_host(self, mock_json) -> None:
        mock_json.return_value = (
            201,
            {
                "url_token": "synthetic-token-123",
                "html_url": "https://attacker.example/p/synthetic-token-123/r",
                "expire_after_views": 1,
                "expire_after_days": 1,
                "retrieval_step": True,
            },
            b"",
        )
        with self.assertRaises(SecretDropError):
            create_push("outbound-secret-value")


class CliLeakTests(unittest.TestCase):
    @patch("secret_drop.cli.create_push")
    @patch("secret_drop.cli.read_secret_source")
    def test_share_outputs_only_one_time_link(self, read_source, create) -> None:
        secret = "outbound-secret-value"
        read_source.return_value = secret
        create.return_value = {
            "ok": True,
            "url": "https://pwpush.com/p/synthetic-token-123/r",
            "provider": "pwpush",
            "expire_views": 1,
            "expire_days": 1,
            "retrieval_step": True,
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli_main(
                [
                    "share",
                    "--from",
                    "dotenv",
                    "--path",
                    "/tmp/project.env",
                    "--name",
                    "DB_PASSWORD",
                    "--json",
                ]
            )
        result = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        self.assertEqual(result["url"], "https://pwpush.com/p/synthetic-token-123/r")
        self.assertNotIn(secret, stdout.getvalue() + stderr.getvalue())
        read_source.assert_called_once_with(
            source="dotenv", path="/tmp/project.env", name="DB_PASSWORD"
        )
        create.assert_called_once_with(
            secret,
            api_base="https://eu.pwpush.com",
            allow_private=False,
        )

    @patch("secret_drop.cli.create_push")
    @patch("secret_drop.cli.read_secret_source")
    def test_share_failure_never_outputs_secret(self, read_source, create) -> None:
        secret = "outbound-secret-value"
        read_source.return_value = secret
        create.side_effect = SecretDropError(f"provider rejected {secret}")
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli_main(
                [
                    "share",
                    "--from",
                    "file",
                    "--path",
                    "/tmp/secret.txt",
                    "--json",
                ]
            )
        self.assertEqual(code, 2)
        self.assertNotIn(secret, stdout.getvalue() + stderr.getvalue())

    @patch("secret_drop.cli.restart_openclaw_gateway")
    @patch("secret_drop.cli.write_secret")
    @patch("secret_drop.cli.retrieve_secret")
    def test_restart_gateway_flag_requests_safe_restart(self, retrieve, write, restart) -> None:
        secret = "REDACTED-SECRET"
        retrieve.return_value = ("pwpush", secret)
        write.return_value = {
            "destination": "openclaw-env",
            "name": "OPENROUTER_API_KEY",
            "restart_required": True,
            "created": False,
            "replaced": True,
            "path": "/tmp/.env",
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli_main(
                [
                    "ingest",
                    "https://pwpush.com/p/testtoken123",
                    "--to",
                    "openclaw-env",
                    "--name",
                    "OPENROUTER_API_KEY",
                    "--restart-gateway",
                    "--json",
                ]
            )
        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 0)
        restart.assert_called_once_with()
        self.assertTrue(payload["gateway_restarted"])
        self.assertFalse(payload["restart_required"])
        self.assertNotIn(secret, stdout.getvalue() + stderr.getvalue())

    @patch("secret_drop.cli.write_secret")
    @patch("secret_drop.cli.retrieve_secret")
    def test_success_output_never_contains_secret(self, retrieve, write) -> None:
        secret = "REDACTED-SECRET"
        retrieve.return_value = ("pwpush", secret)
        write.return_value = {
            "destination": "openclaw-env",
            "name": "OPENROUTER_API_KEY",
            "restart_required": True,
            "created": False,
            "replaced": True,
            "path": "/tmp/.env",
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli_main(
                [
                    "ingest",
                    "https://pwpush.com/p/testtoken123",
                    "--to",
                    "openclaw-env",
                    "--name",
                    "OPENROUTER_API_KEY",
                    "--json",
                ]
            )
        self.assertEqual(code, 0)
        self.assertNotIn(secret, stdout.getvalue())
        self.assertNotIn(secret, stderr.getvalue())

    @patch("secret_drop.cli.write_secret")
    @patch("secret_drop.cli.retrieve_secret")
    def test_failure_output_never_contains_secret_or_fragment(self, retrieve, write) -> None:
        secret = "REDACTED-SECRET"
        retrieve.return_value = ("snappwd", secret)
        write.side_effect = SecretDropError(f"failed with {secret}")
        url = "https://snappwd.io/g/sp-example#fragment-decryption-key"
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = cli_main(
                [
                    "ingest",
                    url,
                    "--to",
                    "openclaw-env",
                    "--name",
                    "OPENROUTER_API_KEY",
                    "--json",
                ]
            )
        combined = stdout.getvalue() + stderr.getvalue()
        self.assertEqual(code, 2)
        self.assertNotIn(secret, combined)
        self.assertNotIn("fragment-decryption-key", combined)


if __name__ == "__main__":
    unittest.main()
