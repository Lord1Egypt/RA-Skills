#!/usr/bin/env python3
"""Smoke tests for the safe-share sanitizer."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sanitize_text import sanitize  # noqa: E402


def assert_contains(text: str, needle: str) -> None:
    if needle not in text:
        raise AssertionError(f"Expected to find {needle!r} in output: {text!r}")


def assert_not_contains(text: str, needle: str) -> None:
    if needle in text:
        raise AssertionError(f"Did not expect to find {needle!r} in output: {text!r}")


def main() -> int:
    sample = "\n".join(
        [
            "Authorization: Bearer super-secret-token",
            "OPENAI_API_KEY=sk-examplesecret123456789",
            "Contact: dev@example.com",
            'url=https://api.example.com/build?token=raw-demo-token&id=42',
            "Cookie: sessionid=abc123def456",
            "server ip: 10.1.2.3",
            "call me at +1 (415) 555-0199",
        ]
    )

    result = sanitize(sample, "placeholder")
    text = result["sanitized_text"]
    summary = {item["type"]: item["count"] for item in result["findings_summary"]}

    assert_contains(text, "Authorization: Bearer <BEARER_TOKEN>")
    assert_contains(text, "OPENAI_API_KEY=<OPENAI_API_KEY>")
    assert_contains(text, "Contact: <EMAIL>")
    assert_contains(text, "token=<QUERY_TOKEN>&id=42")
    assert_contains(text, "Cookie: <COOKIE>")
    assert_contains(text, "server ip: <IPV4>")
    assert_contains(text, "call me at <PHONE_NUMBER>")

    expected_counts = {
        "bearer_token": 1,
        "cookie_header": 1,
        "email": 1,
        "env_assignment": 1,
        "ipv4": 1,
        "phone_number": 1,
        "quoted_assignment": 1,
        "sensitive_query_param": 1,
    }
    if summary != expected_counts:
        raise AssertionError(f"Unexpected findings summary: {json.dumps(summary, sort_keys=True)}")

    false_positive_sample = "\n".join(
        [
            "Build id: 8f4a8f4a",
            "SHA256: 9f86d081884c7d659a2feaa0c55ad015",
            r"Path: C:\temp\tokenizer\notes.txt",
        ]
    )

    false_positive_result = sanitize(false_positive_sample, "placeholder")
    false_positive_text = false_positive_result["sanitized_text"]
    assert_contains(false_positive_text, "Build id: 8f4a8f4a")
    assert_contains(false_positive_text, r"Path: C:\temp\tokenizer\notes.txt")
    assert_not_contains(false_positive_text, "<")

    print("safe-share smoke tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
