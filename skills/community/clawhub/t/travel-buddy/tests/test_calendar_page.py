#!/usr/bin/env python3
"""The page's calendar offer says what the file carries: decided transport, and whether its times
carry zones. Spec: docs/superpowers/specs/2026-10-11-calendar-fixes-design.md.

Run:  python tests/test_calendar_page.py
      python -m pytest tests/test_calendar_page.py
"""

from __future__ import annotations

import copy
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import render_final_trip_html as renderer  # noqa: E402
import validate_trip_html as htmlgate  # noqa: E402

SELF_DRIVE = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))
BOOKING_READY = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))
failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def offer(page: str) -> str:
    match = re.search(r'<p class="calendar-offer">.*?</p>', page, re.S)
    return match.group(0) if match else ""


def main() -> int:
    page = renderer.render(SELF_DRIVE)
    text = htmlgate.visible_text(offer(page))
    check("the offer no longer promises every flight and train", "every flight, train" not in text, text)
    check("it says the decided transport goes in", "chosen or booked" in text, text)
    check("it counts the undecided groups", '<span class="count">2</span>' in offer(page), offer(page))
    check("a zoned plan has no floating warning", "calendar-floating" not in offer(page), offer(page))

    decided = copy.deepcopy(SELF_DRIVE)
    decided["bookings"] = [{"option_id": "gt-lner", "state": "chosen"}, {"option_id": "car-hertz", "state": "chosen"}]
    check("nothing undecided, no count", "calendar-undecided" not in offer(renderer.render(decided)))

    legacy = offer(renderer.render(BOOKING_READY))
    check("a plan without zones warns about floating times",
          "calendar-floating" in legacy and "Google Calendar" in htmlgate.visible_text(legacy), legacy)

    zh = copy.deepcopy(SELF_DRIVE)
    zh["trip"]["language"] = "zh-CN"
    zh_offer = offer(renderer.render(zh))
    zh_text = htmlgate.visible_text(zh_offer)
    check("zh_page: the offer is Chinese", "已选或已订" in zh_text and "还没决定" in zh_text, zh_text)
    check("zh_page: no renderer English", not re.search(r"[A-Za-z]{4,} [a-z]{3,}", zh_text), zh_text)
    zh_legacy = copy.deepcopy(BOOKING_READY)
    zh_legacy["trip"]["language"] = "zh-CN"
    check("zh_page: the floating warning is Chinese", "苹果日历" in htmlgate.visible_text(offer(renderer.render(zh_legacy))))

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("calendar page cases passed")
    return 0


def test_calendar_page() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
