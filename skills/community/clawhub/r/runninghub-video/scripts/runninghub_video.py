#!/usr/bin/env python3
"""Submit RunningHub image-to-video tasks, poll status, and download outputs."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Callable


API_BASE = "https://www.runninghub.cn"
UPLOAD_ENDPOINT = f"{API_BASE}/openapi/v2/media/upload/binary"
QUERY_ENDPOINT = f"{API_BASE}/openapi/v2/query"

RUNNING_STATUSES = {"RUNNING", "PENDING", "PROCESSING", "QUEUED", "WAITING", "SUBMITTED"}
SUCCESS_STATUSES = {"SUCCESS", "SUCCEEDED", "COMPLETED", "DONE"}
FAILURE_STATUSES = {"FAILED", "ERROR", "CANCELLED", "REJECTED"}


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered in {"1", "true", "yes", "y", "on"}:
        return True
    if lowered in {"0", "false", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Unsupported boolean value: {value}")


def load_api_key(cli_value: str | None) -> str:
    if cli_value:
        return cli_value

    env_value = os.environ.get("RUNNINGHUB_API_KEY")
    if env_value:
        return env_value

    if os.name == "nt":
        try:
            import winreg

            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
                value, _ = winreg.QueryValueEx(key, "RUNNINGHUB_API_KEY")
                if value:
                    return value
        except OSError:
            pass

    raise SystemExit(
        "Missing API key. Pass --api-key or set RUNNINGHUB_API_KEY in the user environment."
    )


def request_json(
    url: str,
    *,
    method: str = "POST",
    payload: dict | None = None,
    headers: dict[str, str] | None = None,
    data: bytes | None = None,
    timeout: int = 180,
) -> dict:
    request_headers = {"Accept": "application/json"}
    if headers:
        request_headers.update(headers)

    request_data = data
    if payload is not None:
        request_data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request_headers.setdefault("Content-Type", "application/json")

    request = urllib.request.Request(url, data=request_data, headers=request_headers, method=method)

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"HTTP {exc.code} calling {url}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Network error calling {url}: {exc}") from exc

    text = raw.decode("utf-8", errors="replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Expected JSON from {url}, got:\n{text}") from exc


def encode_multipart(file_path: Path) -> tuple[bytes, str]:
    boundary = f"----runninghub-{uuid.uuid4().hex}"
    mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    file_bytes = file_path.read_bytes()

    chunks: list[bytes] = []
    chunks.append(f"--{boundary}\r\n".encode("utf-8"))
    chunks.append(
        (
            f'Content-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'
            f"Content-Type: {mime_type}\r\n\r\n"
        ).encode("utf-8")
    )
    chunks.append(file_bytes)
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))

    return b"".join(chunks), f"multipart/form-data; boundary={boundary}"


def upload_file(api_key: str, value: str) -> str:
    if value.startswith(("http://", "https://", "data:")):
        return value

    file_path = Path(value).expanduser().resolve()
    if not file_path.is_file():
        raise SystemExit(f"Input file does not exist: {file_path}")

    body, content_type = encode_multipart(file_path)
    response = request_json(
        UPLOAD_ENDPOINT,
        method="POST",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": content_type,
        },
    )

    data = response.get("data") or {}
    upload_url = data.get("download_url") or data.get("downloadUrl")
    if not upload_url:
        raise SystemExit(
            "Upload succeeded but no download URL was returned:\n"
            f"{json.dumps(response, ensure_ascii=False, indent=2)}"
        )

    print(f"[upload] {file_path} -> {upload_url}")
    return upload_url


def build_kling_payload(args: argparse.Namespace, first_url: str, end_url: str | None) -> dict:
    payload = {
        "prompt": args.prompt,
        "firstImageUrl": first_url,
        "duration": args.duration,
        "cfgScale": args.cfg_scale,
        "sound": args.sound,
        "multiShot": args.multi_shot,
        "shotType": args.shot_type,
    }
    if end_url:
        payload["lastImageUrl"] = end_url
    return payload


def build_seedance_payload(args: argparse.Namespace, first_url: str, end_url: str | None) -> dict:
    payload = {
        "prompt": args.prompt,
        "resolution": args.resolution,
        "duration": args.duration,
        "firstFrameUrl": first_url,
        "generateAudio": args.audio,
        "ratio": args.ratio,
        "realPersonMode": args.real_person_mode,
        "conversionSlots": ["all"],
        "returnLastFrame": args.return_last_frame,
    }
    if end_url:
        # This field name is inferred from RunningHub's start/end-frame description for Seedance.
        payload["lastFrameUrl"] = end_url
    return payload


def build_wan_payload(args: argparse.Namespace, first_url: str, _end_url: str | None) -> dict:
    return {
        "imageUrl": first_url,
        "prompt": args.prompt,
        "duration": str(args.duration),
        "resolution": args.wan_resolution,
    }


def model_spec(model_name: str) -> tuple[str, Callable[[argparse.Namespace, str, str | None], dict]]:
    normalized = model_name.strip().lower()
    aliases = {
        "kling": "kling-v3.0-std",
        "seedance": "seedance-2.0-global",
        "seedance-fast": "seedance-2.0-global-fast",
        "wan": "wan-2.2",
    }
    normalized = aliases.get(normalized, normalized)

    registry = {
        "kling-v3.0-std": (
            f"{API_BASE}/openapi/v2/kling-v3.0-std/image-to-video",
            build_kling_payload,
        ),
        "seedance-2.0-global": (
            f"{API_BASE}/openapi/v2/bytedance/seedance-2.0-global/image-to-video",
            build_seedance_payload,
        ),
        "seedance-2.0-global-fast": (
            f"{API_BASE}/openapi/v2/bytedance/seedance-2.0-global-fast/image-to-video",
            build_seedance_payload,
        ),
        "wan-2.2": (
            f"{API_BASE}/openapi/v2/rhart-video/wan-2.2/image-to-video",
            build_wan_payload,
        ),
    }

    if normalized not in registry:
        supported = ", ".join(sorted(registry))
        raise SystemExit(f"Unsupported model '{model_name}'. Supported models: {supported}")
    return registry[normalized]


def submit_task(api_key: str, endpoint: str, payload: dict) -> dict:
    response = request_json(
        endpoint,
        method="POST",
        payload=payload,
        headers={"Authorization": f"Bearer {api_key}"},
    )
    if response.get("errorMessage") and not response.get("taskId"):
        raise SystemExit(json.dumps(response, ensure_ascii=False, indent=2))
    return response


def query_task(api_key: str, task_id: str) -> dict:
    return request_json(
        QUERY_ENDPOINT,
        method="POST",
        payload={"taskId": task_id},
        headers={"Authorization": f"Bearer {api_key}"},
    )


def wait_for_task(api_key: str, task_id: str, poll_interval: int, timeout: int) -> dict:
    started_at = time.time()
    while True:
        result = query_task(api_key, task_id)
        status = str(result.get("status", "")).upper()
        print(f"[poll] taskId={task_id} status={status or 'UNKNOWN'}")

        if status in SUCCESS_STATUSES:
            return result
        if status in FAILURE_STATUSES:
            raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2))

        if time.time() - started_at > timeout:
            raise SystemExit(f"Timed out after {timeout}s waiting for task {task_id}")

        if status not in RUNNING_STATUSES and result.get("results"):
            return result

        time.sleep(poll_interval)


def guess_extension(item: dict, index: int) -> str:
    output_type = item.get("outputType")
    if output_type:
        suffix = str(output_type).strip().lstrip(".")
        return suffix or "bin"

    parsed = urllib.parse.urlparse(str(item.get("url", "")))
    name = Path(parsed.path).name
    suffix = Path(name).suffix.lstrip(".")
    if suffix:
        return suffix
    return "mp4" if index == 0 else "bin"


def download_result(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "runninghub-video-skill"})
    try:
        with urllib.request.urlopen(request, timeout=300) as response, destination.open("wb") as handle:
            handle.write(response.read())
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Download failed with HTTP {exc.code} for {url}\n{body}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Download failed for {url}: {exc}") from exc


def save_outputs(result: dict, out_dir: Path) -> list[Path]:
    results = result.get("results") or []
    if not results:
        raise SystemExit(
            "Task finished but no results were returned:\n"
            f"{json.dumps(result, ensure_ascii=False, indent=2)}"
        )

    out_dir.mkdir(parents=True, exist_ok=True)
    task_id = result.get("taskId", "runninghub-task")
    saved_paths: list[Path] = []

    for index, item in enumerate(results):
        url = item.get("url")
        if not url:
            continue
        extension = guess_extension(item, index)
        destination = out_dir / f"{task_id}-{index + 1}.{extension}"
        download_result(str(url), destination)
        saved_paths.append(destination)
        print(f"[download] {url} -> {destination}")

    if not saved_paths:
        raise SystemExit(f"No downloadable URLs were found:\n{json.dumps(result, ensure_ascii=False, indent=2)}")
    return saved_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="wan-2.2")
    parser.add_argument("--image", required=True, help="Local path, public URL, or data URI for the first frame.")
    parser.add_argument("--end-image", help="Optional local path, public URL, or data URI for the ending frame.")
    parser.add_argument("--prompt", required=True, help="Motion/camera description.")
    parser.add_argument("--api-key", help="RunningHub API key. Defaults to RUNNINGHUB_API_KEY.")
    parser.add_argument("--out-dir", default=str(Path.cwd() / "runninghub-output"))
    parser.add_argument("--duration", default="5")
    parser.add_argument("--poll-interval", type=int, default=8)
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--submit-only", action="store_true")

    parser.add_argument("--cfg-scale", type=float, default=0.8)
    parser.add_argument("--sound", type=parse_bool, default=True)
    parser.add_argument("--multi-shot", type=parse_bool, default=False)
    parser.add_argument("--shot-type", default="customize")

    parser.add_argument("--resolution", default="720p")
    parser.add_argument("--ratio", default="adaptive")
    parser.add_argument("--audio", type=parse_bool, default=True)
    parser.add_argument("--real-person-mode", type=parse_bool, default=True)
    parser.add_argument("--return-last-frame", type=parse_bool, default=False)

    parser.add_argument("--wan-resolution", default="auto")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    api_key = load_api_key(args.api_key)
    endpoint, payload_builder = model_spec(args.model)

    first_url = upload_file(api_key, args.image)
    end_url = upload_file(api_key, args.end_image) if args.end_image else None
    payload = payload_builder(args, first_url, end_url)

    print(f"[submit] model={args.model} endpoint={endpoint}")
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    submit_response = submit_task(api_key, endpoint, payload)
    task_id = submit_response.get("taskId")
    if not task_id:
        raise SystemExit(
            "RunningHub did not return a taskId:\n"
            f"{json.dumps(submit_response, ensure_ascii=False, indent=2)}"
        )

    print(f"[task] taskId={task_id} status={submit_response.get('status', '')}")
    if args.submit_only:
        print(json.dumps(submit_response, ensure_ascii=False, indent=2))
        return 0

    if str(submit_response.get("status", "")).upper() in SUCCESS_STATUSES and submit_response.get("results"):
        final_result = submit_response
    else:
        final_result = wait_for_task(api_key, task_id, args.poll_interval, args.timeout)

    saved = save_outputs(final_result, Path(args.out_dir).expanduser().resolve())
    print(json.dumps({"taskId": task_id, "saved": [str(path) for path in saved]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
