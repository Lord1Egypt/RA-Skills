#!/usr/bin/env python3
"""Calculate total duration for one or more transcript time ranges.

Examples:
  python scripts/calc_duration.py 00:00-01:42
  python scripts/calc_duration.py 03:50-05:17 07:51-10:00
  python scripts/calc_duration.py 00:03:50-00:05:17 00:07:51-00:10:00
"""

from __future__ import annotations

import argparse
import math
import re


def parse_time(value: str) -> int:
    parts = [int(p) for p in value.split(":")]
    if len(parts) == 2:
        minutes, seconds = parts
        return minutes * 60 + seconds
    if len(parts) == 3:
        hours, minutes, seconds = parts
        return hours * 3600 + minutes * 60 + seconds
    raise argparse.ArgumentTypeError(f"bad time: {value}")


def parse_range(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"\s*([0-9:]+)\s*-\s*([0-9:]+)\s*", value)
    if not match:
        raise argparse.ArgumentTypeError(f"bad range: {value}")
    start = parse_time(match.group(1))
    end = parse_time(match.group(2))
    if end < start:
        raise argparse.ArgumentTypeError(f"range ends before it starts: {value}")
    return start, end


def human(seconds: int, approx: bool = True) -> str:
    if seconds < 30:
        return f"{seconds} sec"
    minutes = max(1, math.floor(seconds / 60 + 0.5))
    prefix = "~" if approx and seconds % 60 else ""
    if minutes < 60:
        return f"{prefix}{minutes} min"
    hours = minutes // 60
    rem = minutes % 60
    if rem:
        return f"{prefix}{hours} hr {rem} min"
    return f"{hours} hr"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ranges", nargs="+", help="time ranges like 00:00-01:42")
    parser.add_argument("--exact", action="store_true", help="also print exact seconds")
    args = parser.parse_args()

    range_items: list[str] = []
    for raw in args.ranges:
        range_items.extend(x for x in re.split(r"[,\s]+", raw) if x)

    total = 0
    for item in range_items:
        start, end = parse_range(item)
        total += end - start

    print(human(total, approx=True))
    if args.exact:
        print(f"{total} sec")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
