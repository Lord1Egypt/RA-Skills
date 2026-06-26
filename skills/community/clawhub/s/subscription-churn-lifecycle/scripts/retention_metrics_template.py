"""
Helper for the `subscription-churn-lifecycle` skill.

Provides a structured template for key subscription retention metrics so that
different runs can refer to the same keys when generating checklists or tables.
"""

from __future__ import annotations

from typing import Dict, List


RETENTION_METRICS: Dict[str, List[str]] = {
    "Outcome metrics": [
        "First-month retention (M1)",
        "Month-2 / Month-3 retention (M2/M3)",
        "Average subscription cycles",
        "Subscription LTV/CLV",
        "Overall cancel rate (by cycle)",
        "Win-back rate (churned who re-subscribe)",
    ],
    "Process metrics": [
        "Onboarding content open/click rate",
        "First use/unbox completion rate",
        "Use days/frequency per cycle",
        "Billing preview open/click rate",
        "Cancel reason form completion rate",
        "Win-back/return campaign response and conversion",
    ],
}


def as_markdown_table() -> str:
    """
    Render the metric categories as a markdown table skeleton that can be
    embedded into skill outputs.
    """
    lines: List[str] = []
    lines.append("| Metric type | Metric | Current/estimate | Target | Notes |")
    lines.append("| --- | --- | --- | --- | --- |")

    for metric_type, items in RETENTION_METRICS.items():
        for item in items:
            lines.append(f"| {metric_type} | {item} |  |  |  |")

    return "\n".join(lines)


if __name__ == "__main__":
    print(as_markdown_table())
