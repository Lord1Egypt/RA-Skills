#!/usr/bin/env python3
"""Compute rolling pre-kickoff reminder times for football forecasts."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ALERT_LABELS = {
    190: "T-3h10",
    130: "T-2h10",
    70: "T-1h10",
    10: "T-10min",
}


def parse_iso(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError("kickoff must include an explicit timezone offset or Z")
    return dt


def normalize_matches(data: object) -> list[dict[str, object]]:
    if isinstance(data, dict) and "matches" in data:
        matches = data["matches"]
    elif isinstance(data, dict):
        matches = [data]
    else:
        matches = data
    if not isinstance(matches, list) or not matches:
        raise ValueError("input must be one match, a non-empty match list, or {matches: [...]}")
    if not all(isinstance(item, dict) for item in matches):
        raise ValueError("every match must be an object")
    return matches


def alert_label(minutes_before: int) -> str:
    return ALERT_LABELS.get(minutes_before, f"T-{minutes_before}min")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        required=True,
        help="JSON file containing one match, a match list, or {matches: [...]}",
    )
    parser.add_argument("--timezone", default="Asia/Hong_Kong", help="Output timezone.")
    parser.add_argument(
        "--minutes-before",
        type=int,
        nargs="+",
        default=[10],
        help="One or more positive minute offsets before kickoff.",
    )
    args = parser.parse_args()

    if any(minutes <= 0 for minutes in args.minutes_before):
        parser.error("--minutes-before values must be positive integers")
    if len(set(args.minutes_before)) != len(args.minutes_before):
        parser.error("--minutes-before values must be unique")

    try:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        matches = normalize_matches(data)
        tz = ZoneInfo(args.timezone)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError, ZoneInfoNotFoundError) as exc:
        parser.error(str(exc))

    scheduled_alerts: list[tuple[datetime, dict[str, str]]] = []
    for item in matches:
        try:
            kickoff_value = item.get("kickoff")
            if not isinstance(kickoff_value, str) or not kickoff_value.strip():
                raise ValueError("every match requires an ISO kickoff string")
            kickoff = parse_iso(kickoff_value).astimezone(tz)
            teams = item.get("teams")
            fallback_name = " vs ".join(str(team) for team in teams) if isinstance(teams, list) else ""
            match_name = str(item.get("match") or fallback_name).strip()
            if not match_name:
                raise ValueError("every match requires match text or a teams list")
        except (TypeError, ValueError) as exc:
            parser.error(str(exc))

        for minutes_before in args.minutes_before:
            label = alert_label(minutes_before)
            alert_at_utc = kickoff.astimezone(timezone.utc) - timedelta(minutes=minutes_before)
            alert_at = alert_at_utc.astimezone(tz)
            scheduled_alerts.append(
                (
                    alert_at_utc,
                    {
                        "match": match_name,
                        "kickoff": kickoff.isoformat(timespec="minutes"),
                        "alert_at": alert_at.isoformat(timespec="minutes"),
                        "label": label,
                        "prompt": (
                            "Use $world-cup-2026-predictor to refresh current multi-book odds, "
                            f"lineup/news, line movement, and prior analysis for {match_name}; "
                            f"produce the rolling {label} pre-kickoff forecast in the user's language."
                        ),
                    },
                )
            )

    scheduled_alerts.sort(key=lambda item: (item[0], item[1]["match"], item[1]["label"]))
    alerts = [alert for _, alert in scheduled_alerts]
    print(json.dumps({"alerts": alerts}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
