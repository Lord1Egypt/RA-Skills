#!/usr/bin/env python3
"""Regression tests for scripts/check_plan_consistency.py.

Every case below is a defect that actually shipped in a real Travel Buddy run and passed
`render_final_trip_html.py` plus `validate_trip_html.py` without complaint. The point of the
checker is that these can never pass silently again, so the test reintroduces each one into
the known-good fixture and asserts the gate fires.

Run:  python tests/test_plan_consistency.py
      python -m pytest tests/test_plan_consistency.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "check_plan_consistency.py"
FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"


# Loaded once, by path, so the module under test is the file the CLI runs rather than whatever an
# import path happens to resolve to.
_spec = importlib.util.spec_from_file_location("_checker_under_test", CHECKER)
CHECKER_MODULE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(CHECKER_MODULE)


def run(plan: dict, verification: dict | None = None) -> tuple[int, str]:
    """Run every check in-process and rebuild the output main() would have printed.

    This used to shell out for each of ~70 assertions. Measured: 111 ms per subprocess against
    0.8 ms in-process -- 132x, and 8.9 s of an 11.4 s suite spent starting interpreters rather than
    testing anything. A slow suite gets run less often, which costs more coverage than any single
    check buys.

    What the subprocess DID buy is real and is not thrown away: argument parsing, reading the file
    from disk, the exit code, the stdout/stderr split, and the plan-path binding that
    check_verification needs. Those are the CLI contract, so cli_contract_cases() below still
    shells out -- a handful of times instead of seventy. This helper reproduces main()'s output
    format exactly (notes to stdout, "PLAN CONSISTENCY FAILED" plus dashed errors to stderr) so
    every existing assertion, which matches on those strings, keeps testing what it always did.

    "Exactly" now includes the rule-deduplication main() applies before printing: a rule that
    fires more than once states its rationale on the first finding and back-references it on the
    rest. Reproducing that here rather than printing the raw list is the whole point of the
    helper -- a harness that rebuilt the OLD format would let every needle below keep passing
    against output no CLI run produces, which is the drift this docstring exists to prevent. The
    findings themselves are untouched, so a needle that names a venue, a value or a field still
    matches; a needle that reaches for a rule's rationale now has to find it where a reader would,
    on that rule's first finding.
    """
    # main() rejects a non-object plan before any check sees it, and one case below depends on
    # that: a plan that is a list must exit 2 with an ERROR line rather than reaching a check and
    # raising. Reproducing the guard here is not decoration -- without it the in-process runner is
    # more permissive than the CLI it stands in for, which is the one way this refactor could
    # silently weaken the suite.
    if not isinstance(plan, dict):
        return 2, f"ERROR: plan JSON must be an object, got {type(plan).__name__}.\n"

    # run_plan_checks(), not a bare loop: it is what main() calls, it is what records the emission
    # site each finding came from, and it is what survives a check that raises. A loop here would
    # be a second implementation of the thing under test.
    errors, notes, crashed = CHECKER_MODULE.run_plan_checks(plan)
    if verification is not None:
        errors.current_check = CHECKER_MODULE.check_verification.__name__
        CHECKER_MODULE.check_verification(
            verification, errors, notes, plan=plan, plan_path="plan.json")
        errors.current_check = ""
    status = 2 if crashed else (1 if errors else 0)
    out = "".join(f"note: {note}\n" for note in notes)
    if errors:
        legend, lines = CHECKER_MODULE.format_findings(
            CHECKER_MODULE.split_findings(errors, errors.sites, errors.checks))
        out += "PLAN CONSISTENCY FAILED\n"
        out += "".join(f"({line})\n" for line in legend)
        out += "".join(f"- {line}\n" for line in lines)
        return status, out
    return status, out + "PLAN CONSISTENCY OK\n"


def cli_contract_cases(base: dict) -> list[str]:
    """The handful of behaviours only a real process can prove.

    Kept deliberately small: these are about argv, file IO and exit codes, not about any individual
    rule, so one clean case and one failing case cover the contract that in-process running cannot.

    Every invocation here that is not itself testing the verification gate now carries
    `--no-verification-yet`, because the flag pair below made the bare form a refusal. That is not
    boilerplate to copy without thinking: the waiver is what these cases mean, since each one is
    about argv and file IO rather than about a report.
    """
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        good = Path(tmp) / "plan.json"
        good.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(CHECKER), str(good), "--no-verification-yet"],
                              capture_output=True, text=True)
        if proc.returncode != 0 or "PLAN CONSISTENCY OK" not in proc.stdout:
            failures.append(f"cli: a clean plan must exit 0 with OK on stdout, got {proc.returncode}")

        broken = copy.deepcopy(base)
        broken["days"][0]["route"]["duration_minutes"] = 999
        bad = Path(tmp) / "bad.json"
        bad.write_text(json.dumps(broken, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run([sys.executable, str(CHECKER), str(bad), "--no-verification-yet"],
                              capture_output=True, text=True)
        if proc.returncode != 1 or "PLAN CONSISTENCY FAILED" not in proc.stderr:
            failures.append("cli: a defective plan must exit 1 with the failure banner on stderr")
        if "- day" not in proc.stderr:
            failures.append("cli: individual errors must be dashed lines on stderr")

        # The waiver matters here for a reason worth stating: the verification gate runs BEFORE the
        # plan is read from disk, so a bare invocation of this case would exit 1 on the missing
        # flag and never reach the file-read guard it exists to test. It would still be "failing",
        # so the case would look alive while asserting nothing about unreadable plans.
        missing = subprocess.run([sys.executable, str(CHECKER), str(Path(tmp) / "nope.json"),
                                  "--no-verification-yet"], capture_output=True, text=True)
        if missing.returncode != 2 or "ERROR" not in missing.stderr:
            failures.append("cli: an unreadable plan must exit 2 with an ERROR line, not a traceback")
        if "Traceback" in missing.stderr:
            failures.append("cli: an unreadable plan produced a traceback")

        report = full_verification()
        rp = Path(tmp) / "verification.json"
        rp.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(CHECKER), str(good), "--verification", str(rp)],
            capture_output=True, text=True)
        # The report names "plan.json"; the file on disk is also plan.json, so the binding holds.
        if proc.returncode != 0:
            failures.append(f"cli: --verification with a matching report must pass, got {proc.stderr[:200]}")

        failures.extend(verification_flag_cases(base, report, tmp))
    return failures


def verification_flag_cases(base: dict, report: dict, tmp: str) -> list[str]:
    """--verification is required, or waived out loud. Neither is not an option.

    The defect these cover shipped and was invisible: `--verification` defaulted to None, and
    check_verification -- which is the only reader of the report, is absent from PLAN_CHECKS, and
    has no other call site in the script -- was reachable only when the flag was passed. SKILL.md
    named the bare form in both places it names this script, so the documented invocation was the
    disarmed one and every report check silently did not run.

    Measured on a real workspace plan (plans/2027-02-12-阿利坎特...json) while writing this:
    bare printed 13 findings, and the same plan handed a verification report belonging to another
    trip printed 21. Those 8 include "report is dated 2026-08-04, before the plan's generated_at
    2026-08-09" and "report says it verified 'tokyo-plan.json'" -- a mis-bound report caught at
    build time instead of at save time, which references/research-budget.md prices at a
    re-verification pass, ~300k light to ~700k full.

    A CLI test rather than an in-process one, deliberately: all four behaviours below are argv and
    exit codes, and the in-process `run()` helper cannot see argparse at all. That is exactly how
    the defect survived -- every rule had a test, and nothing tested whether the rule was wired to
    a flag anyone passes.
    """
    failures: list[str] = []
    good = Path(tmp) / "plan.json"

    # 1. Bare: refused. The point of the change. An exit 0 is what an assistant reads, so the
    #    absence of a report has to cost an exit code rather than a note nobody scrolls to.
    proc = subprocess.run([sys.executable, str(CHECKER), str(good)],
                          capture_output=True, text=True)
    if proc.returncode == 0:
        failures.append("verification-flag: a bare invocation must be refused, not exit 0 -- that "
                        "silent success is the entire defect")
    if "--no-verification-yet" not in proc.stderr:
        failures.append("verification-flag: the refusal must name the escape hatch, or the reader "
                        "cannot proceed and will delete the gate instead")
    if "PLAN CONSISTENCY OK" in proc.stdout:
        failures.append("verification-flag: a refused run must not print the OK banner")

    # 2. Waived: runs, and says so on BOTH streams. A caller keeping only stderr would otherwise
    #    read a bare success; a caller keeping only stdout would miss the banner.
    proc = subprocess.run([sys.executable, str(CHECKER), str(good), "--no-verification-yet"],
                          capture_output=True, text=True)
    if proc.returncode != 0 or "PLAN CONSISTENCY OK" not in proc.stdout:
        failures.append(f"verification-flag: --no-verification-yet must run the plan checks and "
                        f"pass a clean plan, got exit {proc.returncode}: {proc.stderr[:200]}")
    if "NOT VERIFIED" not in proc.stderr:
        failures.append("verification-flag: --no-verification-yet must print the banner on stderr")
    if "NO VERIFICATION REPORT" not in proc.stdout:
        failures.append("verification-flag: --no-verification-yet must record the gap as a note on "
                        "stdout, beside the other notes an operator scans")

    # 3. A good report still passes, and passing is not the same as being ignored: the mis-bound
    #    case below is what proves this one ran rather than merely not-crashing.
    rp = Path(tmp) / "verification.json"
    rp.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(CHECKER), str(good), "--verification", str(rp)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        failures.append(f"verification-flag: a matching report must pass, got {proc.stderr[:300]}")
    if "NOT VERIFIED" in proc.stderr:
        failures.append("verification-flag: a verified run must not print the waiver banner")

    # 4. Mis-bound: a report for another plan must be named as such. This is the case that was
    #    unreachable on the documented path, and the one that repays the flag.
    misbound = copy.deepcopy(report)
    misbound["plan"] = "some-other-trip.json"
    mp = Path(tmp) / "misbound.json"
    mp.write_text(json.dumps(misbound, ensure_ascii=False), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(CHECKER), str(good), "--verification", str(mp)],
                          capture_output=True, text=True)
    if proc.returncode != 1:
        failures.append(f"verification-flag: a report naming a different plan must fail, got exit "
                        f"{proc.returncode}")
    if "some-other-trip.json" not in proc.stderr:
        failures.append("verification-flag: the mis-binding error must quote the plan the report "
                        "claims, so the reader can tell which of the two files is wrong")

    # 5. Both flags at once is a contradiction. Refused rather than resolved by precedence,
    #    because the only way to write both is a caller appending the waiver unconditionally --
    #    which would then "pass" forever with whatever report it also handed over.
    proc = subprocess.run([sys.executable, str(CHECKER), str(good), "--verification", str(rp),
                           "--no-verification-yet"], capture_output=True, text=True)
    if proc.returncode == 0:
        failures.append("verification-flag: --verification with --no-verification-yet must be "
                        "refused, not silently resolved in favour of either one")

    # 6. An empty --verification is the unset-shell-variable case (`--verification "$REPORT"`).
    #    It reaches argparse as a falsy value, i.e. indistinguishable from passing nothing, which
    #    is precisely the silent skip this whole change exists to close.
    proc = subprocess.run([sys.executable, str(CHECKER), str(good), "--verification", ""],
                          capture_output=True, text=True)
    if proc.returncode == 0:
        failures.append("verification-flag: an empty --verification path must be refused; it is "
                        "what an unset shell variable expands to")
    if "empty path" not in proc.stderr:
        failures.append("verification-flag: an empty --verification must say the path was empty, "
                        "not that no flag was given -- the reader did write the flag")

    # 7. A report that is a bare list of domain blocks. check_verification opens with _obj(report),
    #    so a list became {} and every real block was then reported as a MISSING domain: findings
    #    that all name the wrong problem on a report whose contents were fine.
    lp = Path(tmp) / "list-report.json"
    lp.write_text(json.dumps(report.get("domains") or [], ensure_ascii=False), encoding="utf-8")
    proc = subprocess.run([sys.executable, str(CHECKER), str(good), "--verification", str(lp)],
                          capture_output=True, text=True)
    if proc.returncode != 2 or "must be an object" not in proc.stderr:
        failures.append(f"verification-flag: a report that is a bare list must exit 2 naming the "
                        f"shape, got exit {proc.returncode}: {proc.stderr[:200]}")
    if "missing required domains" in proc.stderr:
        failures.append("verification-flag: a bare-list report must not be reported as missing the "
                        "domains it actually contains")

    # 8. --emit-walking stays exempt. It exits before any check runs, so there is no verification
    #    for it to skip, and making a data dump demand a report teaches the reflex of reaching for
    #    the waiver -- which is how an escape hatch stops meaning anything.
    proc = subprocess.run([sys.executable, str(CHECKER), str(good), "--emit-walking"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        failures.append(f"verification-flag: --emit-walking must not require a report, got exit "
                        f"{proc.returncode}: {proc.stderr[:200]}")
    if "day 1" not in proc.stdout:
        failures.append("verification-flag: --emit-walking must still print per-day walking totals")
    return failures


def day(plan: dict, number: int) -> dict:
    return next(d for d in plan["days"] if d["number"] == number)


def constraints(**overrides) -> dict:
    """trip.traveler_constraints in the shape the contract defines, with one field overridden.

    Written once here rather than inline per case: when a case hand-builds the block it is free
    to spell a key however it likes, and a check keyed on a name nothing produces passes every
    test while never firing on a real plan."""
    block = {
        "dietary_or_religious_needs": [],
        "allergy_severity": "none",
        "allergy_card_text": None,
        "max_continuous_walking_minutes": None,
        "mobility_notes": [],
    }
    block.update(overrides)
    return block


def replan_context(**overrides) -> dict:
    """plan.replan_context in the shape the contract defines, with one field overridden.

    Same reason as constraints() above: a case that hand-builds the block is free to spell
    "must_reverify" however it likes, and a gate keyed on a name nothing produces passes every
    test in this file while never firing on a plan replan_trip.py actually wrote.
    """
    block = {
        "replanned_from": "2026-09-28-fixture-trip.json",
        "replanned_at": "2026-08-07",
        "change_request": "Push the whole trip back one day.",
        "changed_fields": ["trip.start_date", "trip.end_date", "days[0].date"],
        "retained_note": "Route order, lodging and budget do not depend on the weekday and were kept.",
        "must_reverify": [],
    }
    block.update(overrides)
    return block


def full_verification() -> dict:
    """A clean seven-block report for the fixture, with claims_checked in its current shape.

    Every pointer below resolves against tests/booking-ready-fixture.json, and it has to: most
    cases in this file hand this report the pristine fixture, so a pointer that stopped resolving
    would fail cases that have nothing to do with it. That cost is the point of the field. It used
    to be an integer -- `"claims_checked": 3` -- which the same run that wrote the plan also wrote
    about itself, so a model whose verifier subagent died (a real failure mode) wrote a small
    number, the gate went green, and "verified" landed on a page someone books a train from.
    Migrating this function is the migration every operator with a saved report now has to do.

    The pointers are the ones each block would really have opened, not the cheapest four that
    resolve. Writing them the lazy way would pass the gate and teach the wrong habit here, in the
    file people copy from.
    """
    return {
        "checked_at": "2026-08-03",
        "plan": "plan.json",
        "domains": [
            # The fixture is a domestic trip and carries no entry_context at all, so the entry
            # block has nothing entry-shaped to cite and points at what it read to reach "no
            # formalities apply". This is the awkward corner of the new shape and worth knowing
            # about before it is met on a real plan: a domain whose subject is absent from the
            # itinerary has no field of its own to cite, and the honest answer is to name what was
            # read to conclude the domain does not apply -- not to invent a pointer that resolves.
            {"domain": "entry",
             "claims_checked": ["trip.origin", "trip.destination", "trip.traveler_count",
                                "assumptions[0]"],
             "findings": []},
            {"domain": "transport",
             "claims_checked": ["days[0].route.segments[0].fare_basis",
                                "days[0].route.segments[2].transfer_count",
                                "days[0].route.duration_minutes",
                                "transport_overview.overall_route_map_url"],
             "findings": []},
            # days[0].dining[0] is the fixture's only hours_status="verified" card, so the coverage
            # rule demands a pointer under it; the pair of cases at 22f drives both directions.
            {"domain": "sights_and_hours",
             "claims_checked": ["days[0].dining[0].venue_hours",
                                "days[0].dining[0].hours_status",
                                "days[0].dining[1].venue_hours",
                                "days[0].dining[1].hours_status",
                                "days[0].activities[0].time",
                                "days[0].activities[1].detail"],
             # Both dining cards are cited now. They used to differ -- dining[1] carried
             # hours_status "unverified" so the coverage rule demanded nothing for it -- but a
             # card may no longer name a seating time while admitting nobody checked the hours,
             # and render_final_trip_html requires every card to name one. So every card is
             # researched, and every card has to be cited.
             "findings": []},
            {"domain": "booking_and_lodging",
             "claims_checked": ["booking_options.accommodations[0].nightly_cost_high",
                                "booking_options.accommodations[0].check_out",
                                "booking_options.accommodations[1].direct_review_url",
                                "budget.breakdown[0].per_person_high"],
             "findings": []},
            {"domain": "seasonality",
             "claims_checked": ["trip.start_date", "days[0].contingency",
                                "destination_experience_anchors[0].checked_at"],
             "findings": []},
        ],
        # references/verification.md tells the operator to run seven agents; the report used to
        # accept five, so a run that followed the reference failed the gate and the cheapest escape
        # was to delete the two network-free auditors. In the run that prompted this they had found
        # 27 of 55 findings and 5 of the 6 criticals, so deleting them was the worst possible fix.
        "audits": [
            # days[0].route.duration_minutes is deliberately also in the transport domain above:
            # two blocks opening the same field is honest work, and only repeats *within* one block
            # are inflation. Case 22c asserts both halves of that.
            {"audit": "consistency",
             "claims_checked": ["days[0].route.duration_minutes",
                                "days[0].route.walking_burden",
                                "days[0].dining[0].route_anchor",
                                "budget.estimated_per_person_high"],
             "findings": []},
            # single_option_reason is null in the fixture, on purpose: the completeness auditor's
            # whole job is opening fields that may be empty, and a rule that demanded a non-null
            # value would push every report toward citing only the fields that happen to be filled.
            {"audit": "completeness",
             "claims_checked": ["budget.unverified_categories[0]",
                                "days[0].route.fallback_plan",
                                "booking_options.accommodations[0].single_option_reason",
                                "regional_service_context.booking_platform_selection_note"],
             "findings": []},
        ],
    }


def draft_render_flags(plan: dict) -> list[str]:
    """The validator flags for a page produced by render() alone, derived from the plan.

    Both callers below used to invoke `validate_trip_html.py <page>` bare, which ran none of the
    four conditional checks: the day count, the required booking-link types, the car-link rule and
    the traveller-facing "not fact-checked" banner were all off, and the script still exited 0. So
    a case whose whole point was "this page survives the delivery gate" was measuring a gate with
    most of it switched off.

    Derived rather than typed, so a fixture that gains a day or a ticket category stays covered
    without anybody editing a constant here -- a hand-typed 1 would keep passing on a 2-day plan.

    NOT `--plan`, deliberately: that additionally requires the gate stamp, and these pages come
    from render() with no save_trip_deliverables.py run behind them. They are legitimate draft
    renders and must keep validating as such; asserting the stamp here would assert something
    about a script that never ran.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from plan_flags import derive_html_flags  # noqa: PLC0415 - import after path setup

    flags = derive_html_flags(plan, plan_label="test fixture")
    args = ["--expected-days", str(flags.expected_days),
            "--transport-mode", flags.transport_mode]
    for booking_type in sorted(flags.required_booking_types):
        args += ["--require-booking-type", booking_type]
    if not flags.required_booking_types:
        args.append("--no-booking-types")
    args.append("--require-unverified-banner" if flags.require_unverified_banner
                else "--assert-verified-without-plan")
    return args


def fixture_passes_the_delivery_gate_cases(base: dict) -> list[str]:
    """The known-good fixture must survive the gate a real page is judged by.

    It did not. Two hotel options named their provider "Direct hotel" while linking to
    marriott.com and hyatt.com, which validate_trip_html.py rejects by design -- the button label
    is built from the same provider field, so it read "open Direct hotel" and went somewhere else.
    Nothing noticed for as long as the fixture existed, because every test in this file stopped at
    validate_plan and render: the HTML gate had no known-good baseline at all, so a regression in
    it would have shown up first on somebody's real trip.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import render  # noqa: PLC0415 - import after path setup
    from plan_flags import derive_html_flags  # noqa: PLC0415 - import after path setup

    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "fixture.html"
        page.write_text(render(copy.deepcopy(base)), encoding="utf-8")
        # This used to invoke the validator bare, which silently ran none of the four conditional
        # checks -- so "the known-good fixture survives the delivery gate" was measured with the
        # day count, the booking-type requirement, the car-link rule and the unverified-banner
        # check all switched off. The flags are derived from the fixture rather than typed, so a
        # fixture that gains a day or a ticket category stays covered without anyone editing a
        # constant here.
        #
        # Passed as explicit flags rather than as `--plan`, and the difference is the point:
        # `--plan` additionally requires the gate stamp, and this page was produced by render()
        # alone. That is a legitimate draft render, not a delivery, and it must keep validating
        # as one -- asserting the stamp here would test save_trip_deliverables.py, which never ran.
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_trip_html.py"),
             str(page), *draft_render_flags(base)],
            capture_output=True, text=True)
        if proc.returncode != 0:
            reported = [line for line in (proc.stdout + proc.stderr).splitlines()
                        if line.startswith("- ")]
            failures.append("fixture: the known-good plan does not pass validate_trip_html -- "
                            + "; ".join(reported[:3]))
    return failures


def optional_label_cases(base: dict) -> list[str]:
    """New renderer labels must be optional, and the i18n gate must still catch them untranslated.

    Both halves matter and the first was learned the hard way: making `group_ground` and
    `station_access` required hard-failed every French, Japanese and Spanish plan already saved in
    a workspace, naming labels for a booking category those trips do not contain and their author
    had never heard of. OPTIONAL_UI_LABEL_KEYS exists for exactly that, with the reason written
    above it, and the new keys were simply not added to it.

    Optional alone would be the opposite mistake -- an untranslated label shipping in silence -- so
    the gate carries a pattern for each.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import render  # noqa: PLC0415 - import after path setup

    failures: list[str] = []
    labels = json.loads(
        (ROOT / "templates" / "renderer-ui-labels.example.json").read_text(encoding="utf-8"))

    plan = copy.deepcopy(base)
    plan["trip"]["language"] = "fr"
    plan["ui_labels"] = {k: v for k, v in labels.items()
                         if k not in {"group_ground", "station_access"}}
    try:
        render(plan)
    except Exception as exc:  # noqa: BLE001 - any failure here is the regression
        failures.append(f"labels: a plan authored before the new keys stopped rendering: {exc}")

    # The gate must still object when a translator leaves them English.
    plan = copy.deepcopy(base)
    plan["trip"]["language"] = "fr"
    plan["ui_labels"] = {k: (f"FR-{k}" if isinstance(v, str) else v) for k, v in labels.items()}
    plan["ui_labels"]["group_ground"] = labels["group_ground"]
    plan["ui_labels"]["station_access"] = labels["station_access"]
    plan["booking_options"]["ground_transport"] = [dict(
        json.loads((ROOT / "templates" / "final-trip-plan.json").read_text(encoding="utf-8"))
        ["booking_options"]["ground_transport"][0])]
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "fr.html"
        try:
            page.write_text(render(plan), encoding="utf-8")
        except Exception:  # noqa: BLE001 - the TODO-laden template block may not validate; skip
            return failures
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_trip_html.py"),
             str(page), *draft_render_flags(plan)],
            capture_output=True, text=True)
        if "Rail, coach and ferry options" not in (proc.stdout + proc.stderr):
            failures.append("labels: an untranslated ground heading was not caught by the i18n gate")
    return failures


