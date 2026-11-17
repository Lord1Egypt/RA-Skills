#!/usr/bin/env python3
"""Structural validator for generated (and generator) skill directories.

Usage:
    python3 scripts/validate_skill.py <skill_dir>
Exit code 0 = valid, 1 = problems found (printed one per line).
"""
import os
import re
import sys

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_LINK_RE = re.compile(r"\]\((references/[^)\s]+\.md)\)")


def validate_skill_dir(path):
    problems = []
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        problems.append("SKILL.md is missing at %s" % path)
        return problems

    with open(skill_md, "r", encoding="utf-8") as f:
        text = f.read()

    m = _FRONTMATTER_RE.match(text)
    if not m:
        problems.append("SKILL.md missing YAML frontmatter (name/description)")
    else:
        block = m.group(1)
        if not re.search(r"^name:\s*\S+", block, re.MULTILINE):
            problems.append("SKILL.md frontmatter missing 'name'")
        if not re.search(r"^description:\s*\S+", block, re.MULTILINE):
            problems.append("SKILL.md frontmatter missing 'description'")

    for rel in _LINK_RE.findall(text):
        if not os.path.isfile(os.path.join(path, rel)):
            problems.append("SKILL.md links missing file: %s" % rel)

    required_scripts = [
        "content_db.py", "archive_content.py", "query_db.py",
        "update_metrics.py", "generate_cover.py", "fetch_hotlist.py",
        "web_search.py",
    ]
    scripts_dir = os.path.join(path, "scripts")
    for name in required_scripts:
        if not os.path.isfile(os.path.join(scripts_dir, name)):
            problems.append("missing required script: scripts/%s" % name)

    return problems


def main(argv):
    if len(argv) != 2:
        print("usage: validate_skill.py <skill_dir>", file=sys.stderr)
        return 2
    problems = validate_skill_dir(argv[1])
    for p in problems:
        print(p)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
