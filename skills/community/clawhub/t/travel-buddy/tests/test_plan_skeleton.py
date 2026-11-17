#!/usr/bin/env python3
"""Regression tests for scripts/new_plan_skeleton.py.

The skeleton earns its place only if it renders on the first try. On the run that motivated it,
the first render of a hand-built plan returned 21 errors and every one was structural — segments
not mirroring stops_in_order by exact string equality, an empty service_or_line on a walking leg,
booking-access categories spelled with the budget enum's words, a departure day with no
breakfast, two flight candidates sharing a review_url. Three edit-render round-trips went into
rediscovering rules a generator can simply obey.

So these tests assert two properties that must both hold, because either one alone is a trap:

  1. the skeleton renders clean, across languages, trip lengths and stop counts; and
  2. the rendered page is still rejected while unfilled, so a faster start never becomes a way
     to ship a hollow itinerary.

Run:  python tests/test_plan_skeleton.py
      python -m pytest tests/test_plan_skeleton.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def generate(tmp: Path, name: str, *args: str) -> Path:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "new_plan_skeleton.py"), *args],
        capture_output=True, text=True)
    if result.returncode != 0:
        raise AssertionError(f"skeleton generation failed: {result.stderr}")
    path = tmp / name
    path.write_text(result.stdout, encoding="utf-8")
    return path


def size_limit_cases(failures: list[str]) -> None:
    """A skeleton nobody can fill is not a favour.

    `--start 2027-03-01 --end 2027-05-30 --stops-per-day 12` used to emit 91 days, 181 dining cards,
    1001 route segments and 1.4 MB, exit 0, silently -- and every value in it is a TODO the page
    validator refuses to ship, so the operator had to research all of it before anything rendered.
    The verification pass then scales with the number of claims rather than the number of nights, so
    the real cost lands later and larger than anyone expects at the prompt. These cases pin the four
    behaviours: quiet when normal, a note when large, a refusal past the limit that says what it
    would cost, and --oversize for the author who means it."""
    base = ["--origin", "a", "--destination", "b"]

    def run_size(args: list[str]) -> tuple[int, str]:
        proc = subprocess.run([sys.executable, str(SCRIPTS / "new_plan_skeleton.py"), *base, *args],
                              capture_output=True, text=True)
        # The subject of these cases is the SIZE warning, not an empty stderr. The skeleton writes
        # the plan to stdout, so everything else it has to say -- the next command in the chain,
        # the untyped-constraint markers -- necessarily goes to stderr, and asserting silence there
        # made this fail the moment the pipeline started naming its own next step.
        noise = "\n".join(line for line in proc.stderr.splitlines()
                          if not line.startswith("NEXT:"))
        return proc.returncode, noise

    code, err = run_size(["--start", "2027-03-01", "--end", "2027-03-04", "--stops-per-day", "3"])
    if code != 0 or err.strip():
        failures.append(f"size: an ordinary 4-day plan must raise no size warning, got exit "
                        f"{code} / {err[:120]!r}")

    code, err = run_size(["--start", "2027-03-01", "--end", "2027-03-10", "--stops-per-day", "3"])
    if code != 0 or "NOTE:" not in err:
        failures.append(f"size: a 10-day plan should warn but succeed, got exit {code} / {err[:120]!r}")

    code, err = run_size(["--start", "2027-03-01", "--end", "2027-05-30", "--stops-per-day", "12"])
    if code != 2 or "--oversize" not in err:
        failures.append(f"size: 91 days x 12 stops must be refused and name --oversize, got exit {code}")
    for token in ("dining cards", "route segments"):
        if code == 2 and token not in err:
            failures.append(f"size: the refusal must say what it would cost -- no {token!r} in the message")

    code, err = run_size(["--start", "2027-03-01", "--end", "2027-05-30",
                          "--stops-per-day", "12", "--oversize"])
    if code != 0 or "--oversize accepted" not in err:
        failures.append(f"size: --oversize must let it through and say so, got exit {code}")



def check_plan_language_follows_the_intake(failures: list[str]) -> None:
    """A plan for an English traveller started in Chinese.

    The intake records `preferred_output_language` (the profile's preference, else the language
    the form was submitted in) and `form_language`, and the skeleton defaulted to zh whatever they
    said -- the last place the traveller's language was collected and then dropped. Order: the
    command line, else the preference, else the form language, else zh; each outcome is printed
    like every other copied field, and the resolved language has to reach the plan's own text too
    (the walking legs), not only `trip.language`.
    """
    import json, subprocess, sys, tempfile
    base = json.loads((ROOT / "templates" / "trip-profile.json").read_text(encoding="utf-8"))
    base.update({"origin": {"home_city": "Leiden"},
                 "travel_window": {"start_date": "2027-04-17", "end_date": "2027-04-19"},
                 "party": {"traveler_count": 1}, "budget": {"currency": "EUR", "hard_cap_amount": 900},
                 "destination_scope": {"state": "fixed", "named_places": ["Porto"]}})
    old = {k: v for k, v in base.items() if k not in ("preferred_output_language", "form_language")}
    cases = [
        ("a preference in the traveller's own word", {**base, "preferred_output_language": "English", "form_language": "zh"},
         [], "en", "preferred_output_language -> trip.language: 'en'"),
        ("the code the server writes", {**base, "preferred_output_language": "en"}, [], "en",
         "preferred_output_language -> trip.language: 'en'"),
        ("no preference, the form language", {**base, "preferred_output_language": None, "form_language": "en"},
         [], "en", "form_language -> trip.language: 'en'"),
        ("an unreadable preference falls through, loudly", {**base, "preferred_output_language": "Klingon", "form_language": "en"},
         [], "en", "preferred_output_language -> trip.language: NOT copied"),
        ("the command line wins", {**base, "preferred_output_language": "en"}, ["--language", "zh"], "zh",
         "came from the command line and wins"),
        ("an intake from before the fields existed", old, [], "zh", "the intake records no language"),
    ]
    for label, intake, extra, expected, said in cases:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump(intake, handle, ensure_ascii=False)
            path = handle.name
        proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "new_plan_skeleton.py"),
                               "--from-intake", path, "--mode", "public-transit", "--stops-per-day", "3", *extra],
                              capture_output=True, text=True)
        if proc.returncode != 0:
            failures.append(f"plan language, {label}: the skeleton failed: {proc.stderr[-400:]}")
            continue
        plan = json.loads(proc.stdout)
        got = plan.get("trip", {}).get("language")
        if got != expected:
            failures.append(f"plan language, {label}: trip.language is {got!r}, expected {expected!r}")
        if said not in proc.stderr:
            failures.append(f"plan language, {label}: the report must say {said!r}; it said "
                            f"{[l for l in proc.stderr.splitlines() if 'language' in l]}")
        walking = [seg.get("mode") for day in plan.get("days", []) for seg in day.get("route", {}).get("segments", [])]
        if expected == "en" and any(mode == "步行" for mode in walking):
            failures.append(f"plan language, {label}: the plan should be English but its walking legs "
                            f"are 「步行」 -- the resolved language did not reach the rest of the plan")


def check_work_mode_question_when_the_destination_may_be_a_country(failures: list[str]) -> None:
    """A construction intake naming a whole country must be questioned, not silently built on.

    `destination_scope.state` used to offer "已固定城市/国家" as ONE option, which is two different
    answers: a settled city is Construction, a settled country is constrained discovery. A real run
    answered it with 「美国」, the form recorded mode=construction, and the next step would have been
    an eight-day itinerary for a country. The form's wording is fixed; this is the backstop for an
    intake filled in before that fix.

    Asserted on the QUESTION, not on country detection -- deciding whether a string names a country
    needs a list of every country in every language, and this repository has twice lost that bet
    (assistant names, tty detection). The author answers it in a second; no list can.
    """
    import json, subprocess, sys, tempfile
    base = {"mode": "construction", "intake_status": "complete",
            "travel_window": {"start_date": "2026-10-12", "end_date": "2026-10-15"},
            "origin": {"home_city": "Leiden", "country": "NL"},
            "party": {"traveler_count": 1},
            "budget": {"currency": "EUR", "hard_cap_amount": 1500},
            "destination_scope": {"state": "fixed", "named_places": ["美国"]}}

    def run(intake, extra=()):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False,
                                         encoding="utf-8") as handle:
            json.dump(intake, handle, ensure_ascii=False)
            path = handle.name
        proc = subprocess.run([sys.executable, str(ROOT / "scripts" / "new_plan_skeleton.py"),
                               "--from-intake", path, *extra],
                              capture_output=True, text=True)
        return proc.stderr

    asked = run(base)
    question = [line for line in asked.splitlines() if "CHECK THE WORK MODE" in line]
    if not question:
        failures.append("work mode: a construction intake copying its destination straight from "
                        "the intake must ask whether that destination is a city; it said nothing")
    # Scoped to the question's own line on purpose. Checking the whole of stderr for the
    # destination passes no matter what, because another report line always prints it -- which is
    # how the first version of this case survived a mutation that dropped {first!r} entirely.
    elif "美国" not in question[0]:
        failures.append(f"work mode: the question must quote the destination it is about, got "
                        f"{question[0]!r}")

    # An author who named the city on the command line has already decided; asking again is noise.
    overridden = run(base, ("--destination", "劳德代尔堡"))
    if "CHECK THE WORK MODE" in overridden:
        failures.append("work mode: --destination means the author already chose, so the question "
                        "must not fire")

    # Only an EXPLICIT discovery declaration silences it. `== "construction"` was the first
    # version and it missed "Construction" and every hand-written intake that omits the field --
    # and this script only ever emits a Construction artifact, so silence is a reason to ask.
    for mode in ("construction", "Construction", "CONSTRUCTION ", None, 7):
        quiet = {**base, "mode": mode} if mode is not None else {k: v for k, v in base.items()}
        if "CHECK THE WORK MODE" not in run(quiet):
            failures.append(f"work mode: mode={mode!r} must still be asked about -- an absent or "
                            f"differently-cased mode is not a claim that this is not Construction")
    for mode in ("discovery", "constrained_discovery", "Constrained_Discovery"):
        if "CHECK THE WORK MODE" in run({**base, "mode": mode}):
            failures.append(f"work mode: mode={mode!r} explicitly says discovery, so the question "
                            f"must not fire")


def main() -> int:
    failures: list[str] = []
    size_limit_cases(failures)

    shapes = [
        ("zh 4 days, 4 stops", ["--start", "2026-09-11", "--end", "2026-09-14",
                                "--origin", "阿姆斯特丹", "--destination", "马拉加",
                                "--language", "zh", "--stops-per-day", "4"]),
        ("en 3 days, 2 stops", ["--start", "2026-09-11", "--end", "2026-09-13",
                                "--origin", "Amsterdam", "--destination", "Malaga",
                                "--language", "en", "--stops-per-day", "2"]),
        ("zh 2 days, self-drive", ["--start", "2026-09-11", "--end", "2026-09-12",
                                   "--origin", "A", "--destination", "B",
                                   "--mode", "self-drive"]),
    ]

    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)
        for label, args in shapes:
            plan = generate(tmp, f"{abs(hash(label))}.json", *args)
            html = tmp / f"{abs(hash(label))}.html"

            render = subprocess.run(
                [sys.executable, str(SCRIPTS / "render_final_trip_html.py"), str(plan), str(html)],
                capture_output=True, text=True)
            if render.returncode != 0:
                failures.append(f"{label}: skeleton did not render first try\n{render.stdout}")
                continue

            # `--plan` rather than a hand-counted `--expected-days`, since the plan is right
            # there on disk. It used to read the day count out of the JSON and type it back in as
            # a flag, which is the same two-copies-of-one-fact shape that scripts/plan_flags.py
            # exists to remove -- and the other three settings that flag left unset were the ones
            # that defaulted to off. This also means the skeleton is now checked by the same
            # invocation a real delivery uses.
            validate = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_trip_html.py"), str(html),
                 "--plan", str(plan)],
                capture_output=True, text=True)
            output = validate.stdout + validate.stderr
            if validate.returncode == 0:
                failures.append(f"{label}: an unfilled skeleton must not pass the HTML gate")
            elif "template token or TODO" not in output:
                failures.append(
                    f"{label}: unfilled skeleton was rejected, but not for containing TODOs — "
                    f"it must fail on the placeholders, not on a structural defect:\n{output}")

            # The category enums must never reach visible prose on a non-English page.
            if "--language" in args and args[args.index("--language") + 1] == "zh":
                if "Renderer-owned text is still English" in output:
                    failures.append(f"{label}: skeleton leaks a renderer enum into Chinese prose\n{output}")

    # An English plan's skeleton is English. Its walking legs used to be written 「步行」 whatever the
    # language, and an English page then printed 「步行 · 步行（无线路）」 with both gates calling it
    # VALID (2026-09-24): the i18n gate looks for English on Chinese pages, never the reverse.
    with tempfile.TemporaryDirectory() as raw:
        english = generate(Path(raw), "english.json", "--start", "2026-09-11", "--end", "2026-09-13",
                           "--origin", "Amsterdam", "--destination", "Malaga", "--language", "en",
                           "--stops-per-day", "3")
        text = english.read_text(encoding="utf-8")
        cjk = sorted(set(re.findall(r"[\u3000-\u9fff\uff00-\uffef]+", text)))
        if cjk:
            failures.append(f"an English skeleton carries CJK text: {cjk[:8]}")
        modes = {segment.get("mode") for day in json.loads(text)["days"]
                 for segment in day["route"]["segments"]}
        if "walk" not in modes:
            failures.append(f"an English skeleton's walking legs are not 'walk': {sorted(map(str, modes))}")

    # The skeleton and the data contract have to agree on which fields exist, or a required one
    # is discovered by failing a gate at the end instead of by filling a blank at the start.
    # Three fields drifted exactly that way -- rating_below_floor_reason,
    # guest_rating_below_floor_reason and detour_reason were added to the template and to the
    # checker, and the skeleton went on emitting cards without them.
    import json as _json
    template = _json.loads((ROOT / "templates" / "final-trip-plan.json").read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as raw:
        probe = generate(Path(raw), "drift.json", "--start", "2027-03-05", "--end", "2027-03-08",
                         "--origin", "A", "--destination", "B", "--language", "en",
                         "--currency", "EUR", "--travellers", "1", "--mode", "public-transit",
                         "--stops-per-day", "2")
        skeleton = _json.loads(probe.read_text(encoding="utf-8"))

    def compare(label: str, want: dict, got: dict) -> None:
        missing = sorted(k for k in want if k not in got)
        if missing:
            failures.append(f"skeleton {label} is missing template field(s): {missing}")

    # The two constraints the walking and dining gates MEASURE must leave this script marked as
    # untyped, not answered. They used to be emitted as `allergy_severity: "none"` and
    # `max_continuous_walking_minutes: null` -- values a reader cannot tell from a traveller's
    # answer -- for two fields the skeleton cannot know, because the intake collects both as prose
    # and nothing turns a sentence into an enum or a number. Measured on a real five-day plan with
    # those defaults untouched, deleting every activity's on_foot_minutes changed the finding count
    # from 2 to 2; with the cap typed as 25 the same deletion produced five precise findings. And
    # SKILL.md's light verification tier is allowed only when the severity is none/preference AND
    # the cap is null, so the untouched defaults also bought the cheaper pass.
    #
    # The marker's KEY is imported from the checker rather than spelled here, because that is the
    # failure this case exists to catch: a skeleton writing `untyped_constraints` while the gate
    # reads `untyped_constraint` keeps every test in the suite green and never fires on a plan.
    sys.path.insert(0, str(SCRIPTS))
    from check_plan_consistency import (  # noqa: PLC0415 - import after path setup
        UNTYPED_CONSTRAINTS_MARKER, check_untyped_constraints)

    emitted = skeleton["trip"]["traveler_constraints"]
    if emitted.get("allergy_severity") is not None:
        failures.append(
            f"skeleton emits allergy_severity={emitted.get('allergy_severity')!r}, which reads as "
            f"the traveller's answer. It cannot know this field; it must leave it unset.")
    if emitted.get("max_continuous_walking_minutes") is not None:
        failures.append(
            f"skeleton emits max_continuous_walking_minutes="
            f"{emitted.get('max_continuous_walking_minutes')!r} rather than leaving it unset.")
    unset = emitted.get(UNTYPED_CONSTRAINTS_MARKER)
    if not isinstance(unset, dict):
        failures.append(
            f"skeleton emits no {UNTYPED_CONSTRAINTS_MARKER} marker "
            f"(found {unset!r}); nothing distinguishes 'nobody typed it' from 'genuinely none'")
    else:
        for field in ("allergy_severity", "max_continuous_walking_minutes"):
            if field not in unset:
                failures.append(f"{UNTYPED_CONSTRAINTS_MARKER} does not name {field}")
            elif "TODO:" not in str(unset[field]):
                failures.append(
                    f"{UNTYPED_CONSTRAINTS_MARKER}[{field!r}] carries no TODO marker, so it does "
                    f"not read as unfilled the way every other blank in this skeleton does")
    # And the gate that reads the marker must actually fire on the skeleton's own output -- the
    # one assertion a matching key name still cannot make on its own.
    found: list[str] = []
    check_untyped_constraints(skeleton, found, [])
    if len(found) != 2:
        failures.append(
            f"check_untyped_constraints reports {len(found)} finding(s) on a fresh skeleton, "
            f"expected one per untyped constraint: {found}")

    compare("trip", template["trip"], skeleton["trip"])
    compare("days[].dining[]", template["days"][0]["dining"][0], skeleton["days"][0]["dining"][0])
    compare("days[].route.segments[]", template["days"][0]["route"]["segments"][0],
            skeleton["days"][0]["route"]["segments"][0])
    compare("booking_options.accommodations[]",
            template["booking_options"]["accommodations"][0],
            skeleton["booking_options"]["accommodations"][0])

    # The third of the three disqualifiers references/research-budget.md rule 1 says to settle
    # before any research at all. The intake now collects it, and an author who never opens the
    # intake file would still ask the traveller a question they have already answered -- so the
    # skeleton says it out loud, including when an older intake file does not carry the field.
    import subprocess as _sp, sys as _sys, tempfile as _tf, os as _os
    _base = json.loads((ROOT / "templates" / "trip-profile.json").read_text(encoding="utf-8"))
    _base["origin"] = {"home_city": "阿姆斯特丹"}
    _base["travel_window"] = {"start_date": "2027-04-17", "end_date": "2027-04-23"}
    _base["party"] = {"traveler_count": 2}
    _base["budget"] = {"currency": "EUR", "hard_cap_amount": 1200}
    _base["destination_scope"] = {"state": "fixed", "named_places": ["香港"]}
    with _tf.TemporaryDirectory() as _raw:
        for _label, _bk, _want in (
                ("something booked", {"state": "transport", "details": "CX270 不可退"}, "CX270"),
                ("nothing booked", {"state": "nothing", "details": None}, "still open"),
                ("an intake predating the field", None, "does not say")):
            _body = dict(_base)
            if _bk is None:
                _body.pop("existing_bookings", None)
            else:
                _body["existing_bookings"] = _bk
            _path = _os.path.join(_raw, "intake.json")
            Path(_path).write_text(json.dumps(_body, ensure_ascii=False), encoding="utf-8")
            _proc = _sp.run([_sys.executable, str(ROOT / "scripts" / "new_plan_skeleton.py"),
                             "--from-intake", _path, "--destination", "香港", "--language", "zh",
                             "--mode", "public-transit", "--stops-per-day", "3"],
                            capture_output=True, text=True)
            if "ALREADY BOOKED" not in _proc.stderr:
                failures.append(f"booking state: nothing printed for {_label}")
            elif _want not in _proc.stderr:
                failures.append(f"booking state: {_label} did not say {_want!r}")

    check_work_mode_question_when_the_destination_may_be_a_country(failures)
    check_plan_language_follows_the_intake(failures)

    if failures:
        print("FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("OK: skeleton renders first try in every shape, and stays unshippable until filled.")
    return 0


def test_plan_skeleton_renders_and_stays_unshippable() -> None:
    """Pytest surface: with no test_* function pytest collects nothing from this file and prints
    "no tests ran", which a contributor or CI reads as green. Running the file directly is
    unchanged."""
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
