#!/usr/bin/env python3
"""
Skill File Writer

Writes generated work.md, persona.md to the correct directory structure,
and generates meta.json and the full SKILL.md.

Usage:
    python3 skill_writer.py --action create --slug alex-chen --meta meta.json \
        --work work_content.md --persona persona_content.md \
        --base-dir ./teammates

    python3 skill_writer.py --action update --slug alex-chen \
        --work-patch work_patch.md --persona-patch persona_patch.md \
        --base-dir ./teammates

    python3 skill_writer.py --action list --base-dir ./teammates
"""

from __future__ import annotations

import json
import shutil
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


SKILL_MD_TEMPLATE = """\
---
name: teammate-{slug}
description: "{name} — {identity}. Invoke to get responses in their voice and style."
user-invocable: true
---

# {name}

{identity}

---

## PART A: Work Capabilities

{work_content}

---

## PART B: Persona

{persona_content}

---

## Execution Rules

1. PART B decides first: what attitude to take on this task?
2. PART A executes: use your technical skills to complete the task
3. Always maintain PART B's communication style in output — **never break character into generic AI**
4. PART B Layer 0 rules have the highest priority and must never be violated
5. When the Correction Log has entries, those override earlier layer rules
6. If asked about something outside your knowledge scope, say so the way this person would — don't fabricate expertise they don't have
7. Keep responses at a realistic length for this person's style (a terse person writes 2 sentences, not 5 paragraphs)
"""


def build_identity(meta: dict) -> str:
    """Build a one-line identity string from meta profile."""
    profile = meta.get("profile", {})
    parts = []
    if profile.get("company"):
        parts.append(profile["company"])
    if profile.get("level"):
        parts.append(profile["level"])
    if profile.get("role"):
        parts.append(profile["role"])
    if profile.get("team"):
        parts.append(f"({profile['team']})")
    return " ".join(parts) if parts else "Engineer"


