#!/usr/bin/env python3
"""Regression tests for scripts/plan_flags.py and the validator CLI that consumes it.

A Construction run used to require twelve conditional flag decisions, seven of which silently
disarmed a real check when answered wrong -- and every one of those seven was already computed
from the plan, twenty lines away, in save_trip_deliverables.py. `validate_trip_html.py page.html`
printed "VALID: booking-ready HTML structure passed." and exited 0 with the day-count check, the
booking-type check, the car-link rule and the traveller-facing "not fact-checked" banner check all
off at once. Measured on the fixture page with the banner section deleted, the pre-change script
printed VALID and exited 0.

Three of the seven derived from JSON keys SKILL.md never names (trip.arrival_transport_mode,
booking_options.attraction_tickets, booking_options.ground_transport), and the banner flag was
named in no .md file in the repository at all, so arming it required reading the argparse block.

So this file tests three separate things, because they fail separately:

  1. the derivation is correct and is ONE definition -- not a second copy that drifts, which is
     what the old comment "the same list, kept in step by hand in three files" was describing;
  2. it refuses loudly on every malformed shape, rather than substituting a default -- a deriver
     that quietly returns "nothing is required" rebuilds the exact defect it replaced;
  3. the CLI cannot be run with the checks silently off, and cannot be run with a plan AND a
     contradicting hand-typed answer.

Run:  python tests/test_plan_flags.py
      python -m pytest tests/test_plan_flags.py
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from plan_flags import ALLOWED_TRANSPORT_MODES, PlanFlagsError, derive_html_flags  # noqa: E402
from validate_trip_html import validate  # noqa: E402

VALIDATOR = SCRIPTS / "validate_trip_html.py"
FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"


def plan(**overrides) -> dict:
    """A minimal plan carrying only the keys the deriver reads.

    Deliberately not the booking-ready fixture: this is about which keys decide which flag, and a
    150-key fixture makes a case that turns on one of them unreadable. The fixture is used in the
    end-to-end cases below, where the whole document has to be real.
    """
    doc = {
        # trip.title is here because --plan binds the page to the plan through it: the renderer
        # prints it as the page's only <h1>, and without that pairing check the validator happily
        # checked one trip's page against another trip's plan.
        "trip": {"arrival_transport_mode": "rail", "title": "Flag derivation fixture"},
        "days": [{"day": 1}],
        "transport_preference": {"mode": "public-transit"},
    }
    doc.update(overrides)
    # A `trip=` override replaces the whole block, so every case that overrides it to say something
    # about the arrival mode would also be silently dropping the title and then refusing for a
    # reason it was not testing. The title is filled in unless the caller named it, so each case
    # keeps testing its own subject; the cases that are about the title pass it explicitly, and
    # `title=None` is how they say "absent".
    trip = doc.get("trip")
    if isinstance(trip, dict) and "title" not in trip:
        trip["title"] = "Flag derivation fixture"
    if isinstance(trip, dict) and trip.get("title") is None and "title" in trip:
        trip.pop("title")
    return doc


def flags_of(**overrides):
    return derive_html_flags(plan(**overrides))


def refusal(label: str, failures: list[str], **overrides) -> str:
    """Assert derive_html_flags refuses, and return the message so its wording can be checked.

    The message is checked, not just the exception type. A refusal that does not name the key it
    read is a refusal the operator answers by guessing, and this whole change is about replacing
    guesses with derivations.
    """
    try:
        derive_html_flags(plan(**overrides), plan_label="plan.json")
    except PlanFlagsError as exc:
        return str(exc)
    except Exception as exc:  # noqa: BLE001 - the distinction is the point
        # A bare traceback is technically loud, but it stops the whole file at the first bad
        # shape and reports one line about 'list' object has no attribute 'get'. Reverting the
        # booking_options guard during a mutation probe did exactly that: the run died at case 8
        # and the remaining forty cases never executed, so a real regression could have hidden
        # behind the crash. Refusing must mean PlanFlagsError specifically.
        failures.append(
            f"{label}: raised {type(exc).__name__} instead of PlanFlagsError ({exc}). A malformed "
            f"plan has to refuse through the documented exception, not crash the caller.")
        return ""
    failures.append(f"{label}: derive_html_flags returned instead of refusing")
    return ""


def run_cli(*args: str) -> tuple[int, str]:
    result = subprocess.run([sys.executable, str(VALIDATOR), *args],
                            capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr


def rendered_page(tmp: Path) -> tuple[Path, Path]:
    """Save the fixture through the real delivery path and return (page, saved plan).

    Rendering through save_trip_deliverables.py rather than hand-building a page is the point:
    these cases are about a page that really came off the delivery path, stamp and all, so the
    stripped-stamp case below has something real to strip.
    """
    workspace = tmp / "ws"
    plan_path = tmp / "plan.json"
    plan_path.write_text(FIXTURE.read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "save_trip_deliverables.py"), str(plan_path),
         "--workspace", str(workspace), "--unverified", "--slug", "flagcase"],
        capture_output=True, text=True)
    if result.returncode != 0:
        raise AssertionError(f"fixture save failed: {result.stdout + result.stderr}")
    page = next((workspace / "html").glob("*.html"))
    saved = next((workspace / "plans").glob("*.json"))
    return page, saved


def main() -> int:
    failures: list[str] = []

    def check(label: str, condition: bool, detail: str = "") -> None:
        if not condition:
            failures.append(f"{label}{': ' + detail if detail else ''}")

    # --- 1. the derivation ------------------------------------------------------------
    # Each flag against the key that decides it, including the values a real workspace never
    # produced. Measured across the 15 plans in a real workspace, transport mode was
    # public-transit on all 15 and ground_transport was absent on all 15 -- so self-drive and
    # ground have no coverage from real data at all and would otherwise be tested by nobody.
    check("hotel is required of every trip", flags_of().required_booking_types == frozenset({"hotel"}))
    check("arrival by flight requires a flight link",
          flags_of(trip={"arrival_transport_mode": "flight"}).required_booking_types
          == frozenset({"hotel", "flight"}))
    check("arrival by rail requires no flight link",
          "flight" not in flags_of(trip={"arrival_transport_mode": "rail"}).required_booking_types)
    # This case used to assert the defect. A missing arrival mode "requires no flight link" is the
    # same answer a rail trip gives, so a flight plan whose mode was blank, "air" or "Flight"
    # derived `hotel` alone, the flight-link check never ran, and the page passed carrying no
    # flight card -- the largest purchase on the trip, unchecked, on a green gate. Every spelling
    # outside the enum is now a refusal naming the legal values.
    for wrong in ({}, {"arrival_transport_mode": None}, {"arrival_transport_mode": ""},
                  {"arrival_transport_mode": "air"}, {"arrival_transport_mode": "Flight"},
                  {"arrival_transport_mode": " flight"}, {"arrival_transport_mode": 0},
                  {"arrival_transport_mode": ["flight"]}):
        message = refusal(f"arrival mode {wrong!r}", failures, trip=wrong)
        if message and "arrival_transport_mode" not in message:
            failures.append(
                f"arrival mode {wrong!r} was refused without naming the field, so the operator "
                f"cannot tell which key to fix: {message}")
    for legal in ("rail", "road", "other"):
        check(f"arrival by {legal} requires no flight link",
              "flight" not in flags_of(trip={"arrival_transport_mode": legal})
              .required_booking_types)

    # Truthiness, not presence -- and this is the asymmetry worth pinning. An empty list means the
    # plan researched no ticketed attraction, and requiring a ticket link for it would fail every
    # museum-free trip; a non-empty list means the page owes a button.
    check("attraction_tickets present requires a ticket link",
          "ticket" in flags_of(booking_options={"attraction_tickets": [{"id": "a"}]}).required_booking_types)
    check("attraction_tickets empty requires no ticket link",
          "ticket" not in flags_of(booking_options={"attraction_tickets": []}).required_booking_types)
    check("ground_transport present requires a ground link",
          "ground" in flags_of(booking_options={"ground_transport": [{"id": "g"}]}).required_booking_types)
    check("ground_transport empty requires no ground link",
          "ground" not in flags_of(booking_options={"ground_transport": []}).required_booking_types)
    check("several categories at once all apply",
          flags_of(trip={"arrival_transport_mode": "flight"},
                   booking_options={"attraction_tickets": [1], "ground_transport": [1, 2]}
                   ).required_booking_types == frozenset({"hotel", "flight", "ticket", "ground"}))

    check("day count is the length of days", flags_of(days=[{}, {}, {}, {}]).expected_days == 4)
    check("a one-day trip derives 1", flags_of(days=[{}]).expected_days == 1)

    for mode in ALLOWED_TRANSPORT_MODES:
        check(f"transport mode {mode} passes through",
              flags_of(transport_preference={"mode": mode}).transport_mode == mode)

    # The banner falls toward showing the warning for everything that is not exactly "verified",
    # because the failure it guards is a page silent about never having been fact-checked. On the
    # 15 real plans, 8 carry no verification_status key at all and 9 require the banner.
    check("verified needs no banner",
          flags_of(verification_status="verified").require_unverified_banner is False)
    check("unverified needs the banner",
          flags_of(verification_status="unverified").require_unverified_banner is True)
    check("a missing status needs the banner", flags_of().require_unverified_banner is True)
    check("a null status needs the banner",
          flags_of(verification_status=None).require_unverified_banner is True)
    for wrong in ("Verified", "verifed", " verified", True, 1, ""):
        check(f"status {wrong!r} needs the banner",
              flags_of(verification_status=wrong).require_unverified_banner is True)

    # No gate-stamp assertion: the field was removed. A stamp read out of the plan's own
    # `gates_passed` key cannot prove the plan passed anything, so requiring it refused every
    # legitimate render while certifying a hand-typed forgery. See validate_trip_html.py.
    check("the gate stamp is not a derived setting", not hasattr(flags_of(), "require_gate_stamp"))

    # Non-Latin values must not change any of this. The workspace is majority Chinese, and a
    # deriver that only holds for ASCII would fail on the trips this skill actually plans.
    cjk = flags_of(trip={"arrival_transport_mode": "flight", "title": "北京三日中轴线胡同与故宫"},
                   booking_options={"attraction_tickets": [{"provider": "故宫博物院官方订票"}]},
                   verification_status="未核验")
    check("CJK plan derives the same flags",
          cjk.required_booking_types == frozenset({"hotel", "flight", "ticket"})
          and cjk.require_unverified_banner is True)

    # --- 2. loud refusals -------------------------------------------------------------
    # Every one of these used to be either a stack trace or, worse, a plausible default.
    msg = refusal("empty days", failures, days=[])
    check("empty days refusal names days", "days" in msg, msg)
    check("empty days refusal says the length", "length 0" in msg, msg)

    # An absent key and an explicit null are different mistakes with different fixes -- one field
    # was never filled in, the other was blanked -- and both used to read as "got NoneType".
    absent = dict(plan())
    absent.pop("days")
    try:
        derive_html_flags(absent, plan_label="plan.json")
        failures.append("missing days: derive_html_flags returned instead of refusing")
    except PlanFlagsError as exc:
        check("a missing key is named as missing, not as null", "no such key" in str(exc), str(exc))
    check("an explicit null is named as null",
          "NoneType" in refusal("null days", failures, days=None))

    for label, kwargs in [
        ("days not a list", {"days": {"1": {}}}),
        ("null mode", {"transport_preference": {"mode": None}}),
        ("missing transport_preference", {"transport_preference": None}),
        ("transport_preference not an object", {"transport_preference": []}),
        ("trip not an object", {"trip": []}),
        ("booking_options is a list", {"booking_options": []}),
        ("booking_options is a string", {"booking_options": "none"}),
    ]:
        refusal(label, failures, **kwargs)

    # The mode enum is the subtle one. validate_trip_html keys BOTH car rules on equality with
    # these two strings, so an unrecognised mode does not select a different rule -- it turns both
    # off silently, which is the same shape as the opt-in defaults this change removes.
    for bad_mode in ("mixed", "rail", "", "self drive", "混合", "SELF-DRIVE"):
        message = refusal(f"mode {bad_mode!r}", failures,
                          transport_preference={"mode": bad_mode})
        check(f"mode {bad_mode!r} refusal names the mode", "transport_preference.mode" in message,
              message)

    # booking_options is the one key legitimately allowed to be absent, and absent must mean
    # absent -- not "any falsy value". `plan.get("booking_options") or {}` passed an empty LIST
    # through as "this trip books nothing", turning a type error into two disarmed checks.
    # The trip block carries a real arrival mode because this case is about booking_options, and a
    # plan built with an empty trip now refuses on the arrival enum instead -- which would make the
    # case pass or fail for a reason that has nothing to do with its subject.
    check("absent booking_options is allowed",
          derive_html_flags({"trip": {"arrival_transport_mode": "road", "title": "T"},
                             "days": [{}],
                             "transport_preference": {"mode": "self-drive"}}
                            ).required_booking_types == frozenset({"hotel"}))
    check("null booking_options is allowed",
          flags_of(booking_options=None).required_booking_types == frozenset({"hotel"}))

    for bad_plan, label in [(None, "null plan"), ([], "list plan"), ("{}", "string plan"), (7, "int plan")]:
        try:
            derive_html_flags(bad_plan, plan_label="plan.json")
            failures.append(f"{label}: derive_html_flags returned instead of refusing")
        except PlanFlagsError:
            pass

    # --- 3. the CLI cannot run with the checks silently off ---------------------------
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        page, saved_plan = rendered_page(tmp)

        code, out = run_cli(str(page))
        check("bare invocation is refused", code == 1, f"exit {code}: {out}")
        check("bare refusal names --plan first", "No --plan" in out, out)
        for expected in ("--expected-days", "--require-booking-type", "--transport-mode",
                         "--require-unverified-banner"):
            check(f"bare refusal names {expected}", expected in out, out)

        code, out = run_cli(str(page), "--plan", str(saved_plan))
        check("--plan alone validates a real delivery", code == 0, f"exit {code}: {out}")
        check("--plan prints the armed set", "derived from plan:" in out, out)

        # A hand-typed answer beside the plan is two answers to one question, and the wrong one
        # wins silently: --expected-days 9 against a 1-day plan checks the page against a trip
        # that does not exist.
        code, out = run_cli(str(page), "--plan", str(saved_plan), "--expected-days", "9")
        check("--plan plus a manual flag is refused", code == 1, f"exit {code}: {out}")
        check("conflict names the offending flag", "--expected-days" in out, out)

        # Every manual invocation still works when every setting is supplied.
        code, out = run_cli(str(page), "--expected-days", "1", "--require-booking-type", "hotel",
                            "--transport-mode", "public-transit", "--require-unverified-banner")
        check("full manual invocation still validates", code == 0, f"exit {code}: {out}")

        code, out = run_cli(str(page), "--expected-days", "1", "--no-booking-types",
                            "--transport-mode", "public-transit", "--require-unverified-banner")
        check("--no-booking-types is accepted", code == 0, f"exit {code}: {out}")

        code, out = run_cli(str(page), "--expected-days", "1", "--no-booking-types",
                            "--require-booking-type", "hotel",
                            "--transport-mode", "public-transit", "--require-unverified-banner")
        check("--no-booking-types contradicting a required type is refused", code == 2,
              f"exit {code}: {out}")

        # The escape hatch must announce itself. It switches off a traveller-facing warning on a
        # claim nothing checked, so a silent success here would be the original defect wearing a
        # longer flag name.
        bannerless = tmp / "no-banner.html"
        source = page.read_text(encoding="utf-8")
        import re  # noqa: PLC0415 - only this case needs it
        stripped = re.sub(r'<section id="verification-notice".*?</section>', "", source, flags=re.DOTALL)
        check("fixture page carries a banner to strip", stripped != source)
        bannerless.write_text(stripped, encoding="utf-8")

        code, out = run_cli(str(bannerless), "--plan", str(saved_plan))
        check("a delivery missing the banner is refused under --plan", code == 1, f"exit {code}: {out}")
        check("banner refusal explains the traveller cost", "not fact-checked" in out, out)

        code, out = run_cli(str(bannerless), "--expected-days", "1", "--no-booking-types",
                            "--transport-mode", "public-transit", "--assert-verified-without-plan")
        check("the escape hatch runs", code == 0, f"exit {code}: {out}")
        check("the escape hatch says the status was asserted, not read",
              "ASSERTED, NOT READ" in out, out)

        code, out = run_cli(str(bannerless), "--expected-days", "1", "--no-booking-types",
                            "--transport-mode", "public-transit", "--require-unverified-banner",
                            "--assert-verified-without-plan")
        check("asserting verified while requiring the banner is refused", code == 2,
              f"exit {code}: {out}")

        # --- the gate stamp stays a NOTE, with or without --plan --------------------------
        # It was briefly promoted to an error under --plan, on the argument that a hand-assembled
        # page -- the one thing SKILL.md forbids outright -- otherwise printed VALID and exited 0
        # on the only gate that could ever have seen it. That argument was wrong twice over, and
        # this case pins the reverted behaviour so it is not "fixed" again.
        #
        # It refused legitimate work: render_final_trip_html.py, this repository's own renderer and
        # the command SKILL.md says to iterate with, emits no stamp -- so the documented
        # pre-delivery loop failed on its own output, and all fifteen delivered pages in a real
        # workspace failed on a stamp that postdates them.
        #
        # And it certified the forgery it was aimed at. The stamp is rendered out of
        # `plan["gates_passed"]["checks"]`, a key an author types: a hand-written plan carrying
        # `"gates_passed": {"checks": 24}` renders stamped, so the check waved through exactly the
        # page it existed to catch while stopping every honest one. The assertion below is the
        # forgery, run for real.
        handwritten = tmp / "hand-written.html"
        no_stamp = re.sub(r'<p class="meta" data-gates-checks=.*?</p>', "", source, flags=re.DOTALL)
        check("fixture page carries a gate stamp to strip",
              no_stamp != source and "data-gates-checks" not in no_stamp)
        handwritten.write_text(no_stamp, encoding="utf-8")

        code, out = run_cli(str(handwritten), "--plan", str(saved_plan))
        check("an unstamped page is noted, not refused, under --plan", code == 0,
              f"exit {code}: {out}")
        check("the note survives under --plan", "carries no gate stamp" in out, out)

        code, out = run_cli(str(handwritten), "--expected-days", "1", "--no-booking-types",
                            "--transport-mode", "public-transit", "--require-unverified-banner")
        check("an unstamped draft render is still only noted", code == 0, f"exit {code}: {out}")
        check("the draft note survives", "carries no gate stamp" in out, out)

        # The forgery, so the reason for the revert is a fact in the suite rather than a comment:
        # a stamp typed into the plan renders a stamped page, so requiring the stamp would have
        # passed this and failed the honest unstamped render above.
        forged_plan = tmp / "forged.json"
        forged = json.loads(FIXTURE.read_text(encoding="utf-8"))
        forged["gates_passed"] = {"checks": 24, "checked_by": "typed by hand"}
        forged_plan.write_text(json.dumps(forged, ensure_ascii=False), encoding="utf-8")
        forged_page = tmp / "forged.html"
        rendered = subprocess.run(
            [sys.executable, str(SCRIPTS / "render_final_trip_html.py"), str(forged_plan),
             str(forged_page)], capture_output=True, text=True)
        check("a typed gates_passed renders a stamped page", rendered.returncode == 0
              and "data-gates-checks" in forged_page.read_text(encoding="utf-8"),
              f"exit {rendered.returncode}: {rendered.stdout}{rendered.stderr}")

        # --- --plan must be holding the right plan ----------------------------------------
        # `validate_trip_html.py tripA.html --plan tripB.json` printed VALID: it checked the page
        # against another trip's day count, booking types, transport mode and verification status,
        # and printed "derived from plan: ..." as though the pairing had been established. Two
        # trips open at once, or one stale path in a wrapper, is the whole setup. A flag whose
        # purpose is "derive the truth from the plan" has to establish it is holding the right one.
        code, out = run_cli(str(page), "--plan", str(saved_plan))
        check("the real pairing still validates", code == 0, f"exit {code}: {out}")

        other = tmp / "other-trip.json"
        other_doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
        other_doc["trip"]["title"] = "Completely Different Trip"
        other.write_text(json.dumps(other_doc, ensure_ascii=False), encoding="utf-8")
        code, out = run_cli(str(page), "--plan", str(other))
        check("a page validated against another trip's plan is refused", code == 2,
              f"exit {code}: {out}")
        check("the refusal names both titles",
              "Completely Different Trip" in out and "Renderer quality-gate fixture" in out, out)

        # The title reaches the page through the renderer's HTML escaper, so a raw byte comparison
        # would call a correctly paired plan and page two different trips the moment a title
        # contains an apostrophe or an ampersand. And the workspace this skill actually plans for
        # is majority CJK, so a binding that only held for ASCII would hold for almost none of it.
        for label, title in (("an apostrophe", "Paul's Coffee & Cake tour"),
                             ("CJK", "北京三日 · 中轴线胡同与故宫"),
                             ("a quoted phrase", 'The "old town" walk')):
            tricky_plan = tmp / f"tricky-{label.replace(' ', '-')}.json"
            doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
            doc["trip"]["title"] = title
            tricky_plan.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
            tricky_page = tmp / f"tricky-{label.replace(' ', '-')}.html"
            r = subprocess.run(
                [sys.executable, str(SCRIPTS / "render_final_trip_html.py"), str(tricky_plan),
                 str(tricky_page)], capture_output=True, text=True)
            if r.returncode != 0:
                failures.append(f"render failed for a title with {label}: {r.stdout}{r.stderr}")
                continue
            code, out = run_cli(str(tricky_page), "--plan", str(tricky_plan))
            check(f"a title with {label} binds to its own page", "different trips" not in out, out)

        # A page with no <h1> cannot be identified at all, and saying so is different from saying
        # the trips disagree -- the operator's next move is different for each.
        headless = tmp / "headless.html"
        headless.write_text(re.sub(r"<h1[^>]*>.*?</h1>", "", source, flags=re.DOTALL),
                            encoding="utf-8")
        code, out = run_cli(str(headless), "--plan", str(saved_plan))
        check("a page with no <h1> is refused under --plan", code == 2, f"exit {code}: {out}")
        check("the no-<h1> refusal is not reported as a title mismatch",
              "different trips" not in out, out)

    # The note must stay a note at the function level too, for every existing caller that passes
    # no plan. This is the pre-change default, and it is the regression floor: 15 workspace pages
    # produced byte-identical findings across this change at exactly these arguments.
    notes: list[str] = []
    errors = validate("<html lang='en'></html>", None, set(), None, notes)
    check("no gate stamp is a note by default", any("carries no gate stamp" in n for n in notes),
          str(notes))
    check("no gate stamp is not an error by default",
          not any("data-gates-checks" in e for e in errors), str(errors))

    # --- 4. one definition, not two ---------------------------------------------------
    # The failure this guards against is not a wrong answer, it is a right answer that drifts.
    # save_trip_deliverables.py's own comment called the booking-type list "the same list, kept in
    # step by hand in three files"; a future edit that re-inlines it would pass every case above.
    save_source = (SCRIPTS / "save_trip_deliverables.py").read_text(encoding="utf-8")
    validator_source = (SCRIPTS / "validate_trip_html.py").read_text(encoding="utf-8")
    check("save_trip_deliverables imports the shared deriver",
          "from plan_flags import" in save_source)
    check("validate_trip_html imports the shared deriver",
          "from plan_flags import" in validator_source)
    for key in ("arrival_transport_mode", "attraction_tickets", "ground_transport"):
        check(f"{key} is read in one place only",
              key not in save_source and key not in validator_source,
              f"{key} is still derived outside plan_flags.py")

    # The reason plan_flags.py is its own module rather than a helper in either caller. Importing
    # the validator on its own must not touch save_trip_deliverables; if the deriver ever moves
    # into save_trip_deliverables, this import becomes a cycle and fails here rather than in
    # whatever run happened to hit it first.
    probe = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, %r); import validate_trip_html; "
         "assert 'save_trip_deliverables' not in sys.modules, 'import cycle'; print('ok')"
         % str(SCRIPTS)],
        capture_output=True, text=True)
    check("importing the validator alone stays cycle-free", probe.returncode == 0,
          probe.stdout + probe.stderr)

    if failures:
        print(f"FAIL ({len(failures)}):")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("OK: gate settings derive from the plan, refuse loudly, and cannot be silently disarmed.")
    return 0


def test_plan_flags() -> None:
    """Pytest surface: with no test_* function pytest collects nothing from this file and prints
    "no tests ran", which a contributor or CI reads as green. Running the file directly is
    unchanged."""
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
