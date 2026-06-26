#!/usr/bin/env python3
"""
Execute YumFu daily evolution delivery with low freedom.

This script does not call message tools itself, but it produces a deterministic,
ready-to-follow execution bundle so cron/agent turns stop improvising the last mile.

Workflow:
1. load the daily evolution JSON
2. run prepare_daily_evolution_delivery.py
3. emit exact send instructions for image/text/voice
4. emit exact mark-state commands
5. emit exact sidecar-apply command
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
PREPARE = SCRIPT_DIR / "prepare_daily_evolution_delivery.py"
TURN_STATE = SCRIPT_DIR / "turn_delivery_state.py"
APPLY = SCRIPT_DIR / "run_daily_evolution.py"


def run_json(cmd: list[str]) -> dict[str, Any]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        return {
            "success": False,
            "error": proc.stderr.strip() or proc.stdout.strip() or f"command failed ({proc.returncode})",
            "command": cmd,
        }
    stdout = proc.stdout.strip()
    if not stdout:
        return {"success": False, "error": "empty stdout", "command": cmd}
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "stdout was not valid JSON",
            "stdout": stdout,
            "command": cmd,
        }


def mark_cmd(user_id: str, universe: str, turn_id: str, mark: str) -> list[str]:
    return [
        "python3",
        str(TURN_STATE),
        "--user-id",
        user_id,
        "--universe",
        universe,
        "--turn-id",
        turn_id,
        "--mark",
        mark,
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute YumFu daily evolution delivery planning")
    parser.add_argument("--user-id", required=True)
    parser.add_argument("--universe", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--json", dest="json_path", required=True)
    parser.add_argument("--channel", default="telegram")
    args = parser.parse_args()

    prepare = run_json([
        "python3",
        str(PREPARE),
        "--user-id",
        args.user_id,
        "--universe",
        args.universe,
        "--target",
        args.target,
        "--json",
        args.json_path,
    ])
    if not prepare.get("success"):
        print(json.dumps(prepare, ensure_ascii=False))
        sys.exit(1)

    turn_id = prepare["turn_id"]
    story = prepare["story"]
    image = prepare["image"]
    tts = prepare["tts"]
    next_actions = prepare["next_actions"]

    sends: list[dict[str, Any]] = []
    marks: list[list[str]] = []

    if next_actions.get("send_image_with_caption") and image.get("path"):
        sends.append({
            "kind": "image_with_caption",
            "channel": args.channel,
            "target": args.target,
            "media": image["path"],
            "message": story["caption"],
            "mark_after_success": "image_sent",
        })
        if next_actions.get("mark_image_sent_after_success"):
            marks.append(mark_cmd(args.user_id, args.universe, turn_id, "image_sent"))
        if next_actions.get("mark_main_text_sent_after_success"):
            marks.append(mark_cmd(args.user_id, args.universe, turn_id, "main_text_sent"))
    else:
        sends.append({
            "kind": "text_only",
            "channel": args.channel,
            "target": args.target,
            "message": story["full_text"],
            "mark_after_success": "main_text_sent",
        })
        if next_actions.get("mark_main_text_sent_after_success"):
            marks.append(mark_cmd(args.user_id, args.universe, turn_id, "main_text_sent"))

    if next_actions.get("send_text_followup") and story.get("followup_text"):
        sends.append({
            "kind": "text_followup",
            "channel": args.channel,
            "target": args.target,
            "message": story["followup_text"],
        })

    if next_actions.get("send_tts_voice") and tts.get("path"):
        sends.append({
            "kind": "voice_bubble",
            "channel": args.channel,
            "target": args.target,
            "media": tts["path"],
            "asVoice": True,
            "mark_after_success": "tts_sent",
        })
        if next_actions.get("mark_tts_sent_after_success"):
            marks.append(mark_cmd(args.user_id, args.universe, turn_id, "tts_sent"))

    apply_cmd = [
        "python3",
        str(APPLY),
        "--user-id",
        args.user_id,
        "--universe",
        args.universe,
        "--apply-from-json",
        args.json_path,
    ]

    result = {
        "success": True,
        "kind": "daily-evolution-execution-plan",
        "prepare": prepare,
        "turn_id": turn_id,
        "sends": sends,
        "mark_commands": marks,
        "apply_command": apply_cmd,
        "notes": [
            "send in listed order",
            "run matching mark command only after each successful send",
            "run apply_command after delivery steps complete",
        ],
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
