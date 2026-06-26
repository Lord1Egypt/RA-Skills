#!/usr/bin/env python3

import argparse
from datetime import datetime, timezone
import json
import os
import sys
import time

import requests

BASE_URL = "https://open.vectcut.com"
SUBMIT_PATH = "/process/remove_bg/submit_task/submit_remove_bg_text_behind_task"
DEFAULT_STATUS_PATH = "/process/remove_bg/submit_task/task_status"
DEFAULT_TEXT_PRESET_ID = "fc6982de-c94e-447a-82d0-ab361cb27217"
DONE_STATUSES = {"success", "failed", "not_found", "succeeded"}


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


def _parse_json_response(resp):
    try:
        return resp.json()
    except Exception:
        raise RuntimeError(f"Invalid JSON response: {resp.text}")


def _extract_status(body):
    status = str(body.get("status") or "").strip().lower()
    if status:
        return status
    result = body.get("result")
    if isinstance(result, dict):
        return str(result.get("status") or "").strip().lower()
    return ""


def _validate_payload(payload):
    if not isinstance(payload, dict):
        raise RuntimeError("Payload must be a JSON object.")

    video_url = payload.get("video_url")
    if not isinstance(video_url, str) or not video_url.startswith(("http://", "https://")):
        raise RuntimeError("video_url is required and must be a valid http/https URL.")

    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("text is required and must be a non-empty string.")

    text_preset_id = payload.get("text_preset_id")
    if text_preset_id is None or str(text_preset_id).strip() == "":
        payload["text_preset_id"] = DEFAULT_TEXT_PRESET_ID

    target_start = payload.get("target_start")
    if target_start is not None and not isinstance(target_start, (int, float)):
        raise RuntimeError("target_start must be a number when provided.")


def submit_task(token, payload):
    resp = requests.post(
        f"{BASE_URL}{SUBMIT_PATH}",
        headers=_auth_headers(token),
        json=payload,
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    if body.get("success") is False:
        raise RuntimeError(body.get("error") or str(body))
    task_id = body.get("task_id")
    if not task_id:
        raise RuntimeError(f"submit response missing task_id: {body}")
    return body


def query_task_status(token, task_id, status_path):
    resp = requests.get(
        f"{BASE_URL}{status_path}",
        headers=_auth_headers(token),
        params={"task_id": task_id},
        timeout=60,
    )
    body = _parse_json_response(resp)
    if resp.status_code != 200:
        raise RuntimeError(body.get("error") or str(body))
    return body


def wait_until_done(token, task_id, status_path, poll_interval, timeout):
    started = time.monotonic()
    while True:
        status_body = query_task_status(token, task_id, status_path=status_path)
        status = _extract_status(status_body)
        if status in DONE_STATUSES:
            return status_body
        if time.monotonic() - started >= timeout:
            raise RuntimeError(
                f"Polling timeout after {timeout}s. Last status={status!r}, body={status_body}"
            )
        time.sleep(poll_interval)


def run(payload, status_path=DEFAULT_STATUS_PATH, poll_interval=2.0, timeout=900):
    token = _ensure_token()
    _validate_payload(payload)
    submit_body = submit_task(token, payload)
    status_body = wait_until_done(
        token=token,
        task_id=submit_body["task_id"],
        status_path=status_path,
        poll_interval=poll_interval,
        timeout=timeout,
    )
    final_status = _extract_status(status_body)
    if final_status not in {"success", "succeeded"}:
        raise RuntimeError(f"text-background task failed: {status_body}")

    result = status_body.get("result")
    if not isinstance(result, dict):
        result = status_body

    return {
        "success": True,
        "meta": {
            "task_id": submit_body.get("task_id"),
            "message_id": submit_body.get("message_id"),
            "submit_status": submit_body.get("status"),
            "queue_name": submit_body.get("queue_name"),
            "final_status": final_status,
            "progress": status_body.get("progress"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "status_path": status_path,
        },
        "request_payload": payload,
        "result": {
            "draft_id": result.get("draft_id"),
            "draft_url": result.get("draft_url"),
            "mask_url": result.get("mask_url"),
            "inverted_mask_url": result.get("inverted_mask_url"),
            "purchase_link": result.get("purchase_link"),
            "video_url": status_body.get("video_url"),
            "raw_result": result,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Submit async text-background task and poll until done."
    )
    parser.add_argument(
        "payload_json",
        help="Path to request payload JSON for submit_remove_bg_text_behind_task",
    )
    parser.add_argument("--output", default="text_background_result.json")
    parser.add_argument("--poll-interval", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--status-path", default=DEFAULT_STATUS_PATH)
    args = parser.parse_args()

    try:
        with open(args.payload_json, "r", encoding="utf-8") as f:
            payload = json.load(f)
        result = run(
            payload=payload,
            status_path=args.status_path,
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
