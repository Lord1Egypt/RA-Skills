# Refi Break-Even Ranger

**Rates dropped and your inbox says "save $220/month!" — should you refinance?**

The honest answer needs four numbers lenders don't put next to each other: closing costs +
points, your monthly savings, your **actual stay-horizon**, and the amortization-clock reset
hiding in every new 30-year loan. Get the horizon wrong and a "great" refi quietly loses you
five figures.

## What it does

- **True break-even** — months to recover closing + points from monthly savings.
- **Net saving at YOUR horizon** — runs both loans' full amortization to a common horizon,
  compares interest paid and equity built, subtracts upfront costs. This is the number that
  decides the question.
- **Multi-lender compare** — ranks offers by net horizon saving, exposing the rate-vs-points
  tradeoff (the 4.99%-with-points offer routinely loses to 5.375%-flat).
- **Term strategy** — price the same rate at 15/20/30 years; keep the old payment as extra
  (`--extra-monthly`) to kill the clock reset.
- **Cash-out aware** — loan amount, payment, and break-even recomputed on the real balance.

## Quick start

```bash
python3 scripts/refi_ranger.py analyze \
  --balance 280000 --current-rate 6.5 --current-payment 1768 \
  --new-rate 5.25 --term 30 --closing 4200 --points 0.5 --horizon-years 7

python3 scripts/refi_ranger.py compare --balance 280000 --current-rate 6.5 \
  --current-payment 1768 --offers offers.json
```

## Real-world problem it solves

A borrower with 7 years left at a job compares three quotes. Headline math favors the 4.99%
offer; the compare table at his honest 7-year horizon flips it — the credit union's 5.375%
with $2,500 closing nets $9,039 versus $4,536 for the flashy rate, because 1.5 points +
$6,500 costs never pay back inside the window. Re-run at a 2-year horizon (possible move) and
every offer turns negative: stay put. Two minutes of math, an $11k mistake avoided.

## Scope & limits

P&I math only — taxes/insurance/escrow are payment-neutral between offers; PMI changes belong
in the decision but outside this tool's inputs. Not purchase mortgages or reverse mortgages.
Pure Python 3 stdlib, no dependencies. MIT license.
