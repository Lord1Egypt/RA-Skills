#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from common import (
    DEFAULT_FEEDBACK_FILE,
    DEFAULT_REPLAY_FILE,
    DEFAULT_REPORT_ROOT,
    DEFAULT_TARGET_ROOT,
    DEFAULT_UPDATE_ROOT,
    date_stamp,
    load_env_file,
    load_manifest,
    utc_now,
)
from reporting import build_markdown, send_telegram_report
from scanner import (
    evaluate_skill,
    feedback_summary,
    issue_list,
    propose_update,
    read_feedback,
    replay_skill,
    skill_dirs,
    validate_skill,
)

def main() -> int:
    parser = argparse.ArgumentParser(description="Run nightly skill health review and optional update proposals.")
    parser.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    parser.add_argument("--feedback-file", default=str(DEFAULT_FEEDBACK_FILE))
    parser.add_argument("--replay-cases", default=str(DEFAULT_REPLAY_FILE))
    parser.add_argument("--report-root", default=str(DEFAULT_REPORT_ROOT))
    parser.add_argument("--update-output", default=str(DEFAULT_UPDATE_ROOT))
    parser.add_argument(
        "--scope",
        choices=["managed", "feedback", "all"],
        default="managed",
        help="Skills to review: skill-forge managed installs, feedback-related skills, or all skills.",
    )
    parser.add_argument("--min-score", type=int, default=85)
    parser.add_argument("--feedback-threshold", type=int, default=1)
    parser.add_argument("--negative-feedback-threshold", type=int, default=1)
    parser.add_argument("--feedback-limit", type=int, default=20)
    parser.add_argument("--replay", choices=["off", "hidden"], default="hidden")
    parser.add_argument("--min-replay-score", type=int, default=70)
    parser.add_argument("--propose-updates", action="store_true")
    parser.add_argument("--update-install", choices=["plan", "ask", "telegram", "auto"], default="plan")
    parser.add_argument("--agent-name", default="")
    parser.add_argument("--telegram-report", action="store_true")
    parser.add_argument("--telegram-timeout", type=int, default=300)
    parser.add_argument("--telegram-bot-token-env", default="TELEGRAM_BOT_TOKEN")
    parser.add_argument("--telegram-chat-id-env", default="TELEGRAM_CHAT_ID")
    parser.add_argument("--telegram-dry-run", choices=["off", "approve", "reject", "timeout"], default="off")
    parser.add_argument("--env-file", default="", help="Optional KEY=VALUE env file for scheduled runs.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    load_env_file(args.env_file)
    target_root = Path(args.target_root).expanduser().resolve()
    feedback_file = Path(args.feedback_file).expanduser().resolve()
    report_root = Path(args.report_root).expanduser().resolve()
    report_root.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(target_root)
    feedback_entries = read_feedback(feedback_file)
    skills = []
    updates_proposed = 0

    for skill, path in skill_dirs(target_root, manifest, feedback_entries, args.scope).items():
        validation = validate_skill(path)
        profile = validation.get("inferred_profile", "workflow")
        evaluation = evaluate_skill(path, profile)
        replay = replay_skill(skill, path, args)
        feedback = feedback_summary(feedback_entries, skill)
        issues = issue_list(validation, evaluation, replay, feedback, args)
        update = None
        if args.propose_updates and feedback["total"] >= args.feedback_threshold:
            update = propose_update(skill, args)
            if update and update.get("status") == "ok":
                updates_proposed += 1
        evaluation_summary = {
            "status": "passed" if evaluation and evaluation.get("passed") else "failed" if evaluation else "not-run",
            "score": evaluation.get("score") if evaluation else None,
            "details_hidden": evaluation.get("details_hidden") if evaluation else True,
        }
        replay_summary = {
            "status": "passed" if replay and replay.get("passed") else "failed" if replay and replay.get("cases_run", 0) else "not-run",
            "score": replay.get("score") if replay else None,
            "cases_run": replay.get("cases_run") if replay else 0,
            "details_hidden": replay.get("details_hidden") if replay else True,
        }
        skills.append(
            {
                "skill": skill,
                "path": str(path),
                "validation": validation,
                "evaluation_summary": evaluation_summary,
                "replay_summary": replay_summary,
                "feedback": feedback,
                "issues": issues,
                "update_status": update.get("status") if update else None,
                "update_install_status": update.get("install_status") if update else None,
            }
        )

    report = {
        "created_at": utc_now(),
        "target_root": str(target_root),
        "scope": args.scope,
        "feedback_file": str(feedback_file),
        "summary": {
            "skills_checked": len(skills),
            "needs_attention": sum(1 for item in skills if item["issues"]),
            "updates_proposed": updates_proposed,
        },
        "skills": skills,
    }
    stem = f"nightly-review-{date_stamp()}"
    json_path = report_root / f"{stem}.json"
    md_path = report_root / f"{stem}.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown = build_markdown(report)
    md_path.write_text(markdown, encoding="utf-8")
    telegram = send_telegram_report(markdown, args) if args.telegram_report else {"sent": False, "status": "disabled"}

    payload = {
        "status": "ok",
        "report_json": str(json_path),
        "report_md": str(md_path),
        "summary": report["summary"],
        "telegram": telegram,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else str(md_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
