#!/usr/bin/env python3
import argparse
import json
import os
import plistlib
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_LABEL = "com.cheeseclaw.skill-forge-nightly"
DEFAULT_PLIST = Path.home() / "Library" / "LaunchAgents" / f"{DEFAULT_LABEL}.plist"


def program_arguments(args: argparse.Namespace) -> list[str]:
    command = [
        sys.executable,
        str(BASE_DIR / "nightly_skill_review.py"),
        "--target-root",
        args.target_root,
        "--feedback-file",
        args.feedback_file,
        "--replay-cases",
        args.replay_cases,
        "--report-root",
        args.report_root,
        "--update-output",
        args.update_output,
        "--scope",
        args.scope,
        "--min-score",
        str(args.min_score),
        "--feedback-threshold",
        str(args.feedback_threshold),
        "--negative-feedback-threshold",
        str(args.negative_feedback_threshold),
        "--replay",
        args.replay,
        "--min-replay-score",
        str(args.min_replay_score),
        "--json",
    ]
    if args.propose_updates:
        command.append("--propose-updates")
    if args.update_install:
        command.extend(["--update-install", args.update_install])
    if args.agent_name:
        command.extend(["--agent-name", args.agent_name])
    if args.telegram_report:
        command.append("--telegram-report")
    if args.env_file:
        command.extend(["--env-file", args.env_file])
    return command


def build_plist(args: argparse.Namespace) -> dict:
    log_dir = Path(args.log_dir).expanduser().resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    return {
        "Label": args.label,
        "ProgramArguments": program_arguments(args),
        "StartCalendarInterval": {
            "Hour": args.hour,
            "Minute": args.minute,
        },
        "StandardOutPath": str(log_dir / "skill-forge-nightly.out.log"),
        "StandardErrorPath": str(log_dir / "skill-forge-nightly.err.log"),
        "RunAtLoad": False,
        "KeepAlive": False,
    }


def write_plist(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as handle:
        plistlib.dump(payload, handle, sort_keys=False)


def launchctl(args: list[str]) -> dict:
    completed = subprocess.run(["launchctl", *args], text=True, capture_output=True)
    return {
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
    }


def unload(path: Path) -> dict:
    if not path.exists():
        return {"returncode": 0, "stdout": "", "stderr": "plist not found"}
    return launchctl(["unload", str(path)])


def main() -> int:
    parser = argparse.ArgumentParser(description="Install or remove a macOS LaunchAgent for nightly Skill Forge review.")
    parser.add_argument("--label", default=DEFAULT_LABEL)
    parser.add_argument("--plist", default=str(DEFAULT_PLIST))
    parser.add_argument("--hour", type=int, default=3)
    parser.add_argument("--minute", type=int, default=0)
    parser.add_argument("--target-root", default=str(Path.home() / ".openclaw" / "workspace" / "skills"))
    parser.add_argument("--feedback-file", default=str(Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-feedback.jsonl"))
    parser.add_argument("--replay-cases", default=str(Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-replay-cases.jsonl"))
    parser.add_argument("--report-root", default=str(Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-forge-nightly"))
    parser.add_argument("--update-output", default=str(Path.home() / ".openclaw" / "workspace" / "skill-forge-updates"))
    parser.add_argument("--scope", choices=["managed", "feedback", "all"], default="managed")
    parser.add_argument("--log-dir", default=str(Path.home() / ".openclaw" / "workspace" / "logs"))
    parser.add_argument("--min-score", type=int, default=85)
    parser.add_argument("--feedback-threshold", type=int, default=1)
    parser.add_argument("--negative-feedback-threshold", type=int, default=1)
    parser.add_argument("--replay", choices=["off", "hidden"], default="hidden")
    parser.add_argument("--min-replay-score", type=int, default=70)
    parser.add_argument("--propose-updates", action="store_true")
    parser.add_argument("--update-install", choices=["plan", "telegram", "auto"], default="plan")
    parser.add_argument("--agent-name", default="")
    parser.add_argument("--telegram-report", action="store_true")
    parser.add_argument("--env-file", default="")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    plist_path = Path(args.plist).expanduser().resolve()
    if args.uninstall:
        if args.apply:
            result = unload(plist_path)
            removed = False
            if plist_path.exists():
                plist_path.unlink()
                removed = True
            payload = {"status": "uninstalled" if removed else "uninstalled-noop", "plist": str(plist_path), "launchctl": result}
        else:
            payload = {"status": "planned-uninstall", "plist": str(plist_path)}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
        return 0

    payload = build_plist(args)
    if args.apply:
        write_plist(plist_path, payload)
        unload_result = unload(plist_path)
        load_result = launchctl(["load", str(plist_path)])
        status = "installed" if load_result["returncode"] == 0 else "load-failed"
        result = {"status": status, "plist": str(plist_path), "launchctl_unload": unload_result, "launchctl_load": load_result}
    else:
        result = {"status": "planned", "plist": str(plist_path), "plist_payload": payload}
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
