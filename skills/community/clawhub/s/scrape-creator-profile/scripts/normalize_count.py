#!/usr/bin/env python3
"""
normalize_count.py — Convert abbreviated count strings to integers.

Usage:
    python3 normalize_count.py "12.3K"
    python3 normalize_count.py "4.5M"
    python3 normalize_count.py "1,234"

Also importable:
    from normalize_count import normalize
    normalize("12.3K")  # → 12300
"""

import re
import sys


def normalize(value: str) -> int | None:
    """
    Convert a human-readable count string to an integer.
    Returns None if the string cannot be parsed.
    """
    if value is None:
        return None

    s = str(value).strip().replace(",", "").replace(" ", "").upper()

    # Strip trailing non-numeric characters like "FOLLOWERS", "SUBSCRIBERS", etc.
    s = re.split(r"[^0-9KMB.]", s)[0]

    if not s:
        return None

    multipliers = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}

    for suffix, mult in multipliers.items():
        if s.endswith(suffix):
            try:
                return int(float(s[:-1]) * mult)
            except ValueError:
                return None

    try:
        return int(float(s))
    except ValueError:
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: normalize_count.py <count_string>", file=sys.stderr)
        sys.exit(1)

    result = normalize(sys.argv[1])
    if result is None:
        print(f"Could not parse: {sys.argv[1]!r}", file=sys.stderr)
        sys.exit(1)

    print(result)
