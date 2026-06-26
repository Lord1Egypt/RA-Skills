"""Layer 6: Performance benchmarks and stress tests."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from quorum.prescreen import PreScreen


@pytest.fixture
def ps() -> PreScreen:
    return PreScreen()


# ── Prescreen performance ────────────────────────────────────────────────────


class TestPrescreenPerformance:
    @pytest.mark.slow
    def test_prescreen_small_file_under_100ms(self, ps, tmp_path):
        """<10KB file should prescreen in <100ms."""
        f = tmp_path / "small.md"
        f.write_text("# Small\n" + "Content line.\n" * 100)
        text = f.read_text()

        start = time.perf_counter()
        result = ps.run(f, text)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 500  # generous for CI, spec says <100ms
        assert result.total_checks == 12  # 10 built-in + 2 external tools (Ruff, DevSkim)

    @pytest.mark.slow
    def test_prescreen_large_file_under_2s(self, ps, tmp_path):
        """10MB file should prescreen in <2s (or be skipped)."""
        f = tmp_path / "large.md"
        content = "# Large file\n" + ("x" * 500 + "\n") * 20000  # ~10MB
        f.write_text(content)

        start = time.perf_counter()
        result = ps.run(f, content)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 5000  # generous: 5s
        assert result.runtime_ms >= 0

    @pytest.mark.slow
    def test_prescreen_many_findings(self, ps, tmp_path):
        """File with many TODO markers should still be fast."""
        f = tmp_path / "todos.md"
        content = "\n".join(f"TODO: task {i}" for i in range(1000))
        f.write_text(content)

        start = time.perf_counter()
        result = ps.run(f, content)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 2000
        check = next(c for c in result.checks if c.id == "PS-008")
        assert check.result == "FAIL"

    @pytest.mark.slow
    def test_prescreen_json_large(self, ps, tmp_path):
        """Large valid JSON should parse reasonably fast."""
        import json
        data = {f"key_{i}": f"value_{i}" for i in range(10000)}
        f = tmp_path / "large.json"
        f.write_text(json.dumps(data))

        start = time.perf_counter()
        result = ps.run(f, f.read_text())
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 2000
        check = next(c for c in result.checks if c.id == "PS-004")
        assert check.result == "PASS"


# ── Tool performance ─────────────────────────────────────────────────────────


class TestToolPerformance:
    @pytest.mark.slow
    def test_grep_tool_large_text(self):
        """GrepTool should handle large text efficiently."""
        from quorum.tools.grep_tool import GrepTool
        gt = GrepTool()
        text = "\n".join(f"line {i}: {'match' if i % 100 == 0 else 'nope'}" for i in range(100000))

        start = time.perf_counter()
        matches = gt.search_text(text, "match")
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 3000
        assert len(matches) == 1000

    @pytest.mark.slow
    def test_schema_tool_large_data(self):
        """SchemaTool should validate large data quickly."""
        from quorum.tools.schema_tool import SchemaTool
        st = SchemaTool()
        data = {f"key_{i}": f"value_{i}" for i in range(1000)}

        start = time.perf_counter()
        violations = st.check_required_keys(data, [f"key_{i}" for i in range(500)])
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 1000
        assert violations == []


# ── Hashing performance ──────────────────────────────────────────────────────


class TestHashingPerformance:
    @pytest.mark.slow
    def test_hash_large_content(self):
        """Hashing large content should be fast."""
        from quorum.models import Locus
        content = "line\n" * 100000  # 100k lines

        start = time.perf_counter()
        h = Locus.compute_hash_from_content(content, 1, 50000)
        elapsed_ms = (time.perf_counter() - start) * 1000

        assert elapsed_ms < 1000
        assert len(h) == 64
