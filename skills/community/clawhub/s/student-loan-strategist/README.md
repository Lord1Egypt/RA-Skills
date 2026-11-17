# Student Loan Strategist

**Which repayment plan actually costs the least?** Servicers show a monthly payment; they
don't show the 25-year total, the forgiveness tax bomb, or the PSLF math. This tool runs
real amortization for standard / extended / graduated / income-driven plans and ranks them
by total outlay — including the taxable forgiveness event at year 20/25 and a PSLF track
that counts your 120 qualifying payments.

## The real-world problem

- 43 million US borrowers hold ~$1.7T in student debt; the average owes ~$38k.
- Choosing "extended, lowest payment" over standard 10-yr on a $38k @ 6.2% loan costs
  **~$23,800 extra interest** (simulated above: $74.8k vs $51.1k total).
- Income-driven forgiveness at 20/25 years is **taxable income** — a $60k discharge can
  trigger a ~$13k tax bill in one year ("tax bomb") that nobody budgets for.
- PSLF seekers who refinance or pay extra destroy their own tax-free forgiveness.

## What it does

`scripts/loan_compare.py` (Python stdlib, no deps):

- Level-payment amortization for standard/extended, bisection-solved graduated schedule
- IDR simulation: 2025 poverty lines, 1.5× deduction, 10%/15% tiers, PAYE-style cap at
  the 10-yr standard payment, 3%/yr income growth, negative amortization tracking
- Forgiveness projection with tax bomb at your marginal rate; PSLF mode (tax-free,
  120-payment tracker, "don't pay extra" verdict)
- Avalanche payoff with extra payment; ranked output table + JSON mode

## Quick start

```bash
python3 scripts/loan_compare.py --balance 38000 --rate 6.2 --grad \
    --agi 52000 --family 2 --marginal 22 --extra 150

# PSLF track (teacher/hospital/non-profit), 40 qualifying payments done:
python3 scripts/loan_compare.py --balance 60000 --rate 5.8 --agi 46000 \
    --pslf --payments-made 40
```

## Outputs you get

- Ranked strategy table: first/last payment, payoff or forgiveness date, total paid, interest
- Forgiveness line: gross discharged, tax bomb at your marginal rate
- One-line verdict with reasoning (PSLF-aware)
- JSON mode for piping into reports/calendars

## Limitations

Estimates only — servicer rounding, income growth assumptions, and federal rule changes
(SAVE/REPAYE litigation) shift results. Poverty lines are 2025 contiguous-US. Not tax advice.

## License

MIT © Denis Voronin
