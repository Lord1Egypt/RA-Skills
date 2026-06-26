#!/usr/bin/env python3
"""
Query Vidau video task status and result. Reads API key from env VIDAU_API_KEY or OpenClaw config.
Prints API JSON to stdout; on success also prints [VIDAU_VIDEO_URL]..[/VIDAU_VIDEO_URL] and
[VIDAU_THUMB_PATH]..[/VIDAU_THUMB_PATH] blocks with raw URLs. When presenting succeeded results
to the user, copy video_url and thumb_path verbatim from those blocks (no rewriting).
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_client
from urllib.error import URLError

API_BASE = "https://api.superaiglobal.com/v1"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Query Vidau video task status and result. Requires env VIDAU_API_KEY."
    )
    parser.add_argument("--task-uuid", required=True, help="taskUUID from create task response")
    args = parser.parse_args()

    api_key = api_client.get_api_key()
    if not api_key:
        print(
            "Error: VIDAU_API_KEY is not set. Register at https://www.superaiglobal.com/ to get an API key, then configure apiKey or env.VIDAU_API_KEY in OpenClaw skills.entries.vidau.",
            file=sys.stderr,
        )
        sys.exit(1)

    url = f"{API_BASE}/queryTask/{args.task_uuid}/creations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        raw, _ = api_client.api_request("GET", url, headers=headers, timeout=30)
        raw_str = raw.decode("utf-8")
        print(raw_str)
        out = json.loads(raw_str)
        if out.get("code") == "404":
            msg = out.get("message", "")
            print(
                f"API returned 404 (task not found): message={msg}",
                file=sys.stderr,
            )
            print(
                f"[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid={args.task_uuid}",
                file=sys.stderr,
            )
            sys.exit(1)
        if out.get("code") != "200":
            msg = out.get("message", "")
            print(
                f"API returned non-success: code={out.get('code')}, message={msg}",
                file=sys.stderr,
            )
            sys.exit(1)
        data = out.get("data", {})
        status = (data or {}).get("taskStatus", "").lower()
        if status in ("succeeded", "failed"):
            msg = f"[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid={args.task_uuid}"
            print(msg, file=sys.stderr)
        if status == "succeeded":
            result = (data or {}).get("result") or {}
            if result.get("video_url"):
                print("[VIDAU_VIDEO_URL]")
                print(result["video_url"])
                print("[/VIDAU_VIDEO_URL]")
            if result.get("thumb_path"):
                print("[VIDAU_THUMB_PATH]")
                print(result["thumb_path"])
                print("[/VIDAU_THUMB_PATH]")
    except api_client.APIError as e:
        try:
            err_json = json.loads(e.body)
            msg = err_json.get("message", e.body)
            if err_json.get("code") == "404":
                print(
                    f"[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid={args.task_uuid}",
                    file=sys.stderr,
                )
        except Exception:
            msg = e.body or str(e)
        print(f"HTTP {e.code}: {msg}", file=sys.stderr)
        if e.code == 404:
            print(
                f"[OPENCLAW] DELETE_SCHEDULED_TASK task_uuid={args.task_uuid}",
                file=sys.stderr,
            )
        sys.exit(1)
    except URLError as e:
        print(f"Request failed: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Response is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
