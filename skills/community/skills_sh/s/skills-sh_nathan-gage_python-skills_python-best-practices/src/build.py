#!/usr/bin/env python3
"""Compile rule files into a single AGENTS.md document.

Walks `rules/`, reads frontmatter and body from each rule, groups by section
prefix, and generates a single document with table of contents, abstract, and
expanded rules — matching the Vercel agent-skills layout.

Usage:
    python src/build.py

Run from the skill root (the directory containing `rules/`, `metadata.json`, etc.)
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
SECTION_RE = re.compile(
    r"^## (\d+)\. (.+?) \((\w+)\)\s*\n+\*\*Impact:\*\* ([\w\-]+)\s*\n+\*\*Description:\*\* (.+?)(?=\n## |\Z)",
    re.DOTALL | re.MULTILINE,
)


@dataclass(frozen=True)
class Section:
    order: int
    title: str
    prefix: str
    impact: str
    description: str


@dataclass
class Rule:
    filename: str
    title: str
    impact: str
    impact_description: str | None
    tags: list[str]
    body: str  # body with leading `## Rule Title\n` line stripped


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise ValueError("missing frontmatter")
    fm_raw, body = match.group(1), match.group(2)
    frontmatter: dict[str, str] = {}
    for line in fm_raw.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        frontmatter[key.strip()] = value.strip()
    return frontmatter, body


def load_sections(sections_path: Path) -> list[Section]:
    text = sections_path.read_text()
    sections: list[Section] = []
    for m in SECTION_RE.finditer(text):
        order = int(m.group(1))
        title = m.group(2).strip()
        prefix = m.group(3).strip()
        impact = m.group(4).strip()
        description = m.group(5).strip()
        sections.append(Section(order, title, prefix, impact, description))
    sections.sort(key=lambda s: s.order)
    return sections


def load_rules(rules_dir: Path) -> list[Rule]:
    rules: list[Rule] = []
    for path in sorted(rules_dir.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text()
        frontmatter, body = parse_frontmatter(text)
        body = body.lstrip()
        # Strip the duplicated `## {title}` line at the top of the body
        lines = body.split("\n", 1)
        if lines and lines[0].startswith("## "):
            body = lines[1] if len(lines) > 1 else ""
            body = body.lstrip()
        tags_raw = frontmatter.get("tags", "")
        tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
        rules.append(
            Rule(
                filename=path.name,
                title=frontmatter["title"],
                impact=frontmatter.get("impact", ""),
                impact_description=frontmatter.get("impactDescription"),
                tags=tags,
                body=body.rstrip(),
            )
        )
    return rules


def group_rules(
    sections: list[Section], rules: list[Rule]
) -> list[tuple[Section, list[Rule]]]:
    groups: list[tuple[Section, list[Rule]]] = []
    for section in sections:
        matching = [
            r for r in rules if r.filename.split("-", 1)[0] == section.prefix
        ]
        matching.sort(key=lambda r: r.title)
        groups.append((section, matching))
    return groups


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    slug = re.sub(r"\s+", "-", slug)
    return slug


def render_toc(groups: list[tuple[Section, list[Rule]]]) -> str:
    lines: list[str] = ["## Table of Contents", ""]
    for section, rules in groups:
        section_anchor = f"{section.order}-{slugify(section.title)}"
        lines.append(
            f"{section.order}. [{section.title}](#{section_anchor}) — **{section.impact}**"
        )
        for idx, rule in enumerate(rules, 1):
            rule_id = f"{section.order}.{idx}"
            anchor_id = f"{section.order}{idx}-{slugify(rule.title)}"
            lines.append(f"   - {rule_id} [{rule.title}](#{anchor_id})")
    lines.append("")
    return "\n".join(lines)


def render_rules(groups: list[tuple[Section, list[Rule]]]) -> str:
    parts: list[str] = []
    for section, rules in groups:
        parts.append(f"## {section.order}. {section.title}\n")
        parts.append(f"**Impact: {section.impact}**\n")
        parts.append(f"{section.description}\n")
        for idx, rule in enumerate(rules, 1):
            rule_id = f"{section.order}.{idx}"
            parts.append(f"### {rule_id} {rule.title}\n")
            impact_line = f"**Impact: {rule.impact}"
            if rule.impact_description:
                impact_line += f" ({rule.impact_description})"
            impact_line += "**\n"
            parts.append(impact_line)
            parts.append(f"{rule.body}\n")
    return "\n".join(parts)


def render_document(
    metadata: dict[str, object],
    sections: list[Section],
    rules: list[Rule],
) -> str:
    groups = group_rules(sections, rules)
    header = f"""# Python Best Practices

**Version {metadata["version"]}**
{metadata["organization"]}
{metadata["date"]}

> **Note:**
> This document is optimized for AI agents and LLMs that maintain, generate,
> or refactor Python codebases. Humans may also find it useful, but the
> guidance, examples, and framing prioritize consistency and pattern-matching
> for AI-assisted workflows.

---

## Abstract

{metadata["abstract"]}

---
"""
    toc = render_toc(groups)
    body = render_rules(groups)
    references = "\n## References\n\n"
    refs = metadata.get("references")
    if isinstance(refs, list):
        for ref in refs:
            references += f"- {ref}\n"
    return f"{header}\n{toc}\n---\n\n{body}\n{references}"


def main() -> int:
    root = Path.cwd()
    metadata_path = root / "metadata.json"
    sections_path = root / "rules" / "_sections.md"
    rules_dir = root / "rules"
    output_path = root / "AGENTS.md"

    if not metadata_path.exists():
        print(f"metadata.json not found at {metadata_path}", file=sys.stderr)
        return 1
    if not sections_path.exists():
        print(f"_sections.md not found at {sections_path}", file=sys.stderr)
        return 1

    metadata: dict[str, object] = json.loads(metadata_path.read_text())
    sections = load_sections(sections_path)
    rules = load_rules(rules_dir)

    document = render_document(metadata, sections, rules)
    output_path.write_text(document)

    print(
        f"wrote {output_path.name}: "
        f"{len(sections)} sections, {len(rules)} rules, "
        f"{len(document):,} bytes",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
