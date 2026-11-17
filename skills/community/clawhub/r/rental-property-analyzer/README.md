# Rental Property Analyzer (buy-side deal screener)

**Underwrites a rental purchase in one pass: NOI, cap rate, DSCR, cash-on-cash, break-even rent, depreciation shield, 10-yr IRR, stress grid — and a DEAL / THIN / OVERPRICED verdict that names the assumption that flips it.**

## The problem
Listing pro-formas are optimistic fiction: zero vacancy, no management fee, no capex reserve, cash-on-cash without closing costs. First-time investors spend an evening in spreadsheets and still miss the DSCR a lender requires, the negative-leverage trap (cap rate below the mortgage rate — every borrowed dollar underperforms), or the tax reassessment on purchase. The result is buyers paying 2021 prices at 2026 rates, discovering negative cash flow at the first turnover. A deal screen should take 30 seconds and honest defaults, not hours and hope.

## What this skill does
- **Full ratio stack**: NOI construction line by line, cap rate, 1%-rule, OER red flags, DSCR (lender 1.25 line), monthly cash flow, cash-on-cash vs the T-bill yardstick
- **Negative-leverage detector**: cap < loan rate named explicitly, with the cash-deal comparison available via `--cash`
- **Break-even rent** with cushion verdict (TIGHT < 12%)
- **Depreciation tax shield**: 27.5-yr straight-line at your marginal rate → after-tax CoC
- **10-yr projection**: rent/expense growth, amortizing balance, sale at 6% costs, bisected IRR — and it separates cash-flow-only returns from appreciation-dependent returns
- **Stress grid**: rent −10%, vacancy 8%, rate +1pt, price −5%; verdict names which flip kills the deal

## Quick example
```bash
python3 scripts/deal_screener.py --demo
# $320k SFR @ $2,200 rent → cap 4.7% vs 6.5% loan = NEGATIVE LEVERAGE, CoC ~1%,
#   price cut of ~$26k or rent +$150/mo needed to reach THIN
# $185k duplex @ $2,400 → cap 8%+, DSCR 1.3+, CoC 8%+ → DEAL
```

## Who needs this
- First-time buy-and-hold investors screening listings (the exact group pro-formas are optimized against)
- Agents and wholesalers whose buyers demand honest math
- Owners deciding rent-vs-sell on an inherited property (run both screens)
- Anyone comparing cash vs financed purchase at 6–7% rates

## Install
Python 3.9+, stdlib only, offline.

```bash
git clone https://github.com/voronindenis5/rental-property-analyzer
cd rental-property-analyzer
python3 scripts/deal_screener.py --demo
```

## Disclaimer
Educational underwriting with published-standard formulas and honest default assumptions. Not investment, tax, or lending advice; verify comps, reassessed taxes, HOA rules, and lender DSCR minimums independently.

## License
MIT © Denis Voronin
