#!/usr/bin/env python3
"""Student loan repayment strategy comparator.

Simulates: standard 10-yr, extended 25-yr, graduated 10-yr, income-driven repayment
(IDR 10%/15% with annual recertification, PAYE cap, 20/25-yr forgiveness + tax bomb),
and avalanche payoff with an optional extra monthly payment. PSLF mode tracks
qualifying payments toward the 120 needed and projects tax-free forgiveness.

stdlib only. All money in dollars, monthly steps.
"""
import argparse
import datetime as dt
import json
import math

FPL_2025 = {1: 15060, 2: 20440, 3: 25820, 4: 31200}  # contiguous US, +5380 each extra


def poverty_line(family: int) -> int:
    if family <= 4:
        return FPL_2025[family]
    return FPL_2025[4] + 5380 * (family - 4)


def level_payment(balance: float, apr: float, months: int) -> float:
    r = apr / 12.0
    return balance * r / (1 - (1 + r) ** -months) if r > 0 else balance / months


def amortize(balance, apr, payment_fn, max_months=360):
    """Run month-by-month. payment_fn(month_index, balance)->payment.
    Returns (total_paid, interest, months, end_balance, events)."""
    total = interest = 0.0
    bal = balance
    events = []
    for m in range(1, max_months + 1):
        pay = payment_fn(m, bal)
        i = bal * apr / 12.0
        if pay >= bal + i:  # final payment
            pay = bal + i
            total += pay
            interest += i
            bal = 0.0
            events.append((m, "payoff"))
            return total, interest, m, bal, events
        total += pay
        interest += i
        bal = bal + i - pay  # negative amortization allowed
    return total, interest, max_months, bal, events


def sim_standard(bal, apr):
    p = level_payment(bal, apr, 120)
    t, i, m, e, ev = amortize(bal, apr, lambda m, b: p)
    return dict(name="Standard 10-yr", first=p, last=p, months=m, total=t,
                interest=i, forgiven=0.0, note="PSLF-qualifying")


def sim_extended(bal, apr):
    p = level_payment(bal, apr, 300)
    t, i, m, e, ev = amortize(bal, apr, lambda m, b: p)
    return dict(name="Extended 25-yr", first=p, last=p, months=m, total=t,
                interest=i, forgiven=0.0, note="not PSLF-qualifying")


