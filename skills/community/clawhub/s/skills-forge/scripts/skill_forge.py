#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

from lib.approval import derive_secret
from lib.approval import APPROVAL_SECRET_ENV
from lib.telegram_config import discover_telegram_config


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
REPO_DIR = SKILL_DIR.parent
DEFAULT_TARGET_ROOT = Path.home() / ".openclaw" / "workspace" / "skills"


def read_version() -> str:
    path = SKILL_DIR / "VERSION"
    return path.read_text(encoding="utf-8").strip() if path.exists() else "unknown"


def emit_json(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def run_child(command: list[str], json_mode: bool = False, check: bool = False) -> int:
    completed = subprocess.run(command, text=True, capture_output=True)
    if json_mode:
        payload = {
            "status": "ok" if completed.returncode == 0 else "failed",
            "returncode": completed.returncode,
            "command": command,
        }
        if completed.stdout.strip():
            try:
                payload["result"] = json.loads(completed.stdout)
            except json.JSONDecodeError:
                payload["stdout"] = completed.stdout.strip()
        if completed.stderr.strip():
            payload["stderr"] = completed.stderr.strip()
        emit_json(payload)
    else:
        if completed.stdout:
            print(completed.stdout, end="")
        if completed.stderr:
            print(completed.stderr, end="", file=sys.stderr)
    if check and completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return completed.returncode


def status_item(name: str, ok: bool, detail: str, next_step: str = "", severity: str = "warn") -> dict:
    return {
        "name": name,
        "status": "ok" if ok else severity,
        "detail": detail,
        "next_step": next_step,
    }


def git_status() -> dict:
    if not (REPO_DIR / ".git").exists():
        return {"available": False, "detail": "not running from a git checkout"}
    head = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=REPO_DIR,
        text=True,
        capture_output=True,
    )
    status = subprocess.run(
        ["git", "status", "--porcelain=v2", "--branch"],
        cwd=REPO_DIR,
        text=True,
        capture_output=True,
    )
    lines = [line for line in status.stdout.splitlines() if line]
    dirty_lines = [line for line in lines if not line.startswith("#")]
    return {
        "available": head.returncode == 0 and status.returncode == 0,
        "head": head.stdout.strip(),
        "status": status.stdout.strip(),
        "clean": status.returncode == 0 and not dirty_lines,
        "dirty_entries": len(dirty_lines),
    }


