#!/usr/bin/env python3
"""
Convert natural-language schedule updates into a structured config delta.

This public example focuses on config transformation and preview output.
It does not write local files unless explicitly requested.
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path


def load(path: Path | None) -> dict:
    if path and path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "enabled": True,
        "speaker": {"language": "zh", "voiceType": "female", "tone": "calm"},
        "schedules": [],
    }


def build_updated_config(data: dict, args: argparse.Namespace) -> dict:
    days = [int(x.strip()) for x in args.days.split(",") if x.strip()]
    modules = [x.strip() for x in args.modules.split(",") if x.strip()]

    item = {
        "id": args.id,
        "enabled": True,
        "days": days,
        "time": args.time,
        "modules": modules,
        "style": {"length": "short", "variability": "medium"},
    }

    data["speaker"] = {
        "language": args.language,
        "voiceType": args.voice_type,
        "tone": args.tone,
    }
    if args.timezone:
        data["timezone"] = args.timezone
    schedules = [s for s in data.get("schedules", []) if s.get("id") != args.id]
    schedules.append(item)
    data["schedules"] = schedules
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--id", required=True)
    parser.add_argument("--time", required=True)
    parser.add_argument("--days", default="1,2,3,4,5")
    parser.add_argument("--modules", default="environment_brief,schedule_brief")
    parser.add_argument("--language", default="zh")
    parser.add_argument("--voice-type", default="female")
    parser.add_argument("--tone", default="calm")
    parser.add_argument("--timezone")
    args = parser.parse_args()

    path = Path(args.config) if args.config else None
    data = load(path)
    updated = build_updated_config(data, args)

    if args.write:
        if path is None:
            raise SystemExit("--write requires --config")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(str(path))
    else:
        print(json.dumps(updated, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
