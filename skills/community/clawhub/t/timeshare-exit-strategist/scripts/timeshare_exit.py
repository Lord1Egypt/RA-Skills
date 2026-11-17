#!/usr/bin/env python3
"""timeshare-exit-strategist — keep-vs-exit math, contract classification, and
exit-company scam scoring. Stdlib only.

Subcommands: keep, contract, scamcheck, --demo
"""
import argparse


def cmd_keep(a) -> None:
    print(f"=== KEEP vs EXIT: ${a.annual_fee:,.0f}/yr fees, {a.growth*100:.1f}% growth, "
          f"${a.usage_value:,.0f}/yr realized usage, {a.years}-yr horizon\n")
    print(f"{'Year':<6}{'Fee':>9}{'Fee cum.':>11}{'Value cum.':>12}{'Net burn':>11}")
    fee = a.annual_fee
    fee_cum = val_cum = 0.0
    crossover = None
    rows = []
    for y in range(1, a.years + 1):
        fee_cum += fee
        val_cum += a.usage_value
        net = fee_cum - val_cum
        rows.append((y, fee, fee_cum, val_cum, net))
        fee *= (1 + a.growth)
    for y, f, fc, vc, net in rows:
        print(f"{y:<6}{f:>9,.0f}{fc:>11,.0f}{vc:>12,.0f}{net:>11,.0f}")
    # crossover: first year net burn exceeds exit cost (keeping already lost more)
    for y, f, fc, vc, net in rows:
        if net > a.exit_cost:
            crossover = y
            break
    lifetime_fee = fee_cum
    print(f"\nCumulative fees over {a.years} yrs: ${lifetime_fee:,.0f}")
    print(f"Cumulative usage value:            ${val_cum:,.0f}")
    print(f"Net burn by keeping:               ${lifetime_fee - val_cum:,.0f}")
    print(f"One-time exit cost modeled:        ${a.exit_cost:,.0f}")
    if crossover:
        print(f"\nCROSSOVER: by year {crossover}, keeping has burned more than "
              f"the ${a.exit_cost:,.0f} exit — every year after that is pure loss.")
        verdict = "EXIT WINS ECONOMICALLY" if crossover <= 10 else "KEEP WHILE USAGE HOLDS, EXIT BEFORE FEES ESCALATE"
    else:
        verdict = "KEEP — your realized usage value exceeds fees across the horizon"
    print(f"VERDICT: {verdict}")
    print("\nReality checks: (1) fees historically grow 5-8%/yr — 2-3x inflation;")
    print("(2) perpetual contracts pass to heirs unless disclaimed in time;")
    print("(3) resale value of most weeks is ~$0; never buy 'exit services' before")
    print("asking the developer's owner services about their own deed-back program.")


def cmd_contract(a) -> None:
    print("=== Contract classification\n")
    t = a.type.lower()
    if t == "deeded":
        print("DEEDED WEEK: a real-property interest. It does NOT die with you —")
        print("it passes to your estate/heirs WITH the fee obligation. Resale is")
        print("possible but the market for most resorts is ~zero. Exit levers:")
        print("developer deed-back, resale giveaway (you pay closing), attorney")
        print("if fraud-at-sale is provable, or default (credit hit, lien rules vary).")
        heir_risk = "HIGH — obligations transfer to heirs"
    elif t == "points":
        print("POINTS: a license/membership interest, not real property. Usually")
        print("terminates at death in SOME programs, but many have estate-transfer")
        print("clauses for the fee obligation — read the program's 'successor'")
        print("language. Exit levers: developer take-back, program surrender (some")
        print("burn points-to-exit offers), attorney for sale-fraud or")
        print("misrepresented 'investment' pitches.")
        heir_risk = "VARIES — check successor-membership clause"
    elif t == "rtu":
        print("RIGHT-TO-USE: a term contract with an end date. Count the years —")
        print("the whole question is whether fees-for-remaining-years beat the exit")
        print("cost. Many RTU contracts auto-renew unless cancelled in a notice")
        print("window: find YOUR window and use certified mail.")
        heir_risk = "MEDIUM — term may expire or transfer"
    else:
        print("Unknown type — read the first page of your contract for 'deed',")
        print("'points', 'license', or 'right to use ... until [date]'.")
        heir_risk = "UNKNOWN"
    if a.perpetual == "yes":
        print(f"\nPerpetual flag: YES. {heir_risk}. If inherited recently, disclaimer")
        print("deadlines are short (~9 months federal; state varies) — check")
        print("references/inheritance-playbook.md NOW.")
    if a.paid_off == "no":
        print("\nLoan outstanding: default consequences depend on whether the loan")
        print("is purchase-money (some states bar deficiency) — verify before any")
        print("walk-away decision.")
    print("\nPriority order: 1) developer exit program (ask in writing) 2) resale")
    print("via licensed closing co. 3) licensed timeshare attorney 4) calculated")
    print("default. NEVER upfront-fee 'cancellation' companies (run scamcheck).")


