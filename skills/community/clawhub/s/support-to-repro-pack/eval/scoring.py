"""Scoring data models for evaluation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Score:
    dimension: str
    score: float
    max_score: float
    details: str

    @property
    def percentage(self) -> float:
        if self.max_score == 0:
            return 0
        return round(self.score / self.max_score * 100, 1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "dimension": self.dimension,
            "score": self.score,
            "max_score": self.max_score,
            "percentage": self.percentage,
            "details": self.details,
        }


@dataclass
class CaseScore:
    case_name: str
    scores: list[Score] = field(default_factory=list)

    @property
    def total_score(self) -> float:
        return sum(s.score for s in self.scores)

    @property
    def total_max(self) -> float:
        return sum(s.max_score for s in self.scores)

    @property
    def total_percentage(self) -> float:
        if self.total_max == 0:
            return 0
        return round(self.total_score / self.total_max * 100, 1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_name": self.case_name,
            "scores": [s.to_dict() for s in self.scores],
            "total_score": self.total_score,
            "total_max": self.total_max,
            "total_percentage": self.total_percentage,
        }


@dataclass
class EvalResult:
    cases: list[CaseScore] = field(default_factory=list)

    @property
    def aggregate_score(self) -> float:
        total = sum(c.total_score for c in self.cases)
        maximum = sum(c.total_max for c in self.cases)
        if maximum == 0:
            return 0
        return round(total / maximum * 100, 1)

    def dimension_averages(self) -> dict[str, float]:
        """Average percentage per dimension across all cases."""
        dims: dict[str, list[float]] = {}
        for case in self.cases:
            for score in case.scores:
                dims.setdefault(score.dimension, []).append(score.percentage)
        return {dim: round(sum(vals) / len(vals), 1) for dim, vals in dims.items()}

    def to_dict(self) -> dict[str, Any]:
        return {
            "cases": [c.to_dict() for c in self.cases],
            "aggregate_score": self.aggregate_score,
            "dimension_averages": self.dimension_averages(),
        }
