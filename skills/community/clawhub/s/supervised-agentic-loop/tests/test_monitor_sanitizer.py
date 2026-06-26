"""Tests for sal.monitor.sanitizer — credential redaction."""

import pytest

from sal.monitor.sanitizer import contains_secret, sanitize_args, sanitize_value


class TestSanitizeArgs:
    def test_redacts_openai_key(self):
        """should redact sk- prefixed API keys."""
        args = {"header": "Authorization: Bearer sk-abc123def456ghi789jkl012mno"}
        result = sanitize_args(args)
        assert "sk-abc123" not in result["header"]
        assert "REDACTED" in result["header"]

    def test_redacts_github_pat(self):
        """should redact ghp_ prefixed GitHub tokens."""
        args = {"token": "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk"}
        result = sanitize_args(args)
        assert "ghp_ABCDEF" not in result["token"]

    def test_redacts_aws_key(self):
        """should redact AKIA prefixed AWS keys."""
        args = {"env": "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE"}
        result = sanitize_args(args)
        assert "AKIAIOSFODNN7EXAMPLE" not in result["env"]

    def test_redacts_bearer_token(self):
        """should redact Bearer tokens."""
        args = {"auth": "Bearer eyJhbGciOiJIUzI1NiIsInR5c.abc.xyz"}
        result = sanitize_args(args)
        assert "eyJhbG" not in result["auth"]

    def test_redacts_password(self):
        """should redact password= values."""
        args = {"cmd": "mysql -p password=MyS3cretP@ss"}
        result = sanitize_args(args)
        assert "MyS3cret" not in result["cmd"]

    def test_preserves_safe_args(self):
        """should NOT redact normal values."""
        args = {"command": "echo hello", "path": "/usr/bin/python3"}
        result = sanitize_args(args)
        assert result["command"] == "echo hello"
        assert result["path"] == "/usr/bin/python3"

    def test_deep_redacts_nested(self):
        """should redact in nested dicts and lists."""
        args = {
            "nested": {
                "deep": "token=sk-abc123def456ghi789jkl012mno345"
            },
            "list": ["safe", "ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijk"],
        }
        result = sanitize_args(args)
        assert "sk-abc123" not in str(result)
        assert "ghp_ABCDEF" not in str(result)

    def test_truncates_long_values(self):
        """should truncate values longer than 10KB."""
        args = {"big": "x" * 20_000}
        result = sanitize_args(args)
        assert len(result["big"]) < 15_000
        assert "TRUNCATED" in result["big"]

    def test_handles_non_dict(self):
        """should return empty dict for non-dict input."""
        assert sanitize_args("not a dict") == {}  # type: ignore
        assert sanitize_args(None) == {}  # type: ignore


class TestContainsSecret:
    def test_detects_openai_key(self):
        assert contains_secret("key is sk-abc123def456ghi789jkl012mno") is True

    def test_no_secret_in_normal_text(self):
        assert contains_secret("echo hello world") is False
