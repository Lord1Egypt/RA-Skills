#!/usr/bin/env python3
"""Validate the relationship-science-coach Agent Skill package.

Checks are intentionally dependency-free so the validator can run in restricted
agent environments.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Optional

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESERVED_NAME_PREFIXES = ("claude", "anthropic")


def parse_frontmatter(skill_md: Path) -> tuple[dict[str, Any], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError as exc:
        return {}, [f"Could not read SKILL.md: {exc}"], []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter delimiter '---'."], []
    end = text.find("\n---", 4)
    if end == -1:
        return {}, ["SKILL.md frontmatter is missing closing '---' delimiter."], []
    fm_text = text[4:end].strip("\n")
    if "<" in fm_text or ">" in fm_text:
        errors.append("Frontmatter must not contain XML angle brackets '<' or '>'.")
    data: dict[str, Any] = {}
    current_map: str | None = None
    for lineno, raw in enumerate(fm_text.splitlines(), start=2):
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("  ") and current_map:
            if ":" not in line:
                errors.append(f"Invalid nested frontmatter line {lineno}: {line!r}")
                continue
            key, value = line.strip().split(":", 1)
            if not isinstance(data.get(current_map), dict):
                data[current_map] = {}
            data[current_map][key.strip()] = strip_yaml_scalar(value.strip())
            continue
        current_map = None
        if ":" not in line:
            errors.append(f"Invalid frontmatter line {lineno}: {line!r}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            errors.append(f"Empty frontmatter key on line {lineno}.")
            continue
        if value == "":
            data[key] = {}
            current_map = key
        else:
            data[key] = strip_yaml_scalar(value)
    return data, errors, warnings


def strip_yaml_scalar(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def validate_frontmatter(root: Path, errors: list[str], warnings: list[str]) -> dict[str, Any]:
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing required SKILL.md.")
        return {}
    fm, fm_errors, fm_warnings = parse_frontmatter(skill_md)
    errors.extend(fm_errors)
    warnings.extend(fm_warnings)

    name = str(fm.get("name", ""))
    desc = str(fm.get("description", ""))
    if not name:
        errors.append("Frontmatter is missing required 'name'.")
    elif not NAME_RE.fullmatch(name):
        errors.append("Skill name must use lowercase kebab-case letters/numbers and single hyphens only.")
    elif len(name) > 64:
        errors.append("Skill name exceeds 64 characters.")
    elif name.startswith(RESERVED_NAME_PREFIXES):
        warnings.append("Skill name appears to use a reserved product/company prefix.")
    if name and root.name != name:
        errors.append(f"Skill directory name {root.name!r} must match frontmatter name {name!r}.")

    if not desc:
        errors.append("Frontmatter is missing required 'description'.")
    elif len(desc) > 1024:
        errors.append(f"Description exceeds 1024 characters ({len(desc)}).")
    elif len(desc) < 80:
        warnings.append("Description is short; consider adding trigger conditions and near-miss boundaries.")
    if "Use this skill" not in desc and "Use when" not in desc:
        warnings.append("Description may not be imperative enough for reliable triggering.")

    compatibility = fm.get("compatibility")
    if compatibility and len(str(compatibility)) > 500:
        errors.append("compatibility field exceeds 500 characters.")
    return fm


def validate_structure(root: Path, errors: list[str], warnings: list[str]) -> dict[str, int]:
    counts = {"references": 0, "scripts": 0, "assets": 0, "eval_files": 0}
    if (root / "README.md").exists():
        warnings.append("README.md is present inside the skill folder; Agent Skills guidance recommends putting docs in SKILL.md or references/.")
    for directory in ["references", "scripts", "assets", "evals"]:
        path = root / directory
        if path.exists() and not path.is_dir():
            errors.append(f"{directory}/ exists but is not a directory.")
    for path in (root / "references").glob("*.md") if (root / "references").exists() else []:
        counts["references"] += 1
        if path.stat().st_size > 80_000:
            warnings.append(f"Large reference file {path.relative_to(root)} may hurt progressive disclosure.")
    for path in (root / "scripts").glob("*.py") if (root / "scripts").exists() else []:
        counts["scripts"] += 1
    for path in (root / "assets").iterdir() if (root / "assets").exists() else []:
        if path.is_file():
            counts["assets"] += 1
    for path in (root / "evals").glob("*.json") if (root / "evals").exists() else []:
        counts["eval_files"] += 1
    return counts


def validate_json_files(root: Path, errors: list[str], warnings: list[str]) -> None:
    for subdir in ["assets", "evals"]:
        path = root / subdir
        if not path.exists():
            continue
        for json_file in path.glob("*.json"):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"Invalid JSON in {json_file.relative_to(root)}: {exc}")
                continue
            if json_file.name == "evals.json":
                if not isinstance(data, dict) or "evals" not in data or not isinstance(data["evals"], list):
                    errors.append("evals/evals.json must be an object with an 'evals' list.")
                else:
                    for i, case in enumerate(data["evals"], start=1):
                        if not isinstance(case, dict):
                            errors.append(f"evals/evals.json case {i} is not an object.")
                            continue
                        for field in ["id", "prompt", "expected_output"]:
                            if field not in case:
                                errors.append(f"evals/evals.json case {i} missing {field!r}.")
                        if "assertions" in case and not isinstance(case["assertions"], list):
                            errors.append(f"evals/evals.json case {i} assertions must be a list.")
            if json_file.name.endswith("queries.json"):
                if not isinstance(data, list):
                    errors.append(f"{json_file.relative_to(root)} must be a list of trigger query objects.")
                else:
                    for i, q in enumerate(data, start=1):
                        if not isinstance(q, dict) or "query" not in q or "should_trigger" not in q:
                            errors.append(f"{json_file.relative_to(root)} item {i} must include query and should_trigger.")


def validate_scripts(root: Path, errors: list[str], warnings: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    scripts_dir = root / "scripts"
    if not scripts_dir.exists():
        return results
    for script in sorted(scripts_dir.glob("*.py")):
        try:
            proc = subprocess.run(
                [sys.executable, str(script), "--help"],
                cwd=str(root),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
        except subprocess.TimeoutExpired:
            errors.append(f"{script.relative_to(root)} --help timed out.")
            results.append({"script": str(script.relative_to(root)), "help_ok": False, "reason": "timeout"})
            continue
        ok = proc.returncode == 0 and "usage" in proc.stdout.lower()
        if not ok:
            errors.append(f"{script.relative_to(root)} --help failed or did not print usage.")
        results.append({
            "script": str(script.relative_to(root)),
            "help_ok": ok,
            "returncode": proc.returncode,
            "stdout_chars": len(proc.stdout),
            "stderr_chars": len(proc.stderr),
        })
    return results


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate the structure and metadata of an Agent Skill package.",
        epilog="Example: python3 scripts/validate_skill.py . --check-scripts --pretty",
    )
    parser.add_argument("path", nargs="?", default=".", help="Skill root path. Default: current directory.")
    parser.add_argument("--check-scripts", action="store_true", help="Run each bundled Python script with --help.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not root.exists() or not root.is_dir():
        errors.append(f"Path is not a directory: {root}")
        result = {"valid": False, "errors": errors, "warnings": warnings}
        print(json.dumps(result, indent=2 if args.pretty else None))
        return 1

    frontmatter = validate_frontmatter(root, errors, warnings)
    counts = validate_structure(root, errors, warnings)
    validate_json_files(root, errors, warnings)
    script_results = validate_scripts(root, errors, warnings) if args.check_scripts else []

    result = {
        "valid": not errors,
        "skill_root": str(root),
        "frontmatter": frontmatter,
        "counts": counts,
        "script_help": script_results,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
