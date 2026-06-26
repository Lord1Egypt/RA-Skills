"""Tests for the redaction engine."""

from repro_pack.redactor import RedactionEngine


class TestRedactionEngine:
    def test_redacts_email(self):
        engine = RedactionEngine()
        result = engine.redact("contact user@example.com please")
        assert "user@example.com" not in result
        assert "[EMAIL_1]" in result

    def test_redacts_phone(self):
        engine = RedactionEngine()
        result = engine.redact("call 13812345678 now")
        assert "13812345678" not in result
        assert "PHONE" in result

    def test_redacts_ip(self):
        engine = RedactionEngine()
        result = engine.redact("from 192.168.1.100")
        assert "192.168.1.100" not in result
        assert "IP_ADDRESS" in result

    def test_redacts_multiple_types(self, dirty_log):
        engine = RedactionEngine()
        result = engine.redact(dirty_log)

        # Should not contain any raw PII
        assert "john@example.com" not in result
        assert "192.168.1.100" not in result
        assert "4111111111111111" not in result
        assert "AKIAFAKEKEY00EXAMPLE" not in result
        assert "110105199003071234" not in result
        assert "SuperSecret123!" not in result

        # Should contain placeholders
        assert "[EMAIL_" in result
        assert "[IP_ADDRESS_" in result
        assert "[CREDIT_CARD_" in result
        assert "[AWS_KEY_" in result

    def test_report_counts(self, dirty_log):
        engine = RedactionEngine()
        engine.redact(dirty_log)
        report = engine.get_report()

        assert report.total_found > 0
        assert report.lines_processed > 0
        assert len(report.replacements) == report.total_found

    def test_report_has_line_numbers(self):
        engine = RedactionEngine()
        engine.redact("line1\nuser@test.com on line2\nline3")
        report = engine.get_report()

        assert len(report.replacements) == 1
        assert report.replacements[0].line_number == 2

    def test_preserves_non_pii_text(self):
        engine = RedactionEngine()
        text = "This is a normal log message without any PII"
        result = engine.redact(text)
        assert result == text

    def test_reset(self):
        engine = RedactionEngine()
        engine.redact("user@test.com")
        engine.reset()
        report = engine.get_report()
        assert report.total_found == 0

    def test_multiple_same_type(self):
        engine = RedactionEngine()
        result = engine.redact("a@b.com and c@d.com")
        assert "[EMAIL_1]" in result
        assert "[EMAIL_2]" in result

    def test_redact_jwt(self):
        engine = RedactionEngine()
        jwt = "eyJhbGciOiAibm9uZSJ9.eyJzdWIiOiAiZmFrZSIsICJkZW1vIjogdHJ1ZX0.fakesignature00000"
        result = engine.redact(f"token: {jwt}")
        assert jwt not in result
