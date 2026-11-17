# Buy-Side Underwriting Reference

## 1. The stack, derived
```
Gross Scheduled Rent (GSR)   = rent × 12 (× units)
Vac loss                     = GSR × vacancy%
Effective Gross Income (EGI) = GSR − vac loss
OpEx                          = tax + ins + HOA + mgmt%(EGI) + maint%(EGI) [+ utilities if landlord-paid]
NOI                           = EGI − OpEx
All-in cost                   = price + rehab + closing%(price)
Cap rate                      = NOI / all-in
Debt service (DS)             = amortized payment × 12 (30-yr fixed standard)
DSCR                          = NOI / DS
Cash flow                     = NOI − DS
Cash invested                 = down payment + rehab + closing costs
Cash-on-cash (CoC)            = cash flow / cash invested
OER                           = OpEx / GSR
Break-even rent               = (OpEx + DS) / 12
```

## 2. Why each band exists
- **Cap ≥ rate + 1.5pt**: with cap < loan rate, every borrowed dollar drags return (negative leverage) — you take risk to underperform the mortgage. Post-2022 rates made this the #1 deal-killer; it's why "cash flow" deals vanished.
- **DSCR ≥ 1.25**: agency small-balance multifamily and most portfolio lenders anchor here. Below 1.10, one vacancy month eats the year.
- **OER 35–45%**: the classic "50% rule" (opex = half of GSR, no mortgage) is a stress ceiling for older stock; well-run SFR in low-tax states runs 35–45%. > 50% usually means taxes, HOA, or insurance is structurally heavy — not fixable by management.
- **1%-rule**: rent ≥ 1%/mo of all-in was a 2010s foreclosure-market artifact. In 2024–26 rate environment, 0.6–0.8% is the honest screen; 1%+ survives mostly in Midwest/South markets with older stock. Treat as scent, not test.

## 3. Depreciation shield (27.5-yr straight-line, residential)
Annual paper depreciation = building basis ÷ 27.5. Building basis ≈ 80% of purchase price (land allocation; use the county assessor's land/building split when handy). Sheltered income ≈ depreciation − actual costs already deducted; roughly: if depreciation ≥ pre-tax cash flow, the cash flow is tax-free (paper loss offsets it), subject to passive-activity rules.
- After-tax CoC = (cash flow + (depreciation × marginal rate)) / cash invested (approximation; assumes depreciation exceeds cash flow and you have passive income to absorb losses)
- Cost-segregation (accelerated 5/15-yr components) amplifies early years — for the big deals, not the screening pass.
- Depreciation recapture (25%, §1250) on sale — modeled in the reference sale note, not the screener.

## 4. What the 10-yr projection assumes
- Rent growth (default 3%/yr) and expense growth (default 3%) — running in parallel so NOI grows with inflation only if you raise rents.
- Appreciation (default 3%) affects SALE proceeds only; the "cash-flow-only" line ignores it deliberately.
- Sale at year 10: net = value − 6% selling costs − loan payoff; IRR computed on yearly cash flows + sale.
- Sensitivity grid varies: rent ±10%, vacancy 8%, rate +1pt, price −5%; verdict flips are named.

## 5. Inputs people get wrong (ask these before trusting any output)
1. **Taxes reassess on sale** in most states — the seller's $2,100 bill on a 2015 basis becomes $4,000+ on your purchase price. Always compute: price × county millage.
2. **Landlord insurance** costs 15–25% more than homeowner's and excludes contents.
3. **HOA transfer/capital contributions** at purchase ($250–$1,000 one-time) and rental restrictions (rental caps! check before offer).
4. **Section 8 / rent-control / eviction-timeline jurisdictions** change vacancy risk structurally.
5. **Sewer/water paid by owner** on multifamily — a per-unit monthly cost that eats 3–5% of GSR.

## 6. When the screen says THIN
The honest fixes, ranked by control:
1. Price (negotiate −5–8%: the stress grid prices the exact gap)
2. Rent (verify comps — a stale listing number is the most common input error)
3. Terms (rate buydown, ARM 5/1 at −0.5–1pt for a 5-yr hold)
4. Self-management (+8% CoC, costs your Saturdays)
5. Longer hold (appreciation-dependent — weakest fix, printed as such)

## 7. Sources
- Appraisal Institute income-approach conventions (NOI construction)
- Fannie Mae Delegated Small Loan / DSCR guidance (1.20–1.25 thresholds)
- IRS Pub 527 (residential rental: 27.5-yr MACRS, passive rules, §1250 recapture)
- BiggerPockets community norms for expense %s (calibrated to 35–50% OER reality)