def example_label_file_cases(base: dict) -> list[str]:
    """The copyable label set must be the complete label set.

    `REQUIRED_UI_LABEL_KEYS` is drift-proof by construction -- it is derived from the zh-CN dict.
    `templates/renderer-ui-labels.example.json`, the file every translator starts from, was a
    hand-maintained list with no derivation and no test, so it had silently fallen eleven keys
    behind. A translator did exactly what the repo asks -- copy the file, translate all of it,
    ship a French page -- and got English `verified` / `researched` on every dining card, with the
    i18n gate certifying the page because those two words were not in its lists either.

    Set equality, not a subset: an extra key is drift too, and a missing OPTIONAL key produces the
    silent-English failure while a missing REQUIRED one produces a page that renders entirely in
    English. Neither is visible without this assertion.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import labels_for, validate_plan  # noqa: PLC0415

    failures: list[str] = []
    example = json.loads(
        (ROOT / "templates" / "renderer-ui-labels.example.json").read_text(encoding="utf-8"))
    renderer_keys = set(labels_for("zh-CN"))
    missing = sorted(renderer_keys - set(example))
    extra = sorted(set(example) - renderer_keys)
    if missing:
        failures.append(f"labels: the copyable example file is missing {missing} -- a translator "
                        f"who translates all of it still ships English for those")
    if extra:
        failures.append(f"labels: the example file offers {extra}, which the renderer never reads")

    # And it must be a set validate_plan accepts, so an incomplete one fails loudly here rather
    # than quietly producing an all-English page in production.
    plan = copy.deepcopy(base)
    plan["trip"]["language"] = "fr"
    plan["ui_labels"] = example
    errors = [error for error in validate_plan(plan) if "ui_labels" in error or "label" in error]
    if errors:
        failures.append(f"labels: the shipped example set does not pass validate_plan: {errors[:2]}")
    return failures


def ground_transport_cases(base: dict) -> list[str]:
    """Rail, coach and ferry had no bookable product at all.

    A Japan or European rail trip shipped as "booking-ready" with three compared hotels and no way
    to reach, price-check or availability-check the train -- the largest and most time-sensitive
    purchase on the page. The category is held to the flight standard on purpose: a looser one
    becomes the place authors put what they did not research.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import render, validate_plan  # noqa: PLC0415 - import after path setup

    def leg(identifier: str) -> dict:
        return {"service_identifier": identifier, "departure_local": "10:00",
                "arrival_local": "13:11", "duration_minutes": 191, "stops": 1,
                "connection_or_terminal_note": "One change, same platform as planned"}

    complete = {
        "id": "ground-1", "provider": "Deutsche Bahn", "comparison_platform": "NS International",
        "comparison_checked_at": "2026-09-01", "source_type": "official_provider",
        "checked_at": "2026-09-01", "review_url": "https://int.bahn.de/en",
        "origin_station": "Leiden Centraal", "destination_station": "Köln Hbf",
        "outbound_date": base["trip"]["start_date"], "return_date": base["trip"]["end_date"],
        "outbound_itinerary": leg("NS Intercity + ICE 123"),
        "return_itinerary": leg("ICE 126 + NS Intercity"),
        "material_conditions": "Saver fare is train-bound and non-refundable",
        "availability_status": "available", "price_basis": "per_person_round_trip",
        "fare_low": 51, "fare_high": 61, "fare_currency": "EUR",
        "price_status": "estimate", "price_checked_at": "2026-09-01",
        "station_transfer_note": "Köln Hbf is 200 m from the cathedral; no transfer needed",
        "round_trip_search_provider": "Deutsche Bahn",
        "round_trip_search_url": "https://int.bahn.de/en",
        "round_trip_search_checked_at": "2026-09-01",
        "round_trip_prefilled_fields": ["origin", "destination", "outbound_date", "return_date",
                                        "travellers"],
        "single_option_reason": "No direct service exists; one change is the shortest routing",
    }

    failures: list[str] = []
    plan = copy.deepcopy(base)
    plan["booking_options"]["ground_transport"] = [copy.deepcopy(complete)]
    errors = validate_plan(plan)
    if errors:
        failures.append(f"ground: a complete rail option was rejected: {errors[:2]}")
    else:
        page = render(plan)
        for probe, label in (("ICE 123", "the outbound service identifier"),
                             ("ICE 126", "the return service identifier"),
                             ("Saver fare", "the fare conditions"),
                             ("200 m from the cathedral", "the station transfer note"),
                             ('data-booking-type="ground"', "a bookable ground link")):
            if probe not in page:
                failures.append(f"ground: {label} never reaches the page")

    # Held to the flight standard: each of these alone must be rejected.
    for field in ("origin_station", "destination_station", "material_conditions",
                  "station_transfer_note", "round_trip_search_url", "outbound_itinerary"):
        plan = copy.deepcopy(base)
        item = copy.deepcopy(complete)
        item.pop(field)
        plan["booking_options"]["ground_transport"] = [item]
        if not validate_plan(plan):
            failures.append(f"ground: an option missing {field} was accepted -- the category must "
                            f"not be a looser back door than a flight")

    plan = copy.deepcopy(base)
    item = copy.deepcopy(complete)
    item["price_basis"] = "per_person"          # the flight rule spells this per_person_round_trip
    plan["booking_options"]["ground_transport"] = [item]
    if not validate_plan(plan):
        failures.append("ground: a wrong price_basis was accepted")

    # "Held to exactly the flight standard" is a literal claim in SKILL.md and in
    # references/booking-html-output.md, and it was false: all three comparison rules were keyed on
    # flight_items. A lone unexplained rail option, two cards sharing one review_url, and an option
    # with no id all validated, while the identical omission on a flight was named by the gate.
    plan = copy.deepcopy(base)
    item = copy.deepcopy(complete)
    item.pop("single_option_reason")
    plan["booking_options"]["ground_transport"] = [item]
    if not validate_plan(plan):
        failures.append("ground: one option with no researched single_option_reason was accepted -- "
                        "a flight in the same position is rejected by name")

    plan = copy.deepcopy(base)
    item = copy.deepcopy(complete)
    item.pop("id")
    plan["booking_options"]["ground_transport"] = [item]
    if not validate_plan(plan):
        failures.append("ground: an option with no id was accepted")

    plan = copy.deepcopy(base)
    twin = copy.deepcopy(complete)
    twin["id"] = "ground-2"
    plan["booking_options"]["ground_transport"] = [copy.deepcopy(complete), twin]
    if not any("review_url" in error for error in validate_plan(plan)):
        failures.append("ground: two candidates sharing one review_url were accepted -- the page "
                        "then looks like a comparison and is not")

    plan = copy.deepcopy(base)
    twin = copy.deepcopy(complete)
    twin["review_url"] = "https://www.nsinternational.com/en"
    plan["booking_options"]["ground_transport"] = [copy.deepcopy(complete), twin]
    if not any("distinct, non-empty string ids" in error for error in validate_plan(plan)):
        failures.append("ground: two candidates sharing one id were accepted")

    # The contract template seeded these with 0 and 1970-01-01 rather than null, so the one value
    # meaning "I did not fill this in" was a value every gate accepted: a card advertising a
    # 0-minute journey at EUR 0. The template is fixed; these keep the gate honest regardless.
    plan = copy.deepcopy(base)
    item = copy.deepcopy(complete)
    item.update(fare_low=0, fare_high=0)
    plan["booking_options"]["ground_transport"] = [item]
    if not validate_plan(plan):
        failures.append("ground: a 0-0 fare range was accepted as a researched fare")

    plan = copy.deepcopy(base)
    item = copy.deepcopy(complete)
    item["outbound_itinerary"] = dict(item["outbound_itinerary"], duration_minutes=0)
    plan["booking_options"]["ground_transport"] = [item]
    if not validate_plan(plan):
        failures.append("ground: a leg of zero minutes was accepted as a researched journey")

    # The template block, dropped in verbatim, must not validate. It is the file authors copy from,
    # so a block whose placeholders are all legal values teaches a card the first gate cannot see
    # is empty.
    plan = copy.deepcopy(base)
    plan["booking_options"]["ground_transport"] = [copy.deepcopy(json.loads(
        (ROOT / "templates" / "final-trip-plan.json").read_text(encoding="utf-8"))
        ["booking_options"]["ground_transport"][0])]
    if not validate_plan(plan):
        failures.append("ground: the unfilled contract template block validated as a real option")

    # The card printed "Conditions require recheck" -- option_card's no-data fallback -- in the slot
    # under the price on every ground card, however completely it was researched, three rows above
    # the line that actually states the conditions.
    plan = copy.deepcopy(base)
    plan["booking_options"]["ground_transport"] = [copy.deepcopy(complete)]
    if not validate_plan(plan):
        card = re.search(r'<article class="option" data-option-kind="ground".*?</article>',
                         render(plan), re.S)
        if not card:
            failures.append("ground: the rendered card carries no data-option-kind")
        elif "Conditions require recheck" in card.group(0):
            failures.append("ground: a fully researched card still prints the no-data fallback "
                            "'Conditions require recheck' under its fare")

    # Dates were truthiness-checked only, so "next Friday" and a return before the departure both
    # validated and printed onto the search button.
    for label, patch, must_reject in (
        ("a non-ISO outbound date", {"outbound_date": "next Friday"}, True),
        # Reversed dates need a window wider than the fixture's single day, so this case builds
        # one below rather than here.
        ("a date outside the trip window", {"outbound_date": "2099-01-01"}, True),
    ):
        plan = copy.deepcopy(base)
        item = copy.deepcopy(complete)
        item.update(patch)
        plan["booking_options"]["ground_transport"] = [item]
        if bool(validate_plan(plan)) is not must_reject:
            failures.append(f"ground: {label} was accepted")

    # Two rules that need a multi-day window, which the single-day fixture cannot give: a reversed
    # pair, and the mid-trip leg. The flight rule that outbound_date == trip.start_date is
    # deliberately NOT copied to ground, because a rail leg is often the hop between two cities and
    # pinning it to the window's first day would reject the multi-city case this category serves.
    wide = copy.deepcopy(base)
    wide["trip"]["end_date"] = "2026-09-30"
    day_two = copy.deepcopy(wide["days"][0])
    day_two.update(number=2, date="2026-09-29")
    day_three = copy.deepcopy(wide["days"][0])
    day_three.update(number=3, date="2026-09-30", day_type="departure")
    wide["days"] = [wide["days"][0], day_two, day_three]
    for stay in wide["booking_options"]["accommodations"]:
        stay["check_out"] = "2026-09-30"

    plan = copy.deepcopy(wide)
    item = copy.deepcopy(complete)
    item.update(outbound_date="2026-09-30", return_date="2026-09-29")
    plan["booking_options"]["ground_transport"] = [item]
    if not any("return_date" in e for e in validate_plan(plan)):
        failures.append("ground: a return before the outbound was accepted")

    plan = copy.deepcopy(wide)
    item = copy.deepcopy(complete)
    item.update(outbound_date="2026-09-29", return_date="2026-09-29")   # the mid-trip city hop
    plan["booking_options"]["ground_transport"] = [item]
    if any("outbound_date" in e or "return_date" in e for e in validate_plan(plan)):
        failures.append("ground: a mid-trip rail leg was rejected; only flights must start the trip")

    # Three fields the validator requires and the card did not print, so the fare showed with no
    # hint that it was an estimate, priced weeks ago, on limited inventory -- while the hotel and
    # flight cards beside it said exactly that.
    plan = copy.deepcopy(base)
    item = copy.deepcopy(complete)
    item.update(availability_status="limited", price_status="estimate",
                price_checked_at="2026-07-01")
    plan["booking_options"]["ground_transport"] = [item]
    page = render(plan)
    # "Limited", not the token: an English page prints its enum values as English words since
    # 2026-09-24 (ENGLISH_ENUM_LABELS), so the status reaches the card as the word a reader sees.
    for probe, label in (("2026-07-01", "price_checked_at"), ("Limited", "availability_status"),
                         ("estimate", "price_status")):
        if probe not in page:
            failures.append(f"ground: {label} is required and never reaches the card")

    # Adding the category made a train card POSSIBLE; this is what makes it REQUIRED. Without it a
    # rail-arrival plan with three compared hotels and no way to reach, price-check or
    # availability-check the train passed every gate exactly as before -- the defect the category
    # was built to end, recurring on any run where the author did not think of it.
    # --require-booking-type ground cannot cover for it: that flag is opt-in, and the flight rule
    # it mirrors pointedly does not depend on the operator remembering one.
    rail = copy.deepcopy(base)
    rail["trip"]["arrival_transport_mode"] = "rail"
    if not any("ground_transport" in e for e in validate_plan(copy.deepcopy(rail))):
        failures.append("ground: a rail-arrival plan with no train card was accepted")
    rail["booking_options"]["ground_transport"] = [copy.deepcopy(complete)]
    if any("ground_transport" in e for e in validate_plan(rail)):
        failures.append("ground: a rail-arrival plan WITH a train card was rejected")

    # "road" is an intercity coach only when the trip leaves town. The fixture is Chengdu to
    # Chengdu, where road means the taxi that met the traveller, and demanding a bookable coach
    # card for that would be a gate firing on correct authoring.
    local = copy.deepcopy(base)
    local["trip"]["arrival_transport_mode"] = "road"
    local["trip"]["destination"] = local["trip"]["origin"]
    if any("ground_transport" in e for e in validate_plan(local)):
        failures.append("ground: a same-city road arrival was asked for a coach card")
    intercity = copy.deepcopy(local)
    intercity["trip"]["destination"] = "Somewhere Else Entirely"
    if not any("ground_transport" in e for e in validate_plan(intercity)):
        failures.append("ground: an intercity road arrival with no coach card was accepted")

    # And a plan carrying none of this must be unaffected -- every existing plan predates it.
    if validate_plan(copy.deepcopy(base)):
        failures.append("ground: a plan with no ground_transport array stopped validating")
    return failures


def required_fields_reach_the_page_cases(base: dict) -> list[str]:
    """A field the renderer REQUIRES and never prints is research the traveller paid for and cannot
    see -- SKILL.md states that rule and three fields were violating it.

    Sentinels rather than an eyeball: fill the field with a token nothing else could produce, render,
    and look for it. `fare_basis` was the worst of the three, because a price with no basis is the
    black box the whole source discipline exists to prevent -- on the measured plan, 15 segments
    carried a researched fare and the page showed bare numbers.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import render  # noqa: PLC0415 - import after path setup

    failures: list[str] = []
    plan = copy.deepcopy(base)
    for index, segment in enumerate(day(plan, 1)["route"]["segments"]):
        segment["fare_basis"] = f"ZZ-FARE-{index}-ZZ"
    plan["regional_service_context"]["selection_basis"] = "ZZ-SELECTION-BASIS-ZZ"
    for index, source in enumerate(plan["sources"]):
        source["claim_or_decision_supported"] = f"ZZ-CLAIM-{index}-ZZ"
    page = render(plan)

    for index in range(len(day(plan, 1)["route"]["segments"])):
        if f"ZZ-FARE-{index}-ZZ" not in page:
            failures.append(f"render: segment {index + 1}'s fare_basis never reaches the page, so a "
                            f"traveller sees a price with no basis")
    if "ZZ-SELECTION-BASIS-ZZ" not in page:
        failures.append("render: regional_service_context.selection_basis is required and never "
                        "printed, so the page says which providers were used and never why")
    missing = [i for i in range(len(plan["sources"])) if f"ZZ-CLAIM-{i}-ZZ" not in page]
    if missing:
        failures.append(f"render: {len(missing)} source rows do not show what they support -- a "
                        f"register whose lines all read alike is not a register")
    return failures


def language_coverage_cases(base: dict) -> list[str]:
    """Four defects that all reduce to the same thing: the gate answering in a language it does not
    speak, or a page speaking one nobody asked for."""
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import render  # noqa: PLC0415 - import after path setup

    failures: list[str] = []
    day_one = day(base, 1)["date"]  # a Monday, which every closed-day case below relies on

    def hours_verdict(hours: str) -> str:
        plan = copy.deepcopy(base)
        card = day(plan, 1)["dining"][1]
        card["venue_hours"] = hours
        card["hours_status"] = "verified"
        _, out = run(plan)
        if "closed-day check cannot run" in out:
            return "unreadable"
        if "different days in different languages" in out:
            return "ambiguous"
        if "only cover" in out:
            return "closed"
        return "open"

    # 1. A rest-day marker must never be read as the OPEN set. "Montag geschlossen, 11:00-22:00"
    #    means shut on Monday; the parser matched "Montag", failed to recognise "geschlossen", and
    #    returned {Monday} as the days the venue is open -- approving a dinner on the one day the
    #    kitchen is dark, and refusing it on every day it is not.
    for closed in ("Montag geschlossen, 11:00-22:00", "maandag gesloten 11:00-22:00",
                   "周一休息 11:00-22:00", "Mon closed 11:00-22:00",
                   "Sonntag Ruhetag 11:00-22:00", "lundi fermé 11:00-22:00"):
        if hours_verdict(closed) != "unreadable":
            failures.append(f"hours: {closed!r} must be refused as unreadable, never parsed -- "
                            f"reading a closure as an opening inverts the answer exactly")

    # 2. Languages beyond en/zh/de/nl. Until a language is in the table its rest day is invisible,
    #    so a Kyoto temple or a Paris bistro books on the day it is shut with every gate green.
    #    day 1 is a Monday, so a Tuesday-to-Sunday venue must be reported closed.
    for shut_on_monday in ("火曜日-日曜日 11:00-22:00", "mardi-dimanche 11:00-22:00",
                           "martes a domingo 11:00-22:00", "martedì-domenica 11:00-22:00",
                           "화요일-일요일 11:00-22:00"):
        if hours_verdict(shut_on_monday) != "closed":
            failures.append(f"hours: {shut_on_monday!r} excludes {day_one}'s weekday and must be "
                            f"reported closed")

    # 3. Ambiguity still takes precedence over the generic message, because it names the exact fix.
    if hours_verdict("Ma-Sa 11:00-22:00") != "ambiguous":
        failures.append("hours: an ambiguous abbreviation must get its own message, not the "
                        "generic unreadable one")

    # 4. No renderer-owned Chinese may reach a page in a third language. Ten strings were hardcoded
    #    inside a function every non-English page runs, so a French itinerary shipped 82公里 on every
    #    segment and 酒店 on every booking card while all four gates called it valid.
    # 4b. The general form of the same rule, and the backstop for a hole the validator has: it
    #     fails only English it already knows about, so a string invented after it was written is
    #     invisible to it. Four figure captions shipped English onto a Chinese page exactly that
    #     way and every gate stayed green. The keys of static_replacements ARE, by construction,
    #     the complete list of renderer-owned English, so none of them may survive localization.
    from render_final_trip_html import labels_for, static_replacements  # noqa: PLC0415

    chinese = copy.deepcopy(base)
    chinese["trip"]["language"] = "Chinese"
    zh_page = render(chinese)
    zh_body = re.sub(r"<(style|script).*?</\1>", "", zh_page, flags=re.S)
    survivors = sorted(
        source for source in static_replacements(labels_for("zh-CN"))
        # A key whose localization is identical to itself is a no-op entry (a platform name, a
        # unit that does not translate) and cannot leak anything.
        if static_replacements(labels_for("zh-CN"))[source] != source and source in zh_body
    )
    if survivors:
        failures.append(
            "i18n: renderer-owned English survived localization on a Chinese page: "
            + "; ".join(repr(s[:60]) for s in survivors[:6])
            + (f" (+{len(survivors) - 6} more)" if len(survivors) > 6 else ""))

    # The assertion above catches a table entry that stopped matching -- the byte-identical-key
    # hazard the table documents. It cannot catch a string that was never ADDED to the table,
    # which is the hole itself. This one can, for the elements that are renderer-owned by
    # construction: every figure caption and every SVG accessible name is written by the renderer,
    # never by the traveller, so on a Chinese page each must contain Chinese.
    # figcaption only. An SVG <title> holds the accessible name of a single mark, which is the
    # traveller's own activity or venue name -- user content, legitimately in any language -- and
    # the document <title> is the trip title. Captions are the renderer's own sentences.
    renderer_owned = re.findall(r"<figcaption>(.*?)</figcaption>", zh_body, flags=re.S)
    english_only = [re.sub(r"<[^>]+>", "", text).strip() for text in renderer_owned]
    english_only = [text for text in english_only
                    if text and not re.search(r"[一-鿿]", text)]
    if english_only:
        failures.append(
            "i18n: a renderer-owned caption or accessible name carries no Chinese on a Chinese "
            "page: " + "; ".join(repr(t[:60]) for t in english_only[:5]))

    french = copy.deepcopy(base)
    french["trip"]["language"] = "fr"
    french["ui_labels"] = json.loads(
        (ROOT / "templates" / "renderer-ui-labels.example.json").read_text(encoding="utf-8"))
    page = render(french)
    body = re.sub(r"<(style|script).*?</\1>", "", page, flags=re.S)
    leaked = sorted(set(re.findall(r"[\u4e00-\u9fff]+", re.sub(r"<[^>]+>", " ", body))))
    if leaked:
        failures.append(f"i18n: a French page carries renderer-owned Chinese: {leaked}")
    return failures


def ground_card_coverage_cases(base: dict) -> list[str]:
    """Three ways the ground card sat outside rules every other card obeys.

    1. Its pill shipped the raw machine enum on every non-English page. Four pills were localized
       and the fifth was not, no translator could fix it (no code path read a `pill_ground` key),
       and both gates said VALID.
    2. Its booking-access check was keyed on `transport_preference.mode == "public-transit"` rather
       than on the card being present, so a car ferry inside a self-drive trip -- a real crossing
       that sells out -- was the one channel with no record of whether the traveller can buy from it.
    3. The round-trip-button rule counted per booking type, so a page showing two rail candidates
       where only the first was bookable passed the delivery gate.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import render, validate_plan  # noqa: PLC0415

    ground = json.loads((ROOT / "tests" / "ground-option.json").read_text(encoding="utf-8")) \
        if (ROOT / "tests" / "ground-option.json").exists() else None
    if ground is None:
        ground = {
            "id": "ground-1", "provider": "Deutsche Bahn", "comparison_platform": "NS International",
            "comparison_checked_at": "2026-09-01", "source_type": "official_provider",
            "checked_at": "2026-09-01", "review_url": "https://int.bahn.de/en",
            "origin_station": "Leiden Centraal", "destination_station": "Köln Hbf",
            "outbound_date": base["trip"]["start_date"], "return_date": base["trip"]["end_date"],
            "outbound_itinerary": {"service_identifier": "ICE 120", "departure_local": "08:12",
                                   "arrival_local": "11:04", "duration_minutes": 172, "stops": 0,
                                   "connection_or_terminal_note": "Through service"},
            "return_itinerary": {"service_identifier": "ICE 127", "departure_local": "17:12",
                                 "arrival_local": "20:04", "duration_minutes": 172, "stops": 0,
                                 "connection_or_terminal_note": "Through service"},
            "material_conditions": "Saver fare is train-bound and non-refundable",
            "availability_status": "available", "price_basis": "per_person_round_trip",
            "fare_low": 51, "fare_high": 61, "fare_currency": "EUR",
            "price_status": "estimate", "price_checked_at": "2026-09-01",
            "station_transfer_note": "Köln Hbf is 200 m from the cathedral",
            "round_trip_search_provider": "Deutsche Bahn",
            "round_trip_search_url": "https://int.bahn.de/en",
            "round_trip_search_checked_at": "2026-09-01",
            "round_trip_prefilled_fields": ["origin", "destination", "outbound_date",
                                            "return_date", "travellers"],
            "single_option_reason": "One carrier sells this route",
        }

    failures: list[str] = []

    # 1. The pill, and the through-train label with it. 直飞 means specifically "direct by air", so
    #    the flight-shaped substitution was calling a through train a direct flight.
    plan = copy.deepcopy(base)
    plan["trip"]["language"] = "zh"
    plan["booking_options"]["ground_transport"] = [copy.deepcopy(ground)]
    if validate_plan(plan):
        failures.append("ground-card: the worked option no longer validates")
    else:
        page = render(plan)
        card = re.search(r'<article class="option" data-option-kind="ground".*?</article>',
                         page, re.S)
        if card is None:
            failures.append("ground-card: no ground card rendered")
        else:
            text = re.sub(r"<[^>]+>", " ", card.group(0))
            if ">ground<" in card.group(0):
                failures.append("ground-card: the pill ships the raw English enum on a zh page")
            if "直飞" in text:
                failures.append("ground-card: a through train is labelled 直飞 (direct FLIGHT)")
            if "直达" not in text:
                failures.append("ground-card: a zero-change train is not labelled 直达")

    # 2. Access check keyed on the card, not the mobility mode: a ferry inside a self-drive trip.
    #    Removing the check from a self-drive plan is what isolates the rule -- on a public-transit
    #    plan the mode trigger would cover for it and the case would prove nothing.
    plan = copy.deepcopy(base)
    plan["transport_preference"]["mode"] = "self-drive"
    plan["booking_options"]["ground_transport"] = [copy.deepcopy(ground)]
    checks = plan["regional_service_context"]["booking_access_checks"]
    kept = [check for check in checks
            if isinstance(check, dict) and check.get("category") != "rail_or_ground"]
    if len(kept) == len(checks):
        failures.append("ground-card: the fixture no longer carries a rail_or_ground access "
                        "check, so this case can no longer isolate the rule")
    plan["regional_service_context"]["booking_access_checks"] = kept
    if not any("rail_or_ground" in error for error in validate_plan(plan)):
        failures.append("ground-card: a bookable crossing inside a self-drive trip needs no "
                        "booking-access check -- the one category keyed on something other "
                        "than 'is this card here'")

    # 3. One search button per card, not one per page.
    plan = copy.deepcopy(base)
    second = copy.deepcopy(ground)
    second.update(id="ground-2", provider="NS International",
                  review_url="https://www.nsinternational.com/en",
                  round_trip_search_url="https://www.nsinternational.com/en")
    second.pop("single_option_reason", None)
    first = copy.deepcopy(ground)
    first.pop("single_option_reason", None)
    plan["booking_options"]["ground_transport"] = [first, second]
    if validate_plan(plan):
        failures.append("ground-card: two distinct compared rail options were rejected")
    else:
        page = render(plan)
        cards = re.findall(r'<article class="option" data-option-kind="ground".*?</article>',
                           page, re.S)
        if len(cards) != 2:
            failures.append(f"ground-card: expected two ground cards, rendered {len(cards)}")
        else:
            stripped = page.replace(
                cards[1], re.sub(r'<a class="booking-link"[^>]*data-booking-purpose='
                                 r'"round-trip-search".*?</a>', "", cards[1], flags=re.S))
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "two-rail.html"
                path.write_text(stripped, encoding="utf-8")
                proc = subprocess.run(
                    [sys.executable, str(ROOT / "scripts" / "validate_trip_html.py"), str(path),
                     "--require-booking-type", "ground"],
                    capture_output=True, text=True)
                if proc.returncode == 0:
                    failures.append("ground-card: a second rail candidate with no search button of "
                                    "its own passed the delivery gate -- the traveller compares "
                                    "two fares and can act on one")
    return failures


