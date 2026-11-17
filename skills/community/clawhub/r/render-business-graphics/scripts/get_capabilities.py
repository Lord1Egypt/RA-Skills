#!/usr/bin/env python3
"""Fetch the current V2 contract and emit either a compact capability map or the full contract."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from _client import ChartRenderHttpError, request_json, service_options, write_json


def compact_contract(contract: dict[str, Any]) -> dict[str, Any]:
    summaries = []
    for item in contract.get("contracts", []):
        if not isinstance(item, dict):
            continue
        schema = item.get("schema") or {}
        variant = ((schema.get("properties") or {}).get("variant") or {}).get("enum")
        summaries.append({
            "kind": item.get("kind"),
            "variants": variant or ([] if item.get("kind") in {"organization", "sequence"} else None),
            "example": item.get("example"),
        })
    return {
        "version": contract.get("version"),
        "endpoint": contract.get("endpoint"),
        "formats": contract.get("formats"),
        "kinds": contract.get("kinds"),
        "themes": contract.get("themes"),
        "pages": contract.get("pages"),
        "defaults": contract.get("defaults"),
        "pagePolicy": contract.get("pagePolicy"),
        "capabilities": contract.get("capabilities"),
        "contracts": summaries,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Get chart-render V2 capabilities and contract")
    parser.add_argument("--full", action="store_true", help="Return the complete V2 JSON Schema and examples")
    parser.add_argument("--base-url", help="Render service base URL")
    parser.add_argument("--api-key", help="API key; defaults to CHART_RENDER_API_KEY")
    parser.add_argument("--timeout", type=float, help="HTTP timeout in seconds")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    try:
        base_url, api_key, timeout = service_options(args.base_url, args.api_key, args.timeout)
        contract = request_json(base_url, "/v2/contracts", api_key=api_key, timeout=timeout)
        if not isinstance(contract, dict):
            raise ValueError("contract response must be a JSON object")
        write_json(contract if args.full else compact_contract(contract), args.output)
        return 0
    except (ChartRenderHttpError, ValueError) as error:
        print(f"get_capabilities.py: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
