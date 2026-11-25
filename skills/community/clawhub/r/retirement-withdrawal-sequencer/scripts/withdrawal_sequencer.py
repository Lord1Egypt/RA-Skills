#!/usr/bin/env python3
"""withdrawal_sequencer.py — 5-year retirement withdrawal plan.

Computes: RMDs (Uniform Lifetime Table, ages 73/75 by birth year), bucket
sequencing (cash -> LTCG 0% -> bracket-fill traditional -> Roth last),
federal tax estimate, IRMAA cliff warnings (2-year lookback), Roth-conversion
window verdict.

All rate tables live in CONFIG (2026 US estimates — VERIFY current-year IRS/SSA
figures before relying on output). Stdlib only.
"""
import argparse
from datetime import date

CONFIG = {
    "year": date.today().year,
    # 2026 estimated brackets (post-OBBBA) — VERIFY
    "std_deduction": {"S": 15750, "MFJ": 31500},
    "brackets": {
        "S":  [(0.10, 12400), (0.12, 50400), (0.22, 105700), (0.24, 201775),
               (0.32, 256225), (0.35, 640600), (0.37, 10**9)],
        "MFJ": [(0.10, 24800), (0.12, 100800), (0.22, 211400), (0.24, 403550),
                (0.32, 512450), (0.35, 768700), (0.37, 10**9)],
    },
    "ltcg_0_top": {"S": 49250, "MFJ": 98500},   # 2026 est. 0% LTCG taxable-income tops
    "ltcg_15_top": {"S": 600000, "MFJ": 750000},
    "irmaa": {"S": [106000, 133000, 167000, 200000, 500000],
              "MFJ": [212000, 266000, 334000, 400000, 750000]},
    "irmaa_penalty_per_tier": 1100,  # ~annual Part B+D extra per tier crossed (single rates)
    "rmd_factors": {73: 26.5, 74: 25.5, 75: 24.6, 76: 23.7, 77: 22.9, 78: 22.0,
                    79: 21.1, 80: 20.2, 81: 19.4, 82: 18.5, 83: 17.7, 84: 16.8,
                    85: 16.0, 86: 15.2, 87: 14.4, 88: 13.7, 89: 12.9, 90: 12.2,
                    91: 11.5, 92: 10.8, 93: 10.1, 94: 9.5, 95: 8.9, 96: 8.4,
                    97: 7.8, 98: 7.3, 99: 6.8, 100: 6.4},
    "qcd_limit": 108000,          # 2025 actual; indexed — verify
    "growth": 0.05,               # real-terms portfolio growth assumption
    "basis_pct": 0.60,            # typical cost basis share of a long-held taxable account
}

DISCLAIMER = ("Rates/tables are %d U.S. ESTIMATES — verify against current IRS Rev. Proc. "
              "and SSA IRMAA tables before acting. Not tax advice." % CONFIG["year"])


def rmd_start_year(birth_year: int) -> int:
    return birth_year + (73 if birth_year <= 1959 else 75)  # SECURE 2.0


def fed_tax(taxable: float, status: str) -> float:
    tax, prev = 0.0, 0.0
    for rate, top in CONFIG["brackets"][status]:
        if taxable > prev:
            tax += (min(taxable, top) - prev) * rate
            prev = top
        else:
            break
    return tax


def tax_with_ltcg(ordinary: float, ltcg: float, status: str) -> float:
    """Ordinary income stacked first; LTCG on top at 0/15/20% (NIIT ignored)."""
    zero_top = CONFIG["ltcg_0_top"][status]
    mid_top = CONFIG["ltcg_15_top"][status]
    cg_tax = 0.0
    lo = 0.0
    for rate, hi in [(0.0, max(zero_top - ordinary, 0)), (0.15, max(mid_top - ordinary, 0)), (0.20, 10**9)]:
        band = max(min(ltcg, hi) - lo, 0)
        cg_tax += band * rate
        lo = hi
    return fed_tax(max(ordinary, 0), status) + cg_tax


def irmaa_check(magi: float, status: str):
    tiers = CONFIG["irmaa"][status]
    for i, t in enumerate(tiers):
        if magi < t:
            if i == 0:
                return "OK (no surcharge)", f"MAGI < ${t:,}"
            return (f"TIER {i} surcharge ~${i * CONFIG['irmaa_penalty_per_tier']:,}/yr (single rates)",
                    f"MAGI in ${tiers[i-1]:,}-{t:,}")
    return "TIER 5 max surcharge (~$4,000+/yr)", "MAGI at/above top tier"


