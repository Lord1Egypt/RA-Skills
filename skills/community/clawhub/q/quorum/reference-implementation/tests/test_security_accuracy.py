"""Layer 5: Security tests — credential and PII detection accuracy."""

from __future__ import annotations

from pathlib import Path

import pytest

from quorum.models import Severity
from quorum.prescreen import PreScreen


@pytest.fixture
def ps() -> PreScreen:
    return PreScreen()


def _run_check(ps, tmp_path, content: str, ext: str = ".txt") -> dict:
    """Run prescreen and return checks keyed by ID."""
    f = tmp_path / f"test{ext}"
    f.write_text(content)
    result = ps.run(f, f.read_text())
    return {c.id: c for c in result.checks}


# ── Credential detection true positives ──────────────────────────────────────


class TestCredentialDetectionTruePositives:
    def test_anthropic_api_key(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, 'api_key = "sk-ant-api03-realkey1234567890abcdef"\n')
        assert checks["PS-002"].result == "FAIL"

    def test_password_assignment(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, 'password = "hunter2"\n')
        assert checks["PS-002"].result == "FAIL"

    def test_password_colon(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "password: supersecret\n")
        assert checks["PS-002"].result == "FAIL"

    def test_client_secret(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, 'client_secret = "abcdef1234567890"\n')
        assert checks["PS-002"].result == "FAIL"

    def test_auth_token(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, 'auth_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9"\n')
        assert checks["PS-002"].result == "FAIL"

    def test_access_token(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, 'access_token: "gho_16C7e42F292c6912E7710c838347Ae178B4a"\n')
        assert checks["PS-002"].result == "FAIL"

    def test_pem_private_key(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "BEGIN RSA PRIVATE KEY\nMIIEpQIBAAKCAQEA\n")
        assert checks["PS-002"].result == "FAIL"

    def test_ec_private_key(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "BEGIN EC PRIVATE KEY\nMHQCAQEEI\n")
        assert checks["PS-002"].result == "FAIL"

    def test_long_base64_blob(self, ps, tmp_path):
        blob = "A" * 50
        checks = _run_check(ps, tmp_path, f"secret = {blob}\n")
        assert checks["PS-002"].result == "FAIL"


# ── Credential detection true negatives ──────────────────────────────────────


class TestCredentialDetectionTrueNegatives:
    def test_normal_code(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "x = 42\nname = 'hello'\n")
        assert checks["PS-002"].result == "PASS"

    def test_short_values(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "key = 'abc'\nval = '123'\n")
        assert checks["PS-002"].result == "PASS"

    def test_empty_file(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "Clean file with no secrets.\n")
        assert checks["PS-002"].result == "PASS"


# ── PII detection true positives ─────────────────────────────────────────────


class TestPIIDetectionTruePositives:
    def test_email_address(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "john.doe@company.com\n")
        assert checks["PS-003"].result == "FAIL"

    def test_us_phone(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "(555) 234-5678\n")
        assert checks["PS-003"].result == "FAIL"

    def test_ssn(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "SSN: 123-45-6789\n")
        assert checks["PS-003"].result == "FAIL"

    def test_phone_with_country_code(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "+1 555-987-6543\n")
        assert checks["PS-003"].result == "FAIL"

    def test_multiple_pii_types(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "john@x.com\n123-45-6789\n(555) 234-5678\n")
        assert checks["PS-003"].result == "FAIL"
        desc = checks["PS-003"].description
        assert "email" in desc
        assert "SSN" in desc or "phone" in desc


# ── PII detection true negatives ─────────────────────────────────────────────


class TestPIIDetectionTrueNegatives:
    def test_version_number_not_ssn(self, ps, tmp_path):
        # Version numbers should ideally not trigger SSN
        checks = _run_check(ps, tmp_path, "version: 1.2.3\nsemver: v2.0.0-rc1\n")
        # SSN pattern is very specific, version numbers shouldn't match
        assert checks["PS-003"].result == "PASS"

    def test_no_pii_in_code(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "def foo():\n    return 42\n")
        assert checks["PS-003"].result == "PASS"


# ── Severity levels ──────────────────────────────────────────────────────────


class TestSecuritySeverityLevels:
    def test_credentials_are_critical(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, 'password = "secret"\n')
        assert checks["PS-002"].severity == Severity.CRITICAL

    def test_pii_is_high(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "user@company.com\n")
        assert checks["PS-003"].severity == Severity.HIGH

    def test_hardcoded_paths_are_high(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, '/Users/john/data\n')
        assert checks["PS-001"].severity == Severity.HIGH


# ── Evidence quality ─────────────────────────────────────────────────────────


class TestSecurityEvidenceQuality:
    def test_credential_evidence_redacted(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, 'password = "my_super_secret_password_123"\n')
        evidence = checks["PS-002"].evidence
        assert "***" in evidence

    def test_credential_evidence_has_line_numbers(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, 'x = 1\npassword = "secret"\ny = 2\n')
        assert "L2" in checks["PS-002"].evidence

    def test_pii_evidence_has_breakdown(self, ps, tmp_path):
        checks = _run_check(ps, tmp_path, "john@x.com\n123-45-6789\n")
        desc = checks["PS-003"].description
        # Should mention what types of PII were found
        assert "email" in desc or "SSN" in desc
