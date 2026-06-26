#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pipeline_common import download_media_url


def load_headers(
    inline_headers: list[str] | None = None,
    headers_json: str | None = None,
) -> dict[str, str]:
    headers: dict[str, str] = {}

    if headers_json:
        candidate = Path(headers_json)
        if candidate.is_file():
            loaded = json.loads(candidate.read_text(encoding="utf-8"))
        else:
            loaded = json.loads(headers_json)
        if not isinstance(loaded, dict):
            raise SystemExit("`--headers-json` must point to or contain a JSON object.")
        headers.update({str(key): str(value) for key, value in loaded.items() if value is not None})

    for item in inline_headers or []:
        if "=" not in item:
            raise SystemExit(f"Invalid `--header` value: {item!r}. Expected KEY=VALUE.")
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            raise SystemExit(f"Invalid `--header` value: {item!r}. Expected KEY=VALUE.")
        headers[key] = value

    return headers


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download a direct media URL to disk, including HLS manifests when possible."
    )
    parser.add_argument("url", help="Direct media URL")
    parser.add_argument("output", help="Output file path")
    parser.add_argument(
        "--header",
        action="append",
        help="Optional request header in KEY=VALUE form; may be repeated",
    )
    parser.add_argument(
        "--headers-json",
        help="Optional JSON string or path to a JSON file containing additional request headers",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    headers = load_headers(args.header, args.headers_json)
    download_media_url(args.url, output_path, headers=headers)
    print(f"Saved: {output_path.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
