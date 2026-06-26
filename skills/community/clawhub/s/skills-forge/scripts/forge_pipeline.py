#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from lib.install_flow import install_args, install_eligibility, telegram_approval_args, telegram_required_status
from lib.policy import agent_authorization
from lib.runtime import run_json, run_text


BASE_DIR = Path(__file__).resolve().parent

GOALS_BY_TEMPLATE = {
    "academic": "Help Study Agent produce citation-aware academic scaffolds, source metadata checklists, and bibliography-safe writing support.",
    "product": "Help Product Agent turn repeated product work into scoped PRDs, MVP slices, acceptance criteria, and handoff notes.",
    "integration": "Help agents set up and operate a recurring external integration with clear credentials, health checks, and failure handling.",
    "script": "Help agents replace repeated manual operations with a deterministic script-backed workflow.",
    "workflow": "Help agents handle a recurring task with a stable workflow, output contract, and quality checks.",
}


DEFAULT_TARGET_ROOT = Path.home() / ".openclaw" / "workspace" / "skills"
def run_evaluation(skill_dir: str, profile: str, mode: str) -> Optional[dict]:
    if mode == "off":
        return None
    command = [
        sys.executable,
        str(BASE_DIR / "evaluate_skill_candidate.py"),
        skill_dir,
        "--profile",
        profile,
        "--json",
    ]
    if mode == "details":
        command.append("--show-details")
    return run_json(command, check=False)


def run_decide(args: argparse.Namespace, opportunity: dict) -> dict:
    triggers_csv = ", ".join(opportunity.get("triggers") or [])
    template = opportunity.get("recommended_template", "workflow")
    cmd = [
        sys.executable,
        str(BASE_DIR / "decide_skill_action.py"),
        "--target-root", args.target_root,
        "--evolve-threshold", str(args.evolve_threshold),
        "--ambiguous-margin", str(args.ambiguous_margin),
        "--skill-name", opportunity.get("suggested_skill_name", ""),
        "--triggers", triggers_csv,
        "--template", template,
        "--reason", opportunity.get("reason", ""),
        "--json",
    ]
    return run_json(cmd, check=False)


def record_routing_feedback(target_skill: str, opportunity: dict, agent_name: str) -> dict:
    """Persist the opportunity as a synthetic feedback entry so evolve_skill_pipeline
    has something to build a candidate from. Tagged source=forge-routing for audit.

    The opportunity literally IS feedback the system noticed; treating it as such
    keeps a single feedback timeline rather than inventing a parallel signal channel.
    """
    triggers = opportunity.get("triggers") or []
    reason = opportunity.get("reason", "").strip()
    feedback_text = (
        f"Forge-router gap: {reason or 'no reason'}. "
        f"New trigger surface to consider: {', '.join(triggers) or '(none)'}."
    )
    cmd = [
        sys.executable,
        str(BASE_DIR / "record_skill_feedback.py"),
        "--skill", target_skill,
        "--rating", "neutral",
        "--feedback", feedback_text,
        "--source", "forge-routing",
        "--tags", "forge-routing,auto-detected",
        "--json",
    ]
    if agent_name:
        cmd.extend(["--agent-name", agent_name])
    return run_json(cmd, check=False)


