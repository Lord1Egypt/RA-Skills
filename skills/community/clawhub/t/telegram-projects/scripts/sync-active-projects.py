#!/usr/bin/env python3
"""
sync-active-projects.py — Update SOUL.md with active Telegram projects.

Scans PROJECTS.md for all registered projects, checks which ones had
activity in the last 4 weeks (based on session JSONL modification times),
and updates the project list in SOUL.md.

Also adds any Telegram group sessions that became active but aren't
registered as projects yet (marks them as "no project yet").

Run daily via cron.
"""

import os
import re
import json
import time
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SOUL_MD = os.path.join(WORKSPACE, "SOUL.md")
PROJECTS_MD = os.path.join(WORKSPACE, "PROJECTS.md")
PROJECTS_DIR = os.path.join(WORKSPACE, "projects")
SESSIONS_DIR = os.path.expanduser("~/.openclaw/agents/main/sessions")

ACTIVE_WINDOW_DAYS = 28  # 4 weeks


def get_session_activity():
    """Find all group sessions and their last activity time from sessions.json."""
    activity = {}
    sessions_json = os.path.join(SESSIONS_DIR, "sessions.json")

    if not os.path.exists(sessions_json):
        return activity

    cutoff_ms = (time.time() - (ACTIVE_WINDOW_DAYS * 86400)) * 1000

    with open(sessions_json) as f:
        data = json.load(f)

    for key, info in data.items():
        # Match telegram group sessions: agent:main:telegram:group:-NNNN
        # But not topic sub-sessions (agent:main:telegram:group:-NNNN:topic:N)
        if ":telegram:group:" not in key:
            continue

        parts = key.split(":")
        # Find the chat ID (negative number after "group")
        try:
            group_idx = parts.index("group")
            chat_id = parts[group_idx + 1]
        except (ValueError, IndexError):
            continue

        # Skip topic sub-sessions
        if "topic" in parts:
            continue

        updated_at = info.get("updatedAt", 0)
        if updated_at < cutoff_ms:
            continue

        display_name = info.get("displayName", chat_id)
        # Clean display name: "telegram:g-faya-golem_content" → "FAYA-GOLEM_content"
        clean_name = display_name.replace("telegram:g-", "").replace("telegram:", "")

        activity[chat_id] = {
            "last_active": datetime.fromtimestamp(updated_at / 1000).strftime("%Y-%m-%d"),
            "session_id": info.get("sessionId", ""),
            "display_name": clean_name,
        }

    return activity


def get_registered_projects():
    """Read PROJECTS.md and get registered projects."""
    projects = {}
    if not os.path.exists(PROJECTS_MD):
        return projects

    content = Path(PROJECTS_MD).read_text(encoding="utf-8")

    # Parse table rows
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("|") and not line.startswith("| Chat ID") and not line.startswith("|---"):
            cols = [c.strip() for c in line.split("|")[1:-1]]
            if len(cols) >= 4 and cols[0] != "_(none yet)_":
                chat_id = cols[0]
                projects[chat_id] = {
                    "name": cols[1],
                    "size": cols[2],
                    "tier": cols[3],
                }

    return projects


def get_project_name(chat_id):
    """Try to get a project name from project.md or return chat_id."""
    project_md = os.path.join(PROJECTS_DIR, chat_id, "project.md")
    if os.path.exists(project_md):
        content = Path(project_md).read_text(encoding="utf-8")
        match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if match:
            return match.group(1)
    return chat_id


def get_knowledge_size(chat_id):
    """Get knowledge size for a project."""
    knowledge_md = os.path.join(PROJECTS_DIR, chat_id, "knowledge.md")
    if os.path.exists(knowledge_md):
        content = Path(knowledge_md).read_text(encoding="utf-8")
        tokens = int(len(content) / 3.5)
        if tokens < 5000:
            return f"~{tokens:,} tokens", "1"
        elif tokens < 20000:
            return f"~{tokens:,} tokens", "2"
        else:
            return f"~{tokens:,} tokens", "3"
    return "0", "-"


