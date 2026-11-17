#!/usr/bin/env python3
"""Re-run today's gates over every plan already saved in a Travel Buddy workspace.

Why this exists. The gates in this skill get stricter every time a defect ships, and each new
rule is written against the plan that is being built right now. Nothing ever looked back. Measured
on a real workspace of eleven saved plans, only the most recent passed: the others carried 25 to
126 findings each, and classifying them showed the great majority were not schema drift from
newly-added fields but the very defects the traveller had reported -- 52 to 80 map endpoints per
plan that could not geocode, 21 to 31 opening times asserted with no evidence, and five walking
legs whose implied speed was a run. Those pages are still openable, still say nothing, and still
look exactly like the one plan that is clean.

So this reports rather than repairs. It never edits a saved plan or page: what a stale plan needs
is a decision from the traveller (rebook, re-verify, discard), and a script that silently rewrote
their itinerary would be making that decision for them.

Usage:
    python audit_workspace.py [--workspace PATH] [--plan NAME] [--verbose] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check_plan_consistency import PLAN_CHECKS  # noqa: E402
from render_final_trip_html import validate_plan  # noqa: E402
from verification_sections import changed_sections  # noqa: E402

DEFAULT_WORKSPACE = Path.home() / "Travel Buddy"

# Files that live in plans/ without being plans. The workspace mixes intake forms, next-action
# handoffs, verification reports and discovery logs into the same directory as the itineraries,
# so an audit that globbed *.json would report dozens of "broken plans" that were never plans.
def _report_missing(plan: dict, path) -> str | None:
    """The report path a `verified` plan names, when that path no longer resolves."""
    if str(plan.get("verification_status") or "") != "verified":
        return None
    pointer = plan.get("verification_report")
    if isinstance(pointer, dict):
        return None                      # embedded rather than referenced: nothing to lose
    if not isinstance(pointer, str) or not pointer.strip():
        return "(none named)"
    from pathlib import Path as _Path
    candidate = _Path(pointer).expanduser()
    if not candidate.is_absolute():
        candidate = path.parent / pointer
    return None if candidate.exists() else pointer


def _changed_since_verified(plan: dict) -> list[str]:
    """Sections of a `verified` plan that moved after the save that verified it.

    The receipt is stamped by save_trip_deliverables.py on every verified save; a plan edited in
    the workspace afterwards still says verified, and its page still carries no banner, until the
    changed sections are rechecked and the plan re-saved. Plans saved before receipts existed carry
    none and are left alone -- they cannot say what their report covered.
    """
    if str(plan.get("verification_status") or "") != "verified":
        return []
    receipt = plan.get("verification_receipt")
    if not isinstance(receipt, dict) or not isinstance(receipt.get("sections"), dict):
        return []
    changed, _ = changed_sections(receipt["sections"], plan)
    return changed


NON_PLAN_PREFIXES = ("intake-", "next-action-", "verification-", "replan-",
                     "destination-discovery-", "intermediate-")

# The citation check_plan_consistency.cites() staples onto every finding, read back out. Findings
# are grouped by where their rule is written, so parsing this is what lets the compact report point
# a reader at a reference section without reprinting the paragraph that names it.
#
# `[^\]]+` rather than a tighter pattern because the target is an author-written anchor and a new
# one only has to avoid `]`; findall rather than a single match because nothing stops a check from
# citing twice, and a pattern that silently kept the first would drop the narrower of the two.
_CITATION = re.compile(r"\[see references/([^\]]+)\]")


def is_plan_file(path: Path) -> bool:
    if path.suffix != ".json" or path.name.startswith(NON_PLAN_PREFIXES):
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    # A plan is identified by its shape rather than its filename, because a draft saved by hand
    # carries no naming convention at all -- three such files sat in the measured workspace.
    return isinstance(data, dict) and isinstance(data.get("days"), list) and "trip" in data


def summarize_rules(attributed: list[tuple[str, str, bool]]) -> list[dict]:
    """Collapse a plan's findings to one row per (rule, reference): what fired, how often, read where.

    This is the whole compact report. On the measured workspace the prose is overwhelmingly the
    same sentence repeated -- one plan's 122 findings come from 9 distinct checks -- so a caller
    that wants to know *what is wrong with this plan* is paying for a paragraph it has already read
    47 times. Grouping is not a summary that loses something: the rule identity and the reference
    are the two things a caller acts on, and both survive.

    Keyed on the reference as well as the rule because a check may cite a narrower anchor for one
    of its branches (that is what check_plan_consistency.cite() is for). Folding those into the
    check's default row would send a reader to a section that does not state the rule they hit.

    Sorted by descending count, then by rule and reference, because the tie-break has to be total
    or two runs over an unchanged workspace produce reports that cannot be diffed -- and diffing
    these across runs is how a traveller sees a plan decay.
    """
    rows: dict[tuple[str, tuple[str, ...]], dict] = {}
    for rule_id, message, crashed in attributed:
        references = tuple(dict.fromkeys(_CITATION.findall(message)))
        row = rows.setdefault((rule_id, references), {
            "rule_id": rule_id,
            "count": 0,
            # An empty list, never a missing key: a caller writing row["references"] must not have
            # to know that an uncited finding exists. validate_plan produces them today.
            "references": [f"references/{target}" for target in references],
        })
        row["count"] += 1
        if crashed:
            # Carried verbatim into the compact form, prose rule notwithstanding. A crash is a
            # defect in this skill's own gate rather than in the traveller's plan, it is one short
            # line, and a caller that cannot see it would report the plan as audited when in fact
            # that rule ran nowhere. The flag comes from the raise site rather than from sniffing
            # the message for "crashed", because a check is free to write that word itself and a
            # finding misread as a crash is the same wrong answer in the other direction.
            crashes = row.setdefault("crashed", [])
            if message not in crashes:
                crashes.append(message)
    return sorted(rows.values(),
                  key=lambda row: (-row["count"], row["rule_id"], row["references"]))


def audit_plan(path: Path) -> dict:
    plan = json.loads(path.read_text(encoding="utf-8"))
    structure = validate_plan(plan)
    consistency: list[str] = []
    notes: list[str] = []
    # Which check produced which finding. Every check appends into the same list, so this
    # attribution exists only at the moment of the call -- record the boundary here or it is gone
    # for good. Without it the JSON report had nothing to group on and could only say something by
    # shipping every finding's full prose, which is what made it cost more to read than the plans.
    #
    # validate_plan is a single call and reports no per-rule identity, so its findings are
    # attributed to it by name. That is honest: it is one gate, and its messages name their own
    # field.
    attributed: list[tuple[str, str, bool]] = [("validate_plan", message, False)
                                               for message in structure]
    for check in PLAN_CHECKS:
        name = getattr(check, "__name__", "check")
        before = len(consistency)
        # Which index, if any, holds the crash note rather than a finding about the plan. Recorded
        # as a position because a check that raises half way through has already appended real
        # findings, and those are about the traveller's plan while the last one is about this gate.
        crashed_at = None
        try:
            check(plan, consistency, notes)
        except Exception as exc:  # noqa: BLE001 - a crashing check must not hide the other 18
            consistency.append(f"[{getattr(check, '__name__', 'check')} crashed: {exc}]")
            crashed_at = len(consistency) - 1
        attributed.extend((name, consistency[index], index == crashed_at)
                          for index in range(before, len(consistency)))
    trip = plan.get("trip") or {}
    stamp = plan.get("gates_passed") or {}
    return {
        "file": path.name,
        "title": trip.get("title") or trip.get("destination") or path.stem,
        "start_date": trip.get("start_date"),
        "verification_status": plan.get("verification_status") or "(unset)",
        # Does the evidence still exist? A plan claiming `verified` whose report is gone renders
        # with no banner and reads as an authority nobody can check. Measured on the author's own
        # workspace before save_trip_deliverables started carrying the report in: four of six
        # `verified` plans pointed at files that no longer existed, two of them into a session
        # scratchpad deleted when the session ended. This is the one claim on the page that cannot
        # be re-derived from the plan, so it is the one worth chasing to disk.
        "report_missing": _report_missing(plan, path),
        # And the evidence can still exist while no longer covering the plan: a verified plan
        # edited afterwards is carried under a report that never saw the edit.
        "changed_since_verified": _changed_since_verified(plan),
        # How many checks existed when this plan was saved, against how many exist now. The gap
        # is the only honest way to read a finding count: 40 findings against 19 checks that all
        # existed at save time means the plan was wrong, while 40 against 8 means most of them
        # are rules written after it shipped. Plans saved before stamping report None and have
        # to be read by hand, which is the cost this field removes going forward.
        "checks_at_save": stamp.get("checks"),
        "structure_errors": structure,
        "consistency_errors": consistency,
        "total": len(structure) + len(consistency),
        # One row per (rule, reference). Both output forms are rendered from this same dict, so the
        # human report and the JSON report cannot disagree about which plans are stale or by how
        # much; only the amount of prose differs.
        "rules": summarize_rules(attributed),
    }


def summarize_timing(workspace: Path) -> list[str]:
    """One line per measured run: where the elapsed time actually went.

    Surfaced here because a measurement nobody reads changes nothing, and because the interesting
    number only appears across runs. A single run tells you this trip took 57 minutes; ten runs
    tell you whether the traveller's own answering time is the constant, in which case no amount
    of token thrift will make the skill feel faster.
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from trip_timer import durations, human, timing_dir  # noqa: PLC0415
    except ImportError:  # pragma: no cover - only if the tool is removed
        return []
    directory = timing_dir(workspace)
    if not directory.is_dir():
        return []
    lines: list[str] = []
    for path in sorted(directory.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        spans, compute, wait = durations((data or {}).get("events") or [])
        if not spans:
            continue
        total = compute + wait
        unfinished = [phase for phase, seconds, _ in spans if seconds < 0]
        share = f"{wait / total * 100:.0f}% waiting on you" if total > 0 else "no closed phase"
        note = f"; unfinished: {', '.join(unfinished)}" if unfinished else ""
        lines.append(f"{path.stem}: {human(total)} total — compute {human(compute)}, "
                     f"wait {human(wait)} ({share}){note}")
    return lines


def audit_discovery_runs(plans_dir: Path) -> list[tuple[str, str]]:
    """Which saved discovery results came from a run that actually finished.

    run_destination_discovery.py streams the child assistant's output into a .md and its exit code
    into the sibling .log. In a real workspace, of four runs only one exited 0: two exited 1 and
    left .md files containing a CLI usage error and "API Error: Connection closed mid-response"
    respectively, and one recorded no exit code at all because the process was killed before it
    could write its own ending. The .md files read like finished answers in every case.

    The runner now marks its own result file on a non-zero exit, which covers the first two. It
    cannot cover the third -- a process that is killed cannot write anything -- so that one is
    detected here instead, by the absence of a terminal line in the log.
    """
    results: list[tuple[str, str]] = []
    for log_path in sorted(plans_dir.glob("destination-discovery-*.log")):
        text = log_path.read_text(encoding="utf-8", errors="replace")
        result_path = log_path.with_suffix(".md")
        exit_line = [line for line in text.splitlines() if line.startswith("Exit code:")]
        if not exit_line:
            verdict = "INTERRUPTED (no exit)"
        elif exit_line[-1].strip() != "Exit code: 0":
            verdict = f"FAILED ({exit_line[-1].strip().lower()})"
        else:
            verdict = "ok"
        if verdict != "ok" and result_path.exists():
            verdict += " + result saved"
        results.append((result_path.name if result_path.exists() else log_path.name, verdict))
    return results


def json_report(plans_dir: Path, ordered: list[dict], timing: list[str],
                discovery: list[tuple[str, str]], verbose: bool) -> dict:
    """The machine-readable report, in the same order and with the same verdicts the human one prints.

    What a consumer is expected to do with the compact form. Read it whole -- that is the point of
    it -- and answer the question this script exists for: which saved plans no longer hold. Each
    plan carries its verdict, its finding count, its verification status, the gate stamp to read
    that count against, and one row per rule that fired with the reference section stating the
    rule. That is enough to tell a traveller *what* is stale (map endpoints that will not geocode
    is a different conversation from a newly-required field) and to decide re-plan, re-verify or
    discard. When one plan needs its actual sentences, fetch that one:

        audit_workspace.py --json --verbose --plan <file>

    Why the prose moved behind --verbose. This flag exists so a program, or a model, can consume
    the audit cheaply, and it was doing the opposite: dumping all fifteen plans' findings in full
    cost two orders of magnitude more than the human report it was meant to be a cheaper form of,
    and most of those bytes were one rule's rationale paragraph reprinted once per venue. A report
    a caller cannot afford to read is a check that does not happen -- and the check not happening
    is a traveller walking to a place that closed.

    The counts here are the ones audit_plan computed and the human printer reads from the same
    dicts, so the two forms cannot disagree about which plans are stale; --verbose adds sentences
    and changes no verdict.
    """
    return {
        "workspace": str(plans_dir.parent),
        "plans_dir": str(plans_dir),
        # How many checks exist now, to read each plan's checks_at_save against. Present at the top
        # rather than per plan because it is a property of this run, and a caller comparing two
        # audits needs to know the denominator moved.
        "checks_now": len(PLAN_CHECKS),
        "verbose": verbose,
        "totals": {
            "plans": len(ordered),
            "clean": sum(1 for result in ordered if result["total"] == 0),
            "stale": sum(1 for result in ordered if result["total"] > 0),
            "findings": sum(result["total"] for result in ordered),
        },
        "plans": [_json_plan(result, verbose) for result in ordered],
        "timing": timing,
        "discovery_runs": [{"file": name, "verdict": verdict} for name, verdict in discovery],
    }


def _json_plan(result: dict, verbose: bool) -> dict:
    """One plan's entry: always the verdict and the rule rows, the sentences only when asked."""
    entry = {
        "file": result["file"],
        "title": result["title"],
        "start_date": result["start_date"],
        # The same two words the human report prints in its left column, so a caller does not have
        # to re-derive the verdict from the count and risk deriving it differently.
        "status": "OK" if result["total"] == 0 else "STALE",
        "verification_status": result["verification_status"],
        "checks_at_save": result["checks_at_save"],
        "total": result["total"],
        "structure": len(result["structure_errors"]),
        "consistency": len(result["consistency_errors"]),
        "rules": result["rules"],
    }
    if verbose:
        # The full prose, unchanged and unsplit -- this is what --json alone used to emit for every
        # plan at once. Nothing was deleted, it just costs a flag and, with --plan, one plan.
        entry["structure_errors"] = result["structure_errors"]
        entry["consistency_errors"] = result["consistency_errors"]
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--workspace", default=str(DEFAULT_WORKSPACE),
                        help="Travel Buddy workspace root")
    parser.add_argument("--plan", default=None,
                        help="Audit only plans whose filename contains this (case-insensitive). "
                             "The drill-down after reading --json: one plan's findings in full "
                             "without paying for the other fourteen.")
    parser.add_argument("--verbose", action="store_true",
                        help="Print every finding rather than a per-plan count")
    parser.add_argument("--json", dest="as_json", action="store_true",
                        help="Emit the report as JSON for further processing")
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser()
    plans_dir = workspace / "plans"
    if not plans_dir.is_dir():
        print(f"ERROR: no plans directory at {plans_dir}", file=sys.stderr)
        return 2

    paths = [p for p in sorted(plans_dir.glob("*.json")) if is_plan_file(p)]
    if args.plan is not None and paths:
        needle = args.plan.casefold()
        selected = [p for p in paths if needle in p.name.casefold()]
        if not selected:
            # Refused rather than audited-as-empty. A mistyped --plan that quietly matched nothing
            # would print a clean report, which is the one answer this tool must never give by
            # accident: "no findings" and "nothing was checked" would look identical to the caller,
            # and the caller is deciding whether a traveller's saved trip still holds.
            print(f"ERROR: --plan {args.plan!r} matched none of the {len(paths)} plan(s) in "
                  f"{plans_dir}. Available: {', '.join(p.name for p in paths)}", file=sys.stderr)
            return 2
        paths = selected

    results = [audit_plan(p) for p in paths]
    # Worst first, ties by filename because `paths` is already sorted and Python's sort is stable.
    # Both forms render from this one ordering so that "the third plan down" means the same thing
    # whichever form a reader asked for.
    ordered = sorted(results, key=lambda r: -r["total"])

    if args.as_json:
        # Emitted before the no-plans early return below, and never as prose. `--json` printing the
        # human sentence "No plan files found" on an empty workspace handed a caller invalid JSON
        # for the one workspace state it most needs to parse -- a run that died before it saved
        # anything -- and json.loads raised instead of reporting it.
        print(json.dumps(
            json_report(plans_dir, ordered, summarize_timing(workspace),
                        audit_discovery_runs(plans_dir), args.verbose),
            ensure_ascii=False, indent=2))
        return 0

    if not results:
        print(f"No plan files found in {plans_dir}.")
        # Timing still prints. A workspace with measurements and no saved plan is a run that died
        # before delivery, which is the run whose timing is most worth reading -- and the early
        # return used to swallow exactly that case.
        for line in summarize_timing(workspace):
            print(f"  {line}")
        return 0

    clean = [r for r in results if r["total"] == 0]
    stale = [r for r in results if r["total"] > 0]
    print(f"{len(results)} plan(s) in {plans_dir}\n")
    current = len(PLAN_CHECKS)
    for result in ordered:
        mark = "OK  " if result["total"] == 0 else "STALE"
        at_save = result["checks_at_save"]
        gates = (f"gates {at_save}/{current}" if at_save is not None
                 else "gates unrecorded (pre-stamp)")
        print(f"{mark} {result['total']:>4} finding(s)  {result['file']}"
              f"   [verification: {result['verification_status']}; {gates}]")
        if result.get("report_missing"):
            print(f"        ! claims verified, but its report {result['report_missing']!r} is not "
                  f"there. The page renders with no banner, so this reads as an authority "
                  f"nobody — including the traveller — can check.")
        if result.get("changed_since_verified"):
            changed = result["changed_since_verified"]
            print(f"        ! claims verified, but {len(changed)} part(s) changed after the save that "
                  f"verified it and were not rechecked: {', '.join(changed[:6])}"
                  f"{' ...' if len(changed) > 6 else ''}. The page still carries no banner.")
        if args.verbose and result["total"]:
            for error in result["structure_errors"] + result["consistency_errors"]:
                print(f"        - {error.splitlines()[0][:160]}")

    timing = summarize_timing(workspace)
    if timing:
        print()
        print("Planning time (from scripts/trip_timer.py):")
        for line in timing:
            print(f"  {line}")

    discovery = audit_discovery_runs(plans_dir)
    if discovery:
        print()
        print("Discovery runs:")
        for name, verdict in discovery:
            print(f"  {verdict:<24} {name}")

    print()
    if stale:
        # Said plainly, because the count alone invites the comfortable reading -- "the rules got
        # stricter, of course old plans fail". On the measured workspace that reading was wrong
        # for most findings, and the difference matters: a newly-required field is cosmetic, a map
        # link that does not geocode is the traveller standing at the wrong place.
        print(f"{len(stale)} plan(s) predate the checks that now exist. A finding here is not "
              f"automatically schema drift:")
        print("  run again with --verbose and read them -- map endpoints, opening hours and "
              "walking speeds were wrong when those plans shipped, not merely unrecorded.")
        print("  Nothing has been modified. Re-plan, re-verify or discard is a decision for the "
              "traveller.")
    if clean:
        print(f"{len(clean)} plan(s) pass every check this skill currently has.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
