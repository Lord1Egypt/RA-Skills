#!/usr/bin/env python3
"""Generate a video through the existing Ark HTTP + polling workflow."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request


DEFAULT_MODEL = "doubao-seedance-1-5-pro-251215"
DEFAULT_TASKS_URL = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
API_KEY_CANDIDATES = ("ARK_API_KEY", "VOLCENGINE_ARK_API_KEY", "ARK API KEY")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate video with Volcengine Ark task polling")
    parser.add_argument("--prompt", required=True, help="Final prompt to submit")
    parser.add_argument("--output", help="Output mp4 path")
    parser.add_argument("--api-key", help="Ark API key, otherwise read from environment")
    parser.add_argument("--model", default=os.environ.get("ARK_VIDEO_MODEL", DEFAULT_MODEL), help="Model name")
    parser.add_argument(
        "--tasks-url",
        default=os.environ.get("ARK_VIDEO_TASKS_URL", DEFAULT_TASKS_URL),
        help="Task endpoint URL",
    )
    parser.add_argument("--poll-interval", type=float, default=2.0, help="Polling interval in seconds")
    parser.add_argument("--timeout", type=int, default=300, help="Max wait time in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Print payload without sending the request")
    return parser.parse_args()


def read_windows_env_registry() -> str | None:
    if os.name != "nt":
        return None

    try:
        import winreg
    except ImportError:
        return None

    registry_paths = (
        (winreg.HKEY_CURRENT_USER, r"Environment"),
        (winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
    )

    for root, path in registry_paths:
        try:
            with winreg.OpenKey(root, path) as key:
                for name in API_KEY_CANDIDATES:
                    try:
                        value, _value_type = winreg.QueryValueEx(key, name)
                    except FileNotFoundError:
                        continue
                    if value:
                        return value
        except OSError:
            continue

    return None


def resolve_api_key(explicit_key: str | None) -> str:
    api_key = explicit_key
    if not api_key:
        for name in API_KEY_CANDIDATES:
            api_key = os.environ.get(name)
            if api_key:
                break
    if not api_key:
        api_key = read_windows_env_registry()
    if not api_key:
        raise SystemExit(
            "Missing API key. Set ARK_API_KEY or VOLCENGINE_ARK_API_KEY, "
            "or pass --api-key."
        )
    return api_key


def request_json(method: str, url: str, api_key: str, data: dict | None = None) -> dict:
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {api_key}")
    payload = None
    if data is not None:
        payload = json.dumps(data).encode("utf-8")

    try:
        with urllib.request.urlopen(req, data=payload) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc

    return json.loads(body)


def extract_task_id(task_payload: dict) -> str | None:
    return task_payload.get("id") or task_payload.get("data", {}).get("id")


def extract_video_url(payload: object) -> str | None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in ("url", "video_url") and isinstance(value, str) and value.startswith("http"):
                return value
            nested = extract_video_url(value)
            if nested:
                return nested
    elif isinstance(payload, list):
        for item in payload:
            nested = extract_video_url(item)
            if nested:
                return nested
    return None


def default_output_path(task_id: str) -> str:
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    return os.path.join(desktop, f"ark_video_{task_id}.mp4")


def download_file(url: str, output_path: str) -> None:
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    urllib.request.urlretrieve(url, output_path)


def main() -> None:
    args = parse_args()
    payload = {
        "model": args.model,
        "content": [{"type": "text", "text": args.prompt}],
    }

    if args.dry_run:
        print(json.dumps({"status": "dry_run", "payload": payload}, ensure_ascii=False, indent=2))
        return

    api_key = resolve_api_key(args.api_key)

    try:
        task_payload = request_json("POST", args.tasks_url, api_key, payload)
        task_id = extract_task_id(task_payload)
        if not task_id:
            raise RuntimeError(f"Task created without id: {json.dumps(task_payload, ensure_ascii=False)}")

        start_time = time.time()
        last_status_payload = None

        while True:
            last_status_payload = request_json("GET", f"{args.tasks_url}/{task_id}", api_key)
            status = (
                last_status_payload.get("status")
                or last_status_payload.get("data", {}).get("status")
                or ""
            ).lower()

            if status in ("succeeded", "success", "completed"):
                break
            if status in ("failed", "error"):
                raise RuntimeError(
                    f"Remote task failed: {json.dumps(last_status_payload, ensure_ascii=False)}"
                )
            if time.time() - start_time > args.timeout:
                raise RuntimeError(
                    f"Polling timed out after {args.timeout}s: {json.dumps(last_status_payload, ensure_ascii=False)}"
                )
            time.sleep(args.poll_interval)

        video_url = extract_video_url(last_status_payload)
        if not video_url:
            raise RuntimeError(
                f"Task succeeded but no video url was found: {json.dumps(last_status_payload, ensure_ascii=False)}"
            )

        output_path = args.output or default_output_path(task_id)
        download_file(video_url, output_path)
        result = {
            "status": "succeeded",
            "task_id": task_id,
            "output_path": output_path,
            "video_url": video_url,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
