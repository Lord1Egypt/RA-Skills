"""Tests for PII detector (audit mode)."""

from repro_pack.redactor.detector import detect_pii


class TestDetector:
    def test_detect_returns_matches(self):
        matches = detect_pii("email: user@example.com, ip: 10.0.0.1")
        types = {m.pii_type.value for m in matches}
        assert "email" in types
        assert "ip_address" in types

    def test_detect_does_not_modify_text(self):
        text = "user@example.com"
        detect_pii(text)
        assert text == "user@example.com"

    def test_detect_empty_text(self):
        matches = detect_pii("")
        assert matches == []

    def test_detect_no_pii(self):
        matches = detect_pii("This is a normal message with no sensitive data")
        assert matches == []

    def test_detect_line_numbers(self):
        text = "line 1\nuser@test.com on line 2\nline 3\n10.0.0.1 on line 4"
        matches = detect_pii(text)
        lines = {m.line_number for m in matches}
        assert 2 in lines
        assert 4 in lines
