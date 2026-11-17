#!/usr/bin/env python3
"""The entry answer is the one fact that decides whether the traveller boards.

Two holes, both measured on 2026-09-24 against v2.7.0:

* A plan could be saved and rendered as `verified` while its own entry answer still said
  `unverified`: a Netherlands-to-US plan with `entry_context.status: unverified` produced 0 findings
  and a page with no banner. The entry domain exists to settle exactly that field; a report cannot
  certify a plan that leaves it open.
* A plan whose intake says the trip leaves the traveller's country of residence could omit
  `entry_context` altogether. The template tells a domestic trip to delete the block, and the plan
  alone cannot tell "domestic" from "nobody looked" -- but the intake can.

Run:  python tests/test_entry_answers.py
      python -m pytest tests/test_entry_answers.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_plan_consistency as cpc  # noqa: E402
import new_verification_report as scaffold  # noqa: E402
import plan_flags  # noqa: E402
import render_final_trip_html as renderer  # noqa: E402
import validate_trip_html as htmlgate  # noqa: E402

FIXTURE = ROOT / "tests" / "booking-ready-fixture.json"

failures: list[str] = []


def check(label: str, condition: object, detail: object = "") -> None:
    if not condition:
        failures.append(f"{label}\n    {detail}")


def base_plan() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def entry(status: str) -> dict:
    return {"status": status, "summary": "Checked against the official visa waiver page.",
            "traveler_basis": "short_stay_visa_or_visa_free",
            "source_url": "https://esta.cbp.dhs.gov/", "checked_at": "2026-09-12"}


def fill(node: object) -> object:
    """Replace every scaffold placeholder with a concrete sentence, as an author would."""
    if isinstance(node, dict):
        out = {k: fill(v) for k, v in node.items()}
        if "verdict" in out:
            out["verdict"] = "confirmed"
            out["evidence_url"] = "https://official-source.test/checked"
        return out
    if isinstance(node, list):
        return [fill(v) for v in node]
    if isinstance(node, str) and node.startswith("TODO:"):
        return "Opened the source page and read the rule for these dates."
    return node


def filled_report(plan: dict, plan_path: str) -> dict:
    report, _ = scaffold.build(plan, Path(plan_path))
    return fill(report)


def with_intake(tmp: Path, plan: dict, feasibility: dict) -> dict:
    path = tmp / "intake-20260101-fixture.json"
    path.write_text(json.dumps({"feasibility": feasibility, "party": {}, "budget": {},
                                "experience": {}}, ensure_ascii=False), encoding="utf-8")
    plan["intake_context"]["intake_file"] = str(path)
    return plan


def plan_check(name: str, plan: dict) -> list[str]:
    """Run one PLAN_CHECK by name; a check that does not exist is a failing case, not a crash
    that hides every other result in this file."""
    check_fn = getattr(cpc, name, None)
    if check_fn is None:
        failures.append(f"{name} does not exist")
        return []
    errors: list[str] = []
    check_fn(plan, errors, [])
    return errors


def main() -> int:
    with tempfile.TemporaryDirectory() as raw:
        tmp = Path(raw)

        # 1. The intake says the trip leaves the country; the plan has no entry answer at all.
        plan = with_intake(tmp, base_plan(), {"passport_validity_status": "valid_through_trip",
                                              "entry_assessment_required": False})
        plan.pop("entry_context", None)
        errors: list[str] = []
        cpc.check_preferences_came_from_the_intake(plan, errors, [])
        check("a cross-border intake with no entry_context is refused",
              any("entry_context" in e for e in errors), errors)

        # 2. A domestic intake owes no entry answer.
        plan = with_intake(tmp, base_plan(), {"passport_validity_status": "not_applicable_domestic",
                                              "entry_assessment_required": False})
        plan.pop("entry_context", None)
        errors = []
        cpc.check_preferences_came_from_the_intake(plan, errors, [])
        check("a domestic intake owes no entry_context",
              not [e for e in errors if "entry_context" in e], errors)

        # 3. The traveller has to apply for a visa: that alone says the trip leaves the country.
        plan = with_intake(tmp, base_plan(), {"entry_assessment_required": True})
        plan.pop("entry_context", None)
        errors = []
        cpc.check_preferences_came_from_the_intake(plan, errors, [])
        check("an intake that needs a visa owes an entry answer",
              any("entry_context" in e for e in errors), errors)

    # 4. A plan that calls itself verified cannot leave its entry answer open ...
    plan = base_plan()
    plan["entry_context"] = entry("unverified")
    plan["verification_status"] = "verified"
    errors = plan_check("check_verified_plan_entry_answer", plan)
    check("a verified plan with an unverified entry answer is refused",
          any("entry" in e for e in errors), errors)
    # ... and a per-jurisdiction answer left open counts the same.
    plan["entry_context"] = entry("not_required")
    plan["entry_context"]["per_jurisdiction"] = [
        dict(entry("not_required"), jurisdiction="美国"),
        dict(entry("unverified"), jurisdiction="巴哈马")]
    errors = plan_check("check_verified_plan_entry_answer", plan)
    check("an unverified per-jurisdiction answer on a verified plan is refused",
          any("巴哈马" in e for e in errors), errors)
    # A plan that says it is unverified already carries the banner; nothing to add.
    plan["verification_status"] = "unverified"
    errors = plan_check("check_verified_plan_entry_answer", plan)
    check("an unverified plan is left to its banner", not errors, errors)

    # 5. A verification report cannot certify a plan whose entry answer is still open.
    plan = base_plan()
    plan["entry_context"] = entry("not_required")
    report = filled_report(plan, "plan.json")
    baseline: list[str] = []
    cpc.check_verification(report, baseline, [], plan=plan, plan_path="plan.json")
    plan["entry_context"] = entry("unverified")
    report = filled_report(plan, "plan.json")
    found: list[str] = []
    cpc.check_verification(report, found, [], plan=plan, plan_path="plan.json")
    new = [e for e in found if e not in baseline]
    check("a report cannot certify an unverified entry answer",
          any("entry" in e and "unverified" in e for e in new), new or found)

    # 6. Every jurisdiction's answer reaches the page. The multi-country fix stopped at the JSON:
    #    per_jurisdiction was required, checked for coverage, and rendered nowhere.
    plan = base_plan()
    plan["entry_context"] = entry("not_required")
    plan["entry_context"]["per_jurisdiction"] = [
        dict(entry("not_required"), jurisdiction="泰国", summary="CANARY-A"),
        dict(entry("required_held"), jurisdiction="越南", summary="CANARY-B")]
    page = renderer.render(plan)
    rows = page.split('class="entry-jurisdiction"')[1:]
    check("each jurisdiction's answer is its own row on the page",
          len(rows) == 2 and "CANARY-A" in rows[0] and "CANARY-B" in rows[1],
          f"{len(rows)} row(s)")

    # 7. A per-jurisdiction status is the same closed enum as the flat one.
    bad = json.loads(json.dumps(plan))
    bad["entry_context"]["per_jurisdiction"][1]["status"] = "maybe"
    check("a free-text per-jurisdiction status is refused",
          any("per_jurisdiction" in e for e in renderer.validate_plan(bad)),
          renderer.validate_plan(bad))

    # 8. A Chinese page prints the statuses in Chinese and adds no renderer English.
    chinese = json.loads(json.dumps(plan))
    chinese["trip"]["language"] = "zh-CN"
    without = json.loads(json.dumps(chinese))
    without["entry_context"].pop("per_jurisdiction")
    def page_errors(p: dict, page_html: str) -> list[str]:
        """The page gate armed from the plan. A missing flag or parameter is a failing case, not a
        crash that hides the rest of this file."""
        flags = plan_flags.derive_html_flags(p)
        try:
            return htmlgate.validate(page_html, flags.expected_days,
                                     set(flags.required_booking_types), flags.transport_mode, [],
                                     require_unverified_banner=flags.require_unverified_banner,
                                     entry_jurisdictions=flags.entry_jurisdictions)
        except (AttributeError, TypeError) as exc:
            failures.append(f"the page gate cannot be armed with entry jurisdictions: {exc}")
            return []
    zh_page = renderer.render(chinese)
    zh_rows = "".join(zh_page.split('class="entry-jurisdiction"')[1:])
    check("a Chinese page translates the per-jurisdiction statuses",
          "not_required" not in zh_rows and "required_held" not in zh_rows, zh_rows[:300])
    added = [e for e in page_errors(chinese, zh_page)
             if e not in page_errors(without, renderer.render(without))]
    check("the rows add no renderer English to a Chinese page", not added, added)

    # 9. The page gate, armed from the plan, notices a jurisdiction the page does not show.
    torn = page.replace('data-entry-jurisdiction="越南"', 'data-entry-removed="越南"')
    errors = page_errors(plan, torn)
    check("a page missing a jurisdiction's row is refused under --plan",
          any("越南" in e for e in errors), errors)
    check("the intact page raises no jurisdiction finding",
          not [e for e in page_errors(plan, page) if "jurisdiction" in e],
          [e for e in page_errors(plan, page) if "jurisdiction" in e])

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("entry answer cases passed")
    return 0


def test_entry_answers() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
