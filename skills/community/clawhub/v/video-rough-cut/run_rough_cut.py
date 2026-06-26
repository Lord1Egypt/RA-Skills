#!/usr/bin/env python3
"""Submit and monitor a local B-Roll Studio rough-cut job."""

from __future__ import annotations

import argparse
import io
import json
import mimetypes
import os
import sys
import time
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen


PROCESSING_STATUSES = {
    "processing",
    "transcribing",
    "detecting_pauses",
    "analyzing_brightness",
    "applying_beauty",
    "encoding",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run local rough-cut job via B-Roll Studio API")
    parser.add_argument("--video", required=True, help="Absolute path to source video")
    parser.add_argument("--base-url", default="http://localhost/api/v1", help="API base URL")
    parser.add_argument("--name", default=None, help="Job name")
    parser.add_argument("--platform-preset", default="douyin")
    parser.add_argument("--remove-pauses", dest="remove_pauses", action="store_true", default=True)
    parser.add_argument("--no-remove-pauses", dest="remove_pauses", action="store_false")
    parser.add_argument("--remove-breaths", dest="remove_breaths", action="store_true", default=True)
    parser.add_argument("--no-remove-breaths", dest="remove_breaths", action="store_false")
    parser.add_argument("--adjust-brightness", dest="adjust_brightness", action="store_true", default=True)
    parser.add_argument("--no-adjust-brightness", dest="adjust_brightness", action="store_false")
    parser.add_argument("--trim-head-tail", dest="trim_head_tail", action="store_true", default=True)
    parser.add_argument("--no-trim-head-tail", dest="trim_head_tail", action="store_false")
    parser.add_argument("--auto-center", dest="auto_center", action="store_true", default=True)
    parser.add_argument("--no-auto-center", dest="auto_center", action="store_false")
    parser.add_argument("--stabilize", dest="stabilize", action="store_true", default=True)
    parser.add_argument("--no-stabilize", dest="stabilize", action="store_false")
    parser.add_argument("--denoise-audio", dest="denoise_audio", action="store_true", default=False)
    parser.add_argument("--beauty-mode", choices=["light", "ai", "off"], default="light")
    parser.add_argument("--beauty-strength", type=float, default=0.5)
    parser.add_argument("--min-pause-duration", type=float, default=0.5)
    parser.add_argument("--breath-sensitivity", type=float, default=0.6)
    parser.add_argument("--crossfade-duration", type=float, default=0.02)
    parser.add_argument("--wait", action="store_true", help="Poll until completed or failed")
    parser.add_argument("--download", action="store_true", help="Download output after completion")
    parser.add_argument("--output", default=None, help="Optional explicit download path")
    parser.add_argument("--poll-interval", type=float, default=3.0)
    parser.add_argument("--timeout", type=float, default=1800.0)
    parser.add_argument("--show-decisions", action="store_true", help="Print cut decisions after completion")
    return parser


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def api_url(base_url: str, path: str) -> str:
    return urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def build_multipart(data: dict[str, str], file_path: Path) -> tuple[bytes, str]:
    boundary = "----CodexRoughCutBoundary"
    chunks: list[bytes] = []

    for key, value in data.items():
        chunks.extend([
            f"--{boundary}\r\n".encode(),
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode(),
            str(value).encode(),
            b"\r\n",
        ])

    mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    file_bytes = file_path.read_bytes()
    chunks.extend([
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'.encode(),
        f"Content-Type: {mime}\r\n\r\n".encode(),
        file_bytes,
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ])
    return b"".join(chunks), boundary


def http_json(method: str, url: str, body: bytes | None = None, content_type: str | None = None, timeout: float = 30) -> dict:
    headers = {}
    if content_type:
        headers["Content-Type"] = content_type
    req = Request(url, data=body, headers=headers, method=method)
    with urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8")
    return json.loads(raw)


def http_download(url: str, output_path: Path, timeout: float = 600) -> None:
    req = Request(url, method="GET")
    with urlopen(req, timeout=timeout) as resp:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("wb") as f:
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)


def submit_job(args: argparse.Namespace) -> dict:
    video = Path(args.video).expanduser().resolve()
    if not video.exists():
        raise FileNotFoundError(f"Video not found: {video}")

    data = {
        "name": args.name or video.stem,
        "platform_preset": args.platform_preset,
        "remove_pauses": bool_string(args.remove_pauses),
        "remove_breaths": bool_string(args.remove_breaths),
        "adjust_brightness": bool_string(args.adjust_brightness),
        "apply_beauty": bool_string(args.beauty_mode != "off"),
        "trim_head_tail": bool_string(args.trim_head_tail),
        "auto_center": bool_string(args.auto_center),
        "stabilize": bool_string(args.stabilize),
        "denoise_audio": bool_string(args.denoise_audio),
        "min_pause_duration": str(args.min_pause_duration),
        "breath_sensitivity": str(args.breath_sensitivity),
        "brightness_mode": "auto" if args.adjust_brightness else "off",
        "beauty_mode": args.beauty_mode,
        "beauty_strength": str(args.beauty_strength),
        "crossfade_duration": str(args.crossfade_duration),
        "auto_start": "true",
    }

    body, boundary = build_multipart(data, video)
    return http_json(
        "POST",
        api_url(args.base_url, "/rough-cuts"),
        body=body,
        content_type=f"multipart/form-data; boundary={boundary}",
        timeout=600,
    )


def get_job(base_url: str, job_id: str) -> dict:
    return http_json("GET", api_url(base_url, f"/rough-cuts/{job_id}"), timeout=30)


def get_decisions(base_url: str, job_id: str) -> dict:
    return http_json("GET", api_url(base_url, f"/rough-cuts/{job_id}/decisions"), timeout=30)


def download_output(base_url: str, job_id: str, output_path: Path) -> None:
    http_download(api_url(base_url, f"/rough-cuts/{job_id}/download"), output_path, timeout=600)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        job = submit_job(args)
    except Exception as exc:
        print(f"[rough-cut] submit failed: {exc}", file=sys.stderr)
        return 1

    job_id = job["id"]
    print(f"[rough-cut] created job: {job_id}")
    print(f"[rough-cut] status: {job.get('status')} progress={job.get('progress')}")

    if not args.wait:
        return 0

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        try:
            job = get_job(args.base_url, job_id)
        except Exception as exc:
            print(f"[rough-cut] poll failed: {exc}", file=sys.stderr)
            time.sleep(args.poll_interval)
            continue

        status = job.get("status")
        progress = int(round(float(job.get("progress", 0)) * 100))
        message = job.get("progress_message") or ""
        print(f"[rough-cut] {status} {progress}% {message}")

        if status == "completed":
            if args.show_decisions:
                decisions = get_decisions(args.base_url, job_id)
                print(json.dumps(decisions, ensure_ascii=False, indent=2))
            if args.download:
                output = Path(args.output) if args.output else Path(args.video).with_name(f"{Path(args.video).stem}_rough_cut.mp4")
                download_output(args.base_url, job_id, output)
                print(f"[rough-cut] downloaded to: {output}")
            return 0

        if status in {"failed", "cancelled"}:
            print(json.dumps(job, ensure_ascii=False, indent=2), file=sys.stderr)
            return 2

        if status not in PROCESSING_STATUSES and status != "uploaded":
            print(json.dumps(job, ensure_ascii=False, indent=2))
            return 0

        time.sleep(args.poll_interval)

    print("[rough-cut] timeout waiting for completion", file=sys.stderr)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
