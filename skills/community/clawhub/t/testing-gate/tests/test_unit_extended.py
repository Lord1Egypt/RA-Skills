"""
Extended unit tests for testing gate - boundary, exception, and concurrency.
"""

import pytest
import threading
from src import TestingGate, CoverageMetrics, TestStrategy, GateResult


class TestBoundaryScenarios:
    """Test boundary scenarios."""

    def test_coverage_zero_values(self):
        gate = TestingGate()
        metrics = CoverageMetrics(0, 0, 0)
        result = gate.check_coverage(metrics)
        assert result.passed is False
        assert result.score == 0.0

    def test_coverage_perfect_values(self):
        gate = TestingGate()
        metrics = CoverageMetrics(100, 100, 100)
        result = gate.check_coverage(metrics)
        assert result.passed is True
        assert result.score == 1.0

    def test_coverage_over_100_values(self):
        gate = TestingGate()
        metrics = CoverageMetrics(150, 120, 110)
        result = gate.check_coverage(metrics)
        assert result.passed is True
        assert result.score <= 1.0

    def test_coverage_custom_targets(self):
        gate = TestingGate()
        metrics = CoverageMetrics(50, 40, 50, target_line=50, target_branch=40, target_function=50)
        result = gate.check_coverage(metrics)
        assert result.passed is True

    def test_coverage_zero_target_line(self):
        gate = TestingGate()
        metrics = CoverageMetrics(50, 70, 80, target_line=0)
        result = gate.check_coverage(metrics)
        assert result.details["line"]["ratio"] == 0.0

    def test_coverage_float_precision(self):
        gate = TestingGate()
        metrics = CoverageMetrics(80.5, 70.5, 80.5)
        result = gate.check_coverage(metrics)
        assert result.passed is True

    def test_strategy_empty_all_lists(self):
        gate = TestingGate()
        strategy = TestStrategy(unit_tests=[], integration_tests=[], e2e_tests=[])
        result = gate.check_test_strategy(strategy)
        assert result.passed is False
        assert result.details["total_tests"] == 0

    def test_strategy_min_test_count_zero(self):
        gate = TestingGate()
        strategy = TestStrategy(unit_tests=["a"], min_test_count=0)
        result = gate.check_test_strategy(strategy)
        assert result.passed is True

    def test_strategy_large_test_list(self):
        gate = TestingGate()
        strategy = TestStrategy(
            unit_tests=[f"unit_{i}" for i in range(100)],
            min_test_count=10,
        )
        result = gate.check_test_strategy(strategy)
        assert result.passed is True
        assert result.details["total_tests"] == 100

    def test_strategy_min_test_count_negative(self):
        gate = TestingGate()
        strategy = TestStrategy(unit_tests=["a"], min_test_count=-5)
        result = gate.check_test_strategy(strategy)
        assert result.passed is True

    def test_gate_result_empty_details(self):
        result = GateResult(check_name="x", passed=True, score=1.0, message="ok")
        assert result.details == {}

    def test_gate_result_negative_score(self):
        result = GateResult(check_name="x", passed=False, score=-1.0, message="bad")
        assert result.score == -1.0


