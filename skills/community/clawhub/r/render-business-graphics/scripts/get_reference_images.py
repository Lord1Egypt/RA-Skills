#!/usr/bin/env python3
"""Fetch the graphic catalog, contracts, examples, and optional SVG previews."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from _client import (
    ChartRenderHttpError,
    decode_data_url,
    request_json,
    safe_filename,
    service_options,
    write_json,
)


def compact_item(item: dict[str, Any]) -> dict[str, Any]:
    image = item.get("image") or {}
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "kind": item.get("kind"),
        **({"variant": item["variant"]} if item.get("variant") else {}),
        "image": {
            "name": image.get("name"),
            "format": image.get("format"),
            "mediaType": image.get("mediaType"),
            "width": image.get("width"),
            "height": image.get("height"),
            "contentHash": image.get("contentHash"),
        },
    }


def select_items(catalog: dict[str, Any], graphic_id: str | None, kind: str | None) -> list[dict[str, Any]]:
    items = catalog.get("items")
    if not isinstance(items, list):
        raise ValueError("catalog response does not contain an items array")
    filtered = [item for item in items if isinstance(item, dict) and (not kind or item.get("kind") == kind)]
    if not graphic_id:
        return filtered
    selected = [item for item in filtered if item.get("id") == graphic_id]
    if not selected:
        available = ", ".join(str(item.get("id")) for item in filtered)
        raise ValueError(f"unknown graphic id {graphic_id!r}; available ids: {available}")
    return selected


def save_previews(items: list[dict[str, Any]], output_dir: str) -> list[dict[str, str]]:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    saved: list[dict[str, str]] = []
    for item in items:
        image = item.get("image") or {}
        data_url = image.get("dataUrl")
        if not isinstance(data_url, str):
            continue
        media_type, data = decode_data_url(data_url)
        suffix = ".svg" if media_type == "image/svg+xml" else ".bin"
        target = directory / f"{safe_filename(str(item.get('id') or 'graphic'))}{suffix}"
        target.write_bytes(data)
        saved.append({"id": str(item.get("id")), "path": str(target), "mediaType": media_type})
    return saved


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Get graphic reference images; --id also returns the exact request schema and example"
    )
    parser.add_argument("--id", dest="graphic_id", help="Stable catalog id, for example chart.bar")
    parser.add_argument("--kind", help="Only list one kind, for example chart or smartart")
    parser.add_argument("--base-url", help="Render service base URL")
    parser.add_argument("--api-key", help="API key; defaults to CHART_RENDER_API_KEY")
    parser.add_argument("--timeout", type=float, help="HTTP timeout in seconds")
    parser.add_argument("--output-dir", help="Save catalog preview images as files")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    try:
        base_url, api_key, timeout = service_options(args.base_url, args.api_key, args.timeout)
        catalog = request_json(base_url, "/v2/catalog", api_key=api_key, timeout=timeout)
        items = select_items(catalog, args.graphic_id, args.kind)

        saved = save_previews(items, args.output_dir) if args.output_dir else []
        if args.graphic_id:
            item = dict(items[0])
            if saved:
                item["referenceImage"] = saved[0]
            result: dict[str, Any] = {
                "renderContractVersion": catalog.get("renderContractVersion"),
                "id": item.get("id"),
                "name": item.get("name"),
                "kind": item.get("kind"),
                **({"variant": item["variant"]} if item.get("variant") else {}),
                "parameters": item.get("parameters"),
                "exampleRequest": item.get("exampleRequest"),
                "referenceImage": item.get("referenceImage") or compact_item(item).get("image"),
            }
        else:
            result = {
                "version": catalog.get("version"),
                "renderContractVersion": catalog.get("renderContractVersion"),
                "count": len(items),
                **({"kind": args.kind} if args.kind else {}),
                "items": [compact_item(item) for item in items],
            }
        if saved and not args.graphic_id:
            result["savedPreviews"] = saved
        write_json(result, args.output)
        return 0
    except (ChartRenderHttpError, ValueError, OSError) as error:
        print(f"get_reference_images.py: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