def update_soul_md(active_projects):
    """Update the Telegram Projects section in SOUL.md with active project list."""
    if not os.path.exists(SOUL_MD):
        print("SOUL.md not found!")
        return False

    content = Path(SOUL_MD).read_text(encoding="utf-8")

    # Build the new section
    new_section_lines = [
        "## Telegram Projects (always active)",
        "",
        "Every Telegram group can be a project with permanent knowledge. On **every message in a Telegram group:**",
        "",
        "1. Check `PROJECTS.md` for the current chat-id",
        '2. **If project exists:** Read `projects/{chat-id}/project.md` (always). Load `knowledge.md` per tier:',
        "   - **Tier 1 (< 5K tokens):** Load ALL knowledge",
        "   - **Tier 2 (5-20K):** Read glossary, extract ~5K relevant tokens for the current message",
        "   - **Tier 3 (> 20K):** Read glossary, extract 5-10K relevant tokens + vector search on demand",
        "3. **If no project exists:** Mention once per session that this channel can become a project",
        "4. Report knowledge size on first message after >1h pause: `📁 Project [name]: [size] loaded (Tier X)`",
        "5. For `/knowledge` or `/project` commands → read the `telegram-projects` SKILL.md for detailed rules",
        "",
        'Users add knowledge by saying "permanentes Knowledge: ..." or `/knowledge add [content]`.',
    ]

    if active_projects:
        new_section_lines.append("")
        new_section_lines.append("### Active Projects (last 4 weeks)")
        new_section_lines.append("")
        new_section_lines.append("| Chat ID | Name | Knowledge | Tier | Last Active |")
        new_section_lines.append("|---------|------|-----------|------|-------------|")
        for p in active_projects:
            new_section_lines.append(
                f"| {p['chat_id']} | {p['name']} | {p['size']} | {p['tier']} | {p['last_active']} |"
            )

    new_section = "\n".join(new_section_lines)

    # Replace the section between "## Telegram Projects" and the next "## " header
    pattern = r'## Telegram Projects \(always active\).*?(?=\n## (?!#))'
    replacement = new_section + "\n\n"

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        print("Warning: Could not find/replace Telegram Projects section in SOUL.md")
        return False

    Path(SOUL_MD).write_text(new_content, encoding="utf-8")
    return True


def main():
    print(f"Syncing active projects (window: {ACTIVE_WINDOW_DAYS} days)...")

    # Get all recent group activity
    activity = get_session_activity()
    print(f"Found {len(activity)} active Telegram group sessions")

    # Get registered projects
    registered = get_registered_projects()
    print(f"Found {len(registered)} registered projects")

    # Build active projects list
    active_projects = []
    for chat_id, info in sorted(activity.items(), key=lambda x: x[1]["last_active"], reverse=True):
        if chat_id in registered:
            name = registered[chat_id]["name"]
            size = registered[chat_id]["size"]
            tier = registered[chat_id]["tier"]
        else:
            name = get_project_name(chat_id)
            if name == chat_id:
                # Use display name from session if no project.md
                name = info.get("display_name", chat_id)
            size = "0"
            tier = "-"

        # Check for actual project knowledge
        if os.path.exists(os.path.join(PROJECTS_DIR, chat_id)):
            size, tier = get_knowledge_size(chat_id)

        active_projects.append({
            "chat_id": chat_id,
            "name": name,
            "size": size,
            "tier": tier,
            "last_active": info["last_active"],
        })

    print(f"Active projects to sync: {len(active_projects)}")

    # Update SOUL.md
    if update_soul_md(active_projects):
        print("✓ SOUL.md updated with active projects")
    else:
        print("✗ Failed to update SOUL.md")

    # Also update PROJECTS.md
    # (the glossary builder handles this, but we sync registered status here)
    for chat_id in activity:
        project_dir = os.path.join(PROJECTS_DIR, chat_id)
        if not os.path.exists(project_dir):
            # Don't auto-create — just note it
            print(f"  ℹ {chat_id}: active but no project folder yet")


if __name__ == "__main__":
    main()
