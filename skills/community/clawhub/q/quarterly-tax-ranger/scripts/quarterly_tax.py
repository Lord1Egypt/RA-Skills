#!/usr/bin/env python3
"""
Quarterly Tax Ranger — safe-harbor quarterly estimates for the
self-employed: 100%/110% prior-year rule vs 90% current-year estimate,
annualized-income (Schedule AI) mode for lumpy income, SE tax with wage
base, QBI deduction, per-$1000 set-aside ledger.

Usage:
  quarterly_tax.py --demo
  quarterly_tax.py --prior-tax 8200 --profit 65000 --filing single \
      --state-rate 5.0
  quarterly_tax.py --prior-tax 12400 --filing single --annualized \
      --q 9000 0 0 22000 --state-rate 5.0
"""
import argparse
import sys

# --- 2026-shaped federal constants (est.) ---
STD_DEDUCTION = {"single": 15000, "mfj": 30000, "hoh": 22500}
BRACKETS = {  # (upper bound, rate) per filing status
    "single": [(11925, .10), (48475, .12), (103350, .22), (197300, .24),
               (250525, .32), (626350, .35), (float("inf"), .37)],
    "mfj": [(23850, .10), (96950, .12), (206700, .22), (394600, .24),
            (501050, .32), (751600, .35), (float("inf"), .37)],
    "hoh": [(17000, .10), (64900, .12), (103350, .22), (197300, .24),
            (250500, .32), (626350, .35), (float("inf"), .37)],
}
SS_WAGE_BASE = 176100.0
SS_RATE, MEDICARE_RATE = 0.124, 0.029
SE_FACTOR = 0.9235
ADDITIONAL_MEDICARE_THRESHOLD = 200000

# quarter periods and due dates (2026 tax year)
QUARTERS = [
    ("Q1", "Jan 1 - Mar 31", "Apr 15, 2026", 90),
    ("Q2", "Apr 1 - May 31", "Jun 15, 2026", 61),
    ("Q3", "Jun 1 - Aug 31", "Sep 15, 2026", 92),
    ("Q4", "Sep 1 - Dec 31", "Jan 15, 2027", 122),
]
ANNUALIZE = {"Q1": 4.0, "Q2": 6.0, "Q3": 4.0, "Q4": 1.0}
AGI_110_THRESHOLD = 150000


def se_tax(net):
    base = net * SE_FACTOR
    ss = min(base, SS_WAGE_BASE) * SS_RATE
    med = base * MEDICARE_RATE
    addl = max(0.0, base - ADDITIONAL_MEDICARE_THRESHOLD) * 0.009
    return ss + med + addl


def income_tax(taxable, filing):
    tax, prev = 0.0, 0.0
    for upper, rate in BRACKETS[filing]:
        if taxable > prev:
            tax += (min(taxable, upper) - prev) * rate
            prev = upper
        else:
            break
    return tax


def federal_total(net, filing):
    """(total federal est, components dict) for SE net profit."""
    se = se_tax(net)
    half_se = se / 2
    qbi = max(0.0, (net - half_se)) * 0.20
    taxable = max(0.0, net - STD_DEDUCTION[filing] - half_se - qbi)
    it = income_tax(taxable, filing)
    return it + se, {"se": se, "half_se_deduction": half_se, "qbi": qbi,
                     "taxable_income": taxable, "income_tax": it}


def safe_harbor_target(prior_tax, prior_agi):
    if prior_agi and prior_agi > AGI_110_THRESHOLD:
        return prior_tax * 1.10, "110% of prior-year tax (prior AGI > $150k)"
    return prior_tax, "100% of prior-year tax"


