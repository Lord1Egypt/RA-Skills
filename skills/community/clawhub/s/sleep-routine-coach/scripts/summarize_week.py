#!/usr/bin/env python3
"""Create a descriptive, non-causal weekly sleep habit summary."""

from __future__ import annotations

import argparse
import statistics
from datetime import date, timedelta
from pathlib import Path

from sleep_core import default_data_dir, load_records, parse_timestamp, print_json, recalculate_record


def circular_distance_minutes(values: list[int]) -> int | None:
    if len(values) < 2:
        return None
    anchor = values[0]
    adjusted = [anchor + ((value - anchor + 720) % 1440 - 720) for value in values]
    return round(max(adjusted) - min(adjusted))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=default_data_dir())
    parser.add_argument("--end-date", default=date.today().isoformat())
    args = parser.parse_args()
    end = date.fromisoformat(args.end_date)
    start = end - timedelta(days=6)
    records = [
        recalculate_record(dict(record))
        for record in load_records(args.data_dir)
        if start <= date.fromisoformat(record["date"]) <= end
    ]
    bed_minutes = [
        parse_timestamp(record["goodnight_at"]).hour * 60 + parse_timestamp(record["goodnight_at"]).minute
        for record in records
        if record.get("goodnight_at")
    ]
    wake_minutes = [
        parse_timestamp(record["morning_at"]).hour * 60 + parse_timestamp(record["morning_at"]).minute
        for record in records
        if record.get("morning_at")
    ]
    durations = [
        record["estimated_sleep_duration_minutes"]
        for record in records
        if record.get("estimated_sleep_duration_minutes") is not None
    ]
    rested = [record["rested_score"] for record in records if record.get("rested_score") is not None]
    summary = {
        "period": {"start": start.isoformat(), "end": end.isoformat()},
        "recorded_nights": len(records),
        "goodnight_time_range_minutes": circular_distance_minutes(bed_minutes),
        "morning_time_range_minutes": circular_distance_minutes(wake_minutes),
        "median_estimated_sleep_duration_minutes": round(statistics.median(durations)) if durations else None,
        "average_rested_score": round(statistics.mean(rested), 1) if rested else None,
        "data_completeness": {
            "goodnight": len(bed_minutes),
            "morning": len(wake_minutes),
            "estimated_duration": len(durations),
            "rested_score": len(rested),
        },
        "interpretation": (
            "These are descriptive patterns from self-reported data. They do not establish causes or provide a diagnosis."
        ),
    }
    print_json(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
