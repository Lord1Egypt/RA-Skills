---
name: solar-quote-verifier
description: Use when a solar installer sends a proposal or a sales rep pitches panels — verifies $/W pricing, production estimates for your region and roof orientation, real payback with degradation + inverter replacement + rate escalation, loan vs cash vs lease/PPA traps, ITC credit eligibility, and roof-age conflicts. Outputs FAIR / OVERPRICED / RED-FLAG verdicts with the corrected numbers.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [solar, home-energy, payback, quotes, financing, roof]
---

# Solar Quote Verifier

## Overview

Solar proposals are engineered optimism: production modeled at perfect
orientation, payback quoted before inverter replacement, financing that hides
a 7% dealer fee, "free panels" leases with escalators that outpace utility
rates. `scripts/solar_quote_check.py` re-computes the quote's economics from
first principles — regional insolation, orientation derates, panel
degradation, inverter replacement at year 12–15, utility rate escalation,
ITC 30% credit — and flags the sales-tactics layer (overstated production,
$/W above market, roof older than the loan, lease escalators).

## When to Use

- An installer sends a proposal (email PDF numbers → this skill).
- A door-to-door / cold-call solar pitch with "eliminate your bill".
- Comparing 2–3 competing quotes and needing a like-for-like scorecard.
- Reviewing a lease/PPA offer against buying.

**Don't use for:** off-grid system design (battery sizing is a different
instrument), commercial/C&I scale (>100 kW), or countries with wildly
different subsidy regimes — the tool's tables are US-centric; regional
insolation can be overridden.

## How It Works

1. **$/W sanity**: installed cost ÷ DC wattage vs 2026-ish residential band
   ($2.50–3.50/W pre-ITC; >$4/W = overpriced; >$5/W = walk away).
2. **Production check**: quoted kWh ÷ (kW × 365) vs regional sun-hours ×
   0.84 system derate. Overstatement >10% = RED FLAG (the #1 proposal lie).
3. **Payback, honestly**: annual value of production at your rate, escalated
   2.5%/yr, minus 0.5%/yr degradation, minus one inverter replacement
   (year 12–15, ~$0.35/W), ÷ net cost after ITC. Compare to quoted payback.
4. **Financing X-ray**: dealer-fee loans (APR vs "low payment"), lease/PPA
   escalator (2.9%/yr typical) vs utility escalation (2.5%) — if the escalator
   runs hotter, year-15 lease payments exceed grid parity.
5. **Conflict checks**: roof age (asphalt shingle >10 yr old + 25-yr panels =
   reroof-first math), ITC eligibility (you must have tax appetite; lease/PPA
   gives the credit to the company), net-metering changes.
6. **Verdict**: FAIR / OVERPRICED / RED-FLAG with the three biggest levers.

## Using the Script

```bash
# Demo: a typical overstated proposal
python3 scripts/solar_quote_check.py --demo

# Check a real quote (all costs pre-incentive, USD)
python3 scripts/solar_quote_check.py \
  --kw 8.4 --cost 32760 --quoted-kwh 13500 \
  --rate 0.17 --region southwest --orientation s --pitch 30

# Loan scenario
python3 scripts/solar_quote_check.py --kw 8.4 --cost 32760 \
  --quoted-kwh 13500 --rate 0.17 --region southwest \
  --loan-apr 6.9 --loan-years 20

# Lease/PPA sanity
python3 scripts/solar_quote_check.py --kw 8.4 --ppa-rate 0.13 \
  --ppa-escalator 2.9 --rate 0.17 --region southwest
```

## Worked Example

8.4 kW at $32,760 ($3.90/W — overpriced band) quoting 13,500 kWh/yr in the
southwest: realistic production ≈ 8.4 × 6.0 sun-h × 365 × 0.84 ≈ 15,460 kWh
(quoting LOW here — rare), but at $3.90/W the honest payback is ~13 yr cash
vs the quoted 9 yr once the year-13 inverter ($2,940) and 2.5%/yr rate
escalation are modeled. Verdict: OVERPRICED — negotiate to $3.20/W or get
competing bids; the system itself pencils out.

## Common Pitfalls

1. **Believing quoted production.** It's modeled at ideal azimuth/tilt with
   clean panels and no shade. Recompute from regional sun-hours × 0.84.
2. **Payback without the inverter.** String inverters die at 12–15 yr inside
   a 25-yr finance term; microinverters have better warranties but cost more
   per W up front.
3. **The dealer-fee loan.** "2.99% financing!" usually adds 10–15% to the
   price. Compare CASH price vs LOAN price on the same system.
4. **Lease/PPA escalator ≥ utility escalation.** 2.9%/yr escalator on a
   2.5%/yr utility glide path means the "savings" shrink every year and can
   go negative — the classic PPA trap.
5. **ITC you can't use.** The 30% federal credit needs tax liability; if you
   can't absorb it, your net cost is a third higher (or the credit belongs to
   the lease company — that's why their pitch "includes" it).
6. **Old roof, new panels.** Removing/reinstalling panels to reroof costs
   $2,000–6,000. Panels outliving a 12-yr-old shingle roof is a real conflict.

## Verification Checklist

- [ ] $/W computed and banded (fair/overpriced/walk-away).
- [ ] Production estimate independently recomputed, not trusted.
- [ ] Payback includes degradation + inverter replacement + escalation.
- [ ] Loan and PPA modes disclose their respective traps.
- [ ] Roof-age and ITC-eligibility conflict checks surfaced.
- [ ] Verdict names the three biggest levers, not just a number.
