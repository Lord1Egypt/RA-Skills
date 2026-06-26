#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
import sys
import time

import requests

BASE_URL = "https://open.vectcut.com"
SUBMIT_PATH = "/process/extract_audio/submit_task/submit_extract_audio_task"
STATUS_PATH = "/process/extract_audio/submit_task/task_status"
DONE_STATUSES = {"success", "failed"}


def _auth_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }


def _ensure_token():
    token = os.environ.get("VECTCUT_API_KEY")
    if not token:
        raise RuntimeError(
            "Environment variable VECTCUT_API_KEY is not set. "
            "Please call the vectcut-login skill first."
        )
    return token


def _validate_video_url(video_url):
    if not isinstance(video_url, str) or not video_url.startswith(("http://", "https://")):
        raise RuntimeError("video_url must be a valid http/https link.")


def _parse_json_response(resp):
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text}")


def _normalize_public_url(url):
    if not isinstance(url, str):
        return ""
    fixed = url.strip()
    if fixed.startswith("http://http://"):
        return "http://" + fixed[len("http://http://") :]
    if fixed.startswith("https://https://"):
        return "https://" + fixed[len("https://https://") :]
    return fixed


def submit_task(token, video_url):
    resp = requests.post(
        f"{BASE_URL}{SUBMIT_PATH}",
        headers=_auth_headers(token),
        json={"video_url": video_url},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))
    task_id = body.get("task_id")
    if not task_id:
        raise RuntimeError(f"submit response missing task_id: {body}")
    return body


def query_task_status(token, task_id):
    resp = requests.get(
        f"{BASE_URL}{STATUS_PATH}",
        headers=_auth_headers(token),
        params={"task_id": task_id},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    return body


def wait_until_done(token, task_id, poll_interval, timeout):
    started = time.monotonic()
    while True:
        status_body = query_task_status(token, task_id)
        status = status_body.get("status")
        if status in DONE_STATUSES:
            return status_body

        elapsed = time.monotonic() - started
        if elapsed >= timeout:
            raise RuntimeError(
                f"Polling timeout after {timeout}s. Last status={status!r}, body={status_body}"
            )
        time.sleep(poll_interval)


def run(video_url, poll_interval=2.0, timeout=600):
    token = _ensure_token()
    _validate_video_url(video_url)
    submit_body = submit_task(token, video_url)
    status_body = wait_until_done(
        token, submit_body["task_id"], poll_interval=poll_interval, timeout=timeout
    )
    if status_body.get("status") != "success":
        raise RuntimeError(f"extract-audio task failed: {status_body}")

    result = status_body.get("result") or {}
    public_url = _normalize_public_url(result.get("public_url", ""))
    if not public_url:
        raise RuntimeError(f"extract-audio success but missing public_url: {status_body}")

    return {
        "success": True,
        "meta": {
            "source_video_url": video_url,
            "task_id": submit_body.get("task_id"),
            "message_id": submit_body.get("message_id"),
            "status": status_body.get("status"),
            "progress": status_body.get("progress"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "audio": {
            "public_url": public_url,
            "raw_result": result,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_url")
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=600.0)
    parser.add_argument("--output", default="extracted_audio.json")
    args = parser.parse_args()

    try:
        result = run(
            video_url=args.video_url,
            poll_interval=args.poll_interval,
            timeout=args.timeout,
        )
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
