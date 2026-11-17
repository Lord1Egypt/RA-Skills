#!/usr/bin/env python3
"""Regression tests for scripts/replan_trip.py, driven entirely through the command line.

A date change is the one edit that invalidates researched facts without touching them. Almost
everything under a day is keyed to a WEEKDAY rather than to a date -- opening hours, closure days,
market days, Sunday retail law, a museum that shuts Mondays -- so moving the window by a single day
turns all of it into a guess while the plan still looks complete and still passes every gate. The
measured run that prompted this script did the shift by hand, redid the weekday map from memory,
and introduced an off-by-one in every ticket and every anchor day index.

So the contract has two halves and both are tested here: the script rewrites exactly what a shift
determines (trip and day dates, accommodation windows, dated booking fields, ticket day links) and
rewrites NOTHING else -- prose above all, because "Saturday is the only full shopping day" becomes
false when the dates move and editing the weekday token inside it turns a stale sentence into a
confident lie. Everything it cannot recompute lands in replan_context.must_reverify, where
check_plan_consistency.py refuses the plan until a human resolves each entry.

Every case runs the script as a subprocess. Nothing here imports it, so the tests state the
contract an operator sees and stay true across any rewrite of its internals.

Run:  python tests/test_replan_trip.py
      python -m pytest tests/test_replan_trip.py
"""

from __future__ import annotations

import copy
import datetime
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPLAN = ROOT / "scripts" / "replan_trip.py"
CHECKER = ROOT / "scripts" / "check_plan_consistency.py"
FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"

# The fixture's single day is Monday 2026-09-28. Shifts below are chosen against that: +1 lands on
# a Tuesday, +5 on a Saturday. Stated once here because a case that silently stops crossing a
# weekday boundary still passes while testing nothing.
FIXTURE_START = "2026-09-28"
# replan_trip.py refuses a window that starts before today, and the fixture's dates are fixed, so
# without a pinned today every case here starts failing the day the calendar passes the fixture --
# which is what happened on 2026-10-09, with CI last green two weeks earlier. Every call gets this
# date unless the case passes its own --today.
PINNED_TODAY = "2026-09-01"