def report(args):
    out = []
    filing = args.filing
    prior_agi = args.prior_agi

    # ---------- path A: prior-year safe harbor ----------
    target, why = safe_harbor_target(args.prior_tax or 0, prior_agi)
    out.append("SAFE HARBOR (prior-year rule)")
    out.append("=" * 62)
    out.append(f"prior-year tax: ${args.prior_tax or 0:,.0f}  ->  "
               f"target {why}")
    out.append(f"= ${target:,.0f} total, split evenly:")
    per_q = target / 4
    for q, period, due, _days in QUARTERS:
        out.append(f"  {q} ({period:<12}) due {due:<12} pay ${per_q:,.0f}")
    out.append("(any remainder vs this year's true tax is due Apr 15 "
               "WITHOUT penalty)")

    # ---------- path B: 90% of current-year estimate ----------
    out.append("")
    out.append("CURRENT-YEAR ESTIMATE (90% harbor / set-aside ledger)")
    out.append("-" * 62)
    if args.profit:
        fed, comp = federal_total(args.profit, filing)
        state = args.profit * (args.state_rate / 100)
        eff_fed = fed / args.profit
        eff_state = state / args.profit
        out.append(f"net profit ${args.profit:,.0f} ({filing}):")
        out.append(f"  SE tax ............... ${comp['se']:,.0f} "
                   f"(wage base ${SS_WAGE_BASE:,.0f})")
        out.append(f"  half-SE deduction .... ${comp['half_se_deduction']:,.0f}")
        out.append(f"  QBI deduction ........ ${comp['qbi']:,.0f} (20% pass-"
                   "through, pre-phaseout)")
        out.append(f"  taxable income ....... ${comp['taxable_income']:,.0f}")
        out.append(f"  income tax ........... ${comp['income_tax']:,.0f}")
        out.append(f"  federal total ........ ${fed:,.0f}  "
                   f"({eff_fed:.1%} of net)")
        if args.state_rate:
            out.append(f"  state est ({args.state_rate}%) ... ${state:,.0f} "
                       f"({eff_state:.1%})")
        ninety = fed * 0.90
        out.append(f"  90% harbor ........... ${ninety:,.0f} "
                   f"(${ninety / 4:,.0f}/quarter)")
        set_aside = eff_fed + eff_state
        out.append("")
        out.append(f"SET-ASIDE LEDGER: {set_aside:.1%} of every payment "
                   "->$1000 gross:")
        out.append(f"  federal ${eff_fed * 1000:,.0f} + state "
                   f"${eff_state * 1000:,.0f} = "
                   f"${set_aside * 1000:,.0f}/$1000")
        if args.prior_tax and target:
            cheaper = "prior-year harbor" if target < ninety else \
                      "90% current-year"
            out.append("")
            out.append(f"cheaper certain option: {cheaper} "
                       f"(${min(target, ninety):,.0f})")
    else:
        out.append("(no --profit given: pass --profit for this section)")

    # ---------- path C: annualized (Schedule AI) ----------
    if args.annualized:
        if not args.q or len(args.q) != 4:
            raise SystemExit("--annualized needs --q Q1 Q2 Q3 Q4 net profits")
        out.append("")
        out.append("ANNUALIZED-INCOME METHOD (Form 2210 Schedule AI)")
        out.append("-" * 62)
        cum = 0.0
        paid = 0.0
        cum_days = 0
        for (q, period, due, days), qp in zip(QUARTERS, args.q):
            cum += qp
            cum_days += days
            annualized = cum * (365.0 / cum_days)
            fed_ann, _ = federal_total(annualized, filing)
            required = fed_ann * (cum_days / 365.0)
            payment = max(0.0, required - paid)
            paid += payment
            out.append(f"  {q} cum income ${cum:>9,.0f} annualized "
                       f"${annualized:>10,.0f} -> pay ${payment:>8,.0f} "
                       f"by {due}")
            if q == "Q2":
                out.append("      (note Q2 window is 2 months - that is "
                           "correct, not a bug)")
        out.append(f"total annualized payments: ${paid:,.0f}")
        if args.state_rate:
            out.append(f"add ~{args.state_rate}% state on each period's "
                       "income per your state's schedule")
        out.append("file Form 2210 with Schedule AI attached, or the IRS "
                   "computes the penalty without it")

    out.append("")
    out.append("Estimates use 2026-shaped brackets/std-deduction/wage-base "
               "constants. Payment discipline tool, not tax advice.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--prior-tax", type=float, help="last year's total tax")
    ap.add_argument("--prior-agi", type=float,
                    help="last year's AGI (110%% trigger check)")
    ap.add_argument("--profit", type=float,
                    help="this year's expected net SE profit")
    ap.add_argument("--q", nargs=4, type=float, metavar=("Q1", "Q2", "Q3", "Q4"))
    ap.add_argument("--annualized", action="store_true")
    ap.add_argument("--filing", default="single",
                    choices=["single", "mfj", "hoh"])
    ap.add_argument("--state-rate", type=float, default=0.0,
                    help="state income tax %% as flat estimate")
    args = ap.parse_args(argv)

    if args.demo:
        print("DEMO 1 — steady freelancer, rising income")
        print("~" * 62)
        d1 = argparse.Namespace(prior_tax=8200, prior_agi=71000,
                                profit=92000, annualized=False, q=None,
                                filing="single", state_rate=5.0)
        print(report(d1))
        print()
        print("DEMO 2 — lumpy consultant (Q4-heavy), 110% rule")
        print("~" * 62)
        d2 = argparse.Namespace(prior_tax=12400, prior_agi=168000,
                                profit=None, annualized=True,
                                q=[9000, 0, 0, 22000],
                                filing="single", state_rate=0)
        print(report(d2))
        return 0
    if not (args.prior_tax or args.profit or args.annualized):
        ap.print_help()
        return 1
    print(report(args))
    return 0


if __name__ == "__main__":
    sys.exit(main())
