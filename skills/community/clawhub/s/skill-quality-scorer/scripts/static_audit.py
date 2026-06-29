#!/usr/bin/env python3
"""
Static audit for Agent Skill packages (SKILL.md directories).
Deterministic checks — outputs JSON to stdout. Rubric v2 (T-R-F-S-I-E).

Usage:
  python static_audit.py <skill-directory>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

VERSION = "2.0.0"

EXTRANEOUS_FILES = {
    "CHANGELOG.md",
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
}

CRITICAL_PATTERNS = [
    (r"curl\s+[^\n|]+\|\s*(ba)?sh", "T1", "curl pipe to shell"),
    (r"wget\s+[^\n]+\|\s*(ba)?sh", "T1", "wget pipe to shell"),
    (r"eval\s*\(\s*base64", "T3", "base64 eval execution"),
    (r"exec\s*\(\s*base64", "T3", "base64 exec"),
]

HIGH_PATTERNS = [
    (r"\bsudo\s+", "T4", "sudo usage"),
    (r"(?<![\w/])\.env\b", "T2", "env file reference"),
    (r"api[_-]?key\s*=", "T2", "hardcoded api key pattern"),
]

HUMAN_DOC_PATTERNS = [
    (r"版本记录|Version History|CHANGELOG", "I1", "human version log in skill body"),
    (r"##\s*背景|基于.*经验总结|本技能基于", "I1", "background narrative"),
    (r"保持专业.*语气|建设性语气", "I1", "vague human tone guidance"),
]

MARKDOWN_LINK = re.compile(r"\]\(([^)]+)\)")
MARKDOWN_BACKTICK_PATH = re.compile(r"`((?:scripts|references|assets)/[^`]+)`")
USE_WHEN = re.compile(
    r"use when|当用户|触发|asks to|says|用于.*场景|当.*需要|when evaluating|when the user",
    re.I,
)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def extract_description(raw_yaml: str) -> str:
    """Parse description including multiline >- / | blocks."""
    lines = raw_yaml.splitlines()
    desc_lines: list[str] = []
    in_desc = False
    for i, line in enumerate(lines):
        if re.match(r"^description:\s*", line):
            rest = line.split(":", 1)[1].strip()
            if rest in (">-", ">", "|", "|-", "|"):
                in_desc = True
                continue
            if rest:
                return rest.strip('"').strip("'")
            in_desc = True
            continue
        if in_desc:
            if line and not line[0].isspace() and re.match(r"^[a-zA-Z_][\w-]*:", line):
                break
            if line.strip():
                desc_lines.append(line.strip())
    return " ".join(desc_lines)


def parse_frontmatter(content: str) -> tuple[dict[str, str], str, bool]:
    if not content.startswith("---"):
        return {}, content, False
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content, False
    raw = parts[1]
    body = parts[2]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" in line and not line[0].isspace():
            k, _, v = line.partition(":")
            if k.strip() != "description":
                meta[k.strip()] = v.strip().strip('"').strip("'")
    desc = extract_description(raw)
    if desc:
        meta["description"] = desc
    return meta, body, True


def collect_linked_paths(body: str) -> list[str]:
    paths: set[str] = set()
    for m in MARKDOWN_LINK.finditer(body):
        p = m.group(1).strip()
        if p.startswith("http") or p.startswith("#"):
            continue
        paths.add(p.split("#")[0])
    for m in MARKDOWN_BACKTICK_PATH.finditer(body):
        paths.add(m.group(1))
    return sorted(paths)


def count_code_blocks(body: str) -> tuple[int, int]:
    """Return (opening_fences, opening_fences_with_lang). Closing ``` lines are ignored."""
    total = 0
    with_lang = 0
    in_block = False
    for line in body.splitlines():
        if not line.startswith("```"):
            continue
        rest = line[3:].strip()
        if in_block:
            in_block = False
            continue
        total += 1
        in_block = True
        if rest:
            with_lang += 1
    return total, with_lang


def scan_patterns(text: str, patterns: list[tuple[str, str, str]], severity: str) -> list[dict]:
    out = []
    for pat, item, desc in patterns:
        if re.search(pat, text, re.IGNORECASE | re.MULTILINE):
            out.append({"item": item, "pattern": desc, "severity": severity})
    return out


EXECUTABLE_SUFFIXES = {".py", ".sh", ".js", ".ts", ".bash"}
# Pattern literals in the auditor itself must not self-trigger.
SECURITY_SCAN_SKIP_SCRIPT_NAMES = {"static_audit.py"}


def collect_security_scan_text(skill_dir: Path, skill_md_content: str) -> str:
    """Scan SKILL.md + executable scripts/assets only; skip references/examples rubric text."""
    parts = [skill_md_content]
    for subdir in ("scripts", "assets"):
        base = skill_dir / subdir
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in EXECUTABLE_SUFFIXES:
                continue
            if subdir == "scripts" and path.name in SECURITY_SCAN_SKIP_SCRIPT_NAMES:
                continue
            parts.append(read_text(path))
    return "\n".join(parts)


