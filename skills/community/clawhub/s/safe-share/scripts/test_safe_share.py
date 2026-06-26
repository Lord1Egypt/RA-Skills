#!/usr/bin/env python3
"""Tests for the safe-share sanitizer."""

from __future__ import annotations

from unittest import TestCase, main

from sanitize_text import sanitize


class TestSafeShare(TestCase):
    def test_placeholder_mode_sanitizes_high_risk_values(self):
        sample = "\n".join(
            [
                "Authorization: Bearer super-secret-token",
                "OPENAI_API_KEY=sk-examplesecret123456789",
                "Contact: dev@example.com",
                "url=https://api.example.com/build?token=raw-demo-token&id=42",
                "Cookie: sessionid=abc123def456",
                "server ip: 10.1.2.3",
                "call me at +1 (415) 555-0199",
            ]
        )

        result = sanitize(sample, "placeholder")
        text = result["sanitized_text"]
        summary = {item["type"]: item["count"] for item in result["findings_summary"]}

        self.assertIn("Authorization: Bearer <BEARER_TOKEN>", text)
        self.assertIn("OPENAI_API_KEY=<OPENAI_API_KEY>", text)
        self.assertIn("Contact: <EMAIL>", text)
        self.assertIn("token=<QUERY_TOKEN>&id=42", text)
        self.assertIn("Cookie: <COOKIE>", text)
        self.assertIn("server ip: <IPV4>", text)
        self.assertIn("call me at <PHONE_NUMBER>", text)

        self.assertEqual(
            summary,
            {
                "bearer_token": 1,
                "cookie_header": 1,
                "email": 1,
                "env_assignment": 1,
                "ipv4": 1,
                "phone_number": 1,
                "quoted_assignment": 1,
                "sensitive_query_param": 1,
            },
        )

    def test_false_positive_guardrails_leave_plain_values_alone(self):
        sample = "\n".join(
            [
                "Build id: 8f4a8f4a",
                "SHA256: 9f86d081884c7d659a2feaa0c55ad015",
                r"Path: C:\temp\tokenizer\notes.txt",
            ]
        )

        result = sanitize(sample, "placeholder")
        text = result["sanitized_text"]

        self.assertIn("Build id: 8f4a8f4a", text)
        self.assertIn(r"Path: C:\temp\tokenizer\notes.txt", text)
        self.assertEqual(result["findings_summary"], [])


if __name__ == "__main__":
    main()
