#!/usr/bin/env python3
"""What a self-drive traveller needs on the page, on the path no real run had ever taken.

All eighteen real plans in the author's workspace were public transport, so the self-drive half of
the renderer had never met a real trip. A synthetic English family trip -- train to Edinburgh, a
hired car, Pitlochry and St Andrews -- found what it prints wrong (2026-09-24). That trip is now
tests/self-drive-fixture.json, so this path has a regression fixture of its own:

* The hire's restrictions -- ferries, other countries, driver age -- were a required field printed
  nowhere.
* A driving day never showed how far it drives, while its route figure printed an unlabelled
  number that was the straight-line span between the two furthest stops.
* The overview button read "Open the airport transfer route" on a trip with no airport.
* A train day said "No verified ticket is required for the listed activities."
* The overview's total distance was never compared with the days it sums.

Run:  python tests/test_self_drive_page.py
      python -m pytest tests/test_self_drive_page.py
"""

from __future__ import annotations

import copy
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_plan_consistency as cpc  # noqa: E402
import plan_flags  # noqa: E402
import render_final_trip_html as renderer  # noqa: E402
import validate_trip_html as htmlgate  # noqa: E402

FIXTURE = ROOT / "tests" / "self-drive-fixture.json"
BASE = json.loads(FIXTURE.read_text(encoding="utf-8"))

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def day_html(page: str, number: int) -> str:
    start = page.index(f'id="day-{number}"')
    end = page.find('class="day-card"', start + 10)
    return page[start:end if end > 0 else len(page)]


def main() -> int:
    check("the fixture passes every plan gate", not renderer.validate_plan(BASE),
          renderer.validate_plan(BASE)[:2])
    page = renderer.render(BASE)

    # The hire's limits reach the page.
    note = BASE["booking_options"]["rental_cars"][0]["cross_border_or_restriction_note"]
    check("a rental card prints its restrictions", html.escape(note, quote=True) in page,
          note[:60])

    # A driving day says how far it drives, and the figure says what its number is.
    check("a self-drive day's route line states its distance",
          "45.3 km" in day_html(page, 2).split('class="day-route"', 1)[-1][:900],
          day_html(page, 2).split('class="day-route"', 1)[-1][:300])
    check("the route figure labels its straight-line span", "straight-line" in page,
          "an unlabelled distance")

    # No airport that is not there.
    check("the overview button names no airport on a trip without one",
          "airport transfer route" not in page and "Open the route overview" in page)

    # A train day is not a day with no tickets.
    first = day_html(page, 1)
    check("a train day does not claim no ticket is needed",
          "No verified ticket is required" not in first, "the train day says no ticket")
    check("a train day points at its transport tickets", "transport tickets" in first,
          first[-400:])

    # The overview's total is the sum of the days.
    short = copy.deepcopy(BASE)
    short["transport_overview"]["overall_distance_km"] = 334
    errors: list[str] = []
    cpc.check_routes(short, errors, [])
    check("an overview total that is not the days' sum is refused",
          any("overall_distance_km" in e for e in errors), errors)
    errors = []
    cpc.check_routes(BASE, errors, [])
    check("the days' own sum passes", not [e for e in errors if "overall_distance_km" in e],
          errors)

    # The same page in Chinese adds no renderer English.
    chinese = copy.deepcopy(BASE)
    chinese["trip"]["language"] = "zh-CN"
    zh_page = renderer.render(chinese)
    flags = plan_flags.derive_html_flags(chinese)
    leaks = [e for e in htmlgate.validate(zh_page, flags.expected_days,
                                          set(flags.required_booking_types), flags.transport_mode,
                                          [], require_unverified_banner=flags.require_unverified_banner)
             if "English" in e]
    check("a Chinese self-drive page carries no renderer English", not leaks, leaks[:2])

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("self-drive page cases passed")
    return 0


def test_self_drive_page() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
