#!/usr/bin/env python3
"""Rental property buy-side deal screener.

Underwrites buy-and-hold deals: NOI, cap rate, DSCR, cash-on-cash, 1%-rule,
OER flags, break-even rent, depreciation tax shield, 10-yr projection with
IRR, and a stress grid. Stdlib only. Educational underwriting - verify comps,
taxes, and lender terms before wiring earnest money.
"""
import argparse
import json
import math
import sys


def pmt(rate_annual, years, principal):
    r = rate_annual / 12.0
    n = years * 12
    if r == 0:
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


class Deal:
    def __init__(self, a):
        self.a = a
        self.closing = a.price * a.closing_pct / 100.0
        self.all_in = a.price + a.rehab + self.closing
        self.loan = 0.0 if a.cash else self.all_in * (1 - a.down_pct / 100.0) - a.rehab
        # loan finances price+closing; rehab typically cash
        if not a.cash:
            self.loan = (a.price + self.closing) * (1 - a.down_pct / 100.0)
        self.cash_in = self.all_in - self.loan
        self.gsr = a.rent * 12.0
        self.vac_loss = self.gsr * a.vacancy / 100.0
        self.egi = self.gsr - self.vac_loss
        self.mgmt = self.egi * a.management / 100.0
        self.maint = self.egi * a.maintenance / 100.0
        self.opex = a.tax + a.ins + a.hoa * 12 + self.mgmt + self.maint
        self.noi = self.egi - self.opex
        self.p_i = 0.0 if a.cash else pmt(a.rate / 100.0, 30, self.loan)
        self.ds = self.p_i * 12
        self.cf = self.noi - self.ds
        self.coc = self.cf / self.cash_in if self.cash_in else 0.0
        self.cap = self.noi / self.all_in
        self.dscr = self.noi / self.ds if self.ds else float("inf")
        self.oer = self.opex / self.gsr
        self.one_pct = a.rent / self.all_in
        self.be_rent = (self.opex + self.ds) / 12.0

    def depreciation_shield(self, marginal_rate):
        bldg = self.a.price * self.a.building_pct / 100.0
        return (bldg / 27.5) * marginal_rate


def screen(a, label="", overrides=None):
    o = overrides or {}
    ns = argparse.Namespace(**{**vars(a), **o})
    d = Deal(ns)
    print(f"\n=== {label or 'BASE CASE'} ===" + (f"  [{overrides}]" if overrides else ""))
    print(f"all-in cost      ${d.all_in:>12,.0f}   (price {ns.price:,.0f} + rehab {ns.rehab:,.0f} "
          f"+ closing {d.closing:,.0f})")
    if not ns.cash:
        print(f"loan             ${d.loan:>12,.0f}   @ {ns.rate}% 30-yr → P&I ${d.p_i:,.0f}/mo")
    print(f"cash invested    ${d.cash_in:>12,.0f}")
    print(f"GSR ${d.gsr:,.0f} − vac {ns.vacancy}% (${d.vac_loss:,.0f}) = EGI ${d.egi:,.0f}")
    print(f"OpEx ${d.opex:,.0f} = tax {ns.tax:,.0f} + ins {ns.ins:,.0f} + "
          f"HOA {ns.hoa * 12:,.0f} + mgmt {d.mgmt:,.0f} + maint/repairs {d.maint:,.0f}")
    print(f"NOI              ${d.noi:>12,.0f}   ({d.noi / 12:,.0f}/mo)")
    print(f"cap rate         {d.cap:>12.2%}   vs loan {ns.rate:.1f}% → "
          f"{'POSITIVE' if d.cap > ns.rate / 100 + 0.005 else 'NEGATIVE LEVERAGE' if not ns.cash else 'cash deal'}")
    print(f"1%-rule          {d.one_pct:>12.2%}   (0.6% floor, 1% is a unicorn)")
    print(f"OER              {d.oer:>12.1%}   {'RED FLAG >50%' if d.oer > 0.5 else 'in/near 35-45% band' if d.oer >= 0.3 else 'very low - check you included everything'}")
    if not ns.cash:
        print(f"DSCR             {d.dscr:>12.2f}   (lender line 1.25; <1.10 danger)")
    print(f"annual CF        ${d.cf:>12,.0f}   (${d.cf / 12:,.0f}/mo)")
    print(f"cash-on-cash     {d.coc:>12.2%}   (T-bill yardstick ~4-5%)")
    shield = d.depreciation_shield(ns.marginal_rate)
    at_coc = (d.cf + shield) / d.cash_in if d.cash_in else 0
    print(f"depreciation     ${d.depreciation_shield(1.0):>12,.0f}/yr paper loss → "
          f"shelters ~${shield:,.0f} at {ns.marginal_rate:.0%} → after-tax CoC {at_coc:.2%}")
    be_gap = (ns.rent - d.be_rent) / ns.rent
    print(f"break-even rent  ${d.be_rent:>12,.0f}   ({be_gap:+.0%} cushion vs market "
          f"{'TIGHT <12%' if be_gap < 0.12 else 'OK'})")
    return d


