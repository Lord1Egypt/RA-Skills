#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import re
import urllib.request
from pathlib import Path


DEFAULT_TARGET_ROOT = Path.home() / ".openclaw" / "workspace" / "skills"
DEFAULT_FEEDBACK_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-feedback.jsonl"
DEFAULT_REPLAY_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-replay-cases.jsonl"
DEFAULT_REPORT_ROOT = Path.home() / ".openclaw" / "workspace" / ".learnings" / "somnia-nightly"
DEFAULT_UPDATE_ROOT = Path.home() / ".openclaw" / "workspace" / "somnia-proposals"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def date_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d-%H%M%S")


def load_env_file(path: str) -> None:
    if not path:
        return
    env_path = Path(path).expanduser()
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def load_manifest(target_root: Path) -> dict:
    path = target_root / ".skill-forge-installs.json"
    if not path.exists():
        return {"installs": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"installs": {}, "manifest_error": "invalid-json"}


def parse_frontmatter(content: str) -> dict:
    if not content.startswith("---"):
        return {}
    match = re.match(r"(?s)^---\n(.*?)\n---", content)
    if not match:
        return {}
    metadata = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"').strip("'")
    return metadata


def skill_dirs(target_root: Path, manifest: dict, feedback_entries: list[dict], scope: str) -> dict[str, Path]:
    result = {}
    if scope == "all" and target_root.exists():
        for path in sorted(target_root.iterdir()):
            if path.name.startswith("."):
                continue
            if (path / "SKILL.md").exists():
                result[path.name] = path.resolve()
    if scope == "managed":
        for name, record in manifest.get("installs", {}).items():
            target = Path(record.get("target", "")).expanduser()
            source = Path(record.get("source", "")).expanduser()
            for candidate in [target, source, target_root / name]:
                if candidate and (candidate / "SKILL.md").exists():
                    result.setdefault(name, candidate.resolve())
                    break
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


def validate_skill(path: Path) -> dict:
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        return {"valid": False, "score": 0, "grade": "missing", "issues": ["missing_skill_md"]}
    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    metadata = parse_frontmatter(content)
    issues = []
    score = 100
    if not metadata.get("name"):
        issues.append("missing_name")
        score -= 25
    if len(metadata.get("description", "")) < 40:
        issues.append("weak_description")
        score -= 20
    if "## Trigger" not in content and "Use this skill when" not in content:
        issues.append("missing_trigger_guidance")
        score -= 15
    if "```" in content and "Scripts:" not in content and "Commands" not in content:
        issues.append("commands_not_summarized")
        score -= 10
    score = max(score, 0)
    grade = "milestone" if score >= 90 else "usable" if score >= 75 else "needs-work"
    return {"valid": score >= 75, "score": score, "grade": grade, "issues": issues, "metadata": metadata}


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


def replay_summary(entries: list[dict], skill: str, enabled: bool) -> dict:
    if not enabled:
        return {"status": "not-run", "cases_run": 0, "details_hidden": True}
    cases = [entry for entry in entries if entry.get("skill") == skill]
    return {
        "status": "available" if cases else "not-run",
        "cases_run": len(cases),
        "details_hidden": True,
    }


def issue_list(validation: dict, replay: dict, feedback: dict, args: argparse.Namespace) -> list[str]:
    issues = []
    if not validation.get("valid"):
        issues.append("validation_failed")
    if int(validation.get("score", 0)) < args.min_score:
        issues.append("low_validation_score")
    if feedback["negative"] >= args.negative_feedback_threshold:
        issues.append("negative_feedback")
    if feedback["total"] >= args.feedback_threshold:
        issues.append("feedback_available")
    if replay.get("cases_run", 0) > 0:
        issues.append("replay_cases_available")
    return issues


