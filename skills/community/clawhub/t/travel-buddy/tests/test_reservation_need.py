#!/usr/bin/env python3
"""A dining card says whether it needs booking, as an enum the calendar's reminder can trust.

The reminder used to be guessed from the queue note: "Book for 12:45 on a Saturday" in the
self-drive fixture got none, and "Reservations not accepted" would have got one.
Spec: docs/superpowers/specs/2026-10-11-calendar-fixes-design.md.

Run:  python tests/test_reservation_need.py
      python -m pytest tests/test_reservation_need.py
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_plan_contract as contract  # noqa: E402
import render_final_trip_html as renderer  # noqa: E402

SELF_DRIVE = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))
failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def with_need(value: object, language: str | None = None) -> dict:
    plan = copy.deepcopy(SELF_DRIVE)
    plan["days"][0]["dining"][0]["reservation_need"] = value
    if language:
        plan["trip"]["language"] = language
    return plan


def main() -> int:
    check("the vocabulary", renderer.RESERVATION_NEEDS == ("required", "recommended", "walk_in", "not_accepted"))
    check("every fixture card states its need",
          all(c.get("reservation_need") in renderer.RESERVATION_NEEDS for d in SELF_DRIVE["days"] for c in d["dining"]),
          [c.get("reservation_need") for d in SELF_DRIVE["days"] for c in d["dining"]])
    import validate_trip_html as htmlgate  # noqa: PLC0415
    todo_page = renderer.render(with_need("TODO: required | recommended | walk_in | not_accepted"))
    check("a TODO need is printed, so the page gate's TODO scan refuses the page",
          "TODO: required" in htmlgate.visible_text(todo_page))
    for value in renderer.RESERVATION_NEEDS + (None, "TODO: required | recommended | walk_in | not_accepted"):
        errors = [e for e in renderer.validate_plan(with_need(value)) if "reservation_need" in e]
        check(f"validate_plan accepts {value!r}", not errors, errors)
    errors = [e for e in renderer.validate_plan(with_need("maybe")) if "reservation_need" in e]
    check("validate_plan refuses a value outside the enum", errors, renderer.validate_plan(with_need("maybe"))[:3])

    table, failure = contract._vocabularies()
    check("the contract checks the enum", table.get("days[].dining[].reservation_need") == set(renderer.RESERVATION_NEEDS),
          (failure, table.get("days[].dining[].reservation_need")))
    found = contract.enum_issues(with_need("maybe"), table)
    check("check_plan_contract flags a wrong value", any(i["path"].endswith("reservation_need") for i in found), found)
    found = contract.enum_issues(with_need("TODO: pick one"), table)
    check("check_plan_contract leaves a TODO to the placeholder gate", not found, found)

    page = renderer.render(with_need("required"))
    check("the page shows the need", '<span class="reservation-need" data-reservation-need="required">Booking required</span>' in page)
    zh = renderer.render(with_need("required", "zh-CN"))
    check("the Chinese page shows it in Chinese", 'data-reservation-need="required">需提前订位</span>' in zh
          and "Booking required" not in zh)

    scaffold = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "new_plan_skeleton.py"),
         "--start", "2027-05-07", "--end", "2027-05-10", "--origin", "Amsterdam", "--destination", "Bern",
         "--intake-method", "user_supplied", "--source-note", "scaffold check"],
        capture_output=True, text=True)
    check("the scaffold runs", scaffold.returncode == 0, scaffold.stderr[-300:])
    if scaffold.returncode == 0:
        cards = [c for d in json.loads(scaffold.stdout)["days"] for c in d["dining"]]
        check("the scaffold asks every card for its need",
              cards and all(str(c.get("reservation_need")).startswith("TODO:") for c in cards),
              [c.get("reservation_need") for c in cards][:3])

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("reservation-need cases passed")
    return 0


def test_reservation_need() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
