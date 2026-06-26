#!/usr/bin/env python3
"""Generate a YouTube thumbnail image with Gemini Nano Banana.

This script calls the official Gemini image generation endpoint using only the
Python standard library so it can run in minimal environments.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
from typing import Any


DEFAULT_MODEL = "gemini-2.5-flash-image"
DEFAULT_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a YouTube thumbnail image with Nano Banana."
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Final English image prompt to send to Nano Banana.",
    )
    parser.add_argument(
        "--overlay-text",
        help="Optional overlay text to record in metadata.",
    )
    parser.add_argument(
        "--angle",
        help="Optional thumbnail angle to record in metadata.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini image model to use. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--output",
        default="outputs/generated-thumbnail.png",
        help="PNG path for the generated image.",
    )
    parser.add_argument(
        "--metadata-output",
        help="Optional JSON metadata path. Defaults to <output>.json",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Retry count for transient API failures.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the request payload and exit without calling the API.",
    )
    return parser.parse_args()


def require_api_key() -> str:
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing API key. Set GEMINI_API_KEY or GOOGLE_API_KEY before running."
        )
    return api_key


def build_url(model: str) -> str:
    return DEFAULT_ENDPOINT.format(model=model)


def build_payload(prompt: str) -> dict[str, Any]:
    return {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]},
    }


def post_json(
    *,
    url: str,
    api_key: str,
    payload: dict[str, Any],
    timeout: int,
    retries: int,
) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key,
    }

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        request = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            retriable = exc.code in {429, 500, 502, 503, 504}
            last_error = RuntimeError(f"HTTP {exc.code}: {body}")
            if attempt < retries and retriable:
                time.sleep(2**attempt)
                continue
            raise last_error
        except urllib.error.URLError as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(2**attempt)
                continue
            raise

    assert last_error is not None
    raise last_error


def extract_image_bytes(response: dict[str, Any]) -> bytes:
    candidates = response.get("candidates") or []
    for candidate in candidates:
        content = candidate.get("content") or {}
        parts = content.get("parts") or []
        for part in parts:
            inline_data = part.get("inlineData") or {}
            if inline_data.get("data"):
                return base64.b64decode(inline_data["data"])
    raise RuntimeError(
        "The API response did not include image data. Full response:\n"
        + json.dumps(response, ensure_ascii=False, indent=2)
    )


def extract_text(response: dict[str, Any]) -> str | None:
    candidates = response.get("candidates") or []
    texts: list[str] = []
    for candidate in candidates:
        content = candidate.get("content") or {}
        parts = content.get("parts") or []
        for part in parts:
            if part.get("text"):
                texts.append(part["text"])
    if not texts:
        return None
    return "\n".join(texts)


def write_outputs(
    *,
    output_path: pathlib.Path,
    metadata_path: pathlib.Path,
    image_bytes: bytes,
    metadata: dict[str, Any],
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    payload = build_payload(args.prompt)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    api_key = require_api_key()
    url = build_url(args.model)
    response = post_json(
        url=url,
        api_key=api_key,
        payload=payload,
        timeout=args.timeout,
        retries=args.retries,
    )

    image_bytes = extract_image_bytes(response)
    output_path = pathlib.Path(args.output)
    metadata_path = pathlib.Path(args.metadata_output or f"{args.output}.json")
    response_text = extract_text(response)

    metadata = {
        "model": args.model,
        "angle": args.angle,
        "overlay_text": args.overlay_text,
        "prompt": args.prompt,
        "response_text": response_text,
    }
    write_outputs(
        output_path=output_path,
        metadata_path=metadata_path,
        image_bytes=image_bytes,
        metadata=metadata,
    )

    print(output_path)
    print(metadata_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