def command_doctor(args: argparse.Namespace) -> int:
    target_root = Path(args.target_root).expanduser()
    config = discover_telegram_config(
        args.telegram_bot_token_env,
        args.telegram_chat_id_env,
        args.env_file,
        load_defaults=not args.no_default_env_files,
    )
    token = os.getenv(config["token_env"] or args.telegram_bot_token_env)
    secret_source = "missing"
    try:
        derive_secret(token)
        secret_ok = True
        secret_source = "explicit env" if os.getenv(APPROVAL_SECRET_ENV) else "derived from bot token"
    except RuntimeError:
        secret_ok = False

    checks = [
        status_item(
            "skill-package",
            (SKILL_DIR / "SKILL.md").is_file() and (SKILL_DIR / "VERSION").is_file(),
            f"{SKILL_DIR} version={read_version()}",
            "Run from an installed Skill Forge package containing SKILL.md and VERSION.",
            "block",
        ),
        status_item(
            "python",
            sys.version_info >= (3, 9),
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "Use Python 3.9 or newer.",
            "block",
        ),
        status_item(
            "openclaw-target-root",
            target_root.exists(),
            str(target_root),
            "Create it with: mkdir -p ~/.openclaw/workspace/skills",
        ),
        status_item(
            "telegram-config",
            bool(config["available"]),
            f"token_env={config.get('token_env')} chat_id_env={config.get('chat_id_env')} loaded={config.get('loaded_env_files')}",
            "Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID, or pass --env-file.",
        ),
        status_item(
            "approval-secret",
            secret_ok,
            secret_source,
            "Set SKILL_FORGE_APPROVAL_SECRET or provide a Telegram bot token.",
        ),
        status_item(
            "learnings-dir",
            (Path.home() / ".openclaw" / "workspace" / ".learnings").exists(),
            str(Path.home() / ".openclaw" / "workspace" / ".learnings"),
            "Create it with: mkdir -p ~/.openclaw/workspace/.learnings",
        ),
        status_item(
            "clawhub-cli",
            shutil.which("clawhub") is not None,
            shutil.which("clawhub") or "not found",
            "Install ClawHub CLI if you want registry install/publish workflows.",
        ),
        status_item(
            "release-checks",
            (REPO_DIR / "tests" / "run_release_checks.py").is_file(),
            str(REPO_DIR / "tests" / "run_release_checks.py"),
            "Release checks are available only in the source repository.",
        ),
        status_item(
            "github-actions",
            (REPO_DIR / ".github" / "workflows" / "release-checks.yml").is_file(),
            str(REPO_DIR / ".github" / "workflows" / "release-checks.yml"),
            "Add CI when maintaining the source repository.",
        ),
    ]
    git = git_status()
    if git["available"]:
        checks.append(
            status_item(
                "git",
                bool(git["clean"]),
                git["status"],
                "Commit or stash local changes before publishing.",
            )
        )

    blocking = [item for item in checks if item["status"] == "block"]
    warnings = [item for item in checks if item["status"] == "warn"]
    payload = {
        "status": "blocked" if blocking else ("warn" if warnings else "ok"),
        "product": "Skill Forge",
        "version": read_version(),
        "checks": checks,
        "next_step": f"Run `python3 {SCRIPT_DIR / 'skill_forge.py'} demo --json` for a safe plan-only smoke test.",
    }
    if args.json:
        emit_json(payload)
    else:
        print(f"Skill Forge {payload['version']} doctor: {payload['status']}")
        for item in checks:
            print(f"- {item['status']}: {item['name']} - {item['detail']}")
            if item["status"] != "ok" and item.get("next_step"):
                print(f"  next: {item['next_step']}")
    if args.strict and payload["status"] != "ok":
        return 1
    return 1 if blocking else 0


def command_demo(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "forge_pipeline.py"),
        "--source",
        str(SKILL_DIR / "examples" / "sample-feature-requests.md"),
        "--source",
        str(SKILL_DIR / "examples" / "sample-errors.md"),
        "--output",
        args.output,
        "--target-root",
        args.target_root,
        "--eval",
        args.eval,
        "--install",
        "plan",
        "--agent-name",
        args.agent_name,
        "--json",
    ]
    return run_child(command, json_mode=False)


def command_forge(args: argparse.Namespace) -> int:
    sources = args.source or [
        str(SKILL_DIR / "examples" / "sample-feature-requests.md"),
        str(SKILL_DIR / "examples" / "sample-errors.md"),
    ]
    command = [
        sys.executable,
        str(SCRIPT_DIR / "forge_pipeline.py"),
        "--output",
        args.output,
        "--target-root",
        args.target_root,
        "--install",
        args.install,
        "--eval",
        args.eval,
        "--agent-name",
        args.agent_name,
        "--telegram-dry-run",
        args.telegram_dry_run,
    ]
    for source in sources:
        command.extend(["--source", source])
    if args.env_file:
        command.extend(["--env-file", args.env_file])
    if args.prefer_evolve:
        command.append("--prefer-evolve")
        command.extend(["--evolve-threshold", str(args.evolve_threshold)])
        command.extend(["--ambiguous-margin", str(args.ambiguous_margin)])
    if args.json:
        command.append("--json")
    return run_child(command, json_mode=False)


