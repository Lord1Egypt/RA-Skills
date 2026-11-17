#!/usr/bin/env python3
"""Regression tests for trips that sleep in more than one place.

Everything a multi-stop trip needs was already in the contract -- one `stay_group_id` per stop,
`origin_station`/`destination_station`/`outbound_date` on the intercity leg, a `transfer` day type,
and a day route that carries the physical move. A delivered plan in the author's workspace already
used all of it (Shekou 2 nights, then Dapeng 1 night, with a 76 km ride between them). Two things
were missing, and this file pins both.

**The page never said any of it.** The header renders `origin -> destination` from a single string,
so a reader had to infer from four day cards that the trip moved. The spine is derived from the
stay groups rather than declared, because a declaration is a second copy to drift against the
first -- and `base_location` is deliberately not its source: it is free text, and was found meaning
"where today's activities are" on one plan (four spellings, one hotel) and "where I sleep" on
another.

**"Two comparable candidates" counted across journeys.** Beijing->Shanghai and Shanghai->Beijing
are two items, so the count passed, the review_urls differed so the uniqueness check passed, and
NEITHER leg had been compared against anything. The more legs a trip has, the more confidently the
gate reports a comparison nobody made. Verified against the pre-change renderer before it was
fixed, not assumed.

Run:  python tests/test_multi_stop.py
      python -m pytest tests/test_multi_stop.py
"""

from __future__ import annotations

import copy
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_plan_consistency import check_stay_groups_do_not_overlap  # noqa: E402
from plan_flags import stay_sequence  # noqa: E402
import render_final_trip_html as renderer  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"


def a_stay(group: str, check_in: str, check_out: str, location: str, option: int) -> dict:
    return {"id": f"{group}-{option}", "stay_group_id": group, "stay_location": location,
            "check_in": check_in, "check_out": check_out}


def a_leg(index: int, origin: str, destination: str, date: str,
          group: str | None = None, url: str | None = None) -> dict:
    return {"id": f"g-{index}", "leg_group_id": group, "provider": "operator",
            "review_url": url or f"https://example.invalid/leg{index}",
            "origin_station": origin, "destination_station": destination,
            "outbound_date": date, "single_option_reason": None}


def real_workspace() -> Path | None:
    """The user's own Travel Buddy workspace, ONLY when they have opted in.

    Running a real artifact through the checker is worth more than a fixture -- a fixture is
    written beside the checker and agrees with it by construction, and it was the real workspace
    that turned up eight field names nothing reads. But this suite ships with the skill, so on
    anybody else's machine "read every plan in ~/Travel Buddy" means reading their travel history,
    their hotel bookings and their dates, and printing filenames that carry destinations. That is
    not a trade a test gets to make on the reader's behalf.

    So it is opt-in and says so when it declines, because a silent skip is how a suite goes green
    while testing less than the reader thinks. Set TRAVEL_BUDDY_TEST_WORKSPACE=1 to use the default
    workspace, or to a path to use that one.
    """
    choice = os.environ.get("TRAVEL_BUDDY_TEST_WORKSPACE", "").strip()
    if not choice:
        print("note: real-workspace cases SKIPPED. They read plans under ~/Travel Buddy, which is "
              "the reader's own travel data; set TRAVEL_BUDDY_TEST_WORKSPACE=1 (or to a path) to "
              "run them.", file=sys.stderr)
        return None
    root = Path.home() / "Travel Buddy" if choice in ("1", "true", "yes") else Path(choice).expanduser()
    return root if root.is_dir() else None


