#!/usr/bin/env python3
"""Regression tests for scripts/check_plan_contract.py.

WHAT IS BEING PROTECTED. This script exists because thirteen field-name mistakes in one real
Construction run cost thirteen serial round trips to the gates. Its whole value is that the
thirteen arrive together, so the property under test is not "it finds a typo" but **it finds ALL
of them in one pass** -- a version that reports the first and stops would pass a naive test and
restore the exact cost it was written to remove.

The second property is the one that makes it safe to run at all. SKILL.md's own rule: an error
that sends the author hunting for a problem that does not exist is worse than no error, because it
costs a round trip and teaches distrust of the gate. So a plan that passes the real gates must
report nothing, and that is asserted against the delivered plan rather than a fixture, because a
fixture is written by the same hand as the checker and agrees with it by construction.

Both of this script's own false-positive classes are pinned below. They were not hypothetical: the
first version reported 69 issues where there were 15, and told the author that `amount_low` meant
`note`.

Run:  python tests/test_plan_contract.py
      python -m pytest tests/test_plan_contract.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
SCRIPT = ROOT / "scripts" / "check_plan_contract.py"
CONTRACT = ROOT / "templates" / "final-trip-plan.json"


def run(plan: dict) -> tuple[int, dict]:
    with tempfile.TemporaryDirectory() as raw:
        path = Path(raw) / "plan.json"
        path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(SCRIPT), str(path), "--json"],
                              capture_output=True, text=True)
    try:
        return proc.returncode, json.loads(proc.stdout)
    except ValueError:
        return proc.returncode, {"_stdout": proc.stdout, "_stderr": proc.stderr}


def paths(report: dict) -> set[str]:
    return {i["path"] for i in report.get("issues", [])}


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

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    # 1. The contract itself is a plan the contract knows. If the template cannot pass this, the
    #    checker is measuring something other than the contract -- and every author who starts
    #    from the template, as SKILL.md tells them to, would begin with a screen of errors.
    code, report = run({k: v for k, v in contract.items() if k != "_contract"})
    check("the template passes its own checker", code == 0, json.dumps(report, ensure_ascii=False)[:600])

    # 2. THE PROPERTY THAT IS THE WHOLE POINT: many mistakes, one pass. These are the thirteen
    #    real ones from the measured run, in the six regions of the document they actually
    #    occurred in -- so a checker that stops at the first bad region fails here.
    plan = json.loads(CONTRACT.read_text(encoding="utf-8"))
    plan.pop("_contract", None)
    plan["days"] = [{"route": {"total_duration_minutes": 40, "total_distance_km": 2.0},
                     "dining": [{"price_per_person": 90, "reservation_note": "x",
                                 "backup_venue": "y"}]}]
    plan["budget"]["breakdown"] = [{"amount_low": 100, "price_checked_at": "2026-01-01"}]
    plan["budget"]["total_low"] = 900
    plan["booking_options"]["accommodations"] = [
        {"comparison_searches": [{"url": "https://x", "provider": "p"}]}]
    plan["destination_experience_anchors"] = [{"day_number": 2}]
    plan["regional_service_context"]["checked_alternatives"] = []
    expected = {
        "days[].route.total_duration_minutes", "days[].route.total_distance_km",
        "days[].dining[].price_per_person", "days[].dining[].reservation_note",
        "days[].dining[].backup_venue", "budget.breakdown[].amount_low",
        "budget.breakdown[].price_checked_at", "budget.total_low",
        "booking_options.accommodations[].comparison_searches[].url",
        "booking_options.accommodations[].comparison_searches[].provider",
        "destination_experience_anchors[].day_number",
        "regional_service_context.checked_alternatives",
    }
    code, report = run(plan)
    check("a plan with mistakes exits non-zero", code == 1, f"exit {code}")
    missing = expected - paths(report)
    check("every mistake is reported in ONE pass", not missing,
          f"{len(missing)} of {len(expected)} went unreported: {sorted(missing)}")

    # 3. The suggestion is the difference between a fix and a search, and it must be matched on the
    #    LEAF name. Comparing whole dotted paths scores every sibling alike -- that is how the
    #    first version told the author `budget.breakdown[].amount_low` meant `note`.
    hints = {i["path"]: i.get("suggestion") for i in report.get("issues", [])}
    for wrong, right in (("days[].route.total_duration_minutes", "days[].route.duration_minutes"),
                         ("days[].dining[].price_per_person", "days[].dining[].price_per_person_low"),
                         ("budget.breakdown[].amount_low", "budget.breakdown[].per_person_low"),
                         ("budget.breakdown[].price_checked_at", "budget.breakdown[].checked_at")):
        check(f"{wrong.rsplit('.', 1)[-1]} is pointed at its real name",
              hints.get(wrong) == right, f"suggested {hints.get(wrong)!r}, wanted {right!r}")

    # 4. FALSE-POSITIVE CLASS ONE: an empty array in the contract carries no specimen, so it says
    #    the key exists and nothing about what goes in it. The first version reported every
    #    correctly-written field inside `avoid_list_handling` and `unmet_preferences` as a typo.
    plan = json.loads(CONTRACT.read_text(encoding="utf-8"))
    plan.pop("_contract", None)
    plan["trip"]["traveler_preferences"]["avoid_list_handling"] = [
        {"item": "海鲜", "how_avoided": "全部餐厅改为非海鲜"}]
    plan["trip"]["traveler_preferences"]["unmet_preferences"] = [
        {"preference": "夜游", "reason": "闭园"}]
    code, report = run(plan)
    check("fields inside a contract-empty array are not called typos", code == 0,
          f"exit {code}: {sorted(paths(report))}")

    # 5. FALSE-POSITIVE CLASS TWO: one mistake, one line. Repeating it per array element is the
    #    repeated-text waste the plan gate was already taught not to produce -- six days turned
    #    fifteen problems into sixty-nine lines, and a worklist nobody reads is not a worklist.
    plan = json.loads(CONTRACT.read_text(encoding="utf-8"))
    plan.pop("_contract", None)
    plan["days"] = [{"route": {"total_duration_minutes": 10}} for _ in range(6)]
    code, report = run(plan)
    reported = [i["path"] for i in report["issues"]]
    check("one mistake across six days is one line",
          reported.count("days[].route.total_duration_minutes") == 1, f"{reported}")

    # 6. A type clash, which is the shape that cost the longest round trip: `outbound_itinerary`
    #    written as a sentence where the contract wants an object of six fields. Reported as a
    #    type, not as an unknown key, because "you wrote a string" is the fix.
    plan = json.loads(CONTRACT.read_text(encoding="utf-8"))
    plan.pop("_contract", None)
    plan["booking_options"]["flights"] = [{"outbound_itinerary": "CX270 12:20 → 06:10 直飞"}]
    code, report = run(plan)
    kinds = {i["path"]: i["problem"] for i in report["issues"]}
    check("a string where an object belongs is a type finding",
          kinds.get("booking_options.flights[].outbound_itinerary") == "wrong type", f"{kinds}")

    # 7. `null` is how the contract writes "not filled in yet", so every type is compatible with
    #    it in both directions. A checker that called a filled-in value a clash would fire on
    #    every real plan, since the contract ships almost entirely null.
    plan = json.loads(CONTRACT.read_text(encoding="utf-8"))
    plan.pop("_contract", None)
    plan["trip"]["destination"] = "香港"
    plan["budget"]["cap_per_person"] = None
    code, report = run(plan)
    check("filling a null field is not a type clash", code == 0, f"{sorted(paths(report))}")

    # 8. The keys the skill's own scripts add after the author is done. If these were reported,
    #    every already-delivered plan in a workspace would fail a checker that is supposed to run
    #    before the gates, and the author would be told to delete a stamp they must not touch.
    plan = json.loads(CONTRACT.read_text(encoding="utf-8"))
    plan.pop("_contract", None)
    plan["gates_passed"] = {"checks": 27}
    plan["imagery_sidecar"] = "x-imagery.json"
    plan["replan_context"] = {"reason": "dates moved"}
    code, report = run(plan)
    check("script-written keys are not the author's problem", code == 0,
          f"{sorted(paths(report))}")

    # 9. THE ACCEPTANCE TEST, against real artifacts rather than a fixture: a fixture written
    #    beside the checker agrees with it by construction and proves only that the author was
    #    consistent. Two artifacts are held to zero -- what `new_plan_skeleton.py` emits, because
    #    SKILL.md tells every author to start there and a start that fails its own checker is a
    #    screen of errors before a word is written; and the newest delivered plan, which passed
    #    the real gates.
    skeleton = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "new_plan_skeleton.py"),
         "--start", "2027-05-01", "--end", "2027-05-04", "--origin", "阿姆斯特丹",
         "--destination", "里斯本", "--language", "zh", "--currency", "EUR",
         "--travellers", "2", "--mode", "public-transit", "--stops-per-day", "3"],
        capture_output=True, text=True)
    if skeleton.returncode == 0:
        code, report = run(json.loads(skeleton.stdout))
        check("what the skeleton emits passes the checker", code == 0,
              f"{sorted(paths(report))}")
    else:
        failures.append(f"the skeleton would not run: {skeleton.stderr[-200:]}")

    # Older plans in a real workspace are NOT held to zero, and the reason is worth stating: they
    # were delivered against earlier versions of this template, so failing on them would turn a
    # script regression test into an audit of history that breaks whenever the contract grows.
    # They are still run, and what they report is printed, because that is how this test found the
    # eight silent field-name errors that motivated the note below.
    workspace = real_workspace()
    delivered = [] if workspace is None else [
        p for p in sorted((workspace / "plans").glob("*.json"))
        if not p.name.startswith(("intake-", "next-action-", "shortlist-"))
        and not p.name.endswith("-imagery.json")]
    drift: dict[str, list[str]] = {}
    for real in delivered:
        try:
            body = json.loads(real.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if not isinstance(body, dict) or "days" not in body:
            continue
        _, report = run(body)
        for issue in report.get("issues", []):
            drift.setdefault(issue["path"], []).append(real.name)  # counted, never printed
    if drift:
        # Every one of these is read by no renderer and no gate, which is exactly why it survived
        # delivery: `dietary_needs` where the contract says `dietary_or_religious_needs`, an
        # `excluded_places_checked` written as `true` where a list of the places checked belongs.
        print(f"note: {len(drift)} key(s) in already-delivered plans the contract does not "
              f"declare, none of them fatal and none of them read by anything:", file=sys.stderr)
        for path, where in sorted(drift.items()):
            print(f"      {path}  ({len(where)} plan(s))", file=sys.stderr)  # path only

    # 10. Inputs a caller can really hand over. A traceback names a Python type where the answer
    #     should name the file that was wrong.
    for label, body in (("a bare list", "[]"), ("a string", '"nope"'),
                        ("truncated JSON", '{"days":'), ("an empty file", "")):
        with tempfile.TemporaryDirectory() as raw:
            odd = Path(raw) / "odd.json"
            odd.write_text(body, encoding="utf-8")
            proc = subprocess.run([sys.executable, str(SCRIPT), str(odd)],
                                  capture_output=True, text=True)
        check(f"{label} is refused", proc.returncode == 2, f"exit {proc.returncode}")
        check(f"{label} refuses without a traceback", "Traceback" not in proc.stderr,
              proc.stderr[-200:])


    # --- closed vocabularies -------------------------------------------------------------------
    # The gap this closes, measured on a real Construction run: this script printed CONTRACT OK and
    # the very next command rejected the same file with fourteen findings, every one of them an
    # enum VALUE or a required field rather than a key name. Two "everything at once" passes is the
    # round trip this file exists to delete.
    from check_plan_contract import _vocabularies, enum_issues

    table, failure = _vocabularies()
    check("the vocabularies import from the renderer", not failure, failure)
    check("and there are enough of them to be worth having", len(table) > 20, len(table))

    bad = {"plan_status": "draft",
           "days": [{"day_type": "arrive", "dining": [{"meal": "brunch"}]}],
           "sources": [{"confidence": "very_high"}],
           "booking_options": {"attraction_tickets": [{"ticket_status": "available",
                                                       "price_status": "researched"}]},
           "arrival_essentials": {"payment": {"status": "checked"}}}
    found = {i["path"] for i in enum_issues(bad, table)}
    for path in ("plan_status", "days[].day_type", "days[].dining[].meal", "sources[].confidence",
                 "booking_options.attraction_tickets[].ticket_status",
                 "booking_options.attraction_tickets[].price_status",
                 "arrival_essentials.payment.status"):
        check(f"a wrong value at {path} is reported", path in found, sorted(found))

    # An unhashable value must be a finding, not a crash. `value not in allowed` raises on a list,
    # and a plan carrying `plan_status: ["researched"]` took the whole worklist down with it --
    # the one outcome a pre-gate worklist must never produce, because it then reports none of the
    # twenty other things it had already found.
    for label, value in (("a list", ["researched"]), ("an object", {"a": 1})):
        try:
            crashed = enum_issues({"plan_status": value}, table)
        except Exception as exc:                                    # noqa: BLE001
            failures.append(f"a value that is {label} crashed the checker: {exc!r}")
        else:
            check(f"a value that is {label} is reported", len(crashed), crashed)

    # A null is "not filled in yet", not a wrong value -- calling it one would fire on every
    # skeleton this repository tells authors to start from.
    empty = {"plan_status": None, "days": [{"day_type": None}]}
    check("nulls are not reported as wrong values", not enum_issues(empty, table),
          enum_issues(empty, table))

    good = {"plan_status": "researched", "days": [{"day_type": "full",
                                                   "dining": [{"meal": "lunch"}]}]}
    check("legitimate values pass", not enum_issues(good, table), enum_issues(good, table))

    # The template publishes the same vocabularies for an author to read BEFORE being rejected.
    # Pinned here because a second copy of a list is exactly how this repository's renderer-owned
    # English guard went stale beside the renderer it was meant to mirror.
    import json as _json
    published = _json.loads((ROOT / "templates" / "final-trip-plan.json").read_text(
        encoding="utf-8")).get("_enums", {})
    for path, allowed in table.items():
        check(f"templates/final-trip-plan.json publishes {path}",
              published.get(path) == sorted(allowed),
              f"published {published.get(path)!r}, renderer says {sorted(allowed)!r}")
    extra = {k for k in published if not k.startswith("_")} - set(table)
    check("and publishes nothing the checker does not enforce", not extra, sorted(extra))


    # A failed renderer import must not leave stdout claiming the values were checked. The warning
    # goes to stderr and the verdict goes to stdout, which is what an assistant reads -- so the
    # confident half of that sentence has to disappear with the check it describes.
    import subprocess as _sp, sys as _sys, shutil as _shutil, tempfile as _tf
    with _tf.TemporaryDirectory() as _sandbox:
        broken = Path(_sandbox) / "scripts"
        _shutil.copytree(ROOT / "scripts", broken)
        # The script resolves the contract as SCRIPT_DIR.parent / "templates", so the sandbox
        # needs that too or it fails for the wrong reason and the case proves nothing.
        _shutil.copytree(ROOT / "templates", Path(_sandbox) / "templates")
        target = broken / "render_final_trip_html.py"
        target.write_text("import a_module_that_does_not_exist_xyz\n"
                          + target.read_text(encoding="utf-8"), encoding="utf-8")
        result = _sp.run([_sys.executable, str(broken / "check_plan_contract.py"),
                          str(ROOT / "tests" / "booking-ready-fixture.json")],
                         capture_output=True, text=True)
        check("a failed enum check says so on stdout, not only on stderr",
              "NOT checked" in result.stdout or "KEYS ONLY" in result.stdout,
              result.stdout.strip()[-160:])
        check("and it does not claim every value is in its vocabulary",
              "every value in a closed vocabulary is one that vocabulary contains"
              not in result.stdout, result.stdout.strip()[-160:])

    # The multi-city form SKILL.md documents -- "one object, or a list of them for a multi-city
    # trip" -- was reported as a type error ("the contract declares object"), while the consistency
    # gate accepted it. The template can carry only one specimen, so the checker has to know.
    fixture = json.loads((ROOT / "tests" / "booking-ready-fixture.json").read_text(encoding="utf-8"))
    fixture["trip"]["destination_coords"] = [{"lat": 40.7128, "lon": -74.006, "label": "New York"},
                                             {"lat": 34.0522, "lon": -118.2437, "label": "Los Angeles"}]
    _, report = run(fixture)
    coords = [i for i in report.get("issues", []) if "destination_coords" in i.get("path", "")]
    check("the documented multi-city list of coordinates is known", not coords, str(coords)[:300])
    fixture["trip"]["destination_coords"][1] = {"lat": 34.0522, "lng": -118.2437}
    _, report = run(fixture)
    typo = [i for i in report.get("issues", []) if i.get("path") == "trip.destination_coords[].lng"]
    check("a misspelled key inside the list is still named, with its near-match",
          typo and str(typo[0].get("suggestion") or "").endswith("lon"), str(report)[:300])

    if failures:
        print(f"PLAN CONTRACT FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all plan-contract cases passed")
    return 0


def test_plan_contract() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
