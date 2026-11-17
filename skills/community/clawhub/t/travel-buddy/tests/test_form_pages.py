#!/usr/bin/env python3
"""What the forms' CSS does to their markup -- the part the JavaScript shim cannot see.

The trip form hides its follow-up questions with the `hidden` attribute and the shim tests assert
`element.hidden` flips at the right moment; they did, and every follow-up was on screen anyway.
A later rule, `.grid > div { display:flex }`, outranks the browser's own `[hidden] { display:none }`
(author CSS beats the user-agent stylesheet whatever the specificity), so all seven panels inside
a grid -- "what exactly is booked (required)", the multi-stop bounds, the custom currency and budget
boxes, the held-visa pair, the visa-effort question -- rendered permanently, found on 2026-09-24 by
reading computed styles in a real browser. A traveller who had booked nothing was shown a required
box for booking details.

The check is general rather than about that one rule: a form that uses `hidden` must declare
`[hidden] { display:none !important }`, which is the only rule no later `display` can undo.

Run:  python tests/test_form_pages.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORMS = [ROOT / "assets" / "trip-intake-form.html", ROOT / "assets" / "traveler-profile-intake.html"]


def honours_hidden(html: str) -> bool:
    css = " ".join(re.findall(r"<style[^>]*>(.*?)</style>", html, re.S))
    css = re.sub(r"/\*.*?\*/", " ", css, flags=re.S)   # a comment may quote CSS, braces and all
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if "[hidden]" in [s.strip() for s in selectors.split(",")] and re.search(
                r"display\s*:\s*none\s*!\s*important", body):
            return True
    return False


def main() -> int:
    failures = []
    for form in FORMS:
        html = form.read_text(encoding="utf-8")
        uses_hidden = re.search(r"<[a-z][^>]*\shidden(?:[\s>=])", html) is not None
        if uses_hidden and not honours_hidden(html):
            failures.append(f"{form.name}: uses the hidden attribute but has no "
                            "[hidden] { display:none !important } rule, so any display rule on a "
                            "hidden element shows it")
    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print(f"form page cases passed for {len(FORMS)} form(s)")
    return 0


def test_form_pages() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
