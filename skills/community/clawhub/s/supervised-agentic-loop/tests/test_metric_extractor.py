"""Tests for sal.metric_extractor — all 6 strategies + regex."""

import pytest

from sal.exceptions import MetricParseError
from sal.metric_extractor import BUILTIN_PARSERS, extract_metric, get_parser


class TestNamedStrategies:
    def test_last_line_float(self):
        """should extract float from last line."""
        assert extract_metric("training done\n0.9932", "last_line_float") == 0.9932

    def test_pytest_passed(self):
        """should extract passed count from pytest output."""
        output = "====== 42 passed, 1 warning in 2.34s ======"
        assert extract_metric(output, "pytest_passed") == 42.0

    def test_pytest_failed(self):
        """should extract failed count from pytest output."""
        output = "FAILED test_x.py::test_a - 3 failed, 10 passed"
        assert extract_metric(output, "pytest_failed") == 3.0

    def test_coverage_percent(self):
        """should extract coverage percentage."""
        output = "TOTAL                    456    32    93%"
        assert extract_metric(output, "coverage_percent") == 93.0

    def test_val_bpb(self):
        """should extract val_bpb value."""
        output = "step 1000\nval_bpb: 1.0423\nloss: 2.34"
        assert extract_metric(output, "val_bpb") == 1.0423

    def test_benchmark_ms(self):
        """should extract milliseconds from benchmark output."""
        output = "Average: 42.5 ms per iteration"
        assert extract_metric(output, "benchmark_ms") == 42.5


class TestRegexFallback:
    def test_valid_regex(self):
        """should use regex with one capture group."""
        assert extract_metric("score: 98.7", r"score:\s+([\d.]+)") == 98.7

    def test_regex_no_capture_group(self):
        """should reject regex with zero capture groups."""
        with pytest.raises(ValueError, match="exactly 1 capture group"):
            get_parser(r"\d+")

    def test_regex_two_capture_groups(self):
        """should reject regex with two capture groups."""
        with pytest.raises(ValueError, match="exactly 1 capture group"):
            get_parser(r"(\d+).*(\d+)")


class TestEdgeCases:
    def test_unknown_parser(self):
        """should raise ValueError for unknown parser name."""
        with pytest.raises(ValueError, match="capture group"):
            get_parser("totally_unknown")

    def test_metric_parse_error_on_no_match(self):
        """should raise MetricParseError when regex doesn't match."""
        with pytest.raises(MetricParseError, match="Failed to extract"):
            extract_metric("no numbers here", r"score:\s+([\d.]+)")

    def test_last_line_float_non_numeric(self):
        """should raise MetricParseError for non-numeric last line."""
        with pytest.raises(MetricParseError):
            extract_metric("result: good", "last_line_float")

    def test_all_builtins_registered(self):
        """should have exactly 6 builtin parsers."""
        assert len(BUILTIN_PARSERS) == 6
