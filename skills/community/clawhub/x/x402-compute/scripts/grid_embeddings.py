#!/usr/bin/env python3
"""Build and call SGL Grid text or multimodal embedding requests.

Credentials come only from --api-key, SGL_API_KEY, or COMPUTE_API_KEY.
This script never loads .env files and never performs x402 signing.

Examples:
  python grid_embeddings.py models
  python grid_embeddings.py embed --text "A searchable document" --dimensions 256
  python grid_embeddings.py embed --text "Demo" --image frame.png \
      --audio narration.mp3 --audio-seconds 4.2 --input-type document
  python grid_embeddings.py embed --part text:"Demo" --part image:frame.png \
      --part audio:narration.mp3@4.2 --dry-run
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import mimetypes
import os
from pathlib import Path
import sys
from typing import Any

import requests


DEFAULT_BASE_URL = "https://grid.x402compute.cc"
MODEL = "embeddinggemma-2"
MIB = 1024 * 1024
MAX_BODY = 24 * MIB
MAX_MEDIA = 20 * MIB
MAX_IMAGE_TOTAL = 8 * MIB
MIME_BY_SUFFIX = {
    ".jpg": ("image", "image/jpeg"),
    ".jpeg": ("image", "image/jpeg"),
    ".png": ("image", "image/png"),
    ".webp": ("image", "image/webp"),
    ".wav": ("audio", "audio/wav"),
    ".flac": ("audio", "audio/flac"),
    ".mp3": ("audio", "audio/mpeg"),
    ".mp4": ("video", "video/mp4"),
}


class InputError(ValueError):
    """A local request-construction error."""


def api_key(explicit: str | None) -> str | None:
    return explicit or os.environ.get("SGL_API_KEY") or os.environ.get("COMPUTE_API_KEY")


def media_part(path_value: str, expected_kind: str | None = None, duration: float | None = None) -> tuple[dict[str, Any], int]:
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise InputError(f"Media file does not exist: {path}")
    identified = MIME_BY_SUFFIX.get(path.suffix.lower())
    if not identified:
        guessed = mimetypes.guess_type(path.name)[0]
        raise InputError(f"Unsupported media type for {path.name}: {guessed or 'unknown'}")
    kind, mime_type = identified
    if expected_kind and kind != expected_kind:
        raise InputError(f"Expected {expected_kind}, got {kind}: {path.name}")

    raw = path.read_bytes()
    byte_limit = 16 * MIB if kind == "video" else 8 * MIB
    if not raw or len(raw) > byte_limit:
        raise InputError(f"{path.name} must contain 1-{byte_limit // MIB} MiB")

    part: dict[str, Any] = {
        "type": kind,
        "media": {
            "encoding": "base64",
            "mime_type": mime_type,
            "data": base64.b64encode(raw).decode("ascii"),
            "sha256": hashlib.sha256(raw).hexdigest(),
        },
    }
    if kind in {"audio", "video"}:
        maximum = 30 if kind == "audio" else 32
        if duration is None or not 0 < duration <= maximum:
            raise InputError(f"{kind} duration must be >0 and <= {maximum} seconds")
        part["duration_seconds"] = duration
    elif duration is not None:
        raise InputError("Images do not accept duration_seconds")
    return part, len(raw)


def parse_ordered_part(value: str) -> tuple[dict[str, Any], int]:
    if ":" not in value:
        raise InputError("--part must be text:VALUE, image:PATH, audio:PATH@SECONDS, or video:PATH@SECONDS")
    kind, payload = value.split(":", 1)
    if kind == "text":
        if not payload:
            raise InputError("Text parts must be nonempty")
        return {"type": "text", "text": payload}, 0
    if kind not in {"image", "audio", "video"}:
        raise InputError(f"Unsupported part type: {kind}")
    duration = None
    if kind in {"audio", "video"}:
        if "@" not in payload:
            raise InputError(f"{kind} --part requires PATH@SECONDS")
        payload, seconds = payload.rsplit("@", 1)
        try:
            duration = float(seconds)
        except ValueError as error:
            raise InputError(f"Invalid {kind} duration: {seconds}") from error
    return media_part(payload, kind, duration)


def validate_parts(parts_with_sizes: list[tuple[dict[str, Any], int]]) -> list[dict[str, Any]]:
    if not 1 <= len(parts_with_sizes) <= 16:
        raise InputError("Use 1-16 ordered content parts")
    parts = [part for part, _ in parts_with_sizes]
    images = [(part, size) for part, size in parts_with_sizes if part["type"] == "image"]
    audio = [part for part in parts if part["type"] == "audio"]
    video = [part for part in parts if part["type"] == "video"]
    if len(images) > 8 or len(audio) > 1 or len(video) > 1:
        raise InputError("Use at most eight images, one audio part, and one video part per item")
    if sum(size for _, size in images) > MAX_IMAGE_TOTAL:
        raise InputError("Total image bytes per item must not exceed 8 MiB")
    if sum(size for _, size in parts_with_sizes) > MAX_MEDIA:
        raise InputError("Decoded media per request must not exceed 20 MiB")
    text_bytes = sum(len(part["text"].encode("utf-8")) for part in parts if part["type"] == "text")
    if text_bytes > 10 * MIB:
        raise InputError("Aggregate UTF-8 text must not exceed 10 MiB")
    return parts


def build_body(args: argparse.Namespace) -> dict[str, Any]:
    if args.request_json:
        if args.part or args.text or args.image or args.audio or args.video:
            raise InputError("--request-json cannot be combined with part-building flags")
        try:
            body = json.loads(Path(args.request_json).read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise InputError(f"Could not read request JSON: {error}") from error
        if not isinstance(body, dict):
            raise InputError("Request JSON must contain an object")
        return body

    parts_with_sizes: list[tuple[dict[str, Any], int]] = []
    if args.part:
        if args.text or args.image or args.audio or args.video:
            raise InputError("--part cannot be combined with --text/--image/--audio/--video")
        parts_with_sizes.extend(parse_ordered_part(value) for value in args.part)
    else:
        if args.text:
            parts_with_sizes.append(({"type": "text", "text": args.text}, 0))
        for path in args.image or []:
            parts_with_sizes.append(media_part(path, "image"))
        if args.audio:
            parts_with_sizes.append(media_part(args.audio, "audio", args.audio_seconds))
        elif args.audio_seconds is not None:
            raise InputError("--audio-seconds requires --audio")
        if args.video:
            parts_with_sizes.append(media_part(args.video, "video", args.video_seconds))
        elif args.video_seconds is not None:
            raise InputError("--video-seconds requires --video")

    parts = validate_parts(parts_with_sizes)
    return {
        "model": MODEL,
        "input": [{"content": parts}],
        "input_type": args.input_type,
        "dimensions": args.dimensions,
        "encoding_format": "float",
    }


def encoded_body(body: dict[str, Any]) -> bytes:
    raw = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    if len(raw) > MAX_BODY:
        raise InputError("Encoded JSON body exceeds 24 MiB")
    return raw


def list_models(base_url: str, key: str | None) -> int:
    headers = {"X-API-Key": key} if key else {}
    response = requests.get(
        f"{base_url.rstrip('/')}/v1/models",
        params={"type": "embedding"},
        headers=headers,
        timeout=30,
    )
    try:
        result = response.json()
    except ValueError:
        result = {"error": response.text[:1000]}
    print(json.dumps(result, indent=2))
    return 0 if response.status_code == 200 else 1


def embed(args: argparse.Namespace) -> int:
    body = build_body(args)
    raw = encoded_body(body)
    if args.dry_run:
        print(json.dumps(body, indent=2))
        print(f"\nEncoded request bytes: {len(raw)}", file=sys.stderr)
        return 0

    key = api_key(args.api_key)
    if not key:
        raise InputError("Set COMPUTE_API_KEY or SGL_API_KEY, or pass --api-key. Use --dry-run without credentials.")
    response = requests.post(
        f"{args.base_url.rstrip('/')}/v1/embeddings",
        data=raw,
        headers={"Content-Type": "application/json", "X-API-Key": key},
        timeout=args.timeout,
    )
    try:
        result = response.json()
    except ValueError:
        result = {"error": response.text[:2000]}
    print(json.dumps(result, indent=2))
    return 0 if response.status_code == 200 else 1


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="SGL Grid EmbeddingGemma 2 client")
    root.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Grid base URL")
    root.add_argument("--api-key", help="Grid API key; otherwise SGL_API_KEY or COMPUTE_API_KEY")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("models", help="List currently available embedding models")

    run = commands.add_parser("embed", help="Build and submit one embedding request")
    run.add_argument("--part", action="append", default=[], help="Ordered part: text:VALUE, image:PATH, audio:PATH@SECONDS, video:PATH@SECONDS")
    run.add_argument("--text", help="Text part (convenience order: text, images, audio, video)")
    run.add_argument("--image", action="append", default=[], help="JPEG, PNG, or WebP path; repeatable")
    run.add_argument("--audio", help="WAV, FLAC, or MP3 path")
    run.add_argument("--audio-seconds", type=float, help="Declared audio duration, max 30")
    run.add_argument("--video", help="MP4 path")
    run.add_argument("--video-seconds", type=float, help="Declared video duration, max 32")
    run.add_argument("--request-json", help="Full request body file for batches or custom ordering")
    run.add_argument("--dimensions", type=int, choices=[768, 512, 256, 128], default=768)
    run.add_argument(
        "--input-type",
        choices=["query", "document", "unspecified"],
        default="query",
        help="Retrieval prefix (default: query; use unspecified only to opt out)",
    )
    run.add_argument("--timeout", type=float, default=130)
    run.add_argument("--dry-run", action="store_true", help="Print the exact request without sending")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "models":
            return list_models(args.base_url, api_key(args.api_key))
        return embed(args)
    except InputError as error:
        print(json.dumps({"error": str(error)}, indent=2), file=sys.stderr)
        return 2
    except requests.RequestException as error:
        print(json.dumps({"error": f"Network request failed: {error}"}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
