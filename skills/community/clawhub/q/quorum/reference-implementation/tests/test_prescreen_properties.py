"""Layer 4: Property-based tests for prescreen using Hypothesis."""

from __future__ import annotations

from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from quorum.prescreen import PreScreen


@pytest.fixture
def ps() -> PreScreen:
    return PreScreen()


class TestPrescreenProperties:
    @given(st.text(max_size=5000))
    @settings(max_examples=50, deadline=5000)
    def test_prescreen_handles_any_text(self, text):
        """PS checks must never crash on arbitrary text input."""
        ps = PreScreen()
        tmp = Path("/tmp/quorum_test_prop.md")
        tmp.write_text(text, encoding="utf-8")
        try:
            result = ps.run(tmp, text)
            # Should always return a valid PreScreenResult
            assert result.total_checks >= 0
            assert result.passed >= 0
            assert result.failed >= 0
            assert result.skipped >= 0
        finally:
            tmp.unlink(missing_ok=True)

    @given(st.text(max_size=5000))
    @settings(max_examples=50, deadline=5000)
    def test_prescreen_handles_any_python(self, text):
        """PS-006 must never crash on arbitrary text presented as .py."""
        ps = PreScreen()
        tmp = Path("/tmp/quorum_test_prop.py")
        tmp.write_text(text, encoding="utf-8")
        try:
            result = ps.run(tmp, text)
            check = next((c for c in result.checks if c.id == "PS-006"), None)
            if check:
                assert check.result in ("PASS", "FAIL", "SKIP")
        finally:
            tmp.unlink(missing_ok=True)

    @given(st.text(max_size=5000))
    @settings(max_examples=50, deadline=5000)
    def test_prescreen_handles_any_json(self, text):
        """PS-004 must never crash on arbitrary text presented as .json."""
        ps = PreScreen()
        tmp = Path("/tmp/quorum_test_prop.json")
        tmp.write_text(text, encoding="utf-8")
        try:
            result = ps.run(tmp, text)
            check = next((c for c in result.checks if c.id == "PS-004"), None)
            if check:
                assert check.result in ("PASS", "FAIL", "SKIP")
        finally:
            tmp.unlink(missing_ok=True)

    @given(st.text(max_size=5000))
    @settings(max_examples=50, deadline=5000)
    def test_prescreen_handles_any_yaml(self, text):
        """PS-005 must never crash on arbitrary text presented as .yaml."""
        ps = PreScreen()
        tmp = Path("/tmp/quorum_test_prop.yaml")
        tmp.write_text(text, encoding="utf-8")
        try:
            result = ps.run(tmp, text)
            check = next((c for c in result.checks if c.id == "PS-005"), None)
            if check:
                assert check.result in ("PASS", "FAIL", "SKIP")
        finally:
            tmp.unlink(missing_ok=True)

    @given(st.text(alphabet=st.characters(blacklist_categories=("Cc", "Cs")), max_size=3000))
    @settings(max_examples=30, deadline=5000)
    def test_prescreen_unicode_no_crash(self, text):
        """Unicode text must never cause a crash in any check."""
        ps = PreScreen()
        tmp = Path("/tmp/quorum_test_unicode.txt")
        tmp.write_text(text, encoding="utf-8")
        try:
            result = ps.run(tmp, text)
            assert result.total_checks >= 0
        finally:
            tmp.unlink(missing_ok=True)

    def test_prescreen_very_long_file(self, ps, tmp_path):
        """10MB file should complete (or be skipped) without crash."""
        f = tmp_path / "large.md"
        content = "# Header\n" + ("x" * 1000 + "\n") * 10000  # ~10MB
        f.write_text(content)
        result = ps.run(f, content)
        # Should either process or skip gracefully
        assert result.runtime_ms >= 0

    def test_prescreen_binary_content_safe(self, ps, tmp_path):
        """Binary content with null bytes should be handled gracefully."""
        f = tmp_path / "binary.md"
        f.write_bytes(b"\x00\x01\x02\x03\x04\x05")
        text = f.read_text(errors="replace")
        result = ps.run(f, text)
        # Binary detection should skip all checks
        assert result.total_checks == 0
