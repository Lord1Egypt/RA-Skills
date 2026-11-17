#!/usr/bin/env python3
"""Export a validated MentorForge mentor skill package without installing it."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def copy_package(src: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def read_skill_name(skill_dir: Path) -> str:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"').strip("'")
    return skill_dir.name


def export_codex(skill_dir: Path, output_root: Path) -> None:
    copy_package(skill_dir, output_root / "codex" / skill_dir.name)


def export_claude(skill_dir: Path, output_root: Path) -> None:
    dest = output_root / "claude" / skill_dir.name
    copy_package(skill_dir, dest)
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    claude_md = [
        f"# {skill_dir.name}",
        "",
        "Use this MentorForge-generated mentor skill as local project instructions.",
        "This export is not installed automatically.",
        "",
        "## Skill Instructions",
        "",
        skill_text,
    ]
    (dest / "CLAUDE.md").write_text("\n".join(claude_md), encoding="utf-8")


def export_clawhub(skill_dir: Path, output_root: Path) -> None:
    dest = output_root / "clawhub" / skill_dir.name
    copy_package(skill_dir, dest)
    skill_name = read_skill_name(skill_dir)
    manifest = {
        "name": skill_name,
        "source": "MentorForge",
        "entrypoint": "SKILL.md",
        "description": "Evidence-grounded research mentor skill package.",
        "installed": False,
    }
    (dest / "clawhub-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def export_plain_prompt(skill_dir: Path, output_root: Path) -> None:
    dest = output_root / "plain-prompt" / skill_dir.name
    dest.mkdir(parents=True, exist_ok=True)
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    refs = sorted((skill_dir / "references").glob("*.md")) if (skill_dir / "references").exists() else []
    lines = [
        f"# Plain Prompt Export: {skill_dir.name}",
        "",
        "Paste the following instructions into an agent that does not support SKILL.md packages.",
        "This export is not installed automatically.",
        "",
        "## Runtime Instructions",
        "",
        skill_text,
        "",
        "## Evidence References",
        "",
    ]
    for ref in refs:
        lines.append(f"- {ref.name}")
    (dest / "prompt.md").write_text("\n".join(lines), encoding="utf-8")
    if refs:
        ref_dest = dest / "references"
        ref_dest.mkdir(exist_ok=True)
        for ref in refs:
            shutil.copy2(ref, ref_dest / ref.name)


EXPORTERS = {
    "codex": export_codex,
    "claude": export_claude,
    "clawhub": export_clawhub,
    "plain-prompt": export_plain_prompt,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a MentorForge skill package without installing it.")
    parser.add_argument("--skill-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument(
        "--formats",
        default="codex,claude,clawhub,plain-prompt",
        help="Comma-separated formats: codex,claude,clawhub,plain-prompt",
    )
    args = parser.parse_args()

    skill_dir = args.skill_dir
    if not (skill_dir / "SKILL.md").exists():
        raise SystemExit(f"SKILL.md not found in {skill_dir}")

    formats = [item.strip() for item in args.formats.split(",") if item.strip()]
    for fmt in formats:
        exporter = EXPORTERS.get(fmt)
        if exporter is None:
            raise SystemExit(f"Unknown export format: {fmt}")
        exporter(skill_dir, args.output_dir)
        print(f"Exported {fmt} to {args.output_dir / fmt}")
    print("No runtime installation was performed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