def audit_skill(skill_dir: Path) -> dict:
    skill_dir = skill_dir.resolve()
    skill_md = skill_dir / "SKILL.md"

    result: dict = {
        "version": VERSION,
        "rubric_version": "2.0.0",
        "skill_dir": str(skill_dir),
        "skill_name_folder": skill_dir.name,
        "ok": False,
        "flags": [],
        "auto_scores": {},
        "metrics": {},
        "missing_paths": [],
        "extraneous_files": [],
    }

    if not skill_md.is_file():
        result["error"] = "SKILL.md not found"
        return result

    content = read_text(skill_md)
    meta, body, yaml_ok = parse_frontmatter(content)
    body_lines = body.count("\n") + (1 if body.strip() else 0)
    desc = meta.get("description", "")
    name = meta.get("name", skill_dir.name)

    fences, fences_lang = count_code_blocks(body)

    result["metrics"] = {
        "body_lines": body_lines,
        "yaml_valid": yaml_ok,
        "has_name": bool(meta.get("name")),
        "has_description": bool(desc),
        "description_len": len(desc),
        "description_word_approx": len(desc.split()),
        "has_use_when": bool(USE_WHEN.search(desc)),
        "name_matches_folder": name == skill_dir.name,
        "code_blocks": fences,
        "code_blocks_with_lang": fences_lang,
    }

    for f in skill_dir.iterdir():
        if f.is_file() and f.name in EXTRANEOUS_FILES:
            result["extraneous_files"].append(f.name)

    linked = collect_linked_paths(body)
    missing = []
    for rel in linked:
        target = (skill_dir / rel).resolve()
        try:
            target.relative_to(skill_dir.resolve())
        except ValueError:
            continue
        if not target.exists():
            missing.append(rel)
    result["missing_paths"] = missing

    security_text = collect_security_scan_text(skill_dir, content)

    result["flags"].extend(scan_patterns(security_text, CRITICAL_PATTERNS, "critical"))
    for f in scan_patterns(security_text, HIGH_PATTERNS, "high"):
        if not any(x["pattern"] == f["pattern"] for x in result["flags"]):
            result["flags"].append(f)
    for f in scan_patterns(body, HUMAN_DOC_PATTERNS, "info"):
        result["flags"].append(f)

    has_scripts = (skill_dir / "scripts").is_dir() and any((skill_dir / "scripts").iterdir())
    refs_dir = skill_dir / "references"
    has_refs = refs_dir.is_dir() and any(refs_dir.glob("*"))
    assets_dir = skill_dir / "assets"
    has_assets = assets_dir.is_dir() and any(assets_dir.iterdir()) if assets_dir.is_dir() else False
    refs_linked = any("references/" in p for p in linked)

    auto: dict[str, int] = {}

    # R
    auto["R1"] = 2 if yaml_ok and meta.get("name") and desc else (1 if yaml_ok else 0)
    auto["R2"] = 2 if not missing else (1 if len(missing) <= 1 else 0)

    # F
    auto["F1"] = 2 if result["metrics"]["has_use_when"] else 0
    auto["F4"] = 2 if name == skill_dir.name and re.match(r"^[a-z0-9-]+$", name) else 0
    auto["F5"] = 2 if len(desc) <= 500 else (1 if len(desc) <= 800 else 0)

    # S
    auto["S1"] = 2 if body_lines <= 500 else (1 if body_lines <= 800 else 0)
    auto["S2"] = 2 if (not has_refs or refs_linked) else 1
    auto["S4"] = 2 if not result["extraneous_files"] else (1 if len(result["extraneous_files"]) == 1 else 0)
    auto["S5"] = 2 if len(desc) <= 500 else (1 if len(desc) <= 800 else 0)

    # I
    human_flags = [f for f in result["flags"] if f.get("item") == "I1"]
    auto["I1"] = 0 if human_flags else 2
    auto["I3"] = (
        2 if fences >= 2 and fences_lang == fences and fences > 0
        else (1 if fences >= 1 else 0)
    )

    # T
    if any(f["severity"] == "critical" for f in result["flags"]):
        auto["T1"] = 0
        auto["T3"] = 0
    else:
        auto["T1"] = 2 if not any(f["item"] == "T1" for f in result["flags"]) else 1

    result["auto_scores"] = auto
    result["metrics"]["has_scripts_dir"] = has_scripts
    result["metrics"]["has_references_dir"] = has_refs
    result["metrics"]["has_assets_dir"] = has_assets
    result["ok"] = True
    return result


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"error": "usage: static_audit.py <skill-directory>"}), file=sys.stderr)
        return 2

    result = audit_skill(Path(sys.argv[1]))
    if result.get("error") == "SKILL.md not found":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
