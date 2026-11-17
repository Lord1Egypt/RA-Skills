---
name: social-security-claiming-timer
description: Use when deciding WHEN to claim Social Security (62 vs Full Retirement Age vs 70), modeling break-even ages, early-claim reductions, delayed retirement credits, the earnings test before FRA, or longevity-quartile strategy — computes month-accurate benefit factors by birth year, cumulative-benefit crossover ages for any pair of claiming ages, and names which strategy wins at the 25th/50th/75th percentile lifespan, instead of the folklore "take it early to be safe" or "always delay" one-size answers.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [social-security, retirement, break-even, claiming-age, personal-finance]
---

# Social Security Claiming Timer

## Overview
The single biggest irreversible retirement decision most Americans make — claiming age — is made with folklore. "Take it at 62 because you might die" and "wait to 70 because you get 24% more" are both half-truths: the honest answer is a **break-even age**, and it is *computable from three inputs*: birth year, Primary Insurance Amount (PIA, the benefit at Full Retirement Age from your ssa.gov statement), and your longevity outlook.

This tool does the month-accurate arithmetic the SSA uses — early reductions of 5/9 of 1% per month for the first 36 months and 5/12 of 1% beyond, delayed retirement credits of 2/3 of 1% per month after FRA, the FRA table by birth year (66 → 67 drift) — then runs the **cumulative-benefit crossover** for any pair of claiming ages and reads the verdict against approximate longevity quartiles. It also prices the **earnings test** trap (working at 63 while claiming can withhold checks — though withheld money is recalc'd, not lost) and carries the survivor-benefit rule of thumb: the higher earner's delay protects the surviving spouse.

## When to Use
- Deciding between claiming at 62, FRA, 70, or anywhere between (yes, claiming at 64 is legal and common)
- "Will waiting to 70 pay off?" — get the exact break-even age, not vibes
- Still working past 62 and claiming — earnings-test withholding math
- Couple coordinating: who claims when (higher earner delays → survivor benefit logic)
- Checking a financial advisor's claiming chart for arithmetic errors (they circulate)

**Don't use for:** disability (SSDI — different rules), computing PIA from earnings history (take it from the ssa.gov statement), or non-US pensions. Not tax advice: up to 85% of benefits can be taxable — see references.

## Quick Start
```bash
# Full claiming table 62→70 for someone born 1962 with $2,400/mo PIA
python3 scripts/ss_claim_optimizer.py plan --birth-year 1962 --pia 2400

# The classic question: 62 vs 70 — where's the crossover?
python3 scripts/ss_claim_optimizer.py plan --birth-year 1962 --pia 2400 \
    --compare 62 70 --longevity female

# Working at 63 with a $55,000 salary while claiming
python3 scripts/ss_claim_optimizer.py earnings-check --birth-year 1962 --pia 2400 \
    --claim-age 63 --salary 55000

python3 scripts/ss_claim_optimizer.py --demo   # worked example, no arguments needed
```

## The Engine (what the math actually is)
1. **FRA lookup** by birth year: 1943–1954 → 66y 0m; 1955–1959 → 66y +2m/yr; 1960+ → 67y 0m.
2. **Benefit factor** for claiming age A given FRA:
   - Early (A < FRA): first 36 early months × 5/9 of 1% each; further months × 5/12 of 1%. Born 1960+ claiming at 62 = 60 early months = exactly **70%** of PIA.
   - Delayed (A > FRA): 2/3 of 1% per month = **8%/yr**, capped at 70. FRA 67 → **124%** at 70; FRA 66 → 132%.
3. **Cumulative crossover**: sum monthly checks from each claiming date forward; find the age where strategy B overtakes strategy A. Nominal and discount-adjusted (`--discount`, default 0 — benefits are COLA-indexed, so real terms is the honest default).
4. **Longevity read-out**: break-even vs approximate quartiles (62-year-old female ≈ P25 81 / P50 86 / P75 91; male ≈ 78/83/88 — SSA-period-based approximations, stated as such). If break-even sits below P25, delaying is a bet against a long life; above P50, claiming early loses money in the median case.
5. **Earnings test** (2026 limits, indexed): under FRA year $1 withheld per $2 over $23,400; FRA year $1 per $3 over $62,160 (months before FRA only); no test after FRA. Withheld checks are *recalculated* into your benefit at FRA (ARF) — the script says so, because "you lose it" is the most common myth it kills.

## Verdicts
- `DELAY WINS AT P50` — break-even below median lifespan
- `EARLY WINS AT P50` — crossover beyond median life expectancy
- `TOO CLOSE TO CALL` — break-even within ~2 yr of the relevant quartile
- `EARNINGS TEST BITES` — withholding math materially changes year-1 cash

## Common Pitfalls
1. **Comparing monthly checks instead of lifetime cash.** 124% vs 70% of PIA is noise; the crossover age is the signal.
2. **Ignoring the FRA birth-year drift.** Advice written for a 1950-born (FRA 66, 25% cut at 62) is wrong for a 1962-born (30% cut). The script pins FRA from birth year.
3. **Treating earnings-test withholding as theft.** It is a delayed, interest-free hold; your benefit is re-adjusted upward at FRA.
4. **Couple-level blindness.** For a married couple, the higher earner's age-70 claim often survives as the survivor benefit — worth up to decades of the larger check for the widow(er). Single-decision framing misses this (see references).
5. **Forgetting break-even is a distribution question, not an expected-value question.** Read the verdict at *your* health/longevity quartile, not the population median.

## Verification Checklist
- [ ] FRA printed matches SSA's table for the birth year
- [ ] Factor at 62 and 70 spot-checked (1960+ born: 0.700 / 1.240)
- [ ] Crossover age from `compare` matches the cumulative table's crossing row
- [ ] Discount left at 0 unless the user insists on a personal time preference

## Example
Born 1962, PIA $2,400. Claim 62 → $1,680/mo from age 62.0; claim 70 → $2,976/mo from 70.0. Cumulative crossover lands ≈ **age 80–81** (standard result). At male P50 (≈83) delaying wins by ~$40k nominal; at male P25 (≈78) early wins. The tool prints exactly this, with the honest "if your health outlook is below-median, the early claim is rational" line most calculators refuse to give.