def create_skill(slug: str, meta_path: str, work_path: str, persona_path: str, base_dir: str):
    """Create a new teammate skill from generated content files."""
    base = Path(base_dir)
    skill_dir = base / slug

    # Create directory structure
    (skill_dir / "versions").mkdir(parents=True, exist_ok=True)
    (skill_dir / "knowledge" / "docs").mkdir(parents=True, exist_ok=True)
    (skill_dir / "knowledge" / "messages").mkdir(parents=True, exist_ok=True)
    (skill_dir / "knowledge" / "emails").mkdir(parents=True, exist_ok=True)

    # Read inputs
    meta = json.loads(Path(meta_path).read_text(encoding="utf-8"))
    work_content = Path(work_path).read_text(encoding="utf-8")
    persona_content = Path(persona_path).read_text(encoding="utf-8")

    # Write work.md
    (skill_dir / "work.md").write_text(work_content, encoding="utf-8")

    # Write persona.md
    (skill_dir / "persona.md").write_text(persona_content, encoding="utf-8")

    # Write meta.json
    (skill_dir / "meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Generate and write SKILL.md
    identity = build_identity(meta)
    skill_md = SKILL_MD_TEMPLATE.format(
        slug=slug,
        name=meta["name"],
        identity=identity,
        work_content=work_content,
        persona_content=persona_content,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    print(f"✅ Teammate Skill created at {skill_dir}/")
    print(f"   Commands: /{slug} | /{slug}-work | /{slug}-persona")


def update_skill(slug: str, base_dir: str, work_patch: Optional[str] = None, persona_patch: Optional[str] = None):
    """Update an existing teammate skill with patches."""
    base = Path(base_dir)
    skill_dir = base / slug

    if not skill_dir.exists():
        print(f"❌ Teammate '{slug}' not found at {skill_dir}")
        sys.exit(1)

    # Read existing meta
    meta_path = skill_dir / "meta.json"
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    # Update version
    current_version = meta.get("version", "v1")
    version_num = int(current_version.lstrip("v")) + 1
    meta["version"] = f"v{version_num}"
    meta["updated_at"] = datetime.now(timezone.utc).isoformat()

    # Track what changed
    changes = []

    # Read current content
    work_content = (skill_dir / "work.md").read_text(encoding="utf-8")
    persona_content = (skill_dir / "persona.md").read_text(encoding="utf-8")

    # Apply patches (append to appropriate sections, not just end-of-file)
    if work_patch:
        patch_text = Path(work_patch).read_text(encoding="utf-8")
        # Find the best insertion point: before Correction Log if it exists
        if "## Correction Log" in work_content:
            work_content = work_content.replace(
                "## Correction Log",
                f"{patch_text}\n\n## Correction Log"
            )
        else:
            work_content += f"\n\n{patch_text}"
        (skill_dir / "work.md").write_text(work_content, encoding="utf-8")
        changes.append("work.md")

    if persona_patch:
        patch_text = Path(persona_patch).read_text(encoding="utf-8")
        if "## Correction Log" in persona_content:
            persona_content = persona_content.replace(
                "## Correction Log",
                f"{patch_text}\n\n## Correction Log"
            )
        else:
            persona_content += f"\n\n{patch_text}"
        (skill_dir / "persona.md").write_text(persona_content, encoding="utf-8")
        changes.append("persona.md")

    # Update meta
    if "update_history" not in meta:
        meta["update_history"] = []
    meta["update_history"].append({
        "version": meta["version"],
        "updated_at": meta["updated_at"],
        "files_changed": changes,
    })
    # Keep only last 20 update records
    meta["update_history"] = meta["update_history"][-20:]
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    # Regenerate SKILL.md
    identity = build_identity(meta)
    skill_md = SKILL_MD_TEMPLATE.format(
        slug=slug,
        name=meta["name"],
        identity=identity,
        work_content=work_content,
        persona_content=persona_content,
    )
    (skill_dir / "SKILL.md").write_text(skill_md, encoding="utf-8")

    print(f"✅ Teammate '{slug}' updated to {meta['version']} ({', '.join(changes)})")


def list_skills(base_dir: str):
    """List all teammate skills."""
    base = Path(base_dir)
    if not base.exists():
        print("No teammates found.")
        return

    teammates = []
    for d in sorted(base.iterdir()):
        if not d.is_dir():
            continue
        meta_path = d / "meta.json"
        if not meta_path.exists():
            continue
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        identity = build_identity(meta)
        teammates.append({
            "slug": meta.get("slug", d.name),
            "name": meta.get("name", d.name),
            "identity": identity,
            "version": meta.get("version", "v1"),
            "updated_at": meta.get("updated_at", "unknown"),
        })

    if not teammates:
        print("No teammates found.")
        return

    print(f"Found {len(teammates)} teammate(s):\n")
    for t in teammates:
        print(f"  /{t['slug']}  —  {t['name']}, {t['identity']}  [{t['version']}]  (updated: {t['updated_at'][:10]})")


def main():
    parser = argparse.ArgumentParser(description="Teammate Skill file writer")
    parser.add_argument("--action", required=True, choices=["create", "update", "list"])
    parser.add_argument("--slug", help="Teammate slug")
    parser.add_argument("--meta", help="Path to meta.json")
    parser.add_argument("--work", help="Path to work.md content")
    parser.add_argument("--persona", help="Path to persona.md content")
    parser.add_argument("--work-patch", help="Path to work patch file")
    parser.add_argument("--persona-patch", help="Path to persona patch file")
    parser.add_argument("--base-dir", default="./teammates", help="Base directory for teammate skills")

    args = parser.parse_args()

    if args.action == "create":
        if not all([args.slug, args.meta, args.work, args.persona]):
            parser.error("create requires --slug, --meta, --work, --persona")
        create_skill(args.slug, args.meta, args.work, args.persona, args.base_dir)
    elif args.action == "update":
        if not args.slug:
            parser.error("update requires --slug")
        update_skill(args.slug, args.base_dir, args.work_patch, args.persona_patch)
    elif args.action == "list":
        list_skills(args.base_dir)


if __name__ == "__main__":
    main()
