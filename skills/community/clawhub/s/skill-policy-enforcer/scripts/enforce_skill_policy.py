#!/usr/bin/env python3
"""Enforce a local policy over an agent skill folder."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable


DENY = "deny"
WARN = "warn"


DEFAULT_POLICY: dict[str, Any] = {
    "policy_name": "default-conservative-skill-policy",
    "max_skill_md_words": 1200,
    "max_file_size_kb": 256,
    "allow_network": False,
    "allow_secret_reads": False,
    "require_files": ["SKILL.md"],
    "allowed_frontmatter_fields": ["name", "description"],
    "forbidden_paths": [".env", ".ssh", "id_rsa", "id_ed25519", "credentials", "token", "browser profile"],
    "forbidden_patterns": [
        r"curl\s+[^\n|]+\|\s*(sh|bash)",
        r"Invoke-Expression",
        r"\biex\b",
        r"base64\s+(-d|--decode)",
        r"eval\s*\(",
        r"rm\s+-rf\s+(/|\$HOME|~)",
        r"Remove-Item\s+.*-Recurse",
    ],
    "warn_patterns": [r"\bTODO\b", r"placeholder", r"ignore previous instructions", r"reveal secrets"],
}


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


def parse_scalar(value: str) -> Any:
    value = value.strip().strip("\"'")
    value = value.replace("\\\\", "\\")
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    try:
        return int(value)
    except ValueError:
        return value


def parse_simple_yaml(text: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line:
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(parse_scalar(line[4:]))
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            if value.strip():
                data[key] = parse_scalar(value)
                current_key = None
            else:
                data[key] = []
                current_key = key
    return data


def load_policy(path: Path | None) -> dict[str, Any]:
    if path is None:
        return dict(DEFAULT_POLICY)
    text = read_text(path)
    if path.suffix.lower() == ".json":
        loaded = json.loads(text)
    else:
        loaded = parse_simple_yaml(text)
    policy = dict(DEFAULT_POLICY)
    policy.update(loaded)
    return policy


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
    if any(token in stripped for token in ("DEFAULT_POLICY", "forbidden_patterns", "warn_patterns")):
        return True
    if stripped.startswith(("- \"", "- '")):
        return True
    if stripped.startswith(("r\"", "r'")):
        return True
    if "_pattern = r" in stripped:
        return True
    if "line_of(text, r" in stripped:
        return True
    if stripped.startswith("- ") and ("\\s" in stripped or "\\b" in stripped or "\\(" in stripped):
        return True
    if re.search(r'"\w+[.\w-]+",\s*r"', stripped):
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


def enforce_structure(root: Path, policy: dict[str, Any], findings: list[Finding]) -> None:
    for rel in policy.get("require_files", []):
        required = root / rel
        if not required.exists():
            add(findings, DENY, f"require_files:{rel}", required, "required file is missing.")

    skill_md = root / "SKILL.md"
    if not skill_md.exists():
        return
    text = read_text(skill_md)
    fm, error = parse_frontmatter(text)
    if error:
        add(findings, DENY, "frontmatter.parse", skill_md, error)
    allowed = set(policy.get("allowed_frontmatter_fields", []))
    for key in fm:
        if allowed and key not in allowed:
            add(findings, DENY, f"frontmatter.allowed_fields:{key}", skill_md, f"frontmatter field '{key}' is not allowed.")
    if "name" not in fm or "description" not in fm:
        add(findings, DENY, "frontmatter.required", skill_md, "frontmatter must include name and description.")
    words = len(re.findall(r"\S+", text))
    max_words = int(policy.get("max_skill_md_words", 0) or 0)
    if max_words and words > max_words:
        add(findings, DENY, "max_skill_md_words", skill_md, f"SKILL.md has {words} words; limit is {max_words}.")


def enforce_files(root: Path, policy: dict[str, Any], findings: list[Finding]) -> None:
    max_kb = int(policy.get("max_file_size_kb", 0) or 0)
    forbidden_paths = [str(item).lower() for item in policy.get("forbidden_paths", [])]
    for path in iter_files(root):
        rel = path.relative_to(root).as_posix().lower()
        for forbidden in forbidden_paths:
            if forbidden and forbidden in rel:
                add(findings, DENY, f"forbidden_paths:{forbidden}", path, "path is forbidden by policy.")
        if max_kb and path.stat().st_size > max_kb * 1024:
            add(findings, DENY, "max_file_size_kb", path, f"file size exceeds {max_kb} KB.")


def enforce_patterns(root: Path, policy: dict[str, Any], findings: list[Finding]) -> None:
    secret_pattern = r"(open|read|cat|type|Get-Content|copy|upload|send|exfiltrat)[^\n]{0,80}(\.env|\.ssh|id_rsa|id_ed25519|credentials|token_store|browser profile)"
    network_pattern = r"requests\.|urllib|fetch\s*\(|Invoke-WebRequest|curl\s+|wget\s+"
    for path in iter_files(root):
        if path.suffix.lower() not in {".md", ".py", ".sh", ".ps1", ".js", ".ts", ".json", ".yaml", ".yml", ".txt"}:
            continue
        text = read_text(path)
        if not policy.get("allow_secret_reads", False):
            hit = line_of(text, secret_pattern)
            if hit:
                add(findings, DENY, "allow_secret_reads:false", path, "secret or credential path reference is disallowed.", hit)
        if not policy.get("allow_network", False):
            hit = line_of(text, network_pattern)
            if hit:
                add(findings, DENY, "allow_network:false", path, "network access or URL reference is disallowed.", hit)
        for pattern in policy.get("forbidden_patterns", []):
            hit = line_of(text, str(pattern))
            if hit:
                add(findings, DENY, f"forbidden_patterns:{pattern}", path, "content matches a forbidden pattern.", hit)
        for pattern in policy.get("warn_patterns", []):
            hit = line_of(text, str(pattern))
            if hit:
                add(findings, WARN, f"warn_patterns:{pattern}", path, "content matches a warning pattern.", hit)


def status(findings: list[Finding]) -> str:
    if any(item.severity == DENY for item in findings):
        return "FAIL"
    if any(item.severity == WARN for item in findings):
        return "PASS_WITH_WARNINGS"
    return "PASS"


def to_markdown(root: Path, policy: dict[str, Any], findings: list[Finding]) -> str:
    lines = [
        f"# Skill policy result: {root.name}",
        "",
        f"Policy: `{policy.get('policy_name', 'unnamed')}`",
        f"Status: `{status(findings)}`",
        "",
    ]
    if not findings:
        return "\n".join(lines + ["No findings."])
    for severity in (DENY, WARN):
        group = [item for item in findings if item.severity == severity]
        if not group:
            continue
        lines.append(f"## {severity}")
        for item in group:
            loc = item.path if item.line is None else f"{item.path}:{item.line}"
            lines.append(f"- `{item.rule}` {loc} - {item.message}")
        lines.append("")
    return "\n".join(lines).rstrip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_folder", type=Path)
    parser.add_argument("--policy", type=Path, help="JSON or simple YAML policy file")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--markdown", action="store_true", help="emit Markdown")
    args = parser.parse_args()

    root = args.skill_folder.resolve()
    if not root.exists() or not root.is_dir():
        print(f"Skill folder not found: {root}", file=sys.stderr)
        return 2

    policy = load_policy(args.policy)
    findings: list[Finding] = []
    enforce_structure(root, policy, findings)
    enforce_files(root, policy, findings)
    enforce_patterns(root, policy, findings)

    result = {
        "skill": str(root),
        "policy": policy.get("policy_name", "unnamed"),
        "status": status(findings),
        "findings": [asdict(item) for item in findings],
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(to_markdown(root, policy, findings))
    return 1 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
