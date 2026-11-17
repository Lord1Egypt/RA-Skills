---
name: student-loan-strategist
description: "Use when comparing student loan repayment paths (standard vs extended vs graduated vs income-driven), planning PSLF qualification, sizing extra payments, or projecting forgiveness tax bombs. Runs real amortization and discretionary-income math and ranks strategies by total cost and payoff date."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [student-loans, debt, repayment, IDR, PSLF, amortization, finance]
---

# Student Loan Strategist

## Overview

Student debt decisions are made once (at exit counseling or on a servicer website) and then
never revisited — yet the difference between repayment plans is routinely **$20,000–$80,000**
in extra interest or a five-figure forgiveness tax bill nobody saw coming. Servicers present
plans as a menu without showing 20-year totals; borrowers pick the lowest payment and lose.

This skill is a decision instrument: given balances, rates, income, and family size, it runs
**real amortization and cash-flow simulations** for every major federal plan shape and ranks
them honestly — including the income-driven (IDR) "forgiveness" trap, where the discharged
balance at year 20/25 is taxable income (the "tax bomb").

## When to Use

- Borrower with one or more student loans asks "which plan should I pick?"
- Comparing **extra payments / avalanche** vs staying on an income-driven plan
- Tracking **PSLF** progress (120 qualifying payments) and projecting the forgiveness date
- Estimating the **IDR forgiveness tax bomb** at year 20/25
- Deciding whether refinancing federal → private makes sense (federal protections lost)
- Recertification panic: "what happens if my income drops / I lose my job?"

**Don't use for:** private loan payoff alone (no IDR/forgiveness logic needed — plain
avalanche math still works), or tax filing advice. Always state figures are *estimates*:
servicer rounding, income growth, and rule changes (REPAYE/SAVE litigation) shift results.

## The Math Core

### Discretionary income (federal definition)

```
poverty_line_2025 = {1:15060, 2:20440, 3:25820, 4:31200, each_extra:5380}
discretionary     = max(0, AGI - 1.5 * poverty_line(family_size))
IDR payment      = 10% (old IBR/PAYE undergrad) or 15% (old IBR grad / ICR) of discretionary
```

Rules encoded:
- Payment recalculates **annually** after recertification (default income growth 3%/yr).
- PAYE-style **cap**: IDR payment never exceeds the 10-year standard amount.
- If payment < monthly interest, balance grows (negative amortization). The model tracks
  unpaid interest realistically (it accrues; under PAYE it capitalizes only above 10% of
  original principal — simplified here as immediate accrual, flagged as conservative).
- Forgiveness horizon: **240 payments (20 yr)** if all loans are undergrad, **300 (25 yr)**
  if any graduate loan. Forgiven amount is taxed as ordinary income in the forgiveness year
  (currently no exclusion through 2025 law sunset — always model the bomb).

### PSLF

- 120 qualifying payments while **employed full-time by government/501(c)(3)** on a
  qualifying plan (any IDR or 10-year standard). Payments need not be consecutive.
- PSLF forgiveness is **tax-free** (federal; some states differ — flag for NY/MS states).
- Refinancing to private **destroys** PSLF eligibility permanently.

## Numbered Workflow

1. **Collect inputs:** per-loan (balance, APR, undergrad vs grad), AGI, family size,
   marginal tax rate, employment (PSLF-eligible?), payments already made, extra $/mo available.
2. Run `scripts/loan_compare.py` — it simulates every strategy:
   - Standard 10-yr, Extended 25-yr, Graduated 10-yr (bisect-solved step schedule)
   - IDR 10% and 15% (annual recertification, PAYE cap, forgiveness + tax bomb)
   - Avalanche with optional extra payment
3. Read the ranked table: **total paid**, **payoff/forgiveness date**, **interest**, and the
   forgiveness line (gross discharged / net after tax bomb).
4. Cross-check plan-choice pitfalls below, then give ONE recommendation with the reasoning
   ("lowest total cost" is not always right — PSLF seekers should *minimize payments*).
5. For PSLF users run with `--pslf --payments-made N` to get the projected tax-free
   forgiveness date and the "do not pay extra" verdict.

## Plan-Choice Pitfalls

1. **Picking the lowest payment without the 20/25-yr total.** Extended 25-yr often costs
   2–3× the interest of standard 10-yr. The tool shows both.
2. **Forgetting the tax bomb.** IDR forgiveness at 20/25 yr is taxable income: a $90,000
   discharge at 22% marginal = ~$19,800 due in one year. Model a sinking fund (bomb/240).
3. **Losing PSLF by refinancing** or by switching to extended/graduated (non-qualifying).
4. **Recertification lapse** → payment snaps to standard 10-yr amount + unpaid interest
   capitalizes. Set the annual reminder; the script prints the next deadline.
5. **Extra payments on IDR without targeting.** Extra on avalanche = good if staying to
   payoff; **wrong** if PSLF-bound (every extra dollar is a dollar not forgiven).
6. **Graduated plan trap:** late-step payments can exceed the borrower's income growth;
   the script's solved schedule exposes the final-step payment.
7. **Private refinance only beats federal** when the rate cut is large (≥1.5–2 pts) and the
   borrower accepts losing IDR/PSLF/forbearance safety nets.

## Example Session

```
$ python3 scripts/loan_compare.py --balance 38000 --rate 6.2 --grad \
    --agi 52000 --family 2 --marginal 22 --extra 150

Strategy              Payment(1st/last)  Payoff/Forgiven  Total paid   Interest
Standard 10-yr        $425/$425          2036-04          $51,047      $13,047
Extended 25-yr        $248/$248          2051-04          $74,502      $36,502
Graduated 10-yr       $290/$618          2036-04          $53,880      $15,880
IDR 15% (25-yr)       $294/$386          FORGIVEN 2051-04 $88,315      — $61,623 discharged,
                                                             tax bomb ≈ $13,557 (22%)
Avalanche +$150/mo    $575/$575          2033-05          $45,690      $7,690

VERDICT: Avalanche+$150 pays least overall (2033). If PSLF-eligible, stay on IDR 15%,
  pay minimum, forgiveness ~2051-04 is TAX-FREE under PSLF — total paid ≈ $88k regardless.
```

## Verification Checklist

- [ ] Balance(s), rate(s), AGI, family size confirmed with the user
- [ ] Poverty-line multiple (1.5×) and forgiveness horizon (20 vs 25 yr) correct for their loans
- [ ] Tax bomb shown in gross AND net terms
- [ ] PSLF users warned against extra payments and refinancing
- [ ] Recertification date on the calendar
- [ ] Figures labeled as estimates; rule changes flagged (SAVE/REPAYE litigation)
