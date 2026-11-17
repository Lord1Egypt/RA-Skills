# Claiming Strategy — Reference Guide

## 1. The benefit factor table (why birth year matters)

SSA computes the claiming factor from months relative to FRA:

| Situation | Rate | Annualized |
|---|---|---|
| First 36 months before FRA | 5/9 of 1% / month | −6.67%/yr |
| Months 37–60 before FRA | 5/12 of 1% / month | −5.00%/yr |
| After FRA (up to 70) | +2/3 of 1% / month (for FRA 66; slightly different rate applies to FRA 66+ via 8%/yr statutory cap wording, but 8%/yr is the operative figure) | +8%/yr |

FRA by birth year:
- 1943–1954: 66y 0m
- 1955: 66y 2m; 1956: 66y 4m; 1957: 66y 6m; 1958: 66y 8m; 1959: 66y 10m
- 1960+: 67y 0m

Landmark factors:
- Born 1960+, claim at 62 (60 early months): 1 − 36×(5/900) − 24×(5/1200) = 1 − 0.20 − 0.10 = **0.700**
- FRA 66, claim 62 (48 early months): 1 − 0.20 − 12×(5/1200) = **0.750**
- FRA 67, claim 70 (36 delayed months): 1 + 0.08×3 = **1.240**
- FRA 66, claim 70 (48 delayed months): **1.320** (credit stops at 70 regardless)

## 2. Break-even mechanics

Nominal cumulative for claiming age A from age A to age X:
`Cum(A, X) = benefit(A) × 12 × (X − A)` (month-accurate in the script).

The classic crossovers (COLA affects both arms equally, so real-terms crossover ≈ nominal crossover; a personal discount rate moves it toward the early claim):
- 62 vs 67 (FRA-67 cohort): crossover ≈ 77–78
- 62 vs 70: crossover ≈ 80–81
- 67 vs 70: crossover ≈ 82–83 (delaying from FRA must recoup only 3 years of forgone checks)

## 3. Longevity context (approximate quartiles at 62)

Derived from SSA period life tables with a cohort tilt; **approximations, clearly labeled as such**:

| Quartile | Male | Female |
|---|---|---|
| P25 | ~78 | ~81 |
| P50 (median) | ~83 | ~86 |
| P75 | ~88 | ~91 |

How to read: health status moves you across quartiles faster than money math does. A P25-health 62-year-old should not be shamed out of claiming at 62; a P75-health one is usually leaving five figures on the table by claiming early.

## 4. Earnings test (2026 limits; indexed yearly — verify current-year figures at ssa.gov)

- Under FRA (all year): $1 withheld per $2 earned above **$23,400**
- Year you reach FRA (months before FRA only): $1 per $3 above **$62,160**
- After FRA: no test, and SSA recomputes upward at FRA (Adjustment of Reduction Factor) for months withheld — so it is a delay, not a penalty. A special first-year grace rule counts only months after retirement if earnings were front-loaded.

## 5. Couples — the survivor rule that dominates single-life math

- Married-earner dies → survivor receives **the larger of the two checks**, not both.
- Therefore: **higher earner delays (to 70), lower earner can claim early** is often the dominant pair strategy — it converts the higher earner's delay into a joint-life insurance feature.
- Divorced (married 10+ years, currently unmarried): you can claim on the ex's record without their cooperation; survivor benefits can also apply.
- Widowed: possible to take survivor first and switch to your own retired-worker max at 70 (file-and-suicide-proof ordering; see references §7 checklist).

## 6. Taxation note (affects net, not the factor math)

"Combined income" = AGI + nontaxable interest + ½ of benefits. Above $25k single / $32k joint, up to 85% of the benefit becomes taxable. Working while claiming can push more of the benefit into tax — one more real cost of the "claim and keep working" hybrid.

## 7. What this tool deliberately does NOT do

- PIA computation from earnings history (take PIA from the statement at ssa.gov — it is authoritative)
- WEP/GPO (government pension offset) cases — rules are record-specific
- Breakeven under mortgage/other cash-flow constraints — if the client *needs* the money at 62, liquidity beats optimization; say so plainly

## 8. Sources

- SSA: "Benefits by Year of Birth", "Early or Late Retirement?", "How Work Affects Your Benefits" (pub 05-10063)
- SSA Actuarial Life Table (period life expectancies)
- Survivor benefits: 20 CFR 404.335 et seq.
