#!/usr/bin/env python3
"""Validate a research packet against evidence-first, no-trade contracts."""

from __future__ import annotations

import argparse
from datetime import date, datetime
import json
from pathlib import Path
import sys
from typing import Any
from urllib.parse import urlparse


REQUIRED_TOP_LEVEL = {
    "question",
    "scope",
    "as_of",
    "sources",
    "valuation",
    "risks",
    "recommendation",
    "disclaimer",
}
REQUIRED_RECOMMENDATION = {"stance", "confidence", "trigger", "invalidation"}
FORBIDDEN_EXECUTION_KEYS = {
    "account_id",
    "amount",
    "api_key",
    "broker_payload",
    "credentials",
    "limit_price",
    "order_type",
    "quantity",
    "token",
}


def _is_nonempty(value: Any) -> bool:
    return value not in (None, "", [], {})


def _parse_iso(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        try:
            date.fromisoformat(value)
            return True
        except ValueError:
            return False


def _find_forbidden_keys(value: Any, prefix: str = "") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if str(key).lower() in FORBIDDEN_EXECUTION_KEYS:
                findings.append(path)
            findings.extend(_find_forbidden_keys(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            findings.extend(_find_forbidden_keys(child, f"{prefix}[{index}]"))
    return findings


def validate(packet: Any) -> list[str]:
    """Return deterministic validation errors for a decoded JSON packet."""
    if not isinstance(packet, dict):
        return ["packet must be a JSON object"]

    errors: list[str] = []
    for key in sorted(REQUIRED_TOP_LEVEL):
        if key not in packet or not _is_nonempty(packet[key]):
            errors.append(f"missing or empty required field: {key}")

    forbidden = _find_forbidden_keys(packet)
    errors.extend(f"forbidden execution field: {path}" for path in forbidden)

    as_of = packet.get("as_of")
    if isinstance(as_of, str) and not _parse_iso(as_of):
        errors.append("as_of must be an ISO-8601 date or datetime")

    sources = packet.get("sources")
    if isinstance(sources, list):
        if not sources:
            errors.append("sources must contain at least one dated source")
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                errors.append(f"sources[{index}] must be an object")
                continue
            for field in ("publisher", "url", "published_at", "fetched_at"):
                if not _is_nonempty(source.get(field)):
                    errors.append(f"sources[{index}] missing {field}")
            url = source.get("url")
            if isinstance(url, str) and urlparse(url).scheme not in {"http", "https"}:
                errors.append(f"sources[{index}].url must use http or https")
            for field in ("published_at", "fetched_at"):
                value = source.get(field)
                if isinstance(value, str) and not _parse_iso(value):
                    errors.append(f"sources[{index}].{field} must be ISO-8601")
    elif sources is not None:
        errors.append("sources must be a list")

    valuation = packet.get("valuation")
    if isinstance(valuation, dict):
        for field in ("methods", "assumptions", "range"):
            if not _is_nonempty(valuation.get(field)):
                errors.append(f"valuation missing {field}")
    elif valuation is not None:
        errors.append("valuation must be an object")

    recommendation = packet.get("recommendation")
    if isinstance(recommendation, dict):
        for field in sorted(REQUIRED_RECOMMENDATION):
            if not _is_nonempty(recommendation.get(field)):
                errors.append(f"recommendation missing {field}")
    elif recommendation is not None:
        errors.append("recommendation must be an object")

    disclaimer = packet.get("disclaimer")
    if isinstance(disclaimer, str):
        normalized = disclaimer.lower()
        if "research" not in normalized or "not personalized investment advice" not in normalized:
            errors.append("disclaimer must state research-only and not personalized investment advice")

    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packet", type=Path, help="Path to a JSON research packet.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        packet = json.loads(args.packet.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors = [f"unable to read packet: {error}"]
    else:
        errors = validate(packet)

    report = {"valid": not errors, "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif errors:
        for error in errors:
            print(f"ERROR: {error}")
    else:
        print("Research packet is valid.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
