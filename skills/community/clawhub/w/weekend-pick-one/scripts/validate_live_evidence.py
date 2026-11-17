#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a fresh live-browser release evidence file.")
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--max-age-hours", type=float, default=72.0)
    return parser.parse_args()


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def parse_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    assert_true(parsed.tzinfo is not None, "generated_at and checked_at must include a timezone")
    return parsed


def main() -> None:
    args = parse_args()
    data = json.loads(args.evidence.read_text(encoding="utf-8"))

    for field in ["generated_at", "city", "timezone", "date_start", "date_end", "verdict", "main_plan", "sources", "public_inspiration_status"]:
        assert_true(field in data, f"missing live evidence field: {field}")

    generated_at = parse_datetime(data["generated_at"])
    age_hours = (datetime.now(timezone.utc) - generated_at.astimezone(timezone.utc)).total_seconds() / 3600
    assert_true(0 <= age_hours <= args.max_age_hours, f"live evidence is stale: {age_hours:.1f} hours old")
    assert_true(data["date_start"] <= data["date_end"], "date range is reversed")
    assert_true(data["main_plan"].strip(), "main_plan must be a named place")
    assert_true(not any(marker in data["main_plan"] for marker in [" 或 ", " / ", "／", "任选", "某个"]), "main_plan is not specific")

    source_types = set()
    for source in data["sources"]:
        for field in ["type", "title", "url", "checked_at", "supports"]:
            assert_true(source.get(field), f"source missing field: {field}")
        parsed_url = urlparse(source["url"])
        assert_true(parsed_url.scheme in {"http", "https"} and parsed_url.netloc, f"invalid source URL: {source['url']}")
        parse_datetime(source["checked_at"])
        source_types.add(source["type"])

    assert_true("weather" in source_types, "live evidence needs a weather source")
    assert_true("official" in source_types, "live evidence needs an official venue source")
    assert_true("transport" in source_types, "live evidence needs a transport source")
    assert_true(data["public_inspiration_status"] in {"checked", "blocked", "skipped", "unavailable"}, "invalid public inspiration status")

    print(json.dumps({
        "suite_type": "live_browser_evidence",
        "passed": True,
        "city": data["city"],
        "date_start": data["date_start"],
        "date_end": data["date_end"],
        "source_count": len(data["sources"]),
        "source_types": sorted(source_types),
        "age_hours": round(age_hours, 2),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
