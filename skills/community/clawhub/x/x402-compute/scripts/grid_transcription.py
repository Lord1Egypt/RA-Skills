#!/usr/bin/env python3
"""Validate and submit one release-gated SGL Grid transcription request.

The SDK accepts raw mono 16 kHz signed 16-bit little-endian PCM. This wrapper
deliberately delegates node reservation, key verification, client sealing,
signed-result verification, and decryption to the official singularity-grid SDK.
It never loads .env files and never implements a plaintext or multipart fallback.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, is_dataclass
import json
import math
import os
from pathlib import Path
import sys
from typing import Any

import requests


DEFAULT_BASE_URL = "https://grid.x402compute.cc"
MODEL = "whisper-1"
PROTOCOL = "transcription-v1"
SAMPLE_RATE = 16_000
CHANNELS = 1
BITS_PER_SAMPLE = 16
MAX_SAMPLES = 960_000
MAX_PCM_BYTES = 1_920_000
PRICE_PER_SECOND_USD = 0.0001
SUPPORTED_SUFFIXES = {".pcm", ".raw", ".s16le"}


class InputError(ValueError):
    """A local validation or setup error; no request has been sent."""


def api_key(explicit: str | None) -> str | None:
    return explicit or os.environ.get("SGL_API_KEY") or os.environ.get("COMPUTE_API_KEY")


def read_pcm(path_value: str) -> bytes:
    path = Path(path_value).expanduser()
    if not path.is_file():
        raise InputError(f"PCM file does not exist: {path}")
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise InputError("Input must be raw PCM with a .pcm, .raw, or .s16le suffix; containers are unsupported")
    size = path.stat().st_size
    if size <= 0:
        raise InputError("PCM input must contain at least one two-byte sample")
    if size % 2:
        raise InputError("Signed 16-bit PCM must contain a positive even number of bytes")
    if size > MAX_PCM_BYTES:
        raise InputError(f"PCM input exceeds {MAX_PCM_BYTES} bytes (60 seconds)")
    with path.open("rb") as stream:
        raw = stream.read(MAX_PCM_BYTES + 1)
    if len(raw) > MAX_PCM_BYTES:
        raise InputError("PCM input grew beyond the 60-second limit during reading")
    if len(raw) != size:
        raise InputError("PCM file changed while it was being read")
    return raw


def metadata(raw: bytes, language: str) -> dict[str, Any]:
    if not raw or len(raw) % 2 or len(raw) > MAX_PCM_BYTES:
        raise InputError("PCM must have a positive even byte count and fit the 60-second limit")
    if language != "auto" and (len(language) != 2 or not language.isascii() or not language.islower() or not language.isalpha()):
        raise InputError('language must be "auto" or a lowercase two-letter code')
    samples = len(raw) // 2
    price_micro_usdc = max(100, (samples * 100 + SAMPLE_RATE - 1) // SAMPLE_RATE)
    return {
        "model": MODEL,
        "transcription_protocol": PROTOCOL,
        "audio_format": "pcm_s16le_16k_mono",
        "sample_rate": SAMPLE_RATE,
        "channels": CHANNELS,
        "bits_per_sample": BITS_PER_SAMPLE,
        "sample_count": samples,
        "duration_seconds": samples / SAMPLE_RATE,
        "quote": {
            "sample_count": samples,
            "audio_seconds": samples / SAMPLE_RATE,
            "rate_usd_per_second": PRICE_PER_SECOND_USD,
            "minimum_charge_usd": PRICE_PER_SECOND_USD,
            "price_usd": price_micro_usdc / 1_000_000,
            "currency": "USDC",
        },
        "language": language,
    }


def jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return asdict(value)
    if hasattr(value, "model_dump"):
        return value.model_dump()
    if hasattr(value, "dict"):
        return value.dict()
    if isinstance(value, dict):
        return value
    if hasattr(value, "__dict__"):
        return {key: jsonable(item) for key, item in vars(value).items() if not key.startswith("_")}
    if isinstance(value, (list, tuple)):
        return [jsonable(item) for item in value]
    return value


def list_models(base_url: str, key: str | None) -> int:
    headers = {"X-API-Key": key} if key else {}
    response = requests.get(
        f"{base_url.rstrip('/')}/v1/models",
        params={"type": "transcription"},
        headers=headers,
        timeout=30,
    )
    try:
        result = response.json()
    except ValueError:
        result = {"error": response.text[:1000]}
    print(json.dumps(result, indent=2))
    return 0 if response.status_code == 200 else 1


def transcribe(args: argparse.Namespace) -> int:
    raw = read_pcm(args.path)
    details = metadata(raw, args.language)
    if args.dry_run:
        print(json.dumps(details, indent=2))
        print("\nDry run only: no reservation was made and no audio was sent.", file=sys.stderr)
        return 0

    key = api_key(args.api_key)
    if not key:
        raise InputError("Set COMPUTE_API_KEY or SGL_API_KEY, or pass --api-key. Use --dry-run without credentials.")
    try:
        from singularity_grid import GridClient
    except ImportError as error:
        raise InputError(
            "Install the released singularity-grid SDK with transcription support; this wrapper never reimplements sealing"
        ) from error

    grid = GridClient(api_key=key, base_url=args.base_url, timeout=120)
    if not hasattr(grid, "transcribe_pcm"):
        raise InputError("Installed singularity-grid SDK does not include the client-sealed transcription helper")
    try:
        result = grid.transcribe_pcm(
            raw,
            model=MODEL,
            language=args.language,
            use_credits=True,
            node=args.node,
            max_price=args.max_price,
        )
    except Exception as error:
        # SDK exceptions can contain server response data. Keep failure output metadata-only.
        raise InputError("SDK transcription failed; reconcile any job/payment outcome before retrying") from error
    finally:
        grid.close()
    print(json.dumps(jsonable(result), indent=2, ensure_ascii=False))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description="SGL Grid client-sealed speech-to-text helper")
    root.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Grid base URL")
    root.add_argument("--api-key", help="Grid API key; otherwise SGL_API_KEY or COMPUTE_API_KEY")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("models", help="List currently available transcription models (read-only)")

    run = commands.add_parser("transcribe", help="Validate and transcribe one bounded raw PCM file")
    run.add_argument("path", help="Raw mono 16 kHz signed 16-bit little-endian PCM file")
    run.add_argument("--language", default="auto", help='"auto" or lowercase two-letter language hint')
    run.add_argument("--node", help="Optional eligible provider node id")
    run.add_argument("--max-price", type=float, help="Maximum accepted quote in USD")
    run.add_argument("--dry-run", action="store_true", help="Validate and print metadata without network access")
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "models":
            return list_models(args.base_url, api_key(args.api_key))
        if args.max_price is not None and (not math.isfinite(args.max_price) or args.max_price <= 0):
            raise InputError("--max-price must be a positive finite number")
        return transcribe(args)
    except (InputError, requests.RequestException, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
