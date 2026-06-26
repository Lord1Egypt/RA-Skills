"""Case definition and loading for negotiation simulations.

Total score = Σ satisfaction_i * weight_i

- Weight: [0, 1], how much you care. Sums to 1 across all issues.
- Satisfaction: [0, 1], where the value landed in your preferred direction.
  0 = worst outcome, 1 = best outcome.
- Score = satisfaction * weight
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from itertools import product
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Issue:
    """A single negotiable issue.

    Continuous: value in [range_min, range_max].
      satisfaction = (value - worst) / (best - worst) per party.
    Discrete: categorical options with explicit satisfaction values.
    """
    name: str
    weight_a: float = 0.0  # [0, 1] — how much party A cares
    weight_b: float = 0.0  # [0, 1] — how much party B cares
    # --- Continuous ---
    continuous: bool = False
    range_min: float = 0.0
    range_max: float = 1.0
    best_for_a: str = "max"  # "max" or "min" — which end A prefers
    best_for_b: str = "max"  # "max" or "min" — which end B prefers
    unit: str = ""
    format_str: str = ""
    # --- Discrete ---
    discrete: bool = False
    option_labels: list[str] = field(default_factory=list)
    # satisfaction per option per party, [0, 1]
    satisfaction_a: dict[str, float] = field(default_factory=dict)
    satisfaction_b: dict[str, float] = field(default_factory=dict)

    def get_satisfaction(self, value: Any) -> tuple[float, float]:
        """Get satisfaction [0, 1] for both parties given a value."""
        if self.discrete:
            label = str(value)
            sa = self.satisfaction_a.get(label, 0.0)
            sb = self.satisfaction_b.get(label, 0.0)
            return sa, sb

        # Continuous
        v = self._parse_numeric(value)
        if v is None:
            return 0.0, 0.0
        rng = self.range_max - self.range_min
        if rng == 0:
            return 0.5, 0.5
        t = (v - self.range_min) / rng  # 0 at min, 1 at max
        t = max(0.0, min(1.0, t))
        sa = t if self.best_for_a == "max" else (1.0 - t)
        sb = t if self.best_for_b == "max" else (1.0 - t)
        return sa, sb

    def score(self, value: Any) -> tuple[float, float]:
        """Score = satisfaction * weight."""
        sa, sb = self.get_satisfaction(value)
        return sa * self.weight_a, sb * self.weight_b

    def _parse_numeric(self, value: Any) -> float | None:
        if isinstance(value, (int, float)):
            return float(value)
        nums = re.findall(r'[\d.]+', str(value))
        return float(nums[0]) if nums else None

    def format_value(self, value: float) -> str:
        if self.discrete:
            best_label, best_dist = None, float('inf')
            for label in self.option_labels:
                # For discrete, value is the label itself
                pass
            return str(value)
        if self.format_str:
            return self.format_str.replace("{v}", str(round(value)))
        return f"{value}"


@dataclass
class NegotiationCase:
    """A complete negotiation case."""
    title: str
    description: str
    party_a_name: str
    party_a_role: str
    party_a_background: str
    party_a_batna_score: float
    party_b_name: str
    party_b_role: str
    party_b_background: str
    party_b_batna_score: float
    issues: list[Issue] = field(default_factory=list)
    max_rounds: int = 8

    def all_possible_deals(self) -> list[dict[str, Any]]:
        """Generate deal combinations for visualization."""
        sample_lists = []
        for issue in self.issues:
            if issue.discrete:
                samples = [(issue.name, label) for label in issue.option_labels]
            else:
                n = 5
                samples = [
                    (issue.name, issue.range_min + (issue.range_max - issue.range_min) * k / (n - 1))
                    for k in range(n)
                ]
            sample_lists.append(samples)

        return [dict(combo) for combo in product(*sample_lists)]

    def score_deal(self, deal: dict[str, Any]) -> tuple[int, int]:
        """Total score = Σ satisfaction_i * weight_i. Scaled to 0-100."""
        a_total = 0.0
        b_total = 0.0
        for issue in self.issues:
            value = deal.get(issue.name)
            if value is None:
                continue
            a, b = issue.score(value)
            a_total += a
            b_total += b
        # Scale to 0-100 for display
        return round(a_total * 100), round(b_total * 100)


def load_case(path: str | Path) -> NegotiationCase:
    """Load a negotiation case from a YAML file."""
    with open(path) as f:
        data = yaml.safe_load(f)

    issues = []
    for issue_data in data.get("issues", []):
        if "options" in issue_data:
            # Discrete issue
            option_labels = list(issue_data["options"].keys())
            opts = issue_data["options"]

            # Get raw scores
            a_scores = [opts[o]["party_a"] for o in option_labels]
            b_scores = [opts[o]["party_b"] for o in option_labels]

            # Normalize to satisfaction [0, 1]
            a_min, a_max = min(a_scores), max(a_scores)
            b_min, b_max = min(b_scores), max(b_scores)
            a_range = a_max - a_min if a_max != a_min else 1
            b_range = b_max - b_min if b_max != b_min else 1

            satisfaction_a = {o: (opts[o]["party_a"] - a_min) / a_range for o in option_labels}
            satisfaction_b = {o: (opts[o]["party_b"] - b_min) / b_range for o in option_labels}

            issues.append(Issue(
                name=issue_data["name"],
                weight_a=issue_data.get("weight_a", 0.0),
                weight_b=issue_data.get("weight_b", 0.0),
                discrete=True,
                option_labels=option_labels,
                satisfaction_a=satisfaction_a,
                satisfaction_b=satisfaction_b,
            ))
        else:
            # Continuous issue
            r = issue_data["range"]
            issues.append(Issue(
                name=issue_data["name"],
                weight_a=issue_data.get("weight_a", 0.0),
                weight_b=issue_data.get("weight_b", 0.0),
                continuous=True,
                range_min=r["min"],
                range_max=r["max"],
                best_for_a=r.get("best_for_a", "max"),
                best_for_b=r.get("best_for_b", "max"),
                unit=issue_data.get("unit", ""),
                format_str=issue_data.get("format", ""),
            ))

    return NegotiationCase(
        title=data["title"],
        description=data.get("description", ""),
        party_a_name=data["party_a"]["name"],
        party_a_role=data["party_a"]["role"],
        party_a_background=data["party_a"]["background"],
        party_a_batna_score=data["party_a"].get("batna_score", 0),
        party_b_name=data["party_b"]["name"],
        party_b_role=data["party_b"]["role"],
        party_b_background=data["party_b"]["background"],
        party_b_batna_score=data["party_b"].get("batna_score", 0),
        issues=issues,
        max_rounds=data.get("max_rounds", 8),
    )
