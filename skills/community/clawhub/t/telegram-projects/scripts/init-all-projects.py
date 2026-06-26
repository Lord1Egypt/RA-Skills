#!/usr/bin/env python3
"""
init-all-projects.py — Create project folders for all active Telegram groups.
"""

import os
import json
import time
from pathlib import Path
from datetime import datetime

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
PROJECTS_DIR = os.path.join(WORKSPACE, "projects")
SESSIONS_JSON = os.path.expanduser("~/.openclaw/agents/main/sessions/sessions.json")
ACTIVE_WINDOW_DAYS = 28


def main():
    with open(SESSIONS_JSON) as f:
        data = json.load(f)

    cutoff_ms = (time.time() - (ACTIVE_WINDOW_DAYS * 86400)) * 1000
    created = 0

    for key, info in sorted(data.items(), key=lambda x: x[1].get("updatedAt", 0), reverse=True):
        if ":telegram:group:" not in key:
            continue

        parts = key.split(":")
        if "topic" in parts:
            continue

        try:
            group_idx = parts.index("group")
            chat_id = parts[group_idx + 1]
        except (ValueError, IndexError):
            continue

        updated_at = info.get("updatedAt", 0)
        if updated_at < cutoff_ms:
            continue

        display_name = info.get("displayName", chat_id)
        clean_name = display_name.replace("telegram:g-", "").replace("telegram:", "")

        project_dir = os.path.join(PROJECTS_DIR, chat_id)
        os.makedirs(project_dir, exist_ok=True)

        # Create project.md if not exists
        project_md = os.path.join(project_dir, "project.md")
        if not os.path.exists(project_md):
            last_active = datetime.fromtimestamp(updated_at / 1000).strftime("%Y-%m-%d")
            Path(project_md).write_text(
                f"# {clean_name}\n\n"
                f"- **Chat ID:** {chat_id}\n"
                f"- **Created:** {datetime.now().strftime('%Y-%m-%d')}\n"
                f"- **Last Active:** {last_active}\n"
                f"- **Description:** _(add a description for this project)_\n",
                encoding="utf-8"
            )

        # Create knowledge.md if not exists
        knowledge_md = os.path.join(project_dir, "knowledge.md")
        if not os.path.exists(knowledge_md):
            Path(knowledge_md).write_text(
                f"# Project Knowledge: {clean_name}\n\n"
                f"_No knowledge entries yet. Add with: \"permanentes Knowledge: ...\" or `/knowledge add`_\n",
                encoding="utf-8"
            )

        # Create glossary.md if not exists
        glossary_md = os.path.join(project_dir, "glossary.md")
        if not os.path.exists(glossary_md):
            Path(glossary_md).write_text(
                "# Project Glossary\n\n_No knowledge entries yet._\n",
                encoding="utf-8"
            )

        created += 1
        print(f"  ✓ {chat_id} ({clean_name})")

    print(f"\nDone. {created} projects initialized.")


if __name__ == "__main__":
    main()
