#!/usr/bin/env python3
"""Social Security claiming-age optimizer.

Month-accurate SSA arithmetic: FRA by birth year, early reductions (5/9 & 5/12
of 1%/month), delayed retirement credits (8%/yr to 70), cumulative-benefit
break-even between any two claiming ages, longevity-quartile verdicts, and the
pre-FRA earnings test. Stdlib only.

Disclaimer: educational math, not SSA output. Verify figures at ssa.gov.
"""
import argparse
import math
import sys

# ---------------------------------------------------------------- FRA lookup
def fra_for_birth_year(year: int):
    """Return (years, months) Full Retirement Age per SSA table."""
    if year < 1937:
        return (65, 0)
    if year <= 1942:
        return (65, 2 * (year - 1937))
    if 1943 <= year <= 1954:
        return (66, 0)
    if 1955 <= year <= 1959:
        return (66, 2 * (year - 1954))
    return (67, 0)  # 1960+


def factor_at(age_m: int, fra_m: int) -> float:
    """Benefit factor for claiming at age_m (months since birth), given FRA in months."""
    if age_m < 62 * 12:
        raise ValueError("earliest eligibility is 62")
    if age_m > 70 * 12:
        age_m = 70 * 12  # credits stop at 70
    diff = age_m - fra_m
    if diff == 0:
        return 1.0
    if diff < 0:  # early
        early = -diff
        first = min(early, 36)
        rest = early - first
        return 1.0 - first * (5.0 / 900.0) - rest * (5.0 / 1200.0)
    # delayed: 2/3 of 1% per month == 8%/yr
    return 1.0 + diff * (2.0 / 300.0)


def monthly_benefit(pia: float, age_m: int, fra_m: int) -> float:
    return math.floor(pia * factor_at(age_m, fra_m) * 10) / 10.0  # SSA-style rounding down to dime


# ------------------------------------------------------- cumulative curves
def cumulative(benefit: float, claim_age_m: int, through_age_m: int) -> float:
    """Total nominal dollars paid from claim age through a given age."""
    months = through_age_m - claim_age_m
    return benefit * max(0, months)


def breakeven_age(pia: float, fra_m: int, a_m: int, b_m: int, discount: float = 0.0):
    """Age (in months, fractional) where claiming at b overtakes claiming at a.
    a must be the EARLIER claim. Returns None if never within 100."""
    ben_a = monthly_benefit(pia, a_m, fra_m)
    ben_b = monthly_benefit(pia, b_m, fra_m)
    cum_a = 0.0
    cum_b = 0.0
    prev_diff = None
    for t in range(a_m, 100 * 12 + 1):  # month-by-month to age 100
        cum_a += ben_a * ((1 + discount) ** (-(t - a_m)))
        if t >= b_m:
            cum_b += ben_b * ((1 + discount) ** (-(t - b_m)))
        diff = cum_b - cum_a
        if prev_diff is not None and prev_diff < 0 <= diff:
            # linear interpolation inside the crossing month
            frac = (0 - prev_diff) / (diff - prev_diff) if diff != prev_diff else 0
            return t - 1 + frac
        prev_diff = diff
    return None


LONGEVITY = {  # approximate quartiles at 62 (SSA period + cohort tilt)
    "male": {"p25": 78, "p50": 83, "p75": 88},
    "female": {"p25": 81, "p50": 86, "p75": 91},
}


