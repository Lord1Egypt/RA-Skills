#!/usr/bin/env python3
"""Look up and normalize candidate Texas service addresses."""

from __future__ import annotations

import argparse
import json
from typing import Any, Dict, Iterable, List

from normalize_address_query import normalize_raw_address_query
from powerlego_api import address_validator


def clean(value: Any) -> str:
    return str(value or "").strip()


def first_non_empty(values: Iterable[Any]) -> str:
    for value in values:
        text = clean(value)
        if text:
            return text
    return ""


def coerce_candidate_items(payload: Any) -> List[Any]:
    if isinstance(payload, list):
        return payload

    if not isinstance(payload, dict):
        return []

    direct_list_keys = (
        "candidates",
        "addresses",
        "results",
        "data",
        "items",
        "response",
    )
    for key in direct_list_keys:
        value = payload.get(key)
        if isinstance(value, list):
            return value

    nested_dict_keys = ("response", "data", "result")
    for key in nested_dict_keys:
        value = payload.get(key)
        if isinstance(value, dict):
            nested_items = coerce_candidate_items(value)
            if nested_items:
                return nested_items

    return []


def normalize_candidate(item: Any) -> Dict[str, str]:
    if isinstance(item, str):
        normalized = normalize_raw_address_query(item).get("normalized", {})
        street = clean(normalized.get("street"))
        city = clean(normalized.get("city"))
        state = clean(normalized.get("state")) or "TX"
        zipcode = clean(normalized.get("zipcode"))
        label = ", ".join(part for part in (street, city, state, zipcode) if part)
        return {
            "label": label or clean(item),
            "street": street,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "esiid": "",
        }

    if not isinstance(item, dict):
        return {
            "label": "",
            "street": "",
            "city": "",
            "state": "TX",
            "zipcode": "",
            "esiid": "",
        }

    street = first_non_empty(
        (
            item.get("street"),
            item.get("address1"),
            item.get("address"),
            item.get("service_address"),
        )
    )
    city = first_non_empty((item.get("city"), item.get("service_city")))
    state = first_non_empty((item.get("state"), item.get("service_state"), "TX")) or "TX"
    zipcode = first_non_empty((item.get("zipcode"), item.get("zip"), item.get("postal_code")))
    esiid = first_non_empty((item.get("esiid"), item.get("esi_id")))

    label = first_non_empty(
        (
            item.get("label"),
            item.get("formatted_address"),
            item.get("full_address"),
            item.get("display_address"),
        )
    )
    if not label:
        label = ", ".join(part for part in (street, city, state, zipcode) if part)

    return {
        "label": label,
        "street": street,
        "city": city,
        "state": state,
        "zipcode": zipcode,
        "esiid": esiid,
    }


def dedupe_candidates(candidates: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    deduped: List[Dict[str, str]] = []

    for candidate in candidates:
        key = (
            candidate["label"].lower(),
            candidate["street"].lower(),
            candidate["city"].lower(),
            candidate["state"].lower(),
            candidate["zipcode"],
        )
        if key in seen:
            continue
        seen.add(key)
        deduped.append(candidate)

    return deduped


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Look up candidate Texas service addresses and return a normalized list.",
    )
    parser.add_argument(
        "--address-query",
        required=True,
        help="Raw address query used for candidate lookup.",
    )
    args = parser.parse_args()

    payload = address_validator(args.address_query)
    candidate_items = coerce_candidate_items(payload)
    normalized_candidates = [
        candidate
        for candidate in (normalize_candidate(item) for item in candidate_items)
        if candidate["label"] or candidate["street"]
    ]
    deduped_candidates = dedupe_candidates(normalized_candidates)

    result = {
        "candidate_count": len(deduped_candidates),
        "candidates": deduped_candidates,
        "query": clean(args.address_query),
        "raw_payload_type": type(payload).__name__,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
