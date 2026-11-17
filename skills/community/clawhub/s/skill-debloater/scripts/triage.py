#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
triage.py — objective signal collection for the ALIVE axis of four-axis debloating (skill-debloater Step 2).

Only "collects signals + buckets + suggests" — never deletes any file.
The final deletion decision is handed to the user by the agent via clarify (Step 3).

Usage:
    python3 triage.py "<path to skill directory>" [--json]

Output: keep bucket / review bucket (each item with signals evidence + a suggestion).
Standard library only, no third-party dependencies.
"""
import sys
import re
import json
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SUBDIRS = ("references", "scripts", "assets", "templates")
PLACEHOLDER_PAT = re.compile(
    r"\(omitted|see ?git ?history|elided|same as ?v\d|TODO|TBD|placeholder",
    re.I)
VER_IN_NAME = re.compile(r"v(\d+)\.(\d+)(?:\.(\d+))?", re.I)
VER_ANY = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")


def parse_ver(s):
    m = VER_ANY.search(s or "")
    if not m:
        return None
    return tuple(int(x) if x else 0 for x in m.groups())


def read_frontmatter_version(skill_md: Path):
    if not skill_md.is_file():
        return None
    txt = skill_md.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"^version:\s*(.+)$", txt, re.M)
    return parse_ver(m.group(1)) if m else None


def collect_references(skill_md: Path):
    """Extract all references/scripts/templates/assets paths referenced in SKILL.md's body."""
    txt = skill_md.read_text(encoding="utf-8", errors="ignore")
    refs = set()
    for m in re.finditer(r"(?:references|scripts|templates|assets)/[\w./-]+", txt):
        refs.add(m.group(0).rstrip(".,);:`"))
    return refs


def count_placeholders(p: Path):
    if p.suffix.lower() != ".md":
        return 0
    try:
        lines = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return 0
    return sum(1 for ln in lines if PLACEHOLDER_PAT.search(ln))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if not args:
        print("Usage: python3 triage.py \"<skill directory>\" [--json]")
        sys.exit(1)

    skill_dir = Path(args[0])
    if skill_dir.is_file():
        skill_dir = skill_dir.parent
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        print(f"SKILL.md not found: {skill_md}")
        sys.exit(1)

    cur = read_frontmatter_version(skill_md)
    refs = collect_references(skill_md)

    # Version mismatch: _meta.json vs SKILL.md
    mismatch = None
    meta = skill_dir / "_meta.json"
    if meta.is_file():
        try:
            mv = parse_ver(json.loads(meta.read_text(encoding="utf-8", errors="ignore")).get("version", ""))
            if cur and mv and cur != mv:
                mismatch = {"skill_md": ".".join(map(str, cur)), "meta_json": ".".join(map(str, mv))}
        except Exception:
            pass

    keep, review = [], []
    for sub in SUBDIRS:
        d = skill_dir / sub
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if not p.is_file():
                continue
            rel = f"{sub}/{p.relative_to(d).as_posix()}"
            signals, suggestion = [], None

            referenced = any(rel == r or rel in r or r in rel for r in refs)
            if not referenced:
                signals.append("orphan: not referenced by SKILL.md")

            fv = VER_IN_NAME.search(p.name)
            if fv and cur:
                fver = tuple(int(x) if x else 0 for x in fv.groups())
                if fver < cur:
                    signals.append(f"old-version-tag: v{'.'.join(map(str, fver))} < current {'.'.join(map(str, cur))}")

            ph = count_placeholders(p)
            if ph >= 3:
                signals.append(f"empty-shell: {ph} placeholder lines (omitted/see git etc.)")

            if not signals:
                keep.append({"path": rel, "why": "referenced + current"})
                continue

            # Suggestion rules
            is_orphan = any(s.startswith("orphan") for s in signals)
            is_old = any(s.startswith("old-version-tag") for s in signals)
            is_shell = any(s.startswith("empty-shell") for s in signals)
            if is_orphan and (is_old or is_shell):
                suggestion = "deletable"
            elif is_orphan:
                suggestion = "deletable (unreferenced)"
            elif is_old:
                suggestion = "your call — referenced but an old version, update the body's reference if deleted"
            elif is_shell:
                suggestion = "deletable (content is an empty shell, full content is in git)"
            review.append({"path": rel, "signals": signals, "suggestion": suggestion})

    result = {
        "skill": skill_dir.name,
        "current_version": ".".join(map(str, cur)) if cur else None,
        "version_mismatch": mismatch,
        "buckets": {"keep": keep, "review": review},
    }

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"\n=== Four-axis bucketing: {skill_dir.name}  (current version {result['current_version']}) ===\n")
    if mismatch:
        print(f"[!] Version mismatch: SKILL.md={mismatch['skill_md']} but _meta.json={mismatch['meta_json']}\n")
    print(f"[OK keep] {len(keep)} file(s): referenced and current version, kept automatically\n")
    print(f"[? review] {len(review)} file(s): suspected deletable, need clarify with the user\n")
    for i, r in enumerate(review, 1):
        print(f"  {i}) {r['path']}")
        for s in r["signals"]:
            print(f"       · {s}")
        print(f"       -> suggestion: {r['suggestion']}\n")
    print("Note: this script never deletes any file; use clarify to hand the review items above to the user (default: keep all).\n")


if __name__ == "__main__":
    main()
