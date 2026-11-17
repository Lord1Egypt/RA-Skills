# Refinance Decision Guide

## The Only Question That Matters

**How long will you keep this loan?** (Not the house — the loan. Selling, or refinancing
again, ends it.) Every refi number is downstream of that horizon:

- Break-even (months) = upfront costs ÷ monthly savings.
- If horizon < break-even → you lose money, full stop.
- If horizon > break-even → the net saving is roughly (horizon − break-even) × monthly savings,
  adjusted for the amortization-clock reset.

Estimate the horizon honestly: job/family plans, realistic move probability, and the chance
rates drop again (you can refi twice — each refi stands on its own math).

## The Five Numbers to Demand From Every Lender

1. Rate (locked, with lock period)
2. Points (as % of loan) — and the no-points rate from the SAME lender
3. Itemized closing costs (origination, underwriting, appraisal, title, escrow)
4. Estimated cash-to-close (and what's prepaid vs true cost)
5. Rate-lock terms (days, float-down option, cost)

"Zero closing cost" offers exist: the lender charges a higher rate and keeps the difference
via servicing/YSP. They can be optimal for short horizons — the compare table catches this
when you enter them honestly.

## Offers JSON for `compare`

```json
[
 {"lender": "Bank A", "rate": 5.25,  "term": 30, "closing": 4200, "points": 0.5},
 {"lender": "CU B",   "rate": 5.375, "term": 30, "closing": 2500, "points": 0},
 {"lender": "Bank C", "rate": 4.99,  "term": 30, "closing": 6500, "points": 1.5}
]
```

Optional keys: `"extra"` (extra monthly payment), `"cur_months_left"`. Ranking is by
**net saving at YOUR horizon** — the metric that pays for your vacation, not the lender's
marketing.

## Term Strategy

- **Same-term refi (30→30):** payment drops; lifetime interest can rise if you're years in
  (clock reset). Fix: keep paying the OLD payment as extra (`--extra-monthly`) — you get the
  lower rate AND the old payoff date.
- **Term shortening (30→15):** rate usually drops 0.25-0.5% more; payment often RISES. This is
  a wealth strategy, not a cash-flow one — the verdict line will say HIGHER PAYMENT; that's
  correct, not a bug.
- **Term lengthening (rare, hardship):** lowers payment but maximizes lifetime interest;
  consider loan-modification programs first if hardship-driven.

## Cash-Out Refinance

- Loan amount rises (tool: `--cash-out`), LTV and PMI risk rise, rate is typically +0.125-0.5%
  vs no-cash quotes.
- vs HELOC/HEL: cash-out refi replaces your whole rate (good when refi-rate < current);
  HELOC adds a second lien at a floating rate (good when current first is already low).
  Rule of thumb: if a straight refi already makes sense, cash-out rides along cheaply; if not,
  a HELOC keeps the low first-mortgage rate untouched.
- Cash-out for debt consolidation: the danger is converting 5-year consumer debt into
  30-year amortizing debt — lower payment, massively higher lifetime cost. The horizon math
  shows it mercilessly.

## PMI Interactions

- Refinancing re-measures LTV. Below 80% → no PMI; 80-90% → PMI or lender-paid variant;
  above, expect pricing hits.
- PMI of $150/mo is effectively $150 of "monthly savings" if the refi removes it — include it
  by adding it to the savings side (lower the offer's effective rate or note it separately).

## Rate Shopping Mechanics

- All mortgage credit pulls within a 14-day window (45 days under newer FICO versions) count
  as ONE inquiry. Get 3+ Loan Estimates in the same window.
- Loan Estimates are standardized — fees are directly comparable line-by-line.
- Negotiation levers: the lender's own no-points quote vs points quote; matching a competitor's
  Loan Estimate; asking for a float-down if rates drop during escrow.
- Lock discipline: lock when you have a real number and a close date; long locks (60-90 days)
  cost rate or fees.

## Process Checklist (after the math says GO)

1. Pull 3 Loan Estimates inside the credit window.
2. Verify breakeven vs horizon with FINAL numbers (appraisal can move LTV/PMI).
3. Lock; calendar the lock expiry vs closing date.
4. Do not open credit lines or move big money during underwriting.
5. At closing, compare the Closing Disclosure to the Loan Estimate — fees drift is normal
   small; big drift = challenge it.
