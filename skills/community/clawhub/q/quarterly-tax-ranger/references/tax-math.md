# Quarterly Tax Ranger — Reference

## 1. The payment dates (federal)

| Quarter | Period | Due (2026 tax year) |
|---|---|---|
| Q1 | Jan 1 – Mar 31 | Apr 15, 2026 |
| Q2 | Apr 1 – May 31 | Jun 15, 2026 (observed) |
| Q3 | Jun 1 – Aug 31 | Sep 15, 2026 |
| Q4 | Sep 1 – Dec 31 | Jan 15, 2027 |

Note the asymmetric periods: Q2 is two months. If a date falls on a weekend
or DC holiday, it slides to the next business day.

## 2. Safe harbors (IRC §6654)

No underpayment penalty if ANY of:
1. Balance due at filing < $1,000 (after withholding and timely estimates).
2. Timely estimates ≥ 90% of current-year tax.
3. Timely estimates ≥ 100% of prior-year tax (12 months of tax if prior
   return covered a full year), or **110%** if prior-year AGI > $150,000
   ($75k MFS).

Which to pick:
- Income rising → 100/110% of last year (certain, cheaper than 90% of a
  bigger bill... no wait — it IS the cheaper certain option; the remainder
  is due April 15 without penalty).
- Income falling → 90% or annualized method (don't loan the IRS your
  sinking year's money).

Penalty rate floats with federal short-term rates (it's interest, not a
fixed fine) — typically mid-single digits annualized, computed per period.

## 3. The tax stack for the self-employed (simplified 2026 shapes)

```
net profit (Sched C) = gross − business expenses
SE tax = net × 0.9235 × 15.3%        (SS portion capped at wage base,
                                       est. $176k-ish 2026; +2.9% Medicare
                                       above; +0.9% Add'l Medicare > $200k)
half-SE deduction = SE tax / 2       (above the line)
QBI = 20% × (net − half-SE − SE health-insurance − retirement contribs)
taxable income = gross − std deduction − half-SE − QBI − (other)
federal income tax = brackets(marginal rates: 10/12/22/24/32/35/37)
```

Standard deduction ≈ $15,000 single / $30,000 MFJ (2026 est). QBI
phase-outs begin around $197k single / $394k MFJ (SSTB limits apply above).

## 4. Annualized-income method (Form 2210 Schedule AI)

Instead of 25/25/25/25, each payment reflects tax on cumulative income
annualized to date:

| Period | Annualize over | Cumulative window |
|---|---|---|
| Q1 | 12/3 = 4.0× | Jan–Mar |
| Q2 | 12/2 = 6.0× | Jan–May |
| Q3 | 12/3 = 4.0× | Jan–Aug |
| Q4 | 12/1 = 1.0× | Jan–Dec |

payment(period) = tax(annualized cumulative) × (period days / 365)
                  − payments already made

This is the honest method for lumpy income: a Q4-heavy consultant pays most
in January, not April of the prior year. Paperwork: file Form 2210 with
Schedule AI attached (the IRS can't compute it for you).

## 5. Set-aside doctrine ("as you earn")

For each $1,000 of gross client payment:
- reserve = effective_federal_rate + SE_rate + state_rate
- effective_federal_rate ≈ (income tax after QBI + SE − half-SE deduction)
  / gross — typically 18–30% for mid earners
- SE_rate ≈ 14.1% of net (15.3% × 0.9235) below the wage base
- keep it in a separate high-yield sub-account; pay the IRS on the four
  dates; the float is yours

Folklore "save 30%" overshoots for low-six-figure sole proprietors with
QBI, undershoots for W-2 + heavy side income (stacking brackets).

## 6. Catch-up play (missed a quarter or three)

- Safe harbor compares TOTAL timely payments; late payments accrue the
  penalty per-period, but catching up stops the bleeding from that date.
- You may annualize even if you started late (Schedule AI reduces the
  per-period required amounts that were missed).
- If a big Q4 payment makes Q4 withholding, remember: withholding is treated
  as paid evenly across the year (estimates are paid when paid) — relevant
  only if you also have W-2 income to arbitrage.

## 7. State layer

Most states with income tax mirror federal quarterly dates; thresholds and
safe harbors differ (e.g., California requires 30/40/0/30 for some filers;
New York ~ 100% safe harbor with own AGI cliffs). The `--state-rate` flag
estimates the state slice as a flat % of net — a budgeting approximation,
not a state filing.

## 8. Boundary

Estimates use simplified 2026-shaped constants (brackets, standard
deduction, wage base are IRS-inflation-adjusted each October). This tool
builds payment discipline and correct safe-harbor logic; a CPA signs the
return. Not tax advice.
