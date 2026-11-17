#!/usr/bin/env python3
"""
Solar Quote Verifier — recompute a solar proposal's economics honestly:
$/W pricing, production sanity, real payback (degradation + inverter +
escalation), loan/PPA traps, roof-age and ITC conflicts.

Usage:
  solar_quote_check.py --demo
  solar_quote_check.py --kw 8.4 --cost 32760 --quoted-kwh 13500 \
      --rate 0.17 --region southwest --orientation sw --roof-age 8
  solar_quote_check.py --kw 8.4 --cost 32760 --quoted-kwh 13500 \
      --rate 0.17 --region southwest --loan-apr 6.9 --loan-years 20
  solar_quote_check.py --kw 8.4 --ppa-rate 0.13 --ppa-escalator 2.9 \
      --rate 0.17 --region southwest
"""
import argparse
import sys

REGIONS = {  # annual avg peak sun-hours/day
    "southwest": 6.0, "west": 5.0, "midwest": 4.4, "southeast": 4.8,
    "northeast": 4.2, "northwest": 3.6, "alaska": 2.8, "hawaii": 5.5,
}
ORIENT = {"s": 1.00, "se": 0.96, "sw": 0.96, "e": 0.86, "w": 0.86,
          "n": 0.60, "south": 1.00}
DERATE = 0.84
UTILITY_ESC = 0.025      # long-run US average
DEGRADATION = 0.005      # 0.5%/yr
INVERTER_YEAR = 13
INVERTER_COST_PER_W = 0.35
ITC = 0.30
OM_PER_YEAR = 150
PPA_UTILITY_CROSS = "PPA escalator outpaces utility rate growth"


def band_pw(pw: float) -> str:
    if pw <= 2.50:
        return "EXCEPTIONAL (verify equipment/warranty quality)"
    if pw <= 3.50:
        return "FAIR (market range)"
    if pw <= 4.00:
        return "OVERPRICED (negotiate or bid against)"
    return "WALK-AWAY (way above market)"


def production_model(kw, sun_hours, orient_mult):
    return kw * sun_hours * 365 * DERATE * orient_mult


def payback(net_cost, annual_kwh, rate, years=30):
    """Return (payback_year_or_None, total_net_by_25y, schedule notes)."""
    cum = -net_cost
    payback_year = None
    for y in range(1, years + 1):
        prod = annual_kwh * (1 - DEGRADATION) ** (y - 1)
        value = prod * rate * (1 + UTILITY_ESC) ** (y - 1)
        cum += value - OM_PER_YEAR
        if y == INVERTER_YEAR:
            # cost arrives in real dollars; keep simple nominal
            cum -= 0  # handled by caller adding inverter to net_cost pool
        if payback_year is None and cum >= 0:
            payback_year = y
    return payback_year, cum


