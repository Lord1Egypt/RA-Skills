#!/usr/bin/env python3
"""
Module 4: Data & Config Safety Check
Detects files/config/cache/logs being written INSIDE the skill directory.
After a skill update, the skill directory is overwritten — any data written there is lost.

Safe path: a persistent dir OUTSIDE the skill directory (see safe_data_dir_hint()).
"""

import ast
import re
from pathlib import Path

from _common import safe_data_dir_hint
from i18n import t


# Patterns that indicate a write to a path derived from __file__ or a relative path
# These are heuristic — we flag suspicious patterns for human review.

WRITE_CALL_NAMES = {
    "write_text", "write_bytes", "open", "json.dump",
    "yaml.dump", "toml.dump", "configparser.write",
}

CONFIG_KEYWORDS = re.compile(
    r'(config|conf|setting|cache|token|credential|secret|log|output)',
    re.IGNORECASE
)

SKILL_DIR_REF_PATTERNS = [
    # __file__ based paths
    re.compile(r'__file__'),
    # Path(__file__)
    re.compile(r'Path\s*\(\s*__file__'),
    # os.path.dirname(__file__)
    re.compile(r'os\.path\.(dirname|abspath)\s*\(\s*__file__'),
    # Relative paths that look like config storage
    re.compile(r'["\'](?:\./)?(?:config|cache|\.cache|logs?|data|credentials?|tokens?)[\\/]'),
]


def _extract_string_assignments(source: str) -> dict[str, str]:
    """Extract simple string variable assignments for path tracing."""
    result = {}
    try:
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if (len(node.targets) == 1
                        and isinstance(node.targets[0], ast.Name)
                        and isinstance(node.value, ast.Constant)
                        and isinstance(node.value.value, str)):
                    result[node.targets[0].id] = node.value.value
    except Exception:
        pass
    return result


def check_script_data_safety(script_path: Path) -> list[dict]:
    issues = []
    try:
        source = script_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    lines = source.splitlines()

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Skip comments
        if stripped.startswith("#"):
            continue

        # Check for __file__-based path constructions near write operations
        if "__file__" in line:
            # If this line or nearby lines also have write patterns
            context = "\n".join(lines[max(0, i-3):i+3])
            write_nearby = any(w in context for w in [
                "write_text", "write_bytes", "open(", ".dump(", "makedirs"
            ])
            if write_nearby and CONFIG_KEYWORDS.search(line):
                issues.append({
                    "file": script_path.name,
                    "line": i,
                    "message": t("data.file_write_in_dir", hint=safe_data_dir_hint()),
                    "severity": "WARN",
                })

        # Check for hardcoded relative paths that look like data storage
        for pat in SKILL_DIR_REF_PATTERNS[2:]:  # skip __file__ patterns, handled above
            if pat.search(line):
                if CONFIG_KEYWORDS.search(line):
                    issues.append({
                        "file": script_path.name,
                        "line": i,
                        "message": t("data.relative_write", snippet=stripped[:80]),
                        "severity": "WARN",
                    })
                    break

    return issues


def check_hardcoded_skill_subpaths(skill_dir: Path, script_path: Path) -> list[dict]:
    """Detect hardcoded absolute paths pointing into the skill directory."""
    issues = []
    skill_dir_str = str(skill_dir)
    try:
        source = script_path.read_text(encoding="utf-8")
    except Exception:
        return issues

    for i, line in enumerate(source.splitlines(), 1):
        if skill_dir_str in line and CONFIG_KEYWORDS.search(line):
            issues.append({
                "file": script_path.name,
                "line": i,
                "message": t("data.hardcoded_dir", snippet=line.strip()[:80]),
                "severity": "WARN",
            })
    return issues


def check_existing_data_in_skill_dir(skill_dir: Path) -> list[dict]:
    """Flag config/cache/log files already sitting inside the skill directory."""
    issues = []
    DATA_PATTERNS = re.compile(
        r'\.(json|yaml|yml|cfg|ini|log|db|sqlite|token)$',
        re.IGNORECASE
    )
    KNOWN_OK = {"SKILL.md", "package.json", "requirements.txt"}
    # Subdirs that legitimately hold docs/assets (no runtime data expected).
    # NOTE: scripts/ is intentionally NOT skipped — data files commonly get
    # misplaced under scripts/ (e.g. scripts/cache.json), which is exactly the
    # class of bug this module exists to catch.
    SAFE_DIRS = {"references", "assets"}
    # Code/declaration files that legitimately live under scripts/ etc.
    CODE_SUFFIXES = {".py", ".sh", ".js", ".ts", ".mjs", ".cjs", ".md", ".txt"}

    for f in skill_dir.rglob("*"):
        if f.is_dir():
            continue
        rel = f.relative_to(skill_dir)
        # Skip files inside docs/asset subdirectories
        if rel.parts[0] in SAFE_DIRS:
            continue
        # Skip Python bytecode cache
        if "__pycache__" in rel.parts:
            continue
        # Skip code/declaration files (they are not runtime data)
        if f.suffix.lower() in CODE_SUFFIXES:
            continue
        if f.name in KNOWN_OK:
            continue
        if f.name.startswith("."):
            # Hidden files like .setup-done are common sidecar state
            if DATA_PATTERNS.search(f.name) and CONFIG_KEYWORDS.search(f.name):
                issues.append({
                    "file": str(rel),
                    "line": None,
                    "message": t("data.datafile_in_dir", rel=rel),
                    "severity": "WARN",
                })
            continue
        if DATA_PATTERNS.search(f.name) and CONFIG_KEYWORDS.search(f.name):
            issues.append({
                "file": str(rel),
                "line": None,
                "message": t("data.datafile_in_dir", rel=rel),
                "severity": "WARN",
            })

    return issues


def run(skill_dir: Path) -> dict:
    issues = []
    scripts_dir = skill_dir / "scripts"

    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if not script.is_file() or script.suffix not in {".py", ".sh", ""}:
                continue
            issues.extend(check_script_data_safety(script))
            issues.extend(check_hardcoded_skill_subpaths(skill_dir, script))

    issues.extend(check_existing_data_in_skill_dir(skill_dir))

    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]

    return {
        "module": t("module.data"),
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "issues": issues,
        "tip": t("data.hint", hint=safe_data_dir_hint()),
    }
