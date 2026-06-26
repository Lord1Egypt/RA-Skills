#!/usr/bin/env python3
"""
session-bridge — Context Capsule manager for OpenClaw.

Bridges context across surfaces (Telegram/WhatsApp/TUI) and agents
using lightweight topic-keyed JSON capsules.

Usage:
  bridge.py create  --topic <id> [--source <session-key>] [--agent <agent-id>]
  bridge.py refresh --topic <id>
  bridge.py hydrate --topic <id> [--into <session-key>]
  bridge.py handoff --topic <id> --to <session-key>
  bridge.py status  [--topic <id>]
  bridge.py list
  bridge.py expire  [--max-age-hours 24]
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", Path.home() / ".openclaw/workspace"))
BRIDGES_DIR = WORKSPACE / "tasks" / "bridges"
BRIDGES_DIR.mkdir(parents=True, exist_ok=True)

# ─── Capsule schema ───────────────────────────────────────────────────────────

CAPSULE_VERSION = "1.0"

def capsule_path(topic: str) -> Path:
    safe = topic.replace("/", "--").replace(":", "-").replace(" ", "_")
    return BRIDGES_DIR / f"{safe}.json"

def capsule_md_path(topic: str) -> Path:
    return capsule_path(topic).with_suffix(".md")

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def load_capsule(topic: str) -> dict | None:
    p = capsule_path(topic)
    if not p.exists():
        return None
    with open(p) as f:
        return json.load(f)

def save_capsule(capsule: dict):
    topic = capsule["topic"]
    p = capsule_path(topic)
    capsule["updated"] = now_iso()
    with open(p, "w") as f:
        json.dump(capsule, f, indent=2, ensure_ascii=False)
    render_markdown(capsule)
    return p

def render_markdown(capsule: dict):
    """Write a human-readable .md alongside the JSON capsule."""
    md_p = capsule_md_path(capsule["topic"])
    lines = [
        f"# Session Bridge: {capsule['topic']}",
        f"",
        f"**Status:** {capsule.get('status', 'unknown')}  ",
        f"**Updated:** {capsule.get('updated', '?')}  ",
        f"**Expires after:** {capsule.get('freshness_hours', 24)}h  ",
        f"",
    ]
    if capsule.get("goal"):
        lines += [f"## Goal", f"{capsule['goal']}", ""]
    if capsule.get("decisions"):
        lines += ["## Decisions Made"]
        for d in capsule["decisions"]:
            lines.append(f"- {d}")
        lines.append("")
    if capsule.get("open_questions"):
        lines += ["## Open Questions"]
        for q in capsule["open_questions"]:
            lines.append(f"- {q}")
        lines.append("")
    if capsule.get("next_action"):
        lines += [f"## Next Action", f"{capsule['next_action']}", ""]
    if capsule.get("key_facts"):
        lines += ["## Key Facts"]
        for kf in capsule["key_facts"]:
            lines.append(f"- {kf}")
        lines.append("")
    if capsule.get("linked_sessions"):
        lines += ["## Linked Sessions"]
        for s in capsule["linked_sessions"]:
            lines.append(f"- `{s}`")
        lines.append("")
    with open(md_p, "w") as f:
        f.write("\n".join(lines))

def new_capsule(topic: str, goal: str = "", source_session: str = "", agent: str = "") -> dict:
    return {
        "version": CAPSULE_VERSION,
        "topic": topic,
        "status": "active",
        "goal": goal,
        "decisions": [],
        "open_questions": [],
        "key_facts": [],
        "next_action": "",
        "linked_sessions": [source_session] if source_session else [],
        "owner_agent": agent or "main",
        "freshness_hours": 24,
        "created": now_iso(),
        "updated": now_iso(),
        "confidence": "medium",
    }

def is_stale(capsule: dict) -> bool:
    updated = datetime.fromisoformat(capsule.get("updated", capsule.get("created", now_iso())))
    if updated.tzinfo is None:
        updated = updated.replace(tzinfo=timezone.utc)
    max_age = timedelta(hours=capsule.get("freshness_hours", 24))
    return (datetime.now(timezone.utc) - updated) > max_age

def brief(capsule: dict, max_tokens: int = 350) -> str:
    """Generate a compact hydration briefing (~150-350 tokens)."""
    stale_warn = " ⚠️ (stale)" if is_stale(capsule) else ""
    parts = [
        f"[Session Bridge{stale_warn}] Topic: {capsule['topic']}",
        f"Status: {capsule.get('status', '?')}",
    ]
    if capsule.get("goal"):
        parts.append(f"Goal: {capsule['goal']}")
    if capsule.get("decisions"):
        parts.append("Decisions: " + "; ".join(capsule["decisions"][:3]))
    if capsule.get("open_questions"):
        parts.append("Open: " + "; ".join(capsule["open_questions"][:2]))
    if capsule.get("next_action"):
        parts.append(f"Next: {capsule['next_action']}")
    if capsule.get("linked_sessions"):
        parts.append(f"Sources: {', '.join(capsule['linked_sessions'][:2])}")
    parts.append(f"Updated: {capsule.get('updated', '?')[:16]}Z")
    return "\n".join(parts)

# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_create(args):
    existing = load_capsule(args.topic)
    if existing and not args.force:
        print(f"Capsule already exists for '{args.topic}'. Use --force to overwrite or 'refresh' to update.")
        sys.exit(1)
    capsule = new_capsule(
        topic=args.topic,
        goal=args.goal or "",
        source_session=args.source or "",
        agent=args.agent or "",
    )
    if args.status:
        capsule["status"] = args.status
    p = save_capsule(capsule)
    print(f"✔ Created capsule: {p}")
    print(f"  Markdown view:   {capsule_md_path(args.topic)}")
    print(f"\nEdit the JSON to add decisions, key_facts, next_action, open_questions.")

def cmd_refresh(args):
    capsule = load_capsule(args.topic)
    if not capsule:
        print(f"No capsule found for '{args.topic}'. Use 'create' first.")
        sys.exit(1)
    if args.status:
        capsule["status"] = args.status
    if args.goal:
        capsule["goal"] = args.goal
    if args.next_action:
        capsule["next_action"] = args.next_action
    if args.add_decision:
        capsule.setdefault("decisions", [])
        for d in args.add_decision:
            if d not in capsule["decisions"]:
                capsule["decisions"].append(d)
    if args.add_question:
        capsule.setdefault("open_questions", [])
        for q in args.add_question:
            if q not in capsule["open_questions"]:
                capsule["open_questions"].append(q)
    if args.add_fact:
        capsule.setdefault("key_facts", [])
        for f in args.add_fact:
            if f not in capsule["key_facts"]:
                capsule["key_facts"].append(f)
    if args.link_session:
        capsule.setdefault("linked_sessions", [])
        if args.link_session not in capsule["linked_sessions"]:
            capsule["linked_sessions"].append(args.link_session)
    if args.freshness_hours:
        capsule["freshness_hours"] = args.freshness_hours
    p = save_capsule(capsule)
    print(f"✔ Refreshed capsule: {p}")

def cmd_hydrate(args):
    """Print a brief that can be injected into a session at start."""
    capsule = load_capsule(args.topic)
    if not capsule:
        print(f"No capsule found for '{args.topic}'.")
        sys.exit(1)
    b = brief(capsule)
    print(b)
    # If --into is given, we emit instructions for the agent
    if args.into:
        print(f"\n→ Inject the above into session: {args.into}")
        print(f"  Use sessions_send(sessionKey='{args.into}', message=<brief above>)")

def cmd_handoff(args):
    """Generate a handoff message for cross-agent delivery."""
    capsule = load_capsule(args.topic)
    if not capsule:
        print(f"No capsule found for '{args.topic}'.")
        sys.exit(1)
    b = brief(capsule)
    capsule_file = capsule_path(args.topic)
    msg = f"""{b}

