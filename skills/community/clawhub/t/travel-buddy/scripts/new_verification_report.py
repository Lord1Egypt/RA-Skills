#!/usr/bin/env python3
"""A correctly-shaped verification report to fill in, instead of one to guess at.

Usage: python new_verification_report.py --from-plan <plan.json> [--out <report.json>]

WHY THIS EXISTS, measured on the author's own workspace. Seventeen delivered plans, and the
verification stage -- the most expensive thing this skill asks for, and the one it argues hardest
for -- has never left a surviving artifact behind. Six plans claim `verification_status: verified`;
four of them point at report files that no longer exist, two of those into a session scratchpad
that is deleted when the session ends. Nothing was lazy about that. `new_plan_skeleton.py` exists
because starting a plan from a blank file cost one measured run three round trips and twenty-one
structural errors, and the report is the harder document of the two: seven blocks, a tier the plan
computes rather than the author choosing, and a coverage rule that demands a pointer for every
dining card claiming researched hours. The only guide was the gate telling you what was wrong after
you guessed.

So this emits the shape, bound to the plan, with the pointers already derived and CHECKED to
resolve -- and with every conclusion left as a `TODO:`, because a scaffold for an evidence document
is one wrong step from a forgery generator. `check_plan_consistency.check_verification` refuses a
report still carrying placeholder text, which is what makes this safe to hand to an author: an
unfilled report cannot be delivered, in the same way an unfilled plan cannot be rendered.

WHAT IT DOES NOT DO. It does not verify anything, and it cannot: every `claims_checked` entry it
writes is a pointer at a claim somebody still has to go and check. The pointer says where to look.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from check_plan_consistency import (  # noqa: E402
    RESEARCHED_HOURS_STATUS,
    required_domains_for,
    resolve_pointer,
)
from verification_sections import (  # noqa: E402
    changed_sections,
    command_line,
    digest_is_current,
    resave_command,
    section_digests,
    section_pointers,
)

TODO = "TODO: "


def _seq(value: object) -> list:
    return value if isinstance(value, list) else []


def _obj(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def pointers_for(plan: dict) -> dict[str, list[str]]:
    """Where each block has to look, derived from this plan rather than from a generic list.

    `sights_and_hours` is the one with a coverage rule behind it: every dining card whose
    `hours_status` claims research must be cited by name, because a block that counted its checks
    in the double digits while a meal sat on a venue's rest day is the defect that rule was written
    for. The rest are the fields whose truth the domain owns.
    """
    days = _seq(plan.get("days"))
    booking = _obj(plan.get("booking_options"))
    out: dict[str, list[str]] = {name: [] for name in
                                 ("entry", "transport", "sights_and_hours",
                                  "booking_and_lodging", "seasonality",
                                  "consistency", "completeness")}

    out["entry"] += ["entry_context.status", "entry_context.summary", "entry_context.source_url"]
    for index, _ in enumerate(_seq(_obj(plan.get("entry_context")).get("per_jurisdiction"))):
        out["entry"].append(f"entry_context.per_jurisdiction[{index}].source_url")

    for day_index, day in enumerate(days):
        route = _obj(_obj(day).get("route"))
        out["transport"].append(f"days[{day_index}].route.verified_map_url")
        if route.get("segments"):
            out["transport"].append(f"days[{day_index}].route.segments[0].service_or_line")
        out["seasonality"].append(f"days[{day_index}].contingency")
        # The coverage rule: a card claiming researched hours owes a pointer.
        for card_index, card in enumerate(_seq(_obj(day).get("dining"))):
            if str(_obj(card).get("hours_status") or "") in RESEARCHED_HOURS_STATUS:
                # The gate asks for a pointer UNDER the card, not for `venue_hours` specifically.
                # Naming only that field meant a card claiming researched hours while carrying no
                # `venue_hours` key produced no pointer at all -- the resolve filter dropped it --
                # and the scaffold then handed over a report the coverage rule refuses for a gap it
                # had no way to fill. The card itself always resolves, so it is the fallback.
                prefix = f"days[{day_index}].dining[{card_index}]"
                out["sights_and_hours"].append(
                    f"{prefix}.venue_hours" if _obj(card).get("venue_hours") is not None
                    else prefix)

    for index, _ in enumerate(_seq(plan.get("destination_experience_anchors"))):
        out["sights_and_hours"].append(f"destination_experience_anchors[{index}].source_url")
        out["seasonality"].append(f"destination_experience_anchors[{index}].why_it_matters")

    for kind in ("flights", "ground_transport"):
        for index, _ in enumerate(_seq(booking.get(kind))):
            out["transport"].append(f"booking_options.{kind}[{index}].outbound_itinerary")
            out["booking_and_lodging"].append(f"booking_options.{kind}[{index}].fare_low")
    for index, _ in enumerate(_seq(booking.get("accommodations"))):
        out["booking_and_lodging"] += [
            f"booking_options.accommodations[{index}].nightly_cost_low",
            f"booking_options.accommodations[{index}].availability_status",
            f"booking_options.accommodations[{index}].guest_rating_value"]
    for index, _ in enumerate(_seq(booking.get("attraction_tickets"))):
        out["booking_and_lodging"].append(
            f"booking_options.attraction_tickets[{index}].sale_opens_at")

    out["consistency"] += ["budget.estimated_per_person_low", "budget.breakdown",
                           "transport_overview.overall_duration_minutes"]
    out["completeness"] += ["trip.traveler_preferences.ranked_must_haves",
                            "trip.traveler_constraints.mobility_notes",
                            "budget.included_categories"]

    # Only pointers that actually resolve are written. A report whose pointers miss is refused by
    # the gate, and a scaffold that hands the author a broken one costs the round trip it exists
    # to save.
    return {name: [p for p in dict.fromkeys(entries) if resolve_pointer(plan, p)]
            for name, entries in out.items()}


def build(plan: dict, plan_path: Path) -> tuple[dict, list[str]]:
    required, reason = required_domains_for(plan)
    pointers = pointers_for(plan)
    notes = [f"tier: {'full' if len(required) >= 5 else 'light'} — {reason}"]

    def block(key: str, name_field: str) -> dict:
        cited = pointers.get(key) or []
        if not cited:
            notes.append(f"{key}: no pointer in this plan resolves for it — write the block by "
                         f"hand or say why it has nothing to check")
        return {name_field: key, "claims_checked": cited,
                "findings": [{"claim": TODO + f"what {key} actually checked, in one sentence",
                              "verdict": TODO + "confirmed / wrong / misleading / unverifiable",
                              "correction": None, "severity": TODO + "critical / major / minor (wrong or misleading findings)",
                              "evidence_url": TODO + "the page you opened",
                              "resolved": False, "resolution": None}]}

    domains = sorted(required)
    report = {
        "checked_at": dt.date.today().isoformat(),
        "plan": str(plan_path),
        "method": TODO + "how the five domains were run — concurrently, or as separate passes",
        "domains": [block(name, "domain") for name in domains],
        # Both audits are required at every tier and cost no network, so they are never omitted.
        "audits": [block(name, "audit") for name in ("consistency", "completeness")],
    }
    for name in domains:
        notes.append(f"{name}: {len(pointers.get(name) or [])} pointer(s)")
    for name in ("consistency", "completeness"):
        notes.append(f"{name}: {len(pointers.get(name) or [])} pointer(s)")
    return report, notes


def recheck_entries(plan: dict, report: dict) -> tuple[list[dict], list[str], str | None]:
    """One TODO recheck per section changed since the plan's verified save, or a refusal.

    The receipt the save stamped is the only record of what the report covered, so without one
    for THIS report there is nothing to recheck against -- the honest next step is a full pass,
    and the refusal says so rather than guessing which parts moved.
    """
    receipt = plan.get("verification_receipt") if isinstance(plan.get("verification_receipt"), dict) else {}
    if not receipt or str(receipt.get("report_checked_at") or "") != str(report.get("checked_at") or ""):
        return [], [], ("this plan carries no verification receipt for a report checked on "
                        f"{report.get('checked_at')!r}, so there is nothing to recheck against. "
                        "If it is an edited copy of a plan delivered verified, name the delivered "
                        "copy with --receipt-from <workspace>/plans/<file>.json; otherwise run a "
                        "full verification: python scripts/new_verification_report.py "
                        "--from-plan <plan.json> --out <report.json>.")
    changed, removed = changed_sections(receipt.get("sections") or {}, plan)
    # A recheck covers the part as it was when checked, so each entry records that version's
    # digest; check_verification counts it only while the part still has it. A part the report
    # already rechecked at its current version needs no second entry.
    current = section_digests(plan)
    rechecks = [r for r in report.get("rechecks") or [] if isinstance(r, dict)]
    changed = [section for section in changed
               if not any(str(r.get("section")) == section
                          and digest_is_current(plan, section, r.get("section_digest"))
                          for r in rechecks)]
    today = dt.date.today().isoformat()
    entries = [{
        "section": section,
        "section_digest": current.get(section),
        "checked_at": today,
        "reason": TODO + "what changed in this part, and at whose request",
        "claims_checked": section_pointers(plan, section),
        "findings": [{"claim": TODO + "what the recheck actually opened, in one sentence",
                      "verdict": TODO + "confirmed / wrong / misleading / unverifiable",
                      "correction": None,
                      "severity": TODO + "critical / major / minor (wrong or misleading findings)",
                      "evidence_url": TODO + "the page you opened",
                      "resolved": False, "resolution": None}],
    } for section in changed]
    notes = [f"{len(changed)} section(s) changed since the verified save: "
             + (", ".join(changed) or "none")]
    if removed:
        notes.append("removed since the verified save (nothing to recheck): " + ", ".join(removed))
    return entries, notes, None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--from-plan", required=True, help="The plan this report will vouch for")
    parser.add_argument("--out", default=None,
                        help="Write here instead of standard output (with --recheck: instead of "
                             "amending --report in place)")
    parser.add_argument("--recheck", action="store_true",
                        help="Append one recheck entry per section the plan changed since its "
                             "verified save, to the report named by --report")
    parser.add_argument("--report", help="With --recheck: the verification report to amend")
    parser.add_argument("--receipt-from", default=None,
                        help="With --recheck, when --from-plan is an edited working copy: the "
                             "delivered plan whose verification receipt it is compared against")
    args = parser.parse_args()
    if args.recheck:
        return run_recheck(args)
    args.out = args.out or "-"

    path = Path(args.from_plan)
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR: could not read {args.from_plan}: {exc}", file=sys.stderr)
        return 2
    if not isinstance(plan, dict):
        print("ERROR: the plan must be a JSON object.", file=sys.stderr)
        return 2

    report, notes = build(plan, path)
    body = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.out == "-":
        sys.stdout.write(body)
    else:
        Path(args.out).write_text(body, encoding="utf-8")
        print(f"Verification report skeleton: {args.out}")
    for note in notes:
        print(f"  {note}", file=sys.stderr)
    print("Every conclusion is a TODO on purpose: check_verification refuses a report still "
          "carrying placeholder text, so this cannot be delivered until somebody has actually "
          "looked. The pointers say WHERE to look; they are not evidence that anyone did.",
          file=sys.stderr)
    print(f"NEXT: fill it in, then python scripts/check_plan_consistency.py {args.from_plan} "
          f"--verification {args.out if args.out != '-' else '<report.json>'}", file=sys.stderr)
    return 0


def run_recheck(args: argparse.Namespace) -> int:
    if not args.report:
        print("ERROR: --recheck amends an existing report; name it with --report <report.json>.",
              file=sys.stderr)
        return 2
    try:
        plan = json.loads(Path(args.from_plan).read_text(encoding="utf-8"))
        report = json.loads(Path(args.report).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"ERROR: could not read the plan or the report: {exc}", file=sys.stderr)
        return 2
    if not isinstance(plan, dict) or not isinstance(report, dict):
        print("ERROR: the plan and the report must both be JSON objects.", file=sys.stderr)
        return 2
    # The receipt lives in the delivered copy; an author editing their own working file has none
    # in it -- or one from an older verification -- and this refused them with "run a full
    # verification" while the save they came from was comparing against the delivered copy's
    # receipt all along. The receipt that counts is the one bound to this report.
    def bound(receipt: object) -> bool:
        return (isinstance(receipt, dict)
                and str(receipt.get("report_checked_at") or "") == str(report.get("checked_at") or ""))

    plan_file = Path(args.from_plan).expanduser().resolve()
    fresh_start = "NEXT: " + command_line("new_verification_report.py", "--from-plan", plan_file,
                                          "--out", plan_file.with_name(plan_file.stem
                                                                       + "-new-verification.json"))
    if args.receipt_from and not bound(plan.get("verification_receipt")):
        try:
            delivered = json.loads(Path(args.receipt_from).read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            print(f"ERROR: could not read --receipt-from: {exc}", file=sys.stderr)
            return 2
        if not (isinstance(delivered, dict) and bound(delivered.get("verification_receipt"))):
            print(f"ERROR: {args.receipt_from} carries no verification receipt for the report "
                  f"checked on {report.get('checked_at')!r} -- it was delivered before receipts "
                  f"existed, or by another verification -- so nothing records which parts that "
                  f"report covered. Verify the plan afresh, or save it with --unverified so the "
                  f"page says so:", file=sys.stderr)
            print(fresh_start, file=sys.stderr)
            return 2
        plan["verification_receipt"] = delivered["verification_receipt"]
    entries, notes, refusal = recheck_entries(plan, report)
    if refusal:
        print(f"ERROR: {refusal}", file=sys.stderr)
        print(fresh_start, file=sys.stderr)
        return 2
    amended = dict(report)
    amended["rechecks"] = list(report.get("rechecks") or []) + entries
    body = json.dumps(amended, ensure_ascii=False, indent=2) + "\n"
    # Amended in place unless told otherwise -- what --report's help has always said this does.
    # Walked literally on 2026-09-24, the command the gate printed (no --out) wrote the amended
    # report to standard output and saved nothing, and the report the save reads never changed.
    out = args.out or args.report
    if out == "-":
        sys.stdout.write(body)
    else:
        try:
            Path(out).write_text(body, encoding="utf-8")
        except OSError as exc:
            print(f"ERROR: could not write the amended report to {out}: {exc}. Nothing was "
                  f"changed; name a writable file with --out.", file=sys.stderr)
            return 2
        print(f"Verification report with rechecks: {out}", file=sys.stderr)
    for note in notes:
        print(f"  {note}", file=sys.stderr)
    print("Each new recheck is a TODO on purpose: check_verification refuses placeholder text, so "
          "the amended report cannot certify the plan until somebody has re-opened those parts.",
          file=sys.stderr)
    resave = resave_command(args.from_plan, out, args.receipt_from) if out != "-" else ""
    if resave:
        print(f"Fill in every TODO in {out} with what you re-opened, then save:", file=sys.stderr)
        print(f"NEXT: {resave}", file=sys.stderr)
    elif out != "-":
        # Not in a workspace, so no save can be named; the check that comes before one can be.
        print(f"Fill in every TODO in {out} with what you re-opened, then check it:", file=sys.stderr)
        print("NEXT: " + command_line("check_plan_consistency.py", plan_file, "--verification",
                                      Path(out).expanduser().resolve()), file=sys.stderr)
    else:
        print(f"NEXT: fill them in, then python scripts/check_plan_consistency.py {args.from_plan} "
              f"--verification <report.json>", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
