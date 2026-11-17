---
name: refi-break-even-ranger
description: "Use when evaluating a mortgage refinance — computes true break-even months from closing costs and points vs monthly savings, net lifetime saving at your actual stay-horizon, compares multiple lender offers side by side, and handles cash-out and term changes; guards against the two classic refi traps (resetting the 30-year clock, ignoring how long you'll keep the loan)."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [mortgage, refinance, break-even, personal-finance, loans]
---

# Refi Break-Even Ranger

## Overview
Refinance decisions look simple and aren't. The advertised math ("save $220/month!") hides four
traps: (1) closing costs and points must be recovered before you sell or move — break-even vs
your actual horizon; (2) refinancing a 7-year-old loan into a new 30-year loan RESETS
amortization, so lower rate ≠ lower lifetime interest; (3) the lowest rate often carries the
highest upfront costs, so offer comparison must be net, not headline rate; (4) cash-out changes
the loan amount and everything downstream.

This skill runs the real amortization math for both loans to a common horizon and returns:
monthly savings, break-even months, interest paid over the horizon by each loan, net saving
after upfront costs, equity-build delta, and a plain verdict (REFI / STAY / ONLY-IF-YOU-STAY).
`compare` ranks multiple lender offers by net horizon saving — which routinely flips the
"obvious" winner.

## When to Use
- "Rates dropped — should I refinance?" (any rate-move question)
- "This lender says I'll save $200/month with $5,600 in costs — good deal?"
- Comparing 3 lender offers with different rates/points/closing costs.
- "Should I refi into a 15-year instead of another 30?"
- Cash-out refi vs HELOC sanity check (payment math side).
- "I might move in 2-3 years — does refinancing still make sense?"

**Don't use for:** purchase-mortgage shopping (different cost structure), reverse mortgages,
or investment-property DSCR analysis (needs tax/rates context beyond scope).

## How It Works — Numbered Steps
1. Gather: current balance, rate, monthly payment (P&I), payments remaining; the offer's rate,
   term, closing costs, points; and your honest stay-horizon in years.
2. Run one offer:
   `python3 scripts/refi_ranger.py analyze --balance 280000 --current-rate 6.5 --current-payment 1768 --new-rate 5.25 --term 30 --closing 4200 --points 0.5 --horizon-years 7`
3. Read BREAK-EVEN first: if it exceeds your horizon months, you LOSE money — verdict says STAY.
4. Read NET SAVING OVER HORIZON: the honest number — interest delta minus upfront costs at
   YOUR horizon, not the full term.
5. For multiple offers, build a JSON list and run `compare` — it ranks by net horizon saving
   and exposes the rate-vs-points tradeoff.
6. If the verdict is REFI, also price the same rate at 15/20-year terms (`--term 15`) —
   sometimes the same payment buys a far shorter clock.

## The Math (what the tool does)

- Amortizing payment: `P·r / (1 − (1+r)^−n)` — same as lenders use.
- Break-even = (closing + points·loan) / monthly savings.
- Horizon comparison: run BOTH loans' amortization for `horizon` months; net saving =
  (current payments − current equity) − (new payments − new equity + upfront). This catches
  the clock-reset trap: a new 30-year loan amortizes slowly at first, so equity-build matters.
- Negative amortization guard: if a payment can't cover interest, the tool flags instead of
  silently computing nonsense.

## Common Pitfalls
1. **Break-even beyond the horizon.** The #1 mistake: 40-month break-even with a 24-month
   stay = guaranteed loss. Always supply `--horizon-years`.
2. **The 30-year reset.** Dropping from 6.5% to 5.25% but restarting amortization at year 7
   can still cost MORE lifetime interest if you keep paying for 23 more years. The horizon
   math exposes this.
3. **Chasing headline rate.** 4.99% with 1.5 points + high closing often loses to 5.375%
   with near-zero costs on an honest horizon — the compare table shows this in one line.
4. **Forgetting PMI.** If refi drops below 20% equity threshold changes PMI status, that's
   ±$100-300/month not in the headline — add it to closing or mentally to savings.
5. **Rolling costs into the loan.** Financed closing costs earn interest for 30 years; the
   tool treats them as upfront — if you finance them, your effective break-even stretches.
6. **Extending term to "save".** A 30→30 refi at lower rate saves; a 30→30 at same rate with
   3 years elapsed "saves" monthly only by re-lengthening the loan. Compare terms honestly.
7. **Ignoring rate-shop window.** Multiple mortgage applications within a ~14-45 day window
   count as ONE credit inquiry — get all offers inside it.

## Example
```
Borrower: balance $280k @ 6.5%, paying $1,768/mo, ~7 years left on the job,
maybe moving in ~7 years... but let's check 2 years too.

$ refi_ranger.py analyze --balance 280000 --current-rate 6.5 --current-payment 1768 \
    --new-rate 5.25 --term 30 --closing 4200 --points 0.5 --horizon-years 7
New payment $1,546 → saves $221.83/mo; upfront $5,600
Break-even: 25 months. Interest over 84 mo: $121,867 → $97,360
NET SAVING over horizon: $7,160 → REFI (only if you stay 25+ months)

Same offer, 2-year horizon: verdict flips to STAY (−$11,162).

Three lenders: compare ranks CU B 5.375%/$2,500 closing FIRST (net $9,039)
above Bank C's flashy 4.99%/$10,700 (net $4,536) — points eat the win.
```

## References
- `references/refi-decision-guide.md` — the decision framework, horizon honesty, PMI/term
  interactions, cash-out chapter, negotiation levers, and the rate-shop credit-window rule.
- `references/amortization-math.md` — formulas, worked examples, clock-reset trap quantified,
  equity curves, and how points pricing maps to break-even.
