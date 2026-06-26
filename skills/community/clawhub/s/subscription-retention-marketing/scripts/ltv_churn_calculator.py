#!/usr/bin/env python3
"""
LTV & Churn Impact Calculator for subscription businesses.

Calculates the revenue impact of reducing monthly churn rate
and estimates subscriber lifetime value.

Usage:
    python3 ltv_churn_calculator.py --arpu 35 --churn-rate 8 --improvement 1
    python3 ltv_churn_calculator.py --arpu 35 --churn-rate 8 --improvement 1 --subscribers 500
"""

import argparse
import sys


def calculate_ltv(arpu: float, monthly_churn_pct: float) -> dict:
    churn_rate = monthly_churn_pct / 100.0
    if churn_rate <= 0 or churn_rate >= 1:
        return {"error": "Churn rate must be between 0% and 100% (exclusive)."}

    avg_lifetime_months = 1.0 / churn_rate
    ltv = arpu * avg_lifetime_months
    annual_revenue_per_sub = arpu * 12
    month_3_retention = (1 - churn_rate) ** 3 * 100
    month_6_retention = (1 - churn_rate) ** 6 * 100
    month_12_retention = (1 - churn_rate) ** 12 * 100

    return {
        "arpu": arpu,
        "monthly_churn_pct": monthly_churn_pct,
        "avg_lifetime_months": round(avg_lifetime_months, 1),
        "ltv": round(ltv, 2),
        "annual_revenue_per_sub": round(annual_revenue_per_sub, 2),
        "retention_month_3": round(month_3_retention, 1),
        "retention_month_6": round(month_6_retention, 1),
        "retention_month_12": round(month_12_retention, 1),
    }


def compare_scenarios(
    arpu: float,
    current_churn_pct: float,
    improvement_pct_points: float,
    subscriber_count: int = 1000,
) -> dict:
    new_churn_pct = current_churn_pct - improvement_pct_points
    if new_churn_pct <= 0:
        new_churn_pct = 0.5

    current = calculate_ltv(arpu, current_churn_pct)
    improved = calculate_ltv(arpu, new_churn_pct)

    if "error" in current or "error" in improved:
        return {"error": current.get("error") or improved.get("error")}

    ltv_delta = improved["ltv"] - current["ltv"]
    annual_delta_per_sub = ltv_delta  # simplified: LTV gain realized over lifetime
    total_annual_impact = ltv_delta * subscriber_count

    return {
        "current": current,
        "improved": improved,
        "improvement_pct_points": improvement_pct_points,
        "subscriber_count": subscriber_count,
        "ltv_delta_per_sub": round(ltv_delta, 2),
        "total_ltv_impact": round(total_annual_impact, 2),
        "extra_lifetime_months": round(
            improved["avg_lifetime_months"] - current["avg_lifetime_months"], 1
        ),
    }


def format_report(result: dict) -> str:
    if "error" in result:
        return f"Error: {result['error']}"

    c = result["current"]
    i = result["improved"]
    lines = [
        "",
        "=" * 60,
        "  SUBSCRIPTION LTV & CHURN IMPACT REPORT",
        "=" * 60,
        "",
        f"  ARPU (avg revenue/subscriber/month):  ${c['arpu']:.2f}",
        f"  Subscriber base:                      {result['subscriber_count']:,}",
        "",
        "-" * 60,
        f"  {'Metric':<35} {'Current':>10} {'Improved':>10}",
        "-" * 60,
        f"  {'Monthly churn rate':<35} {c['monthly_churn_pct']:>9.1f}% {i['monthly_churn_pct']:>9.1f}%",
        f"  {'Avg subscriber lifetime (months)':<35} {c['avg_lifetime_months']:>10.1f} {i['avg_lifetime_months']:>10.1f}",
        f"  {'Subscriber LTV':<35} ${c['ltv']:>9.2f} ${i['ltv']:>9.2f}",
        f"  {'Month-3 retention':<35} {c['retention_month_3']:>9.1f}% {i['retention_month_3']:>9.1f}%",
        f"  {'Month-6 retention':<35} {c['retention_month_6']:>9.1f}% {i['retention_month_6']:>9.1f}%",
        f"  {'Month-12 retention':<35} {c['retention_month_12']:>9.1f}% {i['retention_month_12']:>9.1f}%",
        "",
        "-" * 60,
        "  IMPACT OF CHURN REDUCTION",
        "-" * 60,
        f"  Churn improvement:         {result['improvement_pct_points']:.1f} percentage points",
        f"  Extra lifetime per sub:    +{result['extra_lifetime_months']:.1f} months",
        f"  LTV gain per subscriber:   +${result['ltv_delta_per_sub']:.2f}",
        f"  Total LTV impact ({result['subscriber_count']:,} subs): +${result['total_ltv_impact']:,.2f}",
        "",
        "=" * 60,
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate subscription LTV and churn reduction impact"
    )
    parser.add_argument(
        "--arpu",
        type=float,
        required=True,
        help="Average revenue per subscriber per month (USD)",
    )
    parser.add_argument(
        "--churn-rate",
        type=float,
        required=True,
        help="Current monthly churn rate (percentage, e.g. 8 for 8%%)",
    )
    parser.add_argument(
        "--improvement",
        type=float,
        required=True,
        help="Target churn reduction in percentage points (e.g. 1 for 1%%)",
    )
    parser.add_argument(
        "--subscribers",
        type=int,
        default=1000,
        help="Number of active subscribers (default: 1000)",
    )
    args = parser.parse_args()

    result = compare_scenarios(
        arpu=args.arpu,
        current_churn_pct=args.churn_rate,
        improvement_pct_points=args.improvement,
        subscriber_count=args.subscribers,
    )

    print(format_report(result))


if __name__ == "__main__":
    main()
