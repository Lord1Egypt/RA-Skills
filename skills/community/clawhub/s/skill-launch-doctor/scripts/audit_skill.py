#!/usr/bin/env python3
"""Audit an AgentSkill-style skill folder for launch readiness."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


SEVERITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}


@dataclass
class Finding:
    severity: str
    category: str
    message: str
    fix: str
    path: str = ""


@dataclass
class AuditResult:
    target: str
    score: int
    verdict: str
    subscores: Dict[str, int]
    findings: List[Finding]
    suggested_description: str
    stats: Dict[str, int]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="replace")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> Tuple[Optional[str], Dict[str, str], str]:
    if not text.startswith("---\n"):
        return None, {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, {}, text
    raw = text[4:end].strip("\n")
    body = text[text.find("\n", end + 1) + 1 :]
    data: Dict[str, str] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            i += 1
            continue
        key, value = match.group(1), match.group(2)
        if value in {"|", ">"}:
            block: List[str] = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or not re.match(r"^[A-Za-z0-9_-]+:", lines[i])):
                block.append(lines[i].strip())
                i += 1
            data[key] = " ".join(part for part in block if part)
            continue
        data[key] = strip_quotes(value)
        i += 1
    return raw, data, body


def sentence_count(text: str) -> int:
    return len([part for part in re.split(r"[.!?]\s+", text.strip()) if part.strip()])


def words(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9_-]*", text.lower())


def has_any(text: str, patterns: Iterable[str]) -> bool:
    lower = text.lower()
    return any(pattern.lower() in lower for pattern in patterns)


def iter_files(root: Path) -> List[Path]:
    ignored = {".git", "__pycache__", "node_modules", ".venv", "venv", ".mypy_cache", ".pytest_cache"}
    output: List[Path] = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in ignored]
        for file_name in files:
            output.append(Path(current) / file_name)
    return output


def detect_file_references(text: str) -> List[str]:
    refs = set()
    for match in re.finditer(r"`([^`]+\.(?:md|py|sh|js|ts|json|yaml|yml|csv|txt))`", text):
        refs.add(match.group(1).strip())
    for match in re.finditer(r"\(([^)]+\.(?:md|py|sh|js|ts|json|yaml|yml|csv|txt))\)", text):
        refs.add(match.group(1).strip())
    return sorted(refs)


def category_score(max_score: int, penalties: List[int]) -> int:
    return max(0, max_score - sum(penalties))


def build_suggested_description(name: str, existing: str = "", trigger_ready: bool = False) -> str:
    if existing and trigger_ready:
        return existing
    return (
        f"Rewrite `{name or 'this-skill'}` with this shape: "
        "<clear action> <artifact or domain> for <specific outcome>. "
        "Use when <concrete user intent>, <second user intent>, or <third user intent>; "
        "mention important file types, tools, safety boundaries, or setup constraints only when they affect invocation."
    )


def audit(target: Path) -> AuditResult:
    root = target.resolve()
    if root.is_file() and root.name == "SKILL.md":
        root = root.parent

    findings: List[Finding] = []
    skill_md = root / "SKILL.md"
    all_files = iter_files(root) if root.exists() else []
    stats = {
        "files": len(all_files),
        "scripts": len([p for p in all_files if "/scripts/" in str(p)]),
        "references": len([p for p in all_files if "/references/" in str(p)]),
        "assets": len([p for p in all_files if "/assets/" in str(p)]),
    }

    if not root.exists():
        findings.append(Finding("P0", "structure", "Target path does not exist.", "Pass an existing skill directory or SKILL.md file.", str(target)))
        return AuditResult(str(target), 0, "BLOCKED", {"trigger": 0, "structure": 0, "compatibility": 0, "safety": 0, "market": 0}, findings, build_suggested_description("agent"), stats)

    if not skill_md.exists():
        findings.append(Finding("P0", "structure", "Missing SKILL.md.", "Add a SKILL.md file at the skill root.", rel(skill_md, root)))
        return AuditResult(str(root), 0, "BLOCKED", {"trigger": 0, "structure": 0, "compatibility": 0, "safety": 0, "market": 0}, findings, build_suggested_description(root.name), stats)

    text = read_text(skill_md)
    raw_fm, fm, body = parse_frontmatter(text)
    lower_text = text.lower()
    body_lines = [line for line in body.splitlines()]
    body_words = words(body)

    trigger_penalties: List[int] = []
    structure_penalties: List[int] = []
    compatibility_penalties: List[int] = []
    safety_penalties: List[int] = []
    market_penalties: List[int] = []

    if raw_fm is None:
        trigger_penalties.append(25)
        findings.append(Finding("P0", "trigger", "Missing or malformed YAML frontmatter.", "Start SKILL.md with a YAML block containing name and description.", "SKILL.md"))
    else:
        allowed = {"name", "description"}
        extra = sorted(set(fm) - allowed)
        if extra:
            compatibility_penalties.append(min(8, len(extra) * 2))
            findings.append(Finding("P2", "compatibility", f"Frontmatter has extra fields: {', '.join(extra)}.", "For maximum AgentSkills compatibility, keep frontmatter to name and description unless a target registry requires more.", "SKILL.md"))

    name = fm.get("name", "").strip()
    description = fm.get("description", "").strip()

    if not name:
        trigger_penalties.append(10)
        findings.append(Finding("P0", "trigger", "Missing frontmatter name.", "Add a lowercase hyphen-case name.", "SKILL.md"))
    elif not re.match(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$", name):
        trigger_penalties.append(5)
        findings.append(Finding("P1", "trigger", f"Name is not clean hyphen-case: {name}.", "Use lowercase letters, digits, and hyphens only.", "SKILL.md"))

    if not description:
        trigger_penalties.append(25)
        findings.append(Finding("P0", "trigger", "Missing frontmatter description.", "Add what the skill does and when to use it.", "SKILL.md"))
    else:
        desc_words = words(description)
        if len(description) < 120:
            trigger_penalties.append(12)
            findings.append(Finding("P1", "trigger", "Description is too short to trigger reliably.", "Describe the capability plus concrete use cases and user intents.", "SKILL.md"))
        if len(description) > 900:
            trigger_penalties.append(6)
            findings.append(Finding("P2", "trigger", "Description is very long.", "Keep trigger metadata dense; move details to the body or references.", "SKILL.md"))
        if not has_any(description, ["use when", "when", "reviewing", "creating", "editing", "installing", "publishing", "debugging"]):
            trigger_penalties.append(8)
            findings.append(Finding("P1", "trigger", "Description does not clearly state when to use the skill.", "Add trigger contexts such as 'Use when reviewing a SKILL.md...'.", "SKILL.md"))
        if len(set(desc_words)) < 18:
            trigger_penalties.append(6)
            findings.append(Finding("P2", "trigger", "Description has low keyword coverage.", "Include domain nouns, artifacts, and user intent phrases.", "SKILL.md"))
        if has_any(description, ["best", "ultimate", "magic", "revolutionary", "unlimited", "guaranteed"]):
            market_penalties.append(3)
            findings.append(Finding("P3", "market", "Description uses hype language.", "Replace hype with concrete capabilities and boundaries.", "SKILL.md"))

    if "[TODO" in text or "TODO:" in text or re.search(r"\bTODO\b", text):
        structure_penalties.append(8)
        findings.append(Finding("P1", "structure", "Skill still contains TODO placeholders.", "Remove template TODOs before launch.", "SKILL.md"))

    if len(body_lines) < 20:
        structure_penalties.append(8)
        findings.append(Finding("P1", "structure", "Body is too thin for another agent to execute reliably.", "Add a quick start, workflow, review criteria, and output contract.", "SKILL.md"))
    if len(body_lines) > 500:
        structure_penalties.append(6)
        findings.append(Finding("P2", "structure", "Body is long enough to hurt progressive disclosure.", "Move detailed examples, schemas, or provider notes into references/.", "SKILL.md"))
    if not has_any(body, ["quick start", "workflow", "output contract", "decision", "steps"]):
        structure_penalties.append(6)
        findings.append(Finding("P2", "structure", "Body lacks an execution shape.", "Add a quick start, workflow, decision tree, or output contract.", "SKILL.md"))
    if stats["scripts"] == 0 and has_any(body, ["script", "automate", "audit", "score", "validate", "generate"]):
        structure_penalties.append(4)
        findings.append(Finding("P2", "structure", "Body implies automation but no scripts are bundled.", "Add scripts for repeated checks or remove automation claims.", "SKILL.md"))

    aux_docs = [p for p in all_files if p.name.upper() in {"README.MD", "CHANGELOG.MD", "INSTALLATION_GUIDE.MD", "QUICK_REFERENCE.MD"}]
    if aux_docs:
        structure_penalties.append(min(5, len(aux_docs)))
        findings.append(Finding("P3", "structure", "Auxiliary docs can dilute a skill package.", "Keep only files directly used by agents; move launch docs outside the skill when possible.", ", ".join(rel(p, root) for p in aux_docs)))

    refs = detect_file_references(text)
    missing_refs = []
    for ref in refs:
        normalized = ref.replace("{baseDir}/", "").replace("./", "")
        if normalized.startswith("/"):
            continue
        if not (root / normalized).exists():
            missing_refs.append(ref)
    if missing_refs:
        structure_penalties.append(min(10, len(missing_refs) * 2))
        findings.append(Finding("P1", "structure", "SKILL.md references missing bundled files.", "Create the files or update the references: " + ", ".join(missing_refs), "SKILL.md"))

    absolute_paths = re.findall(r"/Users/[^\s`\"')]+|/home/[^\s`\"')]+", text)
    if absolute_paths:
        compatibility_penalties.append(8)
        findings.append(Finding("P1", "compatibility", "Skill contains user-local absolute paths.", "Use relative paths, {baseDir}, or ask the user for their local path.", "SKILL.md"))

    platform_terms = ["codex only", "claude only", "hermes only", "runtime only", "one runtime only"]
    if has_any(lower_text, platform_terms):
        compatibility_penalties.append(8)
        findings.append(Finding("P1", "compatibility", "Skill appears locked to one runtime.", "Make the generic path primary and put runtime-specific notes behind conditional guidance.", "SKILL.md"))

    if has_any(lower_text, ["requires api key", "api_key", "secret", "token"]):
        if not has_any(lower_text, ["environment", "env", "placeholder", "never commit", "setup"]):
            safety_penalties.append(7)
            findings.append(Finding("P1", "safety", "Credential-related text lacks setup or secrecy guidance.", "Explain how to provide credentials without committing or printing secrets.", "SKILL.md"))

    dangerous_patterns = [
        r"rm\s+-rf\s+/",
        r"git\s+reset\s+--hard",
        r"curl\s+[^|]+\|\s*(sh|bash)",
        r"chmod\s+777",
        r"sudo\s+",
        r"eval\s+",
        r"DROP\s+TABLE",
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            safety_penalties.append(10)
            findings.append(Finding("P1", "safety", f"Potentially dangerous command pattern found: {pattern}.", "Add explicit user approval, safer alternatives, or remove the command.", "SKILL.md"))
            break

    if has_any(lower_text, ["send email", "publish", "delete", "payment", "buy", "transfer", "deploy", "post to"]):
        if not has_any(lower_text, ["ask", "approval", "confirm", "explicit", "dry run", "preview"]):
            safety_penalties.append(8)
            findings.append(Finding("P1", "safety", "Sensitive external action lacks an approval gate.", "Require explicit user confirmation before external writes, payments, publishing, or destructive actions.", "SKILL.md"))

    if not has_any(body, ["output contract", "expected output", "report", "include:"]):
        market_penalties.append(5)
        findings.append(Finding("P2", "market", "No clear output contract.", "Tell downstream agents exactly what to return to the user.", "SKILL.md"))
    if sentence_count(body[:1200]) > 18:
        market_penalties.append(3)
        findings.append(Finding("P3", "market", "Opening section is dense.", "Make the first screen quick-start oriented.", "SKILL.md"))
    if len(body_words) > 3500:
        market_penalties.append(5)
        findings.append(Finding("P2", "market", "Skill body is very wordy.", "Move detailed references out of SKILL.md and keep only routing instructions.", "SKILL.md"))

    script_files = [p for p in all_files if "/scripts/" in str(p) and p.suffix in {".py", ".sh", ".js", ".ts"}]
    for script in script_files:
        content = read_text(script)
        if script.suffix == ".py" and "argparse" not in content and "if __name__" not in content:
            structure_penalties.append(2)
            findings.append(Finding("P3", "structure", f"Script may not be directly runnable: {rel(script, root)}.", "Give scripts a CLI entrypoint or document how to call them.", rel(script, root)))
        if re.search(r"(sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)", content):
            safety_penalties.append(20)
            findings.append(Finding("P0", "safety", f"Possible secret in bundled script: {rel(script, root)}.", "Remove the secret, rotate it, and use placeholders or environment variables.", rel(script, root)))

    subscores = {
        "trigger": category_score(30, trigger_penalties),
        "structure": category_score(25, structure_penalties),
        "compatibility": category_score(15, compatibility_penalties),
        "safety": category_score(15, safety_penalties),
        "market": category_score(15, market_penalties),
    }
    score = sum(subscores.values())

    if any(f.severity == "P0" for f in findings):
        verdict = "BLOCKED"
    elif score >= 90:
        verdict = "READY"
    elif score >= 80:
        verdict = "READY WITH FIXES"
    elif score >= 65:
        verdict = "NEEDS WORK"
    else:
        verdict = "NOT READY"

    findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 9), f.category, f.path, f.message))
    return AuditResult(
        str(root),
        score,
        verdict,
        subscores,
        findings,
        build_suggested_description(name or root.name, description, subscores["trigger"] >= 26),
        stats,
    )


def render_markdown(result: AuditResult) -> str:
    lines: List[str] = []
    lines.append("# Skill Launch Doctor Report")
    lines.append("")
    lines.append(f"Target: `{result.target}`")
    lines.append(f"Overall: {result.score}/100 - {result.verdict}")
    lines.append("")
    lines.append("## Subscores")
    lines.append("")
    for key, value in result.subscores.items():
        lines.append(f"- {key}: {value}")
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    if not result.findings:
        lines.append("- No findings.")
    else:
        for finding in result.findings:
            path = f" `{finding.path}`" if finding.path else ""
            lines.append(f"- [{finding.severity}] {finding.category}:{path} {finding.message}")
            lines.append(f"  Fix: {finding.fix}")
    lines.append("")
    lines.append("## Suggested Description")
    lines.append("")
    lines.append(result.suggested_description)
    lines.append("")
    lines.append("## Launch Fix Order")
    lines.append("")
    if any(f.severity in {"P0", "P1"} for f in result.findings):
        for sev in ("P0", "P1"):
            for finding in [f for f in result.findings if f.severity == sev]:
                lines.append(f"- {sev}: {finding.fix}")
    else:
        lines.append("- Polish marketplace copy, run one realistic forward test, then publish.")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Audit an AgentSkill folder for launch readiness.")
    parser.add_argument("target", help="Path to a skill directory or SKILL.md")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--fail-under", type=int, default=None, help="Exit non-zero when score is below this value.")
    args = parser.parse_args(argv)

    result = audit(Path(args.target))
    if args.format == "json":
        payload = asdict(result)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render_markdown(result))

    if result.verdict == "BLOCKED":
        return 2
    if args.fail_under is not None and result.score < args.fail_under:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
