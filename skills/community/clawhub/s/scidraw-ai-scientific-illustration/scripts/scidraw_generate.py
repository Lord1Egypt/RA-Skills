#!/usr/bin/env python3
"""Generate scientific figures with the official SciDraw AI public API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional


DEFAULT_API_BASE_URL = "https://sci-draw.com/api/v1"
ASPECT_RATIOS = (
    "1:1",
    "16:9",
    "9:16",
    "4:3",
    "3:4",
    "3:2",
    "2:3",
    "5:4",
    "4:5",
    "21:9",
)


def die(message: str, code: int = 1) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(code)


def read_prompt(prompt: Optional[str], prompt_file: Optional[str]) -> str:
    if prompt and prompt_file:
        die("Use --prompt or --prompt-file, not both.")
    if prompt_file:
        if prompt_file == "-":
            value = sys.stdin.read()
        else:
            value = Path(prompt_file).read_text(encoding="utf-8")
    elif prompt:
        value = prompt
    else:
        die("Missing prompt. Use --prompt or --prompt-file.")
    value = value.strip()
    if not value:
        die("Prompt is empty.")
    if len(value) > 5000:
        die("Prompt exceeds the SciDraw AI limit of 5000 characters.")
    return value


def decode_json(raw: bytes) -> Dict[str, Any]:
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("SciDraw AI returned an invalid JSON response.") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("SciDraw AI returned an unexpected response.")
    return payload


def api_request(
    method: str,
    url: str,
    api_key: str,
    *,
    payload: Optional[Dict[str, Any]] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "SciDraw-Skill/1.0",
    }
    body = None
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if extra_headers:
        headers.update(extra_headers)

    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            envelope = decode_json(response.read())
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        try:
            envelope = decode_json(raw)
            error = envelope.get("error") or {}
            error_code = error.get("code") or f"HTTP_{exc.code}"
            message = error.get("message") or exc.reason
            request_id = error.get("request_id")
            suffix = f" (request {request_id})" if request_id else ""
            raise RuntimeError(f"{error_code}: {message}{suffix}") from exc
        except RuntimeError:
            raise
        except Exception as parse_exc:
            raise RuntimeError(f"HTTP {exc.code}: {exc.reason}") from parse_exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network request failed: {exc.reason}") from exc

    if envelope.get("success") is not True:
        error = envelope.get("error") or {}
        raise RuntimeError(
            f"{error.get('code', 'API_ERROR')}: "
            f"{error.get('message', 'SciDraw AI request failed.')}"
        )
    data = envelope.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("SciDraw AI response did not contain job data.")
    return data


def wait_for_job(
    api_base_url: str,
    api_key: str,
    job: Dict[str, Any],
    timeout_seconds: int,
) -> Dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    while job.get("status") in {"queued", "processing"}:
        if time.monotonic() >= deadline:
            raise RuntimeError(
                f"Timed out waiting for SciDraw AI job {job.get('id', 'unknown')}."
            )
        time.sleep(2)
        job_id = str(job.get("id") or "")
        if not job_id:
            raise RuntimeError("SciDraw AI response did not contain a job ID.")
        encoded_id = urllib.parse.quote(job_id, safe="")
        job = api_request("GET", f"{api_base_url}/jobs/{encoded_id}", api_key)
    return job


def target_path(out_path: Path, index: int, total: int, file_format: str) -> Path:
    suffix = out_path.suffix or f".{file_format}"
    if total == 1:
        return out_path if out_path.suffix else out_path.with_suffix(suffix)
    stem = out_path.stem if out_path.suffix else out_path.name
    return out_path.with_name(f"{stem}-{index + 1}{suffix}")


def download_file(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "SciDraw-Skill/1.0"},
        method="GET",
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            destination.write_bytes(response.read())
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        raise RuntimeError(f"Could not download generated image: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate scientific figures with the official SciDraw AI API."
    )
    parser.add_argument("--prompt")
    parser.add_argument("--prompt-file")
    parser.add_argument("--out", default="outputs/figure.png")
    parser.add_argument("--aspect-ratio", choices=ASPECT_RATIOS, default="16:9")
    parser.add_argument("--resolution", choices=("2K", "4K"), default="2K")
    parser.add_argument("--count", type=int, choices=range(1, 5), default=1)
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Maximum seconds to wait for the generation job (default: 300).",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    api_key = os.getenv("SCIDRAW_API_KEY", "").strip()
    if not api_key:
        die(
            "SCIDRAW_API_KEY is required. Create one at "
            "https://sci-draw.com/settings/api-keys."
        )
    if not api_key.startswith("sd_"):
        die("SCIDRAW_API_KEY must be a SciDraw AI key beginning with 'sd_'.")
    if args.timeout < 30:
        die("--timeout must be at least 30 seconds.")

    api_base_url = os.getenv(
        "SCIDRAW_API_BASE_URL", DEFAULT_API_BASE_URL
    ).strip().rstrip("/")
    if not api_base_url.startswith(("https://", "http://")):
        die("SCIDRAW_API_BASE_URL must be an HTTP(S) URL.")

    prompt = read_prompt(args.prompt, args.prompt_file)
    out_path = Path(args.out).expanduser().resolve()
    request_payload = {
        "prompt": prompt,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "count": args.count,
    }
    idempotency_key = f"scidraw-skill-{uuid.uuid4().hex}"

    started = time.monotonic()
    try:
        job = api_request(
            "POST",
            f"{api_base_url}/images/generations",
            api_key,
            payload=request_payload,
            extra_headers={
                "Idempotency-Key": idempotency_key,
                "Prefer": "wait=30",
            },
        )
        job = wait_for_job(api_base_url, api_key, job, args.timeout)

        if job.get("status") != "succeeded":
            error = job.get("error") or {}
            raise RuntimeError(
                f"{error.get('code', 'JOB_FAILED')}: "
                f"{error.get('message', 'SciDraw AI generation did not succeed.')}"
            )

        result = job.get("result") or {}
        files = result.get("files") or []
        if not files:
            raise RuntimeError("SciDraw AI job succeeded without output files.")

        saved_files: List[str] = []
        for index, item in enumerate(files):
            url = str(item.get("url") or "")
            if not url:
                raise RuntimeError("SciDraw AI returned a file without a URL.")
            file_format = str(item.get("format") or "png")
            destination = target_path(out_path, index, len(files), file_format)
            download_file(url, destination)
            saved_files.append(str(destination))
    except RuntimeError as exc:
        die(str(exc))

    output = {
        "status": "ok",
        "backend": "scidraw_ai",
        "job_id": job.get("id"),
        "resolution": args.resolution,
        "aspect_ratio": args.aspect_ratio,
        "count": len(saved_files),
        "files": saved_files,
        "elapsed_seconds": round(time.monotonic() - started, 2),
    }
    if args.json:
        print(json.dumps(output, ensure_ascii=False))
    else:
        for saved_file in saved_files:
            print(f"Image saved: {saved_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
