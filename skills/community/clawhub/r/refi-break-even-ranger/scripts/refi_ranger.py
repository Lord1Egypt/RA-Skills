#!/usr/bin/env python3
"""refi-break-even-ranger: mortgage refinance break-even and lifetime-cost analyzer.

Pure-stdlib. Compares a current loan against refinance offers with REAL math:
monthly payment via amortization, amortization schedule to a horizon,
break-even months from (closing costs - points buydown) / monthly savings,
lifetime interest delta at equal horizon, cash-out effect, shortened-term
analysis, rate-shopping comparison table, and the "keep current loan" verdict.

Usage:
  python3 refi_ranger.py analyze \
      --balance 280000 --current-rate 6.5 --current-payment 1768 \
      --new-rate 5.25 --term 30 --closing 4200 --points 0.5 \
      --horizon-years 7
  python3 refi_ranger.py compare --balance 280000 --current-rate 6.5 \
      --current-payment 1768 --offers offers.json
"""
from __future__ import annotations

import argparse
import json
import sys


def monthly_rate(annual_pct: float) -> float:
    return annual_pct / 100.0 / 12.0


def pmt(principal: float, annual_rate_pct: float, term_years: int) -> float:
    """Standard amortizing payment."""
    r = monthly_rate(annual_rate_pct)
    n = term_years * 12
    if r == 0:
        return principal / n
    return principal * r / (1 - (1 + r) ** (-n))


def remaining_balance(principal: float, annual_rate_pct: float, payment: float,
                      months: int) -> float:
    """Balance after `months` payments of `payment` on this rate."""
    r = monthly_rate(annual_rate_pct)
    bal = principal
    for _ in range(months):
        interest = bal * r
        bal = bal + interest - payment
        if bal <= 0:
            return 0.0
    return bal


def lifetime_cost(balance: float, rate_pct: float, payment: float, months: int):
    """Total paid + ending balance over `months`."""
    paid = 0.0
    bal = balance
    r = monthly_rate(rate_pct)
    for _ in range(months):
        interest = bal * r
        principal_part = payment - interest
        if principal_part <= 0:
            # payment doesn't amortize — balance grows (neg-am guard)
            bal += interest - payment
            paid += payment
            continue
        bal -= principal_part
        paid += payment
        if bal <= 0:
            paid += bal  # subtract overpayment
            bal = 0
            break
    return paid, bal


def analyze_offer(balance: float, cur_rate: float, cur_payment: float,
                  cur_months_left: int, new_rate: float, new_term_years: int,
                  closing: float, points_pct: float, extra_monthly: float = 0.0,
                  horizon_years: float | None = None, cash_out: float = 0.0) -> dict:
    """Full refi analysis for one offer vs the current loan."""
    loan_amount = balance + cash_out
    points_cost = loan_amount * points_pct / 100.0
    total_upfront = closing + points_cost

    new_payment_base = pmt(loan_amount, new_rate, new_term_years)
    new_payment = new_payment_base + extra_monthly

    monthly_savings = cur_payment - new_payment_base
    if monthly_savings > 0:
        break_even_months = total_upfront / monthly_savings
    else:
        break_even_months = None  # never breaks even on payment alone

    horizon_m = int((horizon_years or new_term_years) * 12)
    horizon_m = min(horizon_m, cur_months_left + 120)  # sane cap

    # Current loan over horizon
    cur_paid, cur_bal = lifetime_cost(balance, cur_rate, cur_payment,
                                      min(horizon_m, cur_months_left))
    # New loan over horizon (with optional extra payment applied)
    new_paid, new_bal = lifetime_cost(loan_amount, new_rate, new_payment, horizon_m)

    horizon_months = horizon_m
    equity_delta = (balance - cur_bal) - (loan_amount - new_bal)  # + = new builds equity faster
    lifetime_delta = (cur_paid - cur_bal) - (new_paid - new_bal + total_upfront)
    # net cost over horizon = payments - equity ; positive delta = refi saves that much

    verdict = None
    if break_even_months is None:
        verdict = ("HIGHER PAYMENT — this refi raises the monthly payment; only makes sense "
                   "as a term-shortening or cash-out strategy, not a savings play.")
    elif horizon_months < break_even_months:
        verdict = (f"STAY: break-even at {break_even_months:.0f} months exceeds your "
                   f"{horizon_months}-month horizon — you'd lose money refinancing.")
    elif break_even_months <= 24:
        verdict = (f"STRONG REFInance: breaks even in {break_even_months:.0f} months; "
                   f"net saving over {horizon_months} months ≈ ${lifetime_delta:,.0f}.")
    else:
        verdict = (f"REFI ONLY IF YOU STAY: break-even {break_even_months:.0f} months; "
                   f"net over {horizon_months} months ≈ ${lifetime_delta:,.0f}.")

    return {
        "loan_amount": round(loan_amount),
        "new_payment": round(new_payment_base, 2),
        "monthly_savings": round(monthly_savings, 2),
        "points_cost": round(points_cost),
        "total_upfront": round(total_upfront),
        "break_even_months": round(break_even_months, 1) if break_even_months else None,
        "horizon_months": horizon_months,
        "net_saving_horizon": round(lifetime_delta),
        "equity_delta_horizon": round(equity_delta),
        "interest_current_horizon": round(cur_paid - (balance - cur_bal)),
        "interest_new_horizon": round(new_paid - (loan_amount - new_bal)),
        "verdict": verdict,
    }


