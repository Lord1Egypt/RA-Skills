#!/usr/bin/env python3
"""
validate_package.py — Pre-publish fact-check for tristan-rfq-overseer.

This is NOT a one-time fix. Run it before every publish, and every time any
file in this package changes. It exits non-zero on any failure so it can
gate a `clawhub skill publish` step, or be dropped into CI.

Checks performed:
    1. Every .py file compiles (catches Python syntax errors).
    2. Every .py file is scanned for regex patterns that are valid in Python
       but INVALID or unsupported in JavaScript — since ClawHub's upload
       pipeline appears to parse/scan files with a JS-based tool. This is
       what caused the "invalid group specifier name" error: Python's
       (?P<name>...) named-group syntax is not valid JS regex syntax.
    3. Every markdown file with YAML frontmatter (--- ... ---) is checked
       for valid YAML.
    4. Every file referenced by path in SKILL.md / README.md ("assets/...",
       "scripts/...", "references/...") is checked to actually exist on
       disk, and vice versa — every file on disk is checked for at least
       one reference, so nothing is silently orphaned or silently missing.
    5. The package directory is scanned for build artifacts that should
       never ship (__pycache__, .pyc, .DS_Store, .git).

Usage:
    python validate_package.py <path/to/tristan-rfq-overseer>

Exit code 0 = clean. Exit code 1 = at least one failure, do not publish.
"""

import ast
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

# Regex constructs that are valid in Python's `re` module but break or
# behave differently under JavaScript's RegExp engine. Each entry is
# (compiled pattern to detect the construct, human-readable explanation).
JS_UNSAFE_REGEX_CONSTRUCTS = [
    (re.compile(r"\(\?P<"), "Python named group (?P<name>...) — invalid in JS, causes "
                             "'invalid group specifier name'. Use (?<name>...) if the "
                             "pattern must run in JS, or drop the name and use groups() "
                             "by position if it only needs to run in Python."),
    (re.compile(r"\(\?P="), "Python named backreference (?P=name) — invalid in JS."),
    (re.compile(r"\\Z"), r"Python-only \Z end-of-string anchor — not recognized by JS. Use $ instead."),
    (re.compile(r"\\A"), r"Python-only \A start-of-string anchor — not recognized by JS. Use ^ instead."),
]

BUILD_ARTIFACT_PATTERNS = ["__pycache__", ".pyc", ".DS_Store", ".git"]

REFERENCEABLE_DIRS = ("assets/", "scripts/", "references/")


def check_python_syntax(pkg_root: Path) -> list:
    errors = []
    for py_file in pkg_root.rglob("*.py"):
        try:
            ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except SyntaxError as e:
            errors.append(f"[SYNTAX] {py_file.relative_to(pkg_root)}: {e}")
    return errors


def check_js_unsafe_regex(pkg_root: Path) -> list:
    errors = []
    for py_file in pkg_root.rglob("*.py"):
        if py_file.name == "validate_package.py":
            continue  # this file documents the unsafe patterns as strings; it doesn't use them
        text = py_file.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            for pattern, explanation in JS_UNSAFE_REGEX_CONSTRUCTS:
                if pattern.search(line):
                    errors.append(
                        f"[JS-UNSAFE-REGEX] {py_file.relative_to(pkg_root)}:{lineno}: "
                        f"{line.strip()!r} — {explanation}"
                    )
    return errors


def check_yaml_frontmatter(pkg_root: Path) -> list:
    errors = []
    if yaml is None:
        errors.append("[YAML] PyYAML not installed — cannot validate frontmatter. "
                       "Install with: pip install pyyaml --break-system-packages")
        return errors
    for md_file in pkg_root.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            errors.append(f"[YAML] {md_file.relative_to(pkg_root)}: starts with '---' but frontmatter block is not closed.")
            continue
        frontmatter_text = parts[1]
        try:
            yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            errors.append(f"[YAML] {md_file.relative_to(pkg_root)}: invalid frontmatter — {e}")
    return errors


def check_cross_references(pkg_root: Path) -> list:
    errors = []
    doc_files = [pkg_root / "SKILL.md", pkg_root / "README.md"]
    referenced_paths = set()
    ref_pattern = re.compile(r"(?:assets|scripts|references)/[A-Za-z0-9_.\-]+\.[A-Za-z0-9]+")

    for doc in doc_files:
        if not doc.exists():
            errors.append(f"[MISSING-DOC] {doc.name} not found at package root.")
            continue
        text = doc.read_text(encoding="utf-8")
        for match in ref_pattern.findall(text):
            referenced_paths.add(match)

    # Every referenced path should exist on disk.
    for ref in sorted(referenced_paths):
        if not (pkg_root / ref).exists():
            errors.append(f"[BROKEN-REF] {ref} is referenced in SKILL.md/README.md but does not exist on disk.")

    # Every real file under the referenceable dirs should be mentioned somewhere.
    on_disk = set()
    for sub in REFERENCEABLE_DIRS:
        for f in (pkg_root / sub).glob("*"):
            if f.is_file():
                on_disk.add(f"{sub}{f.name}")

    orphaned = on_disk - referenced_paths
    for orphan in sorted(orphaned):
        errors.append(f"[ORPHANED-FILE] {orphan} exists on disk but is not referenced in SKILL.md or README.md.")

    return errors


def check_build_artifacts(pkg_root: Path) -> list:
    errors = []
    for pattern in BUILD_ARTIFACT_PATTERNS:
        for hit in pkg_root.rglob(f"*{pattern}*"):
            errors.append(f"[BUILD-ARTIFACT] {hit.relative_to(pkg_root)} should not be part of the published package.")
    return errors


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_package.py <path/to/tristan-rfq-overseer>", file=sys.stderr)
        sys.exit(2)

    pkg_root = Path(sys.argv[1]).resolve()
    if not pkg_root.exists():
        print(f"Error: {pkg_root} does not exist.", file=sys.stderr)
        sys.exit(2)

    checks = [
        ("Python syntax", check_python_syntax),
        ("JS-unsafe regex constructs", check_js_unsafe_regex),
        ("YAML frontmatter", check_yaml_frontmatter),
        ("Cross-referenced files", check_cross_references),
        ("Build artifacts", check_build_artifacts),
    ]

    all_errors = []
    print(f"Validating package at {pkg_root}\n")
    for name, fn in checks:
        errs = fn(pkg_root)
        status = "PASS" if not errs else f"FAIL ({len(errs)})"
        print(f"  [{status}] {name}")
        all_errors.extend(errs)

    if all_errors:
        print("\n--- Failures ---")
        for e in all_errors:
            print(e)
        print(f"\n{len(all_errors)} issue(s) found. Do not publish until these are resolved.")
        sys.exit(1)

    print("\nAll checks passed. Package is safe to publish.")
    sys.exit(0)


if __name__ == "__main__":
    main()
