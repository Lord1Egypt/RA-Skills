#!/usr/bin/env python3
"""List obsolete HTML elements in source files as review warnings.

Usage:
  python3 scripts/check-legacy-markup.py <html-file-or-directory> [...]

Directory inputs are scanned recursively for .html, .htm, and .xhtml files.
This static inventory does not determine WCAG conformance or inspect rendered
and script-generated content.
"""

import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "resources/legacy_tags.json"
HTML_SUFFIXES = {".htm", ".html", ".xhtml"}


class LegacyElementParser(HTMLParser):
    def __init__(self, path, obsolete):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.obsolete = obsolete
        self.findings = []

    def handle_starttag(self, tag, attrs):
        if tag in self.obsolete:
            line, _ = self.getpos()
            self.findings.append((self.path, line, tag))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def input_files(paths):
    files = []
    for path in paths:
        if path.is_dir():
            files.extend(
                item for item in path.rglob("*")
                if item.is_file() and item.suffix.lower() in HTML_SUFFIXES
            )
        elif path.is_file():
            files.append(path)
        else:
            raise FileNotFoundError(f"Input does not exist: {path}")
    return sorted(set(files))


def scan(files, obsolete):
    findings = []
    for path in files:
        try:
            html = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise OSError(f"Cannot read {path}: {error}") from error
        parser = LegacyElementParser(path, obsolete)
        parser.feed(html)
        findings.extend(parser.findings)
    return findings


def main(argv):
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2
    try:
        files = input_files([Path(value) for value in argv])
        obsolete = set(json.loads(RULES.read_text(encoding="utf-8"))["tags"])
        findings = scan(files, obsolete)
    except (OSError, json.JSONDecodeError, KeyError) as error:
        print(f"Legacy markup check failed: {error}", file=sys.stderr)
        return 2

    print("LEGACY HTML ELEMENTS")
    if not findings:
        print("No obsolete elements found.")
    else:
        for path, line, tag in findings:
            print(f"{path}:{line}: <{tag}>")
        counts = Counter(tag for _, _, tag in findings)
        for tag, count in sorted(counts.items()):
            print(f"{tag}: {count} occurrence(s)")
    kinds = len({tag for _, _, tag in findings})
    print(f"Total: {len(findings)} occurrence(s) across {kinds} element type(s)")
    print("Findings are review warnings, not automatic WCAG failures.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