def project(a, years=10):
    d = Deal(a)
    rows = []
    rent = a.rent
    opex = d.opex
    bal = d.loan
    r = a.rate / 100 / 12
    tot_cf = 0.0
    cfs = [-d.cash_in]
    for yr in range(1, years + 1):
        rent *= 1 + a.growth / 100
        opex *= 1 + a.exp_growth / 100
        noi = rent * 12 * (1 - a.vacancy / 100) - opex
        interest_yr = 0.0
        for _ in range(12):
            i = bal * r
            interest_yr += i
            bal -= (d.p_i - i)
        cf = noi - d.ds
        tot_cf += cf
        cfs.append(cf)
        rows.append((yr, rent, noi, cf, bal))
    value = a.price * (1 + a.apprec / 100) ** years
    sale_net = value * (1 - 0.06) - bal  # 6% selling costs
    # simple IRR via bisection
    def npv(rate):
        return sum(cf / (1 + rate) ** t for t, cf in enumerate(cfs + [sale_net]))
    lo, hi = -0.5, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if npv(mid) > 0:
            lo = mid
        else:
            hi = mid
    print(f"\n--- {years}-yr projection (rent +{a.growth}%/yr, exp +{a.exp_growth}%, "
          f"value +{a.apprec}%/yr, sell at 6% costs) ---")
    print(f"{'yr':>3}{'rent/mo':>10}{'NOI':>11}{'cash flow':>11}{'loan bal':>12}")
    for yr, rent, noi, cf, b in rows:
        print(f"{yr:>3}{rent:>10,.0f}{noi:>11,.0f}{cf:>11,.0f}{b:>12,.0f}")
    print(f"total CF collected: ${tot_cf:,.0f}; est. sale net at yr {years}: ${sale_net:,.0f}")
    print(f"cash-flow-only return: {tot_cf / d.cash_in:.1%} | with-sale IRR ≈ {(lo + hi) / 2:.1%}")
    if tot_cf / d.cash_in < 0.3 and (lo + hi) / 2 > 0.08:
        print("NOTE: returns depend mostly on appreciation - the deal doesn't pay you to wait.")


