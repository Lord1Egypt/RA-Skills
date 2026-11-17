#!/usr/bin/env python3
"""The page after a decision: the decided card leads with a badge, its alternatives fold away.

Run:  python tests/test_booking_page.py
      python -m pytest tests/test_booking_page.py
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import plan_flags  # noqa: E402
import render_final_trip_html as renderer  # noqa: E402
import validate_trip_html as htmlgate  # noqa: E402

SELF_DRIVE = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))
YESTERDAY = (dt.date.today() - dt.timedelta(days=1)).isoformat()

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def plan_with(records: list[dict], language: str = "en") -> dict:
    plan = copy.deepcopy(SELF_DRIVE)
    plan["trip"]["language"] = language
    plan["bookings"] = records
    return plan


BOOKED_RAIL = {"option_id": "gt-lner", "state": "booked", "booked_on": YESTERDAY,
               "booked_via": "QZVIA LNER website", "paid_total": 180, "paid_currency": "GBP"}
CHOSEN_CAR = {"option_id": "car-hertz", "state": "chosen"}


def gate(plan: dict, page: str) -> list[str]:
    flags = plan_flags.derive_html_flags(plan)
    return htmlgate.validate(page, flags.expected_days, set(flags.required_booking_types), flags.transport_mode,
                             [], require_unverified_banner=flags.require_unverified_banner, plan=plan)


def main() -> int:
    plain = renderer.render(copy.deepcopy(SELF_DRIVE))
    check("no_bookings_page_unchanged: no badge, browse heading",
          'class="booking-badge"' not in plain and 'data-bookings="none"' in plain and "Browse options — no purchase made" in plain)

    for language in ("en", "zh-CN"):
        plan = plan_with([BOOKED_RAIL, CHOSEN_CAR], language)
        page = renderer.render(plan)
        panel = re.search(r'<section id="booking-panel".*?</section>\s*(?=<article class="day-card"|<section)', page, re.S)
        panel = panel.group(0) if panel else page
        check(f"the booked card carries its badge ({language})",
              'data-booking-option="gt-lner" data-booking-state="booked"' in page)
        check(f"the chosen card carries its badge ({language})",
              'data-booking-option="car-hertz" data-booking-state="chosen"' in page)
        group = re.search(r'<section class="option-group" data-option-group="ground">.*?</section>', page, re.S)
        group = group.group(0) if group else ""
        check(f"the booked card leads its group ({language})",
              0 <= group.find('data-booking-option="gt-lner"') < group.find('<details class="not-chosen"'), group[:300])
        check(f"the alternative is folded ({language})",
              re.search(r'<details class="not-chosen" data-booking-group="ground_transport:leg-london-edinburgh">.*?Lumo', page, re.S))
        check(f"the details start closed ({language})", '<details class="not-chosen" open' not in page)
        check(f"the channel is printed ({language})", "QZVIA LNER website" in htmlgate.visible_text(page))
        check(f"the panel says a purchase was made ({language})", 'data-bookings="booked"' in page)
        heading = ("Your bookings and options" if language == "en"
                   else renderer.labels_for(language)["booking_heading"])
        browse = re.search(r'<section id="booking-panel"[^>]*><h2>([^<]*)</h2>', page)
        check(f"and its heading says so ({language})", browse and browse.group(1) == heading,
              browse.group(1) if browse else "no heading")
        check(f"the budget gains its booked line ({language})", "booked-so-far" in page and "£180" in page)
        errors = gate(plan, page)
        check(f"the page passes, with no renderer English ({language})", not errors, errors[:3])

    only_chosen = renderer.render(plan_with([CHOSEN_CAR]))
    check("a chosen record is not a purchase", 'data-bookings="chosen"' in only_chosen
          and "Browse options — no purchase made" in only_chosen)
    cleared = renderer.render(plan_with([]))
    check("cleared_page", 'class="booking-badge"' not in cleared and "booked-so-far" not in cleared
          and "Browse options — no purchase made" in cleared)
    dangling = renderer.render(plan_with([{"option_id": "gone-1", "state": "booked", "booked_on": YESTERDAY, "booked_via": "x"}]))
    check("dangling_record_renders", 'class="booking-badge"' not in dangling)

    # The page gate: a record with no badge is refused.
    plan = plan_with([BOOKED_RAIL])
    page = renderer.render(plan).replace('data-booking-state="booked"', 'data-x="booked"')
    check("a page missing a recorded badge fails", any("booking" in e.lower() for e in gate(plan, page)), gate(plan, page)[:3])

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("booking page cases passed")
    return 0


def test_booking_page() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
