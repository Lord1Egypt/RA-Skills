#!/usr/bin/env python3
"""Every wrong field name in the plan, in one pass, with the name it was probably meant to be.

Usage: python check_plan_contract.py <plan.json> [--json]

WHY THIS EXISTS, measured on one real Construction run. Building a plan by hand cost thirteen
round trips to the gates, and not one of them was about the trip: they were field names.
`total_duration_minutes` for `duration_minutes`. `url` for `search_url`. `provider` for
`platform`. `amount_low` for `per_person_low`. `total_low` for `estimated_per_person_low`.
`day_number` for `planned_day`. An `outbound_itinerary` written as a sentence where the contract
wants an object of six fields.

Each one cost a full cycle -- edit, run the gate, read a fresh batch of errors -- because the
gates validate by subject and stop at the first category that fails, which is right for THEM: a
plan whose budget does not add up should not also be lectured about map links. It is wrong for the
author, who could have fixed all thirteen in one edit if anything had told them all thirteen.

So this is not a gate. It answers one question the gates deliberately do not: **is every key in
this document a key the contract knows?** It runs before them, costs no network, and its output is
a worklist rather than a verdict. A misspelling is nearly always a near-miss, so each unknown key
is reported with the closest contract key -- "you wrote X, the contract says Y" is a fix; "unknown
key X" is a search.

WHAT IT DOES NOT DO. It knows nothing about whether the plan is true, feasible, or internally
consistent -- `check_plan_consistency.py` owns all of that and this file must never grow into it.
It also cannot tell a typo from a field somebody added on purpose, so an unrecognised key is
reported as a question, not an error, and the keys the skill's own scripts write are known to it.
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CONTRACT = SCRIPT_DIR.parent / "templates" / "final-trip-plan.json"

# Written by the skill's own scripts after the author is finished, so they are not typos and not
# the author's business. Named rather than pattern-matched, because "ends in _sidecar" would also
# excuse the next misspelling that happens to.
ADDED_BY_SCRIPTS = {
    "gates_passed",            # check_plan_consistency.gates_stamp, via save_trip_deliverables
    "verification_receipt",    # save_trip_deliverables, on a verified save
    "imagery",                 # fetch_plan_imagery, pre-sidecar plans
    "imagery_sidecar",         # fetch_plan_imagery
    "replan_context",          # replan_trip
    "provenance",              # reserved for replan provenance
    "trip.traveler_constraints.untyped_constraints",  # new_plan_skeleton
    "_contract",               # the template's own explanatory block
}


def shapes(node: object, path: str = "") -> dict[str, set[str]]:
    """Map every key path in the contract to the JSON types seen there.

    Lists collapse to their first element: the contract carries one specimen per array, and every
    later element is the same shape. Recording the specimen once is what lets `days[3].route` and
    `days[0].route` be the same rule.
    """
    found: dict[str, set[str]] = {}
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else key
            found.setdefault(child, set()).add(kind(value))
            for sub, kinds in shapes(value, child).items():
                found.setdefault(sub, set()).update(kinds)
    elif isinstance(node, list):
        # An EMPTY array in the contract carries no specimen, so it declares that the key exists
        # and nothing about what goes inside it. Reporting its contents as unknown was this
        # script's own first false-positive class: `avoid_list_handling`, `unmet_preferences` and
        # `comparison_searches` are all shipped empty, and every field the author correctly wrote
        # inside them came back as a misspelling. A path with no specimen is marked open, and
        # everything under it is left alone.
        if node:
            for sub, kinds in shapes(node[0], f"{path}[]").items():
                found.setdefault(sub, set()).update(kinds)
        else:
            found.setdefault(f"{path}[]", set()).add("open")
    return found


# Documented as "one object, or a list of them for a multi-city trip" (SKILL.md), and accepted in
# both forms by check_plan_consistency. The template can carry only one specimen, so the list form
# is declared here rather than reported as a type error -- which is what the checker did to every
# multi-city plan written the way SKILL.md says to write it.
OBJECT_OR_LIST = ("trip.destination_coords",)


def contract_shapes(template: dict) -> dict[str, set[str]]:
    """shapes(), plus the list form of every key that may be one object or a list of them."""
    known = shapes(template)
    for path in OBJECT_OR_LIST:
        known.setdefault(path, set()).add("list")
        for sub in [k for k in list(known) if k.startswith(path + ".")]:
            known[path + "[]" + sub[len(path):]] = set(known[sub])
    return known


def kind(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _ancestors(path: str) -> list[str]:
    """Every prefix of a dotted path, so an open subtree can excuse everything under it."""
    parts = path.split(".")
    return [".".join(parts[:i]) for i in range(1, len(parts))]


def walk(node: object, known: dict[str, set[str]], path: str = "") -> list[dict]:
    """Every key in the plan the contract does not know, and every one whose type it does not."""
    issues: list[dict] = []
    if isinstance(node, dict):
        for key, value in node.items():
            child = f"{path}.{key}" if path else key
            plain = child.replace("[]", "")
            if plain in ADDED_BY_SCRIPTS or child in ADDED_BY_SCRIPTS:
                continue
            if child not in known:
                # Both spellings, because an ancestor may already end in `[]`: the prefixes of
                # `…avoid_list_handling[].item` include `…avoid_list_handling[]`, and appending
                # another `[]` looked for a key that cannot exist. The open subtree was recorded
                # correctly and then never found, so every field inside a contract-empty array was
                # still reported as a misspelling.
                if any(known.get(prefix) == {"open"} or known.get(f"{prefix}[]") == {"open"}
                       for prefix in _ancestors(child)):
                    continue          # inside an array the contract ships empty
                siblings = [k for k in known
                            if k.rsplit(".", 1)[0] == child.rsplit(".", 1)[0]]
                # Matched on the LEAF name, not the whole dotted path: every sibling shares the
                # same prefix, so comparing full paths scores them all alike and returns whichever
                # sorted first -- which is how `amount_low` was told it meant `note`.
                leaf = child.rsplit(".", 1)[-1]
                near = difflib.get_close_matches(
                    leaf, [k.rsplit(".", 1)[-1] for k in siblings], n=1, cutoff=0.45)
                match = next((k for k in siblings if k.rsplit(".", 1)[-1] == near[0]), None) \
                    if near else None
                issues.append({"path": child, "problem": "unknown key",
                               "suggestion": match, "found_type": kind(value)})
                continue
            # `null` is how the contract writes "not filled in yet", so it is compatible with
            # everything. A real type clash is a string where an object belongs -- the shape that
            # cost a round trip when outbound_itinerary was written as a sentence.
            allowed = known[child] - {"null"}
            actual = kind(value)
            if allowed and actual != "null" and actual not in allowed:
                issues.append({"path": child, "problem": "wrong type",
                               "expected_type": "/".join(sorted(allowed)),
                               "found_type": actual, "suggestion": None})
                continue
            issues.extend(walk(value, known, child))
    elif isinstance(node, list):
        for item in node:
            issues.extend(walk(item, known, f"{path}[]"))
    return issues



# ---------------------------------------------------------------------------------------------
# CLOSED VOCABULARIES, read from the renderer rather than restated here.
#
# WHY THIS WAS ADDED, measured on one real Construction run. This script printed "CONTRACT OK:
# every key in plan.json is one templates/final-trip-plan.json declares" -- and the very next
# command, render_final_trip_html.py, rejected the same file with **fourteen** findings. Every one
# of them was a closed enum's VALUE or a required field, not a key name: `plan_status`,
# `price_basis`, `ticket_status`, `price_status`, an anchor's `neighborhood_or_area`, the
# transport_overview map fields. So the author got two separate "here is everything at once"
# passes, which is the same round trip this file was written to delete, one level down.
#
# The values could not be learned from the template either: it writes free text as `null` on
# purpose, so `price_status`, `availability_status` and `ticket_status` all read as "no value" and
# teach nothing. A sibling template, destination-evaluation.json, carries an `_enums` block for
# exactly this reason; final-trip-plan.json had none.
#
# The vocabularies are IMPORTED, never copied. Two hand-maintained lists drift, and this
# repository has already paid for that once: a hand-written list of renderer-owned English strings
# went stale beside the renderer's own substitution table, and a Chinese page shipped carrying
# English. One definition, in the module that enforces it.
def _vocabularies() -> tuple[dict, str]:
    """(path -> allowed values, failure). A non-empty failure means the check could not run."""
    try:
        sys.path.insert(0, str(SCRIPT_DIR))
        import render_final_trip_html as renderer
    except Exception as exc:  # noqa: BLE001 - any import failure must be reported, not swallowed
        return {}, (f"could not import render_final_trip_html ({type(exc).__name__}: {exc}), so "
                    f"enum values were NOT checked. Fix the import rather than trusting this run.")
    booking = set(renderer.BOOKING_STATES)
    price = set(renderer.PRICE_STATUSES)
    avail = set(renderer.BOOKING_ACCESS_STATUSES)
    table = {
        "plan_status": booking,
        "intake_context.method": set(renderer.INTAKE_METHODS),
        "entry_context.status": set(renderer.ENTRY_STATUSES),
        "trip.arrival_transport_mode": set(renderer.ARRIVAL_MODES),
        "trip.traveler_constraints.allergy_severity": set(renderer.ALLERGY_SEVERITIES),
        "transport_preference.mode": set(renderer.TRANSPORT_MODES),
        "budget.calculation_basis": {"per_person"},
        "budget.breakdown[].category": set(renderer.BUDGET_CATEGORIES),
        "budget.breakdown[].price_status": price,
        "sources[].confidence": set(renderer.SOURCE_CONFIDENCE_LEVELS),
        "days[].day_type": set(renderer.DAY_TYPES),
        "days[].dining[].meal": set(renderer.MEAL_TYPES),
        "days[].dining[].reservation_need": set(renderer.RESERVATION_NEEDS),
        "days[].route.route_map_scope": set(renderer.ROUTE_MAP_SCOPES),
        "regional_service_context.google_services_access": {"available", "unavailable", "unknown"},
        "regional_service_context.booking_access_checks[].category":
            set(renderer.BOOKING_ACCESS_CATEGORIES),
        "regional_service_context.booking_access_checks[].access_status": avail,
        "booking_options.flights[].price_basis": {"per_person_round_trip"},
        "booking_options.ground_transport[].price_basis": {"per_person_round_trip"},
        "booking_options.accommodations[].price_basis": {"per_room_per_night"},
        "booking_options.attraction_tickets[].price_basis": {"per_person_ticket"},
        "booking_options.attraction_tickets[].ticket_status": booking,
        "booking_options.rental_cars[].price_basis": {"per_vehicle_per_day"},
    }
    for kind in ("flights", "ground_transport", "accommodations", "attraction_tickets",
                 "rental_cars"):
        table[f"booking_options.{kind}[].price_status"] = price
        table[f"booking_options.{kind}[].availability_status"] = avail
    for kind in ("flights", "ground_transport"):
        for leg in ("outbound_itinerary", "return_itinerary"):
            table[f"booking_options.{kind}[].{leg}.service_identifier_status"] = \
                set(renderer.SERVICE_IDENTIFIER_STATUSES)
    for entry in renderer.ESSENTIAL_ENTRIES:
        table[f"arrival_essentials.{entry}.status"] = set(renderer.ESSENTIAL_STATUSES)
    return table, ""


def enum_issues(plan: object, table: dict, path: str = "") -> list[dict]:
    """Every value sitting in a closed vocabulary that the vocabulary does not contain.

    `null` is skipped everywhere: the contract writes "not filled in yet" that way, and a gate
    that called an unfilled field a wrong value would fire on every skeleton.
    """
    found: list[dict] = []
    if isinstance(plan, dict):
        for key, value in plan.items():
            child = f"{path}.{key}" if path else key
            allowed = table.get(child)
            # `value not in allowed` raises on a list or a dict, because the vocabulary is a set.
            # A plan carrying `plan_status: ["researched"]` crashed this script outright, which is
            # the one outcome a pre-gate worklist must never produce: it reports nothing at all,
            # including the twenty other things it had already found. An unhashable value is not in
            # any vocabulary by definition, so it is a finding like any other.
            try:
                # A `TODO:` marker is the placeholder gate's finding, not a wrong value.
                placeholder = isinstance(value, str) and value.startswith("TODO")
                outside = allowed is not None and value is not None and not placeholder and value not in allowed
            except TypeError:
                outside = allowed is not None
            if outside:
                found.append({"path": child, "problem": "not in the closed vocabulary",
                              "found_value": value, "allowed": sorted(allowed)})
                continue
            found.extend(enum_issues(value, table, child))
    elif isinstance(plan, list):
        for item in plan:
            found.extend(enum_issues(item, table, f"{path}[]"))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("plan", help="Plan JSON path")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    try:
        plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if not isinstance(plan, dict):
        print("ERROR: the plan must be a JSON object.", file=sys.stderr)
        return 2

    known = contract_shapes(contract)
    vocab, vocab_failure = _vocabularies()
    # Deduplicated by path: `days[].dining[].price_per_person` is ONE mistake whatever the plan's
    # length, and printing it once per array element is the repeated-text waste the plan gate was
    # already taught not to produce. Six days turned fifteen problems into sixty-nine lines.
    seen: set[tuple] = set()
    issues = []
    for issue in walk(plan, known):
        key = (issue["path"], issue["problem"])
        if key in seen:
            continue
        seen.add(key)
        issues.append(issue)

    seen_enum: set[tuple] = set()
    for issue in enum_issues(plan, vocab):
        key = (issue["path"], issue["found_value"])
        if key in seen_enum:
            continue
        seen_enum.add(key)
        issues.append(issue)

    if args.json:
        print(json.dumps({"ok": not issues, "issues": issues,
                          "enum_check": vocab_failure or "ran"}, ensure_ascii=False, indent=1))
    elif not issues:
        # The second half of this sentence is a claim about a check that may not have run. Saying
        # it anyway is worse than silence: the warning goes to stderr and this line goes to stdout,
        # which is what an assistant reads, so a failed import would have produced a confident
        # "every value is in its vocabulary" about values nothing had looked at.
        if vocab_failure:
            print(f"CONTRACT OK ON KEYS ONLY: every key in {Path(args.plan).name} is one "
                  f"templates/final-trip-plan.json declares. Closed-vocabulary VALUES were NOT "
                  f"checked -- see the warning on stderr. Do not read this as a clean run.")
        else:
            print(f"CONTRACT OK: every key in {Path(args.plan).name} is one "
                  f"templates/final-trip-plan.json declares, and every value in a closed "
                  f"vocabulary is one that vocabulary contains.")
        # The next command, named rather than left to be re-derived from SKILL.md. An assistant
        # that cannot hold 110KB of prose can still read the line the last command printed, and
        # this pipeline is a fixed order -- there is nothing to decide here, only to remember.
        print(f"NEXT: python scripts/check_plan_consistency.py {args.plan} --no-verification-yet",
              file=sys.stderr)
    else:
        unknown = sum(1 for i in issues if i["problem"] == "unknown key")
        wrong_type = sum(1 for i in issues if i["problem"] == "wrong type")
        wrong_value = sum(1 for i in issues if i["problem"] == "not in the closed vocabulary")
        parts = [f"{n} {what}" for n, what in
                 ((unknown, "unrecognised key(s)"), (wrong_type, "type mismatch(es)"),
                  (wrong_value, "value(s) outside a closed vocabulary")) if n]
        print(f"CONTRACT: {', '.join(parts)}. This is a worklist, not a verdict -- fix them "
              f"together, then run the gates.")
        for issue in issues:
            if issue["problem"] == "not in the closed vocabulary":
                print(f"  value    {issue['path']} is {issue['found_value']!r}, which is not one "
                      f"of: {', '.join(issue['allowed'])}")
            elif issue["problem"] == "unknown key":
                hint = (f" -- did you mean {issue['suggestion']}?" if issue["suggestion"]
                        else " -- no near match in the contract; check it is not a typo, or that "
                             "it belongs in this plan at all")
                print(f"  unknown  {issue['path']}{hint}")
            else:
                print(f"  type     {issue['path']} is {issue['found_type']}, the contract "
                      f"declares {issue['expected_type']}")
    if vocab_failure:
        print(f"WARNING: {vocab_failure}", file=sys.stderr)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