def verdict(a):
    d = Deal(a)
    v = []
    cap_ok = d.cap >= (a.rate / 100 + 0.015) if not a.cash else d.cap >= 0.05
    coc_ok = d.coc >= 0.06
    dscr_ok = a.cash or d.dscr >= 1.25
    if cap_ok and coc_ok and dscr_ok:
        v = "DEAL"
    elif sum([cap_ok, coc_ok, dscr_ok]) >= 2 and (coc_ok or d.coc >= 0.04):
        v = "THIN"
    else:
        v = "OVERPRICED"
    print(f"\n*** VERDICT: {v} ***")
    if not cap_ok and not a.cash:
        print(f"  cap {d.cap:.2%} ≤ rate {a.rate/100:.2%}: NEGATIVE LEVERAGE - "
              f"borrowing makes it worse than paying cash")
    if not coc_ok:
        need_price = None
        gap = 0.06 - d.coc
        print(f"  CoC {d.coc:.2%} < 6%: gap {gap:.1%}")
        if d.cf < 0:
            per_mo = -d.cf / 12
            print(f"  negative ${-d.cf:,.0f}/yr (${per_mo:,.0f}/mo) - price cut needed ≈ "
                  f"${abs(d.cf) / 0.06:,.0f} at the same rent, or rent +"
                  f"${abs(d.cf) / 12 / (1 - a.vacancy/100 - a.management/100 - a.maintenance/100):,.0f}/mo")
    if not dscr_ok:
        print(f"  DSCR {d.dscr:.2f} < 1.25 lender line - loan sized down or denied")
    return v


def cmd_screen(a):
    d = screen(a)
    if a.stress:
        screen(a, "STRESS: rent −10%", overrides={"rent": a.rent * 0.9})
        screen(a, "STRESS: vacancy 8%", overrides={"vacancy": 8})
        screen(a, "STRESS: rate +1pt", overrides={"rate": a.rate + 1.0})
        screen(a, "STRESS: price −5%", overrides={"price": a.price * 0.95})
    project(a, a.years)
    verdict(a)


def cmd_demo(_):
    print("=== DEMO: $320k SFR, $2,200 rent, 25% down @ 6.5% ===")
    base = dict(price=320000, rehab=8000, rent=2200, tax=3600, ins=1400, hoa=0,
                down_pct=25, rate=6.5, vacancy=5, maintenance=8, management=8,
                closing_pct=3.0, building_pct=80, marginal_rate=0.24,
                growth=3.0, exp_growth=3.0, apprec=3.0, years=10, cash=False)
    cmd_screen(argparse.Namespace(**base, stress=True))
    print("\n\n=== DEMO: the deal that works - $185k Midwest duplex, $2,400 combined ===")
    cmd_screen(argparse.Namespace(**{**base, "price": 185000, "rehab": 12000,
                                     "rent": 2400, "tax": 2900, "ins": 1600,
                                     "hoa": 0, "down_pct": 25, "rate": 6.75},
                                    stress=False))


def main():
    argv = sys.argv[1:]
    if argv and argv[0] == "--demo":
        cmd_demo(None)
        return 0
    p = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("screen", help="underwrite one deal")
    s.add_argument("--price", type=float, required=True)
    s.add_argument("--rehab", type=float, default=0)
    s.add_argument("--rent", type=float, required=True, help="monthly, all units combined")
    s.add_argument("--tax", type=float, required=True, help="annual property tax at YOUR basis")
    s.add_argument("--ins", type=float, required=True, help="annual landlord policy")
    s.add_argument("--hoa", type=float, default=0, help="monthly")
    s.add_argument("--down-pct", type=float, default=25)
    s.add_argument("--rate", type=float, default=6.5)
    s.add_argument("--vacancy", type=float, default=5)
    s.add_argument("--maintenance", type=float, default=8, help="percent of EGI incl capex reserve")
    s.add_argument("--management", type=float, default=8)
    s.add_argument("--closing-pct", type=float, default=3.0)
    s.add_argument("--building-pct", type=float, default=80, help="depreciable share of price")
    s.add_argument("--marginal-rate", type=float, default=0.24)
    s.add_argument("--growth", type=float, default=3.0, help="rent growth pct per yr")
    s.add_argument("--exp-growth", type=float, default=3.0, help="expense growth pct per yr")
    s.add_argument("--apprec", type=float, default=3.0, help="appreciation pct per yr")
    s.add_argument("--years", type=int, default=10)
    s.add_argument("--cash", action="store_true", help="no loan")
    s.add_argument("--stress", action="store_true")
    s.set_defaults(func=cmd_screen)
    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
