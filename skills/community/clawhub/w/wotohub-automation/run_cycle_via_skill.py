#!/usr/bin/env python3
"""Safe scheduled-cycle wrapper for OpenClaw cron / agent runs.

Purpose:
- avoid complex inline JSON / heavy shell quoting in cron-generated commands
- keep scheduled execution on the canonical `wotohub_skill.py` entrypoint
- make OpenClaw security policy more likely to allow the command
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))
from router_launcher_env import ensure_router_executor_env

SKILL_ENTRY = ROOT / "wotohub_skill.py"


def _load_json_file(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"JSON file must contain an object: {path}")
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description="Run WotoHub campaign/cycle through canonical skill entrypoint")
    ap.add_argument("--campaign-id", required=True)
    ap.add_argument("--brief-path", required=True)
    ap.add_argument("--mode", default="scheduled_cycle", choices=["single_cycle", "scheduled_cycle"])
    ap.add_argument("--send-policy", default=None)
    ap.add_argument("--token", default=None)
    ap.add_argument("--config-json", help="Inline JSON object merged into config")
    ap.add_argument("--config-path", help="JSON file merged into config")
    ap.add_argument("--metadata-path", help="Optional metadata JSON file")
    ap.add_argument("--output", help="Optional file to write JSON response")
    args = ap.parse_args()

    config = _load_json_file(args.config_path)
    if args.config_json:
        inline = json.loads(args.config_json)
        if not isinstance(inline, dict):
            raise ValueError("--config-json must be a JSON object")
        config.update(inline)
    config.setdefault("mode", args.mode)
    if args.send_policy:
        config["sendPolicy"] = args.send_policy

    req: dict[str, Any] = {
        "requestId": f"cycle-{args.campaign_id}",
        "action": "campaign",
        "type": "cycle",
        "input": {
            "campaignId": args.campaign_id,
            "briefPath": args.brief_path,
        },
        "config": config,
    }
    if args.token:
        req["auth"] = {"token": args.token}
    metadata = _load_json_file(args.metadata_path)
    if metadata:
        req["metadata"] = metadata

    env = ensure_router_executor_env(skill_root=ROOT, env=None)
    proc = subprocess.run(
        [sys.executable, str(SKILL_ENTRY)],
        input=json.dumps(req, ensure_ascii=False),
        text=True,
        capture_output=True,
        check=False,
        cwd=str(ROOT),
        env=env,
    )

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    if proc.returncode != 0:
        if stderr:
            print(stderr, file=sys.stderr)
        if stdout:
            print(stdout, file=sys.stderr)
        return proc.returncode or 1

    if args.output:
        Path(args.output).write_text(stdout + ("\n" if stdout else ""), encoding="utf-8")
    if stdout:
        print(stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