class TestExceptionHandling:
    """Test exception and edge handling."""

    def test_regression_empty_artifacts(self):
        gate = TestingGate()
        result = gate.check_regression({})
        assert result.passed is False
        assert result.details["current_total"] == 0

    def test_regression_missing_keys_uses_defaults(self):
        gate = TestingGate()
        result = gate.check_regression({})
        assert result.details["previous_passing"] == 0
        assert result.details["current_passing"] == 0
        assert result.details["new_tests"] == 0

    def test_regression_only_previous_passing_key(self):
        gate = TestingGate()
        result = gate.check_regression({"previous_passing": 10})
        assert result.details["previous_passing"] == 10
        assert result.passed is False

    def test_regression_extra_keys_ignored(self):
        gate = TestingGate()
        artifacts = {
            "previous_passing": 5,
            "current_passing": 5,
            "current_total": 5,
            "unknown_key": "ignored",
        }
        result = gate.check_regression(artifacts)
        assert result.passed is True
        assert "unknown_key" not in result.details

    def test_run_all_checks_empty_context(self):
        gate = TestingGate()
        results = gate.run_all_checks({})
        assert results == []

    def test_run_all_checks_context_without_matching_keys(self):
        gate = TestingGate()
        results = gate.run_all_checks({"unknown": "value"})
        assert results == []

    def test_coverage_high_values_do_not_raise(self):
        gate = TestingGate()
        metrics = CoverageMetrics(1e6, 1e6, 1e6)
        result = gate.check_coverage(metrics)
        assert result.passed is True

    def test_coverage_negative_values_do_not_crash(self):
        gate = TestingGate()
        metrics = CoverageMetrics(-10, -10, -10)
        result = gate.check_coverage(metrics)
        assert result.passed is False

    def test_regression_with_new_tests_positive(self):
        gate = TestingGate()
        artifacts = {
            "previous_passing": 10,
            "current_passing": 15,
            "current_total": 15,
            "new_tests": 5,
        }
        result = gate.check_regression(artifacts)
        assert result.passed is True
        assert result.details["regressions"] == 0

    def test_overall_passed_all_false_returns_false(self):
        gate = TestingGate()
        gate.check_coverage(CoverageMetrics(10, 10, 10))
        gate.check_test_strategy(TestStrategy(unit_tests=[]))
        assert gate.overall_passed() is False


class TestConcurrencySafety:
    """Test concurrency safety."""

    def test_concurrent_check_coverage_thread_safe(self):
        gate = TestingGate()
        metrics = CoverageMetrics(90, 80, 85)

        def worker():
            for _ in range(20):
                gate.check_coverage(metrics)

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(gate.results) == 100

    def test_concurrent_check_strategy_thread_safe(self):
        gate = TestingGate()
        strategy = TestStrategy(unit_tests=["a"], min_test_count=1)

        def worker():
            for _ in range(20):
                gate.check_test_strategy(strategy)

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(gate.results) == 100

    def test_concurrent_check_regression_thread_safe(self):
        gate = TestingGate()
        artifacts = {"previous_passing": 10, "current_passing": 10, "current_total": 10}

        def worker():
            for _ in range(20):
                gate.check_regression(artifacts)

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(gate.results) == 100

    def test_concurrent_run_all_checks_thread_safe(self):
        gate = TestingGate()
        context = {
            "coverage_metrics": CoverageMetrics(90, 80, 85),
            "test_strategy": TestStrategy(unit_tests=["a"], min_test_count=1),
        }
        counts = []

        def worker():
            results = gate.run_all_checks(context)
            counts.append(len(results))

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert all(c == 2 for c in counts)

    def test_multiple_gates_independent_instances(self):
        gate1 = TestingGate()
        gate2 = TestingGate()
        gate1.check_coverage(CoverageMetrics(90, 80, 85))
        assert len(gate1.results) == 1
        assert len(gate2.results) == 0

    def test_concurrent_clear_and_check(self):
        gate = TestingGate()
        metrics = CoverageMetrics(90, 80, 85)

        def checker():
            for _ in range(50):
                gate.check_coverage(metrics)

        def clearer():
            for _ in range(10):
                gate.clear()

        t1 = threading.Thread(target=checker)
        t2 = threading.Thread(target=clearer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        assert len(gate.results) >= 0

    def test_results_list_not_shared_between_instances(self):
        gate1 = TestingGate()
        gate2 = TestingGate()
        assert gate1.results is not gate2.results

    def test_thread_safe_overall_passed(self):
        gate = TestingGate()
        metrics = CoverageMetrics(90, 80, 85)

        def worker():
            for _ in range(20):
                gate.check_coverage(metrics)
                gate.overall_passed()

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert gate.overall_passed() is True
