---
name: Personal Finance & Wealth Intelligence
slug: wealth-intelligence
description: >
  AI-powered personal finance and wealth management intelligence engine. Covers investment portfolio design
  (5 asset classes: cash, bonds, stocks, real estate, alternatives), retirement planning (401k/IRA/HSA/529),
  tax optimization strategies, debt management (avalanche vs. snowball), real estate analysis (buy vs. rent, mortgage
  optimization), and wealth milestones by life stage (20s to 60s+). Integrates 12 data sources (Yahoo Finance,
  Morningstar, Bankrate, Vanguard/Fidelity/Schwab, Zillow, IRS, SSA, BLS CPI). Delivers portfolio allocation models,
  retirement readiness scores, tax-loss harvesting strategies, and FIRE (Financial Independence Retire Early) planning.
triggers:
  - "investment portfolio"
  - "retirement planning"
  - "tax optimization"
  - "debt payoff strategy"
  - "buy vs rent analysis"
  - "FIRE planning"
  - "financial independence"
  - "savings rate calculator"
  - "529 plan"
  - "estate planning"
  - "mortgage calculator"
  - "asset allocation"
  - "emergency fund"
  - "investment risk tolerance"
author: Marvis
version: "1.0"
metadata:
  emoji: "💰"
  requires: "references/wealth_sources.json"
---

# Personal Finance & Wealth Intelligence

## Capabilities

| # | Capability | Input | Output |
|---|-----------|-------|--------|
| 1 | Portfolio Designer | Risk tolerance + time horizon + goals | Asset allocation (stocks/bonds/cash/alt), fund selection, fee analysis, rebalancing schedule |
| 2 | Retirement Readiness Score | Current assets + savings rate + target retirement age | Projected retirement income, gap analysis, catch-up strategies, Social Security optimization |
| 3 | Tax Optimization Engine | Income + investments + location | Tax-loss harvesting opportunities, tax-efficient fund placement, deductions/credits, Roth conversion analysis |
| 4 | Debt Payoff Strategist | Debts (type, balance, APR) | Avalanche vs. Snowball comparison, payoff timeline, interest savings, consolidation options |
| 5 | Home Buying Analyzer | Market + financials | Buy vs. rent NPV analysis, mortgage rate optimization (15yr vs. 30yr vs. ARM), closing cost estimate, affordability ceiling |
| 6 | Financial Independence (FIRE) Planner | Income + expenses + savings rate | FIRE age projection, required nest egg (4% rule variants), Coast FIRE / Barista FIRE / Lean FIRE scenarios |
| 7 | Education Savings Planner | Child age + college type | 529 vs. UTMA/UGMA vs. taxable comparison, projected costs, contribution schedule, state tax benefits |
| 8 | Insurance Needs Calculator | Life stage + dependents + assets | Term life coverage recommendation, disability income replacement, umbrella policy threshold, long-term care timing |
| 9 | Emergency Fund Optimizer | Monthly expenses + job security | Recommended fund size (3/6/9/12 months), high-yield savings vs. money market vs. I-bond ladder |
| 10 | Wealth Milestone Tracker | Age + net worth + goals | Age-banded benchmarks, net worth percentiles, catch-up plan, estate planning checklist |

## Workflow

```
User Query
  │
  ├─ [Step 1] Classify → financial domain + life stage (20s/30s/40s/50s/60s+) + risk tolerance
  │
  ├─ [Step 2] Data retrieval:
  │   └─ Market: Yahoo Finance, Morningstar, FRED (interest rates, inflation)
  │   └─ Real estate: Zillow/Redfin (home values, rent comps)
  │   └─ Tax: IRS brackets, contribution limits
  │   └─ Rates: Bankrate (mortgage, savings, CD rates)
  │
  ├─ [Step 3] Apply quantitative models:
  │   └─ Monte Carlo simulation (retirement probability)
  │   └─ NPV analysis (buy vs. rent)
  │   └─ Debt payoff optimization (avalanche/snowball math)
  │   └─ Tax-equivalent yield comparison
  │
  ├─ [Step 4] Generate personalized plan with sensitivity analysis
  │
  └─ [Step 5] Disclaimer: not financial advice; consult a licensed professional
```

