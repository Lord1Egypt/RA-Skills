"""Dependency-free parsing for the small YAML subset used by SKILL.md."""

import re


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def parse_frontmatter(raw: str):
    """Return ``(fields, raw_frontmatter, body)`` without requiring PyYAML."""
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return {}, "", raw
    frontmatter_raw = match.group(1)
    body = raw[match.end():]
    fields = {}
    key = None
    for line in frontmatter_raw.splitlines():
        if re.match(r"^\s+", line) and key:
            fields[key] += " " + line.strip()
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            fields[key] = value.strip().strip("'\"")
    return fields, frontmatter_raw, body