def render(result: dict, label: str) -> str:
    L = []
    bar = "=" * 64
    L += [bar, f"REFI ANALYSIS — {label}", bar]
    L.append(f"New loan amount:        ${result['loan_amount']:,}")
    L.append(f"New monthly payment:    ${result['new_payment']:,.2f}")
    L.append(f"Monthly savings:        ${result['monthly_savings']:,.2f}")
    L.append(f"Upfront (closing+pts):  ${result['total_upfront']:,}")
    L.append(f"Break-even:             "
             + (f"{result['break_even_months']:.0f} months"
                if result['break_even_months'] else "NEVER (payment rises)"))
    L.append(f"Interest over {result['horizon_months']}-mo horizon:")
    L.append(f"  current loan: ${result['interest_current_horizon']:,}")
    L.append(f"  refi loan:    ${result['interest_new_horizon']:,}")
    L.append(f"Net saving over horizon (after upfront): ${result['net_saving_horizon']:,}")
    L.append("")
    L.append(f"VERDICT: {result['verdict']}")
    return "\n".join(L)


def cmd_compare(args) -> None:
    with open(args.offers, encoding="utf-8") as f:
        offers = json.load(f)
    rows = []
    for o in offers:
        r = analyze_offer(
            balance=args.balance, cur_rate=args.current_rate,
            cur_payment=args.current_payment,
            cur_months_left=o.get("cur_months_left", args.months_left),
            new_rate=o["rate"], new_term_years=o.get("term", 30),
            closing=o.get("closing", 4000), points_pct=o.get("points", 0),
            extra_monthly=o.get("extra", 0),
            horizon_years=args.horizon_years)
        r["_rate"] = o["rate"]
        r["_term"] = o.get("term", 30)
        rows.append((o.get("lender", "offer"), r))

    print(f"{'LENDER':12} {'RATE':>6} {'TERM':>5} {'PAYMENT':>10} {'SAVE/MO':>9} "
          f"{'UPFRONT':>9} {'B/E MO':>7} {'NET@HORIZON':>12}")
    for name, r in rows:
        be = f"{r['break_even_months']:.0f}" if r["break_even_months"] else "never"
        print(f"{name:12} {r['_rate'] if '_rate' in r else '':>6} "
              f"{r['_term'] if '_term' in r else '':>5} "
              f"${r['new_payment']:>9,.0f} ${r['monthly_savings']:>8,.0f} "
              f"${r['total_upfront']:>8,.0f} {be:>7} ${r['net_saving_horizon']:>11,.0f}")
    print()
    best = max(rows, key=lambda x: x[1]["net_saving_horizon"])
    print(f"Best by net horizon saving: {best[0]} "
          f"(≈ ${best[1]['net_saving_horizon']:,} over {best[1]['horizon_months']} months)")
    print("Full detail per offer: re-run `analyze` with that offer's numbers.")


def main(argv=None):
    p = argparse.ArgumentParser(description="Refinance break-even & lifetime-cost analyzer")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("analyze")
    a.add_argument("--balance", type=float, required=True, help="current payoff balance")
    a.add_argument("--current-rate", type=float, required=True)
    a.add_argument("--current-payment", type=float, required=True)
    a.add_argument("--months-left", type=int, default=360, help="payments remaining")
    a.add_argument("--new-rate", type=float, required=True)
    a.add_argument("--term", type=int, default=30, help="new loan term years")
    a.add_argument("--closing", type=float, default=4000.0)
    a.add_argument("--points", type=float, default=0.0, help="points as % of loan")
    a.add_argument("--extra-monthly", type=float, default=0.0)
    a.add_argument("--horizon-years", type=float, default=None,
                   help="how long you'll keep the loan (default: new term)")
    a.add_argument("--cash-out", type=float, default=0.0)

    c = sub.add_parser("compare")
    c.add_argument("--balance", type=float, required=True)
    c.add_argument("--current-rate", type=float, required=True)
    c.add_argument("--current-payment", type=float, required=True)
    c.add_argument("--months-left", type=int, default=360)
    c.add_argument("--horizon-years", type=float, default=7)
    c.add_argument("--offers", required=True, help="JSON list of offers")

    args = p.parse_args(argv)

    if args.cmd == "analyze":
        r = analyze_offer(args.balance, args.current_rate, args.current_payment,
                          args.months_left, args.new_rate, args.term,
                          args.closing, args.points, args.extra_monthly,
                          args.horizon_years, args.cash_out)
        print(render(r, f"{args.new_rate}% {args.term}y"))
    else:
        cmd_compare(args)


if __name__ == "__main__":
    main(sys.argv[1:])
