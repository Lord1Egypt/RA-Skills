#!/usr/bin/env python3
"""Export an anonymized ride-insights CSV from SQLite."""

import argparse
import csv
import io
import json
import sqlite3
from datetime import datetime


def month_only(value: str | None) -> str:
    if not value:
        return ""
    value = value.strip()
    for fmt in (
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%Y-%m",
    ):
        try:
            return datetime.strptime(value[:16] if fmt == "%Y-%m-%d %H:%M" else value[:19] if fmt == "%Y-%m-%dT%H:%M:%S" else value[:10] if fmt == "%Y-%m-%d" else value[:7], fmt).strftime("%Y-%m")
        except ValueError:
            continue
    if len(value) >= 7 and value[4] == '-':
        return value[:7]
    return value


def round_up_15(value: str | None) -> str:
    if not value:
        return ""
    value = value.strip()

    parsed = None
    for fmt in (
        "%H:%M",
        "%I:%M %p",
        "%B %d, %Y AT %I:%M %p",
        "%b %d, %Y AT %I:%M %p",
    ):
        try:
            parsed = datetime.strptime(value, fmt)
            break
        except ValueError:
            continue

    if parsed is None:
        upper = value.upper()
        marker = " AT "
        if marker in upper:
            tail = value[upper.rfind(marker) + len(marker):].strip()
            for fmt in ("%I:%M %p", "%H:%M"):
                try:
                    parsed = datetime.strptime(tail, fmt)
                    break
                except ValueError:
                    continue

    if parsed is None:
        try:
            hour_str, minute_str = value.split(":", 1)
            hour = int(hour_str)
            minute = int(minute_str)
        except Exception:
            return value
    else:
        hour = parsed.hour
        minute = parsed.minute

    rounded = ((minute + 14) // 15) * 15
    if rounded == 60:
        hour = (hour + 1) % 24
        rounded = 0
    return f"{hour:02d}:{rounded:02d}"


def parse_float(value):
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return value
    text = str(value).strip()
    if not text:
        return ""
    try:
        return float(text)
    except ValueError:
        return ""


def extract_normalized_metrics(extracted_ride_json: str | None):
    if not extracted_ride_json:
        return "", ""
    try:
        payload = json.loads(extracted_ride_json)
    except Exception:
        return "", ""

    distance_km = parse_float(payload.get("distance_km"))
    duration_min = parse_float(payload.get("duration_min"))
    if distance_km != "" or duration_min != "":
        return distance_km, duration_min

    ride = payload.get("ride") or {}
    distance_text = (ride.get("distance_text") or "").strip()
    duration_text = (ride.get("duration_text") or "").strip()

    distance_match = None
    duration_match = None
    try:
        import re
        distance_match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*km\b", distance_text, re.IGNORECASE)
        duration_match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*min\b", duration_text, re.IGNORECASE)
    except Exception:
        pass

    distance_km = parse_float(distance_match.group(1)) if distance_match else ""
    duration_min = parse_float(duration_match.group(1)) if duration_match else ""
    return distance_km, duration_min


def main() -> int:
    parser = argparse.ArgumentParser(description="Export an anonymized ride-insights CSV from SQLite")
    parser.add_argument("--db", required=True, help="Path to the ride-insights SQLite database")
    parser.add_argument("--out", help="Write CSV to this path instead of stdout")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        """
        SELECT
          provider,
          email_date_text,
          start_time_text,
          end_time_text,
          currency,
          amount,
          pickup_city,
          pickup_country,
          dropoff_city,
          dropoff_country,
          extracted_ride_json
        FROM rides
        ORDER BY email_date_text, id
        """
    ).fetchall()

    fieldnames = [
        "provider",
        "email_month",
        "start_time_15m",
        "end_time_15m",
        "currency",
        "amount",
        "distance_km",
        "duration_min",
        "pickup_city",
        "pickup_country",
        "dropoff_city",
        "dropoff_country",
    ]

    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        distance_km, duration_min = extract_normalized_metrics(row["extracted_ride_json"])
        writer.writerow(
            {
                "provider": row["provider"] or "",
                "email_month": month_only(row["email_date_text"]),
                "start_time_15m": round_up_15(row["start_time_text"]),
                "end_time_15m": round_up_15(row["end_time_text"]),
                "currency": row["currency"] or "",
                "amount": row["amount"] if row["amount"] is not None else "",
                "distance_km": distance_km,
                "duration_min": duration_min,
                "pickup_city": row["pickup_city"] or "",
                "pickup_country": row["pickup_country"] or "",
                "dropoff_city": row["dropoff_city"] or "",
                "dropoff_country": row["dropoff_country"] or "",
            }
        )

    csv_text = buffer.getvalue()
    if args.out:
        from pathlib import Path
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(csv_text, encoding="utf-8", newline="")
        print(str(out_path))
    else:
        print(csv_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
