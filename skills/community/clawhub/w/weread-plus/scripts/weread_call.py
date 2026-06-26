#!/usr/bin/env python3
"""Call a WeRead gateway endpoint with flat JSON parameters."""

from __future__ import annotations

import argparse
import json
from typing import Any

from weread_common import WeReadError, api_post, fail, json_dumps


def parse_value(raw: str) -> Any:
    lowered = raw.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return raw


def main() -> None:
    parser = argparse.ArgumentParser(description="Call the WeRead Agent API gateway")
    parser.add_argument("api_name", help="Endpoint name, for example /book/info")
    parser.add_argument("--param", action="append", default=[], help="Flat key=value parameter. Repeatable.")
    parser.add_argument("--json", dest="json_body", help="JSON object of flat parameters")
    parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    args = parser.parse_args()

    params: dict[str, Any] = {}
    if args.json_body:
        try:
            params.update(json.loads(args.json_body))
        except json.JSONDecodeError as exc:
            fail(f"Invalid --json body: {exc}")
    for item in args.param:
        if "=" not in item:
            fail(f"--param must be key=value, got: {item}")
        key, raw_value = item.split("=", 1)
        params[key] = parse_value(raw_value)

    try:
        data = api_post(args.api_name, params)
    except WeReadError as exc:
        fail(str(exc))
    print(json_dumps(data, pretty=not args.compact))


if __name__ == "__main__":
    main()
