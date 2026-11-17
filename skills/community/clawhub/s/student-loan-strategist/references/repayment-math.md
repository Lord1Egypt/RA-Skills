# Student Loan Repayment — Reference

## Federal plan shapes (as modeled)

| Plan | Term | Payment | Notes |
|---|---|---|---|
| Standard | 10 yr | level amortization | qualifying for PSLF; fastest federal payoff |
| Graduated | 10 yr | starts ~50–65% of standard, steps up every 2 yr | NOT PSLF-qualifying; late steps sting |
| Extended | 25 yr | level, fixed or graduated | requires >$30k debt; NOT PSLF-qualifying |
| IBR (old) | 20/25 yr | 10% (UG borrowees pre-2014) / 15% of discretionary, capped at standard-10 | hardship eligibility (partial financial hardship for 10% tier) |
| PAYE-style | 20 yr | 10% of discretionary, hard cap at standard-10 | new borrower cutoffs; used as the 10% model |
| ICR | 25 yr | 20% discretionary OR fixed 12-yr × income factor, whichever lower | Parent PLUS consolidation route |
| SAVE/REPAYE | — | litigation-frozen 2024–2026 | model with 10/15% legacy shapes; always caveat |

Forgiveness horizons: 240 payments if ALL loans are undergrad-originated; 300 if any
graduate loan. (Statutory; confirm current rules — this field moves.)

## Discretionary income

```
FPL 2025 (contiguous US): 1: $15,060; +$5,380 per additional person
discretionary = AGI - 1.5 × FPL(family size)
payment = pct × discretionary, capped at standard-10 payment (PAYE), floor $0
```

Married filing separately excludes spouse income for IBR/PAYE (not REPAYE) — a real lever.

## Tax bomb

- IDR forgiveness (20/25 yr) is **taxable** as ordinary income (no current federal exclusion;
  the 2021–2025 insolvency-window relief lapses — verify at use time).
- PSLF forgiveness is **federal-tax-free**; a few states (e.g., MS historically) may tax.
- Sinking fund: bomb / months-to-forgiveness. At $13.5k bomb and 15 years: ~$75/mo in a
  money-market earning ~4% ≈ covers it with slack.

## PSLF mechanics

- 120 qualifying payments (not necessarily consecutive), full-time gov/501(c)(3) employment,
  Direct loans, qualifying plan (IDR or 10-yr standard; the $0 payments on IDR count if
  employed). Forbearance/deferment generally doesn't count (some waiver programs did).
- Payments made while employed count even if later employment changes.
- Track annually in theEmployer Certification Form; keep pay stubs/W-2s forever.
- TEPSLF backstop existed for wrong-plan payers — historical, verify before relying.

## Refinance decision gate

Refinance federal→private only when ALL true:
1. Rate cut ≥ 1.5 pts on the weighted APR
2. Stable income + 6-month emergency fund
3. No PSLF intent, no IDR safety-net need
4. No state loan-forgiveness program dependence (teacher/nurse/medical)

Otherwise keep federal; direct extra payments at the highest-APR loan (avalanche).

## Modeling notes / simplifications (be honest in reports)

- Income growth default 3%/yr; user can override.
- Unpaid interest accrues and capitalizes continuously in the model (real PAYE caps
  capitalization at 10% of original principal → model slightly overstates IDR cost).
- Fees (late, collection) ignored; assume on-time payments.
- Poverty lines are 2025 contiguous-US; Alaska/HI higher (~1.25×/1.15×).
- Marginal rate used for the bomb is the user-supplied rate at forgiveness (default current).

## Amortization identity used everywhere

```
interest_i = balance × rate/12
principal_i = payment - interest_i
balance    -= principal_i      (payment < interest → balance grows: negative amortization)
```

Graduated schedule solved by bisection: scale factor k so that payments of
`k × base × (1+g)^(2·floor(i/24))` retire the loan in exactly 120 months (g default 8%/2yr,
clamped so first payment ≥ 50% of standard).
