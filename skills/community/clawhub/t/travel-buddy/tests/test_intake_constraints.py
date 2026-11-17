#!/usr/bin/env python3
"""What the form collected about the traveller's limits must reach the plan.

Only `experience.ranked_must_haves` was ever compared with the intake file. The allergy, the walking
limit, the party size and the budget cap were copied across by new_plan_skeleton.py --from-intake
and then read by nothing: a plan built from flags, edited by hand, or written by a second planner
could drop a severe dairy allergy and save clean. Measured on 2026-09-24 against v2.7.0: an intake
carrying 「严重乳制品过敏」 and a 20-minute walking limit, a plan carrying neither, 0 findings --
while the same plan missing one ranked must-have produced 1.

A traveller may still change their mind after the form -- a real run raised its cap to 1300 at the
checkpoint -- so a divergence is allowed when the plan records it in `trip.intake_changes` with a
reason, and the page prints that reason beside the constraints it changed.

Run:  python tests/test_intake_constraints.py
      python -m pytest tests/test_intake_constraints.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_plan_consistency as cpc  # noqa: E402
import render_final_trip_html as renderer  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def intake(**over) -> dict:
    """A minimal intake in the fixture's own currency; `block__key=value` overrides one field."""
    base = {"origin": {"home_city": "Fixture City"},
            "party": {"traveler_count": 2, "mobility_or_access_needs": []},
            "budget": {"currency": "CNY", "hard_cap_amount": None},
            "feasibility": {"dietary_or_religious_needs": []},
            "experience": {"ranked_must_haves": []}}
    for dotted, value in over.items():
        block, key = dotted.split("__")
        base[block][key] = value
    return base


def build(tmp: Path, collected: dict, *, constraints=None, count=None, cap=None,
          changes=None) -> dict:
    path = tmp / "intake-20260101-fixture.json"
    path.write_text(json.dumps(collected, ensure_ascii=False), encoding="utf-8")
    plan = json.loads(FIXTURE.read_text(encoding="utf-8"))
    plan["intake_context"]["intake_file"] = str(path)
    if constraints is not None:
        plan["trip"]["traveler_constraints"] = constraints
    if count is not None:
        plan["trip"]["traveler_count"] = count
    if cap is not None:
        plan["budget"]["cap_per_person"] = cap
    if changes is not None:
        plan["trip"]["intake_changes"] = changes
    return plan


