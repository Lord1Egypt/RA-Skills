#!/usr/bin/env python3
"""Audit an agent skill folder before marketplace publication."""

from __future__ import annotations

import argparse
import json
import py_compile
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


BLOCKER = "blocker"
WARN = "warn"
INFO = "info"


@dataclass
class Finding:
    severity: str
    rule: str
    path: str
    message: str
    line: int | None = None


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def iter_files(root: Path) -> Iterable[Path]:
    skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "dist", "build"}
    for path in root.rglob("*"):
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.is_file():
            yield path


def add(findings: list[Finding], severity: str, rule: str, path: Path, message: str, line: int | None = None) -> None:
    findings.append(Finding(severity, rule, str(path), message, line))


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    if not text.startswith("---\n"):
        return {}, "missing YAML frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return {}, "unterminated YAML frontmatter"
    data: dict[str, str] = {}
    for raw in text[4:end].splitlines():
        if not raw.strip():
            continue
        if ":" not in raw:
            return data, f"invalid frontmatter line: {raw}"
        key, value = raw.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data, None


def looks_like_rule_definition(line: str) -> bool:
    stripped = line.strip()
    if any(token in stripped for token in ("SECURITY_PATTERNS", "forbidden_patterns", "warn_patterns")):
        return True
    if stripped.startswith(("- \"", "- '")):
        return True
    if stripped.startswith(("r\"", "r'")):
        return True
    if "_pattern = r" in stripped:
        return True
    if "line_of(text, r" in stripped:
        return True
    if re.search(r'"\w+[.\w-]+",\s*r"', stripped):
        return True
    if stripped.startswith("- ") and ("\\s" in stripped or "\\b" in stripped or "\\(" in stripped):
        return True
    return False


def line_of(text: str, pattern: str, *, skip_rule_defs: bool = True) -> int | None:
    regex = re.compile(pattern, re.IGNORECASE)
    for index, line in enumerate(text.splitlines(), 1):
        if skip_rule_defs and looks_like_rule_definition(line):
            continue
        if regex.search(line):
            return index
    return None


def audit_structure(root: Path, findings: list[Finding]) -> None:
    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        add(findings, BLOCKER, "structure.required_file", skill_md, "SKILL.md is required at the skill root.")
        return

    text = read_text(skill_md)
    fm, error = parse_frontmatter(text)
    if error:
        add(findings, BLOCKER, "frontmatter.parse", skill_md, error)
        return

    name = fm.get("name", "")
    description = fm.get("description", "")
    if not name:
        add(findings, BLOCKER, "frontmatter.name", skill_md, "frontmatter name is required.")
    elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        add(findings, BLOCKER, "frontmatter.name_format", skill_md, "name must use lowercase letters, digits, and hyphens only.")
    if not description:
        add(findings, BLOCKER, "frontmatter.description", skill_md, "frontmatter description is required.")
    elif not description.startswith("Use when"):
        add(findings, WARN, "frontmatter.description_trigger", skill_md, "description should start with 'Use when' and describe trigger conditions.")
    if len("\n".join(f"{k}: {v}" for k, v in fm.items())) > 1024:
        add(findings, WARN, "frontmatter.length", skill_md, "frontmatter is over 1024 characters.")

    todo_line = line_of(text, r"\bTODO\b|\[TODO|placeholder|Delete this entire")
    if todo_line:
        add(findings, BLOCKER, "template.leftover", skill_md, "unfinished template marker remains.", todo_line)

    words = len(re.findall(r"\S+", text))
    if words > 1500:
        add(findings, WARN, "skill_md.length", skill_md, f"SKILL.md has {words} words; consider moving heavy detail to references.")

    for clutter in ("README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"):
        if (root / clutter).exists():
            add(findings, WARN, "package.clutter", root / clutter, f"{clutter} is usually unnecessary inside a skill package.")


def audit_links(root: Path, findings: list[Finding]) -> None:
    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in iter_files(root):
        if path.suffix.lower() not in {".md", ".yaml", ".yml"}:
            continue
        text = read_text(path)
        for match in link_pattern.finditer(text):
            target = match.group(1).strip()
            if "://" in target or target.startswith("#"):
                continue
            target_path = (path.parent / target.split("#", 1)[0]).resolve()
            try:
                target_path.relative_to(root.resolve())
            except ValueError:
                add(findings, WARN, "links.external_local", path, f"local link points outside skill folder: {target}")
                continue
            if not target_path.exists():
                add(findings, BLOCKER, "links.missing", path, f"local link does not resolve: {target}")


