#!/usr/bin/env python3
"""A score on a card is a claim that somebody read it -- whatever the card says about itself.

97bfc02/caab22d made "a verified guest score beside an unknown availability" a finding, because
the two live on the same page and one visit answers both. The rule keyed on
`guest_rating_status`, an optional field the author writes about their own card: set it to null and
the same score, the same unknown availability and no reason passed (measured 2026-09-24). The
score's citation rule ran only `if guest_rating_url:`, and that URL was optional too, so omitting
it skipped the check written for exactly this defect. And "a researched current price beside an
unknown availability" was refused for hotels only, while a flight, a train or a car priced for
dated search is read off the same kind of page. A ticket price list is undated, so it stays out.

Run:  python tests/test_record_once.py
      python -m pytest tests/test_record_once.py
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_plan_consistency as cpc  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"
BASE = json.loads(FIXTURE.read_text(encoding="utf-8"))

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def errors_of(plan: dict) -> list[str]:
    errors: list[str] = []
    cpc.check_booking_identity(plan, errors, [])
    return errors


def new_errors(plan: dict) -> list[str]:
    baseline = errors_of(BASE)
    return [e for e in errors_of(plan) if e not in baseline]


def priced_unknown(kind: str, **card) -> dict:
    plan = copy.deepcopy(BASE)
    base = {"id": f"{kind}-1", "review_url": "https://provider.test/search",
            "price_status": "researched_current", "availability_status": "unknown"}
    base.update(card)
    plan["booking_options"][kind] = [base]
    return plan


def main() -> int:
    check("the fixture itself raises none of these", not [
        e for e in errors_of(BASE) if "researched_current" in e or "guest score" in e])

    # 1. The status left blank no longer switches the rule off: the score is the claim.
    plan = copy.deepcopy(BASE)
    hotel = plan["booking_options"]["accommodations"][0]
    hotel["guest_rating_status"] = None
    hotel["availability_status"] = "unknown"
    hotel.pop("availability_unknown_reason", None)
    found = [e for e in new_errors(plan) if "availability" in e]
    check("a score with a blank status and an unknown availability is refused", found,
          new_errors(plan))

    # 2. A hotel score has to cite where it was read, like a restaurant's.
    for field in ("guest_rating_url", "guest_rating_checked_at"):
        plan = copy.deepcopy(BASE)
        plan["booking_options"]["accommodations"][0].pop(field, None)
        found = [e for e in new_errors(plan) if field in e]
        check(f"a hotel score without {field} is refused", found, new_errors(plan))

    # 3. Researched current price, unknown availability: refused for every dated search.
    for kind, card in (("flights", {"provider": "KLM"}),
                       ("ground_transport", {"provider": "LNER"}),
                       ("rental_cars", {"provider": "Hertz"})):
        found = [e for e in new_errors(priced_unknown(kind, **card)) if "researched_current" in e]
        check(f"a {kind} card priced as current with unknown availability is refused", found,
              new_errors(priced_unknown(kind, **card)))
    # ... but not for a ticket, whose price list is undated.
    found = [e for e in new_errors(priced_unknown("attraction_tickets", attraction_name="Castle"))
             if "researched_current" in e]
    check("a ticket priced from an undated list is left alone", not found, found)

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("record-once cases passed")
    return 0


def test_record_once() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