def command_decide(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "decide_skill_action.py"),
        "--target-root",
        args.target_root,
        "--evolve-threshold",
        str(args.evolve_threshold),
        "--ambiguous-margin",
        str(args.ambiguous_margin),
    ]
    if args.opportunity_json:
        command.extend(["--opportunity-json", args.opportunity_json])
    elif args.opportunity_stdin:
        command.append("--opportunity-stdin")
    else:
        command.extend([
            "--skill-name", args.skill_name,
            "--triggers", args.triggers,
            "--template", args.template,
            "--reason", args.reason,
        ])
    if args.json:
        command.append("--json")
    return run_child(command, json_mode=False)


def command_evolve(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "evolve_skill_pipeline.py"),
        "--skill",
        args.skill,
        "--output",
        args.output,
        "--target-root",
        args.target_root,
        "--install",
        args.install,
        "--replay",
        args.replay,
        "--min-replay-improvement",
        str(args.min_replay_improvement),
        "--agent-name",
        args.agent_name,
    ]
    if args.env_file:
        command.extend(["--env-file", args.env_file])
    if args.json:
        command.append("--json")
    return run_child(command, json_mode=False)


def command_install(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "propose_skill_install.py"),
        args.skill_dir,
        "--target-root",
        args.target_root,
        "--method",
        args.method,
    ]
    if args.apply:
        command.append("--apply")
    if args.approval_token:
        command.extend(["--approval-token", args.approval_token])
    if args.env_file:
        command.extend(["--env-file", args.env_file])
    if args.bot_token_env:
        command.extend(["--bot-token-env", args.bot_token_env])
    if args.json:
        command.append("--json")
    return run_child(command, json_mode=False)


def command_uninstall(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "propose_skill_install.py"),
        args.skill,
        "--target-root",
        args.target_root,
        "--method",
        args.method,
        "--uninstall",
    ]
    if args.apply:
        command.append("--apply")
    if args.restore_backup:
        command.append("--restore-backup")
    if args.approval_token:
        command.extend(["--approval-token", args.approval_token])
    if args.env_file:
        command.extend(["--env-file", args.env_file])
    if args.bot_token_env:
        command.extend(["--bot-token-env", args.bot_token_env])
    if args.json:
        command.append("--json")
    return run_child(command, json_mode=False)


def command_feedback(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "record_skill_feedback.py"),
        "--skill",
        args.skill,
        "--rating",
        args.rating,
        "--feedback",
        args.feedback,
    ]
    if args.agent_name:
        command.extend(["--agent-name", args.agent_name])
    if args.task:
        command.extend(["--task", args.task])
    if args.expected:
        command.extend(["--expected", args.expected])
    if args.actual:
        command.extend(["--actual", args.actual])
    if args.tags:
        command.extend(["--tags", args.tags])
    if args.json:
        command.append("--json")
    return run_child(command, json_mode=False)


def command_replay(args: argparse.Namespace) -> int:
    command = [
        sys.executable,
        str(SCRIPT_DIR / "replay" / "run_replay_eval.py"),
        "--skill-dir",
        args.skill_dir,
        "--skill",
        args.skill,
        "--cases",
        args.cases,
        "--min-score",
        str(args.min_score),
    ]
    if args.json:
        command.append("--json")
    return run_child(command, json_mode=False)