## Output Formats

### Portfolio Allocation Model
| Asset Class | Conservative | Moderate | Aggressive | Your Allocation |
|-------------|-------------|----------|------------|-----------------|
| US Stocks | 30% | 45% | 60% | [fill] |
| International Stocks | 10% | 20% | 30% | [fill] |
| Bonds | 50% | 25% | 5% | [fill] |
| Cash | 5% | 5% | 0% | [fill] |
| Alternatives (REIT/Gold/Crypto) | 5% | 5% | 5% | [fill] |
| **Expected Return** | 5-6% | 7-8% | 8-10% | [calc] |

### Retirement Projection
| Age | Savings Target | Your Projected Savings | Gap | Action |
|-----|---------------|----------------------|------|--------|
| 30 | 1× salary | $X | $X | [increase savings by Y%] |
| 40 | 3× salary | $X | $X | [consider backdoor Roth] |
| 60 | 8× salary | $X | $X | [catch-up contributions] |
| Retirement | 25× annual expenses | $X | $X | [adjust retirement age] |

### Debt Payoff Comparison
| Strategy | Payoff Date | Total Interest | Monthly Payment (fixed) | Best For |
|----------|------------|----------------|------------------------|----------|
| Avalanche (highest APR first) | Date X | $X,XXX | $X,XXX | Minimum interest cost |
| Snowball (smallest balance first) | Date Y | $X,XXX | $X,XXX | Psychological momentum |
| Consolidation (personal loan @ X%) | Date Z | $X,XXX | $X,XXX | Single payment convenience |

## Usage Guidelines

1. **Always disclaim** — this skill provides educational content, not financial advice. Include "consult a fiduciary advisor" for significant decisions.
2. **Localize** — tax brackets, retirement account types, and insurance markets vary by country; adapt to user's jurisdiction.
3. **Data sensitivity** — never store or transmit personal financial data; all calculations run in-context only.
4. **Conservative projections** — use conservative return assumptions (5-7% real for equities, 2-3% for bonds), not best-case scenarios.
5. **Life-stage framing** — advice for a 25-year-old differs fundamentally from advice for a 55-year-old.
6. **Behavioral finance** — incorporate psychological elements (loss aversion, mental accounting) in explanations.

## Examples

### Example 1: Portfolio Review
**User**: "Review my portfolio: 100% S&P 500, age 35, married, 2 kids, no debt"
**Output**: Concentration risk flagged (no bonds, no international, no real estate); suggested allocation (70/20/10 stock/bond/international); emergency fund gap analysis; term life insurance recommendation; 529 plan start estimate for kids.

### Example 2: FIRE Planning
**User**: "Can I retire at 45? $500K saved, save $60K/year, spend $50K/year, age 32"
**Output**: FIRE age projection (Monte Carlo: 42-48 range at 90% confidence), required nest egg ($1.25M at 4% rule), Coast FIRE alternative (switch to lower-paying job at 38), healthcare bridge strategy (ACA subsidies), sequence-of-returns risk mitigation.

### Example 3: Buy vs. Rent
**User**: "Should I buy a $400K house in Austin vs. keep renting at $2,200/month?"
**Output**: NPV comparison over 7/15/30 years with interest rate sensitivity; mortgage breakdown (P&I, tax, insurance, HOA); opportunity cost of down payment invested in market; breakeven year analysis; rent increase assumptions vs. home appreciation.

---

**Data Base**: `references/wealth_sources.json` — 12 data sources, 5 asset classes, 5 retirement accounts (US), 5 life-stage milestones, 5 debt types.
**Last Updated**: June 2026
**Free Tier**: Available. This skill provides educational financial frameworks; no proprietary advisor data accessed.
