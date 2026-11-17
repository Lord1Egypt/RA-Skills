#!/usr/bin/env python3
"""
unit_verdict.py — is the storage unit still worth paying for?

Subcommands:
  audit       depreciated contents value vs rent -> KEEP/DOWNGRADE/PURGE verdict
  consider    rent-a-unit decision for a bounded life event
  climate     climate-control necessity test
  exit-plan   dated 30-day purge/move-out schedule

Stdlib only.
"""
import argparse
import sys
from datetime import date, timedelta

# category -> (resale_low, resale_high, label)
DEPRECIATION = {
    "wood":      (0.30, 0.50, "solid wood furniture"),
    "uphol":     (0.05, 0.15, "upholstered / mattresses"),
    "appliance": (0.20, 0.40, "working appliances"),
    "electronics": (0.10, 0.25, "electronics"),
    "tools":     (0.40, 0.60, "tools"),
    "kitchen":   (0.10, 0.20, "kitchen / housewares"),
    "clothes":   (0.05, 0.10, "clothes / linens"),
    "books":     (0.05, 0.15, "books / media"),
    "mixed":     (0.15, 0.30, "mixed household goods"),
}

CLIMATE_NEED = {
    "wood instrument": "YES", "art/canvas": "YES", "antiques (real)": "YES",
    "paper archive": "YES", "photos": "YES", "comics/vinyl/collectible paper": "YES",
    "leather furniture": "YES", "electronics (amps, old computers)": "YES",
    "mattress": "no real benefit", "plastic bins": "no", "metal shelving": "no",
    "lawn chairs": "no", "most furniture": "borderline (wood glue joints in dry heat)",
    "tools": "no (oiled steel fine)", "clothes": "no (musty risk low if boxed dry)",
}

SIZE_HINTS = [
    ("5x5", "a closet: boxes, chairs, small items"),
    ("5x10", "studio / dorm room contents"),
    ("10x10", "1-bedroom apartment"),
    ("10x15", "2-bedroom + appliances"),
    ("10x20", "3-bedroom house"),
    ("10x30", "4-bedroom + garage overflow"),
]


def parse_contents(spec):
    out = []
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts = chunk.split(":")
        if len(parts) != 3:
            print(f"  !! bad item '{chunk}' (use name:purchase_value:category)"); sys.exit(1)
        name, val, cat = parts[0].strip(), float(parts[1]), parts[2].strip().lower()
        if cat not in DEPRECIATION:
            print(f"  !! unknown category '{cat}'. Known: {', '.join(DEPRECIATION)}"); sys.exit(1)
        out.append((name, val, cat))
    return out


def value_items(items):
    lo = hi = 0.0
    for _, val, cat in items:
        r = DEPRECIATION[cat]
        lo += val * r[0]
        hi += val * r[1]
    return lo, hi


def cmd_audit(args):
    items = parse_contents(args.contents)
    lo, hi = value_items(items)
    mid = (lo + hi) / 2
    paid = args.rent * args.months_held
    breakeven = mid / args.rent if args.rent else 0

    print(f"\n  UNIT AUDIT — ${args.rent}/mo, held {args.months_held} months, ${paid:.0f} paid so far")
    print("  " + "=" * 58)
    print(f"  {'item':<28} {'paid':>7}  {'worth now':>12}")
    for name, val, cat in items:
        r = DEPRECIATION[cat]
        print(f"  {name[:28]:<28} {val:>7.0f}  {val*r[0]:.0f}-{val*r[1]:.0f}")
    print("  " + "-" * 58)
    print(f"  Contents resale value today:  ${lo:.0f} - ${hi:.0f} (mid ${mid:.0f})")
    print(f"  Already spent on rent:        ${paid:.0f}")
    print(f"  Break-even from month zero:   {breakeven:.0f} months of rent = contents value")

    if paid > mid:
        verdict = "ALREADY-LOST"
        why = (f"Rent paid (${paid:.0f}) exceeds today's contents value (${mid:.0f}).\n"
               "  The unit is no longer storing wealth; it is storing avoidance.\n"
               "  Every further month is $%.0f to postpone one 4-hour sorting session." % args.rent)
    elif breakeven < 12:
        verdict = "KEEP (short bridge)"
        why = (f"Contents (${mid:.0f}) justify up to {breakeven:.0f} months at ${args.rent}/mo.\n"
               "  Rational as a bridge — SET AN EXIT DATE NOW and put it in the calendar.")
    elif breakeven < 24 or args.months_held >= 12:
        verdict = "DOWNGRADE or PURGE"
        why = (f"Break-even at {breakeven:.0f} months and you're {args.months_held} months in.\n"
               "  Downsize one unit class (saves 30-40%) after a purge pass, or exit fully.")
    else:
        verdict = "KEEP (high-value contents)"
        why = (f"Contents value (${mid:.0f}) is high vs rent; storage is cheaper than\n"
               "  rebuying. Re-run this audit yearly or on any rate increase.")
    print(f"\n  VERDICT: {verdict}\n  {why}")
    if args.months_held >= 12:
        print(f"\n  12-MONTH RULE CHECK: held {args.months_held} months.")
        print("  If you haven't retrieved anything in the last year, need is unproven —")
        print("  the exceptions (documented horizon date, true archive) must be explicit.")
    print(f"\n  Rate-increase reality: +8%/yr makes this a ${args.rent*1.08**3:.0f}/mo unit in 3 years.")
    return 0


