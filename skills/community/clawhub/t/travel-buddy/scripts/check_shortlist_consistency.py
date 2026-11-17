#!/usr/bin/env python3
"""Deterministic consistency lint for a Travel Buddy Discovery shortlist.

Discovery was the half of this skill with no gate at all. Construction has nineteen checks plus an
HTML validator; templates/destination-evaluation.json was referenced only in SKILL.md prose, and no
script read it. Every rule about comparability, evidence and the hard-filter ordering lived in
sentences, which is the exact configuration this project has learned fails silently.

A shortlist is a COMPARISON, so its worst defects live BETWEEN candidates rather than inside one.
Each record can be individually impeccable and the ranking still be meaningless -- one figure per
person beside another for the whole party, or one covering flights only beside one covering
everything. Nothing inside a single candidate can detect that, which is why these checks read the
set.

What this deliberately does NOT do: judge whether evidence is sufficient, whether a score is
deserved, or whether a destination is a good idea. Those need a reader. This decides only what
arithmetic and set membership can decide, and says so rather than implying more.

Usage: python check_shortlist_consistency.py <shortlist.json>
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from render_final_trip_html import BUDGET_CATEGORIES  # noqa: E402

PLACEHOLDER_MARKERS = ("TODO:", "example.invalid")

# Arrival modes are interchangeable ways to buy the same thing: getting there. Comparing raw enum
# members would report Brussels-by-rail and Lisbon-by-air as different cost scopes and demand a
# declaration from both, which is a rule firing on correct work. Folding them into one surface
# still catches the defect the check exists for -- a flight-only figure beside an all-in one --
# because 'accommodation' is its own surface and cannot be folded away.
ARRIVAL_SURFACE = {"flight", "rail", "intercity_bus", "ferry", "rental_car", "fuel_tolls_parking"}

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"

# How stale a priced figure may be relative to the document that ranks it. Fares and lodging are
# the most volatile facts in the skill, and a figure researched months before the comparison is
# not a figure about the same trip. Declared here rather than inline so the number is arguable in
# one place.
MAX_PRICE_AGE_DAYS = 45


PASSING_STATUSES = {"passed"}


def _obj(value) -> dict:
    """Malformed input must produce a finding, never a traceback -- an operator who sees a stack
    trace learns nothing about their shortlist and tends to stop running the gate."""
    return value if isinstance(value, dict) else {}


def _seq(value) -> list:
    return value if isinstance(value, list) else []


def _number(value):
    """The value if it is a real number, else None -- never 0.0.

    check_plan_consistency._num returns 0.0 for a missing value, which is right there and wrong
    here: these checks compare declared costs, and reading an absent total as zero would make a
    candidate look free rather than unpriced.
    """
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def _missing(*values: object) -> bool:
    """Empty, absent, or still the template's placeholder.

    Named _missing rather than _unfilled deliberately. check_plan_consistency.py has a function
    called _unfilled that asks a NARROWER question -- does this contain a TODO marker -- so
    _unfilled("") is False there and True here. Two names would have been fine; one name with two
    meanings is a trap, and it caught me: a rule written in that file against the wrong one of the
    pair looked present and measured nothing, and two of its tests passed while asserting a
    failure. The same divergence exists for _num, which returns 0.0 there and None here, so a
    missing number reads as zero on one side of the skill and as absent on the other. Content rules must not run
    on a record nobody has filled in, because the error they produce describes a candidate that
    does not exist yet -- a skeleton once opened with 38 errors, most of them about nothing."""
    for value in values:
        if value is None:
            return True
        if isinstance(value, str):
            text = value.strip()
            if not text or any(marker in text for marker in PLACEHOLDER_MARKERS):
                return True
    return False


def _fold(text: str) -> str:
    """Case-folded, punctuation-free, script-agnostic form for substring comparison.

    str.isalnum() rather than a character allow-list. The Construction side wrote this as an
    allow-list twice and was wrong twice: the first version tokenised on Latin letters and
    exempted every CJK string, the second added CJK and exempted Cyrillic, Greek, Thai, Arabic,
    Hebrew and Devanagari. An allow-list protects only the scripts its author happened to think of.
    """
    return "".join(ch for ch in (text or "").casefold() if ch.isalnum())


def _load_enums(filename: str) -> dict:
    """Read the declared vocabularies out of the contract file rather than restating them.

    Restating them here would create the drift this project has already paid for: a checker that
    invents its own field names is the defect it exists to prevent, and a vocabulary written in
    two places is a vocabulary that will disagree with itself. Adding a state is now a contract
    edit, and the checker follows.
    """
    try:
        doc = json.loads((TEMPLATES / filename).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {key: value for key, value in _obj(doc.get("_enums")).items()
            if isinstance(value, list) and all(isinstance(v, str) for v in value)}


# Resolved once at import. A missing or malformed template degrades the enum rules to silent
# rather than taking the other checks down with it, and main() says so instead of pretending.
CANDIDATE_ENUMS = _load_enums("destination-evaluation.json")
SHORTLIST_ENUMS = _load_enums("discovery-shortlist.json")


def _enum_error(where: str, field: str, value: object, allowed: list[str]) -> str:
    return (f"{where} {field} is {value!r}, which is not one of {', '.join(allowed)}. "
            f"The vocabulary is closed and declared in templates/; a value outside it is read as "
            f"'not that state' by every rule keyed on it, so a typo silently switches them off.")


def _surfaces(categories) -> set[str]:
    return {"arrival_transport" if c in ARRIVAL_SURFACE else str(c)
            for c in _seq(categories) if isinstance(c, str)}


def _priced(candidate: dict) -> bool:
    cost = _obj(candidate.get("cost_estimate"))
    return _number(cost.get("total_low")) is not None or _number(cost.get("total_high")) is not None


def _name(candidate: dict) -> str:
    return str(_obj(candidate.get("destination")).get("name") or "(unnamed candidate)")


# --------------------------------------------------------------------------------------------
# Where the rule is written
# --------------------------------------------------------------------------------------------
# 43 places this file can refuse a shortlist, and until this change not one of them named the
# reference that states the rule. The file's own opening paragraph is the argument for fixing it:
# "every rule about comparability, evidence and the hard-filter ordering lived in sentences, which
# is the exact configuration this project has learned fails silently." Turning those sentences
# into gates was half the job. The other half is that a run which trips a gate has to be able to
# find the sentence again -- otherwise the knowledge is enforced but unreadable, and a model on a
# non-Claude-Code CLI that never opened decision-and-research.md is told its shortlist is wrong
# with no way to learn what right looks like.
#
# Every entry is read off the check that emits it, not off SKILL.md. Two of these checks say in
# their own docstrings that they exist because SKILL.md stated a rule nothing read
# (check_cost_scope_identity, check_scored_candidates_carry_evidence) -- so SKILL.md is precisely
# the wrong place to have looked up where a rule lives.
#
# Anchors resolve to `<a id="...">` markers added to the reference files in this same change, and
# tests/test_packaging.py fails the build if any anchor a gate can emit does not exist.
CHECK_REFERENCES: dict[str, str] = {
    # The comparability rules are all one rule stated once, in step 4 of the evaluation sequence:
    # the same party size, dates/season, night count, category scope and currency. A category
    # vocabulary that drifts into free text, a per-person figure ranked against a party total, and
    # a flight-only figure ranked against an all-in one are three ways to break that single line.
    "check_cost_category_vocabulary": "decision-and-research.md#evaluation-sequence",
    "check_cost_comparable": "decision-and-research.md#evaluation-sequence",
    "check_cost_scope_identity": "decision-and-research.md#evaluation-sequence",
    # The hard filter runs before scoring, and an empty feasible set is an outcome rather than a
    # scoring error. A winner that fails a constraint, a record claiming it passed while naming
    # what it failed, and a declared conflict the pool does not support are all that ordering
    # broken from a different side.
    "check_no_infeasible_winner": "decision-and-research.md#evaluation-sequence",
    "check_status_contradicts_its_own_failures": "decision-and-research.md#evaluation-sequence",
    "check_conflict_agrees_with_the_pool": "decision-and-research.md#evaluation-sequence",
    "check_budget_fit_is_computed": "decision-and-research.md#evaluation-sequence",
    "check_constraint_coverage": "decision-and-research.md#evaluation-sequence",
    # Prices and access dates are the volatile-source rules: verify live, record the access date
    # beside the travel date range.
    "check_price_figures_are_current": "decision-and-research.md#evidence-policy",
    # What each finalist owes the traveller -- sources and access date, and an exclusion that says
    # why it was dropped rather than that it scored lower.
    "check_scored_candidates_carry_evidence": "decision-and-research.md#candidate-output-contract",
    "check_settled_status_has_its_reason": "decision-and-research.md#candidate-output-contract",
    "check_declared_enums": "decision-and-research.md#candidate-output-contract",
}


def cites(check):
    """Stamp every finding a check appends with the reference that states the rule it enforces.

    Same decorator as check_plan_consistency.py's, and deliberately a copy rather than an import.
    Sharing it would mean a new `scripts/*.py` module, and tests/test_packaging.py fails any
    script absent from BOTH READMEs -- so a shared helper would either ship undocumented or drag
    two README edits into a change that has nothing to say to a reader of either. The registry
    above is per-script anyway: these are this gate's rules and nowhere else's.

    Appends, never prepends: tests/test_shortlist_consistency.py matches needles as substrings of
    the whole output (`needle not in out`), and many are the opening words of a message.
    """
    suffix = CHECK_REFERENCES.get(check.__name__)
    suffix = f" [see references/{suffix}]" if suffix else None

    @functools.wraps(check)
    def cited(*args, **kwargs):
        if suffix is None:
            return check(*args, **kwargs)
        errors = args[1]
        before = len(errors)
        result = check(*args, **kwargs)
        for index in range(before, len(errors)):
            if " [see references/" not in errors[index]:
                errors[index] += suffix
        return result

    return cited


@cites
def check_cost_category_vocabulary(doc: dict, errors: list[str], notes: list[str]) -> None:
    """Free text makes every set comparison lie in both directions.

    'flights' and 'flight' are one scope that the identity check below would report as two, and a
    homemade category nobody else writes silently satisfies any rule that only compares sets. The
    vocabulary is imported from the Construction side rather than re-listed here, so one word
    means one thing in both halves of the skill.
    """
    allowed = set(BUDGET_CATEGORIES)
    context = _obj(doc.get("trip_context"))
    places = [("trip_context.budget_scope", context.get("budget_scope"))]
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        cost = _obj(candidate.get("cost_estimate"))
        places.append((f"candidates[{index}].trip_context.budget_scope",
                       _obj(candidate.get("trip_context")).get("budget_scope")))
        places.append((f"candidates[{index}].cost_estimate.included_categories",
                       cost.get("included_categories")))
        for field in ("not_applicable_categories", "unverified_categories"):
            for entry in _seq(cost.get(field)):
                places.append((f"candidates[{index}].cost_estimate.{field}",
                               [_obj(entry).get("category")]))
    for pointer, value in places:
        if value is None:
            continue
        unknown = {str(c) for c in _seq(value) if isinstance(c, str)} - allowed
        if unknown:
            errors.append(
                f"{pointer} uses categories outside the shared vocabulary: "
                f"{', '.join(sorted(unknown))}. Use the same names the Construction budget uses "
                f"({', '.join(sorted(allowed))}), or a set comparison between two candidates "
                f"compares spellings instead of scopes.")


@cites
def check_cost_comparable(doc: dict, errors: list[str], notes: list[str]) -> None:
    """One figure per person beside another for the whole party is a ranking, not a comparison.

    The traveller is shown two totals, picks the smaller, and the smaller one was priced for one
    person while the other was priced for two. Nothing inside either record is wrong; only the
    pair is. So the basis travels with the figure rather than being declared once at the top --
    a single shared declaration cannot be contradicted by anything, and a figure priced on a
    different basis lands under it with no field able to disagree.

    Deliberately NOT checked: nights, origin and date_range. A candidate reached by night train
    sleeps three hotel nights inside a four-night window and prices three, correctly -- the
    Construction half of this skill already says a departure day is a checkout rather than an
    extra night. A rule that failed that candidate would force the author either to price a night
    nobody sleeps in or to demote a perfectly rankable destination, and date_range is free text
    besides.
    """
    context = _obj(doc.get("trip_context"))
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        cost = _obj(candidate.get("cost_estimate"))
        where = f"candidates[{index}] ({_name(candidate)})"
        if not _priced(candidate):
            # An unpriced candidate is a legitimate output -- it was not researched that far --
            # but it must say so, or "no number" is indistinguishable from "nobody looked".
            if _missing(cost.get("not_priced_reason")):
                errors.append(
                    f"{where} shows no cost range and no cost_estimate.not_priced_reason. Say why "
                    f"it is unpriced; an absent figure otherwise reads as an oversight, and the "
                    f"traveller cannot tell it apart from a candidate nobody costed.")
            continue
        basis = str(cost.get("cost_basis") or "").strip()
        if basis != "per_person":
            errors.append(
                f"{where} carries a cost range with cost_basis {basis or 'unset'!r}. Every "
                f"comparable figure in a shortlist is per person -- show a party total only as a "
                f"separately named derived field. Without the basis beside the number, two "
                f"candidates priced differently look like two prices for the same thing.")
        own = _obj(candidate.get("trip_context"))
        for field in ("currency", "party_size"):
            shared, mine = context.get(field), own.get(field)
            if mine is not None and shared is not None and mine != shared:
                errors.append(
                    f"{where} prices in {field}={mine!r} while the shortlist's trip_context says "
                    f"{shared!r}. Two figures on different {field} bases cannot be ranked against "
                    f"each other, and the page shows them side by side.")
        low, high = _number(cost.get("total_low")), _number(cost.get("total_high"))
        if low is not None and high is not None and low > high:
            errors.append(f"{where} cost_estimate.total_low {low} exceeds total_high {high}.")


@cites
def check_cost_scope_identity(doc: dict, errors: list[str], notes: list[str]) -> None:
    """SKILL.md's own sentence, made enforceable: do not compare a flight-only figure with an
    all-in figure.

    The traveller reads 'Fixture Coast EUR 780' beside 'Fixture Harbour EUR 2,400', picks the
    first, and the first covered flights while the second covered everything. Both records are
    internally consistent; the comparison is the lie.

    A category a candidate genuinely cannot incur is declared rather than dropped, because a
    silently absent category is indistinguishable from one nobody priced. Two declared buckets,
    reusing the word the Construction budget already uses for the second: not_applicable (cannot
    incur it) and unverified (can incur it, but the price could not be sourced).
    """
    context = _obj(doc.get("trip_context"))
    basis = context.get("budget_scope")
    if basis is None:
        errors.append(
            "trip_context.budget_scope is missing, so no candidate's cost scope can be checked "
            "against anything. It is the declaration that makes two figures comparable.")
        return
    basis_surfaces = _surfaces(basis)
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        if not _priced(candidate):
            continue
        cost = _obj(candidate.get("cost_estimate"))
        where = f"candidates[{index}] ({_name(candidate)})"
        declared = _surfaces(cost.get("included_categories"))
        for field in ("not_applicable_categories", "unverified_categories"):
            for entry in _seq(cost.get(field)):
                entry = _obj(entry)
                declared |= _surfaces([entry.get("category")])
                if _missing(entry.get("reason")):
                    errors.append(
                        f"{where} lists {entry.get('category')!r} under {field} with no reason. "
                        f"The reason is the whole content of the claim -- without it the field is "
                        f"a way to switch this check off rather than to answer it.")
        missing = basis_surfaces - declared
        extra = declared - basis_surfaces
        if missing:
            errors.append(
                f"{where} prices {sorted(declared)} while the shortlist compares on "
                f"{sorted(basis_surfaces)}; it says nothing about {sorted(missing)}. Either price "
                f"it, or declare it in not_applicable_categories or unverified_categories with a "
                f"reason. A silently absent category is indistinguishable from an unpriced one, "
                f"and its figure still gets ranked against candidates that did include it.")
        if extra:
            errors.append(
                f"{where} prices {sorted(extra)}, which the shortlist's budget_scope does not "
                f"include. Its total is therefore larger than every candidate it is compared "
                f"against, for a reason the traveller cannot see.")
        own_scope = _obj(candidate.get("trip_context")).get("budget_scope")
        if own_scope is not None and _surfaces(own_scope) != basis_surfaces:
            errors.append(
                f"{where} carries its own trip_context.budget_scope {sorted(_surfaces(own_scope))} "
                f"differing from the shortlist's {sorted(basis_surfaces)}. A per-candidate copy "
                f"that drifts is the same scope swap arriving through a second door.")


@cites
def check_status_contradicts_its_own_failures(doc: dict, errors: list[str], notes: list[str]) -> None:
    """A record that says 'passed' while its own failed_constraints names what it failed.

    The two fields drift apart when a candidate is re-evaluated and only one is updated, and the
    verdict is what every downstream reader trusts. Only the unambiguous contradiction is checked
    -- a positive claim against a positive claim -- so no escape hatch is needed and silence is
    never treated as failure.
    """
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        eligibility = _obj(candidate.get("eligibility"))
        status = str(eligibility.get("hard_filter_status") or "").strip().casefold()
        failed = [f for f in _seq(eligibility.get("failed_constraints")) if f]
        if status in PASSING_STATUSES and failed:
            errors.append(
                f"candidates[{index}] ({_name(candidate)}) is marked {status!r} while its own "
                f"failed_constraints still names: {'; '.join(str(f) for f in failed)}. One of the "
                f"two is stale, and every reader downstream believes the status.")


@cites
def check_no_infeasible_winner(doc: dict, errors: list[str], notes: list[str]) -> None:
    """A destination that fails a hard constraint cannot win because it scored well.

    Two symmetric wrong answers, and this catches both. Forward: a winner whose own record carries
    a failed constraint, or whose hard filter was never run -- the traveller books flights for a
    trip whose entry or dates do not work. Backward: every candidate failed and the shortlist
    still leads with a winner, laundering an empty feasible set into a ranking. SKILL.md calls the
    empty set an outcome rather than a scoring error; this is that sentence with teeth.

    Matched by exact name equality, the way route segments already match stops_in_order, because
    a fuzzy match here would either miss a real winner or invent one.
    """
    candidates = [_obj(c) for c in _seq(doc.get("candidates"))]
    by_name = {_name(c): c for c in candidates}
    recommendation = _obj(doc.get("recommendation"))
    # No early return on an empty candidate list. That guard was added for safety and created the
    # loudest version of the very defect this check exists for: a shortlist naming a winner while
    # carrying no candidates at all passed silently, because the loop below had nothing to
    # iterate. An empty pool with a winner is a recommendation with no evidence under it.
    if not candidates and not _missing(recommendation.get("winner")):
        errors.append(
            f"recommendation.winner names {recommendation.get('winner')!r} while the shortlist "
            f"carries no candidates at all. There is nothing behind the recommendation -- no "
            f"cost, no eligibility, no evidence the traveller can check.")
        return
    if not candidates:
        return

    for role in ("winner", "runner_up"):
        named = recommendation.get(role)
        if _missing(named):
            continue
        candidate = by_name.get(str(named).strip())
        if candidate is None:
            errors.append(
                f"recommendation.{role} names {named!r}, which is not the destination.name of any "
                f"candidate. The recommendation and the evidence for it have come apart.")
            continue
        eligibility = _obj(candidate.get("eligibility"))
        status = str(eligibility.get("hard_filter_status") or "").strip().casefold()
        failed = [f for f in _seq(eligibility.get("failed_constraints")) if f]
        if failed:
            errors.append(
                f"recommendation.{role} is {named!r}, whose record fails: "
                f"{'; '.join(str(f) for f in failed)}. A hard constraint is not a low score to be "
                f"outweighed -- present it as infeasible, or say which constraint the traveller "
                f"agreed to relax.")
        if status in ("", "unknown"):
            errors.append(
                f"recommendation.{role} is {named!r} while its hard_filter_status is "
                f"{status or 'unset'!r}. 'Unknown' means nobody established it can be entered, "
                f"reached or afforded, and it is being presented as the best option. Run the "
                f"filter or say plainly that this one is unverified.")

    # A failing candidate may still be shown -- SKILL.md allows "possible if X changes" -- but it
    # must say what would have to change. Scored and ranked beside feasible options with nothing
    # said, it reads as a normal choice, which is the disguise the whole section forbids.
    # This is also what keeps conditional_on_relaxation from being a field nobody reads: the
    # contract carried primary_map_exception_reason unread for three versions on the other side
    # of this skill, and an unenforced field is one the next run is free to leave blank.
    #
    # Silent under a declared constraint conflict, and that narrowing was earned rather than
    # assumed: the first version fired on every candidate of an honestly reported conflict, where
    # all of them failing IS the finding and outcome.minimum_relaxation already answers "what
    # would have to change" once for the whole document. Asking each candidate to repeat it is the
    # ceremony that teaches people to route a check around.
    declared_conflict = str(_obj(doc.get("outcome")).get("state") or "").strip() == "constraint_conflict"
    conditional_names = {_fold(str(_obj(o).get("destination") or ""))
                         for o in _seq(doc.get("conditional_options"))}
    for index, candidate in enumerate([] if declared_conflict else candidates):
        eligibility = _obj(candidate.get("eligibility"))
        if not [f for f in _seq(eligibility.get("failed_constraints")) if f]:
            continue
        if _number(_obj(candidate.get("fit")).get("score")) is None:
            continue
        declared = (not _missing(_obj(candidate.get("fit")).get("conditional_on_relaxation"))
                    or _fold(_name(candidate)) in conditional_names)
        if not declared:
            errors.append(
                f"candidates[{index}] ({_name(candidate)}) fails a hard constraint and still "
                f"carries a score, with nothing saying it is conditional. Name what would have to "
                f"change in fit.conditional_on_relaxation, or list it under conditional_options; "
                f"ranked silently beside feasible candidates it reads as an ordinary choice.")

    feasible = [c for c in candidates
                if str(_obj(c.get("eligibility")).get("hard_filter_status") or "").strip().casefold()
                in PASSING_STATUSES]
    if not feasible and not _missing(recommendation.get("winner")):
        errors.append(
            "no candidate passed the hard filters, yet the shortlist still names a winner. An "
            "empty feasible set is an outcome, not a scoring error: report the constraint "
            "conflict and the smallest relaxation that would restore feasibility, and keep any "
            "alternative explicitly conditional.")


@cites
def check_declared_enums(doc: dict, errors: list[str], notes: list[str]) -> None:
    """Every closed vocabulary, checked against the contract that declares it.

    A status outside its enum is worse than a wrong status, because every rule keyed on it reads
    the unknown value as 'not that state' and quietly stops firing. `feasible` instead of
    `passed` is not a near miss: it turns off the winner check, the conflict check and the
    coverage check at once, and nothing reports that they were turned off.
    """
    if not CANDIDATE_ENUMS or not SHORTLIST_ENUMS:
        notes.append("note: enum vocabularies could not be read from templates/; enum rules did "
                     "not run. Restore templates/destination-evaluation.json and "
                     "templates/discovery-shortlist.json.")
        return
    state = _obj(doc.get("outcome")).get("state")
    allowed_states = SHORTLIST_ENUMS.get("outcome_state", [])
    if _missing(state):
        errors.append(
            "outcome.state is missing. It is required on every Discovery artifact, and not "
            "because bookkeeping is nice: every rule about constraint conflicts keys on it, so "
            "omitting the field is the escape from all of them at once. Declare "
            f"{' | '.join(allowed_states)}.")
    elif allowed_states and str(state).strip() not in allowed_states:
        errors.append(_enum_error("outcome", "state", state, allowed_states))

    fields = (("eligibility", "hard_filter_status"), ("cost_estimate", "budget_fit"),
              ("cost_estimate", "price_confidence"))
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        where = f"candidates[{index}] ({_name(candidate)})"
        for block, field in fields:
            allowed = CANDIDATE_ENUMS.get(field, [])
            value = _obj(candidate.get(block)).get(field)
            if allowed and value is not None and str(value).strip() not in allowed:
                errors.append(_enum_error(where, f"{block}.{field}", value, allowed))
        for field in ("research_status", "recommendation_state"):
            allowed = CANDIDATE_ENUMS.get(field, [])
            value = candidate.get(field)
            if allowed and value is not None and str(value).strip() not in allowed:
                errors.append(_enum_error(where, field, value, allowed))


@cites
def check_settled_status_has_its_reason(doc: dict, errors: list[str], notes: list[str]) -> None:
    """`not_pursued` is a claim about what was deliberately skipped, so it owes a sentence.

    It exists to keep an honest research budget from looking like an unfinished filter: a
    candidate further from origin than three already over the cap need not be priced, and saying
    so is different from saying nobody looked. But an escape nobody has to justify is a way to
    switch a rule off rather than to answer it -- the same reason detour_reason and
    rating_below_floor_reason are checked for presence.
    """
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        eligibility = _obj(candidate.get("eligibility"))
        if str(eligibility.get("hard_filter_status") or "").strip() != "not_pursued":
            continue
        if _missing(eligibility.get("not_pursued_reason")):
            errors.append(
                f"candidates[{index}] ({_name(candidate)}) is marked not_pursued with no "
                f"not_pursued_reason. State what was skipped and why it could not change the "
                f"ranking; without it this is indistinguishable from a filter nobody finished.")


@cites
def check_budget_fit_is_computed(doc: dict, errors: list[str], notes: list[str]) -> None:
    """A verdict about money that was asserted rather than computed.

    A candidate that cleared the hard filters while its own cost block still says `unknown` was
    never measured against the cap it supposedly cleared. And the arithmetic half needs no join
    at all: a low estimate above the declared cap cannot be `within` or `tight`, whatever the
    author typed.

    Quiet on `over`, deliberately. An author correctly dropping a candidate on price should not
    owe a full researched range for it -- that is the research-a-rejected-candidate-twice cost
    the research budget exists to prevent.
    """
    cap = _number(_obj(doc.get("trip_context")).get("budget_cap_per_person"))
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        cost = _obj(candidate.get("cost_estimate"))
        where = f"candidates[{index}] ({_name(candidate)})"
        status = str(_obj(candidate.get("eligibility")).get("hard_filter_status") or "").strip()
        fit = str(cost.get("budget_fit") or "unknown").strip()
        if status in PASSING_STATUSES and fit in ("", "unknown"):
            if _missing(cost.get("budget_fit_unpriced_reason")):
                errors.append(
                    f"{where} passed the hard filters while its budget_fit is still 'unknown'. "
                    f"Budget is one of those filters, so it was either measured -- say within, "
                    f"tight or over -- or it was not, in which case the candidate did not pass "
                    f"it. Write budget_fit_unpriced_reason if this destination clears the money "
                    f"question without a researched range.")
        if fit in ("within", "tight"):
            missing = [f for f in ("total_low", "total_high", "as_of")
                       if _missing(cost.get(f)) and _number(cost.get(f)) is None]
            if not _seq(cost.get("included_categories")):
                missing.append("included_categories")
            if missing:
                errors.append(
                    f"{where} claims budget_fit {fit!r} while {', '.join(missing)} "
                    f"{'is' if len(missing) == 1 else 'are'} empty. That verdict is a comparison "
                    f"between a researched figure and the cap; without the figure it is an "
                    f"opinion wearing the word 'within'.")
            low = _number(cost.get("total_low"))
            if cap is not None and low is not None and low > cap:
                errors.append(
                    f"{where} says budget_fit {fit!r} while its own total_low {low} exceeds the "
                    f"declared cap {cap}. Pure arithmetic on two numbers the shortlist already "
                    f"carries -- the verdict contradicts them.")


@cites
def check_price_figures_are_current(doc: dict, errors: list[str], notes: list[str]) -> None:
    """A figure researched long before the comparison is not a figure about the same trip.

    Fares and lodging are the most volatile facts this skill handles. A candidate priced months
    before the others is ranked against them as if the two numbers meant the same thing, and the
    traveller cannot see the difference. Dates only -- no rate table, no conversion, nothing this
    check would have to guess at.
    """
    generated = str(doc.get("generated_at") or "")[:10]
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", generated):
        return
    document_day = dt.date.fromisoformat(generated)
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        if not _priced(candidate):
            continue
        cost = _obj(candidate.get("cost_estimate"))
        where = f"candidates[{index}] ({_name(candidate)})"
        as_of = str(cost.get("as_of") or "")[:10]
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", as_of):
            errors.append(
                f"{where} carries a cost range with no ISO as_of date. The date is what tells a "
                f"reader whether the figure is still true, and it is the first thing a comparison "
                f"between two candidates depends on.")
            continue
        if not _missing(cost.get("as_of_exception_reason")):
            continue
        priced_day = dt.date.fromisoformat(as_of)
        if priced_day > document_day:
            errors.append(
                f"{where} was priced {as_of}, after the shortlist's own generated_at {generated}. "
                f"One of the two dates is wrong, and staleness is judged by this field.")
        elif (document_day - priced_day).days > MAX_PRICE_AGE_DAYS:
            errors.append(
                f"{where} was priced {as_of}, {(document_day - priced_day).days} days before this "
                f"shortlist was written. Re-check it or say why it holds in "
                f"as_of_exception_reason -- a contracted fare or a fixed package legitimately "
                f"keeps its own date.")


@cites
def check_conflict_agrees_with_the_pool(doc: dict, errors: list[str], notes: list[str]) -> None:
    """Telling a traveller to give up a requirement is expensive, so the claim has to be earned.

    Two failures this catches, both of which end with the traveller changing real plans for
    nothing. A declared conflict while a candidate actually passed: something survived and the
    conflict is a story. And a conflict declared over a filter nobody finished -- an unfinished
    filter and a real conflict produce the same empty pass set, and the traveller is asked to
    relax a genuine requirement to escape the difference. That is what the `blocked` state is
    for, and why `unknown` is not allowed to stand in for either.

    Also the converse, which needs no new fields and is the more valuable half: every candidate
    failed and the artifact still calls itself a shortlist.
    """
    state = str(_obj(doc.get("outcome")).get("state") or "").strip()
    candidates = [_obj(c) for c in _seq(doc.get("candidates"))]
    outcome = _obj(doc.get("outcome"))
    statuses = [str(_obj(c.get("eligibility")).get("hard_filter_status") or "unknown").strip()
                for c in candidates]

    if state == "constraint_conflict":
        survivors = [_name(c) for c, s in zip(candidates, statuses) if s in PASSING_STATUSES]
        if survivors:
            errors.append(
                f"outcome.state is 'constraint_conflict' while {', '.join(survivors)} "
                f"{'is' if len(survivors) == 1 else 'are'} marked passed. Something survived, so "
                f"there is no conflict to report -- present the survivor.")
        unfinished = [_name(c) for c, s in zip(candidates, statuses) if s in ("", "unknown")]
        if unfinished:
            errors.append(
                f"outcome.state is 'constraint_conflict' while the filter never settled "
                f"{', '.join(unfinished)}. An unfinished filter and a real conflict produce the "
                f"same empty pass set; only one of them justifies asking the traveller to give up "
                f"a requirement. Finish those, mark them not_pursued with a reason, or use "
                f"outcome.state 'blocked' with a blocking_fact.")
        if not _missing(_obj(doc.get("recommendation")).get("winner")):
            errors.append(
                "outcome.state is 'constraint_conflict' but recommendation.winner still names a "
                "destination. A conditional option belongs in conditional_options -- an offer is "
                "not a recommendation.")
        if not _seq(outcome.get("blocking_constraints")):
            errors.append(
                "outcome.state is 'constraint_conflict' with no outcome.blocking_constraints. "
                "Name the smallest conflicting set; 'nothing works' is not something a traveller "
                "can act on.")
        if _missing(outcome.get("minimum_relaxation")):
            errors.append(
                "outcome.state is 'constraint_conflict' with no outcome.minimum_relaxation. Say "
                "which single constraint, relaxed, most likely restores feasibility.")
        # Every adjudicated rejection must trace to a constraint the conflict actually claims,
        # or the traveller is asked to relax something that removed hardly any of the pool.
        claimed = {_fold(c) for c in _seq(outcome.get("blocking_constraints")) if isinstance(c, str)}
        if claimed:
            cited: list[str] = []
            for candidate in candidates:
                cited += [str(f) for f in _seq(_obj(candidate.get("eligibility")).get("failed_constraints"))]
            for entry in _seq(doc.get("excluded")):
                value = _obj(entry).get("failed_constraint")
                if isinstance(value, str) and value.strip():
                    cited.append(value)
            orphans = sorted({c for c in cited
                              if not any(claim in _fold(c) or _fold(c) in claim for claim in claimed)})
            if orphans:
                errors.append(
                    "these rejections name constraints the declared conflict does not claim: "
                    + "; ".join(orphans)
                    + ". Either add them to outcome.blocking_constraints or the traveller is "
                      "being asked to relax a constraint that removed only part of the pool.")

    if state == "blocked" and _missing(outcome.get("blocking_fact")):
        errors.append(
            "outcome.state is 'blocked' with no outcome.blocking_fact. Name what could not be "
            "established; 'blocked' without it is indistinguishable from giving up.")

    if state == "shortlist" and candidates and all(s == "failed" for s in statuses):
        errors.append(
            "every candidate is marked failed while outcome.state is 'shortlist'. An empty "
            "feasible set is an outcome, not a scoring error: declare 'constraint_conflict' and "
            "name what to relax.")


CLIMATE_SENTINELS = ("无特别气候限制", "no particular climate", "none")


def constraint_roster(intake: dict) -> list[tuple[str, str]]:
    """The hard constraints the traveller actually declared, computed from their saved intake.

    Computed rather than authored, and that is the whole design. A roster written into the
    shortlist can be under-declared: the author lists the four constraints they remembered to
    apply, every candidate covers all four, and the gate reports full coverage on exactly the run
    that motivated it. An intake field the traveller filled is their declaration and nothing is
    inferred from it -- the id is the field path, and the text is theirs.

    Two hard constraints are deliberately absent. `destination_scope.excluded_places` is
    discharged once, before candidates are generated, so per-candidate bookkeeping about it proves
    nothing -- it gets a direct check instead. The travel window is a property of the run rather
    than of any candidate.
    """
    roster: list[tuple[str, str]] = []
    origin = _obj(intake.get("origin"))
    if not _missing(origin.get("max_one_way_travel_time")):
        roster.append(("origin.max_one_way_travel_time",
                       str(origin["max_one_way_travel_time"])))
    for index, need in enumerate(_seq(_obj(intake.get("party")).get("mobility_or_access_needs"))):
        if not _missing(need):
            roster.append((f"party.mobility_or_access_needs[{index}]", str(need)))
    feasibility = _obj(intake.get("feasibility"))
    for index, pref in enumerate(_seq(feasibility.get("climate_preferences"))):
        if _missing(pref) or any(s in str(pref) for s in CLIMATE_SENTINELS):
            continue
        roster.append((f"feasibility.climate_preferences[{index}]", str(pref)))
    for index, need in enumerate(_seq(feasibility.get("dietary_or_religious_needs"))):
        if not _missing(need):
            roster.append((f"feasibility.dietary_or_religious_needs[{index}]", str(need)))
    if _number(_obj(intake.get("budget")).get("hard_cap_amount")) is not None:
        roster.append(("budget.hard_cap_amount",
                       str(_obj(intake.get("budget")).get("hard_cap_amount"))))
    scope = str(_obj(intake.get("trip_geography")).get("scope") or "").strip()
    if scope and scope != "domestic":
        roster.append(("entry", f"entry feasibility (trip scope: {scope})"))
    return roster


def _declared_ids(bucket) -> set[str]:
    """Constraint ids named in one of the eligibility buckets.

    Objects carry `constraint_id`; a plain string is accepted and simply names no id, which is
    why coverage is reported against ids rather than text. Matching a computed field path against
    free prose would be exactly the fuzzy guess this project keeps removing.
    """
    found = set()
    for entry in _seq(bucket):
        if isinstance(entry, dict) and not _missing(entry.get("constraint_id")):
            found.add(str(entry["constraint_id"]).strip())
    return found


@cites
def check_constraint_coverage(doc: dict, errors: list[str], notes: list[str],
                              intake: dict | None = None) -> None:
    """Every constraint the traveller declared, answered for every candidate they are shown.

    The defect is a winner that passed the four constraints someone happened to think of and was
    never tested against the fifth -- the stated maximum journey time, or the walking limit. It
    survives to the top of the list carrying no failure, because nobody looked, and a record that
    is silent about a constraint is indistinguishable from one that cleared it.

    `not_applicable` is a separate bucket from `unresolved` on purpose. 'The constraint has no
    subject here' and 'nobody established it' are different statements, and conflating them makes
    the rule fire on correct work -- an entry filter on a domestic candidate under a mixed-scope
    run is not an unanswered question.
    """
    if intake is None:
        return
    roster = constraint_roster(intake)
    if not roster:
        notes.append("note: the intake declares no hard constraints, so coverage is vacuous "
                     "here. That is a fact about the intake, not a pass.")
        return
    notes.append("note: constraints this shortlist is held to — "
                 + "; ".join(f"{cid} ({text})" for cid, text in roster))
    roster_ids = {cid for cid, _ in roster}
    buckets = ("confirmed_constraints", "failed_constraints", "unresolved_constraints",
               "not_applicable_constraints")
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        eligibility = _obj(candidate.get("eligibility"))
        where = f"candidates[{index}] ({_name(candidate)})"
        seen: dict[str, list[str]] = {}
        for bucket in buckets:
            for cid in _declared_ids(eligibility.get(bucket)):
                seen.setdefault(cid, []).append(bucket)
        for cid, found_in in sorted(seen.items()):
            if len(found_in) > 1:
                errors.append(
                    f"{where} answers constraint {cid!r} in more than one bucket "
                    f"({', '.join(found_in)}). One verdict per constraint, or the record says two "
                    f"different things and every reader picks the one it reads first.")
        missing = sorted(roster_ids - set(seen))
        if missing:
            errors.append(
                f"{where} says nothing about {', '.join(missing)}. The traveller declared "
                f"{'it' if len(missing) == 1 else 'them'} in their intake, and a candidate silent "
                f"about a constraint is indistinguishable from one that cleared it. Put each in "
                f"confirmed, failed, unresolved or not_applicable_constraints.")
        for entry in _seq(eligibility.get("not_applicable_constraints")):
            entry = _obj(entry)
            if not _missing(entry.get("constraint_id")) and _missing(entry.get("reason")):
                errors.append(
                    f"{where} marks {entry.get('constraint_id')!r} not applicable with no reason. "
                    f"The reason is the claim; without it the bucket is a way to switch coverage "
                    f"off rather than to answer it.")
        extra = sorted(set(seen) - roster_ids)
        if extra:
            notes.append(f"note: {where} records constraints the intake never declared: "
                         f"{', '.join(extra)}. Not an error -- a candidate may honestly carry one.")

    # The exclusion list is discharged once, before generation, so check the thing itself rather
    # than the bookkeeping: no candidate and no exclusion-log entry may name an excluded place.
    excluded_places = [str(p) for p in
                       _seq(_obj(intake.get("destination_scope")).get("excluded_places"))
                       if isinstance(p, str) and p.strip()]
    if excluded_places:
        folded = {(_fold(p), p) for p in excluded_places}
        offered = [(_name(_obj(c)), "candidates") for c in _seq(doc.get("candidates"))]
        offered += [(str(_obj(e).get("destination") or ""), "excluded")
                    for e in _seq(doc.get("excluded"))]
        for name, where in offered:
            for folded_place, original in folded:
                if folded_place and folded_place in _fold(name):
                    errors.append(
                        f"{where} names {name!r}, which the traveller excluded ({original!r}). "
                        f"An excluded place is a hard filter applied before candidates are "
                        f"generated, so it should never have reached the list at all.")



@cites
def check_scored_candidates_carry_evidence(doc: dict, errors: list[str], notes: list[str]) -> None:
    """SKILL.md step 5 says "score only candidates with sufficient evidence". Nothing read it.

    Measured: nothing in this file ever touched `candidate.evidence`, so a candidate could carry
    `fit.score: 82`, be named `recommendation.winner`, and hold `evidence: []` -- a destination
    recommended to a traveller with no stated source under it, passing every gate. A score is a
    claim about research that happened; an empty evidence list says it did not.

    Bound to what the shortlist actually asserts, so it cannot fire on honest work in progress: a
    candidate is only held to this once it is scored or recommended. `research_status: not_started`
    or `partial` with no score is a candidate still being worked on, and saying so is the opposite
    of the defect. Each entry must also carry the three things that make it checkable by someone
    else -- what was claimed, where it came from, and when it was read -- because an evidence list
    of bare sentences is the same "trust me" the score already was.
    """
    recommended = {str(_obj(doc.get("recommendation")).get(role) or "").strip()
                   for role in ("winner", "runner_up")} - {""}
    for index, candidate in enumerate(_seq(doc.get("candidates"))):
        candidate = _obj(candidate)
        name = str(_obj(candidate.get("destination")).get("name") or "").strip()
        where = f"candidates[{index}] ({name or 'unnamed'})"
        scored = _number(_obj(candidate.get("fit")).get("score")) is not None
        if not scored and name not in recommended:
            continue
        why = "is scored" if scored else "is recommended"
        entries = [_obj(e) for e in _seq(candidate.get("evidence"))]
        if not entries:
            errors.append(
                f"{where} {why} but carries no evidence. Step 5 of the discovery pipeline scores "
                f"only candidates with sufficient evidence, so a score with an empty evidence list "
                f"is a number nobody can check -- research it, or drop the score and say the "
                f"research is partial.")
            continue
        for position, entry in enumerate(entries, 1):
            missing = [field for field in ("claim", "source_url", "accessed_on")
                       if _missing(entry.get(field))]
            if missing:
                errors.append(
                    f"{where} evidence[{position - 1}] is missing {', '.join(missing)}. An "
                    f"evidence entry has to say what was claimed, where it came from and when it "
                    f"was read, or the reader cannot tell a checked fact from a remembered one.")
            url = str(entry.get("source_url") or "")
            if url and not url.startswith("https://"):
                errors.append(
                    f"{where} evidence[{position - 1}].source_url is not HTTPS: {url}")

SHORTLIST_CHECKS = (
    check_declared_enums,
    check_cost_category_vocabulary,
    check_cost_comparable,
    check_cost_scope_identity,
    check_price_figures_are_current,
    check_budget_fit_is_computed,
    check_settled_status_has_its_reason,
    check_status_contradicts_its_own_failures,
    check_no_infeasible_winner,
    check_conflict_agrees_with_the_pool,
    check_scored_candidates_carry_evidence,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("shortlist", help="Discovery shortlist JSON path")
    parser.add_argument(
        "--intake", default=None,
        help="Saved trip intake JSON. Supplying it computes the hard-constraint roster from what "
             "the traveller actually declared and requires every candidate to answer each one.")
    parser.add_argument(
        "--no-intake", action="store_true",
        help="Run without the constraint-coverage check, when no saved intake exists. Records the "
             "gap loudly instead of leaving a silent exit 0.")
    args = parser.parse_args()
    # Same shape as save_trip_deliverables.py's --verification/--unverified pair, and for the same
    # reason. Omitting --intake used to print an accurate note and exit 0, and an exit 0 is what an
    # assistant reads -- so the one check that catches a winner never tested against a constraint
    # the traveller stated was skippable by saying nothing. The escape hatch stays, because a gate
    # people route around warns nobody, but it costs visibility rather than silence.
    if not args.intake and not args.no_intake:
        print(
            "ERROR: No --intake. Pass the saved intake JSON "
            "(<workspace>/plans/intake-<stamp>-<slug>.json) so the hard-constraint roster is "
            "computed from what the traveller actually declared, or pass --no-intake to run "
            "without it and record the gap. Without it, the check that catches a winner never "
            "tested against a stated constraint does not run at all, and a roster written by hand "
            "into the shortlist reports full coverage on exactly the run that motivated it.",
            file=sys.stderr)
        return 1
    try:
        doc = json.loads(Path(args.shortlist).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR: Could not read shortlist JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(doc, dict):
        print("ERROR: shortlist JSON must be an object.", file=sys.stderr)
        return 2
    intake = None
    if args.intake:
        try:
            intake = json.loads(Path(args.intake).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"ERROR: Could not read intake JSON: {exc}", file=sys.stderr)
            return 2
        if not isinstance(intake, dict):
            print("ERROR: intake JSON must be an object.", file=sys.stderr)
            return 2

    errors: list[str] = []
    notes: list[str] = []
    for check in SHORTLIST_CHECKS:
        check(doc, errors, notes)
    check_constraint_coverage(doc, errors, notes, intake=intake)
    if intake is None:
        notes.append("NO INTAKE: constraint coverage did not run. This shortlist has NOT been "
                     "tested against the hard constraints the traveller stated -- say so when you "
                     "present it, and do not describe a winner as having cleared their "
                     "requirements. Pass the saved intake to arm the check.")
    for note in notes:
        print(f"note: {note}")
    if errors:
        print("SHORTLIST CONSISTENCY FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    count = len(_seq(doc.get("candidates")))
    print(f"shortlist consistent: {count} candidate(s) checked against a shared comparison basis")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
