#!/usr/bin/env python3
"""The four questions a traveller has walking out of an arrivals hall.

Every other block in a plan is about the days. None of them answered: can I pay, can I get online,
who do I call, am I insured. A page that schedules six days of meals and cannot say whether the
card in the traveller's pocket will work at the first ticket machine has answered the easy half.

The reason this is a *gate* and not a paragraph asking nicely is that these are precisely the facts
that get recalled instead of checked, and recalled wrongly. The case that started it, from a real
plan in the workspace: a Chinese passport holder resident in the Netherlands, flying to Switzerland.
A Dutch EHIC works across the EU. In Switzerland it is worthless to them -- the EU regulation
extending social-security coordination to third-country nationals does not apply to Switzerland,
Norway, Iceland, Liechtenstein or Denmark. Nationality is the only thing separating those two
answers, and nothing in the plan would have asked.

So the tests below are mostly about REFUSAL: the block has to be present, each entry has to have
either a researched answer with a source and a date or an explicit not_applicable WITH a reason,
and a `researched` emergency entry that names no number is refused outright, because that is the
one field in the block somebody dials while something is going wrong.

Run:  python tests/test_arrival_essentials.py
      python -m pytest tests/test_arrival_essentials.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import render_final_trip_html as renderer  # noqa: E402
import validate_trip_html as htmlgate  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def base_plan() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def essentials_findings(plan: dict) -> list[str]:
    return [e for e in renderer.validate_plan(plan) if "arrival_essentials" in e]


def researched(**over) -> dict:
    """A complete `researched` entry, so each test can break exactly one thing."""
    item = {"status": "researched", "summary": "Cards work in town; carry a little cash.",
            "source_url": "https://example.invalid/checked", "checked_at": "2026-09-12",
            "not_applicable_reason": None}
    item.update(over)
    return item


def main() -> int:
    # 1. The block is required at all. This is the case that makes every other test matter: before
    #    it, a plan with no arrival_essentials rendered, validated and saved without a murmur.
    missing = base_plan()
    missing.pop("arrival_essentials", None)
    check("a plan with no arrival_essentials is refused", essentials_findings(missing),
          "the block can be omitted and nothing says so")
    check("the refusal names the four entries",
          any("health_and_insurance" in e for e in essentials_findings(missing)),
          essentials_findings(missing))

    # 2. The fixture itself passes, so every failure below is the thing under test and not a
    #    fixture that never satisfied the rule in the first place.
    check("the fixture's own block satisfies the rule", not essentials_findings(base_plan()),
          essentials_findings(base_plan()))

    # 3. Each of the four is individually required. Looped rather than written four times, because
    #    the loop is what catches a fifth entry added to the contract and not to the check.
    for name in ("payment", "connectivity", "emergency", "health_and_insurance"):
        one_gone = base_plan()
        one_gone["arrival_essentials"].pop(name, None)
        check(f"a plan missing arrival_essentials.{name} is refused",
              any(name in e for e in essentials_findings(one_gone)),
              essentials_findings(one_gone))

    # 4. status is a closed set. An invented status is how a block passes by looking filled in.
    bogus = base_plan()
    bogus["arrival_essentials"]["payment"] = researched(status="probably_fine")
    check("an unknown status is refused", essentials_findings(bogus), "status is not a free field")

    # 5. not_applicable is a real answer and needs a real reason. A domestic trip needs no
    #    consulate; saying so is a different act from nobody having looked, and only the reason
    #    tells them apart.
    silent = base_plan()
    silent["arrival_essentials"]["health_and_insurance"] = {
        "status": "not_applicable", "not_applicable_reason": "   "}
    check("not_applicable with a blank reason is refused", essentials_findings(silent),
          "silence is indistinguishable from nobody having looked")

    stated = base_plan()
    stated["arrival_essentials"]["health_and_insurance"] = {
        "status": "not_applicable",
        "not_applicable_reason": "A domestic trip in the traveller's own city."}
    check("not_applicable WITH a reason is accepted", not essentials_findings(stated),
          essentials_findings(stated))

    # 6. A researched claim carries the same evidence as every other researched claim here.
    for label, over in (
            ("no source_url", {"source_url": None}),
            ("an http source_url", {"source_url": "http://example.invalid/checked"}),
            ("a non-ISO checked_at", {"checked_at": "last week"}),
            ("an empty summary", {"summary": "  "}),
    ):
        broken = base_plan()
        broken["arrival_essentials"]["payment"] = researched(**over)
        check(f"a researched entry with {label} is refused", essentials_findings(broken),
              essentials_findings(broken))

    good = base_plan()
    good["arrival_essentials"]["payment"] = researched()
    check("a complete researched entry is accepted", not essentials_findings(good),
          essentials_findings(good))

    # 7. An `unverified` entry needs a summary but NOT a source -- that is the whole difference
    #    between the two, and a rule that demanded a source for both would make `unverified`
    #    unusable and push authors to claim `researched`.
    honest = base_plan()
    honest["arrival_essentials"]["payment"] = {
        "status": "unverified", "summary": "Not checked against a source on this run."}
    check("an unverified entry with a summary and no source is accepted",
          not essentials_findings(honest), essentials_findings(honest))

    mute = base_plan()
    mute["arrival_essentials"]["payment"] = {"status": "unverified", "summary": ""}
    check("an unverified entry with no summary is refused", essentials_findings(mute),
          "a status with nothing under it tells the traveller nothing")

    # 7b. "Non-empty" is not "readable", and the gate used to confuse them. Both shapes below
    #     passed the first version of this block and reached the page: a list summary rendered as
    #     `['x', 'y']`, and a summary of one zero-width space rendered a card with a heading and
    #     nothing under it. Neither is catchable by the contract, which writes free text as `null`
    #     on purpose, so the gate is the only place this can be decided.
    for label, value in (
            ("a number", 42),
            ("a list", ["x", "y"]),
            ("an object", {"a": 1}),
            ("a zero-width space", "\u200b"),
            ("a byte-order mark", "\ufeff"),
            ("soft hyphens", "\u00ad\u00ad"),
            ("bidi marks", "\u200e\u200f"),
            ("an ideographic space", "\u3000"),
    ):
        blank = base_plan()
        blank["arrival_essentials"]["payment"] = {"status": "unverified", "summary": value}
        check(f"a summary that is {label} is refused", essentials_findings(blank),
              "the gate says filled and the page shows nothing")

    reason_blank = base_plan()
    reason_blank["arrival_essentials"]["payment"] = {
        "status": "not_applicable", "not_applicable_reason": "\u200b"}
    check("a not_applicable reason of invisible characters is refused",
          essentials_findings(reason_blank))

    #     And the other half, which is what keeps the rule from being a Latin-only filter -- the
    #     mistake this repository has made four times elsewhere. Every one of these is a real
    #     answer and must survive.
    for label, value in (
            ("Chinese", "刷卡通用，山区备现金"),
            ("digits only", "112"),
            ("emoji and text", "\U0001f4b3 cards fine"),
            ("Arabic", "البطاقات مقبولة"),
            ("a zero-width joiner inside real words", "card\u200bs fine"),
    ):
        fine = base_plan()
        fine["arrival_essentials"]["payment"] = {"status": "unverified", "summary": value}
        check(f"a {label} summary is accepted", not essentials_findings(fine),
              essentials_findings(fine))

    # 8. The number somebody dials while something is going wrong. A `researched` emergency entry
    #    with a paragraph and no number is the specific failure this rule exists for: it reads as
    #    complete, it passes every generic check above, and it is useless at the only moment it
    #    is opened.
    wordy = base_plan()
    wordy["arrival_essentials"]["emergency"] = researched(
        summary="Emergency services are efficient and English is widely spoken.",
        local_emergency_number=None)
    check("a researched emergency entry with no number is refused", essentials_findings(wordy),
          essentials_findings(wordy))
    numbered = base_plan()
    numbered["arrival_essentials"]["emergency"] = researched(
        summary="Dial the pan-European number.", local_emergency_number="112")
    check("a researched emergency entry WITH a number is accepted",
          not essentials_findings(numbered), essentials_findings(numbered))

    # 9. Collected and not shown is the same defect as never collected -- the rule this skill
    #    already applies to dining ratings. So the block has to reach the page.
    page = renderer.render(base_plan())
    check("the page carries the arrival-essentials region", 'id="arrival-essentials"' in page,
          "the block is in the plan and not on the page")
    for name in ("payment", "connectivity", "emergency", "health_and_insurance"):
        check(f"the page carries the {name} row", f'data-essential="{name}"' in page)

    # A not_applicable entry must print its REASON. Printing the (absent) summary instead would
    # render an empty card, which reads as a section nobody filled in rather than as an answer.
    check("a not_applicable row prints its reason",
          "no border is crossed" in page,
          "the fixture's not_applicable reason did not reach the page")
    check("a not_applicable row is marked as such",
          'data-essential-status="not_applicable"' in page)

    # 10. The page gate requires the region, so a page assembled around the renderer -- or
    #     rendered from a plan that predates the block -- fails loudly rather than quietly
    #     shipping without it.
    stripped = re.sub(r'<section id="arrival-essentials".*?</section>', "", page, flags=re.S)
    found = htmlgate.validate(stripped, None, set(), None, notes=[])
    check("the html gate refuses a page with no arrival-essentials region",
          any("arrival-essentials" in e for e in found),
          [e for e in found if "region" in e])
    kept = htmlgate.validate(page, None, set(), None, notes=[])
    check("the html gate accepts the page that has it",
          not any("arrival-essentials" in e for e in kept),
          [e for e in kept if "arrival-essentials" in e])

    # 11. The i18n backstop. The substitution table translates these headings; only a line in the
    #     gate's own list notices when one stops being translated. This is not hypothetical
    #     symmetry -- a Chinese page shipped carrying "Add this trip to your calendar" and passed
    #     BOTH gates, because the string was translated in the table and never added to the list.
    #     So the test is in two halves: the patterns must MATCH the English render (or they are
    #     decoration), and must NOT match the localized one (or the renderer is leaking).
    #     Written per-STRING rather than per-pattern, and that is the whole point. The first
    #     version of this test asked only "does the gate carry patterns for this panel", so
    #     deleting one of them left the others to answer yes -- it survived a mutation that
    #     removed the heading guard outright. Asking instead "for this exact string the renderer
    #     emits, does SOME pattern in the gate match it" fails the moment any single guard goes.
    patterns, _ = htmlgate.renderer_owned_english()
    renderer_owned = (
        "<h2>Your first hour on the ground</h2>",
        "<strong>Paying</strong>",
        "<strong>Getting online</strong>",
        "<strong>If something goes wrong</strong>",
        "<strong>Health and insurance</strong>",
        ">Add this trip to your calendar<",
    )
    guarded = []
    for literal in renderer_owned:
        check(f"the English render actually emits {literal!r}", literal in page,
              "the test is guarding a string this renderer no longer produces")
        matching = [p for p in patterns if re.search(p, literal)]
        check(f"the gate guards {literal!r}", matching,
              "renderer English with no guard: it can stop being translated and both gates stay "
              "green, which is exactly how a Chinese page shipped saying 'Add this trip to your "
              "calendar'")
        guarded.extend(matching)

    zh = base_plan()
    zh["trip"]["language"] = "zh-CN"
    zh_page = renderer.render(zh)
    for literal in renderer_owned:
        check(f"the localized page does not leak {literal!r}", literal not in zh_page,
              "renderer English survived on a non-English page")
    for pattern in sorted(set(guarded)):
        check(f"the localized page does not match guard {pattern!r}",
              not re.search(pattern, zh_page), "renderer English survived on a non-English page")

    # 12. The scaffold emits the block, so the requirement is met as a form to fill rather than as
    #     a gate failure on an author who never knew it existed.
    contract = json.loads((ROOT / "templates" / "final-trip-plan.json").read_text(encoding="utf-8"))
    check("the contract declares the block", "arrival_essentials" in contract)
    for name in ("payment", "connectivity", "emergency", "health_and_insurance"):
        check(f"the contract declares {name}", name in contract.get("arrival_essentials", {}))

    #     Run as a subprocess rather than imported, because what has to hold is that the COMMAND
    #     SKILL.md tells an author to run emits the block -- importing the module and calling an
    #     internal would test a code path nobody uses. Checking the contract alone was the first
    #     version of this and proved nothing: the contract can declare a block the scaffold never
    #     writes, which is the state this feature started in.
    scaffold = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "new_plan_skeleton.py"),
         "--start", "2027-05-07", "--end", "2027-05-10",
         "--origin", "Amsterdam", "--destination", "Bern",
         "--intake-method", "user_supplied", "--source-note", "scaffold check"],
        capture_output=True, text=True)
    check("the scaffold runs", scaffold.returncode == 0, scaffold.stderr[-300:])
    if scaffold.returncode == 0:
        skeleton = json.loads(scaffold.stdout)
        check("the scaffold emits arrival_essentials", "arrival_essentials" in skeleton,
              "an author who never read the reference meets this as a gate failure instead of a "
              "form to fill")
        check("the scaffold's block satisfies its own gate", not essentials_findings(skeleton),
              essentials_findings(skeleton))
        for name in ("payment", "connectivity", "emergency", "health_and_insurance"):
            entry = skeleton.get("arrival_essentials", {}).get(name, {})
            check(f"the scaffold's {name} entry prompts rather than asserts",
                  str(entry.get("summary", "")).startswith("TODO"),
                  f"a scaffold that states a fact is a scaffold that ships one: {entry}")

    if failures:
        print(f"ARRIVAL ESSENTIALS FAILED ({len(failures)}):", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all arrival-essentials cases passed")
    return 0


def test_arrival_essentials() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
