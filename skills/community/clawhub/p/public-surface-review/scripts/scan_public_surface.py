#!/usr/bin/env python3
"""Inspect public files for audience-fit and packaging problems."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
INTERNAL_DOC_PATTERNS = (
    "social-posts.md",
    "launch-plan.md",
    "publish-checklist.md",
    "github-star-audit.md",
    "reference-patterns.md",
    "demo-script.md",
)
INTERNAL_TERMS = re.compile(
    r"\b(oauth|subagent|main thread|benchmark contract|workflow contract|agent threads|paid api key|control plane)\b",
    re.IGNORECASE,
)
STRONG_INTERNAL_PROMPT_TERMS = re.compile(
    r"\b(main thread|benchmark contract|workflow contract|agent threads|paid api key|control plane|subagent notes?)\b",
    re.IGNORECASE,
)
DEFAULT_PROMPT_LINE = re.compile(r"^(\s*)default_prompt:\s*(.*)$")
BLOCK_SCALAR_HEADER = re.compile(r"^[|>](?:[-+](?:[1-9])?|[1-9][-+]?)?$")
IGNORE_DIRS = {".git", "__pycache__", "dist", "build", "node_modules", ".venv", "venv"}
FALSE_ASSURANCE_PATTERNS = (
    re.compile(r"\bzero false positives?\b", re.IGNORECASE),
    re.compile(r"\bperfect scanner\b", re.IGNORECASE),
    re.compile(r"\bguaranteed safe\b", re.IGNORECASE),
    re.compile(r"\b(?:provides|offers|gives|delivers|ensures)\s+exhaustive (?:safety|security coverage|scanning|protection)\b", re.IGNORECASE),
    re.compile(r"\bsecret-free guarantee\b", re.IGNORECASE),
)


def count_section_bullets(lines: list[str], *headings: str) -> int:
    heading_lookup = {heading.lower() for heading in headings}
    in_section = False
    count = 0
    for line in lines:
        if line.startswith("#"):
            in_section = line.strip().lower() in heading_lookup
            continue
        if in_section and line.lstrip().startswith(("-", "*")):
            count += 1
    return count


def add_finding(findings: list[dict[str, object]], *, code: str, severity: str, file: str, detail: str) -> None:
    findings.append({"code": code, "severity": severity, "file": file, "detail": detail})


def display_input_label(raw_arg: str, resolved: Path) -> str:
    raw_path = Path(raw_arg).expanduser()
    if not raw_path.is_absolute():
        return raw_path.as_posix() or "."
    return resolved.name or "."


def extract_default_prompts(text: str) -> list[str]:
    prompts: list[str] = []
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        match = DEFAULT_PROMPT_LINE.match(lines[index])
        if not match:
            index += 1
            continue

        base_indent = len(match.group(1))
        inline_value = match.group(2).strip()
        if inline_value and not BLOCK_SCALAR_HEADER.fullmatch(inline_value):
            prompts.append(inline_value.strip("\"'"))
            index += 1
            continue

        block_indent: int | None = None
        block_lines: list[str] = []
        index += 1
        while index < len(lines):
            line = lines[index]
            stripped = line.strip()
            current_indent = len(line) - len(line.lstrip(" "))
            if stripped and current_indent <= base_indent:
                break
            if not stripped:
                block_lines.append("")
                index += 1
                continue
            if block_indent is None:
                block_indent = current_indent
            block_lines.append(line[block_indent:])
            index += 1
        prompts.append("\n".join(block_lines).strip())
    return [prompt for prompt in prompts if prompt]


def check_false_assurance(findings: list[dict[str, object]], *, path: Path, root: Path) -> None:
    text = path.read_text(encoding="utf-8")
    rel_path = str(path.relative_to(root))
    for line in text.splitlines():
        for pattern in FALSE_ASSURANCE_PATTERNS:
            if pattern.search(line):
                add_finding(
                    findings,
                    code="false-assurance-language",
                    severity="warning",
                    file=rel_path,
                    detail="Public docs should not claim perfect, exhaustive, or guaranteed release safety.",
                )
                return


def iter_repo_files(root: Path, *, name: str | None = None) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*" if name is None else name):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS or part.startswith(".venv") for part in path.relative_to(root).parts[:-1]):
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, help="Repo root to inspect.")
    parser.add_argument("--out", required=True, help="Output JSON file.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    findings: list[dict[str, object]] = []
    readme = root / "README.md"
    if readme.exists():
        lines = readme.read_text(encoding="utf-8").splitlines()
        if len(lines) > 220:
            add_finding(findings, code="readme-too-long", severity="warning", file="README.md", detail="README exceeds 220 lines.")
        quick_start_line = next((idx for idx, line in enumerate(lines, start=1) if "quick start" in line.lower()), None)
        if quick_start_line is None or quick_start_line > 80:
            add_finding(findings, code="quick-start-buried", severity="warning", file="README.md", detail="Quick Start heading is missing or too far from the top.")
        first_fence = next((idx for idx, line in enumerate(lines, start=1) if line.strip().startswith("```")), None)
        if first_fence is None or first_fence > 100:
            add_finding(findings, code="no-early-command-example", severity="warning", file="README.md", detail="No early runnable code example near the top of the README.")
        top_text = "\n".join(lines[:60])
        internal_hits = len(INTERNAL_TERMS.findall(top_text))
        if internal_hits >= 4:
            add_finding(findings, code="internal-language-near-top", severity="warning", file="README.md", detail="README intro uses too much internal or operator-facing language.")
        if count_section_bullets(lines, "## what is included", "## included") > 20:
            add_finding(findings, code="giant-file-inventory", severity="warning", file="README.md", detail="Large file inventory section is likely low-value for public readers.")
        check_false_assurance(findings, path=readme, root=root)

    for doc_name in INTERNAL_DOC_PATTERNS:
        matches = iter_repo_files(root, name=doc_name)
        for match in matches:
            add_finding(
                findings,
                code="internal-launch-doc-present",
                severity="warning",
                file=str(match.relative_to(root)),
                detail="Internal launch or marketing doc is present in the repo working tree.",
            )

    skill_paths = iter_repo_files(root, name="SKILL.md")
    for skill_path in skill_paths:
        rel_path = str(skill_path.relative_to(root))
        lines = skill_path.read_text(encoding="utf-8").splitlines()
        if len(lines) > 260:
            add_finding(findings, code="skill-too-long", severity="warning", file=rel_path, detail="Public SKILL.md is longer than 260 lines.")
        top_text = "\n".join(lines[:120])
        if len(INTERNAL_TERMS.findall(top_text)) >= 5:
            add_finding(findings, code="skill-too-internal", severity="warning", file=rel_path, detail="Top of SKILL.md reads like internal control text instead of user-facing guidance.")
        check_false_assurance(findings, path=skill_path, root=root)

    yaml_paths = iter_repo_files(root, name="openai.yaml")
    for yaml_path in yaml_paths:
        rel_path = str(yaml_path.relative_to(root))
        text = yaml_path.read_text(encoding="utf-8")
        prompt_text = "\n".join(extract_default_prompts(text))
        prompt_hits = len(INTERNAL_TERMS.findall(prompt_text))
        if prompt_text and (prompt_hits >= 2 or STRONG_INTERNAL_PROMPT_TERMS.search(prompt_text)):
            add_finding(findings, code="public-prompt-too-internal", severity="warning", file=rel_path, detail="Public default prompt exposes too much internal workflow language.")

    for doc_path in (
        root / "SECURITY.md",
        root / "CONTRIBUTING.md",
        root / ".github" / "pull_request_template.md",
    ):
        if doc_path.exists():
            check_false_assurance(findings, path=doc_path, root=root)

    codex_docs_root = root / "docs" / "codex"
    if codex_docs_root.exists():
        for doc_path in sorted(codex_docs_root.rglob("*.md")):
            if any(part in IGNORE_DIRS or part.startswith(".venv") for part in doc_path.relative_to(root).parts[:-1]):
                continue
            check_false_assurance(findings, path=doc_path, root=root)

    payload = {
        "root": display_input_label(args.root, root),
        "finding_count": len(findings),
        "error_count": sum(1 for item in findings if item["severity"] == "error"),
        "warning_count": sum(1 for item in findings if item["severity"] == "warning"),
        "findings": findings,
    }
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