Capsule path: {capsule_file}
→ Use sessions_send to deliver this to: {args.to}"""
    print(msg)

def cmd_status(args):
    if args.topic:
        capsule = load_capsule(args.topic)
        if not capsule:
            print(f"No capsule found for '{args.topic}'.")
            sys.exit(1)
        stale = "⚠️  STALE" if is_stale(capsule) else "✔ fresh"
        print(f"Topic:    {capsule['topic']}")
        print(f"Status:   {capsule['status']}  [{stale}]")
        print(f"Updated:  {capsule.get('updated', '?')}")
        print(f"Goal:     {capsule.get('goal', '(none)')}")
        print(f"Next:     {capsule.get('next_action', '(none)')}")
        print(f"Decisions ({len(capsule.get('decisions', []))}):")
        for d in capsule.get("decisions", []):
            print(f"  - {d}")
        print(f"Open questions ({len(capsule.get('open_questions', []))}):")
        for q in capsule.get("open_questions", []):
            print(f"  - {q}")
    else:
        cmd_list(args)

def cmd_list(args):
    capsules = sorted(BRIDGES_DIR.glob("*.json"))
    if not capsules:
        print("No capsules found.")
        return
    print(f"{'Topic':<40} {'Status':<12} {'Fresh?':<8} Updated")
    print("-" * 80)
    for p in capsules:
        try:
            with open(p) as f:
                c = json.load(f)
            stale = "stale" if is_stale(c) else "ok"
            print(f"{c.get('topic','?'):<40} {c.get('status','?'):<12} {stale:<8} {c.get('updated','?')[:16]}")
        except Exception:
            print(f"{p.name:<40} (unreadable)")

def cmd_expire(args):
    max_age = timedelta(hours=args.max_age_hours)
    removed = 0
    for p in BRIDGES_DIR.glob("*.json"):
        try:
            with open(p) as f:
                c = json.load(f)
            updated = datetime.fromisoformat(c.get("updated", c.get("created", now_iso())))
            if updated.tzinfo is None:
                updated = updated.replace(tzinfo=timezone.utc)
            if (datetime.now(timezone.utc) - updated) > max_age:
                p.unlink()
                md = p.with_suffix(".md")
                if md.exists():
                    md.unlink()
                print(f"Expired: {c.get('topic', p.name)}")
                removed += 1
        except Exception:
            pass
    print(f"✔ Expired {removed} capsule(s).")

# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Session Bridge — context capsule manager for OpenClaw"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # create
    p_create = sub.add_parser("create", help="Create a new context capsule")
    p_create.add_argument("--topic", required=True, help="Topic/thread ID (e.g. project:looking-glass)")
    p_create.add_argument("--source", default="", help="Source session key")
    p_create.add_argument("--agent", default="", help="Owner agent ID")
    p_create.add_argument("--goal", default="", help="Goal/intent of this context thread")
    p_create.add_argument("--status", default="active", help="Status (active/paused/done)")
    p_create.add_argument("--force", action="store_true", help="Overwrite existing capsule")

    # refresh
    p_refresh = sub.add_parser("refresh", help="Update an existing capsule")
    p_refresh.add_argument("--topic", required=True)
    p_refresh.add_argument("--status")
    p_refresh.add_argument("--goal")
    p_refresh.add_argument("--next-action")
    p_refresh.add_argument("--add-decision", action="append", metavar="DECISION")
    p_refresh.add_argument("--add-question", action="append", metavar="QUESTION")
    p_refresh.add_argument("--add-fact", action="append", metavar="FACT")
    p_refresh.add_argument("--link-session", metavar="SESSION_KEY")
    p_refresh.add_argument("--freshness-hours", type=int)

    # hydrate
    p_hydrate = sub.add_parser("hydrate", help="Print a session-start briefing")
    p_hydrate.add_argument("--topic", required=True)
    p_hydrate.add_argument("--into", default="", help="Target session key (for routing hint)")

    # handoff
    p_handoff = sub.add_parser("handoff", help="Generate a cross-agent handoff message")
    p_handoff.add_argument("--topic", required=True)
    p_handoff.add_argument("--to", required=True, help="Target session key")

    # status
    p_status = sub.add_parser("status", help="Show capsule status")
    p_status.add_argument("--topic", default="", help="Topic ID (omit for all)")

    # list
    sub.add_parser("list", help="List all capsules")

    # expire
    p_expire = sub.add_parser("expire", help="Remove stale capsules")
    p_expire.add_argument("--max-age-hours", type=int, default=24)

    args = parser.parse_args()

    dispatch = {
        "create": cmd_create,
        "refresh": cmd_refresh,
        "hydrate": cmd_hydrate,
        "handoff": cmd_handoff,
        "status": cmd_status,
        "list": cmd_list,
        "expire": cmd_expire,
    }
    dispatch[args.command](args)

if __name__ == "__main__":
    main()
