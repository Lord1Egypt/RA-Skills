#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
from dataclasses import dataclass


POLICY_START = dt.date(2025, 1, 1)


@dataclass(frozen=True)
class CategoryRule:
    base_age_years: int
    delay_step_months: int
    delay_gain_months: int
    delay_cap_months: int


CATEGORY_RULES = {
    "male_60": CategoryRule(base_age_years=60, delay_step_months=4, delay_gain_months=1, delay_cap_months=36),
    "female_55": CategoryRule(base_age_years=55, delay_step_months=4, delay_gain_months=1, delay_cap_months=36),
    "female_50": CategoryRule(base_age_years=50, delay_step_months=2, delay_gain_months=1, delay_cap_months=60),
}


def add_months(d: dt.date, months: int) -> dt.date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    day = min(d.day, [31, 29 if y % 4 == 0 and (y % 100 != 0 or y % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return dt.date(y, m, day)


def month_diff(a: dt.date, b: dt.date) -> int:
    return (b.year - a.year) * 12 + (b.month - a.month)


def min_contribution_required_months(retire_date: dt.date) -> int:
    # 2030-01 起从15年逐年增加0.5年，至20年封顶
    if retire_date < dt.date(2030, 1, 1):
        return 15 * 12
    years_from_2030 = retire_date.year - 2030
    extra_months = min(60, (years_from_2030 + 1) * 6)
    return 15 * 12 + extra_months


def calculate_retirement_date(birth_date: dt.date, category: str) -> dict:
    if category not in CATEGORY_RULES:
        raise ValueError(f"Unsupported category: {category}")

    rule = CATEGORY_RULES[category]
    base_retire = dt.date(birth_date.year + rule.base_age_years, birth_date.month, birth_date.day)

    if base_retire < POLICY_START:
        delay = 0
    else:
        months_from_start = month_diff(POLICY_START, dt.date(base_retire.year, base_retire.month, 1))
        delay_steps = months_from_start // rule.delay_step_months + 1
        delay = min(rule.delay_cap_months, delay_steps * rule.delay_gain_months)

    legal_retire = add_months(base_retire, delay)
    legal_age_months = rule.base_age_years * 12 + delay

    return {
        "birth_date": birth_date.isoformat(),
        "category": category,
        "base_retirement_date": base_retire.isoformat(),
        "delay_months": delay,
        "legal_retirement_date": legal_retire.isoformat(),
        "legal_retirement_age_years": legal_age_months // 12,
        "legal_retirement_age_extra_months": legal_age_months % 12,
        "minimum_contribution_required_months": min_contribution_required_months(legal_retire),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate statutory retirement date under gradual delay policy.")
    parser.add_argument("--birth-date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--category", required=True, choices=sorted(CATEGORY_RULES.keys()))
    args = parser.parse_args()

    birth_date = dt.date.fromisoformat(args.birth_date)
    result = calculate_retirement_date(birth_date, args.category)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
