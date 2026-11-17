#!/usr/bin/env python3
"""Fetch one graphic's exact schema, example request, and optional local preview."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from _client import (
    ChartRenderHttpError,
    decode_data_url,
    request_json,
    service_options,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Get one chart-render graphic contract")
    parser.add_argument("graphic_id", help="Stable id such as chart.bar or timeline.milestone")
    parser.add_argument("--base-url", help="Render service base URL")
    parser.add_argument("--api-key", help="API key; defaults to CHART_RENDER_API_KEY")
    parser.add_argument("--timeout", type=float, help="HTTP timeout in seconds")
    parser.add_argument("--preview-output", help="Save the catalog preview to this file")
    parser.add_argument("--output", help="Write contract JSON to this file instead of stdout")
    args = parser.parse_args()

    try:
        base_url, api_key, timeout = service_options(args.base_url, args.api_key, args.timeout)
        catalog = request_json(base_url, "/v2/catalog", api_key=api_key, timeout=timeout)
        items = catalog.get("items") if isinstance(catalog, dict) else None
        item = next((candidate for candidate in items or []
                     if isinstance(candidate, dict) and candidate.get("id") == args.graphic_id), None)
        if item is None:
            available = ", ".join(str(candidate.get("id")) for candidate in items or [] if isinstance(candidate, dict))
            raise ValueError(f"unknown graphic id {args.graphic_id!r}; available ids: {available}")

        preview = item.get("image") or {}
        preview_result: dict[str, Any] = {
            "name": preview.get("name"),
            "format": preview.get("format"),
            "mediaType": preview.get("mediaType"),
            "width": preview.get("width"),
            "height": preview.get("height"),
            "contentHash": preview.get("contentHash"),
        }
        data_url = preview.get("dataUrl")
        if args.preview_output and isinstance(data_url, str):
            _media_type, data = decode_data_url(data_url)
            target = Path(args.preview_output)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            preview_result["path"] = str(target)

        result = {
            "renderContractVersion": catalog.get("renderContractVersion"),
            "id": item.get("id"),
            "name": item.get("name"),
            "kind": item.get("kind"),
            **({"variant": item["variant"]} if item.get("variant") else {}),
            "parameters": item.get("parameters"),
            "exampleRequest": item.get("exampleRequest"),
            "referenceImage": preview_result,
        }
        write_json(result, args.output)
        return 0
    except (ChartRenderHttpError, ValueError, OSError) as error:
        print(f"get_graphic_contract.py: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