def cmd_scamcheck(a) -> None:
    flags = []
    if a.upfront_fee >= 3000:
        flags.append(f"Large upfront fee ${a.upfront_fee:,.0f} (the #1 industry marker)")
    g = (a.guarantees or "").lower()
    if "any" in g or "guarant" in g or "cancel" in g:
        flags.append(f"Guarantee language: {a.guarantees!r} — no one can guarantee "
                     "cancellation of an arbitrary contract")
    if a.timeline_months > 12:
        flags.append(f"Timeline {a.timeline_months} months — designed to outlast "
                     "your credit-card chargeback window (~120 days)")
    if a.upfront_fee >= 5000 and (a.money_back or "").lower().startswith("y"):
        flags.append("Money-back 'guarantee' on a $5k+ fee — historically "
                     "conditions are engineered to be unmeetable")
    print(f"=== Exit-company offer score: {len(flags)} red flags\n")
    for i, f in enumerate(flags, 1):
        print(f"  FLAG {i}: {f}")
    if len(flags) >= 3:
        print("\nVERDICT: SCAM LIKELY — do not pay. Report: your state AG "
              "consumer protection + reportfraud.ftc.gov.")
        print("What they usually do: take the fee, wait you out, then mail you a")
        print("'transfer' that the developer never accepted, or just go dark.")
    elif flags:
        print("\nVERDICT: SUSPICIOUS — verify the named attorney's bar license,")
        print("get all promises in writing, and never pay before services render.")
    else:
        print("\nVERDICT: No standard markers — still confirm attorney licensure")
        print("and avoid large retainers; ask what happens at month 6 if nothing.")
    print("\nReal path: developer deed-back question in writing first. It's free.")


def run_demo() -> None:
    import types
    print("############ DEMO: the classic Orlando week ############\n")
    cmd_keep(types.SimpleNamespace(annual_fee=1200, growth=0.06, usage_value=500,
                                   years=20, exit_cost=4000))
    print("\n############ DEMO: inherited points contract ############\n")
    cmd_contract(types.SimpleNamespace(type="points", perpetual="yes", paid_off="yes"))
    print("\n############ DEMO: the $6,500 exit-company offer ############\n")
    cmd_scamcheck(types.SimpleNamespace(upfront_fee=6500,
                                        guarantees="cancel any timeshare contract",
                                        timeline_months=18, money_back="yes"))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd")
    pk = sub.add_parser("keep")
    pk.add_argument("--annual-fee", type=float, required=True)
    pk.add_argument("--growth", type=float, default=0.06)
    pk.add_argument("--usage-value", type=float, default=400)
    pk.add_argument("--years", type=int, default=20)
    pk.add_argument("--exit-cost", type=float, default=4000)
    pc = sub.add_parser("contract")
    pc.add_argument("--type", required=True, choices=["deeded", "points", "rtu"])
    pc.add_argument("--perpetual", default="yes", choices=["yes", "no"])
    pc.add_argument("--paid-off", default="yes", choices=["yes", "no"])
    ps = sub.add_parser("scamcheck")
    ps.add_argument("--upfront-fee", type=float, required=True)
    ps.add_argument("--guarantees", default="")
    ps.add_argument("--timeline-months", type=int, default=18)
    ps.add_argument("--money-back", default="no")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args()
    if a.demo:
        run_demo()
    elif a.cmd == "keep":
        cmd_keep(a)
    elif a.cmd == "contract":
        cmd_contract(a)
    elif a.cmd == "scamcheck":
        cmd_scamcheck(a)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
