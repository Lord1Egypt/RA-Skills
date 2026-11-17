#!/usr/bin/env python3
"""skill-preflight: deterministically validate a SKILL.md before publishing.

Runs real checks (stdlib only — no pip deps) and emits an HONEST outcome:
ok:true means the file passed EVERY check below, nothing more.

Checks:
  1. frontmatter block exists (--- ... ---)
  2. required keys present + non-empty: name, description, version
  3. version is semver-ish (N.N.N)
  4. metadata.openclaw.requires.bins is declared (list, may be empty)
  5. every declared bin actually resolves on PATH (real execution gate)

Usage: python3 preflight.py <path-to-SKILL.md | skill-folder>
Exit code 0 = ok, 1 = failed, 2 = usage/IO error.
"""
import json
import os
import re
import shutil
import sys


def load_frontmatter(text):
    """Return the raw frontmatter block, or None if absent."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    return m.group(1) if m else None


def scalar(block, key):
    """Grab a top-level `key: value` scalar from the frontmatter block."""
    m = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", block, re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip().strip("'\"") or None


def declared_bins(block):
    """Parse requires.bins whether written inline [a, b] or as a block list.

    Returns (declared: bool, bins: list[str]).
    """
    # inline form:  bins: [python3, jq]   (also bins: [])
    m = re.search(r"bins:\s*\[(.*?)\]", block, re.DOTALL)
    if m:
        inner = m.group(1)
        inner = re.sub(r"#.*", "", inner)  # strip trailing comments
        bins = [b.strip().strip("'\"") for b in inner.split(",")]
        return True, [b for b in bins if b]
    # block form:
    #   bins:
    #     - python3
    m = re.search(r"bins:\s*\n((?:\s*-\s*.+\n?)+)", block)
    if m:
        bins = re.findall(r"-\s*(.+?)\s*$", m.group(1), re.MULTILINE)
        return True, [b.strip().strip("'\"") for b in bins if b.strip()]
    return False, []


def main(argv):
    if len(argv) != 2:
        print(json.dumps({"ok": False, "reason": "usage: preflight.py <SKILL.md|folder>"}))
        return 2

    path = argv[1]
    if os.path.isdir(path):
        path = os.path.join(path, "SKILL.md")
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        print(json.dumps({"ok": False, "reason": f"cannot read {path}: {exc}"}))
        return 2

    checks = []

    block = load_frontmatter(text)
    checks.append({"name": "frontmatter-present", "ok": block is not None,
                   "detail": "found --- … --- block" if block else "no YAML frontmatter"})
    if block is None:
        print(json.dumps({"ok": False, "reason": "missing frontmatter", "checks": checks}, ensure_ascii=False))
        return 1

    for key in ("name", "description", "version"):
        val = scalar(block, key)
        checks.append({"name": f"has-{key}", "ok": bool(val),
                       "detail": val or "MISSING/empty"})

    version = scalar(block, "version")
    semver_ok = bool(version and re.fullmatch(r"\d+\.\d+\.\d+", version))
    checks.append({"name": "version-semver", "ok": semver_ok,
                   "detail": version or "no version"})

    declared, bins = declared_bins(block)
    checks.append({"name": "requires.bins-declared", "ok": declared,
                   "detail": (f"declares {bins}" if declared else
                              "requires.bins not declared")})

    for b in bins:
        resolved = shutil.which(b)
        checks.append({"name": f"bin:{b}", "ok": resolved is not None,
                       "detail": resolved or f"'{b}' not on PATH"})

    ok = all(c["ok"] for c in checks)
    reason = "all checks passed" if ok else \
        "failed: " + ", ".join(c["name"] for c in checks if not c["ok"])
    print(json.dumps({"ok": ok, "reason": reason, "checks": checks}, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
