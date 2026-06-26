"""Tests for sal.results_log — TSV experiment logging."""

import os
import tempfile

import pytest

from sal.results_log import ResultsLog


@pytest.fixture
def tmp_log():
    """Create a temp TSV log."""
    d = tempfile.mkdtemp()
    path = os.path.join(d, "results.tsv")
    return ResultsLog(path)


class TestResultsLog:
    def test_creates_file_with_header(self, tmp_log):
        """should create TSV file with header on init."""
        assert tmp_log.path.exists()
        content = tmp_log.path.read_text()
        assert "iteration\t" in content

    def test_log_and_read(self, tmp_log):
        """should log entries and read them back."""
        tmp_log.log(0, commit="a1b2c3d", metric_value=0.998, status="keep",
                    hypothesis="baseline", duration_s=300)
        tmp_log.log(1, commit="b2c3d4e", metric_value=0.993, status="keep",
                    hypothesis="increase LR", duration_s=310)

        h = tmp_log.history
        assert len(h) == 2
        assert h[0]["iteration"] == 0
        assert h[1]["metric_value"] == pytest.approx(0.993, abs=0.001)

    def test_best_minimize(self, tmp_log):
        """should return lowest metric when minimize=True."""
        tmp_log.log(0, metric_value=1.0, status="keep")
        tmp_log.log(1, metric_value=0.95, status="keep")
        tmp_log.log(2, metric_value=0.97, status="keep")

        best = tmp_log.best(minimize=True)
        assert best is not None
        assert best["metric_value"] == pytest.approx(0.95, abs=0.01)

    def test_best_maximize(self, tmp_log):
        """should return highest metric when minimize=False."""
        tmp_log.log(0, metric_value=80.0, status="keep")
        tmp_log.log(1, metric_value=95.0, status="keep")
        tmp_log.log(2, metric_value=90.0, status="keep")

        best = tmp_log.best(minimize=False)
        assert best is not None
        assert best["metric_value"] == pytest.approx(95.0, abs=0.1)

    def test_best_ignores_discarded(self, tmp_log):
        """should only consider entries with status 'keep'."""
        tmp_log.log(0, metric_value=1.0, status="keep")
        tmp_log.log(1, metric_value=0.5, status="discard")  # Better but discarded

        best = tmp_log.best(minimize=True)
        assert best is not None
        assert best["metric_value"] == pytest.approx(1.0, abs=0.01)

    def test_empty_log_best(self, tmp_log):
        """should return None for empty log."""
        assert tmp_log.best() is None

    def test_count(self, tmp_log):
        """should return correct count."""
        assert tmp_log.count == 0
        tmp_log.log(0, status="keep")
        tmp_log.log(1, status="discard")
        assert tmp_log.count == 2

    def test_error_in_hypothesis(self, tmp_log):
        """should append error to hypothesis text."""
        tmp_log.log(0, hypothesis="try X", error="OOM")
        h = tmp_log.history
        assert "OOM" in h[0]["hypothesis"]
