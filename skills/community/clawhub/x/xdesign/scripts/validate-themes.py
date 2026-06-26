#!/usr/bin/env python3
"""
validate-themes.py
==================

Validate that all HTML templates in deck-studio reference only the themes
that are physically present in assets/themes/.

Why this exists:
- deck-studio was originally bundled with 36 themes, but only 18 were cloned
  into this repo (network issues during initial setup).
- Some templates still reference removed themes (e.g. `minimal-white`,
  `tokyo-night`). Browsers will silently fall back to default white, which
  produces ugly output the user doesn't notice until they look at the page.
- This script catches those broken references before they ship.

Usage:
    python scripts/validate-themes.py
    python scripts/validate-themes.py --strict   # exit 1 on any warning
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECK_STUDIO = ROOT / "deck-studio"
THEMES_DIR = DECK_STUDIO / "assets" / "themes"
TEMPLATES_DIR = DECK_STUDIO / "templates"

# Known good substitutes for themes that were in the original html-ppt-skill
# (36 themes) but were NOT cloned to this repo (only 18 are present).
# If we ever see a reference to a removed theme, we silently rewrite it
# upstream; this validator just confirms no leftovers slipped through.
REMOVED_THEMES = {
    "minimal-white", "tokyo-night", "terminal-green", "soft-pastel",
    "sharp-mono", "sunset-warm", "nord", "solarized-light", "rose-pine",
    "neo-brutalism", "swiss-grid", "xiaohongshu-white", "rainbow-gradient",
    "y2k-chrome", "retro-tv", "vaporwave", "news-broadcast", "pitch-deck-vc",
}


def list_available_themes() -> set[str]:
    if not THEMES_DIR.is_dir():
        print(f"[FATAL] themes dir missing: {THEMES_DIR}", file=sys.stderr)
        sys.exit(2)
    return {f.stem for f in THEMES_DIR.glob("*.css")}


def scan_templates(available: set[str]) -> list[tuple[Path, str, str]]:
    """Return list of (path, theme, kind) for every broken theme reference."""
    issues: list[tuple[Path, str, str]] = []
    theme_in_attr = re.compile(r'data-theme[s]?="([^"]+)"')
    theme_in_link = re.compile(r'themes/([\w-]+)\.css')
    theme_in_body = re.compile(r'<body[^>]*data-theme[s]?="([^"]+)"')

    for html in TEMPLATES_DIR.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        for m in theme_in_link.finditer(text):
            theme = m.group(1)
            if theme not in available:
                issues.append((html, theme, "css-link"))
        for m in theme_in_attr.finditer(text):
            for theme in m.group(1).split(","):
                theme = theme.strip()
                if theme and theme not in available:
                    issues.append((html, theme, "data-theme"))
        for m in theme_in_body.finditer(text):
            for theme in m.group(1).split(","):
                theme = theme.strip()
                if theme and theme not in available:
                    issues.append((html, theme, "body-attr"))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero if any removed-theme reference is found.")
    args = parser.parse_args()

    available = list_available_themes()
    print(f"[INFO] Available themes: {len(available)}")
    for t in sorted(available):
        print(f"       - {t}")
    print()

    issues = scan_templates(available)
    removed_hits = [(p, t, k) for p, t, k in issues if t in REMOVED_THEMES]
    unknown_hits = [(p, t, k) for p, t, k in issues if t not in REMOVED_THEMES]

    print("=" * 70)
    print(f"Removed-theme references (need remap): {len(removed_hits)}")
    print("=" * 70)
    for path, theme, kind in removed_hits:
        rel = path.relative_to(ROOT)
        print(f"  [{kind:11s}] {rel} -> {theme}")

    print()
    print("=" * 70)
    print(f"Unknown theme references (typos?): {len(unknown_hits)}")
    print("=" * 70)
    for path, theme, kind in unknown_hits:
        rel = path.relative_to(ROOT)
        print(f"  [{kind:11s}] {rel} -> {theme}")

    print()
    print("=" * 70)
    if not issues:
        print("[OK] All HTML template theme references are valid.")
        return 0
    if args.strict:
        print(f"[FAIL] {len(issues)} invalid theme reference(s) found.")
        return 1
    print(f"[WARN] {len(issues)} invalid theme reference(s) found "
          f"(re-run with --strict to fail the build).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
