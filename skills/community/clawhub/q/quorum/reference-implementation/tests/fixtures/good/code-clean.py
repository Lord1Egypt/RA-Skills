"""A clean Python module with no issues."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Result:
    """Represents a computation result."""
    value: float
    label: str
    confidence: float = 1.0

    def is_valid(self) -> bool:
        return 0.0 <= self.confidence <= 1.0


def compute_average(values: list[float]) -> float:
    """Compute arithmetic mean of a list of numbers."""
    if not values:
        return 0.0
    return sum(values) / len(values)


def filter_results(results: list[Result], min_confidence: float = 0.5) -> list[Result]:
    """Filter results by minimum confidence threshold."""
    return [r for r in results if r.confidence >= min_confidence]
