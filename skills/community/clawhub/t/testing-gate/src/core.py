"""
Testing gate checker core.
"""

import threading
from typing import Dict, List
from .models import CoverageMetrics, TestStrategy, GateResult


class TestingGate:
    """Testing gate checker for coverage, strategy and regression."""

    __test__ = False  # prevent pytest from collecting this as a test class

    def __init__(self) -> None:
        self.results: List[GateResult] = []
        self._lock = threading.Lock()

    def check_coverage(self, metrics: CoverageMetrics) -> GateResult:
        """Check coverage metrics against targets."""
        checks = {
            "line": (metrics.line_coverage, metrics.target_line),
            "branch": (metrics.branch_coverage, metrics.target_branch),
            "function": (metrics.function_coverage, metrics.target_function),
        }

        details: Dict = {}
        all_passed = True
        ratios: List[float] = []

        for name, (value, target) in checks.items():
            ratio = (value / target) if target > 0 else 0.0
            ratios.append(min(ratio, 1.0))
            passed = value >= target
            if not passed:
                all_passed = False
            details[name] = {
                "value": value,
                "target": target,
                "passed": passed,
                "ratio": round(ratio, 4),
            }

        score = round(sum(ratios) / len(ratios), 4) if ratios else 0.0
        message = "All coverage targets met" if all_passed else "Some coverage targets not met"

        result = GateResult(
            check_name="coverage",
            passed=all_passed,
            score=score,
            message=message,
            details=details,
        )
        with self._lock:
            self.results.append(result)
        return result

    def check_test_strategy(self, strategy: TestStrategy) -> GateResult:
        """Check test strategy validity."""
        total = strategy.total_tests()
        has_unit = len(strategy.unit_tests) > 0
        meets_min = total >= strategy.min_test_count

        layers_present = sum([
            len(strategy.unit_tests) > 0,
            len(strategy.integration_tests) > 0,
            len(strategy.e2e_tests) > 0,
        ])

        details = {
            "total_tests": total,
            "min_test_count": strategy.min_test_count,
            "meets_min_count": meets_min,
            "has_unit_tests": has_unit,
            "has_integration_tests": len(strategy.integration_tests) > 0,
            "has_e2e_tests": len(strategy.e2e_tests) > 0,
            "layers_present": layers_present,
        }

        passed = meets_min and has_unit
        ratio = min(total / strategy.min_test_count, 1.0) if strategy.min_test_count > 0 else 1.0
        layer_score = layers_present / 3.0
        score = round((ratio + layer_score) / 2.0, 4)

        if not has_unit:
            message = "Test strategy missing unit tests"
        elif not meets_min:
            message = f"Test count {total} below minimum {strategy.min_test_count}"
        else:
            message = f"Test strategy valid with {total} tests across {layers_present} layers"

        result = GateResult(
            check_name="test_strategy",
            passed=passed,
            score=score,
            message=message,
            details=details,
        )
        with self._lock:
            self.results.append(result)
        return result

    def check_regression(self, artifacts: Dict) -> GateResult:
        """Check regression based on test artifacts."""
        previous_passing = artifacts.get("previous_passing", 0)
        current_passing = artifacts.get("current_passing", 0)
        current_total = artifacts.get("current_total", 0)
        new_tests = artifacts.get("new_tests", 0)

        regressions = max(0, previous_passing - current_passing)
        pass_rate = (current_passing / current_total) if current_total > 0 else 0.0
        all_current_pass = current_total > 0 and current_passing == current_total
        no_regressions = regressions == 0

        details = {
            "previous_passing": previous_passing,
            "current_passing": current_passing,
            "current_total": current_total,
            "new_tests": new_tests,
            "regressions": regressions,
            "pass_rate": round(pass_rate, 4),
            "all_current_pass": all_current_pass,
        }

        passed = no_regressions and all_current_pass
        score = round(pass_rate, 4) if current_total > 0 else 0.0

        if not no_regressions:
            message = f"{regressions} regression(s) detected"
        elif not all_current_pass:
            message = f"{current_total - current_passing} current test(s) failing"
        else:
            message = "No regressions detected, all tests pass"

        result = GateResult(
            check_name="regression",
            passed=passed,
            score=score,
            message=message,
            details=details,
        )
        with self._lock:
            self.results.append(result)
        return result

    def run_all_checks(self, context: Dict) -> List[GateResult]:
        """Run all checks based on context."""
        with self._lock:
            self.results = []
        if "coverage_metrics" in context:
            self.check_coverage(context["coverage_metrics"])
        if "test_strategy" in context:
            self.check_test_strategy(context["test_strategy"])
        if "regression_artifacts" in context:
            self.check_regression(context["regression_artifacts"])
        with self._lock:
            return list(self.results)

    def overall_passed(self) -> bool:
        """Return True if all recorded results passed."""
        with self._lock:
            if not self.results:
                return False
            return all(r.passed for r in self.results)

    def clear(self) -> None:
        """Clear recorded results."""
        with self._lock:
            self.results = []
