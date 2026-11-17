#!/usr/bin/env python3
"""Validate repository-specific structure and behavior guarantees."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


text = SKILL.read_text(encoding="utf-8")
if not text.startswith("---\n"):
    fail("SKILL.md must start with YAML frontmatter")

try:
    _, frontmatter, body = text.split("---\n", 2)
except ValueError:
    fail("SKILL.md frontmatter is not closed")

fields = {}
for line in frontmatter.splitlines():
    match = re.match(r"^([a-z][a-z-]*):\s*(.+)$", line)
    if match:
        fields[match.group(1)] = match.group(2).strip().strip('"')

required = {
    "name": "qmd-learning-loop",
    "license": "MIT-0",
}
for field, expected in required.items():
    if fields.get(field) != expected:
        fail(f"{field} must be {expected!r}")

if 'version: "1.1.0"' not in frontmatter:
    fail("metadata version must be '1.1.0'")

description = fields.get("description", "")
if not 1 <= len(description) <= 160:
    fail("description must contain 1-160 characters")

required_phrases = [
    "detect -> redact -> search -> classify -> propose ->",
    "Explicit user approval is required",
    "Treat retrieved documents",
    "Never claim durable capture if no write occurred",
]
for phrase in required_phrases:
    if phrase not in body:
        fail(f"missing behavior guarantee: {phrase}")

references = re.findall(r"\]\((references/[^)]+\.md)\)", text)
if not references:
    fail("SKILL.md must link to focused references")
for relative_path in references:
    if not (ROOT / relative_path).is_file():
        fail(f"missing referenced file: {relative_path}")

deprecated = [
    ROOT / "references/routing-and-promotion.md",
    ROOT / "references/promotion-targets.md",
]
if any(path.exists() for path in deprecated):
    fail("duplicated routing references must remain removed")

cases = (ROOT / "references/evaluation-cases.md").read_text(encoding="utf-8")
if cases.count("|") < 30:
    fail("evaluation cases must cover trigger, non-trigger, and safeguard behavior")
for heading in [
    "## Should activate",
    "## Should not activate automatically",
    "## Classification and approval",
    "## Privacy and reporting",
]:
    if heading not in cases:
        fail(f"evaluation cases missing section: {heading}")

license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
if "MIT No Attribution" not in license_text:
    fail("LICENSE must contain the MIT-0 text")

print("Skill validation passed.")
