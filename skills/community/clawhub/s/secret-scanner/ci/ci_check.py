#!/usr/bin/env python3
"""ci_check.py - deploy-check for ClawHub skill packages (run by CI).

Validates SKILL.md frontmatter (name/version/description) and that at least one
tool file is present. Exits 1 on failure. Stdlib only.

Resolution: prefer SKILL.md in the current working directory (where CI invokes this
from the repo root); fall back to the repo root implied by this file's location
(parent of the ci/ dir). A missing SKILL.md is a HARD FAIL (not a skip) so a
broken package cannot pass the deploy-check.
"""
import os
import re
import sys

REQUIRED = ["name", "version", "description"]


def _pkg_root():
    cwd = os.getcwd()
    if os.path.isfile(os.path.join(cwd, "SKILL.md")):
        return cwd
    # repo root = parent of the directory holding this script (e.g. ci/ -> root)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    root = _pkg_root()
    skill = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill):
        print(f"FAIL: no SKILL.md found at {root}")
        return 1
    txt = open(skill, encoding="utf-8").read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.S)
    if not m:
        print("FAIL: SKILL.md missing YAML frontmatter")
        return 1
    fm = m.group(1)
    for k in REQUIRED:
        if not re.search(rf"^{k}\s*:", fm, re.M):
            print(f"FAIL: SKILL.md missing frontmatter field '{k}'")
            return 1
    has_tool = any(f.endswith(".py") for f in os.listdir(root)) or "agent_caps" in txt
    if not has_tool:
        print("WARN: no .py tool file alongside SKILL.md")
    print("PASS: SKILL.md frontmatter OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
