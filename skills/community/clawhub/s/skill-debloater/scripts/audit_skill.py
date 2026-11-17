#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_skill.py — objective health check for an Agent Skill (skill-debloater Step 1).

Usage:
    python3 audit_skill.py "<path to SKILL.md file or skill directory>"

Output: frontmatter compliance / body token estimate + line count / layer-3 file listing.
Standard library only, no third-party dependencies.
"""
import sys
import re
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

BODY_TOKEN_LIMIT = 5000
BODY_LINE_LIMIT = 500
NAME_MAX = 64
DESC_MAX = 1024
ALLOWED_TOP_KEYS = {"name", "description", "license", "compatibility",
                    "metadata", "allowed-tools"}


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~1 token per CJK character, ~1 token per 4 other characters. Only used to check against the threshold."""
    cjk = len(re.findall(r"[一-鿿　-〿＀-￯]", text))
    return cjk + round((len(text) - cjk) / 4)


def split_frontmatter(md: str):
    if not md.startswith("---"):
        return None, md
    end = md.find("\n---", 3)
    if end == -1:
        return None, md
    raw = md[3:end].strip("\n")
    body = md[end + 4:].lstrip("\n")
    fm = {}
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s?(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2)
    return fm, body


def check(label, ok, detail=""):
    print(f"  [{'OK' if ok else '!!'}] {label}" + (f" — {detail}" if detail else ""))
    return ok


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 audit_skill.py \"<SKILL.md file or skill directory>\"")
        sys.exit(1)

    target = Path(sys.argv[1])
    skill_md = target / "SKILL.md" if target.is_dir() else target
    skill_dir = skill_md.parent

    if not skill_md.is_file():
        print(f"SKILL.md not found: {skill_md}")
        sys.exit(1)

    md = skill_md.read_text(encoding="utf-8", errors="ignore")
    fm, body = split_frontmatter(md)

    print(f"\n=== Skill health check: {skill_dir.name} ===\n")

    print("[Frontmatter]")
    if fm is None:
        check("YAML frontmatter present", False, "no --- delimiters found")
    else:
        name = fm.get("name", "")
        desc = fm.get("description", "")
        check(f"name ({len(name)}/{NAME_MAX})", 0 < len(name) <= NAME_MAX)
        check("name characters valid (lowercase/digits/hyphens)",
              bool(re.fullmatch(r"[a-z0-9-]+", name)) if name else False, name)
        check("name matches folder name", name == skill_dir.name,
              f"name={name!r} folder={skill_dir.name!r}")
        check(f"description ({len(desc)}/{DESC_MAX})", 0 < len(desc) <= DESC_MAX)
        check("description contains no < or >", "<" not in desc and ">" not in desc)
        bad = set(fm) - ALLOWED_TOP_KEYS
        check("no invalid top-level keys", not bad,
              f"invalid: {sorted(bad)} (version/author should go in metadata)" if bad else "")

    print("\n[Body]")
    tok = estimate_tokens(body)
    lines = body.count("\n") + 1
    check(f"estimated tokens {tok} (threshold {BODY_TOKEN_LIMIT})", tok <= BODY_TOKEN_LIMIT,
          "bloated, consider pushing down background/examples" if tok > BODY_TOKEN_LIMIT else "")
    check(f"line count {lines} (threshold {BODY_LINE_LIMIT})", lines <= BODY_LINE_LIMIT)

    print("\n[Layer-3 files]")
    found = False
    for sub in ("references", "scripts", "assets", "templates"):
        d = skill_dir / sub
        if d.is_dir():
            for p in sorted(d.rglob("*")):
                if p.is_file():
                    print(f"  {sub}/{p.relative_to(d)}  ({p.stat().st_size/1024:.1f} KB)")
                    found = True
    if not found:
        print("  (none)")

    print("\nNote: token count is a rough estimate; verify with real tasks (three-way verification) after debloating.\n")


if __name__ == "__main__":
    main()
