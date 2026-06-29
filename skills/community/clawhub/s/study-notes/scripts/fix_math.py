#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""fix_math.py — the repair counterpart to build_and_check.py.

Rewrites the naked-Unicode-in-math silent failures that build_and_check flags
(° · − × ≈ ± …) into correct KaTeX, touching ONLY the inside of math spans
($...$ / $$...$$) — prose, SVG <text>, and navigation are left alone.

The subtlety is `\text{}`: a dangerous char inside a unit text like
`\text{J/(mol·K)}` must BREAK OUT of the text group, because `\cdot` typed
literally inside `\text{}` does not render. So inside `\text{...}` a char D
becomes `}<latex>\text{` (e.g. `\text{J/(mol·K)}` → `\text{J/(mol}\cdot\text{K)}`),
while outside any `\text{}` it becomes just `<latex>` (e.g. `27°` → `27{}^\circ`).

Usage:
  python scripts/fix_math.py <file.html> [...]        # fix in place (writes .bak once)
  python scripts/fix_math.py --dry-run <file.html>    # report counts only
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import build_and_check as b  # noqa: E402  (reuse DANGEROUS map + MATH_RE)

TEXT_RE = re.compile(r"\\text\{([^{}]*)\}")


def fix_span(span):
    n = 0

    def fix_text(m):
        nonlocal n
        inner = m.group(1)
        for ch, latex in b.DANGEROUS.items():
            if ch in inner:
                n += inner.count(ch)
                inner = inner.replace(ch, "}" + latex + r"\text{")
        return r"\text{" + inner + "}"

    span = TEXT_RE.sub(fix_text, span)            # inside \text{}: break out
    for ch, latex in b.DANGEROUS.items():         # outside \text{}: straight swap
        if ch in span:
            n += span.count(ch)
            span = span.replace(ch, latex)
    span = span.replace(r"\text{}", "")            # drop empty groups from edge breaks
    return span, n


def fix_html(html):
    total = 0

    def repl(m):
        nonlocal total
        fixed, n = fix_span(m.group())
        total += n
        return fixed

    return b.MATH_RE.sub(repl, html), total


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    dry = "--dry-run" in sys.argv
    if not args:
        sys.exit("usage: fix_math.py [--dry-run] <file.html> [...]")
    for path in args:
        html = open(path, encoding="utf-8", errors="replace").read()
        fixed, n = fix_html(html)
        tag = "would fix" if dry else "fixed"
        print(f"{tag} {n:3d} naked-Unicode-in-math in {os.path.basename(path)}")
        if n and not dry:
            bak = path + ".bak"
            if not os.path.exists(bak):
                with open(bak, "w", encoding="utf-8") as f:
                    f.write(html)
            with open(path, "w", encoding="utf-8") as f:
                f.write(fixed)


if __name__ == "__main__":
    main()
