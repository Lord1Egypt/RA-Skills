#!/usr/bin/env python3
"""Lint rule files for structural correctness.

Checks:
- Frontmatter present, parseable, with required fields (`title`, `impact`, `tags`)
- `references` present when the rule body mentions a Python version, PEP, or
  named third-party library (Pydantic, mypy, ruff, asyncio, etc.) that suggests
  primary-source corroboration is needed
- `impact` is one of the documented levels
- Body starts with `## {title}` matching the frontmatter title
- Body contains an Incorrect/Correct example pair (heuristic: looks for the
  bolded `**Incorrect` and `**Correct` markers)
- Filename prefix maps to a known section in `_sections.md`

Exits with a non-zero status if any rule fails.

Usage:
    python src/validate.py

Run from the skill root.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VALID_IMPACTS: frozenset[str] = frozenset(
    {"CRITICAL", "HIGH", "MEDIUM-HIGH", "MEDIUM", "LOW-MEDIUM", "LOW"}
)
REQUIRED_FRONTMATTER: tuple[str, ...] = ("title", "impact", "tags")

# Heuristics for "this rule depends on language/library behavior, so a
# primary-source reference is required". Any match → require `references`.
#
# Design intent: trigger on signals that are concretely version- or
# library-dependent (a specific stdlib API with known version semantics, a
# Pydantic v2 construct, a tool name) — *not* on bare module names like
# "typing" or "dataclasses" which appear in almost every rule body and would
# turn the validator into noise.
VERSION_OR_LIB_PATTERNS: tuple[re.Pattern[str], ...] = (
    # Concrete version mentions
    re.compile(r"\bPython\s+3\.\d+\+?\b", re.IGNORECASE),
    re.compile(r"\b3\.(?:9|10|11|12|13|14)\+\b"),
    re.compile(r"\bPEP[-\s]?\d+\b", re.IGNORECASE),
    # Version-sensitive stdlib APIs
    re.compile(r"\bwarnings\.deprecated\b"),
    re.compile(r"\bcached_property\b"),
    re.compile(r"\bassert_never\b"),
    re.compile(r"\bzoneinfo\b"),
    re.compile(r"\bKW_ONLY\b"),
    re.compile(r"\bExceptionGroup\b"),
    re.compile(r"\btomllib\b"),
    re.compile(r"\b@overload\b"),
    # Asyncio cancellation semantics shifted across versions
    re.compile(r"\bCancelledError\b"),
    re.compile(r"\basyncio\b"),
    # Third-party tools whose behavior the rule depends on
    re.compile(r"\bpydantic\b", re.IGNORECASE),
    re.compile(r"\bTypeAdapter\b"),
    re.compile(r"\bBaseModel\b"),
    re.compile(r"\bmodel_validator\b"),
    re.compile(r"\bmodel_dump\b"),
    re.compile(r"\bmypy\b"),
    re.compile(r"\bpyright\b"),
    re.compile(r"\bruff\b"),
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
SECTION_RE = re.compile(
    r"^## \d+\. .+? \((\w+)\)\s*\n", re.MULTILINE
)


@dataclass
class RuleIssue:
    filename: str
    issues: list[str] = field(default_factory=list)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str] | None:
    match = FRONTMATTER_RE.match(text)
    if match is None:
        return None
    fm_raw, body = match.group(1), match.group(2)
    frontmatter: dict[str, str] = {}
    for line in fm_raw.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        frontmatter[key.strip()] = value.strip()
    return frontmatter, body


def load_section_prefixes(sections_path: Path) -> set[str]:
    text = sections_path.read_text()
    return {m.group(1).strip() for m in SECTION_RE.finditer(text)}


def needs_reference(body: str) -> str | None:
    for pat in VERSION_OR_LIB_PATTERNS:
        m = pat.search(body)
        if m:
            return m.group(0)
    return None


def validate_rule(
    path: Path, valid_prefixes: set[str]
) -> RuleIssue:
    issue = RuleIssue(filename=path.name)
    text = path.read_text()

    parsed = parse_frontmatter(text)
    if parsed is None:
        issue.issues.append("missing or malformed frontmatter")
        return issue
    frontmatter, body = parsed

    for required in REQUIRED_FRONTMATTER:
        if required not in frontmatter or not frontmatter[required]:
            issue.issues.append(f"missing required frontmatter field: {required!r}")

    impact = frontmatter.get("impact", "")
    if impact and impact not in VALID_IMPACTS:
        issue.issues.append(
            f"impact {impact!r} not in {sorted(VALID_IMPACTS)}"
        )

    prefix = path.stem.split("-", 1)[0]
    if prefix not in valid_prefixes:
        issue.issues.append(
            f"filename prefix {prefix!r} not in _sections.md prefixes "
            f"({sorted(valid_prefixes)})"
        )

    title = frontmatter.get("title", "").strip()
    body_stripped = body.lstrip()
    first_line = body_stripped.split("\n", 1)[0]
    # Compare titles ignoring backticks/whitespace — bodies usually format
    # API names with code fences while frontmatter strings stay plain.
    def _normalize(s: str) -> str:
        return re.sub(r"\s+", " ", s.replace("`", "").strip())
    if title and not first_line.startswith("## "):
        issue.issues.append(
            f"body must start with '## {title}'; found {first_line!r}"
        )
    elif title and _normalize(first_line[3:]) != _normalize(title):
        issue.issues.append(
            f"body heading {_normalize(first_line[3:])!r} "
            f"does not match frontmatter title {_normalize(title)!r}"
        )

    if "**Incorrect" not in body:
        issue.issues.append("body missing **Incorrect** example marker")
    if "**Correct" not in body:
        issue.issues.append("body missing **Correct** example marker")

    references = frontmatter.get("references", "").strip()
    trigger = needs_reference(body)
    if trigger and not references:
        issue.issues.append(
            f"body mentions {trigger!r} (version/library) but `references` is missing"
        )

    return issue


def main() -> int:
    root = Path.cwd()
    rules_dir = root / "rules"
    sections_path = rules_dir / "_sections.md"

    if not sections_path.exists():
        print(f"_sections.md not found at {sections_path}", file=sys.stderr)
        return 1

    valid_prefixes = load_section_prefixes(sections_path)
    failures = 0
    checked = 0

    for path in sorted(rules_dir.glob("*.md")):
        if path.name.startswith("_"):
            continue
        checked += 1
        result = validate_rule(path, valid_prefixes)
        if result.issues:
            failures += 1
            print(f"FAIL {result.filename}", file=sys.stderr)
            for issue in result.issues:
                print(f"  - {issue}", file=sys.stderr)

    print(f"validated {checked} rules; {failures} failures", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
