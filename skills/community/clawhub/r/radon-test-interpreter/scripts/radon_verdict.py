#!/usr/bin/env python3
"""Radon test interpreter: readings -> verdict, risk, and action plan.

Converts pCi/L <-> Bq/m^3, grades test validity (device/duration/season/
closed-house), interpolates EPA lifetime lung-cancer risk by smoking status,
prices mitigation vs retest, and drafts the real-estate negotiation letter.
Stdlib only. Educational - not a substitute for a certified measurement pro.
"""
import argparse
import sys

PCI_PER_BQ = 1.0 / 37.0
BQ_PER_PCI = 37.0

# EPA Citizen's Guide risk table: pCi/L -> (ever-smoker, never-smoker) per 1000
RISK_TABLE = [
    (0.4, 3, 0.5), (1.3, 20, 2), (2.0, 32, 4), (4.0, 62, 7),
    (8.0, 120, 15), (10.0, 150, 18), (20.0, 260, 36),
]

DEVICE_WINDOWS = {  # (min_days, max_days)
    "charcoal": (2, 7), "liquid-scintillation": (2, 7),
    "crm": (2, 7), "alpha-track": (91, 365), "eperm-short": (3, 7),
    "eperm-long": (91, 365),
}


def interp_risk(pci):
    t = RISK_TABLE
    if pci <= t[0][0]:
        row = t[0]
        return (row[1] * pci / row[0], row[2] * pci / row[0])
    if pci >= t[-1][0]:
        slope = (t[-1][1] - t[-2][1]) / (t[-1][0] - t[-2][0])
        slope_ns = (t[-1][2] - t[-2][2]) / (t[-1][0] - t[-2][0])
        extra = pci - t[-1][0]
        return (t[-1][1] + slope * extra, t[-1][2] + slope_ns * extra)
    for lo, hi in zip(t, t[1:]):
        if lo[0] <= pci <= hi[0]:
            f = (pci - lo[0]) / (hi[0] - lo[0])
            return (lo[1] + f * (hi[1] - lo[1]), lo[2] + f * (hi[2] - lo[2]))
    return (0.0, 0.0)


def validity_report(args):
    issues = []
    wins = DEVICE_WINDOWS.get(args.device)
    if not wins:
        issues.append(f"unknown device '{args.device}' — cannot validate duration")
    elif not (wins[0] <= args.duration_days <= wins[1]):
        issues.append(f"{args.device} valid window {wins[0]}-{wins[1]} d, "
                      f"test was {args.duration_days:.0f} d — INVALID result class")
    if wins and wins[0] < 8:  # short-term device
        if args.closed_house in ("no", "unknown"):
            issues.append("closed-house conditions not honored — short-term result "
                          "unreliable (usually reads LOW)")
        if args.season == "summer":
            issues.append("summer short-term test runs 1-2 pCi/L below annual average — "
                          "a pass does not clear the house")
    if args.season == "winter" and wins and wins[0] < 8:
        print("note: winter short-term runs HIGH (stack effect) — a winter pass is "
              "more trustworthy; a winter >=4 is near-certainly real")
    return issues


def verdict(avg, smoker, occupied):
    if avg >= 8.0:
        v = "MITIGATE-URGENT"
    elif avg >= 4.0:
        v = "MITIGATE"
    elif avg >= 2.0:
        v = "RETEST-LONG-TERM / CONSIDER MITIGATING"
    else:
        v = "MONITOR (retest every 2 yr)"
    s, ns = interp_risk(avg)
    who = "above" if avg * BQ_PER_PCI > 100 else "below/at"
    print(f"average = {avg:.2f} pCi/L = {avg * BQ_PER_PCI:.0f} Bq/m^3 "
          f"(WHO reference 100 Bq/m^3 ≈ 2.7 pCi/L: {who})")
    print(f"lifetime lung-cancer risk ≈ {s:.0f}/1000 ever-smoker | {ns:.0f}/1000 never-smoker")
    if smoker and avg >= 2.0:
        print("smoker/ex-smoker in home: risk column matters more than the 4.0 line — "
              "treat 2.7+ as action-worthy")
    if occupied and avg >= 4.0:
        print("occupied lowest level: sleeping/working here multiplies exposure time")
    return v


