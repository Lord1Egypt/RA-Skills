#!/usr/bin/env python3
"""Which time zone each timed thing happens in, and the gate that checks the plan's zones.

Only Apple Calendar shows a zone-less time as written; Outlook converts it to the phone's zone at
import and Google does not support it, so a Tokyo dinner imported in Amsterdam showed at the
Amsterdam hour. The plan now names its zones and the calendar writes UTC from them.
Spec: docs/superpowers/specs/2026-10-11-calendar-fixes-design.md.

Run:  python tests/test_trip_zones.py
      python -m pytest tests/test_trip_zones.py
"""

from __future__ import annotations

import copy
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import trip_zones as tz  # noqa: E402

SELF_DRIVE = json.loads((ROOT / "tests" / "self-drive-fixture.json").read_text(encoding="utf-8"))
BOOKING_READY = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))
UTC = dt.timezone.utc

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def flight(departure: str, arrival: str, minutes: int | None, **zones) -> dict:
    leg = {"service_identifier": "XX1", "departure_local": departure, "arrival_local": arrival, **zones}
    if minutes is not None:
        leg["duration_minutes"] = minutes
    return {"id": "fl-x", "outbound_date": departure[:10] if len(departure) > 5 else "2026-10-17",
            "outbound_itinerary": leg, "return_itinerary": {}}


def with_flight(plan: dict, option: dict, **trip) -> dict:
    """The plan with only this flight: its trains carry no zones of their own, so on a plan naming
    more than one zone they would be findings of their own and blur what each case tests."""
    plan = copy.deepcopy(plan)
    plan["trip"].update(trip)
    plan["booking_options"]["flights"] = [option]
    plan["booking_options"]["ground_transport"] = []
    return plan


def rules_cases() -> None:
    # dst_conversion: Europe/London leaves BST on 2026-10-25.
    check("dst_conversion: before the change is BST",
          tz.to_utc(dt.datetime(2026, 10, 24, 12, 0), "Europe/London") == dt.datetime(2026, 10, 24, 11, 0, tzinfo=UTC))
    check("dst_conversion: after the change is GMT",
          tz.to_utc(dt.datetime(2026, 10, 26, 12, 0), "Europe/London") == dt.datetime(2026, 10, 26, 12, 0, tzinfo=UTC))

    check("a dated value keeps its date", tz.local_moment("2026-11-20 21:55", None) == (dt.datetime(2026, 11, 20, 21, 55), True))
    check("a T-separated value parses", tz.local_moment("2026-11-20T21:55", None) == (dt.datetime(2026, 11, 20, 21, 55), True))
    check("a clock takes the option's date", tz.local_moment("08:00", "2026-10-17") == (dt.datetime(2026, 10, 17, 8, 0), False))
    check("a one-digit hour parses", tz.local_moment("9:30", "2026-10-17") == (dt.datetime(2026, 10, 17, 9, 30), False))
    for bad in ("25:00", "TODO: local time", "", None, "soon"):
        check(f"{bad!r} is no moment", tz.local_moment(bad, "2026-10-17")[0] is None, tz.local_moment(bad, "2026-10-17"))
    check("a clock with no date is no moment", tz.local_moment("08:00", None)[0] is None)

    check("a known zone resolves", tz.zone("Europe/London") is not None)
    for bad in ("GMT+1", "+01:00", "Europe/Atlantis", "../etc/passwd", "", None, 3):
        check(f"{bad!r} is not a zone", tz.zone(bad) is None)

    # Self-drive: London to Scotland, one zone throughout, so its trains need no zones of their own.
    lner = SELF_DRIVE["booking_options"]["ground_transport"][0]
    span = tz.itinerary_span(SELF_DRIVE, lner, "outbound_itinerary", "outbound_date")
    check("a single-zone trip's train resolves from the trip zone",
          span == (dt.datetime(2026, 10, 17, 7, 0, tzinfo=UTC), dt.datetime(2026, 10, 17, 11, 23, tzinfo=UTC)), span)

    # overnight_clock_only: a sleeper written as clocks ends the next morning.
    sleeper = with_flight(SELF_DRIVE, flight("23:10", "07:05", 475))
    option = sleeper["booking_options"]["flights"][0]
    span = tz.itinerary_span(sleeper, option, "outbound_itinerary", "outbound_date")
    check("overnight_clock_only: ends the next morning",
          span and span[1] == dt.datetime(2026, 10, 18, 6, 5, tzinfo=UTC), span)
    check("overnight_clock_only: no duration finding", not tz.zone_problems(sleeper), tz.zone_problems(sleeper))

    # The date line, with real zones: the length comes out right, no patch needed.
    dateline = with_flight(SELF_DRIVE, flight("2026-11-20 19:05", "2026-11-20 07:10", 425,
                                              departure_timezone="Asia/Tokyo", arrival_timezone="Pacific/Honolulu"),
                           origin_timezone="Asia/Tokyo")
    option = dateline["booking_options"]["flights"][0]
    span = tz.itinerary_span(dateline, option, "outbound_itinerary", "outbound_date")
    check("a date-line flight is 425 minutes long", span and (span[1] - span[0]) == dt.timedelta(minutes=425), span)


