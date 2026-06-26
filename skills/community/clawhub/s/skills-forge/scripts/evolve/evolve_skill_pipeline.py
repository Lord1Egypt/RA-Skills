#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Optional


BASE_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = BASE_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))

from lib.install_flow import install_args, install_eligibility, telegram_approval_args, telegram_required_status
from lib.policy import agent_authorization
from lib.runtime import run_json

DEFAULT_TARGET_ROOT = Path.home() / ".openclaw" / "workspace" / "skills"
DEFAULT_FEEDBACK_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-feedback.jsonl"
DEFAULT_REPLAY_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-replay-cases.jsonl"


def run_replay(args: argparse.Namespace, candidate: str, baseline: Optional[str]) -> Optional[dict]:
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
            args.skill,
            "--json",
        ],
        check=False,
    )
    if baseline and Path(baseline).exists():
        compare_cmd = [
            sys.executable,
            str(SCRIPTS_DIR / "replay" / "compare_replay_outputs.py"),
            "--baseline",
            baseline,
            "--candidate",
            candidate,
            "--cases",
            args.replay_cases,
            "--skill",
            args.skill,
            "--min-score",
            str(args.min_replay_score),
            "--min-improvement",
            str(args.min_replay_improvement),
            "--json",
        ]
        return run_json(compare_cmd, check=False)
    command = [
        sys.executable,
        str(SCRIPTS_DIR / "replay" / "run_replay_eval.py"),
        "--skill-dir",
        candidate,
        "--cases",
        args.replay_cases,
        "--skill",
        args.skill,
        "--min-score",
        str(args.min_replay_score),
        "--json",
    ]
    return run_json(command, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Propose, validate, evaluate, and optionally install a skill update from feedback.")
    parser.add_argument("--skill", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--source", default="")
    parser.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    parser.add_argument("--feedback-file", default=str(DEFAULT_FEEDBACK_FILE))
    parser.add_argument("--feedback-limit", type=int, default=20)
    parser.add_argument("--install", choices=["plan", "ask", "telegram", "auto"], default="plan")
    parser.add_argument("--install-method", choices=["symlink", "copy"], default="symlink")
    parser.add_argument("--min-install-score", type=int, default=85)
    parser.add_argument("--eval", choices=["off", "hidden", "details"], default="hidden")
    parser.add_argument("--replay", choices=["off", "hidden"], default="hidden")
    parser.add_argument("--replay-cases", default=str(DEFAULT_REPLAY_FILE))
    parser.add_argument("--min-replay-score", type=int, default=70)
    parser.add_argument(
        "--min-replay-improvement",
        type=int,
        default=0,
        help="Minimum candidate-vs-baseline replay score delta. Negative values disable the regression gate.",
    )
    parser.add_argument("--agent-name", default="")
    parser.add_argument("--telegram-timeout", type=int, default=300)
    parser.add_argument("--telegram-bot-token-env", default="TELEGRAM_BOT_TOKEN")
    parser.add_argument("--telegram-chat-id-env", default="TELEGRAM_CHAT_ID")
    parser.add_argument("--env-file", default="")
    parser.add_argument("--telegram-dry-run", choices=["off", "approve", "reject", "timeout"], default="off")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    proposal_cmd = [
        sys.executable,
        str(BASE_DIR / "propose_skill_update.py"),
        "--skill",
        args.skill,
        "--output",
        args.output,
        "--target-root",
        args.target_root,
        "--feedback-file",
        args.feedback_file,
        "--feedback-limit",
        str(args.feedback_limit),
        "--json",
    ]
    if args.source:
        proposal_cmd.extend(["--source", args.source])
    proposal = run_json(proposal_cmd, check=False)
    if proposal.get("status") != "proposed":
        payload = {"status": proposal.get("status", "needs-review"), "proposal": proposal}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
        return 1

    candidate = proposal["candidate"]
    report = run_json([sys.executable, str(SCRIPTS_DIR / "validate_skill_candidate.py"), candidate, "--json"])
    profile = report.get("inferred_profile", "workflow")
    evaluation = None
    if args.eval != "off":
        eval_cmd = [
            sys.executable,
            str(SCRIPTS_DIR / "evaluate_skill_candidate.py"),
            candidate,
            "--profile",
            profile,
            "--json",
        ]
        if args.eval == "details":
            eval_cmd.append("--show-details")
        evaluation = run_json(eval_cmd, check=False)
    replay = run_replay(args, candidate, proposal.get("source"))
    agent_policy = agent_authorization(args.agent_name, profile)
    plan = run_json(install_args(SCRIPTS_DIR, args, candidate))
    eligible, install_reason = install_eligibility(report, evaluation, replay, agent_policy, args.min_install_score)

    approval = None
    install_status = "planned"
    if args.install in {"ask", "telegram", "auto"}:
        telegram_block = telegram_required_status(args.install)
        if telegram_block:
            install_status = "blocked"
            install_reason = telegram_block
        elif not eligible:
            install_status = "blocked"
        elif args.install == "telegram":
            approval = run_json(telegram_approval_args(SCRIPTS_DIR, args, plan, report, evaluation, profile), check=False)
            if approval.get("approved"):
                claims = approval.get("approval_claims") or {}
                if not approval.get("approval_token"):
                    install_status = "approval-token-missing"
                    install_reason = approval.get("token_error") or "approved response did not include a signed approval token"
                elif claims.get("mode") == "dry-run":
                    install_status = "dry-run-blocked"
                    install_reason = "dry-run approval token is not allowed to mutate state"
                else:
                    plan = run_json(install_args(SCRIPTS_DIR, args, candidate, apply=True, approval=approval), check=False)
                    install_status = "installed" if plan.get("installed") else "install-blocked"
                    if not plan.get("installed"):
                        install_reason = plan.get("reason", install_reason)
            else:
                install_status = f"telegram-{approval.get('status', 'declined')}"

    payload = {
        "status": "ok" if report.get("valid") else "needs-review",
        "proposal": proposal,
        "validation": report,
        "evaluation": evaluation,
        "replay": replay,
        "agent_authorization": agent_policy,
        "approval": approval,
        "install_status": install_status,
        "install_reason": install_reason,
        "install_plan": plan,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
    return 0 if report.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