def cmd_consider(args):
    lo, hi = value_items(parse_contents(args.contents))
    mid = (lo + hi) / 2
    cost = args.rent * args.months
    print(f"\n  CONSIDERING A UNIT: ${args.rent}/mo x {args.months} months = ${cost:.0f}")
    print(f"  Contents (resale) ${lo:.0f}-${hi:.0f}; replacement-if-sold ~${mid:.0f}")
    if args.exit_date:
        print(f"  Stated exit date: {args.exit_date} (a date makes this a plan, not a lease)")
    if cost < mid * 0.5:
        print("\n  VERDICT: RENT — storage costs less than half of contents' replacement value")
        print("  for the bounded period. Calendar the exit date; cancel in writing early.")
    elif cost < mid:
        print("\n  VERDICT: MARGINAL — storage < replacement, but within 2x. Prefer")
        print("  downsizing contents first: sell the $0-replacement items, store the rest")
        print("  in a smaller unit.")
    else:
        print("\n  VERDICT: SKIP — storage for this period costs more than replacing the")
        print("  contents at resale value. Sell now, rebuy later, pocket the difference.")
    print("\n  Facility checklist: month-to-month lease, no admin fee, first-month promo,")
    print("  24h access if you'll need weekends, insurance NOT auto-billed.")
    return 0


def cmd_climate(args):
    items = [i.strip().lower() for i in args.contents.split(",") if i.strip()]
    need = []
    for i in items:
        for k, v in CLIMATE_NEED.items():
            if k.split()[0] in i or i in k:
                if v == "YES":
                    need.append(i)
                break
    print("\n  CLIMATE-CONTROL TEST (+30-50% rent)")
    if need:
        print(f"  Needs climate control: {', '.join(need)}")
        print("  Paper/leather/instruments/wood warp and mold in humidity swings and 100F+ units.")
    else:
        print("  No climate-critical items detected. Standard unit is fine.")
        print("  Save the 30-50% — that's $40-70/mo on a $140 unit.")
    print("\n  Rule of thumb: if it would survive a garage, it survives a standard unit.")
    return 0


def cmd_exit_plan(args):
    today = date.today()
    print(f"\n  30-DAY EXIT PLAN — {args.unit} at {args.facility or 'your facility'}")
    print(f"  Current rent: ${args.rent}/mo. Target: unit empty and cancelled in 30 days.\n")
    weeks = [
        ("Day 1", ["Read contract: notice period (10-30 days typical), deposit terms",
                   "Photograph entire unit for insurance/estate record",
                   "Book charity pickup for day 22-24 (they come to the unit)"]),
        ("Weekend 1 (4h)", ["Photos/documents/heirlooms -> home, no exceptions",
                            "Sort into SELL / DONATE / TRASH / KEEP lanes with tape and labels",
                            "List SELL tier (tools, solid wood, brand names) on marketplace at resale prices"]),
        ("Week 2", ["Answer listings; 14-day sale deadline then demote to DONATE",
                    "Order junk-hauler quote if TRASH lane is large ($150-350 typical)",
                    "Move KEEP lane home or to a downgraded smaller unit if verdict was DOWNGRADE"]),
        ("Weekend 2 (4h)", ["Second sort pass; everything unclaimed becomes DONATE/TRASH",
                            "Box DONATE for pickup; stack TRASH for hauler"]),
        ("Week 3", ["Charity pickup happens; get the receipt (tax-deductible)",
                    "Hauler takes TRASH; facility dumpster rules checked"]),
        ("Week 4", ["Sweep, photograph EMPTY unit",
                    "Written cancellation WITH confirmation (email + signed form)",
                    "Verify deposit return and that insurance billing stopped"]),
    ]
    d = today
    for label, tasks in weeks:
        print(f"  {label}:")
        for t in tasks:
            print(f"    - {t}")
    print(f"\n  Labour budget: ~10 hours total. At ${args.rent*2/10:.0f}/hour-equivalent,")
    print(f"  this plan pays for itself before month two ends.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Storage unit economics")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("audit")
    p.add_argument("--rent", type=float, required=True)
    p.add_argument("--months-held", type=int, required=True)
    p.add_argument("--contents", required=True, help="name:purchase_value:category,...")
    p.set_defaults(fn=cmd_audit)
    p = sub.add_parser("consider")
    p.add_argument("--rent", type=float, required=True)
    p.add_argument("--months", type=int, required=True)
    p.add_argument("--contents", required=True)
    p.add_argument("--exit-date")
    p.set_defaults(fn=cmd_consider)
    p = sub.add_parser("climate")
    p.add_argument("--contents", required=True, help="comma list of item types")
    p.set_defaults(fn=cmd_climate)
    p = sub.add_parser("exit-plan")
    p.add_argument("--rent", type=float, required=True)
    p.add_argument("--unit", default="10x10")
    p.add_argument("--facility", default="")
    p.set_defaults(fn=cmd_exit_plan)
    args = ap.parse_args()
    if not args.cmd:
        ap.print_help(); sys.exit(1)
    sys.exit(args.fn(args) or 0)


if __name__ == "__main__":
    main()
