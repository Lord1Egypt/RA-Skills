# Social Security Claiming Timer

**When to claim Social Security: month-accurate break-even math between 62, FRA, and 70 — with longevity-quartile verdicts instead of folklore.**

## The problem
Claiming age is a one-way door: Americans lock in a permanent −30% to +24% benefit modification for life, and the decision is mostly made on two pieces of folklore — "take it early because you might die" or "delay always wins." Both are wrong for large groups of people. The honest answer is a break-even age computed from your birth year (FRA drifts 66→67), your PIA, and your health outlook. Most online calculators hide the math, assume away longevity differences, or are lead-gen for annuity sales. Meanwhile the stakes are enormous: the difference between claiming at 62 vs 70 for a median-life retiree is commonly $50,000–$150,000 in lifetime benefits, and for couples, the higher earner's choice sets the survivor's check for potentially decades.

## What this skill does
- **Full claiming table 62→70** with exact SSA factors (5/9 and 5/12 of 1% early reductions, 8%/yr delayed credits) pinned to your birth year's FRA
- **Break-even age for any pair of claiming ages** via month-by-month cumulative-benefit crossover, optionally discount-adjusted
- **Longevity-quartile verdicts** — names which strategy wins at P25/P50/P75 lifespan so the decision matches health reality, not population averages
- **Earnings-test pricing** for work-while-claiming (including the "it's withheld, not lost" ARF truth)
- Couple coordination doctrine (higher earner delays → survivor benefit) in the reference guide

## Quick example
```bash
python3 scripts/ss_claim_optimizer.py plan --birth-year 1962 --pia 2400 --compare 62 70
# → 62 = $1,680/mo, 70 = $2,976/mo, break-even ≈ age 80-81
# → DELAY WINS at male P50 (83) / TOO CLOSE at P25 (78)
python3 scripts/ss_claim_optimizer.py --demo
```

## Who needs this
- The ~4 million Americans who turn 62 each year and must pick a claiming month
- Retirees within 8 years of 62 deciding whether work + delayed claiming beats early checks
- Financial advisors and CPAs sanity-checking client claiming charts
- Couples doing survivor-benefit-aware coordination (the single biggest couple-level lever)

## Install
Python 3.9+, stdlib only — no dependencies, no network calls, no data collection.

```bash
git clone https://github.com/voronindenis5/social-security-claiming-timer
cd social-security-claiming-timer
python3 scripts/ss_claim_optimizer.py --demo
```

## Disclaimer
Educational arithmetic based on published SSA rules and approximate life tables. Not affiliated with SSA; not financial advice. Verify PIA at ssa.gov and current-year earnings-test limits before acting.

## License
MIT © Denis Voronin
