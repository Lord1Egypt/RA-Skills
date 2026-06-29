#!/usr/bin/env python3
"""
Module 1: Logic & Syntax Check
- Python: ast.parse syntax check
- Bash: bash -n syntax check
- Internal reference path validation (files referenced in SKILL.md that don't exist)
- Internal import/require resolution
"""

import ast
import re
import subprocess
from pathlib import Path

from _common import is_bash_script
from i18n import t


def check_python_syntax(script_path: Path) -> list[dict]:
    issues = []
    try:
        source = script_path.read_text(encoding="utf-8")
        ast.parse(source, filename=str(script_path))
    except SyntaxError as e:
        issues.append({
            "file": str(script_path.name),
            "line": e.lineno,
            "message": t("logic.py_syntax", msg=e.msg),
            "severity": "ERROR",
        })
    except Exception as e:
        issues.append({
            "file": str(script_path.name),
            "line": None,
            "message": t("logic.py_unparseable", err=e),
            "severity": "WARN",
        })
    return issues


def check_bash_syntax(script_path: Path) -> list[dict]:
    issues = []
    try:
        result = subprocess.run(
            ["bash", "-n", str(script_path)],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as e:
        issues.append({
            "file": str(script_path.name),
            "line": None,
            "message": t("logic.bash_check_fail", err=e),
            "severity": "WARN",
        })
        return issues
    if result.returncode != 0:
        for line in result.stderr.strip().splitlines():
            issues.append({
                "file": str(script_path.name),
                "line": None,
                "message": t("logic.bash_syntax", line=line),
                "severity": "ERROR",
            })
    return issues


def check_internal_paths(skill_dir: Path) -> list[dict]:
    """Check that file paths referenced in SKILL.md actually exist."""
    issues = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return issues

    content = skill_md.read_text(encoding="utf-8")
    # Match markdown links like [text](path) and bare paths like scripts/foo.py
    link_pattern = re.compile(r'\[.*?\]\(([^)#]+)\)')
    code_ref_pattern = re.compile(r'`([^`]+\.(?:py|sh|md|json|yaml|yml))`')

    for pattern in [link_pattern, code_ref_pattern]:
        for match in pattern.finditer(content):
            ref = match.group(1).strip()
            # Skip URLs
            if ref.startswith(("http://", "https://", "mailto:")):
                continue
            # Skip placeholders / globs, not real file references:
            #   <name>.json, {skill}/x.md, *.py, output/{id}.html
            if any(c in ref for c in "<>{}*"):
                continue
            ref_path = skill_dir / ref
            if not ref_path.exists():
                issues.append({
                    "file": "SKILL.md",
                    "line": None,
                    "message": t("logic.missing_ref", ref=ref),
                    "severity": "WARN",
                })
    return issues


def check_internal_imports(skill_dir: Path) -> list[dict]:
    """Check that Python scripts importing local modules can find them."""
    issues = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return issues

    py_files = list(scripts_dir.glob("*.py"))
    local_modules = {f.stem for f in py_files}

    for py_file in py_files:
        try:
            source = py_file.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except Exception:
            continue

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.ImportFrom) and node.module:
                    module_name = node.module.split(".")[0]
                    # Only flag if it looks like a local relative import
                    if node.level > 0 and module_name and module_name not in local_modules:
                        issues.append({
                            "file": py_file.name,
                            "line": node.lineno,
                            "message": t("logic.import_not_found", module=module_name),
                            "severity": "WARN",
                        })
    return issues


def check_todo_leftovers(skill_dir: Path) -> list[dict]:
    """Flag TODO/FIXME/HACK/XXX leftovers in non-script files and SKILL.md.
    Skips scripts/ (checker code legitimately contains these as pattern strings)
    and references/ (docs may use them as examples).
    Only scans SKILL.md and assets/.
    """
    issues = []
    # Strict pattern: only in meaningful user-facing files
    patterns = re.compile(r'\b(TODO|FIXME|HACK|XXX)\b')
    # Only scan SKILL.md — skip scripts/ and references/ entirely
    scan_targets = [skill_dir / "SKILL.md"]
    # Also scan assets/ if present
    assets_dir = skill_dir / "assets"
    if assets_dir.exists():
        scan_targets.extend(f for f in assets_dir.rglob("*") if f.is_file())

    for f in scan_targets:
        if not f.exists() or not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
            for i, line in enumerate(text.splitlines(), 1):
                if patterns.search(line):
                    issues.append({
                        "file": str(f.relative_to(skill_dir)),
                        "line": i,
                        "message": t("logic.leftover_marker", line=line.strip()[:80]),
                        "severity": "WARN",
                    })
        except Exception:
            continue
    return issues


def run(skill_dir: Path) -> dict:
    issues = []
    scripts_dir = skill_dir / "scripts"

    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if not script.is_file():
                continue
            if script.suffix == ".py":
                issues.extend(check_python_syntax(script))
            elif is_bash_script(script):
                issues.extend(check_bash_syntax(script))

    issues.extend(check_internal_paths(skill_dir))
    issues.extend(check_internal_imports(skill_dir))
    issues.extend(check_todo_leftovers(skill_dir))

    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]

    return {
        "module": t("module.logic"),
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "issues": issues,
    }
