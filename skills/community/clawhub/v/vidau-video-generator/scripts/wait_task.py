#!/usr/bin/env python3
"""
Wait for a Vidau video task to finish by polling queryTask. Reads API key from env VIDAU_API_KEY or OpenClaw config.
Prints final API JSON to stdout when task reaches succeeded/failed; on success also prints
[VIDAU_VIDEO_URL]..[/VIDAU_VIDEO_URL] and [VIDAU_THUMB_PATH]..[/VIDAU_THUMB_PATH] with raw URLs.
Exit code: 0 = succeeded, 1 = failed or API error, 2 = timeout.
"""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_client
from urllib.error import URLError

API_BASE = "https://api.superaiglobal.com/v1"


def query_task(api_key: str, task_uuid: str) -> dict:
    """Return full API response dict (code, message, data)."""
    url = f"{API_BASE}/queryTask/{task_uuid}/creations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    raw, _ = api_client.api_request("GET", url, headers=headers, timeout=30)
    out = json.loads(raw.decode("utf-8"))
    if out.get("code") != "200":
        raise RuntimeError(out.get("message", "API returned non-success"))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Wait for Vidau video task to finish. Requires env VIDAU_API_KEY."
    )
    parser.add_argument("--task-uuid", required=True, help="taskUUID from create task response")
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Poll interval in seconds (default 10)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Max wait time in seconds (default 600 = 10 min)",
    )
    args = parser.parse_args()

    api_key = api_client.get_api_key()
    if not api_key:
        print(
            "Error: VIDAU_API_KEY is not set. Register at https://www.superaiglobal.com/ to get an API key, then configure apiKey or env.VIDAU_API_KEY in OpenClaw skills.entries.vidau.",
            file=sys.stderr,
        )
        sys.exit(1)

    deadline = time.monotonic() + args.timeout
    last_out = None

    while time.monotonic() < deadline:
        try:
            out = query_task(api_key, args.task_uuid)
            data = out.get("data", out)
        except api_client.APIError as e:
            try:
                err_json = json.loads(e.body)
                msg = err_json.get("message", e.body)
            except Exception:
                msg = e.body or str(e)
            print(f"HTTP {e.code}: {msg}", file=sys.stderr)
            sys.exit(1)
        except URLError as e:
            print(f"Request failed: {e.reason}", file=sys.stderr)
            sys.exit(1)
        except (json.JSONDecodeError, RuntimeError) as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        status = (data or {}).get("taskStatus", "").lower()
        if status == "succeeded":
            print(json.dumps(out, ensure_ascii=False))
            result = (data or {}).get("result") or {}
            if result.get("video_url"):
                print("[VIDAU_VIDEO_URL]")
                print(result["video_url"])
                print("[/VIDAU_VIDEO_URL]")
            if result.get("thumb_path"):
                print("[VIDAU_THUMB_PATH]")
                print(result["thumb_path"])
                print("[/VIDAU_THUMB_PATH]")
            sys.exit(0)
        if status == "failed":
            print(json.dumps(out, ensure_ascii=False))
            print("Task ended with status failed.", file=sys.stderr)
            sys.exit(1)

        last_out = out
        time.sleep(args.interval)

    print(
        f"Timeout after {args.timeout}s. Last status: {(last_out.get('data', {}) if last_out else {}).get('taskStatus', 'unknown')}",
        file=sys.stderr,
    )
    if last_out is not None:
        print(json.dumps(last_out, ensure_ascii=False))
    sys.exit(2)


if __name__ == "__main__":
    main()
