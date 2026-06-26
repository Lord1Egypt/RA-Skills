#!/usr/bin/env python3
"""
build-project-glossary.py — Build glossaries for all Telegram projects.

Scans each project's knowledge.md and generates a structured glossary.md
that the agent uses for Tier 2/3 knowledge extraction.

Usage:
    python3 scripts/build-project-glossary.py              # All projects
    python3 scripts/build-project-glossary.py --project ID  # Specific project
"""

import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

PROJECTS_DIR = os.path.expanduser("~/.openclaw/workspace/projects")
PROJECTS_MD = os.path.expanduser("~/.openclaw/workspace/PROJECTS.md")


def estimate_tokens(text):
    """Rough token estimate: ~3.5 chars per token for mixed en/de."""
    return len(text) / 3.5


def get_tier(tokens):
    if tokens < 5000:
        return 1
    elif tokens < 20000:
        return 2
    return 3


def parse_knowledge(knowledge_path):
    """Parse knowledge.md into entries."""
    if not os.path.exists(knowledge_path):
        return []

    content = Path(knowledge_path).read_text(encoding="utf-8")
    entries = []

    # Split by ## Entry: headers
    parts = re.split(r'^## Entry: (.+)$', content, flags=re.MULTILINE)

    # parts[0] is header, then alternating title/content
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        tokens = int(estimate_tokens(body))
        entries.append({
            "title": title,
            "body": body[:500],  # First 500 chars for glossary summary
            "tokens": tokens,
        })

    return entries


def extract_concepts(entries):
    """Extract key concepts, people, and decisions from entries."""
    concepts = []
    people = []
    decisions = []

    for entry in entries:
        body = entry["body"]

        # Simple extraction: lines starting with - or * that look like key points
        for line in body.split("\n"):
            line = line.strip()
            if line.startswith(("- **", "* **")):
                concepts.append(line)
            if "decided" in line.lower() or "entschieden" in line.lower() or "regel:" in line.lower():
                decisions.append(f"[{entry['title']}] {line}")

    return concepts[:20], people[:10], decisions[:10]


def build_glossary(project_dir):
    """Build glossary.md for a single project."""
    knowledge_path = os.path.join(project_dir, "knowledge.md")
    glossary_path = os.path.join(project_dir, "glossary.md")
    project_path = os.path.join(project_dir, "project.md")

    entries = parse_knowledge(knowledge_path)
    if not entries:
        # Write empty glossary
        Path(glossary_path).write_text(
            "# Project Glossary\n\n_No knowledge entries yet._\n",
            encoding="utf-8"
        )
        return 0

    total_tokens = sum(e["tokens"] for e in entries)
    tier = get_tier(total_tokens)
    concepts, people, decisions = extract_concepts(entries)

    lines = [
        "# Project Glossary",
        f"",
        f"_Auto-generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
        f"Entries: {len(entries)} | Tokens: ~{total_tokens:,} | Tier: {tier}_",
        "",
        "## Entries Overview",
        "",
    ]

    for e in entries:
        summary = e["body"][:200].replace("\n", " ")
        lines.append(f"### {e['title']}")
        lines.append(f"_~{e['tokens']} tokens_")
        lines.append(f"{summary}...")
        lines.append("")

    if concepts:
        lines.append("## Key Concepts")
        lines.append("")
        for c in concepts:
            lines.append(c)
        lines.append("")

    if decisions:
        lines.append("## Decisions & Rules")
        lines.append("")
        for d in decisions:
            lines.append(f"- {d}")
        lines.append("")

    Path(glossary_path).write_text("\n".join(lines), encoding="utf-8")
    return total_tokens


def update_projects_md():
    """Update PROJECTS.md with current project stats."""
    if not os.path.exists(PROJECTS_DIR):
        return

    projects = []
    for chat_id in os.listdir(PROJECTS_DIR):
        project_dir = os.path.join(PROJECTS_DIR, chat_id)
        if not os.path.isdir(project_dir):
            continue

        knowledge_path = os.path.join(project_dir, "knowledge.md")
        project_path = os.path.join(project_dir, "project.md")

        # Get project name from project.md
        name = chat_id
        if os.path.exists(project_path):
            content = Path(project_path).read_text(encoding="utf-8")
            match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if match:
                name = match.group(1)

        # Get knowledge size
        tokens = 0
        if os.path.exists(knowledge_path):
            content = Path(knowledge_path).read_text(encoding="utf-8")
            tokens = int(estimate_tokens(content))

        tier = get_tier(tokens)
        size_str = f"~{tokens:,} tokens" if tokens > 0 else "0 KB"
        projects.append((chat_id, name, size_str, tier, f"projects/{chat_id}/"))

    # Rebuild the table in PROJECTS.md
    if os.path.exists(PROJECTS_MD):
        content = Path(PROJECTS_MD).read_text(encoding="utf-8")

        # Replace the table
        table_lines = [
            "| Chat ID | Project Name | Knowledge Size | Tier | Path |",
            "|---------|-------------|----------------|------|------|",
        ]
        if projects:
            for chat_id, name, size, tier, path in projects:
                table_lines.append(f"| {chat_id} | {name} | {size} | {tier} | {path} |")
        else:
            table_lines.append("| _(none yet)_ | | | | |")

        # Find and replace table
        table_pattern = r'\| Chat ID \|.*?\n\|[-| ]+\n(?:\|.*\n)*'
        new_table = "\n".join(table_lines) + "\n"
        content = re.sub(table_pattern, new_table, content)

        Path(PROJECTS_MD).write_text(content, encoding="utf-8")


def main():
    project_filter = None
    if "--project" in sys.argv:
        idx = sys.argv.index("--project")
        if idx + 1 < len(sys.argv):
            project_filter = sys.argv[idx + 1]

    if not os.path.exists(PROJECTS_DIR):
        print("No projects directory found.")
        return

    total = 0
    for chat_id in os.listdir(PROJECTS_DIR):
        if project_filter and chat_id != project_filter:
            continue

        project_dir = os.path.join(PROJECTS_DIR, chat_id)
        if not os.path.isdir(project_dir):
            continue

        tokens = build_glossary(project_dir)
        print(f"  ✓ {chat_id}: glossary built ({tokens:,} tokens)")
        total += 1

    update_projects_md()
    print(f"\nDone. {total} project(s) processed. PROJECTS.md updated.")


if __name__ == "__main__":
    main()