def write_update_proposal(skill: str, skill_path: Path, issues: list[str], feedback: dict, args: argparse.Namespace) -> dict:
    if not args.propose_updates:
        return {"status": "disabled"}
    if not issues and feedback["total"] < args.feedback_threshold:
        return {"status": "not-needed"}
    proposal_root = Path(args.update_output).expanduser().resolve() / date_stamp() / skill
    proposal_root.mkdir(parents=True, exist_ok=True)
    proposal = proposal_root / "PROPOSAL.md"
    proposal.write_text(
        "\n".join(
            [
                f"# Somnia Proposal: {skill}",
                "",
                "Somnia does not mutate installed skills. This proposal is a review artifact for Skill Forge or a human maintainer.",
                "",
                f"- source: `{skill_path}`",
                f"- issues: {', '.join(issues) or 'none'}",
                f"- feedback_total: {feedback['total']}",
                f"- feedback_negative: {feedback['negative']}",
                "",
                "Next step: inspect this proposal and run Skill Forge with Telegram approval if an update is justified.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    install_status = "planned" if args.update_install == "plan" else "blocked"
    return {"status": "proposed", "proposal": str(proposal), "install_status": install_status}


def build_markdown(report: dict) -> str:
    lines = [
        "# Somnia Nightly Review",
        "",
        f"- created_at: {report['created_at']}",
        f"- scope: {report['scope']}",
        f"- skills_checked: {report['summary']['skills_checked']}",
        f"- needs_attention: {report['summary']['needs_attention']}",
        f"- proposals_written: {report['summary']['proposals_written']}",
        "",
        "## Findings",
        "",
    ]
    for item in report["skills"]:
        status = "needs-attention" if item["issues"] else "ok"
        lines.extend(
            [
                f"### {item['skill']}",
                "",
                f"- status: {status}",
                f"- validation: {item['validation'].get('grade')} / {item['validation'].get('score')}",
                f"- replay: {item['replay_summary'].get('status', 'not-run')}",
                f"- feedback: total={item['feedback']['total']} negative={item['feedback']['negative']}",
                f"- issues: {', '.join(item['issues']) or 'none'}",
                f"- proposal_status: {item['proposal'].get('status')}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def send_telegram_report(markdown: str, args: argparse.Namespace) -> dict:
    token = os.getenv(args.telegram_bot_token_env)
    chat_id = os.getenv(args.telegram_chat_id_env)
    if not token or not chat_id:
        return {"sent": False, "status": "missing-config"}
    text = markdown if len(markdown) <= 3900 else markdown[:3800].rstrip() + "\n\n[truncated]"
    body = json.dumps({"chat_id": chat_id, "text": text, "disable_web_page_preview": True}).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return {"sent": True, "status": "sent", "message_id": payload.get("result", {}).get("message_id")}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run standalone Somnia skill health review.")
    parser.add_argument("--target-root", default=str(DEFAULT_TARGET_ROOT))
    parser.add_argument("--feedback-file", default=str(DEFAULT_FEEDBACK_FILE))
    parser.add_argument("--replay-cases", default=str(DEFAULT_REPLAY_FILE))
    parser.add_argument("--report-root", default=str(DEFAULT_REPORT_ROOT))
    parser.add_argument("--update-output", default=str(DEFAULT_UPDATE_ROOT))
    parser.add_argument("--scope", choices=["managed", "feedback", "all"], default="managed")
    parser.add_argument("--min-score", type=int, default=85)
    parser.add_argument("--feedback-threshold", type=int, default=1)
    parser.add_argument("--negative-feedback-threshold", type=int, default=1)
    parser.add_argument("--feedback-limit", type=int, default=20)
    parser.add_argument("--replay", choices=["off", "hidden"], default="hidden")
    parser.add_argument("--min-replay-score", type=int, default=70)
    parser.add_argument("--propose-updates", action="store_true")
    parser.add_argument("--update-install", choices=["plan", "telegram"], default="plan")
    parser.add_argument("--agent-name", default="")
    parser.add_argument("--telegram-report", action="store_true")
    parser.add_argument("--telegram-timeout", type=int, default=300)
    parser.add_argument("--telegram-bot-token-env", default="TELEGRAM_BOT_TOKEN")
    parser.add_argument("--telegram-chat-id-env", default="TELEGRAM_CHAT_ID")
    parser.add_argument("--telegram-dry-run", choices=["off", "approve", "reject", "timeout"], default="off")
    parser.add_argument("--env-file", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    load_env_file(args.env_file)
    target_root = Path(args.target_root).expanduser().resolve()
    feedback_file = Path(args.feedback_file).expanduser().resolve()
    replay_file = Path(args.replay_cases).expanduser().resolve()
    report_root = Path(args.report_root).expanduser().resolve()
    report_root.mkdir(parents=True, exist_ok=True)

    feedback_entries = read_jsonl(feedback_file)
    replay_entries = read_jsonl(replay_file)
    manifest = load_manifest(target_root)
    skills = []
    proposals_written = 0

    for skill, path in skill_dirs(target_root, manifest, feedback_entries, args.scope).items():
        validation = validate_skill(path)
        feedback = feedback_summary(feedback_entries, skill)
        replay = replay_summary(replay_entries, skill, args.replay != "off")
        issues = issue_list(validation, replay, feedback, args)
        proposal = write_update_proposal(skill, path, issues, feedback, args)
        if proposal.get("status") == "proposed":
            proposals_written += 1
        skills.append(
            {
                "skill": skill,
                "path": str(path),
                "validation": validation,
                "replay_summary": replay,
                "feedback": feedback,
                "issues": issues,
                "proposal": proposal,
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
            "proposals_written": proposals_written,
        },
        "skills": skills,
    }
    stem = f"somnia-review-{date_stamp()}"
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
