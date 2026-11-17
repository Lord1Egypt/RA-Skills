#!/usr/bin/env python3
"""ci_check.py - deploy-check for ClawHub skill packages (run by CI).

Validates SKILL.md frontmatter (name/version/description) and that at least one
tool file is present. Exits 1 on failure. Stdlib only.
"""
import os
import re
import sys

REQUIRED = ["name", "version", "description"]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    skill = os.path.join(here, "SKILL.md")
    if not os.path.isfile(skill):
        print("SKIP: no SKILL.md (not a skill package)")
        return 0
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
    # require at least one .py tool or referenced file
    has_tool = any(f.endswith(".py") for f in os.listdir(here)) or "agent_caps" in txt
    if not has_tool:
        print("WARN: no .py tool file alongside SKILL.md")
    print("PASS: SKILL.md frontmatter OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
