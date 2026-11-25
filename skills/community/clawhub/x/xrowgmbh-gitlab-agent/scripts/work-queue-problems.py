#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Read-only discovery diagnostics. Output one JSON document on every outcome."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys


spec = importlib.util.spec_from_file_location("queue_report", Path(__file__).with_name("work-queue-report.py"))
queue = importlib.util.module_from_spec(spec)
spec.loader.exec_module(queue)
active = queue.active


def report():
    from datetime import datetime, timezone

    active.PROBLEMS.clear()
    # Use the bounded/captured reader from the read-only report. No assignment,
    # label synchronization, incident adoption or mutating main entrypoint.
    active.api_json = queue.read_api
    owner = active.configured_owner()
    user = active.api_json("user")
    if type(user.get("id")) is not int or not isinstance(user.get("username"), str):
        raise ValueError("Incomplete GitLab identity")
    result = {"generated_at": datetime.now(timezone.utc).isoformat()}
    for code, probe in (
        ("queue-scan-failed", queue.report),
        ("collaborator-scan-failed", lambda: active.assign_unassigned_items(
            user["id"], user["username"], owner, {}, dry_run=True)),
    ):
        try:
            probe()
        except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError) as error:
            active.record_problem(code)
            result["error_code"] = queue.failure_code(error)
    return {**result, "problems": list(active.PROBLEMS)}


def main():
    try:
        value = report()
    except (OSError, subprocess.SubprocessError, ValueError, KeyError, TypeError) as error:
        # No exception/response/configuration text enters the output.
        active.record_problem("discovery-failed")
        value = {"problems": list(active.PROBLEMS), "error_code": queue.failure_code(error)}
    print(json.dumps(value))
    return 0


if __name__ == "__main__":
    sys.exit(main())