def malformed_value_cases(base: dict) -> list[str]:
    """A believable authoring typo must be reported, not raised.

    `set(prefilled_fields)` and `status not in {...}` both take author-supplied values, so writing
    `[{"origin": "Leiden"}]` -- plausible, since the itinerary fields beside it really are objects
    -- killed validate_plan with `TypeError: unhashable type: 'dict'` and a bare traceback, instead
    of the one-line reason the rule exists to print. The same hole was on the flight branch from
    the start.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import (  # noqa: PLC0415
        REQUIRED_FLIGHT_SEARCH_FIELDS, PRICE_STATUSES, has_search_fields, is_one_of, validate_plan)

    failures: list[str] = []

    # The two shared guards, directly: every booking category routes through them, and a fixture
    # carrying one option of every kind does not exist to prove it end to end.
    for value, label in (([{"origin": "Leiden"}], "a dict element"), ([["origin"]], "a list element"),
                         ("origin,destination", "a bare string"), (None, "null")):
        try:
            if has_search_fields(value, REQUIRED_FLIGHT_SEARCH_FIELDS):
                failures.append(f"malformed: has_search_fields accepted {label}")
        except Exception as exc:  # noqa: BLE001 - a raise IS the defect
            failures.append(f"malformed: has_search_fields({label}) raised {type(exc).__name__}")
    for value, label in ((["available"], "a list"), ({"is": "x"}, "a dict"), (None, "null")):
        for allowed, name in (({"available", "limited", "unknown"}, "availability_status"),
                              (PRICE_STATUSES, "price_status")):
            try:
                if is_one_of(value, allowed):
                    failures.append(f"malformed: is_one_of accepted {label} for {name}")
            except Exception as exc:  # noqa: BLE001
                failures.append(f"malformed: is_one_of({label}) raised {type(exc).__name__}")

    # And end to end on the category the fixture can carry, because a helper that is correct and
    # not called is the same defect wearing a different hat.
    ground = {
        "id": "ground-1", "provider": "Deutsche Bahn", "source_type": "official_provider",
        "checked_at": "2026-09-01", "review_url": "https://int.bahn.de/en",
        "origin_station": "Leiden Centraal", "destination_station": "Köln Hbf",
        "outbound_date": base["trip"]["start_date"], "return_date": base["trip"]["end_date"],
        "outbound_itinerary": {"service_identifier": "ICE 120", "departure_local": "08:12",
                               "arrival_local": "11:04", "duration_minutes": 172, "stops": 0,
                               "connection_or_terminal_note": "Through service"},
        "return_itinerary": {"service_identifier": "ICE 127", "departure_local": "17:12",
                             "arrival_local": "20:04", "duration_minutes": 172, "stops": 0,
                             "connection_or_terminal_note": "Through service"},
        "material_conditions": "Saver fare is train-bound", "availability_status": "available",
        "price_basis": "per_person_round_trip", "fare_low": 51, "fare_high": 61,
        "fare_currency": "EUR", "price_status": "estimate", "price_checked_at": "2026-09-01",
        "station_transfer_note": "200 m from the cathedral",
        "round_trip_search_provider": "Deutsche Bahn",
        "round_trip_search_url": "https://int.bahn.de/en",
        "round_trip_search_checked_at": "2026-09-01",
        "round_trip_prefilled_fields": ["origin", "destination", "outbound_date", "return_date",
                                        "travellers"],
        "single_option_reason": "One carrier sells this route",
    }
    for field, value, label in (
        ("round_trip_prefilled_fields", [{"origin": "Leiden"}], "a dict inside prefilled_fields"),
        ("availability_status", ["available"], "a list availability_status"),
        ("price_status", {"is": "estimate"}, "a dict price_status"),
        ("id", ["ground-1"], "a list id"),
        ("review_url", None, "a null review_url"),
    ):
        plan = copy.deepcopy(base)
        plan["booking_options"]["ground_transport"] = [dict(ground, **{field: value})]
        try:
            errors = validate_plan(plan)
        except Exception as exc:  # noqa: BLE001 - a raise IS the defect
            failures.append(f"malformed: {label} raised {type(exc).__name__}: {exc} "
                            f"instead of being reported")
            continue
        if not errors:
            failures.append(f"malformed: {label} was accepted silently")
    return failures


def untyped_constraints_cases(base: dict) -> list[str]:
    """"Nobody typed it" must be loud, and must never be confused with "genuinely none".

    The defect: new_plan_skeleton.py emitted `allergy_severity: "none"` and
    `max_continuous_walking_minutes: null` -- values that read as answers -- for two fields it
    cannot possibly know, because the intake form collects both as prose and nothing turns a
    sentence into an enum or a number. Measured on a real five-day plan, with those defaults
    untouched, deleting EVERY activity's `on_foot_minutes` changed the finding count from 2 to 2
    (check_walking_budget arms itself off `cap is not None`), while the same deletion against a
    typed cap of 25 produced five precise findings. And SKILL.md allows the light verification tier
    only when the severity is none/preference AND the cap is null, so the untouched defaults were
    also exactly what bought the cheaper pass.

    Two properties are asserted here and neither is optional on its own:

      1. the marker fails, in a message that names the field and says what to write; and
      2. a legitimately typed `none` / null passes, with no marker anywhere -- because
         audit_workspace.py replays these same checks over every plan already saved in a
         workspace, and a check that fired on the VALUE rather than on the SENTINEL would
         retroactively invalidate all of them. The precedent is written down at
         render_final_trip_html.intake_context_errors, which lives outside validate_plan for
         exactly that reason.
    """
    marker = CHECKER_MODULE.UNTYPED_CONSTRAINTS_MARKER
    failures: list[str] = []

    def findings(plan: dict) -> list[str]:
        errors: list[str] = []
        CHECKER_MODULE.check_untyped_constraints(plan, errors, [])
        return errors

    def with_constraints(block: object) -> dict:
        plan = copy.deepcopy(base)
        plan["trip"]["traveler_constraints"] = block
        return plan

    # 1. Silence on everything that is not the sentinel. The absent-block case is the shape twelve
    #    of the fifteen plans in the measured workspace have, and the typed-cap case is the other
    #    three; both must go on producing byte-identical findings after this check exists.
    quiet = {
        "no traveler_constraints block at all": copy.deepcopy(base),
        "a typed 'none' severity and a null cap": with_constraints(constraints()),
        "a typed severity and a typed cap": with_constraints(
            constraints(allergy_severity="severe", max_continuous_walking_minutes=25)),
        "an emptied marker (dict)": with_constraints(constraints(**{marker: {}})),
        "an emptied marker (list)": with_constraints(constraints(**{marker: []})),
        "a null marker": with_constraints(constraints(**{marker: None})),
    }
    quiet["no traveler_constraints block at all"]["trip"].pop("traveler_constraints", None)
    for label, plan in quiet.items():
        if found := findings(plan):
            failures.append(f"untyped: {label} must not fire the sentinel check, got {found}")

    # 2. The sentinel itself, in the shape new_plan_skeleton.py writes it. The message has to name
    #    the field, because "a constraint was not typed" sends the author to read a whole block.
    both = with_constraints(constraints(**{marker: {
        "allergy_severity": "TODO: type the severity",
        "max_continuous_walking_minutes": "TODO: type the minutes",
    }}))
    found = findings(both)
    if len(found) != 2:
        failures.append(f"untyped: the skeleton's marker must report both fields, got {found}")
    for field in ("allergy_severity", "max_continuous_walking_minutes"):
        if not any(field in error for error in found):
            failures.append(f"untyped: the marker's report never names {field}: {found}")
    if not any("none | preference | intolerance | severe" in error for error in found):
        failures.append(
            f"untyped: the severity error must quote the enum the author has to choose from, so "
            f"the message says what to write and not only what is wrong: {found}")

    # And end to end through the CLI's own exit code, because a check that is correct in-process
    # and absent from PLAN_CHECKS is a check nothing runs.
    code, out = run(both)
    if code != 1 or "was never typed" not in out:
        failures.append(f"untyped: the marker must fail check_plan_consistency, got exit {code}\n{out}")
    if CHECKER_MODULE.check_untyped_constraints not in CHECKER_MODULE.PLAN_CHECKS:
        failures.append(
            "untyped: check_untyped_constraints is not in PLAN_CHECKS, so neither "
            "save_trip_deliverables.py nor audit_workspace.py would ever run it")

    # 3. One field typed and the other still marked: the author who does half the job must be told
    #    which half is left, and must not be told about the half they finished.
    half = with_constraints(constraints(allergy_severity="preference",
                                        **{marker: {"max_continuous_walking_minutes": "TODO: x"}}))
    found = findings(half)
    if len(found) != 1 or "max_continuous_walking_minutes" not in found[0]:
        failures.append(f"untyped: a half-cleared marker must report only the field left, got {found}")
    if "allergy_severity" in "".join(found):
        failures.append(f"untyped: a cleared field must not still be reported: {found}")

    # 4. Shapes nobody planned for. A hand-edited plan is the normal case -- the whole point of the
    #    marker is that a human deletes entries from it -- so every believable malformation has to
    #    produce a sentence rather than a traceback, and none of them may go quiet: a marker whose
    #    shape the gate cannot read is still a question nobody answered.
    for label, block in (
        ("a list of field names", constraints(**{marker: ["allergy_severity"]})),
        ("a bare string", constraints(**{marker: "TODO: type them both"})),
        ("a number", constraints(**{marker: 2})),
        ("a boolean", constraints(**{marker: True})),
        ("a field name that is not one of the two", constraints(**{marker: {"pace": "TODO: x"}})),
        ("a non-ASCII field name", constraints(**{marker: {"步行上限": "TODO: 填写"}})),
        ("a marker naming a field the block does not carry",
         {k: v for k, v in constraints(**{marker: {"allergy_severity": "TODO: x"}}).items()
          if k != "allergy_severity"}),
    ):
        plan = with_constraints(block)
        try:
            found = findings(plan)
        except Exception as exc:  # noqa: BLE001 - a raise IS the defect
            failures.append(f"untyped: {label} raised {type(exc).__name__}: {exc}")
            continue
        if not found:
            failures.append(f"untyped: {label} was accepted silently")

    # 5. And the containers the check reaches through. A plan whose trip or constraints block is
    #    the wrong type must not take the whole run down with it -- every other finding in the
    #    report is lost with it, which is how one typo hides twenty real defects.
    for label, plan in (
        ("trip as a list", {"trip": [], "days": []}),
        ("trip as a string", {"trip": "Malaga", "days": []}),
        ("traveler_constraints as a string", with_constraints("no allergies, walks fine")),
        ("traveler_constraints as a list", with_constraints(["no allergies"])),
        ("an empty plan", {}),
    ):
        try:
            findings(plan)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"untyped: {label} raised {type(exc).__name__}: {exc}")

    # 6. The scalar spellings of "nothing here is untyped". `false` and `0` were refused -- "is a
    #    bool (False). It must be an object keyed by the constraint fields nobody has typed yet" --
    #    while `""`, `{}` and `[]`, the same sentence written in a container, passed. Measured
    #    before the fix: False -> 1 error, 0 -> 1 error, 0.0 -> 1 error, "" -> 0, {} -> 0, [] -> 0.
    #    The truthy scalars stay refused, and the line between them is not truthiness for its own
    #    sake: `false` and `0` have exactly one reading, while `true` and `3` assert that a question
    #    is open and then name nothing, which is indistinguishable from an author who set out to
    #    list the open fields and stopped.
    for label, value in (("false", False), ("zero", 0), ("zero written as a float", 0.0)):
        if found := findings(with_constraints(constraints(**{marker: value}))):
            failures.append(
                f"untyped: a marker of {label} says 'nothing here is untyped' and must be accepted "
                f"the way {{}} and [] already are, got {found}")
    for label, value in (("true", True), ("a non-zero number", 3), ("a bare word", "yes")):
        if not findings(with_constraints(constraints(**{marker: value}))):
            failures.append(
                f"untyped: a marker of {label} names no field anybody can act on and must still "
                f"be refused")

    # 7. The readers of this one key must agree about every shape of it, because the defect in 6
    #    was not a wrong answer -- it was two answers. required_domains_for asks `if untyped:` and
    #    withholds the light verification tier; check_untyped_constraints refuses the plan. On
    #    `false` they disagreed: the tier said "nothing untyped, take the cheap pass" and the gate
    #    said "unreadable marker, fix it", about the same plan on the same run. This pins the
    #    agreement rather than the implementation, so a future reader added anywhere is caught the
    #    first time it drifts.
    for label, value in (("false", False), ("zero", 0), ("an empty object", {}),
                         ("an empty list", []), ("an empty string", ""),
                         ("the skeleton's own marker", {"allergy_severity": "TODO: x"}),
                         ("a list of names", ["allergy_severity"]),
                         ("true", True), ("a number", 3), ("a bare word", "yes")):
        plan = with_constraints(constraints(**{marker: value}))
        gate_open = bool(findings(plan))
        _, reason = CHECKER_MODULE.required_domains_for(plan)
        tier_open = marker in reason
        if gate_open != tier_open:
            failures.append(
                f"untyped: the gate and the verification tier disagree about a marker of {label}: "
                f"check_untyped_constraints {'refuses' if gate_open else 'accepts'} it while the "
                f"tier {'withholds' if tier_open else 'grants'} the light pass. One key cannot "
                f"mean two things.\ntier reason: {reason}")

    # 8. And the note check_walking_budget prints about a null cap has to FOLLOW the marker. It
    #    said "Not an error -- this traveller stated no walking limit" once per day on exactly the
    #    untyped state the marker exists to deny. Measured on a freshly generated three-day
    #    skeleton: one report carried three copies of that sentence AND both
    #    check_untyped_constraints errors, one of them "max_continuous_walking_minutes was never
    #    typed -- untyped_constraints still names it". Two claims about one field in one report,
    #    and the reassuring one was the false one -- which is the direction that gets a plan
    #    delivered.
    STATED = "stated no walking limit"

    def walking_notes(plan: dict) -> list[str]:
        errors: list[str] = []
        notes: list[str] = []
        CHECKER_MODULE.check_walking_budget(plan, errors, notes)
        return notes

    for label, block in (
        ("the skeleton's marker", constraints(**{marker: {
            "max_continuous_walking_minutes": "TODO: type the minutes"}})),
        ("a list-shaped marker", constraints(**{marker: ["max_continuous_walking_minutes"]})),
    ):
        got = walking_notes(with_constraints(block))
        if [note for note in got if STATED in note]:
            failures.append(
                f"untyped: with {label} naming the cap, the walking note still tells the reader the "
                f"traveller stated no limit -- the same report that says nobody typed it: {got}")
        if not any(marker in note for note in got):
            failures.append(
                f"untyped: with {label} naming the cap, the walking note says nothing about the "
                f"cap being untyped, so the day reads as measured when nothing measured it: {got}")

    # The other half, and it is not optional: a traveller who genuinely said "no limit" is a real
    # case and the original sentence was right about it. Silencing that note along with the false
    # one would trade a wrong sentence for a missing one.
    for label, block in (
        ("no marker at all", constraints()),
        ("an emptied marker", constraints(**{marker: {}})),
        ("a marker of false", constraints(**{marker: False})),
        ("a marker naming only the other field", constraints(**{marker: {
            "allergy_severity": "TODO: type the severity"}})),
    ):
        if not any(STATED in note for note in walking_notes(with_constraints(block))):
            failures.append(
                f"untyped: with {label} the null cap IS the traveller's answer, and the note that "
                f"says so must still print")

    # An unreadable marker must claim neither, because nobody can tell which it is. Routing it to
    # the "stated no walking limit" wording would rebuild the contradiction one shape to the left.
    unreadable = walking_notes(with_constraints(constraints(**{marker: "TODO: type them both"})))
    if [note for note in unreadable if STATED in note]:
        failures.append(
            f"untyped: an unreadable marker is not a traveller stating no walking limit; the note "
            f"must not say it is: {unreadable}")
    return failures





def verification_tier_note_cases(base: dict) -> list[str]:
    """The tier has to be printed where the decision is made, not after it is paid for.

    SKILL.md says of the light/full choice: "check_plan_consistency.py computes this from the
    plan's own fields, so do not argue with it -- read what it printed." That was not true.
    required_domains_for had exactly one call site, inside check_verification, and
    check_verification is not in PLAN_CHECKS -- it runs only when a finished verification report is
    handed in. The tier was computed after the verification had been bought, which is the one
    moment it cannot help.

    references/research-budget.md prices the difference between the tiers, and across fifteen real
    saved plans every one computes `full` -- so nobody has ever been told they could have stopped
    at four blocks. Both halves are asserted here: the note appears on an ordinary plan, and it
    says LIGHT on a plan that actually qualifies. Without the second, the whole thing could be a
    constant.
    """
    failures: list[str] = []

    def notes_for(plan: dict) -> list[str]:
        errors: list[str] = []
        notes: list[str] = []
        CHECKER_MODULE.check_verification_tier_is_stated(plan, errors, notes)
        if errors:
            failures.append(f"tier note: it must refuse nothing, got {errors}")
        return notes

    tier_notes = [n for n in notes_for(copy.deepcopy(base)) if "verification tier" in n]
    if not tier_notes:
        failures.append("tier note: an ordinary plan got no tier line, so the sentence SKILL.md "
                        "tells the author to read is still not printed")
    elif "FULL" not in tier_notes[0]:
        failures.append(f"tier note: the fixture needs the full pass and the note does not say so: "
                        f"{tier_notes[0]}")

    # A plan that genuinely qualifies for the cheap pass, built by satisfying the conditions
    # required_domains_for itself names -- so this cannot drift out of step with the rule.
    light = copy.deepcopy(base)
    for _ in range(8):
        required, reason = CHECKER_MODULE.required_domains_for(light)
        if required <= CHECKER_MODULE.LIGHT_TIER_DOMAINS:
            break
        if "no entry_context" in reason:
            light["entry_context"] = {"status": "not_required"}
        elif "no traveler_constraints" in reason:
            light["trip"]["traveler_constraints"] = {
                "dietary_or_religious_needs": [], "allergy_severity": "none",
                "allergy_card_text": None, "max_continuous_walking_minutes": None,
                "mobility_notes": []}
        else:
            break
    required, _reason = CHECKER_MODULE.required_domains_for(light)
    if required <= CHECKER_MODULE.LIGHT_TIER_DOMAINS:
        light_notes = [n for n in notes_for(light) if "verification tier" in n]
        if not light_notes or "LIGHT" not in light_notes[0]:
            failures.append(f"tier note: a plan that qualifies for the light tier was not told so, "
                            f"which makes the note a constant: {light_notes}")
        elif "4 block" not in light_notes[0]:
            failures.append(f"tier note: the light tier is four blocks and the note must say how "
                            f"many, since that is the number the author is deciding about: "
                            f"{light_notes[0]}")
    else:
        failures.append("tier note: could not build a light-tier plan from the conditions "
                        "required_domains_for names, so the LIGHT half is asserted over nothing")

    # And it must not raise on the shapes a plan can arrive in, because a note-only check that
    # dies takes every real finding in the report with it.
    for label, plan in (("an empty plan", {}), ("no days", {"trip": {}}),
                        ("days as a string", {"trip": {}, "days": "nope"}),
                        ("trip as a list", {"trip": [], "days": [{}]})):
        try:
            CHECKER_MODULE.check_verification_tier_is_stated(plan, [], [])
        except Exception as exc:  # noqa: BLE001 - a raise IS the defect
            failures.append(f"tier note: {label} raised {type(exc).__name__}: {exc}")
    return failures


def preferences_from_the_intake_cases(base: dict) -> list[str]:
    """The form's answers must reach the plan, checked against the form's own file.

    check_preference_coverage iterates ranked_must_haves, so an empty list produces nothing, and
    its docstring blesses that as "the traveller stated no must-have". Measured on a real workspace
    of fifteen saved plans it is empty on all fifteen -- so that check, and every rule downstream of
    it, has never fired. The intake files refute the innocent reading: SEVEN of the fifteen intakes
    in the same workspace carry a non-empty experience.ranked_must_haves and no plan carries any.
    The answers stopped at the plan boundary, and a gate that binds only what the author chose to
    transcribe cannot see a transcription that did not happen.

    The unreadable-intake case is a NOTE on purpose and is asserted here so it stays one. A plan is
    a portable document -- re-rendered, replanned, audited from a moved workspace -- and
    render_final_trip_html.intake_context_errors records that requiring intake_file to resolve was
    tried and reverted, because it failed every legitimate re-save and the way out the error
    suggested was to relabel the intake method, i.e. to write something false.
    """
    failures: list[str] = []

    def findings(plan: dict) -> tuple[list[str], list[str]]:
        errors: list[str] = []
        notes: list[str] = []
        CHECKER_MODULE.check_preferences_came_from_the_intake(plan, errors, notes)
        return errors, notes

    def paired(tmp: Path, collected: object, carried: object) -> dict:
        intake = tmp / "intake.json"
        intake.write_text(json.dumps({"experience": {"ranked_must_haves": collected}},
                                     ensure_ascii=False), encoding="utf-8")
        plan = copy.deepcopy(base)
        plan["intake_context"] = {"method": "html_form", "intake_file": str(intake)}
        plan.setdefault("trip", {}).setdefault("traveler_preferences", {})
        plan["trip"]["traveler_preferences"]["ranked_must_haves"] = carried
        return plan

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        # CJK, because the workspace this runs on is majority Chinese and a check that only held
        # for ASCII would hold for almost none of it.
        wanted = ["海岛/海岸", "湖泊/森林"]

        errors, _ = findings(paired(tmp, wanted, []))
        if not errors:
            failures.append("intake preferences: a plan carrying none of the two must-haves the "
                            "intake collected was accepted -- that is the measured defect")
        elif not all(w in errors[0] for w in wanted):
            failures.append(f"intake preferences: the refusal must name what was dropped, so the "
                            f"author does not have to diff two files: {errors[0]}")

        errors, _ = findings(paired(tmp, wanted, list(wanted)))
        if errors:
            failures.append(f"intake preferences: a plan carrying both was refused: {errors}")

        errors, _ = findings(paired(tmp, wanted, wanted[:1]))
        if len(errors) != 1 or wanted[1] not in errors[0] or wanted[0] in errors[0]:
            failures.append(f"intake preferences: a partial carry must name only what is missing: "
                            f"{errors}")

        # An intake that collected nothing is not evidence of anything.
        for label, collected in (("an empty list", []), ("a missing key", None),
                                 ("a list of blanks", ["", "   "])):
            plan = paired(tmp, collected, [])
            errors, _ = findings(plan)
            if errors:
                failures.append(f"intake preferences: {label} in the intake produced {errors}")

        # Whatever a caller can put in that field, this must not raise: a gate that dies takes
        # every other finding in the report with it.
        for label, shape in (("a string intake", '"nope"'), ("a list intake", "[1, 2]"),
                             ("a number intake", "7"), ("a truncated file", '{"experience":')):
            broken = tmp / f"broken-{abs(hash(label))}.json"
            broken.write_text(shape, encoding="utf-8")
            plan = copy.deepcopy(base)
            plan["intake_context"] = {"method": "html_form", "intake_file": str(broken)}
            try:
                errors, notes = findings(plan)
            except Exception as exc:  # noqa: BLE001 - a raise IS the defect
                failures.append(f"intake preferences: {label} raised "
                                f"{type(exc).__name__}: {exc}")
                continue
            if errors:
                failures.append(f"intake preferences: {label} was refused rather than noted: "
                                f"{errors}")
            if not notes:
                failures.append(f"intake preferences: {label} said nothing at all, so a run that "
                                f"could not cross-check looks exactly like one that did")

        # The portable-document rule, pinned: a missing sibling file costs the check, not the plan.
        gone = copy.deepcopy(base)
        gone["intake_context"] = {"method": "html_form",
                                  "intake_file": str(tmp / "never-written.json")}
        errors, notes = findings(gone)
        if errors:
            failures.append(f"intake preferences: an unreadable intake refused the plan, which is "
                            f"the rule intake_context_errors already tried and reverted: {errors}")
        if not notes:
            failures.append("intake preferences: an unreadable intake must SAY the cross-check did "
                            "not run; silence makes it indistinguishable from a clean pass")

    # And no intake_context at all is not this check's business.
    bare = copy.deepcopy(base)
    bare.pop("intake_context", None)
    errors, notes = findings(bare)
    if errors or notes:
        failures.append(f"intake preferences: a plan naming no intake file must produce nothing, "
                        f"got {errors} / {notes}")
    return failures


def dates_versus_the_gate_stamp_cases(base: dict) -> list[str]:
    """A delivered plan whose dates moved with nothing saying they moved.

    check_replan_context is the gate for a date change and it opens with `if context is None:
    return`, so it never sees the case it exists for: replan_trip.py writes replan_context, and the
    author who edits two date strings by hand writes nothing. Every weekday-keyed fact under a day
    -- opening hours, closure days, market days, the museum that shuts Mondays -- is then a guess
    while the plan still reads as checked. SKILL.md records the measured cost: a one-day shift
    redone by hand put an off-by-one in every ticket and every anchor day index.

    Asking the author to declare the edit cannot work, because not declaring it is the edit. So the
    check reads the receipt: save_trip_deliverables.py stamps the window the gates ran against into
    `gates_passed` AFTER the checks run, so a plan delivered and then hand-edited disagrees with its
    own record.

    Half these cases are about staying quiet, and that half is not optional. A check that accuses
    honest work is a check people route around, and three shapes here are honest: a plan that was
    never delivered, a stamp written before this field existed (one plan in a real workspace has
    exactly that), and a shift that declared itself.
    """
    failures: list[str] = []
    marker = CHECKER_MODULE.gates_stamp

    def findings(plan: dict) -> list[str]:
        errors: list[str] = []
        CHECKER_MODULE.check_dates_agree_with_the_gates_that_ran(plan, errors, [])
        return errors

    def delivered(**trip_overrides) -> dict:
        """A plan carrying the stamp its own dates would have produced."""
        plan = copy.deepcopy(base)
        plan["gates_passed"] = marker(plan)
        plan["trip"].update(trip_overrides)
        return plan

    if not findings(delivered(start_date="2026-10-05")):
        failures.append(
            "dates/stamp: a delivered plan whose start_date moved with no replan_context was "
            "accepted -- that is the hand edit this check exists for, and the one shape "
            "check_replan_context cannot see")
    if not findings(delivered(end_date="2026-10-30")):
        failures.append("dates/stamp: only the start of the window is checked; a moved end_date "
                        "re-keys the same weekday-dependent facts")

    quiet = {
        "a plan that was never delivered": copy.deepcopy(base),
        "a stamp written before the window was recorded": {**copy.deepcopy(base),
                                                           "gates_passed": {"checks": 24}},
    }
    agreeing = copy.deepcopy(base)
    agreeing["gates_passed"] = marker(agreeing)
    quiet["a stamp that agrees with the plan"] = agreeing
    declared = delivered(start_date="2026-10-05")
    declared["replan_context"] = {"must_reverify": []}
    quiet["a shift that declared itself in replan_context"] = declared
    for label, plan in quiet.items():
        if found := findings(plan):
            failures.append(f"dates/stamp: {label} must produce nothing, got {found}")

    # The shapes a plan can actually carry in that key. A gate that raises here takes every other
    # finding in the report down with it, which is how one typo hides two dozen real defects.
    for label, stamp in (("a string", "nope"), ("a list", [1, 2]), ("null", None),
                         ("a number", 7), ("an empty object", {}),
                         ("a non-string date", {"checks": 24, "start_date": 20261005}),
                         ("a blank date", {"checks": 24, "start_date": "   "})):
        plan = copy.deepcopy(base)
        plan["gates_passed"] = stamp
        plan["trip"]["start_date"] = "2026-10-05"
        try:
            findings(plan)
        except Exception as exc:  # noqa: BLE001 - a raise IS the defect
            failures.append(f"dates/stamp: gates_passed as {label} raised "
                            f"{type(exc).__name__}: {exc}")

    # And the stamp itself has to carry the window, or the check above is asserted over nothing.
    stamped = marker(copy.deepcopy(base))
    if stamped.get("start_date") != base["trip"].get("start_date"):
        failures.append(f"dates/stamp: gates_stamp did not record the window it checked: {stamped}")
    if "checks" not in stamped or "checked_by" not in stamped:
        failures.append(f"dates/stamp: gates_stamp dropped what it already recorded: {stamped}")
    # No wall-clock: two saves of one plan must be diffable.
    if marker(copy.deepcopy(base)) != stamped:
        failures.append("dates/stamp: gates_stamp is not deterministic, so two saves of the same "
                        "plan differ and the stamp stops being diffable")
    return failures


def untyped_marker_entry_cases(base: dict) -> list[str]:
    """A loud message that points at nothing is the same failure wearing a different coat.

    The marker's job is to make "nobody typed this" impossible to miss, and the check builds its
    message by interpolating the entry into a field path. Measured before the fix, an entry keyed
    on the empty string produced:

        - trip.traveler_constraints. was never typed -- untyped_constraints still names it ...

    a path with nothing after the dot, telling the author to go and type a field the sentence never
    names. List entries holding a non-string member produced the same shape one container to the
    left. Neither is a wrong answer about the plan -- both are the check failing to say which field
    it means, which costs the author the one thing this marker exists to give them.

    So the property asserted here is not "these shapes error". It is that NO message this check can
    emit ever ends its field path at a bare dot, whatever the author put in the marker -- and that
    an entry nobody can read is still refused rather than skipped, because a silently dropped entry
    returns the plan to the state the marker was added to end.
    """
    marker = CHECKER_MODULE.UNTYPED_CONSTRAINTS_MARKER
    failures: list[str] = []

    # The defect is the field path these messages OPEN with stopping at the dot, so the pattern is
    # anchored at the start of the message rather than searched for anywhere in it. Written
    # unanchored first, it fired on two correct messages: the prose that explains an unrecognised
    # key legitimately ends a sentence with "... is not even present in trip.traveler_constraints."
    # before starting the next one. A test that cannot tell a field path from a full stop reports
    # the defect it was written to catch on exactly the runs where the code is right.
    dangling = re.compile(r"^trip\.traveler_constraints\.(?=\s|$)")

    def findings(block: object) -> list[str]:
        plan = copy.deepcopy(base)
        plan["trip"]["traveler_constraints"] = block
        errors: list[str] = []
        CHECKER_MODULE.check_untyped_constraints(plan, errors, [])
        return errors

    # Every shape an author can put in the marker that names no field. Each must be refused, must
    # not raise, and must not produce the dangling path. The two well-formed rows at the end are the
    # control: they prove the check still names a real field, so a fix that silenced everything
    # cannot pass this by producing no messages at all.
    for label, block, must_error in (
        ("an empty-string key", constraints(**{marker: {"": "TODO: x"}}), True),
        ("a whitespace-only key", constraints(**{marker: {"   ": "TODO: x"}}), True),
        ("a non-string key", constraints(**{marker: {7: "TODO: x"}}), True),
        ("a list holding a non-string member",
         constraints(**{marker: ["allergy_severity", 7]}), True),
        ("a list holding an empty string",
         constraints(**{marker: ["allergy_severity", ""]}), True),
        ("a list holding a nested container",
         constraints(**{marker: ["allergy_severity", ["max_continuous_walking_minutes"]]}), True),
        ("a key whose value is a nested container",
         constraints(**{marker: {"allergy_severity": {"note": "ask them"}}}), True),
        ("a key naming a field traveler_constraints does not carry",
         constraints(**{marker: {"not_a_field": "TODO: x"}}), True),
        ("a non-ASCII key naming no real field",
         constraints(**{marker: {"步行上限": "TODO: 填写"}}), True),
        ("a well-formed dict entry",
         constraints(**{marker: {"allergy_severity": "TODO: ask them"}}), True),
        ("a well-formed list entry",
         constraints(**{marker: ["max_continuous_walking_minutes"]}), True),
    ):
        try:
            found = findings(block)
        except Exception as exc:  # noqa: BLE001 - a raise takes every other finding down with it
            failures.append(f"untyped entry: {label} raised {type(exc).__name__}: {exc}")
            continue
        if must_error and not found:
            failures.append(
                f"untyped entry: {label} names no field anybody can act on and was accepted "
                f"silently, which returns the plan to the state the marker was added to end")
        for message in found:
            if dangling.search(message):
                failures.append(
                    f"untyped entry: {label} produced a field path that stops at the dot, so the "
                    f"message tells the author to type a field it never names: {message}")
    return failures


def constraints_panel_cases(base: dict) -> list[str]:
    """The traveller's hard constraints must reach the page they carry.

    trip.traveler_constraints was validated by the renderer and rendered nowhere. For the run that
    prompted it, a severe triple allergy's entire mechanical effect was "run four more verification
    agents" -- and `allergy_card_text`, the sentence written to hand to restaurant staff, existed
    only in the JSON. Whether the allergy appeared on the page at all depended on the author having
    separately retyped it into free-text dining prose.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import render  # noqa: PLC0415 - import after path setup

    failures: list[str] = []
    plan = copy.deepcopy(base)
    plan["trip"]["traveler_constraints"] = {
        "dietary_or_religious_needs": ["ZZ-DAIRY-ZZ", "ZZ-NUT-ZZ"],
        "allergy_severity": "severe",
        "allergy_card_text": "ZZ-CARD-TEXT-ZZ",
        "max_continuous_walking_minutes": 27,
        "mobility_notes": ["ZZ-MOBILITY-ZZ"],
    }
    page = render(plan)
    for sentinel, label in (("ZZ-DAIRY-ZZ", "a dietary need"), ("ZZ-NUT-ZZ", "a second dietary need"),
                            ("ZZ-CARD-TEXT-ZZ", "the allergy card text"),
                            ("ZZ-MOBILITY-ZZ", "a mobility note"), ("27", "the walking cap")):
        if sentinel not in page:
            failures.append(f"constraints: {label} ({sentinel}) never reaches the page")
    if 'id="traveller-constraints"' not in page:
        failures.append("constraints: the panel is missing entirely")

    # A plan with no constraints must not grow an empty panel -- an empty heading reads as
    # "we checked and there is nothing", which is a different claim from "nobody asked".
    bare = copy.deepcopy(base)
    bare["trip"].pop("traveler_constraints", None)
    if 'id="traveller-constraints"' in render(bare):
        failures.append("constraints: a plan carrying none rendered an empty panel")
    return failures


