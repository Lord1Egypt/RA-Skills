#!/usr/bin/env python3
"""Render a semantic V2 request as an SVG or PNG artifact."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from _client import (
    ChartRenderHttpError,
    header_value,
    read_json_input,
    request_bytes,
    service_options,
    write_json,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a chart-render V2 request")
    parser.add_argument("request", nargs="?", default="-", help="JSON request file, or - for stdin")
    parser.add_argument("--format", choices=("png", "svg"), default="png")
    parser.add_argument("--output", help="Output image path; defaults to graphic.<format>")
    parser.add_argument("--base-url", help="Render service base URL")
    parser.add_argument("--api-key", help="API key; defaults to CHART_RENDER_API_KEY")
    parser.add_argument("--timeout", type=float, help="HTTP timeout in seconds")
    parser.add_argument("--metadata-output", help="Write response metadata JSON to this file")
    args = parser.parse_args()

    try:
        request = read_json_input(args.request)
        if not isinstance(request, dict):
            raise ValueError("render request must be a JSON object")
        base_url, api_key, timeout = service_options(args.base_url, args.api_key, args.timeout)
        raw, headers = request_bytes(
            base_url,
            f"/v2/render/{args.format}",
            method="POST",
            body=json.dumps(request, ensure_ascii=False).encode("utf-8"),
            api_key=api_key,
            timeout=timeout,
            content_type="application/json",
        )
        output_path = Path(args.output or f"graphic.{args.format}")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(raw)

        metadata = {
            "format": args.format,
            "output": str(output_path),
            "sizeBytes": len(raw),
            "contentHash": (header_value(headers, "ETag") or "").strip('"'),
        }
        for key, header in {
            "renderKind": "X-Render-Kind",
            "renderVariant": "X-Render-Variant",
            "pagePreset": "X-Document-Page-Preset",
            "pageSelection": "X-Document-Page-Selection",
            "renderer": "X-Chart-Renderer",
            "rendererVersion": "X-Chart-Renderer-Version",
            "displayWidthMm": "X-Display-Width-Mm",
            "displayHeightMm": "X-Display-Height-Mm",
            "width": "X-Image-Width",
            "height": "X-Image-Height",
            "layoutWidth": "X-Layout-Width",
            "layoutHeight": "X-Layout-Height",
            "rasterScale": "X-Raster-Scale",
        }.items():
            value = header_value(headers, header)
            if value is not None:
                metadata[key] = value
        write_json(metadata, args.metadata_output)
        return 0
    except (ChartRenderHttpError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"render_graphic.py: {error}", file=sys.stderr)
        if isinstance(error, ChartRenderHttpError) and error.details is not None:
            print(json.dumps(error.details, ensure_ascii=False, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