def main() -> int:
    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{label}{': ' + detail if detail else ''}")

    # 1. The spine is DERIVED, and it is empty for a trip that never moves. A one-item spine on a
    #    single-base page would be furniture -- a section that says nothing the header did not.
    plan = {"booking_options": {"accommodations": [
        a_stay("only", "2027-04-17", "2027-04-23", "尖沙咀", 1),
        a_stay("only", "2027-04-17", "2027-04-23", "尖沙咀（九龍）", 2)]}}
    check("a single-base trip has no spine", stay_sequence(plan) == [], f"{stay_sequence(plan)}")

    two = {"booking_options": {"accommodations": [
        a_stay("b", "2026-10-27", "2026-10-28", "深圳大鹏新区", 1),
        a_stay("a", "2026-10-25", "2026-10-27", "深圳南山区蛇口", 1),
        a_stay("a", "2026-10-25", "2026-10-27", "深圳南山区蛇口·海上世界", 2)]}}
    spine = stay_sequence(two)
    check("two stay groups make a two-stop spine", len(spine) == 2, f"{spine}")
    if len(spine) == 2:
        # Ordered by date, not by the order the options happen to sit in the array.
        check("the spine is in travel order",
              [s["group_id"] for s in spine] == ["a", "b"], f"{[s['group_id'] for s in spine]}")
        check("nights are counted, not asserted",
              [s["nights"] for s in spine] == [2, 1], f"{[s['nights'] for s in spine]}")
        # Two hotels in one place are routinely described at different precisions; the shared
        # place is the shorter label, not one property's address.
        check("the shared place wins over one property's address",
              spine[0]["label"] == "深圳南山区蛇口", spine[0]["label"])

    # 2. base_location must NOT be the source. Four spellings of one hotel would otherwise render
    #    a four-stop trip for a traveller who never packed a bag.
    larnaca = {"booking_options": {"accommodations": [
        a_stay("one", "2026-11-16", "2026-11-21", "拉纳卡老城", 1),
        a_stay("one", "2026-11-16", "2026-11-21", "拉纳卡海滨", 2)]},
        "days": [{"base_location": x} for x in
                 ["拉纳卡老城／芬尼库德斯一带", "拉纳卡老城", "拉纳卡城西", "拉纳卡海滨"]]}
    check("four base_location spellings do not invent four stops",
          stay_sequence(larnaca) == [], f"{stay_sequence(larnaca)}")

    # 3. Stay groups may not claim the same night. Every per-day check passes here -- each day
    #    points at one accommodation whose window really does cover it -- so only the PAIR is
    #    wrong, and until a trip has two groups there is no pair to look at.
    tiling = {"booking_options": {"accommodations": [
        a_stay("a", "2026-10-25", "2026-10-27", "蛇口", 1),
        a_stay("b", "2026-10-27", "2026-10-28", "大鹏", 1)]}}
    errors: list[str] = []
    check_stay_groups_do_not_overlap(tiling, errors, [])
    check("a checkout that equals the next check-in is the correct shape", not errors, f"{errors}")

    overlapping = copy.deepcopy(tiling)
    overlapping["booking_options"]["accommodations"][1]["check_in"] = "2026-10-26"
    errors = []
    check_stay_groups_do_not_overlap(overlapping, errors, [])
    check("two hotels on one night is refused", len(errors) == 1, f"{errors}")
    if errors:
        check("the refusal counts the nights paid twice", "1 night" in errors[0], errors[0])

    # A non-ISO window is another check's finding; this one must not crash or double-report.
    broken = copy.deepcopy(tiling)
    broken["booking_options"]["accommodations"][0]["check_out"] = "not a date"
    errors = []
    check_stay_groups_do_not_overlap(broken, errors, [])
    check("a malformed window is left to the check that owns it", not errors, f"{errors}")

    # 4. THE COMPARISON RULE, which is the defect with the widest blast radius: it counted across
    #    journeys, so the more legs a trip had the more confidently it reported a comparison
    #    nobody made.
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def ground_findings(items: list[dict]) -> list[str]:
        candidate = copy.deepcopy(fixture)
        candidate.setdefault("booking_options", {})["ground_transport"] = items
        found = renderer.validate_plan(candidate)
        return [e for e in found if "leg" in e.lower() or "comparable" in e.lower()]

    two_legs = [a_leg(1, "北京南", "上海虹桥", "2026-10-26"),
                a_leg(2, "上海虹桥", "北京南", "2026-10-28")]
    found = ground_findings(two_legs)
    check("two ungrouped journeys are not accepted as one comparison", found,
          "accepted; every extra leg makes the false comparison more confident")
    if found:
        check("the refusal names the fix", "leg_group_id" in found[0], found[0])

    grouped_but_alone = [a_leg(1, "北京南", "上海虹桥", "2026-10-26", "out"),
                         a_leg(2, "上海虹桥", "北京南", "2026-10-28", "back")]
    found = ground_findings(grouped_but_alone)
    check("a grouped leg with one option still owes a comparison", found, "accepted")

    real_pair = [a_leg(1, "北京南", "上海虹桥", "2026-10-26", "out"),
                 a_leg(2, "北京南", "上海虹桥", "2026-10-26", "out",
                       "https://example.invalid/other")]
    check("two genuine options for one journey pass", not ground_findings(real_pair),
          f"{ground_findings(real_pair)}")

    # Two options for one journey may legitimately leave from different stations, which is why
    # legs are grouped by an explicit id and never derived from the endpoints.
    split_stations = [a_leg(1, "北京南", "上海虹桥", "2026-10-26", "out"),
                      a_leg(2, "北京", "上海", "2026-10-26", "out",
                            "https://example.invalid/other")]
    check("one journey compared from two stations is not split into two legs",
          not ground_findings(split_stations), f"{ground_findings(split_stations)}")

    # A single leg needs no new field at all, which is what keeps this free for every trip that
    # does not move.
    single = [a_leg(1, "北京南", "上海虹桥", "2026-10-26", None),
              a_leg(2, "北京南", "上海虹桥", "2026-10-26", None,
                    "https://example.invalid/other")]
    check("a single-leg trip needs no leg_group_id", not ground_findings(single),
          f"{ground_findings(single)}")

    # 4b. A trip that enters two places needs two entry answers. entry_context is ONE object --
    #     one status, one summary, one source_url -- and every gate was satisfied by it, so a
    #     Bangkok/Hanoi/Phnom Penh trip could carry Thailand's answer alone, cite an official Thai
    #     source, pass, and print "visa-free" on a page wrong for two of three countries. A wrong
    #     entry answer is the one finding here the traveller cannot recover from at the airport.
    from check_plan_consistency import check_entry_covers_every_jurisdiction as entry_gate

    def stay(group: str, where: str) -> dict:
        return {"stay_group_id": group, "jurisdiction": where,
                "check_in": "2027-03-01", "check_out": "2027-03-04"}

    def entry_findings(stays: list[dict], context: dict) -> list[str]:
        found: list[str] = []
        entry_gate({"booking_options": {"accommodations": stays},
                    "entry_context": context}, found, [])
        return found

    complete = {"status": "visa_free", "summary": "s", "traveler_basis": "b",
                "source_url": "https://example.invalid", "checked_at": "2027-01-01"}
    # One jurisdiction keeps the flat form exactly as it was; nothing that ships changes shape.
    check("a single-jurisdiction trip is untouched",
          not entry_findings([stay("s1", "日本"), stay("s1", "日本")], complete))

    # Two stops that do not say where they are cannot be checked at all, and silence is the state
    # every plan in the workspace was already in -- so it has to be said, not assumed benign.
    found = entry_findings([stay("s1", ""), stay("s2", "")], complete)
    check("two stops with no jurisdiction are refused", found, "accepted")
    if found:
        check("the refusal says what to write", "jurisdiction" in found[0], found[0][:120])

    three = [stay("s1", "泰国"), stay("s2", "越南"), stay("s3", "柬埔寨")]
    found = entry_findings(three, complete)
    check("three countries answered once is refused", found, "accepted -- wrong about two of three")
    if found:
        for country in ("泰国", "越南", "柬埔寨"):
            check(f"the refusal names {country}", country in found[0], found[0][:160])

    partial = dict(complete, per_jurisdiction=[
        dict(complete, jurisdiction="泰国"), dict(complete, jurisdiction="越南")])
    check("answering two of three is still refused", entry_findings(three, partial), "accepted")

    full = dict(complete, per_jurisdiction=[
        dict(complete, jurisdiction=c) for c in ("泰国", "越南", "柬埔寨")])
    check("three answered is accepted", not entry_findings(three, full),
          f"{entry_findings(three, full)}")

    # A record that names a country and cites nothing reads on the page as an answer somebody
    # checked, which is the failure mode the flat form has always been held to.
    thin = dict(complete, per_jurisdiction=[
        dict(complete, jurisdiction="泰国"), dict(complete, jurisdiction="越南"),
        {"jurisdiction": "柬埔寨", "status": "visa_on_arrival"}])
    found = entry_findings(three, thin)
    check("a record with no source is refused", found, "accepted")
    if found:
        check("and it names which one", "柬埔寨" in found[0], found[0][:120])

    # 4b-ii. Degenerate and adversarial inputs these two gates were NOT built on. Every one of
    #        these was found by running them rather than by reading them.
    #
    #        Jurisdiction is free text, and comparing it raw made `Japan` and `japan ` two
    #        jurisdictions -- telling a single-country traveller their trip entered both. That is
    #        the same free-text trap this file warns about for `base_location`, reintroduced in
    #        the field that was added to avoid it.
    for label, first, second in (("case", "Japan", "japan "),
                                 ("full-width space", "日本", "日本\u3000"),
                                 ("surrounding space", " 香港", "香港 ")):
        found = entry_findings([stay("s1", first), stay("s2", second)], complete)
        check(f"one jurisdiction spelled two ways ({label}) is one jurisdiction", not found,
              f"{found[:1]}")
    check("two genuinely different jurisdictions are still two",
          entry_findings([stay("s1", "日本"), stay("s2", "韩国")], complete), "accepted")

    # A spine must never print a negative night count. The window is refused by validate_plan, so
    # this is unreachable in a delivered plan -- but stay_sequence is a plain function and
    # "-3 晚" is not a number any page should be able to show.
    reversed_window = {"booking_options": {"accommodations": [
        dict(a_stay("a", "2027-05-10", "2027-05-07", "X", 1)),
        dict(a_stay("b", "2027-05-10", "2027-05-12", "Y", 1))]}}
    for stop in stay_sequence(reversed_window):
        if stop["nights"] < 0:
            failures.append(f"a reversed window produced {stop['nights']} nights -- the spine has "
                            f"to skip a malformed window, not print a negative number")

    # Shapes that must not raise. A traceback names a Python type where the answer should name the
    # field that was wrong.
    for label, plan_shape in (("an empty plan", {}),
                              ("a non-dict", "nope"),
                              ("accommodations as a string", {"booking_options": {"accommodations": "x"}}),
                              ("options with no dates", {"booking_options": {"accommodations": [
                                  {"stay_group_id": "a"}, {"stay_group_id": "b"}]}})):
        try:
            stay_sequence(plan_shape)
        except Exception as exc:  # noqa: BLE001 - any raise is the failure
            failures.append(f"stay_sequence raised on {label}: {type(exc).__name__}: {exc}")

    # 4c. The service market is per DAY, not per page. The rule read one page-wide flag, so a
    #     Shenzhen+Hong Kong plan was told its Hong Kong days must use Amap -- not the tool for
    #     Hong Kong transit -- and the only ways out were wrong links for half the trip or no page.
    from plan_flags import is_mainland_market
    for value, expected in (("mainland_china", True), ("中国大陆", True), ("MAINLAND_CHINA", True),
                            ("香港", False), ("japan", False), ("", False), (None, False)):
        check(f"is_mainland_market({value!r}) is {expected}",
              is_mainland_market(value) is expected)

    # 5. The page. A rendered spine is the whole point: the derivation existing and never reaching
    #    the HTML is the same defect as a rating stored and never printed.
    root = real_workspace()
    workspace = (root / "plans") if root else Path("/nonexistent")
    multi = workspace / "2026-10-25-深圳-4-天-3-晚-街区漫步-大鹏海岸-齐齐哈尔往返.json"
    if not multi.exists():
        print(f"note: {multi.name} is not in this workspace; the rendered-page cases were skipped",
              file=sys.stderr)
    else:
        with tempfile.TemporaryDirectory() as raw:
            page = Path(raw) / "page.html"
            proc = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "render_final_trip_html.py"),
                 str(multi), str(page)], capture_output=True, text=True)
            check("the multi-stop plan renders", proc.returncode == 0, proc.stderr[-300:])
            if proc.returncode == 0:
                html = page.read_text(encoding="utf-8")
                block = re.search(r'<section id="trip-spine".*?</section>', html, re.S)
                check("the page carries a spine", block is not None,
                      "derived and never rendered is the same as never derived")
                if block:
                    text = re.sub(r"<[^>]+>", " ", block.group(0))
                    for wanted in ("蛇口", "大鹏", "转场日", "住宿主线"):
                        # The detail is deliberately a length, not the text: this runs against the
                        # reader's own plan, and a failure message that quotes the page would print
                        # their itinerary into a terminal or a CI log.
                        check(f"the spine says {wanted}", wanted in text,
                              f"not found in a {len(text)}-character spine")
                    # The renderer's own English on a Chinese page is a failure the page gate
                    # names in as many words; the spine must not reintroduce it.
                    leaked = [w for w in ("night(s)", "Where you sleep", "Move day") if w in text]
                    check("no renderer English survives on a Chinese page", not leaked, f"{leaked}")

            single_base = workspace / "2027-04-17-香港六日-尖沙咀为基地的海岸-市场与街区.json"
            if single_base.exists():
                flat = Path(raw) / "single.html"
                proc = subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / "render_final_trip_html.py"),
                     str(single_base), str(flat)], capture_output=True, text=True)
                if proc.returncode == 0:
                    check("a single-base page grows no spine",
                          'id="trip-spine"' not in flat.read_text(encoding="utf-8"),
                          "a one-stop spine is furniture")

    if failures:
        print(f"MULTI-STOP FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all multi-stop cases passed")
    return 0


def test_multi_stop() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