def gate_cases() -> None:
    check("a single-zone plan with consistent durations is clean", not tz.zone_problems(SELF_DRIVE),
          tz.zone_problems(SELF_DRIVE))
    check("a plan with no zones is untouched", not tz.zone_problems(BOOKING_READY) and not tz.zone_notes(BOOKING_READY),
          (tz.zone_problems(BOOKING_READY), tz.zone_notes(BOOKING_READY)))

    # multi_zone_requires_itinerary_zones: Amsterdam -> Edinburgh, as Kiwi writes it.
    kiwi = flight("2026-11-20 21:55", "2026-11-20 22:25", 90)
    international = with_flight(SELF_DRIVE, kiwi, origin_timezone="Europe/Amsterdam")
    problems = tz.zone_problems(international)
    check("multi_zone_requires_itinerary_zones: named with both fields",
          any("booking_options.flights[0].outbound_itinerary" in p and "departure_timezone and arrival_timezone" in p
              for p in problems), problems)
    right = with_flight(SELF_DRIVE, flight("2026-11-20 21:55", "2026-11-20 22:25", 90,
                                           departure_timezone="Europe/Amsterdam", arrival_timezone="Europe/London"),
                        origin_timezone="Europe/Amsterdam")
    check("the right zones are quiet", not tz.zone_problems(right), tz.zone_problems(right))
    wrong = with_flight(SELF_DRIVE, flight("2026-11-20 21:55", "2026-11-20 22:25", 90,
                                           departure_timezone="Europe/London", arrival_timezone="Europe/London"),
                        origin_timezone="Europe/Amsterdam")
    problems = tz.zone_problems(wrong)
    check("a wrong zone is caught by the duration",
          any("flights[0].outbound_itinerary" in p and "30 minutes" in p and "duration_minutes is 90" in p for p in problems),
          problems)

    invalid = copy.deepcopy(SELF_DRIVE)
    invalid["trip"]["timezone"] = "GMT+1"
    check("an unknown zone name is refused", any(p.startswith("trip.timezone") for p in tz.zone_problems(invalid)),
          tz.zone_problems(invalid))
    placeholder = copy.deepcopy(SELF_DRIVE)
    placeholder["trip"]["timezone"] = "TODO: IANA time zone of the destination"
    problems = tz.zone_problems(placeholder)
    check("a TODO zone is refused here: the page never prints a zone, so no other gate sees it",
          any("trip.timezone" in p and "TODO" in p for p in problems), problems)

    real_known = tz._known
    tz._known = lambda: frozenset()
    try:
        check("no tz database: nothing refused", not tz.zone_problems(wrong), tz.zone_problems(wrong))
        check("no tz database: a note says so", tz.zone_notes(wrong), tz.zone_notes(wrong))
        check("no tz database: no zone resolves, so the calendar is floating as the note says",
              tz.zone("Europe/London") is None)
    finally:
        tz._known = real_known

    import check_plan_consistency as cpc  # noqa: PLC0415
    check("check_time_zones runs on the save path", cpc.check_time_zones in cpc.PLAN_CHECKS)
    errors: list[str] = []
    cpc.check_time_zones(wrong, errors, [])
    check("findings cite the calendar reference", errors and all("booking-html-output.md#calendar" in e for e in errors), errors)


def skeleton_cases() -> None:
    scaffold = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "new_plan_skeleton.py"),
         "--start", "2027-05-07", "--end", "2027-05-10", "--origin", "Amsterdam", "--destination", "Bern",
         "--intake-method", "user_supplied", "--source-note", "scaffold check"],
        capture_output=True, text=True)
    check("the scaffold runs", scaffold.returncode == 0, scaffold.stderr[-300:])
    if scaffold.returncode == 0:
        skeleton = json.loads(scaffold.stdout)
        trip = skeleton["trip"]
        check("the scaffold asks for both trip zones",
              str(trip.get("timezone")).startswith("TODO:") and str(trip.get("origin_timezone")).startswith("TODO:"), trip)
        problems = tz.zone_problems(skeleton)
        check("and the save path refuses it until both are filled",
              any("trip.timezone" in p and "trip.origin_timezone" in p for p in problems), problems)


def main() -> int:
    rules_cases()
    gate_cases()
    skeleton_cases()
    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("time-zone cases passed")
    return 0


def test_trip_zones() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
