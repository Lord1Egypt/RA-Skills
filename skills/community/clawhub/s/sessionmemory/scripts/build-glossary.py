#!/usr/bin/env python3
"""
Session Glossary Builder
Scans session transcripts and builds a structured glossary index.
Designed to run periodically (cron) to keep the glossary up-to-date.

Output: memory/SESSION-GLOSSAR.md - a structured index of all sessions,
tagged by people, projects, decisions, tools, and key events.

Usage:
  python3 scripts/build-glossary.py                    # Full rebuild
  python3 scripts/build-glossary.py --incremental      # Only new sessions
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path(os.environ.get("WORKSPACE", Path.home() / ".openclaw" / "workspace"))
SESSIONS_DIR = WORKSPACE / "memory" / "sessions"
GLOSSARY_PATH = WORKSPACE / "memory" / "SESSION-GLOSSAR.md"
STATE_PATH = WORKSPACE / "memory" / ".glossary-state.json"


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"processed_files": [], "last_run": None}


def save_state(state):
    state["last_run"] = datetime.now().isoformat()
    STATE_PATH.write_text(json.dumps(state, indent=2))


def extract_entities(text):
    """Extract people, projects, decisions, and topics from text."""
    entities = {
        "people": set(),
        "projects": set(),
        "decisions": set(),
        "topics": set(),
    }

    # Find @mentions and names after "User:" or "**Name**:"
    for match in re.finditer(r'\*\*(\w[\w\s]{1,30})\*\*:', text):
        name = match.group(1).strip()
        if name not in ("User", "Assistant", "System", "toolResult"):
            entities["people"].add(name)

    # Find project-like references
    for match in re.finditer(r'(?:project|projekt|gruppe|group)[:\s]+["\']?([^"\';\n]{3,50})', text, re.I):
        entities["projects"].add(match.group(1).strip())

    # Find decision patterns
    for match in re.finditer(r'(?:decided|entschieden|beschlossen|agreed|decision)[:\s]+(.{10,100}?)(?:\.|$)', text, re.I):
        entities["decisions"].add(match.group(1).strip())

    return entities


def build_glossary(sessions_dir, incremental=False):
    state = load_state()
    processed = set(state.get("processed_files", []))

    all_entities = {
        "people": defaultdict(list),
        "projects": defaultdict(list),
        "decisions": [],
        "sessions": [],
    }

    session_files = sorted(sessions_dir.glob("session-*.md"))

    for session_file in session_files:
        fname = session_file.name

        if incremental and fname in processed:
            continue

        text = session_file.read_text(errors="replace")

        # Extract session metadata
        session_date = "unknown"
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', fname)
        if date_match:
            session_date = date_match.group(1)

        # Get first meaningful line as topic
        lines = [l.strip() for l in text.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('_')]
        topic_preview = lines[0][:100] if lines else "No preview"

        entities = extract_entities(text)

        # Store entities with session reference
        for person in entities["people"]:
            all_entities["people"][person].append((session_date, fname))

        for project in entities["projects"]:
            all_entities["projects"][project].append((session_date, fname))

        for decision in entities["decisions"]:
            all_entities["decisions"].append((session_date, decision, fname))

        all_entities["sessions"].append({
            "file": fname,
            "date": session_date,
            "preview": topic_preview,
            "word_count": len(text.split()),
        })

        processed.add(fname)

    # Build glossary markdown
    lines = [
        "# Session Glossary (auto-generated)",
        f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        f"_Sessions indexed: {len(all_entities['sessions'])}_\n",
    ]

    # People section
    if all_entities["people"]:
        lines.append("## People\n")
        for person, refs in sorted(all_entities["people"].items()):
            dates = sorted(set(d for d, _ in refs))
            lines.append(f"- **{person}** - seen in {len(refs)} sessions ({', '.join(dates[-3:])})")
        lines.append("")

    # Projects section
    if all_entities["projects"]:
        lines.append("## Projects\n")
        for project, refs in sorted(all_entities["projects"].items()):
            dates = sorted(set(d for d, _ in refs))
            lines.append(f"- **{project}** - {len(refs)} mentions ({', '.join(dates[-3:])})")
        lines.append("")

    # Recent decisions
    if all_entities["decisions"]:
        lines.append("## Key Decisions (recent)\n")
        for date, decision, fname in sorted(all_entities["decisions"], reverse=True)[:20]:
            lines.append(f"- [{date}] {decision}")
        lines.append("")

    # Session index
    lines.append("## Session Index\n")
    for s in sorted(all_entities["sessions"], key=lambda x: x["date"], reverse=True)[:50]:
        lines.append(f"- **{s['date']}** ({s['word_count']} words) - {s['preview'][:80]}")
        lines.append(f"  _File: {s['file']}_")

    glossary_text = "\n".join(lines)
    GLOSSARY_PATH.write_text(glossary_text)
    print(f"Glossary written: {len(all_entities['sessions'])} sessions, "
          f"{len(all_entities['people'])} people, {len(all_entities['projects'])} projects")

    state["processed_files"] = list(processed)
    save_state(state)


def main():
    incremental = "--incremental" in sys.argv
    os.makedirs(SESSIONS_DIR, exist_ok=True)
    build_glossary(SESSIONS_DIR, incremental=incremental)


if __name__ == "__main__":
    main()
