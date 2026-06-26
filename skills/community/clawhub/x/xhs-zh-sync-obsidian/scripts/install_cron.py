#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import DEFAULT_CONFIG_PATH


def cron_expr(time_text: str) -> str:
    hour, minute = time_text.split(":", 1)
    return f"{int(minute)} {int(hour)} * * *"


def payload(platform: str, time_text: str, config: str, tz: str, skill_root: Path) -> dict:
    label = "小红书" if platform == "xhs" else "知乎"
    cmd = (
        f"cd {skill_root} && "
        f"python scripts/sync.py --config {config} --platform {platform} && "
        f"python scripts/export_obsidian.py --config {config} --platform {platform} --incremental"
    )
    return {
        "name": f"{label}收藏同步到Obsidian",
        "schedule": {"kind": "cron", "expr": cron_expr(time_text), "tz": tz},
        "sessionTarget": "isolated",
        "payload": {
            "kind": "agentTurn",
            "message": f"Run this command and report only failures: {cmd}",
            "timeoutSeconds": 3600,
        },
        "delivery": {"mode": "none"},
        "enabled": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Print OpenClaw cron job specs for scheduled sync")
    parser.add_argument("--platform", choices=["xhs", "zhihu"], required=True)
    parser.add_argument("--time", required=True, help="HH:MM in the supplied timezone")
    parser.add_argument("--timezone", default="Asia/Shanghai")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--print", action="store_true", dest="print_only")
    args = parser.parse_args()
    spec = payload(args.platform, args.time, args.config, args.timezone, Path(__file__).resolve().parents[1])
    print(json.dumps(spec, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