def fmt_age(m: float) -> str:
    yrs = int(m // 12)
    mo = int(round(m % 12))
    return f"{yrs}y{mo:02d}m"


def verdict_for(be: float, qu: dict) -> str:
    lines = []
    for name, age in qu.items():
        if be < age - 2:
            v = "DELAY WINS"
        elif be > age + 2:
            v = "EARLY WINS"
        else:
            v = "TOO CLOSE TO CALL"
        lines.append(f"  at {name.upper()} (age ~{age}): {v}")
    return "\n".join(lines)


# ---------------------------------------------------------------- commands
def cmd_plan(args):
    fy, fm = fra_for_birth_year(args.birth_year)
    fra_m = fy * 12 + fm
    print(f"Birth year {args.birth_year} → FRA = {fy}y{fm:02d}m")
    print(f"PIA (benefit at FRA): ${args.pia:,.0f}/mo\n")
    print(f"{'Age':<6}{'Factor':>8}{'$/month':>12}{'Δ vs FRA':>10}")
    rows = []
    for age in range(62, 71):
        am = age * 12
        f = factor_at(am, fra_m)
        b = monthly_benefit(args.pia, am, fra_m)
        rows.append((age, f, b))
        print(f"{age:<6}{f:>7.3f}x{b:>11,.0f}{(f - 1) * 100:>+9.1f}%")

    qu = LONGEVITY["male"] if (args.longevity or "male") == "male" else LONGEVITY["female"]
    pairs = [tuple(args.compare)] if args.compare else [(62, max(67, fy)), (62, 70), (max(67, fy), 70)]
    print()
    for x, y in pairs:
        be = breakeven_age(args.pia, fra_m, x * 12, y * 12, args.discount)
        if be is None:
            print(f"{x} vs {y}: no crossover by age 100 (discount {args.discount:.1%})")
            continue
        ben_x = monthly_benefit(args.pia, x * 12, fra_m)
        ben_y = monthly_benefit(args.pia, y * 12, fra_m)
        print(f"\nClaim {x} (${ben_x:,.0f}/mo) vs claim {y} (${ben_y:,.0f}/mo)")
        print(f"  break-even: claiming {y} overtakes at age {fmt_age(be)} "
              f"({(be - x * 12) / 12:.1f} yr of checks recouped)")
        print(verdict_for(be / 12.0, qu))
        # lifetime totals at median
        med = qu["p50"]
        cx = cumulative(ben_x, x * 12, med * 12)
        cy = cumulative(ben_y, y * 12, med * 12)
        print(f"  nominal totals to median age {med}:  age {x} = ${cx:,.0f} | age {y} = ${cy:,.0f}"
              f"  → {'delay ahead' if cy > cx else 'early ahead'} by ${abs(cy - cx):,.0f}")
    print("\nApproximate quartiles used:", qu, "(SSA-derived approximations)")


def cmd_earnings_check(args):
    fy, fm = fra_for_birth_year(args.birth_year)
    fra_m = fy * 12 + fm
    claim_m = int(args.claim_age * 12)
    ben = monthly_benefit(args.pia, claim_m, fra_m)
    claim_yrs, claim_mos = divmod(claim_m, 12)
    print(f"Born {args.birth_year}, FRA {fy}y{fm:02d}m, claiming at {claim_yrs} "
          f"(${ben:,.0f}/mo), salary ${args.salary:,.0f}")
    limit, rate = 23400, 2  # 2026: $1 withheld per $2 over
    note = "under-FRA year"
    if claim_yrs == fy:
        limit, rate = 62160, 3  # FRA-year, months before FRA only
        note = "FRA-year (months before FRA only)"
    if claim_m >= fra_m:
        print("No earnings test after FRA — full checks regardless of salary.")
        return
    excess = max(0.0, args.salary - limit)
    withheld = excess / rate
    withheld = min(withheld, ben * 12)
    months_lost = int(withheld // ben) if ben else 0
    print(f"Earnings test ({note}): limit ${limit:,}, rate $1 per ${rate}")
    print(f"Withheld ≈ ${withheld:,.0f} (~{months_lost} month(s) of checks)")
    print("NOT lost: SSA recalculates your benefit upward at FRA (ARF) for withheld months.")
    net_annual = ben * 12 - withheld
    print(f"Net year-1 benefit cash: ${net_annual:,.0f}")


def cmd_demo(_args):
    print("=== DEMO: born 1962, PIA $2,400 ===\n")
    ns = argparse.Namespace(birth_year=1962, pia=2400, compare=(62, 70), discount=0.0, longevity="male")
    cmd_plan(ns)
    print("\n=== DEMO: earnings test at 63, $55k salary ===\n")
    ns2 = argparse.Namespace(birth_year=1962, pia=2400, claim_age=63, salary=55000)
    cmd_earnings_check(ns2)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0] == "--demo":
        cmd_demo(argparse.Namespace())
        return 0
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)


    sp = sub.add_parser("plan", help="full claiming table + break-evens")
    sp.add_argument("--birth-year", type=int, required=True)
    sp.add_argument("--pia", type=float, required=True, help="PIA from ssa.gov statement")
    sp.add_argument("--compare", nargs=2, type=int, metavar=("AGE_A", "AGE_B"), help="e.g. 62 70")
    sp.add_argument("--discount", type=float, default=0.0, help="personal annual discount rate, e.g. 0.03")
    sp.add_argument("--longevity", choices=["male", "female"], default="male")
    sp.set_defaults(func=cmd_plan)

    se = sub.add_parser("earnings-check", help="earnings-test withholding math")
    se.add_argument("--birth-year", type=int, required=True)
    se.add_argument("--pia", type=float, required=True)
    se.add_argument("--claim-age", type=float, required=True)
    se.add_argument("--salary", type=float, required=True)
    se.set_defaults(func=cmd_earnings_check)


    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
