#!/usr/bin/env python3
"""
Query workflow execution status.

Usage:
    python3 query_workflow.py INSTANCE_ID [--poll] [--interval 3] [--timeout 300]

Output (JSON):
    {
      "instance_id": "...",
      "status": "completed",
      "progress": 1.0,
      "completed_nodes": 5,
      "total_nodes": 5
    }
"""

import argparse
import json
import sys
import os
import time
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
from _common import require_access_key, _cookie_header, GO_API_PREFIX


def query_status_sse(instance_id: str, timeout: int = 30) -> dict:
    """Query workflow status via SSE endpoint (single request)."""
    url = f"{GO_API_PREFIX}/wf/instance/{instance_id}/status_sse"
    req = urllib.request.Request(url, headers={
        "Cookie": _cookie_header(),
        "Accept": "text/event-stream",
    })

    last_status = {}
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            buffer = ""
            while True:
                chunk = resp.read(4096)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8")
                # Parse SSE events
                while "\n\n" in buffer:
                    event_str, buffer = buffer.split("\n\n", 1)
                    for line in event_str.split("\n"):
                        if line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                last_status = data
                                # If completed or failed, we're done
                                status = data.get("status", "")
                                if status in ("completed", "failed", "cancelled"):
                                    return last_status
                            except json.JSONDecodeError:
                                pass
    except Exception:
        pass

    return last_status


def format_status(data: dict) -> dict:
    return {
        "instance_id": data.get("instance_id", ""),
        "status": data.get("status", "unknown"),
        "progress": data.get("progress", 0),
        "total_nodes": data.get("total_nodes", 0),
        "completed_nodes": data.get("completed_nodes", 0),
        "failed_nodes": data.get("failed_nodes", 0),
        "running_nodes": data.get("running_nodes", 0),
    }


def main():
    parser = argparse.ArgumentParser(description="Query workflow status")
    parser.add_argument("instance_id", help="Workflow instance ID")
    parser.add_argument("--poll", action="store_true", help="Poll until complete")
    parser.add_argument("--interval", type=int, default=3, help="Poll interval in seconds (default 3)")
    parser.add_argument("--timeout", type=int, default=300, help="Max poll time in seconds (default 300)")
    args = parser.parse_args()

    require_access_key()

    if args.poll:
        start = time.time()
        while (time.time() - start) < args.timeout:
            status = query_status_sse(args.instance_id, timeout=args.interval + 5)
            result = format_status(status)
            if result["status"] in ("completed", "failed", "cancelled"):
                print(json.dumps(result, indent=2))
                return
            # Print progress to stderr for live feedback
            print(
                f"[{result['status']}] progress={result['progress']:.0%} "
                f"({result['completed_nodes']}/{result['total_nodes']} nodes)",
                file=sys.stderr,
            )
            time.sleep(args.interval)

        # Timeout
        result = format_status(status)
        result["warning"] = "Polling timed out"
        print(json.dumps(result, indent=2))
    else:
        status = query_status_sse(args.instance_id)
        print(json.dumps(format_status(status), indent=2))


if __name__ == "__main__":
    main()
