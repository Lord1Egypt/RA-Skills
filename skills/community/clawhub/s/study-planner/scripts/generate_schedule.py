#!/usr/bin/env python3
"""Generate a study schedule based on subjects, available hours, and deadline."""

import json
import sys
from datetime import datetime, timedelta


def generate_schedule(subjects: list, daily_hours: float, deadline: str, start_date: str = None):
    """
    Generate a balanced study schedule.

    Args:
        subjects: list of dicts with 'name', 'priority' (1-5), 'difficulty' (1-5)
        daily_hours: available study hours per day
        deadline: target deadline (YYYY-MM-DD)
        start_date: start date (YYYY-MM-DD), defaults to today
    """
    start = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.now()
    end = datetime.strptime(deadline, "%Y-%m-%d")
    total_days = (end - start).days

    if total_days <= 0:
        print("Error: deadline must be in the future")
        sys.exit(1)

    # Calculate weight for each subject: priority * difficulty
    total_weight = sum(s["priority"] * s["difficulty"] for s in subjects)

    schedule = []
    for subj in subjects:
        weight = subj["priority"] * subj["difficulty"]
        proportion = weight / total_weight
        total_hours = proportion * daily_hours * total_days

        # Phase allocation: 30% foundation, 40% deep, 20% apply, 10% review
        phases = {
            "基础入门": round(total_hours * 0.30, 1),
            "深入理解": round(total_hours * 0.40, 1),
            "综合应用": round(total_hours * 0.20, 1),
            "查漏补缺": round(total_hours * 0.10, 1),
        }

        schedule.append({
            "subject": subj["name"],
            "total_hours": round(total_hours, 1),
            "daily_hours": round(proportion * daily_hours, 2),
            "phases": phases,
        })

    result = {
        "start_date": start.strftime("%Y-%m-%d"),
        "deadline": deadline,
        "total_days": total_days,
        "daily_hours": daily_hours,
        "subjects": schedule,
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: generate_schedule.py '<json_config>'")
        print('Example: generate_schedule.py \'{"subjects":[{"name":"Python","priority":4,"difficulty":3},{"name":"SQL","priority":3,"difficulty":2}],"daily_hours":3,"deadline":"2026-08-01"}\'')
        sys.exit(1)

    config = json.loads(sys.argv[1])
    result = generate_schedule(
        subjects=config["subjects"],
        daily_hours=config["daily_hours"],
        deadline=config["deadline"],
        start_date=config.get("start_date"),
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
