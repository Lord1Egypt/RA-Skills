#!/usr/bin/env python3
"""Record that the traveller chose or booked an option: one decision per group, never a reference.

  record_booking.py plan.json --option ID --chosen
  record_booking.py plan.json --option ID --booked --on YYYY-MM-DD --via "where" [--paid AMOUNT CUR]
  record_booking.py plan.json --clear ID

The rules are scripts/bookings.py's. A hotel other than the one its days sleep at re-points those
days, because the stay really changed; everything else leaves verification untouched.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import stat
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bookings  # noqa: E402
import verification_sections as vs  # noqa: E402


def _refuse(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def _write(path: Path, plan: dict) -> None:
    mode = stat.S_IMODE(path.stat().st_mode)
    fd, temp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(plan, handle, ensure_ascii=False, indent=2)
    os.chmod(temp, mode)
    os.replace(temp, path)


def next_save(path: Path, plan: dict) -> str:
    workspace = vs.delivered_workspace(path)
    if workspace is None:
        return (f"NEXT: save it as any plan edit -- python scripts/save_trip_deliverables.py {path} "
                f"--workspace <your Travel Buddy workspace> --overwrite, with --verification <report.json> "
                f"for a verified plan or --unverified otherwise.")
    args: list[object] = [path, "--workspace", workspace, "--overwrite"]
    slug = vs.delivered_slug(path)
    if slug:
        args += ["--slug", slug]
    report = plan.get("verification_report")
    if plan.get("verification_status") == "verified" and isinstance(report, str) and report.strip():
        report_path = (path.parent / report).resolve()
        args += ["--verification", report_path]
    else:
        args += ["--unverified"]
    return "NEXT: " + vs.command_line("save_trip_deliverables.py", *args)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record the traveller's chosen or booked option.")
    parser.add_argument("plan", help="Plan JSON")
    parser.add_argument("--option", help="The option id the traveller chose or booked")
    state = parser.add_mutually_exclusive_group()
    state.add_argument("--chosen", action="store_true", help="Decided, not yet paid")
    state.add_argument("--booked", action="store_true", help="Paid and confirmed")
    parser.add_argument("--on", help="Booking date, YYYY-MM-DD (with --booked)")
    parser.add_argument("--via", help="Where it was booked (with --booked)")
    parser.add_argument("--paid", nargs=2, metavar=("AMOUNT", "CURRENCY"), help="What was paid (with --booked)")
    parser.add_argument("--clear", metavar="ID", help="Remove the record for this option")
    parser.add_argument("--today", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    path = Path(args.plan)
    try:
        plan = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return _refuse(f"cannot read {path}: {exc}")
    if not isinstance(plan, dict):
        return _refuse(f"{path} is not a plan object")
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    records = bookings.records(plan)

    if args.clear:
        kept = [r for r in records if r.get("option_id") != args.clear]
        if len(kept) == len(records):
            return _refuse(f"no booking record for {args.clear!r} to clear")
        plan["bookings"] = kept
        _write(path, plan)
        print(f"CLEARED {args.clear}")
        print(next_save(path, plan))
        return 0

    if not args.option or not (args.chosen or args.booked):
        return _refuse("pass --option ID with --chosen or --booked, or --clear ID")
    index = bookings.option_index(plan)
    if args.option not in index:
        return _refuse(f"no option {args.option!r} in booking_options; ids are: {', '.join(sorted(index))}")
    record: dict = {"option_id": args.option, "state": "booked" if args.booked else "chosen"}
    if args.booked:
        if not args.on or not args.via:
            return _refuse("--booked needs --on YYYY-MM-DD and --via \"where it was booked\"")
        record.update(booked_on=args.on, booked_via=args.via.strip())
    elif args.on or args.via:
        return _refuse("--on and --via belong to --booked")
    if args.paid:
        if not args.booked:
            return _refuse("--paid belongs to --booked: nothing is paid on a chosen option")
        amount, currency = args.paid
        if not re.fullmatch(r"\d+(\.\d{1,2})?", amount):
            return _refuse(f"--paid amount {amount!r} must be a plain number such as 1015 or 1015.50")
        value = float(amount)
        record.update(paid_total=int(value) if value.is_integer() else value, paid_currency=currency.upper())

    kind, option = index[args.option]
    group = bookings.group_key(kind, option)
    replaced = [r.get("option_id") for r in records
                if r.get("option_id") in index and bookings.group_key(*index[r["option_id"]]) == group]
    plan["bookings"] = [r for r in records if r.get("option_id") not in replaced] + [record]

    switched: list[int] = []
    left: list[str] = []
    if kind == "accommodations":
        for day in plan.get("days") or []:
            current = index.get(str(day.get("accommodation_option_id") or ""))
            if current and current[0] == "accommodations" and bookings.group_key(*current) == group \
                    and day.get("accommodation_option_id") != args.option:
                day["accommodation_option_id"] = args.option
                switched.append(day.get("number"))
                name_left = current[1].get("property_name") or day.get("accommodation_option_id")
                if name_left not in left:
                    left.append(name_left)

    problems = bookings.record_problems(plan, today)
    if problems:
        return _refuse("; ".join(problems))
    _write(path, plan)
    if replaced:
        print(f"REPLACED {', '.join(str(r) for r in replaced)} with {args.option} ({group})")
    else:
        print(f"RECORDED {args.option} as {record['state']} ({group})")
    name = option.get("property_name") or args.option
    if switched:
        print(f"STAY SWITCHED: day(s) {', '.join(str(n) for n in switched)} now sleep at {name} "
              f"(was {', '.join(left)})"
              + (" -- they changed, so the save will ask for their recheck" if plan.get("verification_status") == "verified" else ""))
    # Code moved the ids; the check-in lines, route stops and directions are prose, and only an edit
    # moves them. The save refuses until they name the recorded stay, so say which, and say it first.
    stale = bookings.stale_stay_mentions(plan)
    for sentence in stale:
        print(f"EDIT: {sentence}")
    if stale:
        print(f"NEXT: edit the field(s) above to name {name}. Then: " + next_save(path, plan)[len("NEXT: "):])
    else:
        print(next_save(path, plan))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
