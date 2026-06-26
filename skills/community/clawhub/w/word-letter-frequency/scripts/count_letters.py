#!/usr/bin/env python3
"""Utility to count how many times each letter appears in a word or short phrase."""

from __future__ import annotations

import argparse
import json
from collections import Counter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "text",
        help="Word or short phrase to analyze. Wrap in quotes if it contains spaces.",
    )
    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Treat uppercase and lowercase letters as different characters (default: case-insensitive).",
    )
    parser.add_argument(
        "--include-non-alpha",
        action="store_true",
        help="Include non-alphabetic characters in the count (default: ignore them).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the counts as compact JSON instead of plain text.",
    )
    return parser.parse_args()


def count_letters(text: str, case_sensitive: bool = False, include_non_alpha: bool = False) -> Counter:
    processed = text if case_sensitive else text.lower()
    if not include_non_alpha:
        processed = "".join(ch for ch in processed if ch.isalpha())
    return Counter(processed)


def format_counts(counter: Counter[str]) -> str:
    if not counter:
        return "(no characters were counted)"
    width = max(len(char) for char in counter)
    lines = ["Character  Count", "---------  -----"]
    for char in sorted(counter):
        lines.append(f"{char.ljust(width)}  {counter[char]}")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    counter = count_letters(args.text, args.case_sensitive, args.include_non_alpha)
    if args.json:
        print(json.dumps(counter, ensure_ascii=False))
    else:
        print(format_counts(counter))


if __name__ == "__main__":
    main()