def verification_banner_cases(base: dict) -> list[str]:
    """A plan saved with --unverified must say so on the page, not only in a JSON field.

    Whoever books from this plan reads the HTML; a machine-readable flag they never see is
    the same as no flag at all. The banner is renderer-owned copy, so on a non-English page
    it must localize completely -- validate_trip_html.py fails on renderer English otherwise.
    """
    sys.path.insert(0, str(ROOT / "scripts"))
    from render_final_trip_html import render  # noqa: PLC0415 - import after path setup

    failures: list[str] = []

    unverified = copy.deepcopy(base)
    unverified["verification_status"] = "unverified"
    page = render(unverified)
    if 'id="verification-notice"' not in page:
        failures.append("banner: an unverified plan rendered no verification notice")
    if "Not fact-checked" not in page:
        failures.append("banner: English page is missing the notice text")

    verified = copy.deepcopy(base)
    verified["verification_status"] = "verified"
    if 'id="verification-notice"' in render(verified):
        failures.append("banner: a verified plan rendered a notice it should not have")

    # A plan with NO verification_status must show the banner, not hide it. This case used to
    # assert the opposite, and that was the defect: the banner fired only on the literal string
    # "unverified", while the skeleton writes None, a plan that never reached the verification
    # stage keeps None, and replan_trip.py deliberately resets to None. So the default state of
    # every plan in the repo rendered as fully fact-checked, and a run that pointed
    # render_final_trip_html.py at the workspace landed both artifacts, passed validate_trip_html,
    # and produced a page a traveller would book from with no warning on it at all.
    if 'id="verification-notice"' not in render(copy.deepcopy(base)):
        failures.append("banner: a plan with no verification_status must still warn -- "
                        "unset is not verified")

    for absent in (None, "", "researched", "in_progress"):
        probe = copy.deepcopy(base)
        probe["verification_status"] = absent
        if 'id="verification-notice"' not in render(probe):
            failures.append(f"banner: verification_status={absent!r} must warn; only the literal "
                            f"'verified' may suppress the notice")

    zh = copy.deepcopy(base)
    zh["trip"]["language"] = "中文"
    zh["verification_status"] = "unverified"
    zh_page = render(zh)
    if "未经事实核验" not in zh_page:
        failures.append("banner: Chinese page did not localize the notice title")
    if "Not fact-checked" in zh_page or "skipped the five-domain" in zh_page:
        failures.append("banner: renderer English leaked onto the Chinese page")

    return failures


def repeated_rule_plan(base: dict, count: int = 6) -> dict:
    """A plan that trips one rule `count` times, each time about a different venue.

    The fixture is clean by construction, so a report with anything to deduplicate has to be
    built. Every part of these names is chosen to make the test adversarial rather than
    decorative. They END with the same characters, which is what real workspace venue names do
    ("...（当日择店）") and what makes a naive longest-common-suffix split cut INSIDE the name; the
    unique ASCII token in the middle makes "did this finding's own text survive" decidable; and
    the CJK makes it decidable for a language with no spaces, which is the half of the workspace a
    whitespace-shaped rule would quietly get wrong.

    Verified adversarial rather than assumed: removing the word-start rule from the estimate makes
    the case below report 9 lost tokens, and removing the closing-punctuation move makes it report
    5. A probe that passes no matter what the code does is not a test.
    """
    plan = copy.deepcopy(base)
    template = copy.deepcopy(plan["days"][0]["dining"][0])
    stops = []
    for index in range(count):
        stop = copy.deepcopy(template)
        stop["meal"] = ("breakfast", "lunch", "dinner")[index % 3]
        stop["venue_name"] = f"测试餐厅UniqueVenueToken{index}号（当日择店）"
        stop["venue_hours"] = ""
        stops.append(stop)
    plan["days"][0]["dining"] = stops
    return plan


def dedupe_cases(base: dict) -> list[str]:
    """The rule rationale is printed once; everything each finding says for itself survives.

    The property under test is NOT a byte count. It is that suppressing a repeated rationale
    cannot cost the reader anything only that finding said -- because a report that saves bytes by
    dropping which venue is broken sends the author back into the plan, which costs more than it
    saved. Tokens rather than raw substrings, and the difference is worth stating: a substring
    that STRADDLES the cut (the end of the venue name plus the first words of the rule) is by
    construction split across two printed lines, and no deduplication scheme of any shape can keep
    it contiguous. Both halves are printed; only the join is not. Every token, on either side of
    the cut, must still be there.
    """
    failures: list[str] = []
    plan = repeated_rule_plan(base)
    errors, notes, crashed = CHECKER_MODULE.run_plan_checks(plan)
    if crashed:
        return [f"dedupe: the probe plan crashed {crashed}, so nothing below was tested"]
    split = CHECKER_MODULE.split_findings(errors, errors.sites, errors.checks)
    legend, lines = CHECKER_MODULE.format_findings(split)
    printed = "\n".join(legend + lines)

    if len(lines) != len(errors):
        failures.append(f"dedupe: {len(errors)} findings printed as {len(lines)} lines; every "
                        f"finding must keep its own dashed line")

    repeated = [f for f in split if sum(1 for g in split if g.rule_id == f.rule_id) > 1]
    if not repeated:
        failures.append("dedupe: the probe plan produced no repeated rule, so this case proved "
                        "nothing -- rebuild it until one rule fires more than once")
    if not legend:
        failures.append("dedupe: a report with a repeated rule printed no legend, so a reader "
                        "landing on a back-reference has nothing telling them what it means")

    counts: dict[str, int] = {}
    for message in errors:
        for token in set(message.split()):
            counts[token] = counts.get(token, 0) + 1
    lost = sorted(token for token, seen in counts.items() if seen == 1 and token not in printed)
    if lost:
        failures.append(f"dedupe: {len(lost)} token(s) appear in exactly one finding and in none "
                        f"of the printed lines: {lost[:5]}")

    for finding in split:
        if finding.head + finding.tail != finding.message:
            failures.append(f"dedupe: head+tail does not rebuild the finding: {finding.head!r} + "
                            f"{finding.tail!r}")
            break

    # The scheme must never make a report bigger. A legend costs bytes whether or not the
    # deduplication it explains earns them back, and a "saving" that can go negative is one
    # nobody can reason about.
    plain = "\n".join(f.message for f in split)
    if len(printed) >= len(plain):
        failures.append(f"dedupe: printing {len(printed)} bytes where the undeduplicated report "
                        f"is {len(plain)} -- the repeated rule was not suppressed")

    # A report with nothing to share must come out byte-identical to what it printed before any of
    # this existed, or every clean-ish run pays for a feature it does not use.
    single = copy.deepcopy(base)
    single["days"][0]["dining"][0]["venue_hours"] = ""
    errors, _notes, _crashed = CHECKER_MODULE.run_plan_checks(single)
    split = CHECKER_MODULE.split_findings(errors, errors.sites, errors.checks)
    legend, lines = CHECKER_MODULE.format_findings(split)
    if legend or lines != list(errors):
        failures.append("dedupe: a report with no repeated rule was rewritten anyway; it must be "
                        "byte-identical to the plain finding list")
    return failures


def rule_split_cases() -> list[str]:
    """The head/tail cut, on the inputs that break a scheme tuned to one example.

    Empty, one finding, wrong-type, CJK with no spaces, and parallel lists that do not line up.
    The last one has to RAISE: a short sites list would print one rule's rationale under another
    rule's id, and a wrong attribution is worse than a missing one because it reads as an answer.
    """
    failures: list[str] = []
    module = CHECKER_MODULE

    if module.split_findings([]) != []:
        failures.append("split: an empty finding list must split to an empty list")
    if module.format_findings([]) != ([], []):
        failures.append("split: an empty split must print nothing at all")

    lone = module.split_findings(["day 1: something is wrong."])
    if len(lone) != 1 or lone[0].head + lone[0].tail != "day 1: something is wrong.":
        failures.append("split: a single finding with no site must survive intact")

    try:
        module.split_findings(["a", "b"], sites=[None], checks=["x", "y"])
    except ValueError:
        pass
    else:
        failures.append("split: parallel lists of different lengths must raise, not mis-attribute")

    # No spaces anywhere, which is the shape a Chinese message actually has. The estimate must
    # still refuse to cut inside a word: with no whitespace boundary there is nothing safe to
    # share, so it must share nothing rather than slice a name in half.
    cjk = ["东银座一带的餐厅没有营业时间", "浅草一带的餐厅没有营业时间"]
    for finding in module.split_findings(cjk):
        if finding.tail and " " not in finding.tail:
            failures.append(f"split: cut a space-free message at {finding.tail!r}, which can only "
                            f"be inside a word")

    if module._closing_punctuation("_url. Two options") != 0:
        failures.append("split: moved '_url.' to the head, which eats half a field name")
    if module._closing_punctuation("' has no venue_hours") != 1:
        failures.append("split: left the closing quote on the rule, so the head ends unbalanced")
    if module._closing_punctuation(" while hours_status is") != 0:
        failures.append("split: moved leading whitespace, which belongs to neither side")
    return failures


def pointer_cases(base: dict) -> list[str]:
    """Every pointer resolves against the plan it was derived from, or is None and says so.

    A pointer that does not resolve costs exactly the read it was meant to save, and teaches an
    author to stop reading the field -- which is worse than never having had it.
    """
    failures: list[str] = []
    module = CHECKER_MODULE
    plan = repeated_rule_plan(base)
    errors, _notes, _crashed = module.run_plan_checks(plan)
    split = module.split_findings(errors, errors.sites, errors.checks)
    placed = 0
    for finding in split:
        pointer = module.pointer_for(finding.head or finding.message, plan)
        if pointer is None:
            continue
        placed += 1
        if not module.resolve_pointer(plan, pointer):
            failures.append(f"pointer: {pointer!r} does not resolve against the plan it came from")
    if not placed:
        failures.append("pointer: nothing in this report was placed, so nothing was tested")

    if module.pointer_for("", plan) is not None:
        failures.append("pointer: empty text must place nothing")
    if module.pointer_for(None, plan) is not None:
        failures.append("pointer: a non-string must place nothing rather than raise")
    if module.pointer_for("day 1: x", []) is not None:
        failures.append("pointer: a plan that is not an object must place nothing rather than raise")
    if module.pointer_for("day 9999: nothing here", plan) is not None:
        failures.append("pointer: a day the plan does not have must place nothing")

    # The day is found by its own number field, not by position, because a replan can leave a
    # plan numbered 2,3,4 and positional arithmetic then points at the wrong day in silence.
    renumbered = copy.deepcopy(base)
    renumbered["days"][0]["number"] = 7
    if module.pointer_for("day 7: anything", renumbered) != "days[0]":
        failures.append("pointer: day 7 in a one-day plan numbered 7 must resolve to days[0]")
    if module.pointer_for("day 1: anything", renumbered) is not None:
        failures.append("pointer: day 1 must place nothing when no day is numbered 1")
    return failures


def json_output_cases(base: dict) -> list[str]:
    """--json is parseable on every exit, and rebuilds the prose findings exactly.

    Run through the real CLI rather than in-process: the point of the flag is that a wrapper can
    parse whatever comes back, and the exits that used to print a bare stderr line are the ones
    most likely to break it.
    """
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        def gate(plan: dict, *extra: str) -> tuple[int, str, str]:
            path = Path(tmp) / "plan.json"
            path.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
            proc = subprocess.run([sys.executable, str(CHECKER), str(path),
                                   "--no-verification-yet", *extra],
                                  capture_output=True, text=True)
            return proc.returncode, proc.stdout, proc.stderr

        code, out, err = gate(base, "--json")
        try:
            doc = json.loads(out)
        except ValueError as exc:
            return [f"json: a clean plan did not print valid JSON ({exc}): {out[:200]}"]
        if code != 0 or doc["ok"] is not True or doc["findings"]:
            failures.append(f"json: a clean plan must be ok with no findings, got {code} {doc['ok']}")

        # CJK, and a lot of it: ensure_ascii=False is what keeps the report readable, and a
        # \u-escaped one is both bigger and unsearchable.
        cjk_plan = repeated_rule_plan(base)
        code, out, err = gate(cjk_plan, "--json")
        try:
            doc = json.loads(out)
        except ValueError as exc:
            return [f"json: a CJK plan did not print valid JSON ({exc}): {out[:200]}"]
        if code != 1 or doc["ok"] is not False:
            failures.append(f"json: a plan with findings must exit 1 and say ok false, got {code}")
        if "测试餐厅UniqueVenueToken0号（当日择店）" not in out:
            failures.append("json: CJK was escaped or lost; the report has to stay searchable")
        for finding in doc["findings"]:
            if set(finding) != {"rule_id", "pointer", "message"}:
                failures.append(f"json: a finding carries {sorted(finding)}, not the three fields "
                                f"a caller is told to expect")
                break
            if finding["rule_id"] not in doc["rules"]:
                failures.append(f"json: {finding['rule_id']} has no entry in rules, so its "
                                f"reasoning is nowhere in the output")
                break
        if not any(f["pointer"] is None for f in doc["findings"]) and \
                not all(f["pointer"] for f in doc["findings"]):
            failures.append("json: pointer must be present on every finding, null or not")

        # The whole defence against this becoming a why-strip: message + its rule rebuilds the
        # finding the checks produced, byte for byte, so nothing was reworded and nothing dropped.
        # Compared against the checks' own output rather than against the printed prose, because
        # the prose is deduplicated too and comparing two compressions proves neither.
        raw, _notes, _crashed = CHECKER_MODULE.run_plan_checks(cjk_plan)
        rebuilt = [f["message"] + doc["rules"][f["rule_id"]] for f in doc["findings"]]
        if rebuilt != list(raw):
            failures.append(f"json: rebuilding the findings did not give back what the checks "
                            f"produced ({len(rebuilt)} against {len(raw)})")
            for built, original in zip(rebuilt, raw):
                if built != original:
                    failures.append(f"json: rebuilt {built[:90]!r} against {original[:90]!r}")
                    break
        _code, _out, err = gate(cjk_plan)
        prose = [line for line in err.splitlines() if line.startswith("- ")]
        if len(prose) != len(raw):
            failures.append(f"json: {len(raw)} findings printed as {len(prose)} dashed lines")
        for finding in doc["findings"]:
            if finding["pointer"] and not CHECKER_MODULE.resolve_pointer(cjk_plan,
                                                                        finding["pointer"]):
                failures.append(f"json: pointer {finding['pointer']!r} does not resolve")
                break

        # Refused before the plan is read: a wrapper that always passes --json must always get
        # JSON, including from the exits that are only a stderr line without it.
        path = Path(tmp) / "plan.json"
        path.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
        for argv, label in (
                ([str(CHECKER), str(path), "--json"], "no --verification"),
                ([str(CHECKER), str(Path(tmp) / "nope.json"), "--no-verification-yet", "--json"],
                 "unreadable plan"),
                ([str(CHECKER), str(path), "--verification", "", "--json"], "empty report path")):
            proc = subprocess.run([sys.executable, *argv], capture_output=True, text=True)
            if proc.returncode == 0:
                failures.append(f"json: {label} must not exit 0")
            try:
                refused = json.loads(proc.stdout)
            except ValueError as exc:
                failures.append(f"json: {label} printed unparseable stdout ({exc})")
                continue
            if refused["ok"] is not False or not refused["findings"]:
                failures.append(f"json: {label} produced JSON that does not say what went wrong")

        # --emit-walking honours the flag too, for the same reason.
        proc = subprocess.run([sys.executable, str(CHECKER), str(path), "--emit-walking", "--json"],
                              capture_output=True, text=True)
        try:
            walking = json.loads(proc.stdout)
        except ValueError as exc:
            failures.append(f"json: --emit-walking did not print valid JSON ({exc})")
        else:
            if not walking.get("walking"):
                failures.append("json: --emit-walking printed no walking totals")

        # A check that raises must not take the JSON down with it: the run is incomplete, which is
        # exit 2 and a finding that says so, not a traceback where the report should be.
        crasher = Path(tmp) / "crashing_gate.py"
        crasher.write_text(
            "import importlib.util, sys\n"
            f"spec = importlib.util.spec_from_file_location('m', {str(CHECKER)!r})\n"
            "m = importlib.util.module_from_spec(spec)\n"
            f"sys.path.insert(0, {str(CHECKER.parent)!r})\n"
            "spec.loader.exec_module(m)\n"
            "def check_that_raises(plan, errors, notes):\n"
            "    raise ValueError('probe: this check cannot finish')\n"
            "m.PLAN_CHECKS = m.PLAN_CHECKS + (check_that_raises,)\n"
            "sys.argv = ['gate'] + sys.argv[1:]\n"
            "raise SystemExit(m.main())\n", encoding="utf-8")
        for extra, parses in ((["--json"], True), ([], False)):
            proc = subprocess.run([sys.executable, str(crasher), str(path),
                                   "--no-verification-yet", *extra],
                                  capture_output=True, text=True)
            if proc.returncode != 2:
                failures.append(f"crash: a raising check must exit 2, got {proc.returncode}")
            if "ValueError" not in proc.stderr or "Traceback" not in proc.stderr:
                failures.append("crash: the traceback must still reach stderr in full")
            if "check_that_raises" not in proc.stdout + proc.stderr:
                failures.append("crash: the report must name the check that could not finish")
            if not parses:
                continue
            try:
                doc = json.loads(proc.stdout)
            except ValueError as exc:
                failures.append(f"crash: --json stopped being JSON when a check raised ({exc})")
                continue
            if doc["ok"] is not False:
                failures.append("crash: a run that could not finish must not report ok")
    return failures



def check_a_flight_number_may_be_unresearched_but_never_invented(itinerary_findings, failures):
    """The one field on a booking card that cannot be estimated, and its honest blank.

    A fare has a range and a duration has a typical value, but a service identifier is either the
    right string or a lie. The contract used to require it unconditionally, which left an author
    who could not price the actual services two moves: invent a plausible number, or put prose in
    a field meant for a code. Both were taken on one real run -- and this repository has already
    shipped a fabricated `KL1927`, which reads as researched to every gate and to the traveller.

    So the identifier now has the escape the dining rating has had all along (`rating_status:
    "none"` plus a written reason). The four cases below are the whole rule.

    Written against `itinerary_findings` directly rather than against the fixture, and that is not
    a style choice: the first version built legs on top of booking-ready-fixture.json, which
    carries **zero flight cards**, so its own `if not flights: return` guard skipped everything and
    the case passed while three mutations of the code it claimed to test all survived. A test whose
    subject the fixture does not contain is a test that reports on nothing.
    """
    def leg(**over):
        base = {"service_identifier": "AA123", "departure_local": "09:10", "arrival_local": "18:40",
                "duration_minutes": 570, "stops": 1, "connection_or_terminal_note": "via PHL"}
        base.update(over)
        return [e for e in itinerary_findings(base, "flight.outbound_itinerary", lambda _r, m: m)]

    if leg():
        failures.append(f"flight identifier: a fully researched leg must pass, got {leg()[:1]}")

    honest = leg(service_identifier=None, service_identifier_status="unresearched",
                 service_identifier_unresearched_reason="No direct route; the carrier and number "
                 "only exist on the search page for these dates.")
    if honest:
        failures.append(f"flight identifier: unresearched WITH a reason must pass, got {honest[:1]}")

    mute = leg(service_identifier=None, service_identifier_status="unresearched",
               service_identifier_unresearched_reason=None)
    if not mute:
        failures.append("flight identifier: unresearched with no reason must be refused -- a blank "
                        "that does not explain itself is indistinguishable from an oversight")

    both = leg(service_identifier="KL1927", service_identifier_status="unresearched",
               service_identifier_unresearched_reason="not checked")
    if not both:
        failures.append("flight identifier: a number under an 'unresearched' label must be refused; "
                        "that is the fabricated-flight-number defect wearing a disclaimer")

    missing = leg(service_identifier=None)
    if not missing:
        failures.append("flight identifier: a researched leg with no identifier must still be "
                        "refused, or the escape becomes the default")

    # Everything else about this leg is legitimate, so ONLY the vocabulary check can refuse it.
    # The first version wrote `leg(service_identifier_status="probably")` with the identifier still
    # filled in, which the unresearched-needs-a-reason rule caught instead -- so the case passed
    # while a mutation that deleted the vocabulary check survived.
    # Whitespace and invisible characters are not a value. `is None or == ""` let both through,
    # so an identifier of "   " read as researched to every gate while the page showed a blank --
    # the same hole the arrival-essentials block had, closed with the same visible_text() test.
    for label, value in (("spaces", "   "), ("a zero-width space", "\u200b"),
                         ("a byte-order mark", "\ufeff")):
        blank = leg(service_identifier=value)
        if not blank:
            failures.append(f"flight identifier: an identifier that is only {label} must be "
                            f"refused; it renders as a gap under a label that says researched")
    if not leg(arrival_local="  "):
        failures.append("flight identifier: a whitespace-only local time must be refused too, or "
                        "the hole just moves to the next string field")

    bogus = leg(service_identifier=None, service_identifier_status="probably",
                service_identifier_unresearched_reason="not checked")
    if not bogus:
        failures.append("flight identifier: an invented status must be refused by the vocabulary "
                        "check, not left to another rule to catch by accident")



def check_per_weekday_hours_are_used_when_present(check_dining, failures):
    """The sharper hours claim wins, and it corrects the flattened one in both directions.

    `venue_hours` must reduce to one open-days-plus-times set so the closed-day check can parse it,
    which forces a venue open 11:30-22:00 on weekdays and 11:30-23:00 at the weekend down to the
    narrowest window that holds every day. On a real run all eight venues were researched per
    weekday and all eight were flattened before they reached the page.

    That is not only lost information, it is a FALSE REJECTION: a Friday meal at 22:10 is fine at a
    venue that closes at 23:00 on Fridays, and the flattened 22:00 refuses it -- pushing the author
    to move a meal that was never a problem. Both directions are asserted below.
    """
    import datetime as dt

    def plan_with(hours_by_weekday, window, date="2026-10-18"):   # 2026-10-18 is a Sunday
        return {"trip": {"start_date": date, "end_date": date, "currency": "EUR"},
                "days": [{"number": 1, "date": date, "day_type": "full",
                          "route": {"stops_in_order": ["Somewhere"]},
                          "dining": [{"meal": "dinner", "time_window": window,
                                      "venue_name": "Test Venue", "route_anchor": "Somewhere",
                                      "hours_status": "researched",
                                      "venue_hours": "Mon-Sun 12:00-21:00",
                                      "venue_hours_by_weekday": hours_by_weekday}]}]}

    WEEK = {"mon": "11:30-22:00", "tue": "11:30-22:00", "wed": "11:30-22:00",
            "thu": "11:30-22:00", "fri": "11:30-23:00", "sat": "11:30-23:00",
            "sun": "12:00-21:00"}

    def run(plan):
        errs: list[str] = []
        check_dining(plan, errs, [])
        return [e for e in errs if "scheduled" in e or "closed" in e]

    late_sunday = run(plan_with(WEEK, "21:15-22:00", "2026-10-18"))
    if not late_sunday:
        failures.append("per-weekday hours: a Sunday meal past Sunday's closing time must be "
                        "refused using that weekday's hours")
    elif "12:00-21:00" not in late_sunday[0]:
        failures.append(f"per-weekday hours: the refusal must quote the day's own hours, got "
                        f"{late_sunday[0]!r}")

    # 2026-10-16 is a Friday, when this venue is open until 23:00. The flattened window says 22:00
    # and would refuse it; the per-weekday table must not.
    late_friday = run(plan_with(WEEK, "22:10-22:50", "2026-10-16"))
    if late_friday:
        failures.append(f"per-weekday hours: a Friday meal inside FRIDAY's hours must pass even "
                        f"though the flattened window ends earlier, got {late_friday[0]!r}")

    # Closure is written as the WORD, not as null. A null that meant "closed" would have turned
    # every unfilled skeleton into a venue shut seven days a week, and null means "not filled in"
    # in every other field of this contract -- breaking that convention in one place is how a
    # reader learns to distrust it everywhere.
    shut = run(plan_with(dict(WEEK, sun="closed"), "13:00-14:00", "2026-10-18"))
    if not shut:
        failures.append("per-weekday hours: a weekday written as 'closed' must be refused -- that "
                        "is the one thing the flattened string cannot express at all")
    shut_zh = run(plan_with(dict(WEEK, sun="休息"), "13:00-14:00", "2026-10-18"))
    if not shut_zh:
        failures.append("per-weekday hours: 休息 must mean closed too, or a Chinese plan silently "
                        "loses the check")
    unfilled = run(plan_with(dict(WEEK, sun=None), "21:15-22:00", "2026-10-18"))
    if not unfilled:
        failures.append("per-weekday hours: a null weekday means NOT FILLED IN, so the flattened "
                        "venue_hours must govern that day rather than the check vanishing")

    # UNREADABLE IS NOT CLOSED. Found by feeding the parser shapes it was not built against: a
    # full-width dash is what a Chinese keyboard produces by default, and it silently became
    # "shut all day", refusing a meal at a venue that was open. Same shape as the null trap above
    # and as every other Latin-constant-meets-CJK defect in this repository.
    for label, value in (("a full-width dash", "11:30－23:00"),
                         ("a phrase", "看心情"),
                         ("a bare number", 1130)):
        noisy = run(plan_with(dict(WEEK, sun=value), "13:00-14:00", "2026-10-18"))
        if not noisy:
            failures.append(f"per-weekday hours: {label} carries no readable window and must be "
                            f"REPORTED, not silently read as a closed day")
        elif "closed" in noisy[0] and "not a closed day" not in noisy[0]:
            failures.append(f"per-weekday hours: {label} was reported as a closure, which inverts "
                            f"the answer: {noisy[0]!r}")

    # An empty string means nobody filled it in, not that the venue is shut.
    blank = run(plan_with(dict(WEEK, sun="  "), "13:00-14:00", "2026-10-18"))
    if blank:
        failures.append(f"per-weekday hours: a blank weekday must fall back to venue_hours, not be "
                        f"read as closed, got {blank[0]!r}")

    # Absent table: the flattened string still governs, so nothing regresses for existing plans.
    without = {"trip": {"start_date": "2026-10-18", "end_date": "2026-10-18", "currency": "EUR"},
               "days": [{"number": 1, "date": "2026-10-18", "day_type": "full",
                         "route": {"stops_in_order": ["Somewhere"]},
                         "dining": [{"meal": "dinner", "time_window": "21:15-22:00",
                                     "venue_name": "Test Venue", "route_anchor": "Somewhere",
                                     "hours_status": "researched",
                                     "venue_hours": "Mon-Sun 12:00-21:00"}]}]}
    if not run(without):
        failures.append("per-weekday hours: with no table the flattened venue_hours must still "
                        "govern, or every plan written before this field stops being checked")