def check(args):
    out = []
    warn = []
    ok = True

    kw = args.kw
    rate = args.rate

    # ---- PPA / lease sanity (no system cost needed) ----
    if args.ppa_rate:
        out.append("PPA / LEASE SANITY")
        out.append("=" * 60)
        out.append(f"PPA start rate ${args.ppa_rate:.3f}/kWh vs utility "
                   f"${rate:.3f}/kWh "
                   f"(savings {1 - args.ppa_rate / rate:.0%} of offset kWh)")
        esc = (args.ppa_escalator or 2.9) / 100.0
        cross = None
        for y in range(1, 26):
            ppa = args.ppa_rate * (1 + esc) ** (y - 1)
            util = rate * (1 + UTILITY_ESC) ** (y - 1)
            if ppa >= util:
                cross = y
                break
        if cross:
            warn.append(f"PPA rate catches utility rate in year {cross} "
                        f"({PPA_UTILITY_CROSS}) — after that the 'savings' "
                        f"are negative. Escalator "
                        f"{args.ppa_escalator or 2.9}% > utility "
                        f"{UTILITY_ESC:.1%}.")
            ok = False
        else:
            out.append(f"escalator {args.ppa_escalator or 2.9}%/yr stays "
                       f"under utility glide path for 25 yr — plausible")
        out.append("remember: lease/PPA company takes the 30% ITC, and lease "
                   "transfer can complicate a home sale")
        out.append("")
        verdict = "RED-FLAG" if cross else "PLAUSIBLE"
        out.append(f"VERDICT: {verdict}")
        return "\n".join(out + [""] + [f"  ! {w}" for w in warn]), ok

    # ---- purchase / loan analysis ----
    if not (kw and args.cost and args.quoted_kwh and rate):
        raise SystemExit("need --kw --cost --quoted-kwh --rate "
                         "(or --ppa-rate)")

    pw = args.cost / (kw * 1000)
    out.append("PRICE CHECK")
    out.append("=" * 60)
    out.append(f"system: {kw:g} kW DC for ${args.cost:,.0f} "
               f"=> ${pw:.2f}/W pre-incentive")
    price_v = band_pw(pw)
    out.append(f"band: {price_v}")
    if pw > 3.5:
        ok = False
        warn.append(f"${pw:.2f}/W is above the $2.50-3.50/W market band — "
                    "get competing bids or push back; every $0.10/W on "
                    f"{kw:g} kW is ${kw * 100:.0f}.")
    if pw > 4.0:
        warn.append("Walk-away pricing: request itemization (panels, "
                    "inverter, racking, labor, PERMITTING) — dealer-fee "
                    "loans hide 10-15% in here.")

    # production
    sun = args.sun_hours or REGIONS.get(args.region, 4.4)
    om = ORIENT.get((args.orientation or "s").lower(), 1.0)
    model_kwh = production_model(kw, sun, om)
    out.append("")
    out.append("PRODUCTION CHECK")
    out.append("-" * 60)
    out.append(f"region '{args.region}' sun-hours {sun} x derate {DERATE} "
               f"x orientation {om:.2f}")
    out.append(f"model: {model_kwh:,.0f} kWh/yr   quoted: "
               f"{args.quoted_kwh:,.0f} kWh/yr")
    over = (args.quoted_kwh - model_kwh) / model_kwh
    if over > 0.10:
        ok = False
        warn.append(f"Quoted production {over:.0%} above physical model — "
                    "RED FLAG. Ask for PVWatts inputs (azimuth, tilt, shade, "
                    "weather file). Overstated production inflates savings "
                    "and shrinks quoted payback dishonestly.")
        price_v = "RED-FLAG (production overstated)"
    elif over < -0.15:
        out.append(f"quoted is {over:.0%} BELOW model — conservative "
                   "(fine, maybe shading not declared)")
    else:
        out.append(f"quoted within {over:+.0%} of model — realistic")

    # net cost after ITC
    itc_eligible = args.no_itc is False
    net = args.cost * ((1 - ITC) if itc_eligible else 1.0)
    inverter_cost = kw * 1000 * INVERTER_COST_PER_W
    out.append("")
    out.append("HONEST PAYBACK")
    out.append("-" * 60)
    if itc_eligible:
        out.append(f"net cost after 30% ITC: ${net:,.0f} "
                   "(ASSUMES you can absorb the credit)")
    else:
        out.append(f"net cost, NO ITC (flagged ineligible): ${net:,.0f}")
    total_pool = net + (0 if args.microinverters else inverter_cost)
    if args.microinverters:
        out.append("inverter replacement: SKIPPED (microinverters w/ 25y "
                   "warranty assumed)")
    else:
        out.append(f"+ future string-inverter replacement ~year "
                   f"{INVERTER_YEAR}: ${inverter_cost:,.0f} "
                   "(0.35/W; skip if microinverters w/ 25y warranty)")
    use_kwh = min(args.quoted_kwh, model_kwh)
    pb, cum25 = payback(total_pool, use_kwh, rate)
    out.append(f"year-1 value: {use_kwh:,.0f} kWh x ${rate:.2f} = "
               f"${use_kwh * rate:,.0f}")
    out.append(f"model says: payback year {pb if pb else '>30'}, "
               f"25-yr net ${cum25:,.0f} "
               f"(incl. ${OM_PER_YEAR}/yr O&M, {UTILITY_ESC:.1%} rate esc, "
               f"{DEGRADATION:.1%} degradation)")
    if args.quoted_payback:
        q = args.quoted_payback
        honest = pb if pb else 99
        out.append(f"quote claims payback year {q} "
                   f"{'— consistent' if abs(q - honest) <= 1 else '— OPTIMISTIC vs model'}")
        if honest - q >= 3:
            ok = False
            warn.append(f"Quoted payback {q} yr vs honest {honest} yr: the "
                        "gap is usually missing inverter, degradation, O&M, "
                        "or inflated production.")
    if cum25 < 0:
        ok = False
        warn.append("25-yr net is NEGATIVE at these numbers — system never "
                    "pays back at this price/rate combination.")

    # loan x-ray
    if args.loan_apr:
        out.append("")
        out.append("LOAN X-RAY")
        out.append("-" * 60)
        n = args.loan_years or 20
        r = args.loan_apr / 100 / 12
        m = net * r * (1 + r) ** (n * 12) / ((1 + r) ** (n * 12) - 1)
        out.append(f"{args.loan_apr}% x {n} yr on ${net:,.0f} net: "
                   f"${m:,.0f}/mo, total ${m * n * 12:,.0f}")
        out.append("dealer-fee test: ask for the CASH price of the same "
                   "system; if cash < loan principal by >5%, the 'low APR' "
                   "is prepaid in the price")
        year1_val = use_kwh * rate
        if m * 12 > year1_val:
            warn.append(f"Loan payments ${m * 12:,.0f}/yr exceed year-1 "
                        f"solar value ${year1_val:,.0f}/yr — you are cash-"
                        "negative from day one (bet entirely on rate "
                        "escalation).")

    # roof conflict
    if args.roof_age and args.roof_age >= 10:
        ok = False
        warn.append(f"Roof is {args.roof_age} yr old; panels warranted 25 yr, "
                    "asphalt shingle lives 20-25 yr. Reroof first, or budget "
                    "$2,000-6,000 remove-and-reinstall mid-life.")

    verdict = "FAIR" if ok else ("OVERPRICED" if pw > 3.5 else "RED-FLAG")
    out.append("")
    out.append(f"VERDICT: {price_v if not ok else verdict}")
    if warn:
        out.append("")
        out.append("FLAGS:")
        out.extend(f"  ! {w}" for w in warn)
    return "\n".join(out), ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--kw", type=float, help="system DC kW")
    ap.add_argument("--cost", type=float, help="gross installed cost USD")
    ap.add_argument("--quoted-kwh", type=float)
    ap.add_argument("--rate", type=float, help="utility $/kWh")
    ap.add_argument("--region", default="midwest", choices=sorted(REGIONS))
    ap.add_argument("--sun-hours", type=float,
                    help="override region insolation")
    ap.add_argument("--orientation", default="s",
                    help="s/se/sw/e/w/n azimuth class")
    ap.add_argument("--no-itc", action="store_true",
                    help="you cannot use the federal credit")
    ap.add_argument("--microinverters", action="store_true",
                    help="skip inverter-replacement cost")
    ap.add_argument("--loan-apr", type=float)
    ap.add_argument("--loan-years", type=int)
    ap.add_argument("--ppa-rate", type=float,
                    help="PPA/lease $/kWh offer")
    ap.add_argument("--ppa-escalator", type=float, default=2.9)
    ap.add_argument("--quoted-payback", type=float,
                    help="payback year claimed by proposal")
    ap.add_argument("--roof-age", type=float)
    args = ap.parse_args(argv)

    if args.demo:
        print("DEMO 1 — overstated production + high $/W "
              "(classic door-knocker)")
        print("~" * 60)
        d1 = argparse.Namespace(kw=9.6, cost=44160, quoted_kwh=16800,
                                rate=0.16, region="midwest", sun_hours=None,
                                orientation="w", no_itc=False,
                                microinverters=False, loan_apr=None,
                                loan_years=None, ppa_rate=None,
                                ppa_escalator=2.9, quoted_payback=8,
                                roof_age=12)
        print(check(d1)[0])
        print()
        print("DEMO 2 — PPA with hot escalator")
        print("~" * 60)
        d2 = argparse.Namespace(kw=8.4, cost=None, quoted_kwh=None,
                                rate=0.17, region="southwest", sun_hours=None,
                                orientation="s", no_itc=False,
                                microinverters=False, loan_apr=None,
                                loan_years=None, ppa_rate=0.145,
                                ppa_escalator=3.5, quoted_payback=None,
                                roof_age=None)
        print(check(d2)[0])
        return 0
    print(check(args)[0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