def run_evolve_via_routing(args: argparse.Namespace, target_skill: str) -> dict:
    cmd = [
        sys.executable,
        str(BASE_DIR / "evolve_skill_pipeline.py"),
        "--skill", target_skill,
        "--output", args.output,
        "--target-root", args.target_root,
        "--install", args.install,
        "--eval", args.eval,
        "--telegram-dry-run", args.telegram_dry_run,
        "--telegram-bot-token-env", args.telegram_bot_token_env,
        "--telegram-chat-id-env", args.telegram_chat_id_env,
        "--telegram-timeout", str(args.telegram_timeout),
        "--min-install-score", str(args.min_install_score),
        "--json",
    ]
    if args.agent_name:
        cmd.extend(["--agent-name", args.agent_name])
    if args.env_file:
        cmd.extend(["--env-file", args.env_file])
    return run_json(cmd, check=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run detect -> generate -> validate for one candidate skill.")
    parser.add_argument("--source", action="append", default=[], help="Source learnings/log file.")
    parser.add_argument("--output", required=True, help="Output root for generated candidates.")
    parser.add_argument("--top", type=int, default=1)
    parser.add_argument(
        "--install",
        choices=["plan", "ask", "telegram", "auto"],
        default="plan",
        help="Installation behavior after validation. Mutating installs require Telegram approval; ask/auto are blocked safety aliases.",
    )
    parser.add_argument(
        "--install-method",
        choices=["symlink", "copy"],
        default="symlink",
        help="Install method used when --install ask/auto proceeds.",
    )
    parser.add_argument(
        "--target-root",
        default=str(DEFAULT_TARGET_ROOT),
        help="OpenClaw skills root used for install plans and installs.",
    )
    parser.add_argument(
        "--min-install-score",
        type=int,
        default=85,
        help="Minimum validation score required before ask/auto installation.",
    )
    parser.add_argument(
        "--eval",
        choices=["off", "hidden", "details"],
        default="hidden",
        help="Run candidate smoke evaluation. Hidden mode suppresses internal cases.",
    )
    parser.add_argument(
        "--agent-name",
        default="",
        help="Optional target agent name used to enforce profile install policy.",
    )
    parser.add_argument(
        "--telegram-timeout",
        type=int,
        default=300,
        help="Seconds to wait for Telegram approval when --install telegram is used.",
    )
    parser.add_argument(
        "--telegram-bot-token-env",
        default="TELEGRAM_BOT_TOKEN",
        help="Environment variable containing the Telegram bot token.",
    )
    parser.add_argument(
        "--telegram-chat-id-env",
        default="TELEGRAM_CHAT_ID",
        help="Environment variable containing the Telegram approval chat ID.",
    )
    parser.add_argument(
        "--env-file",
        default="",
        help="Optional KEY=VALUE env file. Telegram config is also auto-discovered from common OpenClaw env files.",
    )
    parser.add_argument(
        "--telegram-dry-run",
        choices=["off", "approve", "reject", "timeout"],
        default="off",
        help="Developer test mode for Telegram approval without network calls.",
    )
    parser.add_argument(
        "--prefer-evolve",
        action="store_true",
        help="Route the detected opportunity through decide_skill_action.py first; "
             "if it matches an installed skill, evolve that skill instead of forging a new one.",
    )
    parser.add_argument(
        "--evolve-threshold",
        type=float,
        default=0.45,
        help="Fitness threshold for routing to evolve. Default 0.45.",
    )
    parser.add_argument(
        "--ambiguous-margin",
        type=float,
        default=0.1,
        help="Top-vs-second fitness margin within which routing is flagged ambiguous.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    detect_cmd = [sys.executable, str(BASE_DIR / "detect_skill_opportunities.py"), "--top", str(args.top), "--json"]
    for source in args.source:
        detect_cmd.extend(["--source", source])
    detected = run_json(detect_cmd)
    opportunities = detected.get("opportunities", [])
    if not opportunities:
        payload = {"status": "no-opportunity", "detected": detected}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else "no opportunity")
        return 0

    opportunity = opportunities[0]

    routing = None
    if args.prefer_evolve:
        routing = run_decide(args, opportunity)
        if routing.get("decision") == "evolve" and routing.get("target_skill"):
            target_skill = routing["target_skill"]
            feedback_record = record_routing_feedback(target_skill, opportunity, args.agent_name)
            evolve_result = run_evolve_via_routing(args, target_skill)
            payload = {
                "status": evolve_result.get("status", "needs-review"),
                "routed_to": "evolve",
                "routing": routing,
                "opportunity": opportunity,
                "feedback_record": feedback_record,
                "evolve_result": evolve_result,
            }
            print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else f"routed-to-evolve:{target_skill}")
            return 0 if evolve_result.get("status") == "ok" else 1

    skill_name = opportunity["suggested_skill_name"]
    triggers = ", ".join(opportunity.get("triggers") or [skill_name])
    template = opportunity.get("recommended_template", "workflow")
    goal = GOALS_BY_TEMPLATE.get(template, GOALS_BY_TEMPLATE["workflow"])
    generated_line = run_text(
        [
            sys.executable,
            str(BASE_DIR / "generate_skill_scaffold.py"),
            "--skill-name",
            skill_name,
            "--output",
            args.output,
            "--goal",
            goal,
            "--triggers",
            triggers,
            "--template",
            template,
        ]
    )
    skill_dir = generated_line.split()[0]
    report = run_json([sys.executable, str(BASE_DIR / "validate_skill_candidate.py"), skill_dir, "--json"])
    profile = report.get("inferred_profile", template)
    evaluation = run_evaluation(skill_dir, profile, args.eval)
    agent_policy = agent_authorization(args.agent_name, profile)
    plan = run_json(install_args(BASE_DIR, args, skill_dir))
    eligible, install_reason = install_eligibility(report, evaluation, None, agent_policy, args.min_install_score)

    install_status = "planned"
    approval = None
    if args.install in {"ask", "telegram", "auto"}:
        telegram_block = telegram_required_status(args.install)
        if telegram_block:
            install_status = "blocked"
            install_reason = telegram_block
        elif not eligible:
            install_status = "blocked"
        elif args.install == "telegram":
            approval = run_json(telegram_approval_args(BASE_DIR, args, plan, report, evaluation, profile), check=False)
            if approval.get("approved"):
                claims = approval.get("approval_claims") or {}
                if not approval.get("approval_token"):
                    install_status = "approval-token-missing"
                    install_reason = approval.get("token_error") or "approved response did not include a signed approval token"
                elif claims.get("mode") == "dry-run":
                    install_status = "dry-run-blocked"
                    install_reason = "dry-run approval token is not allowed to mutate state"
                else:
                    plan = run_json(install_args(BASE_DIR, args, skill_dir, apply=True, approval=approval), check=False)
                    install_status = "installed" if plan.get("installed") else "install-blocked"
                    if not plan.get("installed"):
                        install_reason = plan.get("reason", install_reason)
            else:
                install_status = f"telegram-{approval.get('status', 'declined')}"

    payload = {
        "status": "ok" if report["valid"] else "needs-review",
        "routed_to": "forge",
        "routing": routing,
        "opportunity": opportunity,
        "skill_dir": skill_dir,
        "validation": report,
        "evaluation": evaluation,
        "agent_authorization": agent_policy,
        "approval": approval,
        "install_status": install_status,
        "install_reason": install_reason,
        "install_plan": plan,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
