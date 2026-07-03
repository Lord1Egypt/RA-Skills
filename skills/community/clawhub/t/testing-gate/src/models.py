"""
Data models for testing gate.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class CoverageMetrics:
    """Coverage metrics data."""
    line_coverage: float
    branch_coverage: float
    function_coverage: float
    target_line: float = 80.0
    target_branch: float = 70.0
    target_function: float = 80.0

    def overall_coverage(self) -> float:
        """Return average of the three coverage values."""
        return (self.line_coverage + self.branch_coverage + self.function_coverage) / 3.0

    def to_dict(self) -> Dict:
        return {
            "line_coverage": self.line_coverage,
            "branch_coverage": self.branch_coverage,
            "function_coverage": self.function_coverage,
            "target_line": self.target_line,
            "target_branch": self.target_branch,
            "target_function": self.target_function,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "CoverageMetrics":
        return cls(
            line_coverage=data["line_coverage"],
            branch_coverage=data["branch_coverage"],
            function_coverage=data["function_coverage"],
            target_line=data.get("target_line", 80.0),
            target_branch=data.get("target_branch", 70.0),
            target_function=data.get("target_function", 80.0),
        )


@dataclass
class TestStrategy:
    """Test strategy data."""

    __test__ = False  # prevent pytest from collecting this as a test class

    unit_tests: List[str] = field(default_factory=list)
    integration_tests: List[str] = field(default_factory=list)
    e2e_tests: List[str] = field(default_factory=list)
    min_test_count: int = 1

    def total_tests(self) -> int:
        """Return total number of tests across all layers."""
        return len(self.unit_tests) + len(self.integration_tests) + len(self.e2e_tests)

    def to_dict(self) -> Dict:
        return {
            "unit_tests": list(self.unit_tests),
            "integration_tests": list(self.integration_tests),
            "e2e_tests": list(self.e2e_tests),
            "min_test_count": self.min_test_count,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "TestStrategy":
        return cls(
            unit_tests=list(data.get("unit_tests", [])),
            integration_tests=list(data.get("integration_tests", [])),
            e2e_tests=list(data.get("e2e_tests", [])),
            min_test_count=data.get("min_test_count", 1),
        )


@dataclass
class GateResult:
    """Gate check result."""
    check_name: str
    passed: bool
    score: float
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "check_name": self.check_name,
            "passed": self.passed,
            "score": self.score,
            "message": self.message,
            "details": self.details,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "GateResult":
        return cls(
            check_name=data["check_name"],
            passed=data["passed"],
            score=data["score"],
            message=data["message"],
            details=data.get("details", {}),
        )
