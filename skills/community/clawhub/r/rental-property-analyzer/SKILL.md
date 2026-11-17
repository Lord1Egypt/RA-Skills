---
name: rental-property-analyzer
description: Use when screening a rental property purchase (single-family, duplex, small multifamily) — underwrites the deal with real investor math: NOI, cap rate, cash-on-cash, DSCR, amortization with full payment schedule, 1%-rule and 50%-rule cross-checks, operating-expense-ratio red flags, break-even rent, depreciation tax shield, and stress tests (rent −10%, vacancy 8%, rate +1%) — then names DEAL / THIN / OVERPRICED with the drivers that move the verdict, instead of the listing's pro-forma that pretends vacancies, capex, and management don't exist.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [real-estate, rental, investment, cap-rate, cash-on-cash, dscr]
---

# Rental Property Analyzer (buy-side deal screener)

## Overview
Every listing's pro-forma is a work of optimistic fiction: "market rent" with 0% vacancy, no management fee, no capex reserve, and a "cash-on-cash" computed without closing costs. First-time investors run spreadsheet gymnastics for hours and still miss one of: the 50%-rule cross-check, the DSCR a lender will actually require (1.20–1.25), the depreciation tax shield that quietly rescues marginal deals, or the break-even rent that tells you how much cushion exists.

This skill underwrites a deal from raw inputs in one pass: purchase price, rehab, rent, taxes, insurance, HOA, loan terms, and honest expense assumptions (vacancy %, maintenance %, management %). It produces the full ratio stack, a monthly amortization engine, 10-year cash flow with appreciation and rent growth, sensitivity grid, and a verdict that names which assumptions the outcome hangs on. When the listing pro-forma disagrees with the output, the disagreement is itemized — that's the point.

## When to Use
- Screening a buy-and-hold purchase: SFR, condo, duplex, small multifamily
- Comparing 2–3 candidate properties on identical honest assumptions
- Sanity-checking a wholesaler/agent pro-forma before touring
- Deciding between cash and financed purchase (run both, compare CoC)
- Pre-qualifying a deal before talking to a lender (DSCR preview)

**Don't use for:** short-term rental / Airbnb underwriting (occupancy dynamics differ — different skill), house-hacking roommate math (close but tenant-law-heavy), REIT/fund analysis, or fix-and-flip (no resale-spread engine here — this is the buy-and-hold screener).

## Quick Start
```bash
# A classic candidate: $320k SFR, $2,200 rent, 25% down at 6.5%
python3 scripts/deal_screener.py screen \
    --price 320000 --rehab 8000 --rent 2200 \
    --tax 3600 --ins 1400 --hoa 0 \
    --down-pct 25 --rate 6.5 \
    --vacancy 5 --maintenance 8 --management 8

# Same deal stressed: rent -10%, vacancy 8%, rate +1pt
python3 scripts/deal_screener.py screen --price 320000 --rehab 8000 --rent 2200 \
    --tax 3600 --ins 1400 --down-pct 25 --rate 6.5 --stress

# All-cash variant for comparison
python3 scripts/deal_screener.py screen --price 320000 --rehab 8000 --rent 2200 \
    --tax 3600 --ins 1400 --cash

python3 scripts/deal_screener.py --demo
```

## The Ratio Stack (what each number means and its pass band)
| Metric | Formula | Healthy (SFR/small MF) | Red flag |
|---|---|---|---|
| NOI | rent×12 − opex (vac, maint, mgmt, tax, ins, HOA) | — | — |
| Cap rate | NOI ÷ all-in cost | ≥ mortgage rate + 1.5pt | < mortgage rate (negative leverage) |
| 1%-rule | monthly rent ÷ all-in cost | ≥ 0.7% (1%+ is a unicorn now) | < 0.6% |
| OER | opex ÷ gross scheduled rent | 35–45% | > 50% on SFR (taxes/HOA too heavy) |
| DSCR | NOI ÷ annual debt service | ≥ 1.25 (lender line) | < 1.10 (negative cash flow risk) |
| Cash-on-cash | (NOI − debt service) ÷ cash invested | ≥ 6% | < 4% (T-bills beat it risk-free) |
| Break-even rent | (opex + debt service) ÷ 12 | ≥ 12% under market | within 5% of market (no cushion) |

Depreciation shield: building basis (default 80% of price) ÷ 27.5 yr × marginal rate = annual paper loss that often shelters the cash flow — after-tax CoC printed with it.

## Verdicts
- `DEAL` — cap rate and CoC clear bands, DSCR ≥ 1.25
- `THIN` — one band missed by a little; names the assumption that flips it (usually rent +5% or price −5%)
- `OVERPRICED` — cap rate below financing rate (negative leverage) or negative cash flow at stressed rent
- `NEGATIVE LEVERAGE` — financing makes it worse than cash; printed explicitly because beginners miss it

## Common Pitfalls
1. **Pro-forma vacancy = 0.** Even perfect tenants turn over; 5% minimum, 8% in transient areas.
2. **Capex hidden in "maintenance 8%."** Roofs/furnaces/HVAC lumpy failures average 5–10%/yr alone; the script's maintenance input IS the capex+repairs line — don't double it, don't halve it.
3. **Closing costs forgotten in CoC.** 2–5% of price (title, transfer, lender) is part of cash-in; the script includes `--closing-pct` (default 3%).
4. **Self-managed = free.** Price management anyway (8–10%) — your labor isn't free and future-you may hire it out.
5. **Appreciation worship.** The 10-yr projection prints cash-flow-only returns separately from the appreciation-dependent total; if the deal only works with 4%/yr appreciation, the verdict says so.

## Verification Checklist
- [ ] Rent verified against actual comps (not the listing's "estimated rent")
- [ ] Taxes from the county rate on YOUR purchase price (reassessment!), not seller's bill
- [ ] HOA, special assessments, and insurance quoted for landlord policy
- [ ] Stress scenario run before writing an offer
- [ ] DSCR checked against the actual lender's minimum (Fannie small-loan ≈ 1.20–1.25)

## Example
$320k SFR + $8k rehab, $2,200 rent, 25% down @ 6.5%. Output: all-in $337.6k, NOI ≈ $16.1k → cap 4.76% vs 6.5% loan = **NEGATIVE LEVERAGE**, DSCR 0.86 (below lender line), cash flow −$224/mo, CoC −3% → **OVERPRICED**: needs a ~$45k price cut or +$283/mo rent just to reach the CoC band — both numbers printed by the verdict. The Midwest duplex demo ($185k, $2,400 combined) flips to **DEAL**: cap 9.1%, DSCR 1.66, CoC 12.3%. That's a real screen in 10 seconds instead of a spreadsheet evening.
