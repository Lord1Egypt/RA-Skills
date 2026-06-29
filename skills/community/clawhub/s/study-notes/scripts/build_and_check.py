#!/usr/bin/env python3
r"""build_and_check.py — concatenate study-notes part files and run static checks.

Subcommands:

  build  p1.html p2.html ... -o final.html   Concatenate parts, then check.
  check  final.html                          Run the static checks only.

Static checks (catch the SILENT failures KaTeX never reports):
  1. Dangerous Unicode inside $...$ / $$...$$  (·  °  −  ×  ≈  ±  etc.)
  2. \boxed{} occurrences                       (must be removed inside .fbox /
                                                 .big-formula / .callout / .answer-box)
  3. Forbidden KaTeX commands                   (\celsius \unit \SI \qty \cancel
                                                 \ket \bra \tensor ...)
  4. <div> balance                              (open vs close, +.page sanity)
  5. $ delimiter balance                        (stray unmatched $)

Exit code: 0 = clean, 1 = one or more FAIL-level problems.
\boxed is reported as a WARNING (allowed only in plain prose), and does not by
itself fail the build — but review every hit.

Pure standard library.
"""
import argparse
import re
import sys

# math span: $$...$$ (non-greedy, multiline) OR $...$ (single line-ish)
MATH_RE = re.compile(r'(\$\$[\s\S]*?\$\$|\$[^$\n]+?\$)')

# Unicode chars that must not appear inside math (use LaTeX commands instead)
DANGEROUS = {
    "·": r"\cdot",      # ·
    "°": r"{}^\circ",   # °
    "−": r"-",          # −  (minus sign)
    "×": r"\times",     # ×
    "≈": r"\approx",    # ≈
    "±": r"\pm",        # ±
    "≠": r"\ne",        # ≠
    "≤": r"\le",        # ≤
    "≥": r"\ge",        # ≥
    "∞": r"\infty",     # ∞
    "∇": r"\nabla",     # ∇
}

# Commands KaTeX does NOT support out of the box. A command here is flagged ONLY
# when the file does not register it as a macro (see registered_macros). The design
# system's template defines \degree, \bm, \cdotp, \d, \e, \i, \dj — and some files
# also define \celsius / \unit. A \cmd backed by a macro in THIS file renders fine,
# so check_forbidden skips it; the same \cmd used WITHOUT a macro definition (older
# templates) is still caught. This removes the \celsius/\unit false positive that
# used to FAIL otherwise-healthy files on their own macro-definition line, while
# still catching a genuinely undefined \celsius in a file that never registered it.
FORBIDDEN_CMDS = [
    r"\celsius", r"\unit", r"\SI", r"\qty", r"\cancel",
    r"\ket", r"\bra", r"\tensor", r"\si",
]

CONTAINER_HINT = (".fbox / .big-formula / .callout / .answer-box / .example-block")


def line_of(text, pos):
    return text[:pos].count("\n") + 1


def check_unicode_in_math(html):
    hits = []
    for m in MATH_RE.finditer(html):
        span = m.group()
        for ch, fix in DANGEROUS.items():
            if ch in span:
                hits.append((line_of(html, m.start()), ch, fix, span[:70].replace("\n", " ")))
    return hits


def check_boxed(html):
    return [line_of(html, m.start()) for m in re.finditer(r"\\boxed", html)]


def registered_macros(html):
    r"""Names of \macros the file registers in its renderMathInElement macros:{...}
    block, e.g. '\\celsius': '...' or "\\bm":"...". Returns a set WITHOUT the leading
    backslash, so {'celsius', 'unit', 'degree', ...}. A command the file defines this
    way renders correctly in that file, so it must not be flagged as forbidden."""
    return set(re.findall(r"""['"]\\\\([A-Za-z]+)['"]\s*:""", html))


def check_forbidden(html):
    defined = registered_macros(html)
    hits = []
    for cmd in FORBIDDEN_CMDS:
        if cmd.lstrip("\\") in defined:
            continue  # registered as a macro in THIS file → renders fine, not forbidden
        for m in re.finditer(re.escape(cmd) + r"(?![A-Za-z])", html):
            hits.append((line_of(html, m.start()), cmd))
    return hits