def run_cli(args: list[str]) -> tuple[int, str]:
    if "--today" not in args:
        args = [*args, "--today", PINNED_TODAY]
    proc = subprocess.run([sys.executable, str(REPLAN), *args], capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def run_replan(plan: object, *args: str) -> tuple[int, str, dict | None]:
    """Shift `plan` and return (exit code, output, parsed result or None if nothing was written)."""
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "plan.json"
        source.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        target = Path(tmp) / "shifted.json"
        code, out = run_cli([str(source), *args, "--out", str(target)])
        shifted: dict | None = None
        if target.exists():
            try:
                shifted = json.loads(target.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                shifted = None
    return code, out, shifted


def multi_day(base: dict, count: int) -> dict:
    """The fixture stretched to `count` identical days, so "every days[].date moved" means something.

    A one-day plan cannot tell a script that shifts the whole array from one that shifts days[0]
    and forgets the loop -- which is exactly the off-by-one class this script exists to remove.
    """
    plan = copy.deepcopy(base)
    template = plan["days"][0]
    start = datetime.date.fromisoformat(plan["trip"]["start_date"])
    plan["days"] = []
    for offset in range(count):
        this_day = copy.deepcopy(template)
        this_day["number"] = offset + 1
        this_day["date"] = (start + datetime.timedelta(days=offset)).isoformat()
        plan["days"].append(this_day)
    plan["trip"]["end_date"] = (start + datetime.timedelta(days=count - 1)).isoformat()
    check_out = (start + datetime.timedelta(days=count)).isoformat()
    for stay in plan["booking_options"]["accommodations"]:
        old_check_out = stay["check_out"]
        stay["check_out"] = check_out
        # The comparison-search URL carries the same window as the stay, so it has to move with it.
        # Feeding the script a plan whose own booking link already disagreed with its own stay
        # would make any later mismatch unattributable -- ours or the script's.
        for search in stay.get("comparison_searches", []):
            search["search_url"] = search["search_url"].replace(old_check_out, check_out)
    return plan


def plus(date: str, days: int) -> str:
    return (datetime.date.fromisoformat(date) + datetime.timedelta(days=days)).isoformat()


def entries(shifted: dict | None) -> list[dict]:
    context = (shifted or {}).get("replan_context")
    raw = context.get("must_reverify") if isinstance(context, dict) else None
    return [e for e in raw if isinstance(e, dict)] if isinstance(raw, list) else []


def cites(shifted: dict | None, needle: str) -> list[dict]:
    """must_reverify entries whose path mentions `needle`.

    Substring rather than equality on purpose: the contract fixes which FACT has to be flagged,
    not whether the script points at the card or at the field inside it, and a test that pins the
    latter fails a correct implementation for a spelling.
    """
    return [e for e in entries(shifted) if needle in str(e.get("path") or "")]


def names(shifted: dict | None, needle: str) -> list[dict]:
    """must_reverify entries that name `needle` in either the path or the reason.

    Grouping is a real design choice, not a spelling: one entry per prose field and one entry per
    day that carries several are both defensible, and the second names its fields inside the
    reason. What the contract actually requires is that the operator who has to re-read a sentence
    can find WHICH sentence without re-reading the plan, and both shapes deliver that.
    """
    return [e for e in entries(shifted)
            if needle in str(e.get("path") or "") or needle in str(e.get("reason") or "")]


def check_plan(plan: dict) -> tuple[int, str]:
    # --no-verification-yet, and not because the flag is decoration: check_plan_consistency.py now
    # refuses a bare invocation, since `--verification` defaulting to None meant the report checks
    # were reachable only from an undocumented invocation and ran nowhere on the documented one.
    # Every case in this file is about what replan_trip.py did to the plan JSON, never about a
    # verification report -- a shifted plan has none by definition, because replan_trip.py clears
    # verification_status precisely so a plan whose dates moved cannot claim it was verified on
    # them. So the waiver is the honest argv here. Without it every case below would exit 1 on the
    # missing flag and the assertions on WHY the plan failed would pass or fail for the wrong
    # reason.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "plan.json"
        path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(CHECKER), str(path), "--no-verification-yet"],
                              capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def main() -> int:
    if not REPLAN.exists():
        # Skipped rather than failed, and only because the absence is already loud somewhere else:
        # SKILL.md names `python scripts/replan_trip.py`, and test_packaging.py fails on any
        # SKILL.md reference that does not exist. Duplicating that failure here would report one
        # missing file twice and teach the next reader to ignore this suite. If that packaging
        # check is ever removed, this branch has to become a failure the same day.
        print(f"SKIPPED: {REPLAN.relative_to(ROOT)} does not exist yet, so none of the replan "
              f"cases ran. test_packaging.py fails on the same absence -- fix it there.",
              file=sys.stderr)
        return 0

    base = json.loads(FIXTURE.read_text(encoding="utf-8"))
    failures: list[str] = []

    if base["trip"]["start_date"] != FIXTURE_START:
        failures.append(
            f"the fixture now starts {base['trip']['start_date']}, not {FIXTURE_START}. Every "
            f"shift below was chosen to cross a weekday boundary from a Monday; recompute them "
            f"or the cases stop testing the weekday problem they were written for.")

    def fail(name: str, detail: str) -> None:
        failures.append(f"{name}: {detail}")

    # 1. The arithmetic half. A shift moves the trip window and every day inside it, and adds no
    # days and drops none -- the hand edit that prompted this script renumbered days as it went.
    code, out, shifted = run_replan(multi_day(base, 3), "--shift-days", "1")
    if code != 0 or shifted is None:
        fail("+1 day shift", f"expected a written plan and exit 0, got exit {code}\n{out}")
    else:
        expected_days = [plus(FIXTURE_START, offset + 1) for offset in range(3)]
        actual_days = [d.get("date") for d in shifted.get("days", [])]
        if actual_days != expected_days:
            fail("+1 day shift", f"days are dated {actual_days}, expected {expected_days}")
        if len(shifted.get("days", [])) != 3:
            fail("+1 day shift", f"day count changed to {len(shifted.get('days', []))}, expected 3")
        window = (shifted.get("trip", {}).get("start_date"), shifted.get("trip", {}).get("end_date"))
        if window != (plus(FIXTURE_START, 1), plus(FIXTURE_START, 3)):
            fail("+1 day shift", f"trip window is {window}, expected "
                                 f"{(plus(FIXTURE_START, 1), plus(FIXTURE_START, 3))}")
        numbers = [d.get("number") for d in shifted.get("days", [])]
        if numbers != [1, 2, 3]:
            fail("+1 day shift", f"day numbers became {numbers}; a shift moves dates, not indexes")

    # The accommodation window is the other half of "what a shift determines", and it is the half
    # that fails quietly: check_plan_consistency.py accepts a day on the checkout date, so a stay
    # whose check_in moved while its check_out stayed put still covers every day of a short trip
    # and passes the gate -- while the traveller holds a booking for the wrong nights. Asserted as
    # a window rather than two dates because both halves must move by the SAME amount: a shift
    # relocates a stay, it never lengthens or shortens one.
    for shift in (1, 5):
        code, out, shifted = run_replan(multi_day(base, 3), "--shift-days", str(shift))
        if code != 0 or shifted is None:
            fail(f"+{shift} day accommodation window",
                 f"expected a written plan and exit 0, got exit {code}\n{out}")
            continue
        for index, stay in enumerate(shifted.get("booking_options", {}).get("accommodations", [])):
            was = base["booking_options"]["accommodations"][index]
            expected = (plus(was["check_in"], shift), plus(plus(FIXTURE_START, 3), shift))
            window = (stay.get("check_in"), stay.get("check_out"))
            if window != expected:
                fail(f"+{shift} day accommodation window",
                     f"stay {stay.get('id')!r} is booked {window[0]}..{window[1]}, expected "
                     f"{expected[0]}..{expected[1]}. Both ends of a stay move with the trip; "
                     f"moving one turns a three-night booking into a different stay, and a large "
                     f"enough shift moves check_in past check_out. Note where check_out sits: it "
                     f"is the morning AFTER the last night, so it is the one traveller date that "
                     f"legitimately falls one day outside the old trip window -- any rule that "
                     f"only moves dates inside that window skips exactly this field.")
            # The same date, in the form the traveller actually clicks. A stay whose record moved
            # while its prefilled search did not sends someone to a booking page for the nights
            # they are not there, and they find out at the payment screen.
            for search in stay.get("comparison_searches", []):
                url = str(search.get("search_url") or "")
                for param, value in (("checkin", expected[0]), ("checkout", expected[1])):
                    if f"{param}={value}" not in url:
                        fail(f"+{shift} day booking link",
                             f"stay {stay.get('id')!r} search URL does not carry "
                             f"{param}={value}: {url}")

    # 2. The half a script cannot do. These hours are published against weekdays, the venue is shut
    # on the new one, and nothing in the plan changed -- which is precisely why the shifted plan
    # still passes every arithmetic check. Monday 2026-09-28 + 5 is a Saturday.
    weekday_keyed = copy.deepcopy(base)
    lunch = weekday_keyed["days"][0]["dining"][0]
    lunch["venue_hours"] = "Mon-Fri 11:00-15:00"
    lunch["hours_status"] = "verified"
    code, out, shifted = run_replan(weekday_keyed, "--shift-days", "5")
    if code != 0 or shifted is None:
        fail("weekday-keyed hours", f"expected a written plan and exit 0, got exit {code}\n{out}")
    else:
        flagged = cites(shifted, "days[0].dining[0]")
        if not flagged:
            fail("weekday-keyed hours",
                 f"'Mon-Fri 11:00-15:00' moved from a Monday to a Saturday and nothing was raised "
                 f"under days[0].dining[0]. must_reverify was "
                 f"{[e.get('path') for e in entries(shifted)]}")
        elif not str(flagged[0].get("reason") or "").strip():
            fail("weekday-keyed hours",
                 "the entry has an empty reason; a path with no reason tells whoever resolves it "
                 "nothing about what to go and look up")
        elif any(e.get("resolved") is True for e in flagged):
            fail("weekday-keyed hours",
                 "the entry was written already resolved, which means the gate never stops on it "
                 "and the whole record is decoration")

    # 3. A plan whose dates moved was never verified on those dates, so the old verdict cannot
    # ride along. The renderer's banner keys off this field, and leaving it at "verified" puts the
    # word on a page whose weekday-keyed facts are now unchecked.
    verified = multi_day(base, 2)
    verified["verification_status"] = "verified"
    verified["verification_report"] = "reports/2026-08-03-fixture-verification.json"
    code, out, shifted = run_replan(verified, "--shift-days", "1")
    if code != 0 or shifted is None:
        fail("verification cleared", f"expected a written plan and exit 0, got exit {code}\n{out}")
    elif shifted.get("verification_status") == "verified":
        fail("verification cleared",
             "verification_status is still 'verified' after the dates moved. Clear it, or set it "
             "to 'unverified' so the page renders the not-fact-checked banner.")

    # 3b. The same argument one field over, and it was missed when 3 was written because this one
    # is not about facts in the world -- it is about checks that ran. `gates_passed` records that
    # the deterministic gates passed, and save_trip_deliverables.py renders it as a visible
    # "Structure checks passed: N" line. Those gates ran on the OLD dates, against the old
    # day-to-weekday mapping, the old accommodation windows and the old ticket day links. Carried
    # forward it produced the worst shape this script can emit: a shifted plan that
    # check_plan_consistency.py REFUSES, rendering a page that tells the traveller two dozen
    # structure checks passed on it. Clearing verification_status did not cover for it -- they are
    # separate claims and the page prints both.
    stamped = multi_day(base, 2)
    stamped["gates_passed"] = {"checks": 24, "checked_by": "check_plan_consistency.PLAN_CHECKS"}
    code, out, shifted = run_replan(stamped, "--shift-days", "1")
    if code != 0 or shifted is None:
        fail("gate stamp cleared", f"expected a written plan and exit 0, got exit {code}\n{out}")
    elif shifted.get("gates_passed"):
        fail("gate stamp cleared",
             f"gates_passed survived the shift as {shifted.get('gates_passed')!r}. The gates it "
             f"records ran on the old calendar, and the page prints it as 'Structure checks "
             f"passed' to the traveller.")

    # 3c. The NEXT block this script prints is a runnable script, not prose, and step 2 stopped
    # being runnable when check_plan_consistency.py made --verification mandatory: a bare call now
    # exits 1 out of argparse having run ZERO checks. Both the old refusal and the new one exit 1,
    # so a caller reading only the exit code could not tell "the gate refused your plan" from "the
    # gate never ran". Pinned by running what it prints.
    code, out, shifted = run_replan(multi_day(base, 2), "--shift-days", "1")
    printed = [line for line in out.splitlines() if "check_plan_consistency.py" in line]
    if not printed:
        fail("NEXT names the consistency gate", f"no step naming it in:\n{out}")
    else:
        step = printed[0]
        if "--no-verification-yet" not in step and "--verification" not in step:
            fail("NEXT step 2 is runnable",
                 f"the printed command is the bare form, which now exits 1 out of argparse "
                 f"without running a single check: {step.strip()}")

    # 4. Prose is never rewritten. This sentence is false the moment the dates move, and the
    # tempting fix -- swap "Monday" for the new weekday -- would turn a sentence a reader can
    # catch into one they cannot, since nothing else in it was re-researched.
    stale = copy.deepcopy(base)
    prose = "Day 1 (2026-09-28) is a Monday, so the guided tour runs as scheduled."
    stale["days"][0]["contingency"] = prose
    code, out, shifted = run_replan(stale, "--shift-days", "5")
    if code != 0 or shifted is None:
        fail("prose untouched", f"expected a written plan and exit 0, got exit {code}\n{out}")
    else:
        got = shifted["days"][0].get("contingency")
        if got != prose:
            fail("prose untouched",
                 f"the contingency sentence was rewritten to {got!r}. A shift may not edit prose: "
                 f"the rest of the sentence was researched for the old date, so patching the "
                 f"weekday inside it produces a confident lie instead of a visible staleness.")
        if not names(shifted, "days[0].contingency"):
            fail("prose untouched",
                 f"the sentence names a weekday and was left alone, correctly, but no "
                 f"must_reverify entry names days[0].contingency in its path or its reason. "
                 f"Leaving prose alone is only half the contract; the other half is saying which "
                 f"sentence went stale, or it ships unread. must_reverify was "
                 f"{[e.get('path') for e in entries(shifted)]}")

    # 5. The success case the four above cannot supply on their own: once a human resolves what the
    # shift raised, the plan the script produced must be shippable. Without this, every case here
    # is satisfied by a script that flags everything and recomputes nothing -- and a replan that
    # raises fifty entries for a one-day move is a replan the next operator does by hand again.
    code, out, shifted = run_replan(multi_day(base, 3), "--shift-days", "1")
    if code != 0 or shifted is None:
        fail("shifted plan is shippable", f"expected a written plan, got exit {code}\n{out}")
    else:
        resolved = copy.deepcopy(shifted)
        for entry in entries(resolved):
            entry["resolved"] = True
            entry["resolution"] = "Rechecked against the new weekday; unchanged."
        gate_code, gate_out = check_plan(resolved)
        if gate_code != 0:
            fail("shifted plan is shippable",
                 f"with every must_reverify entry resolved, check_plan_consistency.py still "
                 f"rejects the shifted plan (exit {gate_code}). The shift left the plan "
                 f"self-contradictory:\n{gate_out}")

    # 6. Bad input produces a message, never a traceback. An operator who gets a stack trace learns
    # nothing about their plan and stops running the tool -- and the tool they stop running is the
    # one standing between a moved date and an unchecked weekday.
    with tempfile.TemporaryDirectory() as tmp:
        out_path = str(Path(tmp) / "out.json")
        not_json = Path(tmp) / "not-a-plan.json"
        not_json.write_text("this is not JSON at all", encoding="utf-8")
        a_list = Path(tmp) / "a-list.json"
        a_list.write_text("[1, 2, 3]", encoding="utf-8")

        bad_inputs = {
            "missing file": [str(Path(tmp) / "no-such-plan.json"), "--shift-days", "1",
                             "--out", out_path],
            "not JSON": [str(not_json), "--shift-days", "1", "--out", out_path],
            "plan is a list": [str(a_list), "--shift-days", "1", "--out", out_path],
            "shift is not a number": [str(FIXTURE), "--shift-days", "tomorrow", "--out", out_path],
        }
        for name, args in bad_inputs.items():
            code, out = run_cli(args)
            if code == 0:
                fail(f"bad input ({name})", f"exited 0 and reported nothing wrong\n{out}")
            if "Traceback" in out:
                fail(f"bad input ({name})", f"raised instead of reporting\n{out[-400:]}")
            if not out.strip():
                fail(f"bad input ({name})",
                     f"exited {code} in silence; the operator is left guessing what to fix")

    # 7. The refusal the pin above steps around still exists. A today after the new window must
    # refuse with the remedy and write nothing; without this, pinning today everywhere would let
    # the past-window guard be deleted with the suite still green.
    code, out, shifted = run_replan(base, "--shift-days", "1", "--today", "2026-12-31")
    if code == 0 or shifted is not None or "before today" not in out:
        fail("a shift into the past is refused",
             f"with --today after the shifted window, exit {code}, wrote "
             f"{'a plan' if shifted is not None else 'nothing'}:\n{out[-400:]}")

    # 8. A booking does not move with the plan. A ticket bought for 28 September is not a ticket for
    # the 29th, and a room paid for two is not a room for three; left alone the shifted page says
    # "Booked" over dates and a party nobody bought for. A chosen record is a decision, not a
    # purchase, and survives -- the option it names is shifted and re-flagged like any other card.
    paid = copy.deepcopy(base)
    paid["bookings"] = [{"option_id": "stay-a", "state": "booked", "booked_on": "2026-08-30",
                         "booked_via": "hotel website", "paid_total": 900, "paid_currency": "CNY"}]
    for label, argv in (("a date shift", ("--shift-days", "1")), ("a party change", ("--travellers", "3"))):
        code, out, shifted = run_replan(paid, *argv)
        flagged = cites(shifted, "bookings[0]")
        if code != 0 or len(flagged) != 1 or "stay-a" not in str(flagged[0].get("reason")) \
                or "record_booking.py" not in str(flagged[0].get("reason")):
            fail(f"a booked record is re-flagged after {label}",
                 f"exit {code}; bookings entries {flagged}\n{out[-400:]}")
    decided = copy.deepcopy(base)
    decided["bookings"] = [{"option_id": "stay-a", "state": "chosen"}]
    code, out, shifted = run_replan(decided, "--shift-days", "1")
    if code != 0 or cites(shifted, "bookings"):
        fail("a chosen record is not a purchase and is not flagged", f"exit {code}; {cites(shifted, 'bookings')}")

    if failures:
        print(f"REPLAN FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all replan regression cases passed")
    return 0


def test_replan_trip_regressions() -> None:
    """Pytest surface: with no test_* function pytest collects nothing from this file and prints
    "no tests ran", which a contributor or CI reads as green -- the same false green the cases
    above exist to stop. Running the file directly is unchanged."""
    if not REPLAN.exists():
        import pytest  # noqa: PLC0415 - only needed on the skip path

        pytest.skip(f"{REPLAN.relative_to(ROOT)} does not exist yet; test_packaging.py fails on "
                    f"the same absence, so this is reported, not swallowed")
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
