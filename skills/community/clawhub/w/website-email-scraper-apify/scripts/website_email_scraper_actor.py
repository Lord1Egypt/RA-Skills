#!/usr/bin/env python3
"""Run the Website Email Scraper & Phone Finder Apify actor from an agent-friendly CLI."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_ACTOR_ID = "kWfD7C0WpHtIt8VAh"
DEFAULT_TIMEOUT_SEC = 1800

VALID_RESULT_MODE = {"emailsOnly", "contactsOnly", "allWebsites"}
UNSUPPORTED_FIELDS = {
    "searchStringsArray",
    "locationQuery",
    "placeIds",
    "maxCrawledPlacesPerSearch",
    "contactResultMode",
    "reviewsSort",
    "maxReviews",
}


class SkillError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def resolve_token(explicit: str | None) -> str:
    token = explicit or os.getenv("APIFY_TOKEN", "")
    if not token:
        raise SkillError("Apify token missing. Pass --apify-token or set APIFY_TOKEN.")
    return token


def positive_int(value: Any, field: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise SkillError(f"{field} must be an integer.") from exc
    if number <= 0:
        raise SkillError(f"{field} must be > 0.")
    return number


def bounded_int(value: Any, field: str, minimum: int, maximum: int) -> int:
    number = positive_int(value, field)
    if number < minimum or number > maximum:
        raise SkillError(f"{field} must be between {minimum} and {maximum}.")
    return number


def bool_value(value: Any, field: str) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "1", "yes", "y"}:
            return True
        if lowered in {"false", "0", "no", "n"}:
            return False
    raise SkillError(f"{field} must be a boolean.")


def string_list(values: Any, field: str) -> list[str]:
    if values in (None, ""):
        return []
    if isinstance(values, str):
        return [line.strip() for line in values.splitlines() if line.strip()]
    if isinstance(values, list):
        normalized: list[str] = []
        for value in values:
            if isinstance(value, dict) and isinstance(value.get("url"), str):
                text = value["url"].strip()
            else:
                text = str(value).strip()
            if text:
                normalized.append(text)
        return normalized
    raise SkillError(f"{field} must be a string or array of strings.")


def normalize_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise SkillError("Input payload must be a JSON object.")

    forbidden = sorted(field for field in UNSUPPORTED_FIELDS if field in payload)
    if forbidden:
        raise SkillError(
            "This actor scans submitted website domains and URLs, not Google Maps searches or reviews. "
            f"Remove unsupported field(s): {', '.join(forbidden)}."
        )

    aliases: list[str] = []
    aliases.extend(string_list(payload.get("domains"), "domains"))
    aliases.extend(string_list(payload.get("urls"), "urls"))
    aliases.extend(string_list(payload.get("startUrls"), "startUrls"))
    payload["domains"] = aliases

    if not payload["domains"]:
        raise SkillError("Provide at least one domain or website URL in domains.")

    payload["maxResults"] = positive_int(payload.get("maxResults", 1000), "maxResults")
    payload["maxPagesPerWebsite"] = bounded_int(payload.get("maxPagesPerWebsite", 3), "maxPagesPerWebsite", 1, 25)
    payload["concurrency"] = bounded_int(payload.get("concurrency", 100), "concurrency", 1, 500)
    payload["requestTimeoutSecs"] = bounded_int(payload.get("requestTimeoutSecs", 5), "requestTimeoutSecs", 2, 30)

    result_mode = str(payload.get("resultMode", "emailsOnly"))
    if result_mode not in VALID_RESULT_MODE:
        raise SkillError(f"resultMode must be one of: {', '.join(sorted(VALID_RESULT_MODE))}.")
    payload["resultMode"] = result_mode

    for field, default in {
        "extractPhones": True,
        "extractSocials": True,
        "includePersonalData": True,
        "sameDomainOnly": True,
    }.items():
        payload[field] = bool_value(payload.get(field, default), field)

    payload.pop("urls", None)
    payload.pop("startUrls", None)
    return payload


def load_payload(args: argparse.Namespace) -> dict[str, Any]:
    if args.input_json:
        try:
            payload = json.loads(args.input_json)
        except json.JSONDecodeError as exc:
            raise SkillError(f"Invalid --input-json: {exc}") from exc
    elif args.input_file:
        try:
            payload = json.loads(Path(args.input_file).read_text(encoding="utf-8"))
        except OSError as exc:
            raise SkillError(f"Cannot read --input-file: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise SkillError(f"Invalid JSON in --input-file: {exc}") from exc
    else:
        raise SkillError("Provide --input-json or --input-file.")
    return normalize_payload(payload)


def build_quick_domains_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "domains": args.domains,
        "maxResults": args.max_results,
        "resultMode": args.result_mode,
        "maxPagesPerWebsite": args.max_pages,
        "concurrency": args.concurrency,
        "requestTimeoutSecs": args.request_timeout,
        "extractPhones": not args.no_phones,
        "extractSocials": not args.no_socials,
        "includePersonalData": not args.no_personal_data,
        "sameDomainOnly": not args.allow_cross_domain,
    }
    return normalize_payload(payload)


def run_actor(token: str, actor_id: str, payload: dict[str, Any], timeout_sec: int, budget_usd: float | None) -> dict[str, Any]:
    params: dict[str, str | int | float] = {
        "token": token,
        "timeout": timeout_sec,
        "clean": "true",
    }
    if budget_usd is not None:
        if budget_usd <= 0:
            raise SkillError("--budget-usd must be > 0.")
        params["maxTotalChargeUsd"] = budget_usd

    actor_path = urllib.parse.quote(actor_id, safe="")
    url = f"https://api.apify.com/v2/acts/{actor_path}/run-sync-get-dataset-items?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_sec + 30) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SkillError(f"Apify HTTP {exc.code}: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise SkillError(f"Apify request failed: {exc}") from exc

    try:
        rows = json.loads(raw) if raw else []
    except json.JSONDecodeError as exc:
        raise SkillError(f"Apify returned invalid JSON: {raw[:1000]}") from exc

    if not isinstance(rows, list):
        raise SkillError("Apify response was not a dataset items array.")

    return {
        "ok": True,
        "actorId": actor_id,
        "fetchedAt": utc_now(),
        "inputUsed": payload,
        "itemCount": len(rows),
        "rows": rows,
    }


def add_common_run_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--actor-id", default=DEFAULT_ACTOR_ID)
    parser.add_argument("--apify-token")
    parser.add_argument("--budget-usd", type=float)
    parser.add_argument("--timeout-sec", type=int, default=DEFAULT_TIMEOUT_SEC)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run from custom JSON input.")
    run_parser.add_argument("--input-file")
    run_parser.add_argument("--input-json")
    add_common_run_args(run_parser)

    quick = subparsers.add_parser("quick-domains", help="Run from domains or website URLs.")
    quick.add_argument("--domains", nargs="+", required=True)
    quick.add_argument("--max-results", type=int, default=100)
    quick.add_argument("--result-mode", choices=sorted(VALID_RESULT_MODE), default="emailsOnly")
    quick.add_argument("--max-pages", type=int, default=3)
    quick.add_argument("--concurrency", type=int, default=100)
    quick.add_argument("--request-timeout", type=int, default=5)
    quick.add_argument("--no-phones", action="store_true")
    quick.add_argument("--no-socials", action="store_true")
    quick.add_argument("--no-personal-data", action="store_true")
    quick.add_argument("--allow-cross-domain", action="store_true")
    add_common_run_args(quick)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "run":
            payload = load_payload(args)
        elif args.command == "quick-domains":
            payload = build_quick_domains_payload(args)
        else:
            raise SkillError(f"Unsupported command: {args.command}")

        token = resolve_token(args.apify_token)
        timeout_sec = positive_int(args.timeout_sec, "timeout-sec")
        result = run_actor(token, args.actor_id, payload, timeout_sec, args.budget_usd)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except SkillError as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
