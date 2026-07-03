"""
Test suite for testing gate skill - core functionality.
"""

import pytest
from src import TestingGate, CoverageMetrics, TestStrategy, GateResult


class TestTestingGateInit:
    """Test TestingGate initialization."""

    def test_init_creates_empty_results(self):
        gate = TestingGate()
        assert gate.results == []

    def test_overall_passed_empty_returns_false(self):
        gate = TestingGate()
        assert gate.overall_passed() is False

    def test_clear_empties_results(self):
        gate = TestingGate()
        metrics = CoverageMetrics(80, 70, 80)
        gate.check_coverage(metrics)
        assert len(gate.results) == 1
        gate.clear()
        assert gate.results == []


class TestCoverageCheck:
    """Test coverage checking."""

    def test_coverage_all_targets_met(self):
        gate = TestingGate()
        metrics = CoverageMetrics(90, 80, 85)
        result = gate.check_coverage(metrics)
        assert result.passed is True
        assert result.check_name == "coverage"

    def test_coverage_line_below_target_fails(self):
        gate = TestingGate()
        metrics = CoverageMetrics(70, 80, 85)
        result = gate.check_coverage(metrics)
        assert result.passed is False
        assert result.details["line"]["passed"] is False

    def test_coverage_branch_below_target_fails(self):
        gate = TestingGate()
        metrics = CoverageMetrics(90, 60, 85)
        result = gate.check_coverage(metrics)
        assert result.passed is False
        assert result.details["branch"]["passed"] is False

    def test_coverage_function_below_target_fails(self):
        gate = TestingGate()
        metrics = CoverageMetrics(90, 80, 70)
        result = gate.check_coverage(metrics)
        assert result.passed is False
        assert result.details["function"]["passed"] is False

    def test_coverage_exact_target_passes(self):
        gate = TestingGate()
        metrics = CoverageMetrics(80, 70, 80)
        result = gate.check_coverage(metrics)
        assert result.passed is True

    def test_coverage_just_below_target_fails(self):
        gate = TestingGate()
        metrics = CoverageMetrics(79.9, 69.9, 79.9)
        result = gate.check_coverage(metrics)
        assert result.passed is False

    def test_coverage_score_is_between_zero_and_one(self):
        gate = TestingGate()
        metrics = CoverageMetrics(90, 80, 85)
        result = gate.check_coverage(metrics)
        assert 0.0 <= result.score <= 1.0

    def test_coverage_details_contain_all_layers(self):
        gate = TestingGate()
        metrics = CoverageMetrics(90, 80, 85)
        result = gate.check_coverage(metrics)
        assert "line" in result.details
        assert "branch" in result.details
        assert "function" in result.details


class TestTestStrategyCheck:
    """Test test strategy checking."""

    def test_strategy_valid_with_all_layers(self):
        gate = TestingGate()
        strategy = TestStrategy(
            unit_tests=["test_a", "test_b"],
            integration_tests=["test_int"],
            e2e_tests=["test_e2e"],
            min_test_count=1,
        )
        result = gate.check_test_strategy(strategy)
        assert result.passed is True

    def test_strategy_no_unit_tests_fails(self):
        gate = TestingGate()
        strategy = TestStrategy(
            unit_tests=[],
            integration_tests=["test_int"],
            e2e_tests=["test_e2e"],
        )
        result = gate.check_test_strategy(strategy)
        assert result.passed is False

    def test_strategy_below_min_count_fails(self):
        gate = TestingGate()
        strategy = TestStrategy(
            unit_tests=["test_a"],
            min_test_count=5,
        )
        result = gate.check_test_strategy(strategy)
        assert result.passed is False

    def test_strategy_exact_min_count_passes(self):
        gate = TestingGate()
        strategy = TestStrategy(
            unit_tests=["t1", "t2", "t3"],
            min_test_count=3,
        )
        result = gate.check_test_strategy(strategy)
        assert result.passed is True

    def test_strategy_only_unit_tests_passes(self):
        gate = TestingGate()
        strategy = TestStrategy(
            unit_tests=["t1", "t2"],
            integration_tests=[],
            e2e_tests=[],
        )
        result = gate.check_test_strategy(strategy)
        assert result.passed is True

    def test_strategy_details_total_tests(self):
        gate = TestingGate()
        strategy = TestStrategy(
            unit_tests=["a", "b"],
            integration_tests=["c"],
            e2e_tests=["d", "e"],
        )
        result = gate.check_test_strategy(strategy)
        assert result.details["total_tests"] == 5

    def test_strategy_layers_present_count(self):
        gate = TestingGate()
        strategy = TestStrategy(
            unit_tests=["a"],
            integration_tests=["b"],
            e2e_tests=["c"],
        )
        result = gate.check_test_strategy(strategy)
        assert result.details["layers_present"] == 3


class TestRegressionCheck:
    """Test regression checking."""

    def test_regression_no_regressions_all_pass(self):
        gate = TestingGate()
        artifacts = {
            "previous_passing": 50,
            "current_passing": 50,
            "current_total": 50,
        }
        result = gate.check_regression(artifacts)
        assert result.passed is True

    def test_regression_with_regressions_fails(self):
        gate = TestingGate()
        artifacts = {
            "previous_passing": 50,
            "current_passing": 48,
            "current_total": 50,
        }
        result = gate.check_regression(artifacts)
        assert result.passed is False
        assert result.details["regressions"] == 2

    def test_regression_zero_total_fails(self):
        gate = TestingGate()
        artifacts = {
            "previous_passing": 0,
            "current_passing": 0,
            "current_total": 0,
        }
        result = gate.check_regression(artifacts)
        assert result.passed is False

    def test_regression_details_pass_rate(self):
        gate = TestingGate()
        artifacts = {
            "previous_passing": 40,
            "current_passing": 40,
            "current_total": 50,
        }
        result = gate.check_regression(artifacts)
        assert result.details["pass_rate"] == 0.8


class TestRunAllChecks:
    """Test run_all_checks."""

    def test_run_all_checks_with_full_context(self):
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(90, 80, 85),
            "test_strategy": TestStrategy(unit_tests=["a"], min_test_count=1),
            "regression_artifacts": {
                "previous_passing": 10,
                "current_passing": 10,
                "current_total": 10,
            },
        }
        results = gate.run_all_checks(context)
        assert len(results) == 3
        assert gate.overall_passed() is True

    def test_run_all_checks_partial_context(self):
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(90, 80, 85),
        }
        results = gate.run_all_checks(context)
        assert len(results) == 1

    def test_run_all_checks_clears_previous_results(self):
        gate = TestingGate()
        gate.check_coverage(CoverageMetrics(90, 80, 85))
        assert len(gate.results) == 1
        context = {"test_strategy": TestStrategy(unit_tests=["a"])}
        gate.run_all_checks(context)
        assert len(gate.results) == 1