def command_release_check(args: argparse.Namespace) -> int:
    checks = []
    release_script = REPO_DIR / "tests" / "run_release_checks.py"
    if release_script.exists():
        completed = subprocess.run([sys.executable, str(release_script)], cwd=REPO_DIR, text=True, capture_output=True)
        checks.append(
            {
                "name": "release-checks",
                "status": "ok" if completed.returncode == 0 else "failed",
                "returncode": completed.returncode,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
            }
        )
    else:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "validate_skill_candidate.py"), str(SKILL_DIR), "--json"],
            text=True,
            capture_output=True,
        )
        checks.append(
            {
                "name": "skill-validation",
                "status": "ok" if completed.returncode == 0 else "failed",
                "returncode": completed.returncode,
                "stdout": completed.stdout.strip(),
                "stderr": completed.stderr.strip(),
            }
        )
    if not release_script.exists():
        secret_scan = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "security" / "scan_secrets.py"), "--root", str(SKILL_DIR), "--json"],
            cwd=SKILL_DIR,
            text=True,
            capture_output=True,
        )
        checks.append(
            {
                "name": "secret-scan",
                "status": "ok" if secret_scan.returncode == 0 else "failed",
                "returncode": secret_scan.returncode,
                "stdout": secret_scan.stdout.strip(),
                "stderr": secret_scan.stderr.strip(),
            }
        )
    failed = [item for item in checks if item["status"] != "ok"]
    payload = {"status": "failed" if failed else "ok", "checks": checks}
    if args.json:
        emit_json(payload)
    else:
        for item in checks:
            print(f"{item['status']} {item['name']}")
            if item["status"] != "ok" and item["stderr"]:
                print(item["stderr"], file=sys.stderr)
    return 1 if failed else 0


