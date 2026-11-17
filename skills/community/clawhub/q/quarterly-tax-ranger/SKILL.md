---
name: quarterly-tax-ranger
description: Use when you owe quarterly estimated taxes (freelance, 1099, gig, small business) — computes safe-harbor payments across the four IRS due dates (Apr 15 / Jun 16 / Sep 15 / Jan 15), warns on underpayment penalties, handles uneven income with the annualized-income method (Form 2210 Schedule AI), and builds a self-employment tax + QBI + deduction ledger so April 15 is bookkeeping, not archaeology.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [taxes, freelance, 1099, self-employment, quarterly, estimated-payments]
---

# Quarterly Tax Ranger

## Overview

Freelancers and side-hustlers get destroyed twice: once by the April bill
they didn't save for, and again by the underpayment penalty on top. The
math that prevents both is simple but never done: set aside the right
fraction of every payment, and send four correct estimates on time —
adjusted for the fact that Q2 income isn't Q1 income. `scripts/quarterly_tax.py`
computes safe-harbor quarterly payments (100%/110% of last year's tax), the
annualized-income method for lumpy earners, SE tax with the Social Security
wage-base interaction, QBI deduction pass-through, and prints a per-payment
"as you earn" set-aside ledger.

## When to Use

- First year freelancing / first 1099 / first profitable side business.
- Income is uneven (big Q4 contract, seasonal gig) — safe harbor overpays.
- Deciding how much of each client payment to move to a tax sub-account.
- Catching up after missed quarterlies without panicking.

**Don't use for:** corporate/LLC payroll tax (different regime), non-US
self-employment (rates differ; safe-harbor dates are IRS), or state
estimates in every state — federal math with a state add-on line.

## How It Works

1. **The three safe harbors**: owe < $1,000 at filing, OR pay 90% of current
   year tax, OR pay 100% of last year's tax (110% if last-year AGI > $150k).
   Any one avoids the underpayment penalty — the script picks the cheapest
   certain one.
2. **Quarterly split**: default 25/25/25/25 of the safe-harbor target; due
   dates Apr 15 / Jun 16 (Jun 15 on weekends) / Sep 15 / Jan 15 next year.
3. **Annualized income (Form 2210 Schedule AI)**: for lumpy income, compute
   tax on cumulative YTD annualized income each period and pay only what
   that period actually earned — Q1-heavy vs Q4-heavy incomes get very
   different correct payments.
4. **SE tax**: 92.35% × 15.3% up to the SS wage base, 2.9% (plus 0.9%
   Additional Medicare over $200k) above; half of SE tax deducts from
   income.
5. **QBI**: 20% of qualified business income (pre-199A phaseouts) reduces
   taxable income before the marginal-rate estimate.
6. **Ledger**: per $1,000 of gross, the set-aside split (federal income +
   SE + state) and the running balance vs the next due date.

## Using the Script

```bash
# Demo: three realistic freelancer profiles
python3 scripts/quarterly_tax.py --demo

# You: last year's total tax, this year's expected net profit
python3 scripts/quarterly_tax.py --prior-tax 8200 --profit 65000 \
    --filing single --state-rate 5.0

# Lumpy income: quarterly net profits (Q1..Q4)
python3 scripts/quarterly_tax.py --prior-tax 8200 --filing single \
    --q 9000 0 0 22000 --annualized --state-rate 5.0
```

## Worked Example

Single freelancer, $65k expected net, $8,200 last-year tax, 5% state:
safe-harbor target = $8,200 (100% rule, under $150k AGI) → $2,050 per
quarter; the "as-earned" 90% estimate for THIS year (SE tax + income after
QBI + half-SE deduction) ≈ $14.5k federal → the ledger says set aside 24.9¢
per $1 gross (incl. state) and the two numbers are compared so you can pick
safe-harbor certainty vs. paying-as-earned. With `--annualized` and
`--q 9000 0 0 22000`, Q1's payment drops to the tax on annualized Q1 income
only (~$2.4k) instead of a flat quarter of an estimate that assumed
February-level income all year.

## Common Pitfalls

1. **Forgetting SE tax entirely.** Income tax withholding habits (22%
   bracket) meet 15.3% SE tax on top — first-year freelancers under-save by
   a third.
2. **Treating the four dates as even quarters.** Q2 is 2 months (Apr–May),
   Q3 and Q4 are 3. The DATES are fixed; income usually isn't.
3. **Missing the 110% cliff.** Last-year AGI over $150k means 100% safe
   harbor is NOT available — 110% is. The script checks this.
4. **Safe harbor on a falling-income year.** Paying 100% of a big last-year
   bill protects you but loans the IRS money interest-free; annualized
   method pays the true amount — if income is collapsing, that's the move.
5. **QBI amnesia.** Forgetting the 20% pass-through deduction overwithholds;
   it's why "30% for taxes" folklore overshoots for many sole proprietors.
6. **State quarterlies.** Most states mirror the federal dates but have
   their own thresholds; the `--state-rate` line is an estimate, not a
   filing.

## Verification Checklist

- [ ] Safe-harbor selection states WHICH harbor and why (100/110/90%).
- [ ] Quarterly due dates printed with each payment (no weekends assumed
      blindly).
- [ ] SE tax shows the wage-base split when profit crosses it.
- [ ] QBI and half-SE deduction applied in the 90%-estimate path.
- [ ] Annualized mode labels itself "Schedule AI method" and shows the
      per-period cumulative income.
- [ ] Output ends with the "estimates, not tax advice" boundary line.
