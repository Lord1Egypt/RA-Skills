#!/usr/bin/env python3
"""Resolve a user's reply against a numbered candidate address list."""

from __future__ import annotations

import argparse
import json
import re
from typing import List


NO_MATCH_PHRASES = {
    "none",
    "none of these",
    "none of them",
    "neither",
    "no match",
    "not listed",
    "not right",
    "not correct",
    "wrong address",
    "different address",
}

ORDINAL_WORDS = {
    "first": 1,
    "second": 2,
    "third": 3,
    "fourth": 4,
    "fifth": 5,
}


def normalize(value: str) -> str:
    lowered = value.strip().lower()
    return re.sub(r"[^a-z0-9]+", " ", lowered).strip()


def parse_index(selection: str, count: int) -> int | None:
    stripped = selection.strip()

    if re.fullmatch(r"\d+", stripped):
        index = int(stripped)
        if 1 <= index <= count:
            return index

    number_match = re.search(r"(?:option|candidate|address|number|#)\s*(\d+)", stripped, re.I)
    if number_match:
        index = int(number_match.group(1))
        if 1 <= index <= count:
            return index

    normalized_selection = normalize(selection)
    for word, index in ORDINAL_WORDS.items():
        if re.search(rf"\b{word}\b", normalized_selection) and index <= count:
            return index

    return None


def find_address_match(selection: str, candidates: List[str]) -> int | None:
    normalized_selection = normalize(selection)
    normalized_candidates = [normalize(candidate) for candidate in candidates]

    exact_matches = [
        index for index, candidate in enumerate(normalized_candidates, start=1)
        if candidate == normalized_selection
    ]
    if len(exact_matches) == 1:
        return exact_matches[0]

    contains_matches = [
        index for index, candidate in enumerate(normalized_candidates, start=1)
        if normalized_selection and normalized_selection in candidate
    ]
    if len(contains_matches) == 1:
        return contains_matches[0]

    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resolve a user's reply against candidate Texas service addresses.",
    )
    parser.add_argument("--selection", required=True, help="The user's follow-up reply.")
    parser.add_argument(
        "--candidate",
        action="append",
        default=[],
        help="A candidate address. Repeat for each option in display order.",
    )
    args = parser.parse_args()

    selection = args.selection.strip()
    candidates = [candidate.strip() for candidate in args.candidate if candidate.strip()]
    normalized_selection = normalize(selection)

    if normalized_selection in NO_MATCH_PHRASES:
        result = {
            "status": "no_match",
            "selected_index": None,
            "selected_address": None,
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return

    selected_index = parse_index(selection, len(candidates))
    if selected_index is None:
        selected_index = find_address_match(selection, candidates)

    if selected_index is not None:
        result = {
            "status": "selected",
            "selected_index": selected_index,
            "selected_address": candidates[selected_index - 1],
        }
    else:
        result = {
            "status": "unclear",
            "selected_index": None,
            "selected_address": None,
        }

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
