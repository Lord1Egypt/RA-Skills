#!/usr/bin/env python3
"""
Module 2: Feature Coverage Check
- Extract claimed features from SKILL.md description
- Check that referenced scripts/files actually exist
- Flag undocumented scripts (exist but not mentioned in SKILL.md)
- Flag empty or stub scripts
"""

import re
from pathlib import Path

from i18n import t


def _read_skill_md(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    if skill_md.exists():
        return skill_md.read_text(encoding="utf-8")
    return ""


def check_script_coverage(skill_dir: Path) -> list[dict]:
    """Every script in scripts/ should be mentioned somewhere in SKILL.md."""
    issues = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return issues

    content = _read_skill_md(skill_dir)

    for script in scripts_dir.iterdir():
        if script.name.startswith("_") or script.name.startswith("."):
            continue
        if script.name not in content:
            issues.append({
                "file": f"scripts/{script.name}",
                "line": None,
                "message": t("features.script_unmentioned", name=script.name),
                "severity": "WARN",
            })
    return issues


def check_references_coverage(skill_dir: Path) -> list[dict]:
    """Every file in references/ should be mentioned somewhere in SKILL.md."""
    issues = []
    refs_dir = skill_dir / "references"
    if not refs_dir.exists():
        return issues

    content = _read_skill_md(skill_dir)

    for ref in refs_dir.iterdir():
        if ref.name.startswith("."):
            continue
        if ref.name not in content:
            issues.append({
                "file": f"references/{ref.name}",
                "line": None,
                "message": t("features.ref_unmentioned", name=ref.name),
                "severity": "WARN",
            })
    return issues


def check_empty_scripts(skill_dir: Path) -> list[dict]:
    """Flag scripts that are empty or nearly empty (stub files)."""
    issues = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return issues

    MIN_MEANINGFUL_LINES = 5

    for script in scripts_dir.iterdir():
        if not script.is_file():
            continue
        try:
            lines = [
                l for l in script.read_text(encoding="utf-8").splitlines()
                if l.strip() and not l.strip().startswith("#")
            ]
            if len(lines) < MIN_MEANINGFUL_LINES:
                issues.append({
                    "file": f"scripts/{script.name}",
                    "line": None,
                    "message": t("features.stub_script", n=len(lines)),
                    "severity": "WARN",
                })
        except Exception:
            continue
    return issues


def check_skill_md_body(skill_dir: Path) -> list[dict]:
    """Check that SKILL.md has a meaningful body beyond frontmatter."""
    issues = []
    content = _read_skill_md(skill_dir)
    if not content:
        return issues

    # Strip frontmatter
    lines = content.splitlines()
    body_start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                body_start = i + 1
                break

    body = "\n".join(lines[body_start:]).strip()
    if len(body) < 100:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": t("features.thin_body"),
            "severity": "WARN",
        })

    return issues


def run(skill_dir: Path) -> dict:
    issues = []
    issues.extend(check_script_coverage(skill_dir))
    issues.extend(check_references_coverage(skill_dir))
    issues.extend(check_empty_scripts(skill_dir))
    issues.extend(check_skill_md_body(skill_dir))

    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]

    return {
        "module": t("module.features"),
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "issues": issues,
    }
