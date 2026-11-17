#!/usr/bin/env python3
"""Generate bounded post-match review wakeups without guessing final results."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from kickoff_alerts import normalize_matches, parse_iso


INITIAL_DELAY_MINUTES = {
    "league_or_group": 135,
    "friendly": 135,
    "single_leg_knockout": 165,
    "two_leg_first": 165,
    "two_leg_second": 165,
}
MAX_RETRIES = 4
RETRY_MINUTES = 15


def can_finalize(status: object) -> bool:
    """Return true only for the result status accepted by the review ledger."""

    return isinstance(status, str) and status.strip().lower() == "final"


def retry_schedule(
    initial: str,
    count: int = MAX_RETRIES,
    *,
    timezone_name: str | None = None,
) -> list[str]:
    """Return bounded retry timestamps on the same absolute timeline."""

    if isinstance(count, bool) or not isinstance(count, int) or not 0 <= count <= MAX_RETRIES:
        raise ValueError(f"retry count must be between 0 and {MAX_RETRIES}")
    start = parse_iso(initial)
    output_timezone = ZoneInfo(timezone_name) if timezone_name else start.tzinfo
    start_utc = start.astimezone(timezone.utc)
    return [
        (start_utc + timedelta(minutes=RETRY_MINUTES * (index + 1)))
        .astimezone(output_timezone)
        .isoformat(timespec="seconds")
        for index in range(count)
    ]


def _match_name(match: dict[str, Any]) -> str:
    teams = match.get("teams")
    fallback = " vs ".join(str(team) for team in teams) if isinstance(teams, list) else ""
    name = str(match.get("match") or fallback).strip()
    if not name:
        raise ValueError("every match requires match text or a teams list")
    return name


def _review_prompt(match_name: str) -> str:
    return (
        "Use $world-cup-2026-predictor to review "
        f"{match_name}. Fetch one official final-result source or two agreeing independent "
        "sources. Keep score_90m, score_after_extra_time, penalties, and qualification "
        "separate. Run scripts/postmatch_review.py against the archived forecast, and answer "
        "in the user's language. If the match is not final, use the bounded retry time; never "
        "finalize postponed, abandoned, or suspended matches."
    )


def build_alert(
    match: dict[str, Any], *, timezone_name: str | None = None
) -> dict[str, Any]:
    """Build the initial post-match wakeup for one scheduled match."""

    if not isinstance(match, dict):
        raise ValueError("match must be an object")
    kickoff_value = match.get("kickoff")
    if not isinstance(kickoff_value, str) or not kickoff_value.strip():
        raise ValueError("every match requires an ISO kickoff string")
    kickoff = parse_iso(kickoff_value)
    output_timezone = ZoneInfo(timezone_name) if timezone_name else kickoff.tzinfo
    kickoff = kickoff.astimezone(output_timezone)

    match_type = match.get("match_type")
    if match_type not in INITIAL_DELAY_MINUTES:
        supported = ", ".join(sorted(INITIAL_DELAY_MINUTES))
        raise ValueError(f"match_type must be one of: {supported}")

    run_at_utc = kickoff.astimezone(timezone.utc) + timedelta(
        minutes=INITIAL_DELAY_MINUTES[match_type]
    )
    run_at = run_at_utc.astimezone(output_timezone)
    name = _match_name(match)
    alert: dict[str, Any] = {
        "match": name,
        "match_type": match_type,
        "kickoff": kickoff.isoformat(timespec="seconds"),
        "run_at": run_at.isoformat(timespec="seconds"),
        "prompt": _review_prompt(name),
    }
    event_id = match.get("event_id")
    if isinstance(event_id, str) and event_id.strip():
        alert["event_id"] = event_id.strip()
    return alert


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        required=True,
        help="JSON file containing one match, a match list, or {matches: [...]}",
    )
    parser.add_argument("--timezone", default="Asia/Hong_Kong", help="Output timezone.")
    parser.add_argument(
        "--retry-count",
        type=int,
        default=MAX_RETRIES,
        help=f"Number of 15-minute retries after the initial wakeup (0-{MAX_RETRIES}).",
    )
    args = parser.parse_args()

    try:
        if not 0 <= args.retry_count <= MAX_RETRIES:
            raise ValueError(f"retry count must be between 0 and {MAX_RETRIES}")
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))
        matches = normalize_matches(data)
        ZoneInfo(args.timezone)
        alerts = []
        for match in matches:
            alert = build_alert(match, timezone_name=args.timezone)
            alert["retry_at"] = retry_schedule(
                alert["run_at"],
                args.retry_count,
                timezone_name=args.timezone,
            )
            run_at_utc = parse_iso(alert["run_at"]).astimezone(timezone.utc)
            alerts.append((run_at_utc, alert))
        alerts.sort(key=lambda item: (item[0], item[1]["match"]))
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        TypeError,
        ValueError,
        ZoneInfoNotFoundError,
    ) as exc:
        parser.error(str(exc))

    print(
        json.dumps(
            {"alerts": [alert for _, alert in alerts]},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
