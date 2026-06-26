#!/usr/bin/env python3
"""Assert version consistency across the skill.

Single source of truth: ``SKILL.md`` ``metadata.version``. Every other
declared version must match it (sub-skill ``SKILL.md`` ``metadata.version``,
``SOURCES.json`` ``skill_version``, ``README.md`` version badge,
``CHANGELOG.md`` latest top-level entry, ``AGENTS.md`` skill-version table
row + ``onboard.py --agent`` example JSON ``version`` field).

Exits 0 if everything matches, 1 otherwise. Designed to run in CI so
the v1.4.0 / v1.4.1 / v1.4.2 / v1.4.3 cycle of "version drift across
entry-point files" is caught mechanically rather than discovered by an
adversarial reviewer pass.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

VERSION_RE = re.compile(r'(?m)^  version:\s*"([^"]+)"\s*$')
BADGE_RE = re.compile(r'badge/version-([0-9][^-\]]*)-blue')
CHANGELOG_RE = re.compile(r'(?m)^## \[([^\]]+)\] - ')
AGENTS_TABLE_RE = re.compile(r"\|\s*Skill version\s*\|\s*([^|\s]+)\s*\|")
AGENTS_JSON_VERSION_RE = re.compile(r'"version":\s*"([^"]+)"')


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def read(p: Path) -> str:
    if not p.exists():
        return ""
    return p.read_text()


def main() -> int:
    errors: list[str] = []

    skill_md = read(REPO / "SKILL.md")
    m = VERSION_RE.search(skill_md)
    if not m:
        print("ERROR: SKILL.md is missing metadata.version", file=sys.stderr)
        return 1
    expected = m.group(1)
    print(f"Source-of-truth version: SKILL.md metadata.version = {expected}")

    for sub in sorted((REPO / "skills").glob("*/SKILL.md")):
        text = read(sub)
        sm = VERSION_RE.search(text)
        if not sm:
            fail(f"{sub.relative_to(REPO)}: missing metadata.version", errors)
        elif sm.group(1) != expected:
            fail(
                f"{sub.relative_to(REPO)}: version {sm.group(1)} != {expected}",
                errors,
            )
        else:
            print(f"  OK: {sub.relative_to(REPO)} = {sm.group(1)}")

    sources = read(REPO / "SOURCES.json")
    if sources:
        try:
            data = json.loads(sources)
            sv = data.get("skill_version")
            if sv != expected:
                fail(f"SOURCES.json: skill_version {sv} != {expected}", errors)
            else:
                print(f"  OK: SOURCES.json skill_version = {sv}")
        except json.JSONDecodeError as exc:
            fail(f"SOURCES.json: invalid JSON ({exc})", errors)
    else:
        fail("SOURCES.json: file missing", errors)

    readme = read(REPO / "README.md")
    if readme:
        bm = BADGE_RE.search(readme)
        if not bm:
            fail("README.md: version badge not found", errors)
        elif bm.group(1) != expected:
            fail(f"README.md: version badge {bm.group(1)} != {expected}", errors)
        else:
            print(f"  OK: README.md badge = {bm.group(1)}")

    changelog = read(REPO / "CHANGELOG.md")
    if changelog:
        cm = CHANGELOG_RE.search(changelog)
        if not cm:
            fail("CHANGELOG.md: no '## [X.Y.Z] - DATE' entry found", errors)
        elif cm.group(1) != expected:
            fail(
                f"CHANGELOG.md: latest entry [{cm.group(1)}] != {expected}",
                errors,
            )
        else:
            print(f"  OK: CHANGELOG.md latest entry = {cm.group(1)}")

    agents = read(REPO / "AGENTS.md")
    if agents:
        atm = AGENTS_TABLE_RE.search(agents)
        if not atm:
            fail("AGENTS.md: 'Skill version' table row not found", errors)
        elif atm.group(1) != expected:
            fail(
                f"AGENTS.md: skill-version table row {atm.group(1)} != {expected}",
                errors,
            )
        else:
            print(f"  OK: AGENTS.md skill-version row = {atm.group(1)}")

        for jm in AGENTS_JSON_VERSION_RE.finditer(agents):
            v = jm.group(1)
            # Only flag if it looks like a skill version (matches X.Y.Z) and
            # disagrees -- AGENTS.md may legitimately reference upstream
            # SDK / repo versions in JSON examples that should NOT match.
            if re.fullmatch(r"\d+\.\d+\.\d+", v) and v != expected:
                # Heuristic: flag if the surrounding 200 chars mention skill /
                # surreal-skills / onboard.py --agent
                start = max(0, jm.start() - 200)
                end = min(len(agents), jm.end() + 200)
                context = agents[start:end].lower()
                if any(
                    s in context
                    for s in ("onboard.py", "skill", "surreal-skills")
                ):
                    fail(
                        f"AGENTS.md: JSON \"version\":\"{v}\" near skill-context"
                        f" should be {expected}",
                        errors,
                    )

    if errors:
        print("\nERRORS:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("\nAll declared versions match.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
