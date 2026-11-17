#!/usr/bin/env python3
"""Self-check for this skill. Run after editing any file in the skill; fix every failure before committing.

    python3 scripts/check_skill.py

Checks:
  1. SKILL.md has name and description (description <= 1024 characters, name matches the folder) and stays under
     500 lines, so the entry file remains a map and the detail lives in references/.
  2. Every file in references/ and assets/templates/ is named in SKILL.md (an unlisted file is never read).
  3. Every relative path written in backticks (references/..., assets/..., scripts/...) exists.
  4. The bundled agents exist next to the skill (plugin layout) and disable the Agent tool.
  5. JSON templates parse; no CJK characters in the English method files.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
PLUGIN = SKILL.parents[1]
ROSTER = ["research-collector", "research-bull", "research-bear", "research-auditor", "research-translator"]
CJK = re.compile(r"[㐀-鿿]")


def main() -> int:
    fail = []
    entry = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", entry, re.S)
    if not m:
        fail.append("SKILL.md has no frontmatter")
    else:
        fm = m.group(1)
        name = re.search(r"^name:\s*(\S+)", fm, re.M)
        desc = re.search(r"^description:\s*(.+)$", fm, re.M)
        if not name or name.group(1) != SKILL.name:
            fail.append(f"frontmatter name must equal the folder name {SKILL.name}")
        if not desc or len(desc.group(1)) > 1024:
            fail.append("description missing or longer than 1024 characters")
    if len(entry.splitlines()) > 500:
        fail.append("SKILL.md exceeds 500 lines")

    for p in sorted((SKILL / "references").rglob("*.md")) + sorted((SKILL / "assets" / "templates").glob("*")):
        if p.name not in entry:
            fail.append(f"SKILL.md does not mention {p.relative_to(SKILL)}")

    pat = re.compile(r"`((?:references|assets|scripts)/[A-Za-z0-9_./-]+\.(?:md|py|json))`")
    for f in sorted(SKILL.rglob("*.md")):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for tok in pat.findall(line):
                if not (SKILL / tok).exists():
                    fail.append(f"{f.relative_to(SKILL)}:{i} missing path {tok}")
            if CJK.search(line) and f.name != "SKILL.md":
                fail.append(f"{f.relative_to(SKILL)}:{i} contains CJK characters")

    for a in ROSTER:
        p = PLUGIN / "agents" / f"{a}.md"
        if not p.exists():
            fail.append(f"agent missing: agents/{a}.md")
            continue
        fm = p.read_text(encoding="utf-8").split("---")[1]
        dis = re.search(r"^disallowedTools:\s*(.+)$", fm, re.M)
        if not dis or "Agent" not in [t.strip() for t in dis.group(1).split(",")]:
            fail.append(f"agents/{a}.md must list Agent in disallowedTools")

    for p in (SKILL / "assets" / "templates").glob("*.json"):
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail.append(f"{p.name}: invalid JSON ({e})")

    for f in fail:
        print("  x", f)
    print(f"skill self-check: {'FAILED ' + str(len(fail)) if fail else 'all passed'}")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
