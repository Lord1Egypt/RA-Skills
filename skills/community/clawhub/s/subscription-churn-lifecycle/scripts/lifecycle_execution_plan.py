"""
Utility script for the `subscription-churn-lifecycle` skill.

Generates a simple 4–8 week lifecycle execution plan focused on churn prevention
and retention, based on high-level focus areas (e.g., onboarding, usage
education, pre-renewal reminders, win-back).

This is intentionally lightweight: the skill or the user should adjust the
generated plan to fit their actual team capacity and tools.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class LifecycleWeek:
    week: int
    theme: str
    goals: List[str]
    tasks: List[str]


def generate_lifecycle_plan(
    focus_areas: List[str] | None = None,
    weeks: int = 6,
) -> List[LifecycleWeek]:
    """
    Generate a lifecycle execution plan.

    :param focus_areas: Optional list of high-level focus areas
                        (e.g. ["Onboarding", "Pre-renewal reminder", "Win-back"]).
                        If omitted, a default sequence will be used.
    :param weeks: Number of weeks to plan for (4–8 is recommended).
    """
    if weeks <= 0:
        raise ValueError("weeks must be positive")

    default_focus = [
        "Subscription model and data diagnosis",
        "Onboarding and first-cycle experience",
        "Usage context and habit building",
        "Pre-renewal reminder and value recap",
        "Cancel path and reason collection",
        "Win-back and return experiments",
    ]

    areas = focus_areas or default_focus

    def default_goals_for_area(area: str) -> List[str]:
        return [
            f"Set 1–2 measurable goals for \"{area}\" this week",
            f"Ship at least 1 change or experiment related to \"{area}\"",
        ]

    def default_tasks_for_area(area: str) -> List[str]:
        return [
            f"Review current touchpoints/copy/config for \"{area}\"",
            f"Design and review 1–2 changes (start small)",
            f"Configure and launch in tooling; record metrics and observation window",
        ]

    plan: List[LifecycleWeek] = []

    for i in range(weeks):
        area_index = min(i, len(areas) - 1)
        area = areas[area_index]
        plan.append(
            LifecycleWeek(
                week=i + 1,
                theme=area,
                goals=default_goals_for_area(area),
                tasks=default_tasks_for_area(area),
            )
        )

    return plan


def plan_to_dict(plan: List[LifecycleWeek]) -> List[Dict[str, Any]]:
    """Convert plan to a list of serializable dicts."""
    return [asdict(item) for item in plan]


def print_plan(plan: List[LifecycleWeek]) -> None:
    """Pretty-print the plan in a CLI-friendly format."""
    for item in plan:
        print(f"Week {item.week} theme: {item.theme}")
        print("  Goals:")
        for g in item.goals:
            print(f"    - {g}")
        print("  Key tasks:")
        for t in item.tasks:
            print(f"    - {t}")
        print()


if __name__ == "__main__":
    plan = generate_lifecycle_plan()
    print_plan(plan)