def fmt(x): return f"${x:,.0f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--age1", type=int, required=True, help="older account owner age this year")
    ap.add_argument("--age2", type=int, default=0)
    ap.add_argument("--birth-year1", type=int, default=0, help="exact birth year (refines RMD age 73/75)")
    ap.add_argument("--status", choices=["S", "MFJ"], default="MFJ")
    ap.add_argument("--taxable", type=float, required=True)
    ap.add_argument("--traditional", type=float, required=True)
    ap.add_argument("--roth", type=float, default=0)
    ap.add_argument("--cash-pct", type=float, default=10, help="%% of taxable in cash (default 10)")
    ap.add_argument("--spend", type=float, required=True, help="annual gross spending need")
    ap.add_argument("--other-income", type=float, default=0, help="SS + pension + wages (ordinary)")
    ap.add_argument("--charitable", type=float, default=0, help="annual giving (QCD candidate)")
    a = ap.parse_args()

    y0 = CONFIG["year"]
    by1 = a.birth_year1 or (y0 - a.age1)
    rmd_y = rmd_start_year(by1)
    st, sd = a.status, CONFIG["std_deduction"][a.status]

    print(f"=== {y0}-{y0+4} WITHDRAWAL PLAN | ages {a.age1}/{a.age2 or '-'} {st} ===")
    print(f"buckets: taxable {fmt(a.taxable)} ({a.cash_pct}% cash) | traditional {fmt(a.traditional)} | roth {fmt(a.roth)}")
    print(f"RMD START: {rmd_y} (born {by1} -> age {73 if by1 <= 1959 else 75}); "
          f"missed RMD = 25% excise (10% if fixed within 2 yrs; Form 5329)\n")

    d_trad = 0.0
    trad, tx, roth = a.traditional, a.taxable, a.roth
    basis = CONFIG["basis_pct"]
    for k in range(5):
        yr = y0 + k
        age = a.age1 + k
        need = a.spend - a.other_income

        # 1) cash inside taxable (interest is ordinary income)
        d_cash = min(tx * a.cash_pct / 100.0, need)
        need -= d_cash
        tx -= d_cash

        # 2) taxable-account sales -> LTCG portion only of the withdrawal
        d_sale = ltcg = 0.0
        if need > 0 and tx > 0:
            d_sale = min(need, tx)
            ltcg = d_sale * (1 - basis)
            need -= d_sale
            tx -= d_sale

        # 3) traditional: RMD (mandatory) once started
        d_trad = 0.0
        if yr >= rmd_y and trad > 0:
            f = CONFIG["rmd_factors"].get(min(age, 100))
            d_trad = trad / f if f else trad * 0.05
            trad -= d_trad
            need = max(need - d_trad, 0)

        # 4) Roth last
        d_roth = min(roth, max(need, 0))
        roth -= d_roth

        ordinary = a.other_income + d_cash * 0.05        # interest on cash slice, small
        magi = ordinary + ltcg + d_trad                  # Roth never counts
        taxable_income = max(ordinary + ltcg + d_trad - sd, 0)
        tax = tax_with_ltcg(ordinary + d_trad, ltcg, st)
        irmaa, detail = irmaa_check(magi, st)

        parts = []
        if d_cash: parts.append(f"cash {fmt(d_cash)}")
        if d_sale: parts.append(f"taxable-sale {fmt(d_sale)} (gain {fmt(ltcg)})")
        if d_trad: parts.append(f"trad/RMD {fmt(d_trad)}")
        if d_roth: parts.append(f"roth {fmt(d_roth)}")
        print(f"{yr} (age {age}): draw: " + (", ".join(parts) if parts else "covered by other income"))
        print(f"     taxable income {fmt(taxable_income)} -> est. federal tax {fmt(tax)} "
              f"(eff {tax / max(magi, 1) * 100:.1f}% of MAGI)")
        print(f"     MAGI {fmt(magi)} -> IRMAA {irmaa} [{detail}] — hits Medicare premiums in {yr + 2}")
        if yr >= by1 + 70 and a.charitable > 0 and d_trad > 0:
            print(f"     QCD: direct {fmt(min(a.charitable, CONFIG['qcd_limit']))} from IRA to charity — "
                  f"satisfies RMD, excluded from MAGI")

        trad *= 1 + CONFIG["growth"]; tx *= 1 + CONFIG["growth"]; roth *= 1 + CONFIG["growth"]

    # conversion window analysis
    b12 = CONFIG["brackets"][st][1][1]     # top of 12% bracket
    b22 = CONFIG["brackets"][st][2][1]     # top of 22% bracket
    if rmd_y > y0:
        f_first = CONFIG["rmd_factors"].get(min(a.age1 + (rmd_y - y0), 100), 26.5)
        proj_rmd = trad / f_first
        print(f"\nCONVERSION WINDOW {y0}-{rmd_y - 1} (pre-RMD):")
        print(f"  Fill the 12% bracket each year (taxable income up to {fmt(b12)}) — headroom now: "
              f"{fmt(max(b12 - (a.other_income + a.spend * 0.15), 0))}")
        print(f"  Projected first RMD in {rmd_y}: ~{fmt(proj_rmd)} vs 22%-bracket top {fmt(b22)}.")
        if proj_rmd + a.other_income > b22:
            print("  VERDICT: future RMDs likely cross into 22%+ — convert at 12-22% NOW; each $10k moved saves "
                  "~$1,000-2,000 per decade of avoided 22-24% drag.")
        else:
            print("  VERDICT: RMDs look contained under the 22% bracket — conversions optional; "
                  "protect IRMAA headroom instead.")
        print(f"  Constraints: RMD comes out FIRST (conversion stacks on top); conversions irreversible; "
              f"watch IRMAA tier 1 at {fmt(CONFIG['irmaa'][st][0])}.")
    else:
        print(f"\nRMD YEARS: bracket-fill logic reversed — this year's RMD was {fmt(d_trad)}; "
              f"any conversion stacks on top of it.")
    print(f"\nCash-buffer rule (sequence-of-returns): hold 1-2 yrs of spending "
          f"({fmt(a.spend)}-{fmt(2 * a.spend)}) in cash/short Treasuries so a down market never forces equity sales.")
    print("\n" + DISCLAIMER)


if __name__ == "__main__":
    main()