def sim_graduated(bal, apr):
    # payments grow 8% every 24 months; solve scale k to retire in 120 months
    lo, hi = 0.1, 5.0
    std = level_payment(bal, apr, 120)

    def sched(k):
        return lambda m, b: min(std * 5, max(0.05 * std, k * std * (1.08 ** ((m - 1) // 24))))

    for _ in range(60):
        mid = (lo + hi) / 2
        t, i, mo, e, ev = amortize(bal, apr, sched(mid))
        if mo > 120:
            lo = mid
        else:
            hi = mid
    fn = sched(hi)
    first = fn(1, bal)
    last = fn(120, 0.01)
    t, i, m, e, ev = amortize(bal, apr, fn)
    return dict(name="Graduated 10-yr", first=first, last=last, months=m, total=t,
                interest=i, forgiven=0.0, note="steps up every 2 yrs; not PSLF")


def sim_idr(bal, apr, agi, family, pct, months_to_forgive, marginal,
            growth=0.03, payments_made=0, pslf=False, extra=0.0):
    cap = level_payment(bal, apr, 120)
    state = {"agi": agi, "year": 0, "pay": None}
    qual = payments_made

    def payment(m, b):
        if state["pay"] is None or (m - 1) % 12 == 0:
            state["year"] += 1
            disc = max(0.0, state["agi"] - 1.5 * poverty_line(family))
            state["pay"] = min(cap, disc * (pct / 100.0) / 12.0)
            state["agi"] *= 1 + growth
        return state["pay"] + (0 if pslf else extra)

    t, i, mo, end, ev = amortize(bal, apr, payment, max_months=months_to_forgive - payments_made)
    if end > 1.0:  # forgiveness event
        forgiven = end
        bomb = forgiven * (marginal / 100.0) if not pslf else 0.0
        note = f"PSLF: tax-FREE forgiveness" if pslf else f"tax bomb ≈ ${bomb:,.0f} ({marginal}%)"
        return dict(name=f"IDR {pct:.0f}% ({months_to_forgive//12}-yr)",
                    first=payment(1, bal), last=state["pay"], months=mo,
                    total=t + bomb, interest=i, forgiven=forgiven,
                    bomb=bomb, note=note)
    return dict(name=f"IDR {pct:.0f}% pays off", first=payment(1, bal), last=state["pay"],
                months=mo, total=t, interest=i, forgiven=0.0, note="paid in full")


def sim_avalanche(bal, apr, extra):
    p = level_payment(bal, apr, 120) + extra
    t, i, m, e, ev = amortize(bal, apr, lambda m, b: p)
    return dict(name=f"Avalanche +${extra:.0f}/mo", first=p, last=p, months=m,
                total=t, interest=i, forgiven=0.0,
                note=f"fastest payoff" if extra else "standard pace")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--balance", type=float, required=True)
    ap.add_argument("--rate", type=float, required=True, help="APR %, e.g. 6.2")
    ap.add_argument("--grad", action="store_true", help="any graduate loan -> 25-yr IDR horizon")
    ap.add_argument("--agi", type=float, default=45000.0)
    ap.add_argument("--family", type=int, default=1)
    ap.add_argument("--marginal", type=float, default=22.0, help="marginal tax rate %")
    ap.add_argument("--growth", type=float, default=3.0, help="annual income growth %")
    ap.add_argument("--extra", type=float, default=0.0, help="extra $/mo for avalanche")
    ap.add_argument("--pslf", action="store_true", help="PSLF track: count qualifying payments")
    ap.add_argument("--payments-made", type=int, default=0, help="qualifying payments already made")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    bal, apr = args.balance, args.rate / 100.0
    horizon = 300 if args.grad else 240

    rows = [
        sim_standard(bal, apr),
        sim_extended(bal, apr),
        sim_graduated(bal, apr),
        sim_idr(bal, apr, args.agi, args.family, 10, horizon, args.marginal,
                args.growth / 100.0, args.payments_made, args.pslf, 0),
        sim_idr(bal, apr, args.agi, args.family, 15, horizon, args.marginal,
                args.growth / 100.0, args.payments_made, args.pslf, 0),
    ]
    if args.extra > 0:
        rows.append(sim_avalanche(bal, apr, args.extra))
    if args.pslf:
        # on PSLF the guidance is: minimum payment, no extra
        pslf_row = sim_idr(bal, apr, args.agi, args.family, 10, 120, 0,
                           args.growth / 100.0, args.payments_made, True, 0)
        pslf_row["name"] = "IDR on PSLF track (120 qual.)"
        rows.append(pslf_row)

    today = dt.date.today()
    def when(months):
        d = today
        for _ in range(months):
            d = (dt.timedelta(days=31) + d).date() if isinstance(d, dt.timedelta) else d
        # simple month add
        y, mth = today.year + (today.month - 1 + months) // 12, (today.month - 1 + months) % 12 + 1
        return f"{y}-{mth:02d}"

    if args.json:
        out = [dict(r, date=when(r["months"])) for r in rows]
        print(json.dumps(out, indent=2))
        return

    hdr = f"{'Strategy':<24}{'Payment 1st/last':>20}{'Payoff/Forgiven':>18}{'Total paid':>13}{'Interest':>11}"
    print(hdr)
    print("-" * len(hdr))
    for r in sorted(rows, key=lambda x: x["total"]):
        print(f"{r['name']:<24}{r['first']:>10,.0f}/{r['last']:>7,.0f}  {when(r['months']):>15}"
              f"{r['total']:>13,.0f}{r['interest']:>11,.0f}")
        tail = f"   forgiven ${r['forgiven']:,.0f}" if r.get("forgiven") else ""
        if r.get("bomb"):
            tail += f", tax bomb ${r['bomb']:,.0f} net"
        print(f"   ↳ {r['note']}{tail}")

    best = min(rows, key=lambda x: x["total"])
    print(f"\nVERDICT: {best['name']} — lowest total outlay (${best['total']:,.0f}), "
          f"done {when(best['months'])}.")
    if args.pslf:
        print("  PSLF: pay the MINIMUM; every extra $1 is $1 less forgiven. Never refinance federal→private.")
    disc = max(0.0, args.agi - 1.5 * poverty_line(args.family))
    print(f"  (Discretionary income: ${disc:,.0f}/yr → IDR floor payment "
          f"${disc*0.10/12:,.0f}/mo at 10%)")
    print("  Estimates only: rules (SAVE/REPAYE) and poverty lines change; recertify annually.")


if __name__ == "__main__":
    main()