def run(plan: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    cpc.check_preferences_came_from_the_intake(plan, errors, notes)
    return errors, notes


def main() -> int:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)

        # 1. A severe allergy in the intake and nowhere in the plan: the case that shipped silent.
        errors, _ = run(build(tmp, intake(feasibility__dietary_or_religious_needs=[
            "severe dairy allergy"])))
        check("an allergy the intake recorded and the plan dropped is refused",
              any("severe dairy allergy" in e for e in errors), errors)

        # 2. Carried with different case and spacing: the same statement, no finding.
        errors, _ = run(build(tmp, intake(feasibility__dietary_or_religious_needs=[
            "severe dairy allergy"]), constraints={
                "dietary_or_religious_needs": ["Severe Dairy Allergy "]}))
        check("a carried allergy passes whatever its case", not errors, errors)

        # 3. The walking limit, the other constraint whose violation strands a traveller.
        errors, _ = run(build(tmp, intake(party__mobility_or_access_needs=[
            "no walk over 20 min"])))
        check("a mobility note the plan dropped is refused",
              any("no walk over 20 min" in e for e in errors), errors)

        # 4. Party size: refused silently diverging, accepted when the change is recorded.
        errors, _ = run(build(tmp, intake(), count=1))
        check("a party-size divergence is refused",
              any("traveler_count" in e for e in errors), errors)
        errors, _ = run(build(tmp, intake(), count=1, changes=[
            {"field": "traveler_count", "intake_value": 2, "plan_value": 1,
             "reason": "Their friend cancelled (chat, 2026-09-20)."}]))
        check("a recorded party-size change passes", not errors, errors)

        # 5. The budget cap, raised at the checkpoint the way a real run raised it.
        errors, _ = run(build(tmp, intake(budget__hard_cap_amount=750), cap=1300))
        check("a cap divergence is refused", any("cap_per_person" in e for e in errors), errors)
        errors, _ = run(build(tmp, intake(budget__hard_cap_amount=750), cap=1300, changes=[
            {"field": "cap_per_person", "intake_value": 750, "plan_value": 1300,
             "reason": "Raised at the checkpoint for the lake hotel."}]))
        check("a recorded cap change passes", not errors, errors)
        errors, _ = run(build(tmp, intake(budget__hard_cap_amount=750), cap=1300, changes=[
            {"field": "cap_per_person", "intake_value": 750, "plan_value": 1300,
             "reason": "   "}]))
        check("a change with no reason is refused",
              any("intake_changes[0]" in e and "reason" in e for e in errors), errors)
        errors, _ = run(build(tmp, intake(budget__hard_cap_amount=750), cap=750))
        check("a carried cap passes", not errors, errors)

        # 5b. A recorded change excuses a figure only while it still describes the plan. A stale
        #     entry -- 2 -> 1 recorded, the plan since moved to 5 -- used to silence the check for
        #     that field entirely, and the page printed "Party size: 2 -> 1" beside "5 traveller(s)".
        errors, _ = run(build(tmp, intake(), count=5, changes=[
            {"field": "traveler_count", "intake_value": 2, "plan_value": 1,
             "reason": "Their friend cancelled (chat, 2026-09-20)."}]))
        check("a stale party-size change does not excuse a different party size",
              any("traveler_count" in e for e in errors), errors)
        errors, _ = run(build(tmp, intake(budget__hard_cap_amount=750), cap=5000, changes=[
            {"field": "cap_per_person", "intake_value": 750, "plan_value": 1300,
             "reason": "Raised at the checkpoint for the lake hotel."}]))
        check("a stale cap change does not excuse a different cap",
              any("cap_per_person" in e for e in errors), errors)
        errors, _ = run(build(tmp, intake(budget__hard_cap_amount=900), cap=1300, changes=[
            {"field": "cap_per_person", "intake_value": 750, "plan_value": 1300,
             "reason": "Raised at the checkpoint for the lake hotel."}]))
        check("a change from a figure the intake no longer says does not excuse",
              any("cap_per_person" in e for e in errors), errors)
        errors, _ = run(build(tmp, intake(budget__hard_cap_amount=750), cap=1300, changes=[
            {"field": "cap_per_person", "intake_value": "750", "plan_value": "1300.00",
             "reason": "Raised at the checkpoint for the lake hotel."}]))
        check("a change written with its numbers as text still counts", not errors, errors)

        # 6. A cap in another currency cannot be compared: say so, never fail on it.
        errors, notes = run(build(tmp, intake(budget__hard_cap_amount=750,
                                              budget__currency="EUR"), cap=5900))
        check("a cross-currency cap is a note, not an error",
              not errors and any("EUR" in n and "CNY" in n for n in notes), (errors, notes))

        # 7. intake_changes may only name a field this check compares.
        errors, _ = run(build(tmp, intake(), changes=[{"field": "allergy", "reason": "x"}]))
        check("an unknown intake_changes field is refused",
              any("intake_changes[0]" in e and "allergy" in e for e in errors), errors)

        # 8. The portable-document rule: an intake that is not there costs the cross-check, never
        #    the plan.
        plan = build(tmp, intake(feasibility__dietary_or_religious_needs=["nuts"]))
        plan["intake_context"]["intake_file"] = str(tmp / "intake-moved-away.json")
        errors, notes = run(plan)
        check("a missing intake is a note only", not errors and notes, (errors, notes))

        # 9. The page shows a recorded change -- stored and never shown is never gathered -- and a
        #    Chinese page shows it without renderer English.
        plan = build(tmp, intake(), count=1, changes=[
            {"field": "traveler_count", "intake_value": 2, "plan_value": 1,
             "reason": "CANARY-REASON"}])
        page = renderer.render(plan)
        check("the change and its reason reach the page",
              "CANARY-REASON" in page and 'class="intake-changes"' in page)
        plan["trip"]["language"] = "zh-CN"
        chinese = renderer.render(plan)
        check("a Chinese page translates the change heading",
              "Changed since your form" not in chinese and "CANARY-REASON" in chinese)
        check("a Chinese page translates the field label",
              "Travellers: " not in chinese.split('class="intake-changes"', 1)[-1][:400])

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("intake constraint cases passed")
    return 0


def test_intake_constraints() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
