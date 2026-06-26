"""Tests for sal.verification — 4 deterministic gates."""

import os
import tempfile

import pytest

from sal.verification import (
    VerificationResult,
    run_full_verification,
    verify_files_exist,
    verify_python_syntax,
    verify_tests,
)


@pytest.fixture
def tmp_dir():
    """Create a temp dir with test files."""
    d = tempfile.mkdtemp()
    # Valid Python file
    with open(os.path.join(d, "good.py"), "w") as f:
        f.write("x = 1\nprint(x)\n")
    # Invalid Python file
    with open(os.path.join(d, "bad.py"), "w") as f:
        f.write("def broken(\n")
    # Empty file
    with open(os.path.join(d, "empty.py"), "w") as f:
        pass
    yield d


class TestGate1FilesExist:
    def test_existing_files(self, tmp_dir):
        """should pass for existing non-empty files."""
        result = verify_files_exist(["good.py"], tmp_dir)
        assert result.passed is True

    def test_missing_file(self, tmp_dir):
        """should fail for missing files."""
        result = verify_files_exist(["missing.py"], tmp_dir)
        assert result.passed is False
        assert "NOT FOUND" in result.summary

    def test_empty_file(self, tmp_dir):
        """should fail for empty files."""
        result = verify_files_exist(["empty.py"], tmp_dir)
        assert result.passed is False


class TestGate2PythonSyntax:
    def test_valid_syntax(self, tmp_dir):
        """should pass for valid Python."""
        result = verify_python_syntax(["good.py"], tmp_dir)
        assert result.passed is True

    def test_invalid_syntax(self, tmp_dir):
        """should fail for syntax errors."""
        result = verify_python_syntax(["bad.py"], tmp_dir)
        assert result.passed is False
        assert "SyntaxError" in result.summary

    def test_skips_non_python(self, tmp_dir):
        """should skip non-.py files."""
        result = verify_python_syntax(["readme.md"], tmp_dir)
        # No checks added for non-py file → evaluates to False
        assert len(result.checks) == 0


class TestGate3Tests:
    def test_passing_command(self):
        """should pass for exit code 0."""
        result = verify_tests("echo 'all good'")
        assert result.passed is True

    def test_failing_command(self):
        """should fail for non-zero exit code."""
        result = verify_tests("false")
        assert result.passed is False

    def test_timeout(self):
        """should fail on timeout."""
        result = verify_tests("sleep 10", timeout=1)
        assert result.passed is False
        assert "TIMEOUT" in result.summary


class TestFullVerification:
    def test_all_gates_pass(self, tmp_dir):
        """should pass when all gates succeed."""
        result = run_full_verification(
            required_files=["good.py"],
            test_command="echo 'pass'",
            base_dir=tmp_dir,
        )
        assert result.passed is True
        assert "CHECKS PASSED" in result.summary

    def test_syntax_gate_fails(self, tmp_dir):
        """should fail when syntax gate fails."""
        result = run_full_verification(
            required_files=["bad.py"],
            base_dir=tmp_dir,
        )
        assert result.passed is False
        assert "SyntaxError" in result.summary