def command_version(args: argparse.Namespace) -> int:
    payload = {"product": "Skill Forge", "version": read_version(), "skill_dir": str(SKILL_DIR)}
    if args.json:
        emit_json(payload)
    else:
        print(payload["version"])
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Skill Forge product console.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="Check environment readiness.")
    doctor.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    doctor.add_argument("--env-file", default="")
    doctor.add_argument("--telegram-bot-token-env", default="TELEGRAM_BOT_TOKEN")
    doctor.add_argument("--telegram-chat-id-env", default="TELEGRAM_CHAT_ID")
    doctor.add_argument("--no-default-env-files", action="store_true")
    doctor.add_argument("--strict", action="store_true")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=command_doctor)

    demo = subparsers.add_parser("demo", help="Run a safe plan-only demo.")
    demo.add_argument("--output", default="./generated-forge-demo")
    demo.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    demo.add_argument("--agent-name", default="StudyAgent")
    demo.add_argument("--eval", choices=["off", "hidden", "details"], default="hidden")
    demo.add_argument("--json", action="store_true")
    demo.set_defaults(func=command_demo)

    forge = subparsers.add_parser("forge", help="Detect, generate, validate, and optionally request install approval.")
    forge.add_argument("--source", action="append", default=[])
    forge.add_argument("--output", default="./generated")
    forge.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    forge.add_argument("--install", choices=["plan", "ask", "telegram", "auto"], default="plan")
    forge.add_argument("--eval", choices=["off", "hidden", "details"], default="hidden")
    forge.add_argument("--agent-name", default="")
    forge.add_argument("--telegram-dry-run", choices=["off", "approve", "reject", "timeout"], default="off")
    forge.add_argument("--env-file", default="")
    forge.add_argument(
        "--prefer-evolve",
        action="store_true",
        help="Route the detected opportunity through `decide` first; if it matches an installed skill, evolve that skill instead of forging a new one. Default off in 1.x for backward compatibility.",
    )
    forge.add_argument("--evolve-threshold", type=float, default=0.45,
                       help="Fitness threshold for routing to evolve. Default 0.45.")
    forge.add_argument("--ambiguous-margin", type=float, default=0.1,
                       help="Top-vs-second fitness margin within which routing is flagged ambiguous. Default 0.1.")
    forge.add_argument("--json", action="store_true")
    forge.set_defaults(func=command_forge)

    decide = subparsers.add_parser("decide",
        help="Given an opportunity, decide whether to evolve an installed skill or forge a new one.")
    decide.add_argument("--opportunity-json", default="",
                        help="Path to an opportunity JSON file (e.g. one entry from detect_skill_opportunities.py output).")
    decide.add_argument("--opportunity-stdin", action="store_true",
                        help="Read the opportunity JSON object from stdin.")
    decide.add_argument("--skill-name", default="", help="Inline opportunity: suggested skill name.")
    decide.add_argument("--triggers", default="", help="Inline opportunity: comma-separated triggers.")
    decide.add_argument("--template",
                        choices=["academic", "product", "integration", "script", "workflow"],
                        default="workflow")
    decide.add_argument("--reason", default="", help="Inline opportunity: short reason / evidence snippet.")
    decide.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    decide.add_argument("--evolve-threshold", type=float, default=0.45)
    decide.add_argument("--ambiguous-margin", type=float, default=0.1)
    decide.add_argument("--json", action="store_true")
    decide.set_defaults(func=command_decide)

    evolve = subparsers.add_parser("evolve", help="Propose a reviewed update from feedback.")
    evolve.add_argument("--skill", required=True)
    evolve.add_argument("--output", default="./generated-updates")
    evolve.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    evolve.add_argument("--install", choices=["plan", "ask", "telegram", "auto"], default="plan")
    evolve.add_argument("--replay", choices=["off", "hidden"], default="hidden")
    evolve.add_argument("--min-replay-improvement", type=int, default=0)
    evolve.add_argument("--agent-name", default="")
    evolve.add_argument("--env-file", default="")
    evolve.add_argument("--json", action="store_true")
    evolve.set_defaults(func=command_evolve)

    install = subparsers.add_parser("install", help="Print or apply a signed-gated install plan.")
    install.add_argument("skill_dir")
    install.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    install.add_argument("--method", choices=["symlink", "copy"], default="symlink")
    install.add_argument("--apply", action="store_true")
    install.add_argument("--approval-token", default="")
    install.add_argument("--env-file", default="")
    install.add_argument("--bot-token-env", default="TELEGRAM_BOT_TOKEN")
    install.add_argument("--json", action="store_true")
    install.set_defaults(func=command_install)

    uninstall = subparsers.add_parser("uninstall", help="Print or apply a signed-gated uninstall plan.")
    uninstall.add_argument("skill")
    uninstall.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    uninstall.add_argument("--method", choices=["symlink", "copy"], default="symlink")
    uninstall.add_argument("--apply", action="store_true")
    uninstall.add_argument("--restore-backup", action="store_true")
    uninstall.add_argument("--approval-token", default="")
    uninstall.add_argument("--env-file", default="")
    uninstall.add_argument("--bot-token-env", default="TELEGRAM_BOT_TOKEN")
    uninstall.add_argument("--json", action="store_true")
    uninstall.set_defaults(func=command_uninstall)

    feedback = subparsers.add_parser("feedback", help="Record redacted skill usage feedback.")
    feedback.add_argument("--skill", required=True)
    feedback.add_argument("--rating", choices=["positive", "neutral", "negative"], required=True)
    feedback.add_argument("--feedback", required=True)
    feedback.add_argument("--agent-name", default="")
    feedback.add_argument("--task", default="")
    feedback.add_argument("--expected", default="")
    feedback.add_argument("--actual", default="")
    feedback.add_argument("--tags", default="")
    feedback.add_argument("--json", action="store_true")
    feedback.set_defaults(func=command_feedback)

    replay = subparsers.add_parser("replay", help="Run replay evaluation for a skill directory.")
    replay.add_argument("--skill-dir", required=True)
    replay.add_argument("--skill", required=True)
    replay.add_argument("--cases", default=str(Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-replay-cases.jsonl"))
    replay.add_argument("--min-score", type=int, default=70)
    replay.add_argument("--json", action="store_true")
    replay.set_defaults(func=command_replay)

    release = subparsers.add_parser("release-check", help="Run product release gates.")
    release.add_argument("--json", action="store_true")
    release.set_defaults(func=command_release_check)

    version = subparsers.add_parser("version", help="Print Skill Forge version.")
    version.add_argument("--json", action="store_true")
    version.set_defaults(func=command_version)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