def cmd_readings(args):
    vals = [float(v) for v in args.values]
    print(f"readings (pCi/L): {', '.join(f'{v:.1f}' for v in vals)}")
    if max(vals) - min(vals) > 2.0 and len(vals) > 1:
        print(f"WARNING: spread {max(vals) - min(vals):.1f} pCi/L — rooms stratified; "
              "verdict should follow the LOWEST LIVABLE LEVEL, not the diluted average")
    avg = sum(vals) / len(vals)
    issues = validity_report(args)
    if any("INVALID" in i for i in issues):
        print("VERDICT: INVALID-TEST —", "; ".join(issues))
        print("retest with correct protocol before deciding anything")
        return
    for i in issues:
        print("caution:", i)
    v = verdict(avg, args.smokers > 0, args.occupants)
    print(f"\nVERDICT: {v}")
    if "MITIGATE" in v:
        lo, hi = (800, 1500) if avg < 10 else (1000, 2500)
        print(f"  mitigation (active soil depressurization): ${lo}-{hi} install, "
              f"$100-250/yr to run; post-mitigation target < 2.0")
        print(f"  vs doing nothing: this level carries the risk printed above, "
              f"EVERY year of exposure")
    elif "RETEST" in v:
        print("  run a 91+ day alpha-track or long-term e-perm in the lowest livable "
              "level, no closed-house protocol needed")
    print("  retest cadence: every 2 yr, and after renovations/HVAC/finished-basement changes")


def cmd_realestate(args):
    v = verdict(args.reading, args.smokers > 0, True)
    credit = args.mitigation_cost * 1.15  # bid cushion + verification test
    print(f"\nVERDICT: {v}")
    print(f"""
--- negotiation ask (copy into the repair-credit request) ---
Radon result {args.reading:.1f} pCi/L (EPA action level 4.0) exceeds the
mitigation threshold. Buyer requests ONE of:
  1. Seller-installed mitigation by an AARST-NRPP/NEHA-NRPP certified contractor,
     completed before closing, with post-install verification test < 4.0 pCi/L
     (target < 2.0), OR
  2. Credit of ${credit:,.0f} at closing = mitigation ${args.mitigation_cost:,.0f}
     (mid-range of 2 local bids) + 15% contingency + verification test.
Basis: EPA A Citizen's Guide to Radon; ASTM E2121 mitigation practice.
Note: 'unfinished basement' is not a defense - stack effect moves soil gas
upstairs; upstairs levels typically run 30-50% of the level below.""")


def cmd_convert(args):
    v = float(args.value)
    print(f"{v} pCi/L = {v * BQ_PER_PCI:.0f} Bq/m^3 | {v} Bq/m^3 = {v * PCI_PER_BQ:.2f} pCi/L")
    print(f"EPA action 4.0 pCi/L = 148 Bq/m^3 | WHO reference 100 Bq/m^3 = 2.70 pCi/L")


def cmd_risk(args):
    s, ns = interp_risk(float(args.pci))
    print(f"{float(args.pci):.1f} pCi/L: lifetime lung-cancer risk ≈ "
          f"{s:.0f}/1000 ever-smoker ({s / 10:.1f}%) | {ns:.0f}/1000 never-smoker ({ns / 10:.1f}%)")
    print("scale: 4.0 pCi/L ≈ 200 chest x-rays/yr of lung dose")


def cmd_demo(_):
    print("=== winter charcoal 5.2, basement bedroom, smoker ===\n")
    ns = argparse.Namespace(values=["5.2"], duration_days=3, device="charcoal",
                            season="winter", closed_house="yes",
                            occupants="basement-bedroom", smokers=1)
    cmd_readings(ns)
    print("\n=== summer 2.9, valid protocol ===\n")
    ns2 = argparse.Namespace(values=["2.9"], duration_days=4, device="charcoal",
                             season="summer", closed_house="yes",
                             occupants="none", smokers=0)
    cmd_readings(ns2)
    print("\n=== real-estate 6.1 contingency ===\n")
    cmd_realestate(argparse.Namespace(reading=6.1, mitigation_cost=1400, smokers=0))


def main():
    argv = sys.argv[1:]
    if argv and argv[0] == "--demo":
        cmd_demo(None)
        return 0
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("readings", help="interpret one or more readings")
    r.add_argument("values", nargs="+")
    r.add_argument("--duration-days", type=float, default=3.0)
    r.add_argument("--device", default="charcoal",
                   choices=list(DEVICE_WINDOWS) + ["crm", "alpha-track"])
    r.add_argument("--season", choices=["winter", "summer", "shoulder"], default="shoulder")
    r.add_argument("--closed-house", choices=["yes", "no", "unknown"], default="yes")
    r.add_argument("--occupants", default="none",
                   help="e.g. basement-bedroom / office / none")
    r.add_argument("--smokers", type=int, default=0)
    r.set_defaults(func=cmd_readings)

    re_ = sub.add_parser("realestate", help="contingency verdict + credit letter")
    re_.add_argument("--reading", type=float, required=True)
    re_.add_argument("--mitigation-cost", type=float, default=1400)
    re_.add_argument("--smokers", type=int, default=0)
    re_.set_defaults(func=cmd_realestate)

    c = sub.add_parser("convert", help="pCi/L <-> Bq/m3")
    c.add_argument("value", help="number in pCi/L")
    c.set_defaults(func=cmd_convert)

    k = sub.add_parser("risk", help="EPA risk-table lookup")
    k.add_argument("--pci", required=True)
    k.add_argument("--smoker", action="store_true")
    k.set_defaults(func=cmd_risk)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
