#!/usr/bin/env python3
"""Regression tests for scripts/check_shortlist_consistency.py.

Discovery mode had no gate at all, so unlike the Construction tests these cases do not pin defects
that shipped -- they pin the defects the design pass identified as reachable, each one stated as a
concrete wrong answer a traveller could act on. Every rule here survived an adversarial review that
was told to kill by default; none survived unchanged, which is why several cases below exist
specifically to prove a rule does NOT fire on correct work.
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "discovery-shortlist-fixture.json"
INTAKE = ROOT / "tests" / "discovery-intake-fixture.json"
SCRIPT = ROOT / "scripts" / "check_shortlist_consistency.py"


def run(doc: dict, intake: bool = False) -> tuple[int, str]:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "shortlist.json"
        path.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        command = [sys.executable, str(SCRIPT), str(path)]
        # --no-intake is the deliberate escape hatch, not a default: the cases below are about
        # every other rule, and omitting both flags is now its own refusal (tested separately).
        command += ["--intake", str(INTAKE)] if intake else ["--no-intake"]
        result = subprocess.run(command, capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr


def main() -> int:
    base = json.loads(FIXTURE.read_text(encoding="utf-8"))
    failures: list[str] = []

    # Omitting the intake used to print an accurate note and exit 0 -- and an exit 0 is what an
    # assistant reads, so the one check that catches a winner never tested against a stated
    # constraint was skippable by saying nothing. Same shape as --verification/--unverified.
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "shortlist.json"
        path.write_text(json.dumps(base, ensure_ascii=False), encoding="utf-8")
        bare = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                              capture_output=True, text=True)
        if bare.returncode == 0:
            failures.append("running with neither --intake nor --no-intake must refuse, "
                            f"got exit 0\n{bare.stdout + bare.stderr}")
        elif "--no-intake" not in (bare.stdout + bare.stderr):
            failures.append("the refusal must name the escape hatch\n" + bare.stderr)
        opted_out = subprocess.run([sys.executable, str(SCRIPT), str(path), "--no-intake"],
                                   capture_output=True, text=True)
        if opted_out.returncode != 0:
            failures.append("--no-intake must run\n" + opted_out.stdout + opted_out.stderr)
        elif "NO INTAKE" not in (opted_out.stdout + opted_out.stderr):
            failures.append("--no-intake must say loudly that coverage did not run\n"
                            + opted_out.stdout)

    def expect_ok(name: str, doc: dict, intake: bool = False) -> None:
        code, out = run(doc, intake)
        if code != 0:
            failures.append(f"{name}: expected pass, got exit {code}\n{out}")

    def expect_fail(name: str, doc: dict, needle: str, intake: bool = False) -> None:
        code, out = run(doc, intake)
        if code != 1 or needle not in out:
            failures.append(f"{name}: expected failure containing {needle!r}, got exit {code}\n{out}")

    expect_ok("the fixture that defines correct output passes", copy.deepcopy(base))

    # The defect the whole file exists for: two figures that cannot be ranked against each other.
    # The traveller sees the smaller number, picks it, and it was priced for one person while the
    # other was priced for the party.
    doc = copy.deepcopy(base)
    doc["candidates"][1]["cost_estimate"]["cost_basis"] = "party_total"
    expect_fail("a party total ranked beside per-person figures", doc, "per person")

    doc = copy.deepcopy(base)
    doc["candidates"][1]["trip_context"]["party_size"] = 2
    expect_fail("a candidate priced for a different party size", doc, "cannot be ranked")

    doc = copy.deepcopy(base)
    doc["candidates"][1]["trip_context"]["currency"] = "USD"
    expect_fail("a candidate priced in another currency", doc, "cannot be ranked")

    # SKILL.md's own sentence: do not compare a flight-only figure with an all-in figure.
    doc = copy.deepcopy(base)
    doc["candidates"][1]["cost_estimate"]["included_categories"] = ["flight"]
    doc["candidates"][1]["trip_context"]["budget_scope"] = ["flight", "accommodation"]
    expect_fail("a flight-only figure beside all-in figures", doc, "says nothing about")

    # ...and the escape is a declaration with a reason, not a way to switch the rule off.
    doc = copy.deepcopy(base)
    doc["candidates"][1]["cost_estimate"]["included_categories"] = ["flight"]
    doc["candidates"][1]["cost_estimate"]["not_applicable_categories"] = [
        {"category": "accommodation", "reason": "Hosted by family; no lodging cost is incurred."}]
    expect_ok("a category correctly declared not applicable", doc)

    doc = copy.deepcopy(base)
    doc["candidates"][1]["cost_estimate"]["included_categories"] = ["flight"]
    doc["candidates"][1]["cost_estimate"]["not_applicable_categories"] = [
        {"category": "accommodation", "reason": ""}]
    expect_fail("a declared exemption with no reason", doc, "with no reason")

    # The rule must not fire on a legitimate mixed-mode shortlist. This is the false positive the
    # adversarial pass produced against the first draft: a rail-reached candidate compared with a
    # flown one is fully comparable -- same window, party, currency and basis -- and demanding a
    # declaration from either would fail correct work. Arrival modes are folded into one surface
    # for exactly this reason, and 'accommodation' is not foldable, so the check above still bites.
    doc = copy.deepcopy(base)
    doc["trip_context"]["budget_scope"] = ["flight", "accommodation"]
    doc["candidates"][1]["cost_estimate"]["included_categories"] = ["rail", "accommodation"]
    doc["candidates"][1]["trip_context"]["budget_scope"] = ["rail", "accommodation"]
    expect_ok("a rail-reached candidate compared with a flown one", doc)

    # Spelling is not scope. 'flights' and 'flight' are one scope that a set comparison reports as
    # two, so the vocabulary is closed and shared with the Construction budget.
    doc = copy.deepcopy(base)
    doc["candidates"][0]["cost_estimate"]["included_categories"] = ["flights", "accommodation"]
    expect_fail("a category spelled outside the shared vocabulary", doc, "outside the shared vocabulary")

    # An unpriced candidate is a legitimate output, but "no number" must be distinguishable from
    # "nobody looked".
    doc = copy.deepcopy(base)
    doc["candidates"][2]["cost_estimate"]["total_low"] = None
    doc["candidates"][2]["cost_estimate"]["total_high"] = None
    expect_fail("an unpriced candidate with no reason", doc, "not_priced_reason")

    doc = copy.deepcopy(base)
    doc["candidates"][2]["cost_estimate"]["total_low"] = None
    doc["candidates"][2]["cost_estimate"]["total_high"] = None
    doc["candidates"][2]["cost_estimate"]["not_priced_reason"] = (
        "Ferry season unconfirmed, so lodging could not be located; kept as an idea only.")
    # Dropping the figure drops the verdict with it: 'tight' is a comparison against the cap, and
    # there is now nothing to compare. The candidate is already 'failed', so no budget_fit is owed.
    doc["candidates"][2]["cost_estimate"]["budget_fit"] = "unknown"
    expect_ok("an unpriced candidate that says why", doc)

    # A hard constraint is not a low score to be outweighed.
    doc = copy.deepcopy(base)
    doc["candidates"][0]["eligibility"]["failed_constraints"] = ["needs a visa the traveller lacks"]
    expect_fail("a winner that fails a hard constraint", doc, "not a low score to be outweighed")

    doc = copy.deepcopy(base)
    doc["candidates"][0]["eligibility"]["hard_filter_status"] = "unknown"
    expect_fail("a winner whose hard filter never ran", doc, "nobody established")

    # The status and the record it summarises must not contradict each other.
    doc = copy.deepcopy(base)
    doc["candidates"][0]["eligibility"]["failed_constraints"] = [
        {"constraint_id": "budget.hard_cap_amount", "note": "Over the cap in every week."}]
    expect_fail("a passing status over its own failed constraint", doc, "One of the")

    # An empty feasible set is an outcome, not a scoring error.
    doc = copy.deepcopy(base)
    for candidate in doc["candidates"]:
        candidate["eligibility"]["hard_filter_status"] = "failed"
        candidate["eligibility"]["failed_constraints"] = ["outside the budget cap"]
    expect_fail("a winner named when nothing was feasible", doc, "empty feasible set")

    # ...and reporting the conflict honestly, with no winner, is accepted.
    doc = copy.deepcopy(base)
    for candidate in doc["candidates"]:
        candidate["eligibility"]["hard_filter_status"] = "failed"
        candidate["eligibility"]["failed_constraints"] = ["outside the budget cap"]
    doc["recommendation"] = {"winner": None, "runner_up": None,
                             "why_not_runner_up": "No candidate cleared the budget cap."}
    # Both blockers are named, including the one that only removed the excluded entry. The rule
    # caught that omission when this case first listed the cap alone, which is exactly its job:
    # a traveller asked to raise their budget would not have learned that a red-eye rule also
    # removed part of the pool.
    doc["outcome"] = {"state": "constraint_conflict",
                      "blocking_constraints": ["outside the budget cap", "no red-eye"],
                      "minimum_relaxation": "Raise the cap by about EUR 150, or drop a night.",
                      "blocking_fact": None}
    expect_ok("a constraint conflict reported instead of a winner", doc)

    # A recommendation must point at evidence that exists.
    doc = copy.deepcopy(base)
    doc["recommendation"]["winner"] = "Somewhere Never Evaluated"
    expect_fail("a winner with no candidate record", doc, "not the destination.name of any")

    # --- the contract-dependent rules -------------------------------------------------------
    # Each of these needed a field the contract did not have. They are grouped because they share
    # one design decision: the author declares and the checker reads, never the other way round.

    # outcome.state is required, because every conflict rule keys on it and omitting the field
    # would otherwise be the single escape from all of them at once.
    doc = copy.deepcopy(base)
    doc.pop("outcome")
    expect_fail("a shortlist with no declared outcome", doc, "outcome.state is missing")

    doc = copy.deepcopy(base)
    doc["outcome"]["state"] = "looks_fine"
    expect_fail("an outcome state outside the declared enum", doc, "not one of")

    # A status outside its vocabulary is worse than a wrong status: every rule keyed on it reads
    # the unknown value as "not that state" and silently stops firing.
    doc = copy.deepcopy(base)
    doc["candidates"][0]["eligibility"]["hard_filter_status"] = "feasible"
    expect_fail("a hard_filter_status outside the declared enum", doc, "hard_filter_status")

    doc = copy.deepcopy(base)
    doc["candidates"][0]["recommendation_state"] = "shortlisted"
    expect_fail("a recommendation_state off the booking ladder", doc, "recommendation_state")

    # not_pursued is the honest alternative to an unfinished filter, so it owes its sentence.
    doc = copy.deepcopy(base)
    doc["candidates"][2]["eligibility"]["hard_filter_status"] = "not_pursued"
    doc["candidates"][2]["eligibility"]["failed_constraints"] = []
    expect_fail("not_pursued with no reason", doc, "not_pursued_reason")

    doc = copy.deepcopy(base)
    doc["candidates"][2]["eligibility"]["hard_filter_status"] = "not_pursued"
    doc["candidates"][2]["eligibility"]["failed_constraints"] = []
    doc["candidates"][2]["eligibility"]["not_pursued_reason"] = (
        "Not priced: further from origin than the two already at the cap, so it cannot win.")
    expect_ok("not_pursued with a reason that says what was skipped", doc)

    # A money verdict that was asserted rather than computed.
    doc = copy.deepcopy(base)
    doc["candidates"][0]["cost_estimate"]["budget_fit"] = "unknown"
    expect_fail("a passing candidate whose budget was never measured", doc, "still 'unknown'")

    doc = copy.deepcopy(base)
    doc["candidates"][0]["cost_estimate"]["budget_fit"] = "unknown"
    doc["candidates"][0]["cost_estimate"]["budget_fit_unpriced_reason"] = (
        "Hosted throughout and reached on a companion fare; the cap cannot bind.")
    expect_ok("an unmeasured budget with a declared reason", doc)

    # Pure arithmetic on two numbers the shortlist already carries.
    doc = copy.deepcopy(base)
    doc["candidates"][0]["cost_estimate"]["total_low"] = 900
    doc["candidates"][0]["cost_estimate"]["total_high"] = 950
    expect_fail("a 'within' verdict above the declared cap", doc, "exceeds the declared cap")

    doc = copy.deepcopy(base)
    doc["candidates"][0]["cost_estimate"]["as_of"] = None
    expect_fail("a priced candidate with no as_of date", doc, "no ISO as_of date")

    doc = copy.deepcopy(base)
    doc["candidates"][0]["cost_estimate"]["as_of"] = "2027-01-01"
    expect_fail("a figure dated after the shortlist itself", doc, "after the shortlist's own")

    doc = copy.deepcopy(base)
    doc["candidates"][0]["cost_estimate"]["as_of"] = "2025-01-01"
    expect_fail("a figure researched long before the comparison", doc, "days before this")

    doc = copy.deepcopy(base)
    doc["candidates"][0]["cost_estimate"]["as_of"] = "2025-01-01"
    doc["candidates"][0]["cost_estimate"]["as_of_exception_reason"] = (
        "Contracted corporate fare, fixed for the calendar year.")
    expect_ok("an old figure that says why it still holds", doc)

    # Telling a traveller to give up a requirement is expensive, so the claim has to be earned.
    def conflict(doc: dict) -> dict:
        doc["outcome"] = {"state": "constraint_conflict",
                          "blocking_constraints": ["budget.hard_cap_amount"],
                          "minimum_relaxation": "Raise the cap by about EUR 150, or drop a night.",
                          "blocking_fact": None}
        doc["recommendation"] = {"winner": None, "runner_up": None, "why_not_runner_up": None}
        for candidate in doc["candidates"]:
            candidate["eligibility"]["hard_filter_status"] = "failed"
            candidate["eligibility"]["failed_constraints"] = [
                {"constraint_id": "budget.hard_cap_amount", "note": "Over the cap in every week."}]
        doc["excluded"] = []
        return doc

    expect_ok("an honestly declared constraint conflict", conflict(copy.deepcopy(base)))

    doc = conflict(copy.deepcopy(base))
    doc["candidates"][0]["eligibility"]["hard_filter_status"] = "passed"
    doc["candidates"][0]["eligibility"]["failed_constraints"] = []
    expect_fail("a conflict declared while something survived", doc, "Something survived")

    # The defect that makes this rule worth its weight: an unfinished filter and a real conflict
    # produce the same empty pass set, and only one of them justifies the ask.
    doc = conflict(copy.deepcopy(base))
    doc["candidates"][1]["eligibility"]["hard_filter_status"] = "unknown"
    doc["candidates"][1]["eligibility"]["failed_constraints"] = []
    expect_fail("a conflict declared over a filter that never finished", doc,
                "same empty pass set")

    doc = conflict(copy.deepcopy(base))
    doc["outcome"]["blocking_constraints"] = []
    expect_fail("a conflict that names nothing to relax", doc, "smallest conflicting set")

    doc = conflict(copy.deepcopy(base))
    doc["outcome"]["minimum_relaxation"] = None
    expect_fail("a conflict with no minimum relaxation", doc, "minimum_relaxation")

    doc = conflict(copy.deepcopy(base))
    doc["recommendation"]["winner"] = "Fixture Coast"
    expect_fail("a conflict that still names a winner", doc, "not a recommendation")

    # The traveller must not be asked to relax a constraint that removed only part of the pool.
    doc = conflict(copy.deepcopy(base))
    doc["candidates"][2]["eligibility"]["failed_constraints"] = [
        {"constraint_id": "entry", "note": "Visa required that the traveller does not hold."}]
    doc["excluded"] = [{"destination": "Fixture Highlands", "reason": "Red-eye only.",
                        "failed_constraint": "no red-eye arrivals"}]
    expect_fail("rejections the declared conflict does not claim", doc, "does not claim")

    doc = copy.deepcopy(base)
    doc["outcome"]["state"] = "blocked"
    expect_fail("a blocked outcome with no blocking fact", doc, "blocking_fact")

    # A failing candidate may be shown, but not silently: scored beside feasible options with
    # nothing said, it reads as an ordinary choice. This is also what keeps
    # conditional_on_relaxation from being another field nobody reads.
    doc = copy.deepcopy(base)
    doc["candidates"][2]["fit"].pop("conditional_on_relaxation", None)
    doc["conditional_options"] = []
    expect_fail("a failing candidate scored with nothing marking it conditional", doc,
                "reads as an ordinary choice")

    # And the narrowing that rule needed. Its first version fired on every candidate of an
    # honestly reported conflict, where all of them failing IS the finding and
    # outcome.minimum_relaxation already answers "what would have to change" for the whole
    # document. Requiring each candidate to repeat it is the ceremony that gets a check bypassed.
    doc = conflict(copy.deepcopy(base))
    doc["conditional_options"] = []
    for candidate in doc["candidates"]:
        candidate["fit"].pop("conditional_on_relaxation", None)
    expect_ok("failing candidates under a declared conflict need no per-candidate condition", doc)

    doc = copy.deepcopy(base)
    for candidate in doc["candidates"]:
        candidate["eligibility"]["hard_filter_status"] = "failed"
    expect_fail("every candidate failed while still called a shortlist", doc, "empty")

    # --- constraint coverage, computed from the intake ---------------------------------------
    # Without --intake this rule does not run, and the run says so rather than implying coverage.
    code, out = run(copy.deepcopy(base))
    if "constraint coverage did not run" not in out:
        failures.append(f"a run with no intake must say coverage did not run\n{out}")

    expect_ok("the fixture answers every constraint its intake declares",
              copy.deepcopy(base), intake=True)

    doc = copy.deepcopy(base)
    doc["candidates"][0]["eligibility"]["confirmed_constraints"] = [
        c for c in doc["candidates"][0]["eligibility"]["confirmed_constraints"]
        if c["constraint_id"] != "party.mobility_or_access_needs[0]"]
    expect_fail("a candidate silent about a stated constraint", doc,
                "party.mobility_or_access_needs[0]", intake=True)

    doc = copy.deepcopy(base)
    doc["candidates"][0]["eligibility"]["unresolved_constraints"].append(
        {"constraint_id": "budget.hard_cap_amount", "note": "Also recorded here."})
    expect_fail("one constraint answered in two buckets", doc, "more than one bucket", intake=True)

    doc = copy.deepcopy(base)
    doc["candidates"][0]["eligibility"]["not_applicable_constraints"] = [
        {"constraint_id": "entry", "reason": ""}]
    doc["candidates"][0]["eligibility"]["confirmed_constraints"] = [
        c for c in doc["candidates"][0]["eligibility"]["confirmed_constraints"]
        if c["constraint_id"] != "entry"]
    expect_fail("a not-applicable verdict with no reason", doc, "not applicable with no reason",
                intake=True)

    # The exclusion list is discharged before generation, so the thing itself is checked rather
    # than bookkeeping about it.
    doc = copy.deepcopy(base)
    doc["candidates"][1]["destination"]["name"] = "Fixture Forbidden Isle"
    doc["recommendation"]["runner_up"] = "Fixture Forbidden Isle"
    expect_fail("a candidate the traveller had excluded", doc, "which the traveller excluded",
                intake=True)

    # An early return added for safety created the loudest version of the defect this file exists
    # for: a shortlist naming a winner while carrying no candidates passed silently, because the
    # loop that checks the winner had nothing to iterate.
    doc = copy.deepcopy(base)
    doc["candidates"] = []
    expect_fail("a winner named over an empty candidate pool", doc, "no candidates at all")

    # And an empty pool with no winner stays legal: a constrained run that excluded everything
    # says so through outcome.state, and demanding candidates there would fire on correct work.
    doc = copy.deepcopy(base)
    doc["candidates"] = []
    doc["recommendation"] = {"winner": None, "runner_up": None, "why_not_runner_up": None}
    expect_ok("an empty pool that claims no winner", doc)

    # Malformed input is a finding, never a traceback.
    code, out = run({"candidates": "not a list", "trip_context": None})
    if "Traceback" in out:
        failures.append(f"malformed input produced a traceback\n{out}")

    # SKILL.md step 5 says "score only candidates with sufficient evidence", and nothing read
    # candidate.evidence at all -- so a candidate could carry fit.score 82, be named winner, and
    # hold evidence: [], recommending a destination to a traveller with no source under it.
    p = copy.deepcopy(base)
    p["candidates"][0]["evidence"] = []
    expect_fail("a scored winner with no evidence", p, "carries no evidence", intake=True)

    for field in ("claim", "source_url", "accessed_on"):
        p = copy.deepcopy(base)
        p["candidates"][0]["evidence"][0].pop(field)
        expect_fail(f"an evidence entry missing {field}", p, field, intake=True)

    p = copy.deepcopy(base)
    p["candidates"][0]["evidence"][0]["source_url"] = "http://fixture.example/climate"
    expect_fail("an evidence entry sourced over plain HTTP", p, "not HTTPS", intake=True)

    # Honest work in progress must stay quiet, or the rule punishes saying so.
    p = copy.deepcopy(base)
    p["candidates"].append({"destination": {"name": "Still researching"},
                            "research_status": "partial", "evidence": []})
    code, out = run(p, intake=True)
    if "carries no evidence" in out:
        failures.append("an unscored, unrecommended candidate must not be held to the evidence "
                        f"rule\n{out}")

    if failures:
        print(f"FAILED {len(failures)} case(s):\n", file=sys.stderr)
        for failure in failures:
            print(f"--- {failure}\n", file=sys.stderr)
        return 1
    print("all shortlist-consistency regression cases passed")
    return 0


def test_shortlist_consistency() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