def check_div_balance(html):
    opens = len(re.findall(r"<div\b", html))
    closes = len(re.findall(r"</div\s*>", html))
    page_open = len(re.findall(r'<div\s+class="[^"]*\bpage\b', html))
    return opens, closes, page_open


def check_dollar_balance(html):
    stripped = MATH_RE.sub("", html)
    # remove escaped \$ before counting
    stripped = stripped.replace(r"\$", "")
    stray = stripped.count("$")
    return stray


def run_checks(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"FAIL: file not found: {path}")
        return False

    fails = 0
    print(f"=== checking {path} ({len(html)} chars) ===")

    uni = check_unicode_in_math(html)
    if uni:
        fails += 1
        print(f"\n[FAIL] {len(uni)} dangerous Unicode char(s) inside math:")
        for ln, ch, fix, ctx in uni[:40]:
            print(f"  line {ln}: U+{ord(ch):04X} '{ch}' -> use {fix}   …{ctx}…")
        if len(uni) > 40:
            print(f"  … and {len(uni) - 40} more")
    else:
        print("[ok]  no dangerous Unicode inside math")

    fb = check_forbidden(html)
    if fb:
        fails += 1
        print(f"\n[FAIL] {len(fb)} forbidden KaTeX command(s):")
        for ln, cmd in fb[:40]:
            print(f"  line {ln}: {cmd}")
    else:
        print("[ok]  no forbidden KaTeX commands")

    opens, closes, page_open = check_div_balance(html)
    if opens != closes:
        fails += 1
        print(f"\n[FAIL] <div> imbalance: {opens} '<div>' vs {closes} '</div>' "
              f"(diff {opens - closes:+d})")
    else:
        print(f"[ok]  <div> balanced ({opens} open / {closes} close)")
    if page_open != 1:
        print(f"[warn] found {page_open} '.page' wrappers (expected exactly 1)")

    stray = check_dollar_balance(html)
    if stray:
        fails += 1
        print(f"\n[FAIL] {stray} stray '$' outside any matched math span "
              "(likely an unbalanced delimiter — check for $ ... missing closing $)")
    else:
        print("[ok]  $ delimiters balanced")

    boxed = check_boxed(html)
    if boxed:
        print(f"\n[WARN] {len(boxed)} '\\boxed' occurrence(s) at line(s) "
              f"{', '.join(map(str, boxed[:30]))}{' …' if len(boxed) > 30 else ''}")
        print(f"       Remove \\boxed{{}} when it sits inside {CONTAINER_HINT}.")
        print("       (Allowed only in plain prose. Review each one.)")
    else:
        print("[ok]  no \\boxed found")

    print()
    if fails:
        print(f"RESULT: {fails} FAIL-level check(s). Fix and re-run.")
        return False
    print("RESULT: all checks passed." + (" (review \\boxed warnings above)" if boxed else ""))
    return True


def cmd_build(args):
    pieces = []
    for p in args.parts:
        try:
            with open(p, "r", encoding="utf-8") as f:
                pieces.append(f.read())
        except FileNotFoundError:
            sys.exit(f"part not found: {p}")
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(pieces))
    print(f"Concatenated {len(args.parts)} part(s) -> {args.out}\n")
    ok = run_checks(args.out)
    sys.exit(0 if ok else 1)


def cmd_check(args):
    ok = run_checks(args.html)
    sys.exit(0 if ok else 1)


def main():
    p = argparse.ArgumentParser(description="Concatenate study-notes parts and run static checks.")
    sub = p.add_subparsers(dest="cmd", required=True)

    pb = sub.add_parser("build", help="concatenate part files then check")
    pb.add_argument("parts", nargs="+", help="part HTML files in order")
    pb.add_argument("-o", "--out", required=True, help="output HTML")
    pb.set_defaults(func=cmd_build)

    pc = sub.add_parser("check", help="run static checks on an HTML file")
    pc.add_argument("html")
    pc.set_defaults(func=cmd_check)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()