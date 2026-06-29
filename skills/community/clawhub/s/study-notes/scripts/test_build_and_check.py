#!/usr/bin/env python3
r"""Self-contained regression tests for build_and_check.py.

Locks in the macro-aware forbidden-command fix: a \command that the file registers
as a KaTeX macro must NOT be flagged, while the same command used WITHOUT a macro
definition (older templates) must still be caught. No external corpus needed.

Run:  python test_build_and_check.py
"""
import build_and_check as b

# Mimic a real template macro-registration line: in the HTML bytes, '\celsius' has
# TWO backslashes (a JS string escaping one LaTeX backslash). \\\\ here -> '\\' there.
DEFINES = (
    "<script>renderMathInElement(document.body,{macros:{"
    "'\\\\celsius':'{{{}^\\\\circ\\\\text{C}}}','\\\\unit':'{\\\\,\\\\text}',"
    "'\\\\degree':'{{}^\\\\circ}'}});</script>\n"
    "<div class=\"fbox\">$T=20\\celsius$ and $v=3\\unit{m/s}$</div>"
)
USES_UNDEFINED = "<div class=\"fbox\">$T=20\\celsius$</div>"
SI_ALWAYS_BAD = "<script>macros:{'\\\\degree':'{{}^\\\\circ}'}</script><div>$\\SI{1}{m}$</div>"


def run():
    # 1. macros the file defines are recognised
    macros = b.registered_macros(DEFINES)
    assert {"celsius", "unit", "degree"} <= macros, f"macros not detected: {macros}"

    # 2. a defined macro is NOT reported as forbidden (the old false positive)
    hits = b.check_forbidden(DEFINES)
    assert hits == [], f"defined \\celsius/\\unit must not be flagged, got {hits}"

    # 3. the SAME command, used without being defined, is STILL caught
    hits = b.check_forbidden(USES_UNDEFINED)
    assert any(cmd == r"\celsius" for _, cmd in hits), \
        f"undefined \\celsius must still be caught, got {hits}"

    # 4. genuinely unsupported commands stay forbidden regardless of unrelated macros
    hits = b.check_forbidden(SI_ALWAYS_BAD)
    assert any(cmd == r"\SI" for _, cmd in hits), f"\\SI must always be caught, got {hits}"

    print("OK  build_and_check regression tests passed (4/4)")


if __name__ == "__main__":
    run()
