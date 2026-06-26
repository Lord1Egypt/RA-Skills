#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from common import SCRIPTS_DIR, date_stamp, run_json

def skill_dirs(target_root: Path, manifest: dict, feedback_entries: list[dict], scope: str) -> dict[str, Path]:
    result = {}
    if scope == "all" and target_root.exists():
        for path in sorted(target_root.iterdir()):
            if path.name.startswith("."):
                continue
            if (path / "SKILL.md").exists():
                result[path.name] = path.resolve()
    for name, record in manifest.get("installs", {}).items():
        source = Path(record.get("source", "")).expanduser()
        target = Path(record.get("target", "")).expanduser()
        if source and (source / "SKILL.md").exists():
            result.setdefault(name, source.resolve())
        elif target and (target / "SKILL.md").exists():
            result.setdefault(name, target.resolve())
    if scope == "managed":
        own_skill = target_root / "skill-forge"
        if (own_skill / "SKILL.md").exists():
            result.setdefault("skill-forge", own_skill.resolve())
    if scope == "feedback":
        for entry in feedback_entries:
            name = entry.get("skill")
            if not name or name in result:
                continue
            target = target_root / name
            if (target / "SKILL.md").exists():
                result[name] = target.resolve()
    return result


def read_feedback(feedback_file: Path) -> list[dict]:
    if not feedback_file.exists():
        return []
    entries = []
    for line in feedback_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def feedback_summary(entries: list[dict], skill: str) -> dict:
    matched = [entry for entry in entries if entry.get("skill") == skill]
    ratings = {"positive": 0, "neutral": 0, "negative": 0}
    for entry in matched:
        rating = entry.get("rating") or "neutral"
        ratings[rating] = ratings.get(rating, 0) + 1
    return {
        "total": len(matched),
        "positive": ratings.get("positive", 0),
        "neutral": ratings.get("neutral", 0),
        "negative": ratings.get("negative", 0),
        "latest": matched[-1].get("created_at") if matched else None,
    }


def validate_skill(skill_dir: Path) -> dict:
    return run_json([sys.executable, str(SCRIPTS_DIR / "validate_skill_candidate.py"), str(skill_dir), "--json"])


def evaluate_skill(skill_dir: Path, profile: str) -> Optional[dict]:
    result = run_json(
        [
            sys.executable,
            str(SCRIPTS_DIR / "evaluate_skill_candidate.py"),
            str(skill_dir),
            "--profile",
            profile,
            "--json",
        ]
    )
    if result.get("status") == "invalid-json":
        return None
    return result


def replay_skill(skill: str, skill_dir: Path, args: argparse.Namespace) -> Optional[dict]:
    if args.replay == "off":
        return None
    run_json(
        [
            sys.executable,
            str(SCRIPTS_DIR / "replay" / "collect_replay_cases.py"),
            "--feedback-file",
            args.feedback_file,
            "--output",
            args.replay_cases,
            "--skill",
            skill,
            "--json",
        ]
    )
    return run_json(
        [
            sys.executable,
            str(SCRIPTS_DIR / "replay" / "run_replay_eval.py"),
            "--skill-dir",
            str(skill_dir),
            "--cases",
            args.replay_cases,
            "--skill",
            skill,
            "--min-score",
            str(args.min_replay_score),
            "--json",
        ]
    )


def issue_list(validation: dict, evaluation: Optional[dict], replay: Optional[dict], feedback: dict, args: argparse.Namespace) -> list[str]:
    issues = []
    if not validation.get("valid"):
        issues.append("validation_failed")
    if int(validation.get("score", 0)) < args.min_score:
        issues.append("low_validation_score")
    if evaluation and not evaluation.get("passed"):
        issues.append("hidden_evaluation_failed")
    if replay and replay.get("cases_run", 0) > 0 and not replay.get("passed"):
        issues.append("replay_failed")
    if feedback["negative"] >= args.negative_feedback_threshold:
        issues.append("negative_feedback")
    if feedback["total"] >= args.feedback_threshold:
        issues.append("feedback_available")
    return issues


def propose_update(skill: str, args: argparse.Namespace) -> Optional[dict]:
    output = Path(args.update_output).expanduser().resolve() / date_stamp()
    command = [
        sys.executable,
        str(SCRIPTS_DIR / "evolve" / "evolve_skill_pipeline.py"),
        "--skill",
        skill,
        "--output",
        str(output),
        "--target-root",
        args.target_root,
        "--feedback-file",
        args.feedback_file,
        "--feedback-limit",
        str(args.feedback_limit),
        "--install",
        args.update_install,
        "--eval",
        "hidden",
        "--replay",
        args.replay,
        "--replay-cases",
        args.replay_cases,
        "--min-replay-score",
        str(args.min_replay_score),
        "--json",
    ]
    if args.agent_name:
        command.extend(["--agent-name", args.agent_name])
    if args.update_install == "telegram":
        command.extend(
            [
                "--telegram-timeout",
                str(args.telegram_timeout),
                "--telegram-bot-token-env",
                args.telegram_bot_token_env,
                "--telegram-chat-id-env",
                args.telegram_chat_id_env,
                "--telegram-dry-run",
                args.telegram_dry_run,
            ]
        )
    if getattr(args, "env_file", ""):
        command.extend(["--env-file", args.env_file])
    return run_json(command)