def check_a_review_score_is_not_cited_to_a_price_search(check_booking_identity, failures):
    """A review score cannot be read off an availability search, so it may not be cited to one.

    Shipped, and caught by the traveller rather than by anything here. Both hotels on a delivered
    plan carried `guest_rating_source: "Booking.com"` with `guest_rating_url` set to the SAME dated
    Booking search the compare-prices button used. That page shows rooms and rates; it has never
    shown a review score, so nothing could have been read from it -- and nothing was. The figures
    came from a search-result summary that pooled several platforms, which is how a CROSS-PLATFORM
    review count ("2776 reviews across platforms") ended up paired with one platform's score and
    attributed to a site nobody had opened. Published 9.2 from 2776 and 7.9 from 2271; the property
    pages actually say 9.1 from 105 and 8.1 from 101.

    Six more entries across two other saved trips in the same workspace carried it, so this is an
    authoring habit rather than one slip -- which is the argument for a check rather than a note.

    What is checkable is the citation, not the number. That is the point: the link has to go
    somewhere a reader can look and disagree.
    """
    SEARCH = ("https://www.booking.com/searchresults.html?ss=Hotel+X"
              "&checkin=2026-10-12&checkout=2026-10-19&group_adults=1&no_rooms=1")
    PROPERTY = "https://www.trip.com/hotels/somewhere-hotel-detail-123/hotel-x/"

    def plan(rating_url):
        return {"booking_options": {"accommodations": [{
            "property_name": "Hotel X", "guest_rating_status": "verified",
            "guest_rating_value": 8.1, "guest_rating_scale": 10, "guest_rating_count": 101,
            "guest_rating_source": "Trip.com", "guest_rating_url": rating_url,
            "review_url": PROPERTY, "stay_group_id": "stay-1",
            "comparison_searches": [{"platform": "Booking.com", "search_url": SEARCH,
                                     "checked_at": "2026-09-12",
                                     "prefilled_fields": ["destination"]}]}]}}

    # Only the citation rule's own findings. An ABSENT url is now its own finding -- the hotel
    # score owes guest_rating_url and guest_rating_checked_at like a dining card owes its citation
    # -- and a filter on the bare field name would count that one as this rule firing.
    def citation_findings(errs):
        return [e for e in errs if "guest_rating_url is " in e or "guest_rating_url carries" in e]

    def run(url):
        errs: list[str] = []
        check_booking_identity(plan(url), errs, [])
        return citation_findings(errs)

    if not run(SEARCH):
        failures.append("rating citation: citing the score to the very same price search must be "
                        "refused -- that page has never shown a review score")

    # A comparison search with no date parameters is caught by the byte-identity rule alone --
    # without this case, that rule could be deleted and the suite stayed green, because every
    # other example here also carries check-in parameters.
    bare = "https://www.booking.com/searchresults.html?ss=Hotel+X"
    def plan_bare():
        p = plan(bare)
        p["booking_options"]["accommodations"][0]["comparison_searches"][0]["search_url"] = bare
        return p
    errs: list[str] = []
    check_booking_identity(plan_bare(), errs, [])
    if not citation_findings(errs):
        failures.append("rating citation: a comparison search with no date parameters is still a "
                        "search -- citing the score to the very same link must be refused")

    other_search = SEARCH.replace("Hotel+X", "Hotel+Y")
    if not run(other_search):
        failures.append("rating citation: a DIFFERENT availability search is no better -- any URL "
                        "carrying check-in/occupancy is a price query, not a property page")

    if run(PROPERTY):
        failures.append(f"rating citation: the property's own detail page must be accepted, got "
                        f"{run(PROPERTY)[:1]}")

    if run(""):
        failures.append("rating citation: an absent URL is a different finding, owned elsewhere; "
                        "this check must not fire on it")

    # And the renderer has to make the honest form POSSIBLE. The rating link used to be labelled
    # with `comparison_platform`, so a score could only ever be cited to the site you book on --
    # cite it anywhere else and the provider-identity check failed the page. That is the structural
    # reason the bad pattern was reachable at all, so it is fixed here rather than only warned
    # about: the link goes to where the score was read, so it names that platform.
    import render_final_trip_html as _r
    line = _r.hotel_rating_line({"guest_rating_status": "verified", "guest_rating_value": 8.1,
                                 "guest_rating_scale": 10, "guest_rating_count": 101,
                                 "guest_rating_source": "Trip.com",
                                 "guest_rating_url": PROPERTY,
                                 "comparison_platform": "Booking.com"})
    if 'data-provider="Trip.com"' not in line:
        failures.append(f"rating citation: the rating link must name the platform the score came "
                        f"from, not the booking platform, got {line[:200]!r}")



def check_a_verified_score_owes_an_availability_from_the_same_visit(check_booking_identity, failures):
    """The record-once rule, which lived in a reference file and was read by nothing.

    references/decision-and-research.md: "every accommodation carries its guest score beside a price
    and an availability that came off the same visit." A card claiming a VERIFIED score while its
    availability is `unknown` contradicts that -- the sellability of the dates is on the same page
    as the score, so either the page was never opened (and the score is not verified) or it was
    opened and two of the three fields were left behind.

    That is the shape a delivered plan carried on both hotels -- verified / unknown / estimate --
    while its scores had actually been lifted from a multi-platform search summary and attributed
    to a site nobody had opened. Ten cards across three saved trips carried it, and
    booking-ready-fixture.json did too, so the known-good example was teaching it.

    This is the ROOT of that defect, one layer under the citation rules: those prove the link goes
    somewhere a score can be read; this asks whether anyone went.
    """
    def card(**over):
        base = {"property_name": "Hotel X", "stay_group_id": "stay-1",
                "guest_rating_status": "verified", "guest_rating_value": 8.1,
                "guest_rating_scale": 10, "guest_rating_count": 101,
                "guest_rating_source": "Trip.com",
                "guest_rating_url": "https://www.trip.com/hotels/x-detail-1/hotel-x/",
                "review_url": "https://www.trip.com/hotels/x-detail-1/hotel-x/",
                "availability_status": "unknown", "comparison_searches": []}
        base.update(over)
        errs: list[str] = []
        check_booking_identity({"booking_options": {"accommodations": [base]}}, errs, [])
        return [e for e in errs if "availability" in e]

    if not card():
        failures.append("record-once: a verified score beside an unknown availability with no "
                        "reason must be refused -- they live on the same page")

    if card(availability_unknown_reason="The platform answers this machine with a challenge page."):
        failures.append("record-once: saying WHY availability is unknown must be accepted; a "
                        "platform really can refuse a scripted request")

    if card(availability_status="available"):
        failures.append("record-once: an availability that was actually checked must pass")

    # A card with no rating claim is not claiming to have been on the page, so it is not caught
    # here -- that gap is owned by the rating rules above, and firing twice helps nobody.
    if card(guest_rating_status="none", guest_rating_value=None,
            guest_rating_absence_reason="Too new for reviews."):
        failures.append("record-once: a card claiming no score is not claiming a visit, so this "
                        "check must stay quiet on it")


