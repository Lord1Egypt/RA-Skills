#!/usr/bin/env python3
"""Fetch the authoritative theme names from the chart render service."""

from __future__ import annotations

import argparse
import sys

from _client import ChartRenderHttpError, request_json, service_options, write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="Get supported chart-render themes")
    parser.add_argument("--base-url", help="Render service base URL")
    parser.add_argument("--api-key", help="API key; defaults to CHART_RENDER_API_KEY")
    parser.add_argument("--timeout", type=float, help="HTTP timeout in seconds")
    parser.add_argument("--output", help="Write JSON to this file instead of stdout")
    args = parser.parse_args()

    try:
        base_url, api_key, timeout = service_options(args.base_url, args.api_key, args.timeout)
        themes = request_json(base_url, "/v1/themes", api_key=api_key, timeout=timeout)
        write_json(themes, args.output)
        return 0
    except (ChartRenderHttpError, ValueError) as error:
        print(f"get_themes.py: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
