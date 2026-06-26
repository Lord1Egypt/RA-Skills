#!/usr/bin/env python3
"""Create a sanitized external evidence card skeleton for SOTA review."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from sota_public_safety import sanitize_alias, sanitize_url


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Path to the output JSON file.")
    parser.add_argument("--target-url", required=True, help="External evidence URL.")
    parser.add_argument("--tool", default="external", help="Evidence source label.")
    parser.add_argument("--browser-alias", default="", help="Sanitized source alias.")
    parser.add_argument("--session-alias", default="", help="Sanitized session alias.")
    parser.add_argument("--requested-mode", default="", help="Requested model or notebook mode.")
    parser.add_argument("--runtime-type", default="", help="Requested runtime type such as T4 or A100.")
    parser.add_argument("--timeout-seconds", type=int, default=0, help="Primary execution timeout.")
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    target_info = sanitize_url(args.target_url, allow_raw=False)

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "browser": {
            "tool": args.tool,
            "browser_alias": sanitize_alias(args.browser_alias, label="browser-alias"),
            "session_alias": sanitize_alias(args.session_alias, label="session-alias"),
            "attach_status": "",
            "requested_mode": args.requested_mode,
            "actual_mode": "",
        },
        "target": {
            "url": target_info["url"],
            "target_host": target_info["target_host"],
            "target_kind": target_info["target_kind"],
            "target_label": target_info["target_label"],
            "url_redacted": target_info["url_redacted"],
            "page_title": "",
            "runtime_type": args.runtime_type,
        },
        "execution": {
            "timeout_seconds": args.timeout_seconds,
            "readiness_probe": "",
            "success_marker": "",
            "temporary_cell_used": False,
        },
        "evidence": {
            "screenshots": [],
            "downloads": [],
            "artifact_manifest_path": "",
            "validation_scorecard_path": "",
            "local_pull_status": "",
        },
        "outcome": {
            "status": "pending",
            "reason": "",
        },
    }

    out_path.write_text(f"{json.dumps(payload, indent=2)}\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