def main() -> int:
    base = json.loads(FIXTURE.read_text(encoding="utf-8"))
    failures: list[str] = []

    def expect_ok(name: str, plan: dict, verification: dict | None = None) -> None:
        code, out = run(plan, verification)
        if code != 0:
            failures.append(f"{name}: expected pass, got exit {code}\n{out}")

    def expect_fail(name: str, plan: dict, needle: str, verification: dict | None = None) -> None:
        code, out = run(plan, verification)
        if code != 1 or needle not in out:
            failures.append(f"{name}: expected failure containing {needle!r}, got exit {code}\n{out}")

    def expect_fail_naming(name: str, plan: dict, needles: list[str],
                           verification: dict | None = None) -> None:
        """For the checks whose contract fixes what the message must NAME rather than how it is
        worded -- both activities and both times, or the leg's minutes and the cap it broke.

        Asserting the tokens instead of a sentence lets the wording be improved without breaking
        the test, while still failing a message the author cannot act on: 'day 3 walks too far'
        does not tell anyone which leg to shorten or by how much."""
        code, out = run(plan, verification)
        missing = [n for n in needles if n not in out]
        if code != 1 or missing:
            failures.append(
                f"{name}: expected failure naming {needles!r} (missing {missing!r}), "
                f"got exit {code}\n{out}")

    def open_market(plan: dict) -> dict:
        """Move a plan to a market where Google is the working default.

        For cases that need a Google URL to exercise a rule about something else -- coordinate
        dialect, anchor radius -- without also asserting that a mainland-China itinerary may ship
        links nobody there can open. Mutates and returns the plan for use inline.
        """
        plan["regional_service_context"].update({
            "destination_service_market": "united_states",
            "google_services_access": "available",
            "primary_map_provider": "Google Maps",
            "primary_map_exception_reason":
                "Amap deep links remain for the legs whose venues publish Amap coordinates.",
        })
        return plan

    expect_ok("clean fixture passes", copy.deepcopy(base))
    expect_ok("clean fixture with full verification", copy.deepcopy(base), full_verification())

    # 1. Route totals were authored by hand; one real day claimed 50 min against 121 of segments.
    p = copy.deepcopy(base)
    day(p, 1)["route"]["duration_minutes"] = 999
    expect_fail("route duration not derived", p, "route.duration_minutes")

    p = copy.deepcopy(base)
    day(p, 1)["route"]["cost_high"] = 999
    expect_fail("route cost not derived", p, "route.cost_high")

    # 2. The heaviest walking day was labelled the lightest, against a hard accessibility constraint.
    p = copy.deepcopy(base)
    p["days"].append(copy.deepcopy(day(p, 1)))
    p["days"][1]["number"] = 2
    p["days"][1]["date"] = "2026-09-29"
    p["trip"]["end_date"] = "2026-09-29"
    for seg in p["days"][1]["route"]["segments"]:
        seg["walking_minutes"] = 40
    p["days"][1]["route"]["walking_burden"] = "120 minutes, the lightest day of the trip."
    expect_fail("lightest-day claim contradicts data", p, "lightest day")

    # 3. Prose drifting from the computed figure is how the adjective and the data diverge.
    p = copy.deepcopy(base)
    day(p, 1)["route"]["walking_burden"] = "Very light, barely any walking at all."
    expect_fail("walking prose not derived", p, "does not quote the computed")

    # 4. A dinner 2.5 km off-route with no transport leg went unnoticed.
    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][0]
    card.pop("route_anchor", None)
    card["venue_name"] = "Somewhere Far Away"
    expect_fail("dining off route", p, "no route_anchor")

    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["route_anchor"] = "A stop that does not exist"
    expect_fail("dining anchor not a stop", p, "not one of this day's stops_in_order")

    # 5. Meals were scheduled at venues that had already closed.
    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["venue_hours"] = "08:00-11:00"
    expect_fail("meal outside opening hours", p, "is scheduled")

    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][0]
    card.pop("venue_hours", None)
    card.pop("hours_status", None)
    expect_fail("opening hours never checked", p, "hours_status")

    # 6. A weekday-gated service was booked on the wrong weekday.
    # The fixture's only day is a Monday, so the wrong claim here must name a different day.
    p = copy.deepcopy(base)
    day(p, 1)["contingency"] = "本日为周三，导览照常举行。"
    expect_fail("weekday claim contradicts date", p, "asserts")

    p = copy.deepcopy(base)
    day(p, 1)["contingency"] = "本日为周一，导览照常举行。"
    expect_ok("correct weekday claim passes", p)

    # Opening-hour ranges legitimately name other weekdays; they must not trip the check.
    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["reservation_or_queue_note"] = "周一至周六 17:30–22:00，周日休息。"
    expect_ok("weekday ranges are not day claims", p)

    # 7. A stated budget cap was broken without the traveller ever agreeing to it.
    p = copy.deepcopy(base)
    p["budget"]["cap_per_person"] = 10
    expect_fail("cap broken silently", p, "overrun_acknowledged")

    p = copy.deepcopy(base)
    p["budget"]["cap_per_person"] = 10
    p["budget"]["overrun_acknowledged"] = True
    expect_ok("cap breach acknowledged", p)

    # 8. Budget totals disagreed with the rows they were supposedly summed from.
    p = copy.deepcopy(base)
    p["budget"]["estimated_per_person_high"] = 1
    expect_fail("budget totals not summed", p, "included categories")

    # 9. Calendar coverage: no gaps, no duplicates, departure day is a checkout.
    p = copy.deepcopy(base)
    p["trip"]["end_date"] = "2026-09-30"
    expect_fail("date gap", p, "must cover every date")

    # A departure day must land on the checkout date, or a night is being paid for twice.
    p = copy.deepcopy(base)
    day(p, 1)["day_type"] = "departure"
    expect_fail("extra night on departure day", p, "checkout date")

    p = copy.deepcopy(base)
    day(p, 1)["day_type"] = "departure"
    for stay in p["booking_options"]["accommodations"]:
        stay["check_out"] = day(p, 1)["date"]
    expect_ok("departure day equals checkout", p)

    # 10. Verification report: every domain must be covered and every defect resolved.
    report = full_verification()
    report["domains"] = report["domains"][:2]
    expect_fail("verification missing domains", copy.deepcopy(base), "missing required domains", report)

    report = full_verification()
    report["domains"][0]["findings"] = [
        {"claim": "entry requires only a visa", "verdict": "wrong", "resolved": False}
    ]
    expect_fail("verification defect unresolved", copy.deepcopy(base),
                "never resolved", report)

    report = full_verification()
    report["domains"][0]["findings"] = [
        {"claim": "entry requires only a visa", "verdict": "wrong", "severity": "critical",
         "resolved": True,
         "resolution": "entry_context now names the electronic travel authorisation as well"}
    ]
    expect_ok("verification defect resolved", copy.deepcopy(base), report)

    # This case used to pass with `resolved: True` and nothing else -- the shape that made a wrong
    # finding vanish without anyone saying what was done about it (2026-09-24). A closed finding
    # now names its change; the bare flag is the unresolved entry it always was.
    report = full_verification()
    report["domains"][0]["findings"] = [
        {"claim": "entry requires only a visa", "verdict": "wrong", "severity": "critical",
         "resolved": True}
    ]
    expect_fail("verification defect closed by a bare flag", copy.deepcopy(base),
                "no resolution", report)

    # 10a. The verification tier is read off the plan, never declared by the run. A two-night rail
    # city break with no allergy and no walking cap was paying the same seven-block pass as a
    # multi-city flight itinerary, and three of those blocks had no subject on it -- which is how
    # an operator learns to reach for --unverified instead. The danger runs the other way too, so
    # the absence cases below matter more than the qualifying one: every plan written before
    # entry_context and traveler_constraints existed lacks both, and treating a missing block as
    # "no constraint" would silently downgrade exactly the plans nobody has re-examined.
    def light_plan() -> dict:
        p = copy.deepcopy(base)
        p["entry_context"] = {"status": "not_required"}
        p["trip"]["traveler_constraints"] = constraints()
        p["trip"]["arrival_transport_mode"] = "rail"
        p["booking_options"]["flights"] = []
        p["booking_options"]["rental_cars"] = []
        p["budget"]["breakdown"] = [r for r in p["budget"]["breakdown"]
                                    if r.get("category") not in {"flight", "ferry", "rental_car"}]
        for d in p["days"]:
            d["base_location"] = "One City"
        p["booking_options"]["accommodations"] = [{"stay_group_id": "only-stay"}]
        return p

    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location("_cpc", CHECKER)
    _cpc = _ilu.module_from_spec(_spec); _spec.loader.exec_module(_cpc)

    def tier(plan: dict) -> str:
        # Light keeps the two domains whose facts strand a traveller rather than disappoint one:
        # weekday-keyed opening hours, and the leg between two places. The first draft kept only
        # hours, on the reasoning that a trip with no flight has no transport to check -- backwards
        # for the very trip this tier exists for, since a two-night rail break is nothing but
        # transport and nobody would have verified the train runs that day, that way, at that fare.
        required, _ = _cpc.required_domains_for(plan)
        return "light" if required == _cpc.LIGHT_TIER_DOMAINS else "full"

    if tier(light_plan()) != "light":
        failures.append("tier: a short single-city rail plan with no constraints should qualify as light")
    for label, mutate in (
        ("a flight", lambda p: p["booking_options"]["flights"].append({})),
        ("a rental car", lambda p: p["booking_options"]["rental_cars"].append({})),
        ("arrival by air", lambda p: p["trip"].update(arrival_transport_mode="flight")),
        ("an entry requirement", lambda p: p["entry_context"].update(status="required_to_apply")),
        ("a severe allergy", lambda p: p["trip"]["traveler_constraints"].update(allergy_severity="severe")),
        ("a walking cap", lambda p: p["trip"]["traveler_constraints"].update(max_continuous_walking_minutes=30)),
        # Absence is the dangerous direction and the easy one to get wrong twice: the first pass
        # covered entry_context and traveler_constraints and left booking_options, days and the
        # arrival mode reading as "nothing to declare". Every top-level block a condition depends
        # on is listed here, so a later refactor that adds a condition has somewhere obvious to
        # add its absence case too.
        ("NO entry_context at all", lambda p: p.pop("entry_context")),
        ("NO traveler_constraints at all", lambda p: p["trip"].pop("traveler_constraints")),
        ("NO booking_options at all", lambda p: p.pop("booking_options")),
        ("NO budget at all", lambda p: p.pop("budget")),
        # A ferry cannot be expressed in arrival_transport_mode, whose enum is
        # flight/rail/road/other, so a budget row is the only place it appears. SKILL.md says a
        # ferry needs the full pass -- sailings are seasonal, weather-cancelled and often the
        # single point of failure in a day -- and without this the doc promised a check the code
        # could not see.
        ("a ferry priced in the budget",
         lambda p: p["budget"]["breakdown"].append({"category": "ferry"})),
        ("a flight priced in the budget",
         lambda p: p["budget"]["breakdown"].append({"category": "flight"})),
        # allergy_severity was a DENYLIST -- `in {"intolerance", "severe"}` with an `or "none"`
        # default -- so every value the code did not recognise bought the cheap tier: null, an
        # absent key, "Severe" with a capital S, "anaphylactic". new_plan_skeleton.py hardcodes
        # "none" and --from-intake has no source for the field, so the DEFAULT of a plan built the
        # documented way was the value that skipped four verification domains, on a traveller who
        # had written "anaphylactic peanut allergy, I carry an EpiPen" on the form.
        ("a null allergy_severity",
         lambda p: p["trip"]["traveler_constraints"].update(allergy_severity=None)),
        ("an absent allergy_severity",
         lambda p: p["trip"]["traveler_constraints"].pop("allergy_severity")),
        ("allergy_severity 'anaphylactic' (not in the enum)",
         lambda p: p["trip"]["traveler_constraints"].update(allergy_severity="anaphylactic")),
        ("allergy_severity 'Severe' (wrong case)",
         lambda p: p["trip"]["traveler_constraints"].update(allergy_severity="Severe")),
        # The tier's two constraint clauses -- a severity of none/preference, and a null cap --
        # were EXACTLY what new_plan_skeleton.py emitted for two fields it cannot know, so a plan
        # nobody had asked the question bought the cheap tier on the strength of not having been
        # asked, and the reason string told the operator "no severe allergy or walking cap". The
        # marker is the difference between an answer and an unanswered question, and the tier has
        # to read it as the second one. Both spellings the check tolerates are covered, because a
        # tier that fires only on the dict shape is a tier a hand-edit can switch back off.
        ("the skeleton's untyped-constraint marker",
         lambda p: p["trip"]["traveler_constraints"].update(
             **{_cpc.UNTYPED_CONSTRAINTS_MARKER: {"allergy_severity": "TODO: type it",
                                                  "max_continuous_walking_minutes": "TODO: type it"}})),
        ("an untyped-constraint marker naming only the walking cap",
         lambda p: p["trip"]["traveler_constraints"].update(
             **{_cpc.UNTYPED_CONSTRAINTS_MARKER: ["max_continuous_walking_minutes"]})),
        # A need stated in prose while the typed field sits at its default is a constraint nobody
        # can measure, and dropping four domains on the strength of an unconverted note is backwards.
        ("dietary needs in prose while severity is 'none'",
         lambda p: p["trip"]["traveler_constraints"].update(
             dietary_or_religious_needs=["Anaphylactic peanut allergy - carries an EpiPen"])),
        ("mobility notes in prose while the cap is null",
         lambda p: p["trip"]["traveler_constraints"].update(
             mobility_notes=["Cannot walk more than 15 minutes at a stretch"])),
        # The reason string claimed "single-city" and nothing tested it: four days across Ghent and
        # Bruges with a coach between them read as light, dropping the transport domain -- so nobody
        # checked the one leg whose failure strands the traveller between two hotels.
        # The fixture is a single day, so a second base has to be added rather than edited in --
        # which is also the honest shape of the defect: a second city arrives as a second day.
        ("two base_locations",
         lambda p: p["days"].append(dict(p["days"][0], number=2, date="2026-09-29",
                                         base_location="A Second City"))),
        ("two stay groups",
         lambda p: p["booking_options"]["accommodations"].append(
             {"stay_group_id": "a-second-stay-group"})),
        ("NO days at all", lambda p: p.pop("days")),
        ("an empty days list", lambda p: p.update(days=[])),
        ("no arrival_transport_mode", lambda p: p["trip"].pop("arrival_transport_mode")),
        ("an unset entry status", lambda p: p["entry_context"].clear()),
        # A ground card asserts a fare range, an availability status and a prefilled search URL --
        # exactly what booking_and_lodging verifies. On a rail city break, the trip the light tier
        # was built for, that card is the largest and most time-sensitive purchase on the page, and
        # the tier left it as the one thing no verifier looked at.
        ("a ticketed rail leg",
         lambda p: p["booking_options"].update(ground_transport=[{"id": "ground-1"}])),
    ):
        p = light_plan()
        mutate(p)
        if tier(p) != "full":
            failures.append(f"tier: a plan carrying {label} must need the full pass, not the light tier")

    # 10a-ii. The tier's reason string is what an operator reads when the gate refuses to let them
    # off with four domains, and a reason that does not name the marker leaves them re-reading the
    # allergy fields looking for a value that is already correct. The marker's own defence is that
    # it explains itself: this asserts the sentence names the marker AND the field still open.
    marked = light_plan()
    marked["trip"]["traveler_constraints"][_cpc.UNTYPED_CONSTRAINTS_MARKER] = {
        "max_continuous_walking_minutes": "TODO: type it"}
    _, why = _cpc.required_domains_for(marked)
    for token in (_cpc.UNTYPED_CONSTRAINTS_MARKER, "max_continuous_walking_minutes"):
        if token not in why:
            failures.append(f"tier: the full-pass reason never names {token!r}: {why}")
    if "allergy_severity" in why:
        failures.append(
            f"tier: the reason names allergy_severity, which this plan HAS typed -- a tier that "
            f"explains itself with a fact untrue of the plan teaches operators to skim it: {why}")

    # 10b. The two network-free auditors are part of the protocol, not an optional extra. The gate
    # used to accept a five-domain report silently, so a run that followed references/
    # verification.md and produced seven blocks failed, while a run that skipped the two cheapest
    # and highest-yield agents passed.
    report = full_verification()
    report.pop("audits")
    expect_fail("verification report omits both audits", copy.deepcopy(base),
                "missing required audits", report)

    report = full_verification()
    report["audits"] = [report["audits"][0]]
    expect_fail("verification report omits one audit", copy.deepcopy(base),
                "missing required audits", report)

    # An audit that examined nothing is an audit nobody ran, and the old integer shape let it say
    # so in one character. The rule is the same for audits as for domains; case 22a drives the
    # message itself, this one only pins that audits are not exempt from it.
    report = full_verification()
    report["audits"][0]["claims_checked"] = 0
    expect_fail("audit reports no claims checked", copy.deepcopy(base), "claims_checked", report)

    report = full_verification()
    report["audits"].append({"audit": "vibes",
                             "claims_checked": ["trip.title"], "findings": []})
    expect_fail("invented audit name", copy.deepcopy(base), "not part of the protocol", report)

    report = full_verification()
    report["audits"][1]["findings"] = [{
        "claim": "the page never shows the traveller's own budget cap",
        "verdict": "misleading", "correction": "render cap_per_person", "severity": "critical"}]
    expect_fail("audit finding left unresolved", copy.deepcopy(base), "never resolved", report)

    report = full_verification()
    report["audits"][1]["findings"] = [{
        "claim": "the page never shows the traveller's own budget cap",
        "verdict": "misleading", "correction": "render cap_per_person", "severity": "critical",
        "resolved": True, "resolution": "budget block now prints cap_per_person"}]
    expect_ok("audit finding resolved", copy.deepcopy(base), report)

    # 11. Substring matching once let a day whose real walking total was 5 minutes satisfy the
    # rule by writing "15 minutes" -- the exact inversion the check exists to prevent.
    p = copy.deepcopy(base)
    for seg in day(p, 1)["route"]["segments"]:
        seg["walking_minutes"] = 0
    day(p, 1)["route"]["segments"][0]["walking_minutes"] = 5
    day(p, 1)["route"]["walking_burden"] = "15 minutes of walking."
    expect_fail("walking figure matched as a substring", p, "does not quote the computed")

    p = copy.deepcopy(base)
    for seg in day(p, 1)["route"]["segments"]:
        seg["walking_minutes"] = 0
    day(p, 1)["route"]["segments"][0]["walking_minutes"] = 5
    day(p, 1)["route"]["walking_burden"] = "5 minutes on foot; the climb is 15 metres."
    expect_ok("larger numbers nearby do not break the match", p)

    # 12. A timeline that renders in list order but runs backwards on the clock.
    p = copy.deepcopy(base)
    acts = day(p, 1)["activities"]
    if len(acts) >= 2:
        acts[0]["time"], acts[1]["time"] = "18:00", "09:00"
        expect_fail("activities out of chronological order", p, "time travel")

    # 13. References that point at nothing render as blanks or dropped cards.
    p = copy.deepcopy(base)
    tickets = p["booking_options"]["attraction_tickets"]
    if tickets:
        tickets[0]["day_number"] = 99
        expect_fail("ticket references a day that does not exist", p, "which is not in this plan")

    p = copy.deepcopy(base)
    day(p, 1)["activities"][0]["ticket_option_id"] = "no-such-ticket"
    expect_fail("activity references an undefined ticket", p, "which no attraction_tickets entry")

    # 14. Malformed input must produce a finding, not a traceback: an operator who sees a stack
    # trace learns nothing about their plan and stops running the gate.
    for name, broken in {
        "route is null": {"trip": {"start_date": "2026-01-01", "end_date": "2026-01-01"},
                          "days": [{"number": 1, "date": "2026-01-01", "route": None}]},
        "dining card is a string": {"trip": {"start_date": "2026-01-01", "end_date": "2026-01-01"},
                                    "days": [{"number": 1, "date": "2026-01-01", "dining": ["oops"],
                                              "route": {"segments": [], "walking_burden": "0"}}]},
        "plan is a list": [1, 2, 3],
        # replan_context arrives from a hand edit as often as from replan_trip.py, so its two
        # plausible malformations belong here rather than in a case that only checks the wording.
        "replan_context is a string": {"trip": {"start_date": "2026-01-01", "end_date": "2026-01-01"},
                                       "days": [], "replan_context": "moved the trip a day later"},
        "must_reverify holds strings": {"trip": {"start_date": "2026-01-01", "end_date": "2026-01-01"},
                                        "days": [],
                                        "replan_context": {"must_reverify": ["check the hours"]}},
    }.items():
        code, out = run(broken)
        if "Traceback" in out:
            failures.append(f"crash on {name}: checker raised instead of reporting\n{out[-400:]}")

    # 15. The verification report is written by the run it vouches for, so cheap forgeries must fail.
    report = full_verification()
    report["domains"].append({"domain": "made_up",
                              "claims_checked": ["trip.title"], "findings": []})
    expect_fail("invented domain", copy.deepcopy(base), "not part of the protocol", report)

    report = full_verification()
    for domain in report["domains"]:
        domain.pop("claims_checked", None)
    expect_fail("no claims_checked at all", copy.deepcopy(base), "claims_checked", report)

    report = full_verification()
    report["plan"] = "a-completely-different-trip.json"
    expect_fail("report bound to another plan", copy.deepcopy(base), "was supplied for", report)

    report = full_verification()
    report.pop("plan")
    expect_fail("report names no plan", copy.deepcopy(base), "no 'plan' field", report)

    p = copy.deepcopy(base)
    p["generated_at"] = "2026-08-03"
    report = full_verification()
    report["checked_at"] = "2019-01-01"
    expect_fail("report predates the plan", p, "before the plan's generated_at", report)

    # --- gaps found by the 2026-08-05 audit. Each of these passed every gate before it. ---

    # `actual` was computed and never compared, so a day could claim fewer interchanges than its
    # own legs declared. The rule is a lower bound, not equality: bus -> walk -> bus is one
    # vehicle change across two segments that each declare none, and equality would reject it.
    p = copy.deepcopy(base)
    day(p, 1)["route"]["transfer_count"] = 0
    expect_fail("transfer_count below what the segments declare", p, "fewer than the")
    p = copy.deepcopy(base)
    segments = day(p, 1)["route"]["segments"]
    day(p, 1)["route"]["transfer_count"] = sum(s.get("transfer_count") or 0 for s in segments)
    expect_ok("transfer_count equal to the segment declarations is fine", p)

    # The ceiling used to be the segment COUNT, which collided with the lower bound on the most
    # ordinary shape there is: one ticketed journey with two changes. With three legs the floor
    # demanded 3 and the ceiling allowed at most 3, so exactly one value passed and it was not
    # necessarily the true one -- and an author whose only way past a gate is a number they know is
    # wrong writes it, after which the figure on the page means nothing. The real ceiling is one
    # interchange per boundary between legs, plus every interchange declared inside a leg.
    p = copy.deepcopy(base)
    route = day(p, 1)["route"]
    route["segments"][0]["transfer_count"] = 2      # one ticketed leg with two changes
    route["transfer_count"] = 5                     # 2 boundaries + 3 declared in-leg
    expect_ok("a leg carrying its own interchanges can be summarised honestly", p)

    p = copy.deepcopy(base)
    route = day(p, 1)["route"]
    route["segments"][0]["transfer_count"] = 2
    route["transfer_count"] = 6                     # one above the ceiling
    expect_fail("transfer_count above what the day can contain", p, "exceeds the")

    # A category declared included but never itemised makes the headline total a black box --
    # exactly what the breakdown exists to prevent.
    p = copy.deepcopy(base)
    p["budget"]["included_categories"] = sorted(set(p["budget"]["included_categories"]) | {"insurance"})
    expect_fail("included category with no breakdown row", p, "no breakdown row prices it")

    # A reversed window did not fail; it made the day-coverage loop iterate nothing, silently
    # disabling every downstream date check.
    p = copy.deepcopy(base)
    p["trip"]["start_date"], p["trip"]["end_date"] = "2026-09-30", "2026-09-28"
    expect_fail("reversed trip window", p, "is after trip.end_date")

    # Totals are summed from segments, so a negative leg can cancel a real one and leave the
    # arithmetic checks satisfied.
    p = copy.deepcopy(base)
    first = day(p, 1)["route"]["segments"][0]
    first["duration_minutes"] = -first["duration_minutes"]
    day(p, 1)["route"]["duration_minutes"] = sum(s["duration_minutes"] for s in day(p, 1)["route"]["segments"])
    expect_fail("negative segment duration", p, "is negative")


    # --- the 2026-08-07 run: four gates green, one unrideable plan. Every case below is a defect
    # that survived all of them, and the check the contract adds so it cannot survive again. ---

    # The cases below are arithmetic against the fixture's own segment totals, so state what they
    # assume. Without this, editing the fixture turns "needs 448, spans 405" into a number nobody
    # can trace, and the quietest way for it to break is for the defect to stop being a defect --
    # a case that no longer violates anything still passes, it just stops testing anything.
    fixture_segments = day(base, 1)["route"]["segments"]
    assumed = {"duration": 73, "walking": 20}
    actual = {"duration": sum(s["duration_minutes"] for s in fixture_segments),
              "walking": sum(s["walking_minutes"] for s in fixture_segments)}
    if actual != assumed:
        failures.append(
            f"the fixture's day 1 now sums to {actual} minutes of segments, not {assumed}. The "
            f"clock-closure and walking-budget cases below hard-code those totals; recompute their "
            f"durations and burden strings so each one is still the violation, or the near miss, "
            f"it claims to be.")

    # 16a. The day's clock, overlap half. Two stops that run at the same time render as a tidy
    # list -- the timeline is in ascending order, so the existing "time travel" check is happy --
    # and the traveller only discovers the collision while standing in the first one.
    p = copy.deepcopy(base)
    acts = day(p, 1)["activities"]
    acts[0]["duration_minutes"] = 120                       # 09:00 -> 11:00
    acts.insert(1, {"time": "10:00", "name": "Fixture overlapping activity",
                    "duration_minutes": 30, "ticket_option_id": None,
                    "detail": "Starts while the first stop is still running."})
    acts[2]["duration_minutes"] = 60                        # 15:00 -> 16:00
    expect_fail_naming("activities overlap on the clock", p,
                       ["Fixture activity A", "Fixture overlapping activity", "09:00", "10:00"])

    # 16b. The same check, arithmetic half, and the exact shape that shipped: a promenade that
    # ended at 14:00, the next activity at 15:00, and 35 minutes of the plan's OWN segments plus a
    # lunch in a third place in between. Nothing here overlaps -- 09:00 + 330 ends at 14:30 and the
    # next stop is 15:00 -- yet the 73 minutes of segments the day declares cannot fit in the 30
    # minutes it leaves for them.
    p = copy.deepcopy(base)
    acts = day(p, 1)["activities"]
    acts[0]["duration_minutes"] = 355
    acts[1]["duration_minutes"] = 45                        # needs 418 min, spans 405
    # 418 = 355 + 45 activity minutes + the 18-minute A->B leg. Only the INTERIOR segments count:
    # this case originally asserted 448, charging all 73 segment minutes, and that was wrong in a
    # way that rejected correct plans. The span runs from the first activity's start to the last
    # one's end, so the 25-minute hotel->A leg happens before it opens and the 30-minute B->hotel
    # leg after it closes -- 55 of the 73 were load the window never carries. A day at A
    # 09:00-14:00 and at B 15:00-16:00 (leave 08:35, home 16:30, entirely feasible) was reported as
    # needing 433 minutes out of 420. This case passed then only because the fixture happened to
    # have 47 minutes of slack, which is exactly how a test can green-light a broken check.
    expect_fail_naming("day's own numbers do not fit its clock", p, ["day 1", "418"])

    # The mirror case, and the reason the number above had to be recomputed rather than nudged:
    # a day whose bounding legs are long must still pass when its interior fits.
    p = copy.deepcopy(base)
    acts = day(p, 1)["activities"]
    acts[0]["duration_minutes"] = 300                       # at A 09:00-14:00
    acts[1]["duration_minutes"] = 60                        # at B 15:00-16:00, 18-min leg between
    expect_ok("bounding legs outside the span do not count against it", p)

    p = copy.deepcopy(base)
    acts = day(p, 1)["activities"]
    acts[0]["duration_minutes"] = 240
    acts[1]["duration_minutes"] = 45                        # needs 358 min, spans 405
    expect_ok("a day whose activities and segments do fit passes", p)

    # 17. A stated walking cap is a number, so a leg that breaks it is decidable. It was not
    # decided: the plan recommended connections well past the traveller's limit and every gate
    # passed, because nothing compared a segment against the constraint the traveller had given.
    p = copy.deepcopy(base)
    p["trip"]["traveler_constraints"] = constraints(max_continuous_walking_minutes=12)
    day(p, 1)["route"]["segments"][0]["walking_minutes"] = 33
    day(p, 1)["route"]["walking_burden"] = (
        "Derived from segments: 47 minutes of walking across the day (0 km on foot).")
    expect_fail_naming("segment walk exceeds the stated cap", p, ["day 1", "33", "12"])

    p = copy.deepcopy(base)
    p["trip"]["traveler_constraints"] = constraints(max_continuous_walking_minutes=40)
    day(p, 1)["route"]["segments"][0]["walking_minutes"] = 33
    day(p, 1)["route"]["walking_burden"] = (
        "Derived from segments: 47 minutes of walking across the day (0 km on foot).")
    # A stated cap now also obliges every activity to answer with a number, so this plan declares
    # them; the case is about the segment rule, and leaving them silent would fail it for an
    # unrelated reason.
    for activity in day(p, 1)["activities"]:
        activity["on_foot_minutes"] = 0
    expect_ok("a leg inside the stated cap passes", p)

    # The hole that obliged it. Measured on the shipped fixture: a traveller with a 20-minute cap
    # and activities declaring nothing saved clean with the page reading "20 min", while the SAME
    # plan with the walking honestly written as 180 was refused -- the gate rewarded silence and
    # punished the honest number, for exactly the traveller it exists to protect.
    p = copy.deepcopy(base)
    p["trip"]["traveler_constraints"] = constraints(max_continuous_walking_minutes=20)
    for activity in day(p, 1)["activities"]:
        activity.pop("on_foot_minutes", None)
    expect_fail_naming("a stated cap with activities that declare no on_foot_minutes", p,
                       ["day 1", "on_foot_minutes", "Undeclared is not zero"])

    # And a measured zero is an answer, not silence: an author who looked at a concert and wrote 0
    # has done the thing being asked for.
    p = copy.deepcopy(base)
    p["trip"]["traveler_constraints"] = constraints(max_continuous_walking_minutes=20)
    for activity in day(p, 1)["activities"]:
        activity["on_foot_minutes"] = 0
    expect_ok("a stated cap with every activity declaring a measured zero", p)

    # new_plan_skeleton.py stamps every date it cannot know as the epoch, and nothing rejected it:
    # a dining checked_at, a route map_checked_at and a source accessed_at all set to 1970-01-01
    # saved clean while the page went on printing "verified" beside each. A timestamp IS the
    # evidence, so a sentinel one asserts a check that never happened.
    for label, mutate in (
        ("a dining card checked on the epoch",
         lambda x: day(x, 1)["dining"][0].__setitem__("checked_at", "1970-01-01")),
        ("a route map checked on the epoch",
         lambda x: day(x, 1)["route"].__setitem__("map_checked_at", "1970-01-01")),
        ("a source accessed on the epoch",
         lambda x: x["sources"][0].__setitem__("accessed_at", "1970-01-01")),
    ):
        p = copy.deepcopy(base)
        mutate(p)
        expect_fail_naming(label, p, ["1970-01-01", "placeholder"])

    # A ticket you cannot be at a screen to buy is not a ticket the traveller has. Kabukiza
    # single-act seats go on sale 12:00 the day before, and the plan itself had the traveller in
    # the Narita immigration queue at that moment -- its own timeline refuting its own instruction,
    # with nothing comparing the two because the sale moment was not data.
    trip_day = day(copy.deepcopy(base), 1)["date"]

    # The fixture's day 1 runs 09:00 to 15:00. Times are read, never rewritten: moving an activity
    # here breaks check_clock_closure, and the case then fails for a reason it was not testing.
    def with_ticket(sale, scheduled=True):
        p = copy.deepcopy(base)
        ticket = {"id": "T1", "day_number": 1, "attraction_name": "Kabukiza single-act seats",
                  "checked_at": "2026-08-20"}
        if sale is not None:
            ticket["sale_opens_at"] = sale
        p["booking_options"]["attraction_tickets"] = [ticket]
        if scheduled:
            day(p, 1)["activities"][0]["ticket_option_id"] = "T1"
        return p

    expect_fail("a scheduled ticket declaring no sale window",
                with_ticket(None), "declares no sale_opens_at")
    # Option C: the burden lands only on tickets a day actually uses. A booking option nobody
    # scheduled cannot strand anyone, and taxing every museum admission is how a rule gets routed
    # around a research budget.
    _, out = run(with_ticket(None, scheduled=False))
    if "sale_opens_at" in out:
        failures.append("an unscheduled ticket must not be held to the sale-window rule\n" + out)

    # basis is the anti-rubber-stamp: a required field with a free vocabulary invites
    # "always_available" typed without opening anything, which is an invented fact rather than a
    # visible blank -- worse than what it replaces.
    expect_fail("always_available with no basis",
                with_ticket({"status": "always_available", "opens_at": None, "basis": None}),
                "no basis")
    expect_fail("a basis that is still a placeholder",
                with_ticket({"status": "always_available", "opens_at": None,
                             "basis": "TODO: check the box office"}), "placeholder")
    expect_fail("a status outside the vocabulary",
                with_ticket({"status": "probably fine", "opens_at": None, "basis": "x"}),
                "not one of")
    expect_ok("always_available with a real basis (the cheap common case)",
              with_ticket({"status": "always_available", "opens_at": None,
                           "basis": "Official site: open seating, tickets at the door all season."}))
    expect_fail("a scheduled_release with no opens_at",
                with_ticket({"status": "scheduled_release", "opens_at": None,
                             "basis": "Sold the day before."}), "no ISO opens_at")

    expect_fail_naming("the recorded defect: seats released while the traveller is still in transit",
                       with_ticket({"status": "scheduled_release",
                                    "opens_at": f"{trip_day}T07:00:00+09:00",
                                    "basis": "Official site: released 07:00 on the day."}),
                       ["07:00", "still in transit"])
    expect_fail("a sale that opens after the day the plan already uses the ticket",
                with_ticket({"status": "scheduled_release", "opens_at": "2026-12-01T12:00:00+09:00",
                             "basis": "Released 2026-12-01."}), "already has the traveller using it")

    # The two that must stay quiet, or the rule is a wall: a sale the traveller is around for, and
    # the ordinary case of buying before leaving home.
    expect_ok("a sale the traveller is present for",
              with_ticket({"status": "scheduled_release", "opens_at": f"{trip_day}T11:00:00+09:00",
                           "basis": "Official site: released 11:00."}))
    expect_ok("a sale that opens before departure",
              with_ticket({"status": "scheduled_release", "opens_at": "2026-09-01T12:00:00+09:00",
                           "basis": "Official site: released two weeks ahead."}))

    # replan_context tells the author to re-check the fact and "record what you found in
    # 'resolution'" -- and only the boolean was ever read. Flipping every flag to true with no
    # resolution shipped a replanned plan whose weekday-keyed opening hours, researched for a
    # Monday that is now a Thursday, were never re-checked, while the gate said all resolved.
    def replanned(entries: list[dict]) -> dict:
        p = copy.deepcopy(base)
        p["replan_context"] = {"replanned_from": "old.json", "replanned_at": "2026-08-22",
                               "change_request": "three days later", "changed_fields": ["dates"],
                               "must_reverify": entries}
        return p

    entry = {"path": "days[0].dining[0].venue_hours",
             "reason": "hours were checked for a Monday this day no longer is"}
    expect_fail_naming("a must_reverify entry resolved with no resolution text",
                       replanned([dict(entry, resolved=True)]),
                       ["must_reverify[0]", "no 'resolution'"])
    expect_fail_naming("a resolution that is still a placeholder",
                       replanned([dict(entry, resolved=True, resolution="TODO: re-check")]),
                       ["must_reverify[0]", "placeholder"])
    expect_ok("a must_reverify entry resolved with what was found",
              replanned([dict(entry, resolved=True,
                              resolution="Re-checked for Thursday: 11:00-14:30, closed Tuesdays.")]))

    # A dated ticket and the day its activity sits on have to name the same day. Membership was
    # all that was ever checked -- day_number had to EXIST among the days -- so a ticket dated day
    # 1 whose activity ran on day 2 passed, which is the Tokyo run's time-critical ticket pointed
    # at the wrong evening, surviving the fix meant to close it.
    def two_day_ticket(ticket_day: int, activity_day: int) -> dict:
        p = copy.deepcopy(base)
        p["days"].append(copy.deepcopy(day(p, 1)))
        p["days"][1]["number"] = 2
        p["days"][1]["date"] = "2026-09-29"
        p["trip"]["end_date"] = "2026-09-29"
        p["booking_options"]["attraction_tickets"] = [
            {"id": "T1", "day_number": ticket_day, "attraction_name": "Evening opera",
             "checked_at": "2026-08-20",
             # A scheduled ticket now owes a sale window; this case is about the day-agreement
             # rule, so it declares the cheap honest one rather than failing for another reason.
             "sale_opens_at": {"status": "always_available", "opens_at": None,
                               "basis": "Official box office lists open seating all season."}}]
        day(p, activity_day)["activities"][0]["ticket_option_id"] = "T1"
        return p

    expect_fail_naming("a ticket dated a different day than the activity using it",
                       two_day_ticket(1, 2), ["Evening opera", "day 1", "day 2"])
    # The correct pairing must stay quiet, or the rule is a wall rather than a check.
    _, out = run(two_day_ticket(2, 2))
    if "Evening opera" in out:
        failures.append("a ticket dated the same day as its activity must not be flagged\n" + out)
    # And a ticket listed as an option but scheduled nowhere cannot contradict itself.
    p = copy.deepcopy(base)
    p["booking_options"]["attraction_tickets"] = [
        {"id": "T9", "day_number": 1, "attraction_name": "Unscheduled museum",
         "checked_at": "2026-08-20"}]
    _, out = run(p)
    if "Unscheduled museum" in out:
        failures.append("an unscheduled ticket must not be flagged as a day mismatch\n" + out)

    # Reported once with its paths, not once per field: a fresh four-day skeleton carries 61 of
    # them, and sixty-one copies of the same sentence bury every other finding.
    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["checked_at"] = "1970-01-01"
    day(p, 1)["route"]["map_checked_at"] = "1970-01-01"
    p["sources"][0]["accessed_at"] = "1970-01-01"
    _, output = run(p)
    sentinel_lines = [line for line in output.splitlines()
                      if line.startswith("- ") and "1970-01-01" in line]
    if len(sentinel_lines) != 1:
        failures.append("epoch sentinels are reported in one aggregated error: "
                        f"got {len(sentinel_lines)} lines\n{output}")
    elif "3 timestamp(s)" not in sentinel_lines[0]:
        failures.append("the aggregated error must say how many it found\n" + sentinel_lines[0])

    # A stop the traveller stands in for 95 minutes breaks the same cap as a 95-minute connection,
    # and it is the half nobody counted: the burden figure only ever summed the legs between stops.
    p = copy.deepcopy(base)
    p["trip"]["traveler_constraints"] = constraints(max_continuous_walking_minutes=12)
    day(p, 1)["activities"][0]["on_foot_minutes"] = 95
    day(p, 1)["route"]["walking_burden"] = (
        "Derived from segments: 20 minutes of walking between stops, plus 95 minutes on foot at "
        "the stops themselves (0 km on foot).")
    expect_fail_naming("activity on foot exceeds the stated cap", p, ["day 1", "95", "12"])

    # 18. The misleading figure the gate itself certified: the page said "42 minutes on foot" for a
    # day that scheduled roughly three and a half hours of it, against a hard mobility constraint,
    # and the old check REQUIRED that number be printed because connections were all it summed.
    # Once activities carry on_foot_minutes, quoting one of the two totals is no longer enough.
    p = copy.deepcopy(base)
    day(p, 1)["activities"][0]["on_foot_minutes"] = 95
    day(p, 1)["activities"][1]["on_foot_minutes"] = 25      # 120 min on foot, burden still says 20
    expect_fail_naming("walking_burden quotes the connections only", p, ["120"])

    p = copy.deepcopy(base)
    day(p, 1)["activities"][0]["on_foot_minutes"] = 95
    day(p, 1)["activities"][1]["on_foot_minutes"] = 25
    day(p, 1)["route"]["walking_burden"] = (
        "Derived from segments: 20 minutes of walking between stops, plus 120 minutes on foot at "
        "the stops themselves (0 km on foot). Flat throughout, with seating at each stop.")
    expect_ok("walking_burden quoting both totals passes", p)

    # 19. Opening hours as they are actually published. "周二至周日 15:00-21:00" failed to parse,
    # and a failed parse SKIPPED the hours check -- so the more informative string was the one that
    # switched the gate off, while the lossy "15:00-21:00" switched it on. The dinner card is used
    # here because its window sits inside the hours: the only thing wrong is the weekday.
    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][1]
    card["venue_hours"] = "周二至周日 15:00-21:00"           # day 1 is a Monday
    card["hours_status"] = "verified"
    expect_fail_naming("venue closed on the weekday the meal is booked", p, ["Fixture Dinner"])

    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][1]
    card["venue_hours"] = "Tue-Sun 15:00-21:00"
    card["hours_status"] = "verified"
    expect_fail_naming("English weekday prefix is parsed too", p, ["Fixture Dinner"])

    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][1]
    # Fixture day 1 is a Monday. "Mittwoch-Samstag" shuts Sun+Mon, the common German Ruhetag
    # pattern, so the meal is booked on a closed day and the gate must say so.
    card["venue_hours"] = "Mittwoch-Samstag 15:00-21:00"
    card["hours_status"] = "verified"
    expect_fail_naming("German weekday prefix is parsed too", p, ["Fixture Dinner"])

    # The three two-letter abbreviations that mean different days in different languages must be
    # REFUSED, not guessed. French "Ma-Sa" is mardi-samedi; read as Dutch maandag-zaterdag it says
    # the venue opens Mondays, and the gate would then approve a dinner on the one day the kitchen
    # is shut. Refusing lands on the "hours are not machine-checkable" error, which tells the
    # author what to write instead -- a wrong answer would tell them nothing.
    for ambiguous in ("Ma-Sa 15:00-21:00", "Di-Sa 15:00-21:00", "Do-Sa 15:00-21:00"):
        p = copy.deepcopy(base)
        card = day(p, 1)["dining"][1]
        card["venue_hours"] = ambiguous
        card["hours_status"] = "verified"
        expect_fail_naming(f"ambiguous weekday abbreviation is refused, not guessed ({ambiguous[:5]})",
                           p, ["Fixture Dinner", "different days in different languages"])

    # The three shapes that must stay silent, because a gate that fires on correct authoring gets
    # switched off: a range that wraps past Sunday, a list, and hours that simply include Monday.
    # German and Dutch belong here rather than in a "nice to have" list: this skill's most common
    # cross-border trips are inside western Europe, and an author copying hours off a venue's own
    # site copies them in the venue's language. "Mo-Sa 09:00-18:00" is the standard form on German
    # opening-hours pages, and before these tokens existed it parsed as nothing -- so the rule that
    # rejects unparseable hours rejected an honest string, on exactly the trips this skill runs.
    for label, hours in [("wrapping range", "Sat-Mon 15:00-21:00"),
                         ("Chinese list", "周一、周三 15:00-21:00"),
                         ("open all week", "周一至周日 15:00-21:00"),
                         ("German short range", "Mo-So 15:00-21:00"),
                         ("German long range", "Montag-Sonntag 15:00-21:00"),
                         ("German täglich", "täglich 15:00-21:00"),
                         ("Dutch, written out", "maandag-zondag 15:00-21:00"),
                         ("Dutch dagelijks", "dagelijks 15:00-21:00")]:
        p = copy.deepcopy(base)
        card = day(p, 1)["dining"][1]
        card["venue_hours"] = hours
        card["hours_status"] = "verified"
        expect_ok(f"venue open on the scheduled weekday passes ({label})", p)

    # Hours nobody can parse must be reported, not skipped: "open late" is how a venue_hours field
    # gets filled in without anyone establishing when the venue is actually open.
    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][1]
    card["venue_hours"] = "open late"
    card["hours_status"] = "verified"
    expect_fail_naming("venue_hours that cannot be parsed", p, ["Fixture Dinner"])

    # 19b. A meal can sit on a real stop, inside the venue's real hours, on a day whose activities
    # never overlap, and still be impossible: the leg that carries the traveller to its anchor
    # costs time the window never budgeted. A Sunday lunch shipped written 13:00-14:30 at a stop
    # reachable no earlier than 14:15, leaving fifteen minutes of a ninety-minute window, and the
    # day had 142 minutes of slack overall so no span check could see it either.
    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["time_window"] = "09:10-09:30"
    expect_fail_naming("meal window opens before its own leg can deliver the traveller", p,
                       ["cannot arrive before", "09:25"])

    # The narrower half of the same rule, guarded on purpose: the first draft counted activities
    # ending before the window CLOSED, which swept in the meal's own activity slot and reported
    # three real dinners as impossible on a four-day plan. A meal whose window opens exactly when
    # the previous activity ends, with a modelled leg, must stay silent.
    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["time_window"] = "11:00-12:30"
    expect_ok("a meal with room after its leg passes", p)

    # 20. The weekday claim check settled Chinese prose only, so the same false statement in
    # English -- on a plan whose whole page is English -- went through untouched.
    p = copy.deepcopy(base)
    day(p, 1)["contingency"] = (
        "Day 1 (2026-09-28) is a Tuesday, so the guided tour runs as scheduled.")
    expect_fail("English weekday claim contradicts the date", p, "asserts")

    # And the reason that check must stay conservative: opening hours and closing days name other
    # weekdays on purpose, in English exactly as in Chinese.
    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["reservation_or_queue_note"] = (
        "Closed on Tuesday; the kitchen runs Monday to Saturday, 17:30-22:00.")
    expect_ok("English weekday ranges are not day claims", p)

    # 21. Backward compatibility, asserted rather than assumed: the three new fields are optional,
    # so a plan authored before they existed must pass exactly as it did. A gate that only holds
    # for plans written after it shipped is a gate nobody can adopt mid-trip.
    legacy = copy.deepcopy(base)
    legacy_blob = json.dumps(legacy, ensure_ascii=False)
    for field in ("traveler_constraints", "entry_context", "on_foot_minutes"):
        if field in legacy_blob:
            failures.append(
                f"backward compatibility: the fixture now carries {field!r}, so this case no "
                f"longer demonstrates that a plan without the new fields passes. Give it its own "
                f"copy of the plan with the new fields stripped.")
    expect_ok("plan carrying none of the new fields still passes", legacy)

    # ...and its mirror. A suite that only proves the new checks fire cannot tell a correct check
    # from a strict one, and the next author routes around a strict one.
    p = copy.deepcopy(base)
    p["trip"]["traveler_constraints"] = constraints(
        dietary_or_religious_needs=["no dairy"],
        allergy_severity="severe",
        allergy_card_text="我对乳制品严重过敏，请勿使用黄油、奶油或奶酪。",
        max_continuous_walking_minutes=60,
        mobility_notes=["Prefers step-free interchanges."])
    p["entry_context"] = {
        "status": "not_required",
        "summary": "Domestic trip; no entry formalities apply.",
        "traveler_basis": "resident of the destination country",
        "source_url": "https://www.gov.cn",
        "checked_at": "2026-07-30T10:00:00+08:00",
    }
    acts = day(p, 1)["activities"]
    acts[0].update({"duration_minutes": 120, "on_foot_minutes": 40})   # 09:00 -> 11:00
    acts[1].update({"duration_minutes": 90, "on_foot_minutes": 25})    # 15:00 -> 16:30
    day(p, 1)["route"]["walking_burden"] = (
        "Derived from segments: 20 minutes of walking between stops, plus 65 minutes on foot at "
        "the stops themselves (0 km on foot). Flat throughout, with seating at each stop.")
    expect_ok("a plan using all three new fields correctly passes", p)

    # 22. claims_checked as plan pointers. The integer it replaced was a promise the run wrote
    # about itself: the report and the plan were produced by the same run, so "claims_checked: 14"
    # cost one keystroke more than "claims_checked: 1" and neither cost a lookup. A pointer costs
    # what it claims -- to make ten of them resolve you have to open the plan ten times.

    # 22a. The shape that shipped. An operator holding an old report needs the message to name the
    # replacement and show one example, or the only thing they learn is that their report broke.
    report = full_verification()
    report["domains"][1]["claims_checked"] = 12
    # "number" is in the needles because a generic "must be a list" would also fire here, and an
    # operator holding a report full of counts needs to be told that the count itself is what went
    # away -- otherwise the obvious repair is to wrap it: "claims_checked": [12].
    expect_fail_naming("claims_checked is still an integer", copy.deepcopy(base),
                       ["claims_checked", "12", "number", "days[0].dining[0].venue_hours"], report)

    # ...and that repair, which is the first thing a hurried migration produces.
    report = full_verification()
    report["domains"][1]["claims_checked"] = [12, 3]
    expect_fail_naming("claims_checked wraps the old counts in a list", copy.deepcopy(base),
                       ["not a pointer string", "12"], report)

    # 22b. A pointer that resolves against nothing. This is the whole mechanism: if a fabricated
    # list were as cheap as a fabricated number, the migration would have bought nothing. The
    # message names the offending pointer because a report can carry dozens, and "a pointer failed"
    # leaves the author diffing the list by eye.
    report = full_verification()
    report["domains"][1]["claims_checked"].append("days[3].route.segments[0].fare_basis")
    expect_fail_naming("claims_checked pointer resolves against nothing", copy.deepcopy(base),
                       ["days[3].route.segments[0].fare_basis", "does not resolve"], report)

    # The same failure with the shape that reads most plausible: the fixture really has an
    # attraction_tickets array, it is simply empty, so a block claiming to have checked ticket
    # prices checked a ticket that does not exist.
    report = full_verification()
    report["domains"][3]["claims_checked"].append("booking_options.attraction_tickets[0].price_low")
    expect_fail_naming("pointer indexes past the end of a real list", copy.deepcopy(base),
                       ["booking_options.attraction_tickets[0].price_low", "does not resolve"], report)

    # 22c. Repeating a path inflates apparent coverage without opening anything new.
    report = full_verification()
    report["domains"][1]["claims_checked"].append("days[0].route.segments[0].fare_basis")
    expect_fail_naming("same pointer listed twice in one domain", copy.deepcopy(base),
                       ["days[0].route.segments[0].fare_basis", "twice"], report)

    # ...and the half that keeps that rule from being noise. Uniqueness is scoped to one block on
    # purpose: transport and the consistency auditor both opening days[0].route.duration_minutes is
    # two agents doing their job, and a global uniqueness rule would punish the overlap that makes
    # the fan-out worth running.
    report = full_verification()
    report["domains"][4]["claims_checked"].append("days[0].route.duration_minutes")
    expect_ok("the same pointer in two different blocks is legitimate", copy.deepcopy(base), report)

    # 22d. An empty list says exactly what "claims_checked: 0" said, so it fails for the same
    # reason. seasonality is used here rather than sights_and_hours because emptying the latter
    # also trips the coverage rule at 22f, and a case that fires two checks proves neither.
    report = full_verification()
    report["domains"][4]["claims_checked"] = []
    expect_fail_naming("claims_checked is an empty list", copy.deepcopy(base),
                       ["seasonality", "claims_checked: []"], report)
    # 22d-ii. The one empty block with a known cause: a plan with no entry_context gives the entry
    # domain nothing to point at. Met on 2026-09-24 building a verified domestic UK plan -- the
    # scaffold wrote an empty entry block, the gate refused it with "List the paths it examined",
    # and nothing said the missing piece was the plan's own entry answer.
    report = full_verification()
    for block in report["domains"]:
        if block.get("domain") == "entry" or block.get("name") == "entry":
            block["claims_checked"] = []
    no_entry = copy.deepcopy(base)
    no_entry.pop("entry_context", None)
    expect_fail_naming("an empty entry block on a plan with no entry answer says what to record",
                       no_entry, ["entry", "claims_checked: []", "not_required"], report)

    # 22e. A pointer whose value is null must PASS. Opening a field and finding it empty is real
    # verification work -- single_option_reason being null is how the completeness auditor learns
    # the plan is not hiding a sole-option decision. Demanding a non-null value would quietly
    # rewrite the rule into "cite only the fields somebody already filled in".
    report = full_verification()
    report["domains"][3]["claims_checked"] = [
        "booking_options.accommodations[0].single_option_reason",
        "booking_options.accommodations[1].single_option_reason",
        "regional_service_context.primary_map_exception_reason",
    ]
    expect_ok("pointers to fields whose value is null resolve", copy.deepcopy(base), report)

    # 22f. The one coverage rule, both directions. This is where the shipped defect lived: a
    # restaurant card declared its hours researched while they were wrong by 90 minutes at the
    # front and an hour at the back, and the meal sat on the venue's rest day -- and the report's
    # sights_and_hours block was clean, with a claims count in the double digits. Nothing tied the
    # count to the card, so nothing noticed that no verifier had ever opened it.
    report = full_verification()
    report["domains"][2]["claims_checked"] = ["days[0].activities[0].time",
                                              "days[0].dining[1].venue_url"]
    expect_fail_naming("sights_and_hours cites no researched dining card", copy.deepcopy(base),
                       ["days[0].dining[0]", "Fixture Lunch", "verified"], report)

    # Citing the card itself, rather than a field under it, is the same claim and must pass.
    report = full_verification()
    report["domains"][2]["claims_checked"] = ["days[0].dining[0]", "days[0].dining[1]",
                                              "days[0].activities[1].name"]
    expect_ok("citing the dining card itself satisfies coverage", copy.deepcopy(base), report)

    # Dropping a card's pointers pulls the requirement with it, so the rule cannot be dodged by
    # trimming the report after the plan was written. (This used to promote dining[1] from
    # "unverified" to "researched" instead; every card is researched now, because a card may no
    # longer name a seating time while admitting nobody checked the hours.)
    report = full_verification()
    report["domains"][2]["claims_checked"] = [c for c in report["domains"][2]["claims_checked"]
                                              if "dining[1]" not in c]
    expect_fail_naming("a card the report stopped citing must fail", copy.deepcopy(base),
                       ["days[0].dining[1]", "Fixture Dinner", "verified"], report)

    # And the boundary that keeps it low-noise: a card whose hours_status claims nothing demands
    # nothing. A rule that fired on honest "unverified" cards would make every plan with a
    # not-yet-checked dinner unshippable, and the cheapest escape from that is deleting the rule.
    p = copy.deepcopy(base)
    day(p, 1)["dining"][1]["venue_hours"] = "17:00-22:00"      # hours_status stays "unverified"
    expect_ok("a card that claims nothing is not demanded", p, full_verification())

    # 23. replan_context.must_reverify. A date shift is the one edit that invalidates researched
    # facts without touching them: opening hours, closure days, market days and Sunday retail law
    # are keyed to a WEEKDAY, so moving the window by a day makes all of them a guess while the
    # plan still looks complete and still passes every other check in this file. replan_trip.py
    # records each such fact; this is the gate that refuses to ship while one is still open.
    p = copy.deepcopy(base)
    p["replan_context"] = replan_context(must_reverify=[
        {"path": "days[0].dining[0].venue_hours",
         "reason": "weekday moved Monday -> Tuesday; these hours are weekday-keyed",
         "resolved": False, "resolution": None}])
    expect_fail_naming("replan leaves a researched fact unre-verified", p,
                       ["days[0].dining[0].venue_hours", "weekday-keyed"])

    p = copy.deepcopy(base)
    p["replan_context"] = replan_context(must_reverify=[
        {"path": "days[0].dining[0].venue_hours",
         "reason": "weekday moved Monday -> Tuesday; these hours are weekday-keyed",
         "resolved": True,
         "resolution": "Rechecked on the venue's own page: Tue 11:00-15:00, unchanged."}])
    expect_ok("every re-verification resolved passes", p)

    # The forgery this costs nothing to write and a human skimming the JSON reads as done.
    # "resolved": "yes" is truthy in most languages people reach for and is not the JSON literal
    # the gate tests, so the message has to say which one it found rather than just "unresolved".
    p = copy.deepcopy(base)
    p["replan_context"] = replan_context(must_reverify=[
        {"path": "days[0].dining[0].venue_hours",
         "reason": "weekday moved Monday -> Tuesday; these hours are weekday-keyed",
         "resolved": "yes", "resolution": "looked fine"}])
    expect_fail_naming("resolved is a truthy string, not the JSON literal true", p,
                       ["days[0].dining[0].venue_hours", "'yes'", "true"])

    # A shift can genuinely invalidate nothing -- a whole-week move keeps every weekday -- and a
    # replan that reports that honestly must not be punished for carrying the block at all.
    p = copy.deepcopy(base)
    p["replan_context"] = replan_context()
    expect_ok("a replan with nothing to re-verify passes", p)

    # And the compatibility half: replan_context is optional, so a plan that was never replanned
    # must pass exactly as it did before this key existed.
    if "replan_context" in json.dumps(base, ensure_ascii=False):
        failures.append(
            "backward compatibility: the fixture now carries replan_context, so the case below no "
            "longer shows that a plan without it is unaffected. Give it its own stripped copy.")
    expect_ok("a plan with no replan_context is unaffected", copy.deepcopy(base))

    failures += verification_banner_cases(base)
    # The CLI contract, proven by real processes: argv, file IO, exit codes, the stdout/stderr
    # split. Every other assertion in this file now runs in-process, 132x faster.
    failures += optional_label_cases(base)
    failures += fixture_passes_the_delivery_gate_cases(base)
    failures += example_label_file_cases(base)
    failures += ground_transport_cases(base)
    failures += ground_card_coverage_cases(base)
    failures += malformed_value_cases(base)
    failures += required_fields_reach_the_page_cases(base)
    failures += language_coverage_cases(base)
    # The clock check drops the leg out of the lodging as happening before the day's window --
    # unless a timed activity happens AT the lodging, which puts the traveller there during it. A
    # hotel breakfast made that leg free, hiding a morning that could not happen.
    start_point = day(base, 1)["route"]["start"]
    shape = [{"time": "08:30", "name": "Hotel breakfast", "area_or_venue": start_point,
              "duration_minutes": 70, "detail": "x"},
             {"time": "09:45", "name": "First stop", "area_or_venue": "Fixture activity A",
              "duration_minutes": 60, "detail": "y"},
             {"time": "11:00", "name": "Second stop", "area_or_venue": "Fixture activity B",
              "duration_minutes": 60, "detail": "z"}]
    p = copy.deepcopy(base)
    day(p, 1)["activities"] = copy.deepcopy(shape)
    expect_fail("lodging activity makes the outbound leg count", p, "does not close")

    p = copy.deepcopy(base)
    away = copy.deepcopy(shape)
    away[0]["area_or_venue"] = "Fixture activity A"   # same numbers, nobody at the lodging
    day(p, 1)["activities"] = away
    expect_ok("without a lodging activity the outbound leg stays outside the window", p)

    # 23. The three defects a user found in a delivered plan, after every gate above had passed.
    # A map URL parameter is a geocoder query, not a caption: the plan wrote its own Chinese
    # display label into origin=, Google resolved "酒店（拉斯坎特拉斯海滨）" -- literally the word
    # "hotel" plus a description -- to TAIWAN, and offered a 65-hour drive to the Canary Islands.
    # check_link_targets called all 25 map links ok, because the host was right and the status was
    # 200. The rule that catches it needs no geocoder: the straight line between a leg's endpoints
    # cannot be longer than the distance that leg claims.
    p = copy.deepcopy(base)
    seg = day(p, 1)["route"]["segments"][0]
    seg["verified_map_url"] = ("https://uri.amap.com/navigation?from=120.5174,24.0615,Hotel"
                               "&to=104.0700,30.6000,StopA&mode=bus")
    expect_fail("an endpoint that geocoded to another country", p, "km apart in a straight line")

    p = copy.deepcopy(base)
    route = day(p, 1)["route"]
    route["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1&origin=30.5723,104.0665"
                                 "&destination=30.6570,104.0817&waypoints=30.6000,104.0700"
                                 "&travelmode=transit")
    expect_fail("a transit route with waypoints, which Google refuses to compute", p,
                "does not compute those")

    p = copy.deepcopy(base)
    route = day(p, 1)["route"]
    route["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1&origin=30.5723,104.0665"
                                 "&destination=30.6570,104.0817&travelmode=walking")
    expect_fail("a walking button over a distance nobody walks", p, "WALKING directions over")

    # A venue with no quality signal is a taste assertion. The delivered plan shipped a dinner at a
    # restaurant that returns no listing anywhere, and two lunches at venues that open at 20:00.
    p = copy.deepcopy(base)
    for key in ("rating_value", "rating_scale", "rating_count", "rating_source", "rating_url",
                "rating_checked_at"):
        day(p, 1)["dining"][0].pop(key, None)
    expect_fail("a recommended venue with no rating at all", p, "needs a quality signal")

    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["rating_value"] = 3.1
    expect_fail("a venue below the 3.5/5 floor", p, "below")

    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["hours_status"] = "unverified"
    expect_fail("a meal put on the clock while nobody checked the hours", p,
                "is a claim the venue is open then")

    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["rating_status"] = "none"
    day(p, 1)["dining"][0]["rating_absence_reason"] = ""
    expect_fail("no rating and no reason for its absence", p, "rating_absence_reason is empty")

    # A comparison link that opens a city is not a link to the thing being compared. Because no
    # button ever opened either hotel on the platform that sells it, nobody saw that one cost more
    # than the traveller's whole budget cap and the other had no availability on those dates.
    p = copy.deepcopy(base)
    for option in p["booking_options"]["accommodations"]:
        option["comparison_searches"][0]["search_url"] = (
            "https://www.booking.com/searchresults.html?ss=Chengdu&checkin=2026-09-28"
            "&checkout=2026-09-29&group_adults=2&no_rooms=1")
    expect_fail("both hotels pointing at the same city search", p, "not scoped to this property")

    # 24. What the first version of section 23 could NOT catch, found by attacking it: the
    # distance rule only runs when both endpoints parse as coordinates, and the shipped bug used
    # free text throughout. Reproduced: relabel every endpoint with the original Chinese captions,
    # set every scope to primary_leg, and the checker exited 0 -- a gate that misses the bug it
    # was written for. Free text is now refused outright, because no offline check can tell
    # "Mercado de Vegueta" (which resolves) from "酒店（拉斯坎特拉斯海滨）" (which resolved to
    # Taiwan); only a geocoder can, and it is not here.
    p = copy.deepcopy(base)
    for seg in day(p, 1)["route"]["segments"]:
        seg["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1"
                                   "&origin=%E9%85%92%E5%BA%97&destination=%E5%B9%BF%E5%9C%BA"
                                   "&travelmode=transit")
    expect_fail("map endpoints written as free text, with the scope rule dodged", p,
                "is free text, not a coordinate pair")

    # transport_overview carries a pair too, and went uninspected in the first version.
    p = copy.deepcopy(base)
    p["transport_overview"]["overall_route_map_url"] = (
        "https://www.google.com/maps/dir/?api=1&origin=Hotel&destination=Airport&travelmode=transit")
    expect_fail("the overview map endpoint nobody was checking", p, "transport_overview")

    # A property whose name is not written in Latin script used to skip the scoping rule
    # entirely, because the tokeniser split on a Latin-only character class and returned nothing.
    # mainland China and Japan are core markets for this skill, so the hole exempted exactly the
    # travellers it mattered most for.
    for cjk in ("东京银座三井花园酒店", "ホテルグレイスリー新宿", "NH"):
        p = copy.deepcopy(base)
        option = p["booking_options"]["accommodations"][0]
        option["property_name"] = cjk
        option["comparison_searches"][0]["search_url"] = (
            "https://www.booking.com/searchresults.html?ss=Chengdu&checkin=2026-09-28"
            "&checkout=2026-09-29&group_adults=2&no_rooms=1")
        expect_fail(f"a city search behind the non-Latin name {cjk!r}", p,
                    "not scoped to this property")

    # And the other direction: a correctly scoped search must not be flagged, including when the
    # plan appends its own bracketed annotation to the property name.
    p = copy.deepcopy(base)
    option = p["booking_options"]["accommodations"][0]
    option["property_name"] = "东京银座三井花园酒店（仅限 16 岁以上）"
    option["comparison_searches"][0]["search_url"] = (
        "https://www.booking.com/searchresults.html?ss="
        "%E4%B8%9C%E4%BA%AC%E9%93%B6%E5%BA%A7%E4%B8%89%E4%BA%95%E8%8A%B1%E5%9B%AD%E9%85%92%E5%BA%97"
        "&checkin=2026-09-28&checkout=2026-09-29&group_adults=2&no_rooms=1")
    expect_ok("a property-scoped search under a bracketed non-Latin name", p)

    # 25. What an adversarial pass over section 24 found. The leg-length rule is RELATIVE, so it
    # is blind to a consistently reversed pair: writing lon,lat at both ends of a Las Palmas leg
    # leaves the points 4.73 km apart instead of 4.70 -- and moves every pin to latitude -15.4,
    # longitude 28.1, which is southern Africa. Measured, not imagined. One declared destination
    # coordinate makes every endpoint absolutely checkable.
    p = copy.deepcopy(base)
    for seg in day(p, 1)["route"]["segments"]:
        seg["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1"
                                   "&origin=-15.436633,28.139552&destination=-15.413464,28.102546"
                                   "&travelmode=transit")
        seg["distance_km"] = 6.2
    expect_fail("both endpoints reversed, which keeps the leg length plausible", p,
                "from the trip's declared destination")

    # And the anchor cannot be optional, or the rule above simply switches itself off.
    p = copy.deepcopy(base)
    p["trip"].pop("destination_coords", None)
    expect_fail("coordinates used with no declared destination to check them against", p,
                "trip.destination_coords is missing")

    # Deleting the declared distance used to switch the endpoint rule off entirely: _num()
    # returns 0.0 for a missing value, so the "no declared distance" fallback was dead code.
    p = copy.deepcopy(base)
    seg = day(p, 1)["route"]["segments"][0]
    seg.pop("distance_km", None)
    seg["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1"
                               "&origin=30.5723,104.0665&destination=40.416775,-3.703790"
                               "&travelmode=transit")
    expect_fail("an endpoint on another continent with no distance_km to check it against", p,
                "from the trip's declared destination")

    # 26. Two more the adversarial pass found, one of them self-inflicted. dest_id is Booking's
    # CITY identifier and had been added to the id allow-list, so the exemption whitelisted the
    # canonical city search -- the exact URL the rule exists to reject.
    p = copy.deepcopy(base)
    p["booking_options"]["accommodations"][0]["comparison_searches"][0]["search_url"] = (
        "https://www.booking.com/searchresults.html?ss=Chengdu&dest_id=-1899695&dest_type=city"
        "&checkin=2026-09-28&checkout=2026-09-29&group_adults=2&no_rooms=1")
    expect_fail("a city search wearing Booking's dest_id", p, "not scoped to this property")

    # The same "one option shown twice" defect the hotel rule was written for also shipped on
    # flights: both candidates in a delivered plan carried an identical round-trip search URL.
    p = copy.deepcopy(base)
    flights = p["booking_options"].get("flights") or []
    if len(flights) >= 2:
        flights[1]["round_trip_search_url"] = flights[0]["round_trip_search_url"]
        expect_fail("two flight candidates sharing one search URL", p,
                    "share the same round_trip_search_url")

    # 27. The four the adversarial pass listed that the previous round left open. Each is a rule
    # the docs already stated and nothing measured -- the class that produced all of this.
    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["venue_url"] = (
        "https://www.google.com/maps/search/?api=1&query="
        "%E9%85%92%E5%BA%97%E8%87%AA%E5%8A%A9%E6%97%A9%E9%A4%90")   # "hotel buffet breakfast"
    expect_fail("a venue link that searches a description instead of the venue", p,
                "searches something else")

    # OpenStreetMap packs both ends into one parameter, so an OSM-routed plan carried no endpoint
    # the checker could see at all.
    p = copy.deepcopy(base)
    seg = day(p, 1)["route"]["segments"][0]
    seg["verified_map_url"] = ("https://www.openstreetmap.org/directions"
                               "?route=104.0665%2C30.5723%3B-15.41%2C28.10")
    expect_fail("an OSM route= pair pointing off the map", p, "from the trip's declared destination")

    # The multi_stop rule demanded waypoints and then never counted them, so one throwaway
    # waypoint certified a day of any length.
    p = copy.deepcopy(base)
    route = day(p, 1)["route"]
    route["route_map_scope"] = "multi_stop"
    route["stops_in_order"] = ["A", "B", "C", "D", "E"]
    route["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1&origin=30.5723,104.0665"
                                 "&destination=30.6570,104.0817&waypoints=30.60,104.07"
                                 "&travelmode=walking")
    expect_fail("one waypoint standing in for a five-stop day", p, "waypoint(s), but the day has")

    # A checked alternative is a button too, and nothing looked inside one.
    p = copy.deepcopy(base)
    day(p, 1)["route"]["segments"][0]["alternative_map_links"] = [
        {"provider": "Apple", "url": "https://maps.apple.com/?saddr=%E9%85%92%E5%BA%97&daddr=%E5%B9%BF%E5%9C%BA",
         "checked_at": "2026-07-30", "map_link_kind": "directions", "note": "alt"}]
    expect_fail("a caption hiding in a checked alternative link", p, "is free text")

    # 28. The doc-sync audit found two more, both the same shape as the CJK hole: an allow-list
    # protects the alphabets whoever wrote it thought of and goes quiet everywhere else. The
    # second version kept Latin, kana, CJK and hangul -- and silently exempted Cyrillic, Greek,
    # Thai, Arabic, Hebrew and Devanagari. _fold now keeps whatever Unicode calls alphanumeric.
    for name in ("Кафе Пушкинъ", "Ταβέρνα Ψαρρά", "ร้านอาหารบ้านไทย", "مطعم الشرق",
                 "מלון דן", "होटल ताज"):
        p = copy.deepcopy(base)
        option = p["booking_options"]["accommodations"][0]
        option["property_name"] = name
        option["comparison_searches"][0]["search_url"] = (
            "https://www.booking.com/searchresults.html?ss=Chengdu&checkin=2026-09-28"
            "&checkout=2026-09-29&group_adults=2&no_rooms=1")
        expect_fail(f"a city search behind the name {name!r}", p, "not scoped to this property")

    # And the other direction, so the rule cannot be satisfied by rejecting everything.
    p = copy.deepcopy(base)
    option = p["booking_options"]["accommodations"][0]
    option["property_name"] = "Кафе Пушкинъ"
    option["comparison_searches"][0]["search_url"] = (
        "https://www.booking.com/searchresults.html?ss="
        "%D0%9A%D0%B0%D1%84%D0%B5%20%D0%9F%D1%83%D1%88%D0%BA%D0%B8%D0%BD%D1%8A"
        "&checkin=2026-09-28&checkout=2026-09-29&group_adults=2&no_rooms=1")
    expect_ok("a property-scoped search under a Cyrillic name", p)

    # The skeleton writes {"lat": 0, "lon": 0}, which the anchor check reads as not-yet-filled.
    # Saying "missing" about a field that is visibly present sends the author looking for the
    # wrong thing, so the placeholder gets its own sentence.
    p = copy.deepcopy(base)
    p["trip"]["destination_coords"] = {"lat": 0, "lon": 0}
    expect_fail("destination_coords left at the skeleton's zeros", p, "still at its placeholder")

    # 29. Hotels were judged on price and location and nothing else -- a traveller asked why the
    # standard that applies to a dinner did not apply to a week of nights, and the answer was
    # that guest_rating_* existed only as a field one plan invented, enforced and rendered by
    # nothing. Booking publishes out of 10 where Google publishes out of 5, so the scale rides
    # with the value.
    p = copy.deepcopy(base)
    for key in ("guest_rating_value", "guest_rating_scale", "guest_rating_count",
                "guest_rating_source"):
        p["booking_options"]["accommodations"][0].pop(key, None)
    expect_fail("a hotel with no guest rating at all", p, "needs the same quality evidence")

    p = copy.deepcopy(base)
    p["booking_options"]["accommodations"][0]["guest_rating_value"] = 6.4
    expect_fail("a hotel below the 7.0/10 floor", p, "below the 7.0/10 floor")

    # The floor is applied in one scale, so a 5-point score must be converted rather than
    # compared raw -- 3.4/5 is 6.8/10 and fails; comparing 3.4 against 7.0 would fail every
    # Google-scored property ever entered.
    p = copy.deepcopy(base)
    option = p["booking_options"]["accommodations"][0]
    option["guest_rating_scale"] = 5
    option["guest_rating_value"] = 4.4
    expect_ok("a 4.4/5 hotel, which is 8.8/10 and fine", p)

    p = copy.deepcopy(base)
    option = p["booking_options"]["accommodations"][0]
    option["guest_rating_status"] = "none"
    option["guest_rating_absence_reason"] = ""
    expect_fail("no hotel rating and no reason for its absence", p, "with no reason")

    # 30. Two route defects that every existing gate passed, both introduced by swapping
    # coordinates into a plan whose numbers were written before it had any.
    p = copy.deepcopy(base)
    seg = day(p, 1)["route"]["segments"][0]
    seg["mode"] = "步行"
    seg["distance_km"] = 1.3
    seg["duration_minutes"] = 6
    expect_fail("a 1.3 km walk given six minutes", p, "which is running")

    # A leg whose endpoints belong to a different pair of stops keeps every other rule happy:
    # both coordinates are real places in the right city, and the distance between them is
    # plausible. What gives it away is that the leg claims to be five times longer than the gap
    # between its own ends.
    p = copy.deepcopy(base)
    seg = day(p, 1)["route"]["segments"][0]
    seg["distance_km"] = 30.0
    seg["duration_minutes"] = 45
    seg["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1&origin=30.5723,104.0665"
                               "&destination=30.6000,104.0700&travelmode=transit")
    expect_fail("a leg five times longer than the gap between its own endpoints", p,
                "apart (")

    # 31. Booking convenience, which is a property of what a button opens rather than of how it
    # is labelled. A search that does not carry the trip's dates makes the traveller type the
    # journey in twice, and the prefilled-fields list was a promise the plan wrote about itself
    # until it was compared to the URL beside it. Providers spell dates differently, so every
    # common encoding counts.
    p = copy.deepcopy(base)
    flights = p["booking_options"].get("flights") or []
    if len(flights) >= 1:
        flights[0]["round_trip_search_url"] = "https://www.skyscanner.net/transport/flights/ams/lpa/"
        expect_fail("a flight search URL with no dates in it", p, "does not carry the outbound date")

    p = copy.deepcopy(base)
    option = p["booking_options"]["accommodations"][0]
    option["comparison_searches"][0]["search_url"] = (
        "https://www.booking.com/searchresults.html?ss=" + "Fixture%20Hotel%20A")
    expect_fail("a hotel search scoped to the property but stripped of its dates", p,
                "does not carry the check-in date")

    # A bare host root under a button that reads "view the official direct-booking page" promises
    # a booking page and delivers a front door. Two flight cards shipped that way.
    p = copy.deepcopy(base)
    p["booking_options"]["accommodations"][0]["direct_review_url"] = "https://www.marriott.com"
    expect_fail("a home page labelled as the official direct-booking page", p, "a bare home page")

    # And the shape that is allowed: an own-site link with no dates is fine -- many carriers
    # cannot be deep-linked at all -- as long as it is about this product.
    p = copy.deepcopy(base)
    p["booking_options"]["accommodations"][0]["direct_review_url"] = (
        "https://www.marriott.com/hotels/fixture-hotel-a")
    expect_ok("an own-site property page carrying no dates", p)

    # 32. A placeholder must announce itself, not masquerade as a bad answer. The skeleton writes
    # rating_value 0, and the floor rule read that as "you are recommending a venue rated 0/5.
    # Replace it" -- sending the author to hunt for a badly-reviewed restaurant nobody chose. A
    # fresh four-day skeleton produced 38 errors that way; it now produces 13, one per real task.
    # Both directions are pinned here, because the cheap way to pass the first half is to stop
    # checking anything.
    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][0]
    card["venue_name"] = "TODO: venue for lunch"
    card["venue_url"] = "https://example.invalid/TODO-replace-with-a-researched-url"
    card["rating_value"] = 0
    expect_fail_naming("an unfilled dining card reports as unfilled", p,
                       ["placeholder"], full_verification())

    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][0]
    card["venue_name"] = "TODO: venue for lunch"
    card["rating_value"] = 0
    ok, output = run(p)
    if "below the 3.5/5 floor" in output:
        failures.append("an unfilled dining card must not be accused of being badly rated: "
                        + output)

    # And the guard must not become a way to switch the rule off: a card that IS filled in and
    # rated 3.1/5 still fails.
    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["rating_value"] = 3.1
    expect_fail("a filled-in card rated 3.1/5", p, "below the 3.5/5 floor")

    p = copy.deepcopy(base)
    p["booking_options"]["accommodations"][0]["property_name"] = "TODO: property 1"
    ok, output = run(p)
    if "below the 7.0/10 floor" in output:
        failures.append("an unfilled accommodation must not be accused of a low guest score: "
                        + output)

    p = copy.deepcopy(base)
    p["booking_options"]["accommodations"][0]["guest_rating_value"] = 6.2
    expect_fail("a filled-in hotel rated 6.2/10", p, "below the 7.0/10 floor")

    # 33. Three findings from the strict self-check, each a rule that was wrong rather than merely
    # missing. The worst is the one that broke the market this skill mandates Amap for: range
    # alone cannot tell lat,lon from lon,lat, so Ürümqi (87.6,43.8) written in Amap's documented
    # order was read as latitude 87.6 and reported 4,946 km away in the Arctic -- and an author
    # who "checked the coordinate order" as the message demanded got a green gate and every
    # button pointing at the Arctic. The order comes from the provider now.
    p = copy.deepcopy(base)
    seg = day(p, 1)["route"]["segments"][0]
    p["trip"]["destination_coords"] = {"lat": 43.8256, "lon": 87.6168}
    seg["verified_map_url"] = ("https://uri.amap.com/navigation?from=87.6168,43.8256,Hotel"
                               "&to=87.6300,43.8400,Park&mode=bus")
    seg["distance_km"] = 2.5
    day(p, 1)["route"]["verified_map_url"] = seg["verified_map_url"]
    day(p, 1)["route"]["distance_km"] = 2.5
    ok, output = run(p)
    if "from the trip's declared destination" in output:
        failures.append("a correct Amap lon,lat pair west of 90 degrees must not be accused of "
                        "being on another continent: " + output)

    # The same URL written in the wrong dialect for that provider still fails, because otherwise
    # the fix would have silently repaired the plan's text while the button stayed broken.
    p = copy.deepcopy(base)
    p["trip"]["destination_coords"] = {"lat": 43.8256, "lon": 87.6168}
    seg = day(p, 1)["route"]["segments"][0]
    seg["verified_map_url"] = ("https://uri.amap.com/navigation?from=43.8256,87.6168,Hotel"
                               "&to=43.8400,87.6300,Park&mode=bus")
    seg["distance_km"] = 2.5
    expect_fail("an Amap URL written lat,lon", p, "from the trip's declared destination")

    # A floor whose error message offers an escape no code reads rejects the honest author and
    # waves through the one who flips a status field. Both halves are pinned.
    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][0]
    card["rating_value"] = 3.4
    card["rating_below_floor_reason"] = "The only kitchen in town serving this dietary need."
    expect_ok("a below-floor venue with the reason the message asks for", p)

    p = copy.deepcopy(base)
    card = day(p, 1)["dining"][0]
    card["rating_value"] = 3.4
    card["rating_status"] = "none"
    card["rating_absence_reason"] = "market stall"
    expect_fail("a floor dodged by flipping rating_status while keeping the score", p,
                "cannot both have a")

    p = copy.deepcopy(base)
    option = p["booking_options"]["accommodations"][0]
    option["guest_rating_value"] = 6.2
    option["guest_rating_below_floor_reason"] = "The only accessible room in the village."
    expect_ok("a below-floor hotel with its reason", p)

    p = copy.deepcopy(base)
    option = p["booking_options"]["accommodations"][0]
    option["guest_rating_status"] = "none"
    option["guest_rating_absence_reason"] = "newly opened"
    option["guest_rating_value"] = 6.2
    expect_fail("a hotel floor dodged the same way", p, "how a floor gets dodged")

    # 34. The two boundaries the self-check found, where a rule that was right in the common case
    # rejected a real trip. Neither is fixed by moving a number: a Norwegian fjord crossing runs
    # 5.0x its straight line and a leg pointing at the wrong stop ran 5.1x, so the author declares
    # the detour rather than the checker guessing at it.
    p = copy.deepcopy(base)
    seg = day(p, 1)["route"]["segments"][0]
    # A drive, said as one: the fixture's leg is a metro ride, and a metro leg with a driving button
    # is its own finding now (check_map_link_modes) -- this case is about the detour, not the mode.
    seg["mode"] = "驾车"
    seg["distance_km"] = 350.0
    seg["duration_minutes"] = 270
    seg["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1&origin=30.5723,104.0665"
                               "&destination=30.6000,104.0700&travelmode=driving")
    seg["detour_reason"] = "No road crosses the canyon; the drive rounds it via Marble Canyon."
    route = day(p, 1)["route"]
    route["distance_km"] = sum(s["distance_km"] for s in route["segments"])
    route["duration_minutes"] = sum(s["duration_minutes"] for s in route["segments"])
    route["detour_reason"] = seg["detour_reason"]
    # This case and the anchor case below reach for a Google URL because Google's lat,lon dialect
    # is what the coordinate rule under test reads. The fixture's market is mainland China, where
    # a Google link is now a finding in its own right, so the market moves with the link -- a
    # coordinate test must not depend on shipping an unopenable button.
    open_market(p)
    expect_ok("a genuine detour declared in detour_reason", p)

    # Without the declaration the same shape is still refused, or the field would be a way to
    # switch the rule off rather than to answer it.
    p = copy.deepcopy(base)
    seg = day(p, 1)["route"]["segments"][0]
    seg["mode"] = "驾车"
    seg["distance_km"] = 350.0
    seg["duration_minutes"] = 270
    seg["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1&origin=30.5723,104.0665"
                               "&destination=30.6000,104.0700&travelmode=driving")
    expect_fail("the same detour with nothing said about it", p, "apart (")

    # A trip can have more than one base. New York and Los Angeles are 3,936 km apart, so a
    # single anchor put one of them outside any useful radius.
    p = copy.deepcopy(base)
    p["trip"]["destination_coords"] = [{"lat": 30.5723, "lon": 104.0665},
                                       {"lat": 39.9042, "lon": 116.4074}]
    seg = day(p, 1)["route"]["segments"][0]
    seg["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1&origin=39.9042,116.4074"
                               "&destination=39.9100,116.4200&travelmode=transit")
    seg["distance_km"] = 1.8
    route = day(p, 1)["route"]
    route["distance_km"] = sum(s["distance_km"] for s in route["segments"])
    open_market(p)
    expect_ok("a second city declared as a second anchor", p)

    # And a point near neither base is still wrong.
    p = copy.deepcopy(base)
    p["trip"]["destination_coords"] = [{"lat": 30.5723, "lon": 104.0665},
                                       {"lat": 39.9042, "lon": 116.4074}]
    seg = day(p, 1)["route"]["segments"][0]
    seg["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1&origin=28.1395,-15.4366"
                               "&destination=28.1476,-15.4291&travelmode=transit")
    seg["distance_km"] = 2.0
    expect_fail("a point near neither declared base", p, "from the trip's declared destination")

    # 35. The three the self-check listed as minor and left open. Each is small; each is the
    # shape that has produced every larger defect here -- a rule stated somewhere and measured
    # nowhere.
    p = copy.deepcopy(base)
    seg = day(p, 1)["route"]["segments"][0]
    seg["verified_map_url"] = ("https://www.google.com/maps/dir/?api=1&origin=30.5723,104.0665"
                               "&destination=30.6000,104.0700"
                               "&destination_place_id=ChIJsomewhereelse&travelmode=transit")
    expect_fail("a URL carrying both coordinates and a place id", p, "place id")

    # "Read the price off the platform page" cannot be watched, but its shadow can: a page that
    # gave you today's price also said whether the dates were sellable. The plan that prompted
    # this release shipped a sold-out hotel marked unknown.
    p = copy.deepcopy(base)
    option = p["booking_options"]["accommodations"][0]
    option["price_status"] = "researched_current"
    option["availability_status"] = "unknown"
    expect_fail("a researched price beside an unknown availability", p, "sellable")

    p = copy.deepcopy(base)
    option = p["booking_options"]["accommodations"][0]
    option["price_status"] = "estimate"
    option["availability_status"] = "unknown"
    expect_ok("an estimated price beside an unknown availability, which is consistent", p)

    # The duplicate-URL rule was keyed on stay_group_id, a label the same author writes -- so
    # filing two hotels under different groups was enough to let them share one link.
    p = copy.deepcopy(base)
    first, second = p["booking_options"]["accommodations"][0], p["booking_options"]["accommodations"][1]
    second["stay_group_id"] = first["stay_group_id"] + "-other"
    second["comparison_searches"][0]["search_url"] = first["comparison_searches"][0]["search_url"]
    expect_fail("two hotels in different stay groups sharing one comparison URL", p,
                "share the same comparison")

    # 36. A user opened a delivered page and found a whole paragraph printed as
    # "这 · 是 · 路 · 线 · 概 · 览" -- every character of it, spaced by dots. transport_overview.notes
    # is a list of strings, it was written as one string, and the renderer joins these: iterating a
    # str yields its characters. Every gate passed, because the value was a perfectly good string
    # and the join was perfectly good code, and nothing checked the TYPE.
    for path, setter in (
        ("transport_overview.notes",
         lambda p, v: p["transport_overview"].__setitem__("notes", v)),
        ("assumptions", lambda p, v: p.__setitem__("assumptions", v)),
        ("recheck_before_purchase", lambda p, v: p.__setitem__("recheck_before_purchase", v)),
        ("budget.included_categories",
         lambda p, v: p["budget"].__setitem__("included_categories", v)),
    ):
        p = copy.deepcopy(base)
        setter(p, "one paragraph written as a bare string instead of a one-element list")
        expect_fail(f"{path} given a bare string", p, "the contract declares it a list")

    # A correctly-typed list still passes, or the rule would just forbid the field.
    p = copy.deepcopy(base)
    p["transport_overview"]["notes"] = ["first note", "second note"]
    expect_ok("notes as a real list of strings", p)

    # 37. The second thing the same traveller reported, after the dot-separated characters: the
    # overview's header printed a leg's duration beside the whole trip's fare, and one of its
    # sentences still said "about 25 minutes" after the leg had been corrected to 35. Both are
    # the prose class -- text that restates data and then drifts from it, or that assumes a
    # renderer it does not have.
    p = copy.deepcopy(base)
    p["transport_overview"]["notes"] = ["这是**路线概览**，不是全天路线"]
    expect_fail("Markdown emphasis in a prose field", p, "contains Markdown emphasis")

    p = copy.deepcopy(base)
    day(p, 1)["dining"][0]["why_this_stop"] = "**这家**是唯一的选择"
    expect_fail("Markdown emphasis in a dining rationale", p, "contains Markdown emphasis")

    # A lone asterisk is usually a footnote, and flagging those would make the rule arguable.
    p = copy.deepcopy(base)
    p["transport_overview"]["notes"] = ["票价见站台标示 * 以当日为准"]
    expect_ok("a lone asterisk, which is a footnote and not emphasis", p)

    # Prose that restates a leg's duration must restate it correctly.
    leg = min(int(s["duration_minutes"]) for d in base["days"]
              for s in d["route"]["segments"] if s.get("duration_minutes"))
    # 15 sits within three minutes of a real leg -- close enough to read as a restatement,
    # and not equal to any leg, which is the drift shape. The window is three rather than five
    # because 40 once sat within five of a 35-minute leg while describing a lift's last ascent.
    p = copy.deepcopy(base)
    p["transport_overview"]["notes"] = ["机场巴士约 15 分钟"]
    expect_fail("a note whose minutes drift from the leg they describe", p, "drifts from it")

    p = copy.deepcopy(base)
    p["transport_overview"]["notes"] = [f"机场巴士约 {leg} 分钟"]
    expect_ok("a note quoting the leg's own figure", p)

    # And a number that describes something else entirely is not a drift.
    p = copy.deepcopy(base)
    p["transport_overview"]["notes"] = ["电梯末班为闭馆前 40 分钟"]
    expect_ok("a minute figure about something other than a leg", p)

    # Neither of these is a restatement, and the first version of the rule flagged both -- which
    # is how a check earns the reputation that gets it routed around.
    p = copy.deepcopy(base)
    p["transport_overview"]["notes"] = ["两段原本超过 30 分钟的步行已改为公交接驳"]
    expect_ok("a limit, introduced by a comparison word, not a leg duration", p)

    p = copy.deepcopy(base)
    p["transport_overview"]["notes"] = ["机场巴士约 20–35 分钟（视路况）"]
    expect_ok("a range, where neither end is a single claim about a leg", p)

    # 38. The other half of the map-link problem: the coordinate rule fixed where a link points,
    # not who can open it. render_final_trip_html.map_link_allowed already covered part of this,
    # and saying so matters -- each case below sits in the part it did not reach: it keys on the
    # market string being exactly "mainland_china", reads three route fields, and never looks at
    # `unknown` access. This lint saw none of it at all: the shipped Beijing plan scored 36 errors
    # before its 18 Amap links were swapped for Google ones and 36 after. check_link_targets.py
    # cannot cover it either -- it asks whether a host answers the machine running it, which is
    # never the machine inside the blocked market.
    p = copy.deepcopy(base)
    day(p, 1)["route"]["verified_map_url"] = (
        "https://www.google.com/maps/dir/?api=1&origin=30.657,104.066"
        "&destination=30.664,104.083&travelmode=transit")
    expect_fail("a Google link in a market the plan itself calls unavailable", p,
                "cannot open where they will be standing")

    # The declaration must not contradict itself in the other direction either: a plan cannot
    # call its market mainland China and then claim Google works there.
    p = copy.deepcopy(base)
    p["regional_service_context"]["google_services_access"] = "available"
    expect_fail("a restricted market declared with Google available", p,
                "the honest value is 'unavailable'")

    # 'unknown' is the value that looks harmless and is not: it means nobody checked, on a button
    # the traveller is being asked to press. Two shipped plans sat in exactly this state.
    p = copy.deepcopy(base)
    p["regional_service_context"]["destination_service_market"] = "united_states"
    p["regional_service_context"]["google_services_access"] = "unknown"
    p["regional_service_context"]["primary_map_provider"] = "Google Maps"
    day(p, 1)["route"]["verified_map_url"] = (
        "https://www.google.com/maps/dir/?api=1&origin=30.657,104.066"
        "&destination=30.664,104.083&travelmode=transit")
    expect_fail("Google links shipped while access is unknown", p, "nobody established")

    # An unnamed market cannot be defended by any of the rules above, so the omission is the
    # finding rather than a silent exemption from all three.
    p = copy.deepcopy(base)
    p["regional_service_context"]["destination_service_market"] = ""
    expect_fail("no declared market at all", p, "destination_service_market is empty")

    # Both false positives this rule produced on its first draft, kept as tests because each one
    # accused a plan that was doing exactly the right thing. The cause was one mistake made
    # twice: comparing a provider's display name to a host, i.e. asking whether '高德地图'
    # appears in 'uri.amap.com'. It does not, and neither does 'Google 地图' appear in
    # 'www.google.com'. A rule that fires on correct work is worse than no rule -- it is the
    # rule everyone learns to route around.
    p = copy.deepcopy(base)
    p["regional_service_context"]["primary_map_provider"] = "高德地图 / Amap"
    expect_ok("a Chinese provider name against its Latin host", p)

    # The same false positive in its other language. Built by converting the fixture's own Amap
    # links to Google ones -- same places, coordinate order flipped to Google's dialect -- so the
    # plan stays internally true and the only thing under test is whether 'Google 地图' is
    # recognised as owning google.com.
    def to_google(plan: dict) -> dict:
        def convert(url: str) -> str:
            query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
            ends = []
            for key in ("from", "to"):
                lon, lat = query[key][0].split(",")[:2]
                ends.append(f"{lat},{lon}")
            return (f"https://www.google.com/maps/dir/?api=1&origin={ends[0]}"
                    f"&destination={ends[1]}&travelmode=transit")

        def walk(node):
            if isinstance(node, dict):
                return {k: (convert(v) if isinstance(v, str) and "uri.amap.com" in v else walk(v))
                        for k, v in node.items()}
            if isinstance(node, list):
                return [walk(v) for v in node]
            return node

        return walk(plan)

    p = to_google(copy.deepcopy(base))
    p["regional_service_context"]["destination_service_market"] = "spain_eu"
    p["regional_service_context"]["google_services_access"] = "available"
    p["regional_service_context"]["primary_map_provider"] = "Google 地图"
    expect_ok("a Chinese-labelled Google provider against google.com", p)

    # Hong Kong, Macau and Taiwan are separate markets where Google works. They stay clear of the
    # restricted rule because it matches only explicit 'mainland' spellings, never a bare 'china'.
    p = copy.deepcopy(base)
    p["regional_service_context"]["destination_service_market"] = "hong_kong_china"
    p["regional_service_context"]["google_services_access"] = "available"
    expect_ok("a market whose name contains china but is not mainland", p)

    # The escape hatch has to actually work, or the rule becomes unsatisfiable for the legitimate
    # mixed case -- an official venue map, a rail operator's own planner.
    p = copy.deepcopy(base)
    p["regional_service_context"]["primary_map_provider"] = "Baidu Maps"
    p["regional_service_context"]["primary_map_exception_reason"] = (
        "Amap deep links are used for navigation because the venue pages publish Amap "
        "coordinates; Baidu remains the traveller's default app for search.")
    expect_ok("an off-provider map link with the declared reason", p)

    p = copy.deepcopy(base)
    p["regional_service_context"]["primary_map_provider"] = "Baidu Maps"
    expect_fail("an off-provider map link with no reason", p,
                "primary_map_exception_reason is empty")

    # 39. Two messages that were right about the exit code and wrong about the reason, which is a
    # failure mode this skill keeps rediscovering: the Ürümqi coordinate error told an author to
    # "fix the order" and handed them a green gate with every pin in the Arctic.
    report = full_verification()
    report["domains"][0].pop("domain")
    expect_fail("a verification block with no domain key", copy.deepcopy(base),
                "have no 'domain' key naming which", report)

    report = full_verification()
    report["audits"][0].pop("audit")
    expect_fail("a verification block with no audit key", copy.deepcopy(base),
                "have no 'audit' key naming which", report)

    # Only the lower bound of the date window was checked, so a report could be stamped years
    # ahead -- the one direction that makes stale research look freshly confirmed.
    report = full_verification()
    report["checked_at"] = "2099-01-01"
    expect_fail("a verification report dated in the future", copy.deepcopy(base),
                "which is in the future", report)

    # 40. The first check in this file that measures whether the plan is the trip that was ASKED
    # for rather than whether it is safe and self-consistent. validate_plan already counts anchors
    # -- three minimum on a multi-day city trip -- so the gap is not that nothing looked, it is
    # that nothing asked whether an anchor answers anything: rewriting every one of them as
    # "somewhere" / "no particular reason" produced zero findings from that rule and zero from all
    # nineteen checks here. The intake had collected "coast is my must-have"; the plan had no
    # field to put it in, so SKILL.md's "do not substitute a list of famous sights for real fit"
    # had a headcount behind it and nothing else.
    p = copy.deepcopy(base)
    p["trip"]["traveler_preferences"]["ranked_must_haves"] = ["street food", "harbour walking"]
    expect_fail("a must-have no anchor answers", p, "ranked 'harbour walking' as a must-have")

    # The escape is a declared reason, not an empty field -- the season really can make a
    # must-have impossible, and saying so is a different act from ignoring it.
    p = copy.deepcopy(base)
    p["trip"]["traveler_preferences"]["ranked_must_haves"] = ["street food", "harbour walking"]
    p["trip"]["traveler_preferences"]["unmet_preferences"] = [
        {"preference": "harbour walking",
         "reason": "The harbour promenade is closed for works through the travel window."}]
    expect_ok("a must-have excused with what makes it impossible", p)

    p = copy.deepcopy(base)
    p["trip"]["traveler_preferences"]["ranked_must_haves"] = ["street food", "harbour walking"]
    p["trip"]["traveler_preferences"]["unmet_preferences"] = [
        {"preference": "harbour walking", "reason": ""}]
    expect_fail("an unmet must-have with no reason", p, "no reason")

    # A typo in satisfies_preference silently un-answers a must-have, so a claim that matches
    # nothing the traveller said is the finding rather than a harmless extra.
    p = copy.deepcopy(base)
    p["destination_experience_anchors"][0]["satisfies_preference"] = "street foods"
    expect_fail("an anchor answering a preference nobody stated", p, "never stated")

    # Softer preferences advise rather than bind: "prefer mild warmth" is a quality of a choice
    # already made, not a thing the days must contain, and failing on it would fire every winter.
    p = copy.deepcopy(base)
    p["trip"]["traveler_preferences"]["natural_subtypes"] = ["lakes"]
    expect_ok("an unanswered soft preference is a note, not an error", p)

    # The avoid list is answered rather than pattern-matched: deciding from a plan's own fields
    # whether it contains a red-eye needs a different fact for every entry a traveller might
    # write, while asking how each was honoured needs none.
    p = copy.deepcopy(base)
    p["trip"]["traveler_preferences"]["avoid_list_handling"] = []
    expect_fail("an avoidance the plan says nothing about", p, "says nothing about it")

    p = copy.deepcopy(base)
    p["trip"]["traveler_preferences"]["avoid_list_handling"] = [
        {"item": "red-eye arrivals", "how_avoided": ""}]
    expect_fail("an avoidance handled with no explanation", p, "no how_avoided")

    # Omission must not be the escape. Every hole this skill has closed had the same shape: a rule
    # that only ran when the author filled in the field it read.
    p = copy.deepcopy(base)
    p["trip"].pop("traveler_preferences")
    expect_fail("a plan carrying no preferences at all", p, "traveler_preferences is missing")

    # An empty block is a claim -- the traveller stated no must-have -- and must stay legal, or
    # the rule becomes impossible to satisfy for a traveller who genuinely wants "anywhere warm".
    p = copy.deepcopy(base)
    p["trip"]["traveler_preferences"] = {"ranked_must_haves": [], "natural_subtypes": [],
                                         "human_cultural_subtypes": [], "pace": None,
                                         "avoid_list": [], "avoid_list_handling": [],
                                         "unmet_preferences": []}
    p["destination_experience_anchors"][0]["satisfies_preference"] = None
    expect_ok("a traveller who stated no preferences", p)

    # 41. How the page reads, which no gate had ever looked at. Two faults, both measured on
    # delivered plans rather than imagined -- and neither is purple prose: the writing in those
    # plans is specific and reason-led, with no "vibrant tapestry" anywhere, and it still reads
    # generated.
    #
    # The page printing one sentence twice. `focus` and `route_logic` came back byte-identical on
    # 4 of 5 days of one shipped plan and 5 of 8 of another, and `fallback_plan` duplicated
    # `contingency` on nearly every day of the first. Each field alone was filled in and sensible,
    # so nothing fired.
    p = copy.deepcopy(base)
    day(p, 1)["route"]["route_logic"] = day(p, 1)["focus"]
    expect_fail("one sentence printed under two headings on the same card", p, "repeats")

    # Across days it must stay quiet: two days can honestly carry the same wet-weather fallback,
    # and an error there fires on correct work -- it fired on a test that clones a day on purpose
    # to exercise replanning.
    p = copy.deepcopy(base)
    p["days"].append(copy.deepcopy(day(p, 1)))
    p["days"][1]["number"] = 2
    p["days"][1]["date"] = "2026-09-29"
    p["trip"]["end_date"] = "2026-09-29"
    code, out = run(p)
    if "repeats" in out:
        failures.append(f"identical prose on two different days must not be an error\n{out}")

    # One sentence shape used for everything. The dash is not the fault; the monotony is, and
    # Wikipedia's "Signs of AI writing" lists em-dash overuse for exactly that reason. Measured at
    # 50% of narrative fields on a shipped plan, so the ceiling is 35% -- available where it earns
    # its place, refused as the default way a sentence is built.
    p = copy.deepcopy(base)
    for index, d in enumerate(p["days"]):
        d["focus"] = f"第 {index + 1} 天中央市场开到 15:00、城堡开到 18:00——把两件事排在同一天走完"
        d["contingency"] = f"第 {index + 1} 天遇雨改走有顶的拱廊——今天没有任何预约会因此作废"
        d["route"]["route_logic"] = f"第 {index + 1} 天市场 15:00 收市而城堡不闭馆——所以先市场后城堡"
        d["route"]["fallback_plan"] = f"第 {index + 1} 天若电梯停运则改为海滩与长廊——都不依赖开门时间"
    expect_fail("every rationale built as fact-dash-significance", p, "one shape for everything")

    # And a plan that uses the dash sparingly is fine, or the rule would just ban a punctuation
    # mark rather than the habit.
    p = copy.deepcopy(base)
    day(p, 1)["focus"] = "市场开到 15:00，城堡冬季开到 18:00——两件事排在同一天"
    expect_ok("a dash used once, where it earns its place", p)

    # 42. The prose rule was built and measured on Chinese plans, so it recognised —— and the
    # typographic em dash and nothing else. An English plan written with the ASCII "--" or an en
    # dash escaped it entirely: the tell is the sentence shape and the shape does not change with
    # the codepoint.
    def every_field(text: str) -> dict:
        p = copy.deepcopy(base)
        for index, d in enumerate(p["days"]):
            d["focus"] = f"{text} ({index}a)"
            d["contingency"] = f"{text} ({index}b)"
            d["route"]["route_logic"] = f"{text} ({index}c)"
            d["route"]["fallback_plan"] = f"{text} ({index}d)"
        return p

    for label, text in (
            ("an ASCII double hyphen",
             "The market shuts at 15:00 and the castle at 18:00 -- both land on one day"),
            ("an en dash",
             "The market shuts at 15:00 and the castle at 18:00 – both land on one day")):
        expect_fail(f"one sentence shape built with {label}", every_field(text),
                    "one shape for everything")

    # And the narrowing that rule needed immediately: a dash BETWEEN DIGITS is a range, which is
    # correct typography rather than a sentence shape. Counting those fired on an opening-hours
    # line, which is precisely the false positive that gets a style rule routed around.
    for label, text in (
            ("opening hours", "Open 09:00–18:00 in winter and 09:00–20:00 in summer, shut Mondays"),
            ("a duration range", "Bus 20-35 minutes to the centre, runs 06:20-22:30, fare EUR 4.60"),
            ("hyphenated words", "The state-of-the-art lift is well-signposted and step-free")):
        expect_ok(f"a dash inside {label} is not a sentence shape", every_field(text))

    # 43. The repetition rule crashed instead of reporting. Its cross-scope comparison recovered
    # the day number by slicing the DISPLAY LABEL -- "day 3 focus".split()[1] -> "3" -- which held
    # only while every label began with "day <N> ". Anchor labels are "anchor[0].why_it_matters":
    # one token, no space, so the slice raised IndexError. check_prose_texture is in PLAN_CHECKS
    # and save_trip_deliverables.py runs PLAN_CHECKS, so a plan whose anchors shared a sentence
    # took down the only path that writes files a traveller keeps -- with a traceback, so the
    # operator saw a broken tool rather than a plan to fix. Every case below runs the checker
    # in-process: a raise here is a failed test, not a swallowed one.
    #
    # Two anchors are two DIFFERENT places, so one rationale copied onto both is false about at
    # least one of them. Same always-wrong shape as one sentence under two headings of a day card,
    # so it is an error rather than the note that cross-day repetition gets.
    p = copy.deepcopy(base)
    p["destination_experience_anchors"].append(
        copy.deepcopy(p["destination_experience_anchors"][0]))
    shared = "This is the one place the whole trip was planned around, and it earns the detour."
    p["destination_experience_anchors"][0]["why_it_matters"] = shared
    p["destination_experience_anchors"][1]["why_it_matters"] = shared
    expect_fail_naming("one rationale used for two different anchors", p,
                       ["anchor[1].why_it_matters", "repeats", "anchor[0].why_it_matters"])

    # An anchor rationale equal to a DAY field is the cross-scope case, and it must stay a note:
    # an anchor explaining why a place matters can honestly be the sentence that day's focus is
    # built from. It must also name both sides, or the operator cannot find the pair.
    p = copy.deepcopy(base)
    proto = p["destination_experience_anchors"][0]
    p["destination_experience_anchors"] = [
        {**copy.deepcopy(proto), "why_it_matters": text}
        for text in (day(p, 1)["focus"], day(p, 1)["contingency"],
                     day(p, 1)["route"]["route_logic"])]
    code, out = run(p)
    if code != 0:
        failures.append(f"anchor prose shared with a day must be a note, not an error\n{out}")
    if "word-for-word identical" not in out or "anchor[0].why_it_matters = day 1 focus" not in out:
        failures.append(f"the cross-scope note must name the anchor and the day field\n{out}")

    # The two day rules re-pinned against the new scope key, because the fix moved BOTH of them
    # onto it: disabling either one is now a one-line change that section 41 alone would not
    # localise to this comparison.
    p = copy.deepcopy(base)
    day(p, 1)["contingency"] = day(p, 1)["focus"]
    expect_fail("two headings of one day card printing one sentence", p, "repeats")

    p = copy.deepcopy(base)
    p["days"].append(copy.deepcopy(day(p, 1)))
    p["days"][1]["number"] = 2
    p["days"][1]["date"] = "2026-09-29"
    p["trip"]["end_date"] = "2026-09-29"
    code, out = run(p)
    if "repeats" in out:
        failures.append(f"prose shared across two days must stay a note\n{out}")

    # And the identity key itself. The scope used to be built from `number`, which is data and can
    # be missing or repeated: two days that both omit it folded into one scope called "dayNone",
    # so the always-wrong error fired on two fields sitting on two different cards. Position in
    # the list is the one thing about a day record that is always there and always unique.
    for label, first, second in (
            ("both missing their number", {"focus": shared}, {"focus": shared}),
            ("both numbered 1", {"number": 1, "focus": shared}, {"number": 1, "focus": shared})):
        p = copy.deepcopy(base)
        p["days"] = [first, second]
        code, out = run(p)
        if "repeats" in out:
            failures.append(f"two separate day cards {label} are not one card\n{out}")

    # The same rule on one malformed day must still fire, or the guard above has simply switched
    # the check off for every plan whose days are incomplete.
    p = copy.deepcopy(base)
    p["days"] = [{"focus": shared, "contingency": shared}]
    code, out = run(p)
    if "repeats" not in out:
        failures.append(f"one day card missing its number still prints one sentence twice\n{out}")

    failures += constraints_panel_cases(base)
    failures += untyped_constraints_cases(base)
    failures += untyped_marker_entry_cases(base)
    failures += dates_versus_the_gate_stamp_cases(base)
    failures += preferences_from_the_intake_cases(base)
    failures += verification_tier_note_cases(base)
    failures += cli_contract_cases(base)
    failures += dedupe_cases(base)
    failures += rule_split_cases()
    failures += pointer_cases(base)
    failures += json_output_cases(base)

    import render_final_trip_html as _renderer
    check_a_flight_number_may_be_unresearched_but_never_invented(
        _renderer.itinerary_findings, failures)
    check_per_weekday_hours_are_used_when_present(CHECKER_MODULE.check_dining, failures)
    check_a_review_score_is_not_cited_to_a_price_search(
        CHECKER_MODULE.check_booking_identity, failures)
    check_a_verified_score_owes_an_availability_from_the_same_visit(
        CHECKER_MODULE.check_booking_identity, failures)

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all plan-consistency regression cases passed")
    return 0


def test_plan_consistency_regressions() -> None:
    """Pytest surface: with no test_* function pytest collects nothing from this file and prints
    "no tests ran", which a contributor or CI reads as green -- the same class of false green the
    cases above exist to stop. Running the file directly is unchanged."""
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
