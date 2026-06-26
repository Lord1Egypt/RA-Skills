#!/usr/bin/env python3
"""Wellness push helper.

This script builds (or reads) a rendered digest message and prints it.
Optionally, it can emit an OpenClaw `message` tool call template for an agent
(or a human) to send to a target channel.

Why template instead of sending directly?
- Skill scripts are channel-agnostic and don’t have direct access to OpenClaw’s
  message routing in-process.

Usage:

  # Build + print digest (from inputs and/or bridge)
  python3 scripts/wellness_push.py --date today --use-bridge --in /tmp/whoop_today.json

  # Print a message-tool template for sending
  python3 scripts/wellness_push.py --date today --use-bridge \
    --send-channel discord --send-target "#wellness" \
    --render markdown --channel discord

No third-party deps.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime


def run_digest(args: argparse.Namespace) -> str:
    cmd = [
        sys.executable,
        "scripts/wellness_digest.py",
        "--date",
        args.date,
        "--tz",
        args.tz,
        "--render",
        args.render,
        "--channel",
        args.channel,
    ]

    for p in args.inputs:
        cmd += ["--in", p]
    if args.use_bridge:
        cmd += ["--use-bridge", "--bridge-dir", args.bridge_dir]
    if args.out:
        cmd += ["--out", args.out]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise SystemExit(res.stderr.strip() or "wellness_digest failed")
    return res.stdout


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--tz", default="Asia/Shanghai")
    ap.add_argument("--in", dest="inputs", action="append", default=[])
    ap.add_argument("--use-bridge", action="store_true")
    ap.add_argument("--bridge-dir", default="~/.config/openclaw/wellness/bridge")
    ap.add_argument("--out", default=None)
    ap.add_argument("--render", choices=["text", "markdown"], default="markdown")
    ap.add_argument("--channel", default="generic", help="formatting preset")

    # Optional: emit a message-tool template
    ap.add_argument("--send-channel", default=None, help="discord|slack|telegram|whatsapp|... (OpenClaw message tool channel)")
    ap.add_argument("--send-target", default=None, help="channel/user id/name depending on provider")

    args = ap.parse_args()
    args.bridge_dir = args.bridge_dir.replace("~", "{HOME}")
    args.bridge_dir = args.bridge_dir.format(HOME=str(__import__("os").path.expanduser("~")))

    msg = run_digest(args).strip() + "\n"
    print(msg, end="")

    if args.send_channel and args.send_target:
        template = {
            "action": "send",
            "channel": args.send_channel,
            "target": args.send_target,
            "message": msg,
        }
        print("\n---\nOpenClaw message tool template (paste into an agent instruction):\n")
        print(json.dumps(template, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
