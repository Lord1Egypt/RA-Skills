# Quarterly Tax Ranger

**Safe-harbor quarterly tax payments for the self-employed — computed, dated, and honest about lumpy income.**

## The problem

The freelance/side-hustle tax system fails people through one number they
never compute: how much of each client payment to reserve, and what four
checks to mail the IRS (Apr 15 / Jun 15 / Sep 15 / Jan 15). The result is
predictable — a five-figure April bill with no savings, plus an
underpayment penalty for the privilege. First-year 1099 earners routinely
under-save by a third because W-2 instincts ignore the 15.3%
self-employment tax stacking on top of income tax. Meanwhile "save 30%"
folklore overshoots for anyone with the 20% QBI deduction.

## What it does

`scripts/quarterly_tax.py` (stdlib-only, offline):

1. **Safe-harbor selector** — 100% of last year's tax, or **110% if last
   AGI > $150k** (the cliff everyone misses), vs the 90%-of-current-year
   estimate — tells you which is cheaper and certain.
2. **Current-year estimator** — the full simplified stack: SE tax with the
   Social Security wage-base split + Additional Medicare, half-SE deduction,
   **QBI 20% pass-through**, standard deduction, 2026-shaped brackets.
3. **Annualized-income mode (Schedule AI)** — for lumpy earners: Q1-heavy
   vs Q4-heavy incomes get different correct payments; a consultant earning
   $22k in Q4 and nothing in Q2/Q3 doesn't prepay February's annualized
   fantasy all year.
4. **Set-aside ledger** — X¢ per $1 of gross split federal/state, so a tax
   sub-account accumulates exactly what the four dates demand.
5. Catch-up guidance baked into the reference (per-period penalty accrual,
   Schedule AI as the late-starter's friend).

## Example

```bash
$ python3 scripts/quarterly_tax.py --demo
```
Demo 1 (rising income): prior-year harbor $8,200 → $2,050/quarter, vs
current-year estimate ~$22.7k federal (24.7% of net + 5% state = set aside
29.7¢/$1) — remainder due April 15 without penalty. Demo 2 (Q4-heavy,
$168k prior AGI): 110% rule applies; annualized payments run ~$1.0k /
$0 / $0 / ~$5.4k instead of flat quarters.

Your numbers:
```bash
python3 scripts/quarterly_tax.py --prior-tax 8200 --profit 65000 \
  --filing single --state-rate 5.0
python3 scripts/quarterly_tax.py --prior-tax 12400 --annualized \
  --q 9000 0 0 22000 --filing single
```

## Who needs this

~16 million US sole proprietors/gig workers plus every W-2 earner with side
income above ~$1k/year. The four dates don't move; the math is 30 lines and
one afternoon of panic — this makes it 3 seconds and no April surprise.

## Boundary

2026-shaped constants (brackets, $176.1k wage base, $15k/$30k standard
deduction are estimates the IRS finalizes each fall). A budgeting and
safe-harbor discipline tool, not tax advice — CPAs sign returns, this
script builds the discipline that makes the CPA's job easy.

## License

MIT © 2026 Denis Voronin
