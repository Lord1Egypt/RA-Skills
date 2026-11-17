#!/usr/bin/env python3
"""Small REST fallback client for the Antscity MRO Inquiry Match Skill.

The client intentionally uses only the Python standard library so an agent that
cannot register a remote MCP server can still use the matching API.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import ssl
import sys
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://mro-api.iwilley.com"


@dataclass
class ApiError(Exception):
    status: int | None
    message: str


def json_input(path: str) -> Any:
    try:
        if path == "-":
            return json.load(sys.stdin)
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ApiError(None, f"cannot read JSON input: {exc}") from exc


def api_config() -> tuple[str, str]:
    api_key = os.environ.get("MRO_API_KEY", "").strip()
    if not api_key:
        raise ApiError(None, "MRO_API_KEY is required; register and create an API key at https://mro-api.iwilley.com")
    base_url = os.environ.get("MRO_API_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ApiError(None, "MRO_API_BASE_URL must be an absolute http(s) URL")
    return base_url, api_key


def decode_response(raw: bytes) -> Any:
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"raw": raw.decode("utf-8", errors="replace")}


def tls_context() -> ssl.SSLContext:
    """Use certifi when present, while retaining stdlib-only compatibility."""
    try:
        import certifi  # type: ignore[import-not-found]

        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def call_api(method: str, path: str, payload: Any | None, timeout: float) -> Any:
    base_url, api_key = api_config()
    body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = Request(
        f"{base_url}{path}",
        data=body,
        method=method,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}",
            **({"Content-Type": "application/json"} if body is not None else {}),
        },
    )
    try:
        with urlopen(request, timeout=timeout, context=tls_context()) as response:
            return decode_response(response.read())
    except HTTPError as exc:
        detail = decode_response(exc.read())
        raise ApiError(exc.code, json.dumps(detail, ensure_ascii=False)) from exc
    except URLError as exc:
        raise ApiError(None, f"network error: {exc.reason}") from exc


def print_json(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def match_command(args: argparse.Namespace) -> int:
    payload = json_input(args.input)
    if not isinstance(payload, dict):
        raise ApiError(None, "match input must be one JSON object")
    print_json(call_api("POST", "/v1/match-inquiry", payload, args.timeout))
    return 0


def get_product_command(args: argparse.Namespace) -> int:
    path = "/v1/products/{}/{}".format(quote(args.source, safe=""), quote(args.source_id, safe=""))
    print_json(call_api("GET", path, None, args.timeout))
    return 0


def batch_command(args: argparse.Namespace) -> int:
    payload = json_input(args.input)
    inquiries = payload.get("inquiries") if isinstance(payload, dict) else payload
    if not isinstance(inquiries, list) or not inquiries:
        raise ApiError(None, "batch input must be a non-empty JSON array or an object with an inquiries array")
    if len(inquiries) > 20:
        raise ApiError(None, "batch input accepts at most 20 independent inquiries")
    if not all(isinstance(item, dict) for item in inquiries):
        raise ApiError(None, "every inquiry must be a JSON object")

    def one(index: int, inquiry: dict[str, Any]) -> dict[str, Any]:
        try:
            return {"index": index, "result": call_api("POST", "/v1/match-inquiry", inquiry, args.timeout)}
        except ApiError as exc:
            return {"index": index, "error": {"status": exc.status, "message": exc.message}}

    workers = min(max(args.workers, 1), len(inquiries), 8)
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(lambda pair: one(*pair), enumerate(inquiries)))
    print_json({"results": results})
    return 0 if all("result" in item for item in results) else 1


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="REST fallback client for the Antscity MRO API")
    result.add_argument("--timeout", type=float, default=60.0, help="network timeout in seconds (default: 60)")
    commands = result.add_subparsers(dest="command", required=True)
    sources = commands.add_parser("sources", help="list authorized sources and private catalogue count (free)")
    sources.set_defaults(handler=lambda args: (print_json(call_api("GET", "/v1/sources", None, args.timeout)) or 0))
    match = commands.add_parser("match", help="call POST /v1/match-inquiry")
    match.add_argument("--input", required=True, help="JSON request file, or - for stdin")
    match.set_defaults(handler=match_command)
    product = commands.add_parser("get-product", help="call GET /v1/products/{source}/{sourceId}")
    product.add_argument("--source", required=True)
    product.add_argument("--source-id", required=True)
    product.set_defaults(handler=get_product_command)
    batch = commands.add_parser("batch", help="run independent match requests through REST")
    batch.add_argument("--input", required=True, help="JSON array or {\"inquiries\": [...]} file, or - for stdin")
    batch.add_argument("--workers", type=int, default=4, help="local concurrent requests, 1-8 (default: 4)")
    batch.set_defaults(handler=batch_command)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        return args.handler(args)
    except ApiError as exc:
        print_json({"error": {"status": exc.status, "message": exc.message}})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
