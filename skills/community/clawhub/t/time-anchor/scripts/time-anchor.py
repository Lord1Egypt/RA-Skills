#!/usr/bin/env python3
"""Time anchor - deterministic date math for any target date."""

import argparse
import json
from datetime import date, datetime, timedelta


TARGETS = {
    "2026-05-31": "End of May",
    "2026-06-01": "Plaster painting window",
    "2026-06-15": "SpaceX IPO listing",
    "2026-08-01": "Sasol Q2 results",
    # Add named events as they come up: "YYYY-MM-DD": "Event name"
}

DAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
DAY_MAP = {name: idx for idx, name in enumerate(DAY_NAMES)}


def parse_iso_date(date_str):
    """Parse YYYY-MM-DD into a date object."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError(
            f"Invalid date format '{date_str}'. Expected YYYY-MM-DD."
        ) from exc


def today_date():
    """Return today's local date."""
    return date.today()


def format_date(value):
    """Format a date object as YYYY-MM-DD."""
    return value.isoformat()


def days_between(from_date, to_date):
    """Calculate day and week deltas between two date objects."""
    delta = (to_date - from_date).days
    weeks = round(delta / 7, 1) if delta >= 0 else -(round(abs(delta) / 7, 1))
    return delta, weeks


def month_end(current_date):
    """Return the last date of the current month."""
    if current_date.month == 12:
        next_month = date(current_date.year + 1, 1, 1)
    else:
        next_month = date(current_date.year, current_date.month + 1, 1)
    return next_month - timedelta(days=1)


def week_labels(delta):
    """Return human and JSON labels for a weekday delta."""
    return ("this", "this_week") if delta <= 7 else ("next", "next_week")


def resolve_weekday(name):
    """Resolve a weekday name to canonical capitalization and index."""
    day_lower = name.strip().lower()

    exact = [day for day in DAY_MAP if day.lower() == day_lower]
    if len(exact) == 1:
        return exact[0], DAY_MAP[exact[0]]

    if len(day_lower) >= 3:
        fuzzy = [day for day in DAY_MAP if day.lower().startswith(day_lower)]
        if len(fuzzy) == 1:
            return fuzzy[0], DAY_MAP[fuzzy[0]]
        if len(fuzzy) > 1:
            raise ValueError(
                f'Ambiguous weekday prefix "{name}". Matches: {", ".join(sorted(fuzzy))}'
            )

    raise ValueError(
        f'Unknown weekday "{name}". Options: {", ".join(DAY_MAP.keys())}'
    )


def get_weekday_targets(name, anchor_date=None):
    """Return upcoming weekday occurrences and ambiguity metadata.

    Label semantics: deltas from 0 to 7 days inclusive are treated as "this"
    / "this_week"; 8+ days becomes "next" / "next_week".
    """
    anchor_date = anchor_date or today_date()
    day_name, target_day_idx = resolve_weekday(name)

    options = []
    for offset in range(22):
        candidate = anchor_date + timedelta(days=offset)
        if candidate.weekday() != target_day_idx:
            continue

        delta, weeks = days_between(anchor_date, candidate)
        human_label, json_label = week_labels(delta)
        options.append(
            {
                "date": format_date(candidate),
                "label": json_label,
                "human_label": f"{human_label} {day_name}",
                "days_until": delta,
                "weeks_until": weeks,
                "is_today": delta == 0,
            }
        )
        if len(options) >= 2:
            break

    return {
        "weekday": day_name,
        "ambiguous": len(options) >= 2,
        "options": options,
    }


def render_weekday_targets(result):
    """Render weekday target results as text plus trailing JSON."""
    lines = [f'Upcoming {result["weekday"]}s:']
    for option in result["options"]:
        marker = " <- TODAY" if option["is_today"] else ""
        lines.append(
            f'  {option["human_label"]} ({option["date"]}) -> '
            f'{option["days_until"]:+d} days / {option["weeks_until"]:.1f} weeks{marker}'
        )

    json_payload = {
        "ambiguous": result["ambiguous"],
        "options": [
            {
                "date": option["date"],
                "label": option["label"],
                "days_until": option["days_until"],
            }
            for option in result["options"]
        ],
    }
    lines.append(json.dumps(json_payload))
    return "\n".join(lines)


def get_full_anchor(anchor_date=None):
    """Return today's date, configured targets, and month info."""
    anchor_date = anchor_date or today_date()
    targets = []
    for target_str, label in TARGETS.items():
        target_date = parse_iso_date(target_str)
        delta, weeks = days_between(anchor_date, target_date)
        targets.append(
            {
                "label": label,
                "date": target_str,
                "days_until": delta,
                "weeks_until": weeks,
                "direction": "in" if delta >= 0 else "",
            }
        )

    end_of_month = month_end(anchor_date)
    return {
        "today": format_date(anchor_date),
        "weekday": anchor_date.strftime("%A"),
        "targets": targets,
        "month_info": {
            "current_month": anchor_date.strftime("%B %Y"),
            "days_remaining_excluding_today": (end_of_month - anchor_date).days,
        },
    }


def render_full_anchor(result):
    """Render full anchor results as text."""
    lines = [f'Today: {result["today"]} ({result["weekday"]})', ""]
    for target in result["targets"]:
        lines.append(
            f'{target["label"]:35s} ({target["date"]}) -> '
            f'{target["days_until"]:+d} days / {target["weeks_until"]} weeks {target["direction"]}'
        )

    lines.extend(
        [
            "",
            f'{result["month_info"]["current_month"]}: '
            f'{result["month_info"]["days_remaining_excluding_today"]} '
            'days remaining (excluding today)',
        ]
    )
    return "\n".join(lines)


def render_single_target(target_date, anchor_date=None):
    """Render a single arbitrary target date lookup."""
    anchor_date = anchor_date or today_date()
    delta, weeks = days_between(anchor_date, target_date)
    direction = "in" if delta >= 0 else ""
    return "\n".join(
        [
            f"Target: {format_date(target_date)}",
            f"From:   {format_date(anchor_date)} ({anchor_date.strftime('%A')})",
            f"Days:   {delta:+d} days / {weeks} weeks {direction}",
        ]
    )


def render_month(anchor_date=None):
    """Render current month remaining days."""
    anchor_date = anchor_date or today_date()
    return (
        f"{anchor_date.strftime('%B')} {anchor_date.year}: "
        f"{(month_end(anchor_date) - anchor_date).days} days remaining (excluding today)"
    )


def parse_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Deterministic date math for arbitrary dates and weekdays."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--today", action="store_true", help="Show today's date and weekday")
    group.add_argument("--until", metavar="DATE", help="Show distance to YYYY-MM-DD")
    group.add_argument("--weekday", metavar="DAY", help="Show next upcoming weekday occurrences")
    group.add_argument("--month", action="store_true", help="Show days remaining in current month")
    return parser.parse_args()


def main():
    """CLI entrypoint."""
    args = parse_args()
    anchor_date = today_date()

    if args.today:
        print(f"{format_date(anchor_date)} ({anchor_date.strftime('%A')})")
        return

    if args.until:
        print(render_single_target(parse_iso_date(args.until), anchor_date))
        return

    if args.weekday:
        print(render_weekday_targets(get_weekday_targets(args.weekday, anchor_date)))
        return

    if args.month:
        print(render_month(anchor_date))
        return

    print(render_full_anchor(get_full_anchor(anchor_date)))


if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        raise SystemExit(f"Error: {exc}")