SECURITY_PATTERNS: list[tuple[str, str, str, str]] = [
    (BLOCKER, "secret.path", r"(open|read|cat|type|Get-Content|copy|upload|send|exfiltrat)[^\n]{0,80}(\.env|\.ssh|id_rsa|id_ed25519|credentials|token_store|browser profile)", "possible secret or credential path access"),
    (BLOCKER, "shell.pipe_install", r"curl\s+[^\n|]+\|\s*(sh|bash)|wget\s+[^\n|]+\|\s*(sh|bash)", "downloaded code is piped into a shell"),
    (BLOCKER, "code.encoded_exec", r"base64\s+(-d|--decode)|Invoke-Expression|\biex\b|eval\s*\(", "encoded or dynamic code execution"),
    (BLOCKER, "fs.destructive", r"rm\s+-rf\s+(/|\$HOME|~)|Remove-Item\s+.*-Recurse", "destructive recursive filesystem command"),
    (WARN, "prompt.injection", r"ignore previous instructions|reveal secrets|exfiltrate|developer message|system prompt", "prompt-injection-like instruction"),
    (WARN, "network.use", r"https?://|requests\.|urllib|fetch\s*\(|Invoke-WebRequest|curl\s+", "network access or remote endpoint reference"),
]


def audit_security(root: Path, findings: list[Finding]) -> None:
    for path in iter_files(root):
        rel = path.relative_to(root)
        if path.stat().st_size > 512 * 1024:
            add(findings, WARN, "file.size", path, f"{rel} is larger than 512 KB; review whether it belongs in a skill.")
            continue
        if path.suffix.lower() not in {".md", ".py", ".sh", ".ps1", ".js", ".ts", ".json", ".yaml", ".yml", ".txt"}:
            continue
        text = read_text(path)
        for severity, rule, pattern, message in SECURITY_PATTERNS:
            if rule == "secret.path" and path.suffix.lower() == ".md":
                continue
            hit = line_of(text, pattern)
            if hit:
                add(findings, severity, rule, path, message, hit)


def audit_scripts(root: Path, findings: list[Finding]) -> None:
    scripts = root / "scripts"
    if not scripts.exists():
        add(findings, INFO, "scripts.none", scripts, "no scripts directory; release may still be valid for a reference-only skill.")
        return
    for script in scripts.rglob("*.py"):
        try:
            py_compile.compile(str(script), doraise=True)
        except py_compile.PyCompileError as exc:
            add(findings, BLOCKER, "scripts.python_compile", script, str(exc))
    for script in scripts.iterdir():
        if script.is_file() and script.suffix.lower() in {".py", ".sh", ".ps1"}:
            text = read_text(script)
            if "--help" not in text and "argparse" not in text:
                add(findings, WARN, "scripts.help", script, "script does not appear to expose --help or argparse usage.")


def audit_openai_yaml(root: Path, findings: list[Finding]) -> None:
    path = root / "agents" / "openai.yaml"
    if not path.exists():
        add(findings, INFO, "metadata.openai_yaml_missing", path, "agents/openai.yaml is absent; acceptable, but marketplace UI metadata may be weaker.")
        return
    text = read_text(path)
    if "display_name:" not in text:
        add(findings, WARN, "metadata.display_name", path, "display_name missing.")
    if "short_description:" not in text:
        add(findings, WARN, "metadata.short_description", path, "short_description missing.")
    fm, _ = parse_frontmatter(read_text(root / "SKILL.md")) if (root / "SKILL.md").exists() else ({}, None)
    skill_name = fm.get("name")
    if skill_name and f"${skill_name}" not in text:
        add(findings, WARN, "metadata.default_prompt", path, f"default_prompt should mention ${skill_name}.")


def decision(findings: list[Finding]) -> str:
    if any(f.severity == BLOCKER for f in findings):
        return "BLOCKED"
    if any(f.severity == WARN for f in findings):
        return "READY_WITH_WARNINGS"
    return "READY"


def to_markdown(root: Path, findings: list[Finding]) -> str:
    lines = [f"# Skill release audit: {root.name}", "", f"Decision: `{decision(findings)}`", ""]
    if not findings:
        return "\n".join(lines + ["No findings."])
    for severity in (BLOCKER, WARN, INFO):
        group = [f for f in findings if f.severity == severity]
        if not group:
            continue
        lines.append(f"## {severity}")
        for finding in group:
            loc = finding.path
            if finding.line:
                loc = f"{loc}:{finding.line}"
            lines.append(f"- `{finding.rule}` {loc} - {finding.message}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_folder", type=Path)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--markdown", action="store_true", help="emit Markdown")
    args = parser.parse_args()

    root = args.skill_folder.resolve()
    findings: list[Finding] = []
    if not root.exists() or not root.is_dir():
        print(f"Skill folder not found: {root}", file=sys.stderr)
        return 2

    audit_structure(root, findings)
    audit_links(root, findings)
    audit_security(root, findings)
    audit_scripts(root, findings)
    audit_openai_yaml(root, findings)

    result = {"skill": str(root), "decision": decision(findings), "findings": [asdict(f) for f in findings]}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(to_markdown(root, findings))
    return 1 if result["decision"] == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
