# Timeshare Exit Strategist

**Honest keep-vs-exit math for timeshare owners — fee-escalation crossover year, contract-type routing, real exit paths ranked, and the upfront-fee scam fingerprint.**

## The problem
~10 million US households own a timeshare with maintenance fees compounding at 2-3× inflation under contracts that often outlive the owner and bind the heirs. The legitimate resale market for most weeks is zero. Into that trap an entire scam industry sells "cancellation" for $4,000-$10,000 upfront — delivering nothing while the clock runs out on chargebacks. Owners face three bad options and no honest numbers. This tool produces the honest numbers: the exact year keeping starts costing more than exiting, what each real exit path costs, and whether that exit-company offer matches the fraud pattern.

## What this skill does
- `keep` — year-by-year fee-escalation table vs realized usage value, crossover year where the $X exit beats keeping
- `contract` — deeded vs points vs right-to-use classification with heir-risk and the exit levers each type actually has
- `scamcheck` — scores exit-company offers against the red-flag pattern (big upfront fee, guarantee language, 12+ month timeline, money-back theater)
- `--demo` — the classic Orlando week, an inherited points contract, and a $6,500 exit offer scored live

## Quick example
```bash
python3 scripts/timeshare_exit.py --demo
```
The classic case: $1,200/yr fees at 6% growth with $500/yr actual usage crosses a $4,000 exit cost early in the decade — and the 20-year fee total is $44k for $10k of vacation value.

## Who needs this
- Timeshare owners watching fees rise and usage fall
- Heirs who just inherited a week (disclaimer clocks are short — check the reference)
- Anyone pitched by a "timeshare exit" or "cancellation" company
- Financial advisors and estate attorneys fielding the question

## Install
Python 3.9+, stdlib only:

```bash
python3 scripts/timeshare_exit.py --demo
```

## License
MIT © Denis Voronin
