#!/usr/bin/env python3
"""Resolve an address on nbn's public places API and report the premises technology."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

AUTOCOMPLETE_URL = "https://places.nbnco.net.au/places/v1/autocomplete"
DETAILS_URL = "https://places.nbnco.net.au/places/v2/details/{loc_id}"
CHECK_ADDRESS_URL = "https://www.nbnco.com.au/check-address"
SOURCE = "website_aem_no_tracking_id"

UNIT_PREFIX_RE = re.compile(
    r"^(APT\b|APARTMENT\b|FLAT\b|KSK\b|L \d+\b|LEVEL\b|LOT\b|LVL\b|SHOP\b|STE\b|SUITE\b|TNCY\b|UNIT\b)"
)
UNIT_QUERY_RE = re.compile(
    r"\b(APT|APARTMENT|FLAT|LEVEL|LOT|LVL|SHOP|STE|SUITE|TENANCY|TNCY|UNIT)\b"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Look up nbn premises technology for an Australian address."
    )
    parser.add_argument("--address", required=True, help="Full street address")
    parser.add_argument(
        "--timeout-seconds", type=int, default=30, help="HTTP timeout in seconds"
    )
    return parser.parse_args()


def build_headers(include_transaction_id: bool) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Origin": "https://www.nbnco.com.au",
        "Referer": CHECK_ADDRESS_URL,
        "User-Agent": "Codex qld-property-research skill",
    }
    if include_transaction_id:
        headers["transactionid"] = str(random.randint(10**14, 10**15 - 1))
    return headers


def fetch_json(url: str, timeout_seconds: int, include_transaction_id: bool) -> dict:
    req = urllib.request.Request(
        url, headers=build_headers(include_transaction_id), method="GET"
    )
    with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
        return json.load(resp)


def normalize(text: str) -> str:
    return re.sub(r"[^A-Z0-9]+", " ", text.upper()).strip()


def suggestion_score(query: str, suggestion: dict) -> int:
    query_norm = normalize(query)
    formatted = suggestion.get("formattedAddress") or ""
    formatted_norm = normalize(formatted)

    score = 0
    if formatted_norm == query_norm:
        score += 100
    elif formatted_norm.startswith(query_norm):
        score += 50
    elif query_norm.startswith(formatted_norm):
        score += 35

    query_has_unit = bool(UNIT_QUERY_RE.search(query.upper()))
    suggestion_is_unit = bool(UNIT_PREFIX_RE.match(formatted.upper()))

    if query_has_unit == suggestion_is_unit:
        score += 15
    elif not query_has_unit and not suggestion_is_unit:
        score += 25
    else:
        score -= 10

    return score


def autocomplete(address: str, timeout_seconds: int) -> dict:
    params = {
        "query": address,
        "timestamp": int(time.time() * 1000),
    }
    url = AUTOCOMPLETE_URL + "?" + urllib.parse.urlencode(params)
    return fetch_json(url, timeout_seconds, include_transaction_id=True)


def pick_suggestion(address: str, suggestions: list[dict]) -> dict | None:
    if not suggestions:
        return None

    ranked = sorted(
        (
            (suggestion_score(address, suggestion), index, suggestion)
            for index, suggestion in enumerate(suggestions)
        ),
        key=lambda item: (-item[0], item[1]),
    )
    best_score, _, best = ranked[0]
    best = dict(best)
    best["selectionScore"] = best_score
    return best


def get_details(loc_id: str, timeout_seconds: int) -> dict:
    url = DETAILS_URL.format(loc_id=urllib.parse.quote(loc_id, safe="")) + "?" + urllib.parse.urlencode(
        {"source": SOURCE}
    )
    return fetch_json(url, timeout_seconds, include_transaction_id=False)


def summarize(query: str, selected: dict, details: dict) -> dict:
    address_detail = details.get("addressDetail") or {}
    serving_area = details.get("servingArea") or {}

    premises_technology = address_detail.get("techType")
    serving_area_technology = serving_area.get("techType")

    if premises_technology and serving_area_technology and premises_technology != serving_area_technology:
        interpretation = (
            f"Official nbn premises technology is {premises_technology}. "
            f"The broader serving-area technology is {serving_area_technology}, "
            "so use the premises technology as the property-specific result."
        )
    elif premises_technology:
        interpretation = (
            f"Official nbn premises technology is {premises_technology}."
        )
    else:
        interpretation = "nbn did not return a premises technology for this address."

    return {
        "status": "ok",
        "query": query,
        "selected_match": {
            "id": selected.get("id"),
            "formatted_address": selected.get("formattedAddress"),
            "latitude": selected.get("latitude"),
            "longitude": selected.get("longitude"),
            "selection_score": selected.get("selectionScore"),
        },
        "nbn": {
            "premises_technology": premises_technology,
            "serving_area_technology": serving_area_technology,
            "service_type": address_detail.get("serviceType") or serving_area.get("serviceType"),
            "service_status": address_detail.get("serviceStatus") or serving_area.get("serviceStatus"),
            "reason_code": address_detail.get("reasonCode"),
            "alt_reason_code": address_detail.get("altReasonCode"),
            "mdu_fibre_eligibility": address_detail.get("mduFibreEligibility"),
            "speed_tier_availability": address_detail.get("speedTierAvailability"),
            "zero_build_cost": address_detail.get("zeroBuildCost"),
            "tech_change_status": address_detail.get("techChangeStatus"),
            "program_type": address_detail.get("programType"),
            "target_eligibility_quarter": address_detail.get("targetEligibilityQuarter"),
        },
        "interpretation": interpretation,
        "sources": {
            "check_address_page": CHECK_ADDRESS_URL,
            "autocomplete_endpoint": AUTOCOMPLETE_URL,
            "details_endpoint": DETAILS_URL.format(loc_id=selected.get("id")),
        },
    }


def main() -> int:
    args = parse_args()
    try:
        lookup = autocomplete(args.address, args.timeout_seconds)
        suggestions = lookup.get("suggestions") or []
        selected = pick_suggestion(args.address, suggestions)
        if not selected:
            print(
                json.dumps(
                    {
                        "status": "not_found",
                        "query": args.address,
                        "message": "No official nbn address suggestions matched the supplied address.",
                        "sources": {
                            "check_address_page": CHECK_ADDRESS_URL,
                            "autocomplete_endpoint": AUTOCOMPLETE_URL,
                        },
                    },
                    indent=2,
                )
            )
            return 0

        details = get_details(selected["id"], args.timeout_seconds)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(
            json.dumps(
                {
                    "error": "nbn_http_error",
                    "status": exc.code,
                    "body": body,
                },
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1
    except urllib.error.URLError as exc:
        print(
            json.dumps(
                {"error": "nbn_connection_error", "reason": str(exc)},
                indent=2,
            ),
            file=sys.stderr,
        )
        return 1

    print(json.dumps(summarize(args.address, selected, details), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
