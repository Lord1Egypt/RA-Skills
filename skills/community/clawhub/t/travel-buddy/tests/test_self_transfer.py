#!/usr/bin/env python3
"""A self-transfer leg is consented to in the traveller's words and warned about on the page.

kiwi_flights.py excludes separate-ticket connections unless the traveller accepts them; when they
do, the leg carries `self_transfer: true`. Nothing protects a missed connection on separate tickets,
so the page must say so on the card, and the plan must hold the words in which the traveller agreed.

Run:  python tests/test_self_transfer.py
      python -m pytest tests/test_self_transfer.py
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

import check_plan_consistency as cpc  # noqa: E402
import plan_flags  # noqa: E402
import render_final_trip_html as renderer  # noqa: E402
import validate_trip_html as htmlgate  # noqa: E402
import kiwi_flights as kf  # noqa: E402
from test_kiwi_flights import DIRECT, KLM, SELF_TRANSFER, REQUEST  # noqa: E402

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def flight_plan(language: str = "en", consent: str | None = None, marked: bool = True) -> dict:
    plan = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))
    plan["trip"].update({"language": language, "traveler_count": 4, "currency": "EUR"})
    request = dict(REQUEST, language="zh" if language.startswith("zh") else "en")
    source = dict(SELF_TRANSFER, _self_transfer=True) if marked else SELF_TRANSFER
    cards = [kf.itinerary_to_card(source, request, 0, "2026-10-11", single=False),
             kf.itinerary_to_card(KLM, request, 1, "2026-10-11", single=False)]
    plan["booking_options"]["flights"] = cards
    if consent is not None:
        plan["trip"]["traveler_preferences"]["accepts_self_transfer"] = consent
    return plan


def consistency(plan: dict) -> list[str]:
    errors: list[str] = []
    cpc.check_self_transfer_consent(plan, errors, [])
    return errors


def main() -> int:
    check("the check runs on the save path", cpc.check_self_transfer_consent in cpc.PLAN_CHECKS)
    check("a self-transfer leg without consent fails",
          any("accepts_self_transfer" in e for e in consistency(flight_plan())), consistency(flight_plan()))
    check("a placeholder is not consent", consistency(flight_plan(consent="TODO: ask")))
    check("the traveller's words are", not consistency(flight_plan(consent="Fine, we travel light.")))
    bad = flight_plan(consent="ok")
    bad["booking_options"]["flights"][0]["outbound_itinerary"]["self_transfer"] = "yes"
    check("a non-boolean mark is refused", any("must be true, false or absent" in e for e in consistency(bad)))
    check("no marked leg, no finding", not consistency(flight_plan(marked=False)))

    for language in ("en", "zh-CN"):
        plan = flight_plan(language, consent="Fine, we travel light.")
        page = renderer.render(plan)
        check(f"the warning row is printed ({language})", 'data-self-transfer-leg="outbound"' in page)
        check(f"only for the marked leg ({language})", 'data-self-transfer-leg="return"' not in page)
        check(f"the price note is printed ({language})",
              renderer.html.escape(plan["booking_options"]["flights"][0]["price_note"], quote=True) in page)
        flags = plan_flags.derive_html_flags(plan)
        errors = htmlgate.validate(page, flags.expected_days, set(flags.required_booking_types),
                                   flags.transport_mode, [], require_unverified_banner=flags.require_unverified_banner,
                                   plan=plan)
        check(f"no renderer English and no warning finding ({language})",
              not [e for e in errors if "English" in e or "self-transfer" in e.lower()], errors[:3])
        stripped = page.replace('data-self-transfer-leg="outbound"', 'data-x="outbound"')
        errors = htmlgate.validate(stripped, flags.expected_days, set(flags.required_booking_types),
                                   flags.transport_mode, [], require_unverified_banner=flags.require_unverified_banner,
                                   plan=plan)
        check(f"a page missing the warning fails ({language})",
              any("self-transfer" in e.lower() for e in errors), errors[:3])

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("self-transfer cases passed")
    return 0


def test_self_transfer() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
