#!/usr/bin/env python3
"""The bookings block: which group an option belongs to, what a valid record is, and why recording
a decision never re-opens a verification.

A plan was "booking-ready" and then stopped: nothing recorded that option A was booked, so the page
kept offering A and B under "Browse options -- no purchase made" and the calendar exported both.
Spec: docs/superpowers/specs/2026-10-11-booking-lifecycle-design.md.

Run:  python tests/test_bookings.py
      python -m pytest tests/test_bookings.py
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

import bookings  # noqa: E402
import verification_sections as vs  # noqa: E402

SELF_DRIVE = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))
BOOKING_READY = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))
SAVE = ROOT / "scripts" / "save_trip_deliverables.py"
TODAY = dt.date.today()
YESTERDAY = (TODAY - dt.timedelta(days=1)).isoformat()
TOMORROW = (TODAY + dt.timedelta(days=1)).isoformat()

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def with_records(plan: dict, *records: dict) -> dict:
    plan = copy.deepcopy(plan)
    plan["bookings"] = list(records)
    return plan


def booked(option_id: str, **extra) -> dict:
    return {"option_id": option_id, "state": "booked", "booked_on": YESTERDAY, "booked_via": "the airline's site", **extra}


def rules_cases() -> None:
    check("rail candidates share their leg group",
          bookings.group_key("ground_transport", {"id": "gt-lner", "leg_group_id": "leg-london-edinburgh"})
          == bookings.group_key("ground_transport", {"id": "gt-lumo", "leg_group_id": "leg-london-edinburgh"}))
    check("hotels group by stay group", bookings.group_key("accommodations", {"stay_group_id": "stay-pitlochry"})
          == "accommodations:stay-pitlochry")
    check("all rental cars are one group", bookings.group_key("rental_cars", {"id": "a"}) == bookings.group_key("rental_cars", {"id": "b"}))
    check("each ticket is its own group", bookings.group_key("attraction_tickets", {"id": "a"})
          != bookings.group_key("attraction_tickets", {"id": "b"}))
    check("the index finds every option", {"gt-lner", "car-hertz", "acc-pit-1", "tk-blair"} <= set(bookings.option_index(SELF_DRIVE)))
    check("days of a stay group", bookings.stay_days(SELF_DRIVE, "accommodations:stay-pitlochry") == [1, 2],
          bookings.stay_days(SELF_DRIVE, "accommodations:stay-pitlochry"))

    def problems(*records: dict) -> list[str]:
        return bookings.record_problems(with_records(SELF_DRIVE, *records), TODAY)

    check("a valid booked record passes", not problems(booked("gt-lner", paid_total=180, paid_currency="GBP")), problems(booked("gt-lner")))
    check("a chosen record passes", not problems({"option_id": "car-hertz", "state": "chosen"}))
    check("absent_block_is_quiet", not bookings.record_problems(SELF_DRIVE, TODAY))
    for label, record, needle in (
        ("dangling_record", booked("gone-1"), "gone-1"),
        ("an unknown state", {"option_id": "gt-lner", "state": "held"}, "state"),
        ("booked without a date", {"option_id": "gt-lner", "state": "booked", "booked_via": "x"}, "booked_on"),
        ("booked in the future", booked("gt-lner", booked_on=TOMORROW), "after today"),
        ("booked with a malformed date", booked("gt-lner", booked_on="15/10/2026"), "booked_on"),
        ("booked without a channel", {"option_id": "gt-lner", "state": "booked", "booked_on": YESTERDAY}, "booked_via"),
        ("paid without a currency", booked("gt-lner", paid_total=180), "paid_currency"),
        ("a negative payment", booked("gt-lner", paid_total=-1, paid_currency="GBP"), "paid_total"),
        ("a lower-case currency", booked("gt-lner", paid_total=180, paid_currency="gbp"), "paid_currency"),
        ("paid on a chosen record", {"option_id": "gt-lner", "state": "chosen", "paid_total": 1, "paid_currency": "GBP"}, "chosen"),
    ):
        found = problems(record)
        check(f"{label} is refused", any(needle in p for p in found), found)
    two = problems(booked("gt-lner"), {"option_id": "gt-lumo", "state": "chosen"})
    check("two records in one group are refused", any("same group" in p for p in two), two)
    switched = problems(booked("acc-pit-2"))
    check("a recorded hotel the days do not sleep at is refused", any("accommodation_option_id" in p for p in switched), switched)
    check("records for different groups are fine", not problems(booked("gt-lner"), booked("acc-pit-1"), {"option_id": "car-hertz", "state": "chosen"}))


def verification_cases() -> None:
    check("bookings is outside the verification fingerprints", "bookings" in vs.META_KEYS)
    plain = vs.section_digests(SELF_DRIVE)
    recorded = vs.section_digests(with_records(SELF_DRIVE, booked("gt-lner")))
    check("recording a booking changes no section's digest", plain == recorded,
          sorted(set(recorded.items()) ^ set(plain.items()))[:4])

    # End to end through the save path: a verified save, a booking recorded, a re-save with the
    # same report -- no recheck is asked for.
    from test_plan_consistency import full_verification  # noqa: PLC0415
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        plan = copy.deepcopy(BOOKING_READY)
        stem = f"{plan['trip']['start_date']}-trip"
        source = tmp / f"{stem}.json"
        source.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        report = full_verification()
        report["plan"] = source.name
        report_path = tmp / "report.json"
        report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        save = [sys.executable, str(SAVE), str(source), "--workspace", str(tmp / "ws"), "--slug", "trip"]
        first = subprocess.run(save + ["--verification", str(report_path)], capture_output=True, text=True)
        check("the verified save succeeds", first.returncode == 0, (first.stdout + first.stderr)[-600:])
        plan["bookings"] = [booked("stay-a")]
        source.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        again = subprocess.run(save + ["--overwrite", "--verification", str(report_path)], capture_output=True, text=True)
        check("re-saving after recording a booking needs no recheck", again.returncode == 0,
              (again.stdout + again.stderr)[-800:])


def gate_cases() -> None:
    import check_plan_consistency as cpc  # noqa: PLC0415
    check("check_bookings runs on the save path", cpc.check_bookings in cpc.PLAN_CHECKS)

    def run(plan: dict) -> list[str]:
        errors: list[str] = []
        cpc.check_bookings(plan, errors, [])
        return errors

    check("a valid block raises nothing", not run(with_records(SELF_DRIVE, booked("gt-lner"))))
    check("absent_block_is_quiet (gate)", not run(SELF_DRIVE))
    dangling = run(with_records(SELF_DRIVE, booked("gone-1")))
    check("dangling_record (gate)", any("gone-1" in e for e in dangling), dangling)
    check("every finding names its reference", all("replanning.md#bookings" in e for e in dangling), dangling)

    # A hotel switch re-points the days' id; the check-in line, the route stops and the next day's
    # check-out still name the hotel the traveller did not take, and the page navigates them there.
    switched = with_records(SELF_DRIVE, {"option_id": "acc-pit-2", "state": "chosen"})
    for day in switched["days"]:
        if day.get("accommodation_option_id") == "acc-pit-1":
            day["accommodation_option_id"] = "acc-pit-2"
    stale = run(switched)
    check("stale_stay_names: each day still naming the untaken hotel is named, with its fields",
          any("day 1" in e and "Atholl Palace Hotel" in e and "days[0].route.end" in e
              and "Pitlochry Hydro Hotel" in e for e in stale)
          and any("day 3" in e and "days[2].activities[0].name" in e for e in stale), stale)
    renamed = copy.deepcopy(switched)
    renamed["days"] = json.loads(json.dumps(renamed["days"]).replace("Atholl Palace Hotel", "Pitlochry Hydro Hotel"))
    check("stale_stay_names: quiet once the days name the recorded stay", not run(renamed), run(renamed))
    encoded = copy.deepcopy(renamed)
    encoded["days"][1]["route"]["maps_url"] = "https://www.google.com/maps/dir/?api=1&destination=Atholl+Palace+Hotel"
    check("stale_stay_names: a URL-encoded name counts", any("days[1].route.maps_url" in e for e in run(encoded)),
          run(encoded))
    contained = copy.deepcopy(renamed)
    contained["booking_options"]["accommodations"][0]["property_name"] = "Pitlochry Hydro"
    check("stale_stay_names: a sibling name inside the recorded name is not a mention", not run(contained),
          run(contained))
    undecided = copy.deepcopy(switched)
    undecided["bookings"] = []
    check("stale_stay_names: no record, no finding (plans saved before bookings are unchanged)",
          not run(undecided), run(undecided))


def main() -> int:
    rules_cases()
    verification_cases()
    gate_cases()
    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("booking cases passed")
    return 0


def test_bookings() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
