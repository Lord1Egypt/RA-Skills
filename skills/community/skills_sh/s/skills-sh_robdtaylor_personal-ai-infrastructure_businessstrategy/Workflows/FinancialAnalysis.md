# FinancialAnalysis Workflow

Rigorous analysis of financial statements and business performance.

## Analysis Framework

### Step 1: Data Collection

Request or identify:
- Income statement (P&L) - 2-3 years if available
- Balance sheet - 2-3 years if available
- Cash flow statement
- Industry/sector for benchmarking
- Business stage (startup, growth, mature)

### Step 2: Profitability Analysis

**Revenue Quality**
- Growth rate (YoY, MoM)
- Revenue mix (products, services, recurring)
- Customer concentration
- Seasonality patterns
- Revenue recognition method

**Margin Analysis**
| Metric | Formula | Benchmark Action |
|--------|---------|------------------|
| Gross Margin | (Revenue - COGS) / Revenue | Compare to industry |
| Operating Margin | Operating Income / Revenue | Trend analysis |
| Net Margin | Net Income / Revenue | Quality of earnings |
| Contribution Margin | (Revenue - Variable Costs) / Revenue | Unit economics |

**Cost Structure**
- Fixed vs variable breakdown
- Operating leverage (% fixed costs)
- Cost trends vs revenue trends
- Unusual or one-time items

### Step 3: Liquidity Analysis

**Working Capital**
| Metric | Formula | Target |
|--------|---------|--------|
| Current Ratio | Current Assets / Current Liabilities | >1.5 |
| Quick Ratio | (Cash + AR) / Current Liabilities | >1.0 |
| Working Capital | Current Assets - Current Liabilities | Positive |

**Cash Conversion Cycle**
| Component | Formula | Action |
|-----------|---------|--------|
| Days Sales Outstanding | (AR / Revenue) × 365 | Lower is better |
| Days Inventory Outstanding | (Inventory / COGS) × 365 | Lower is better |
| Days Payable Outstanding | (AP / COGS) × 365 | Higher (within terms) |
| Cash Conversion Cycle | DSO + DIO - DPO | Minimize |

### Step 4: Efficiency Analysis

**Asset Utilization**
| Metric | Formula | Interpretation |
|--------|---------|----------------|
| Asset Turnover | Revenue / Total Assets | Higher = efficient |
| Inventory Turnover | COGS / Average Inventory | Industry dependent |
| AR Turnover | Revenue / Average AR | Higher = faster collection |
| Fixed Asset Turnover | Revenue / Fixed Assets | Capital efficiency |

### Step 5: Leverage Analysis

**Capital Structure**
| Metric | Formula | Risk Level |
|--------|---------|------------|
| Debt-to-Equity | Total Debt / Equity | <1.0 conservative |
| Debt-to-Assets | Total Debt / Total Assets | <0.5 conservative |
| Interest Coverage | EBIT / Interest Expense | >3.0 safe |
| Debt Service Coverage | Operating Cash Flow / Debt Payments | >1.25 |

### Step 6: Cash Flow Analysis

**Operating Cash Flow Quality**
- Cash from operations vs net income (>1.0 is healthy)
- Sources: Working capital changes, non-cash adjustments
- Sustainability of cash generation

**Free Cash Flow**
```
Operating Cash Flow
- Capital Expenditures
- Working Capital Investment
= Free Cash Flow
```

**Burn Rate (for startups)**
```
Monthly Burn = (Cash Start - Cash End) / Months
Runway = Current Cash / Monthly Burn
```

### Step 7: Trend Analysis

Analyze 3-year trends for:
- Revenue growth acceleration/deceleration
- Margin expansion/compression
- Working capital efficiency
- Cash flow consistency

### Step 8: Benchmarking

Compare key metrics to:
- Industry averages
- Direct competitors (if known)
- Historical company performance
- Stage-appropriate benchmarks

## Red Flags Checklist

### Revenue Red Flags
- [ ] Declining growth rate
- [ ] Customer concentration >20%
- [ ] Unusual revenue recognition timing
- [ ] Large "other revenue" without explanation
- [ ] Revenue growing faster than cash collection

### Profitability Red Flags
- [ ] Gross margin declining
- [ ] SG&A growing faster than revenue
- [ ] Frequent "one-time" adjustments
- [ ] EBITDA significantly different from operating cash flow
- [ ] Aggressive capitalization of expenses

### Balance Sheet Red Flags
- [ ] AR growing faster than revenue (collection issues)
- [ ] Inventory growing faster than COGS (obsolescence risk)
- [ ] Goodwill >30% of assets (acquisition risk)
- [ ] Related party receivables
- [ ] Off-balance sheet obligations

### Cash Flow Red Flags
- [ ] Persistent negative operating cash flow with positive net income
- [ ] Declining cash conversion despite revenue growth
- [ ] Heavy reliance on financing activities
- [ ] CapEx consistently exceeding depreciation
- [ ] Stretched payables funding operations

## Output Template

```
📊 FINANCIAL ANALYSIS: [Company Name]
Period: [Date Range]
Industry: [Sector]

═══════════════════════════════════════
EXECUTIVE SUMMARY
═══════════════════════════════════════
[3-5 bullet points on overall health]

═══════════════════════════════════════
KEY METRICS DASHBOARD
═══════════════════════════════════════
Revenue:        £X.XM (YoY: +X%)
Gross Margin:   XX% (Industry: XX%)
EBITDA:         £X.XM (XX% margin)
Free Cash Flow: £X.XM
Runway:         X months

═══════════════════════════════════════
PROFITABILITY
═══════════════════════════════════════
[Analysis with trends]

═══════════════════════════════════════
LIQUIDITY & WORKING CAPITAL
═══════════════════════════════════════
[Analysis with trends]

═══════════════════════════════════════
EFFICIENCY
═══════════════════════════════════════
[Analysis with trends]

═══════════════════════════════════════
LEVERAGE & RISK
═══════════════════════════════════════
[Analysis with trends]

═══════════════════════════════════════
⚠️ CONCERNS / RED FLAGS
═══════════════════════════════════════
1. [Issue with impact]
2. [Issue with impact]
3. [Issue with impact]

═══════════════════════════════════════
✅ RECOMMENDATIONS
═══════════════════════════════════════
Immediate (0-30 days):
1. [Action]

Short-term (1-3 months):
1. [Action]

Medium-term (3-12 months):
1. [Action]
```

## Industry Benchmarks Reference

Quick reference for common sectors (adjust based on research):

| Sector | Gross Margin | Operating Margin | Asset Turnover |
|--------|--------------|------------------|----------------|
| SaaS | 70-85% | 15-25% | 0.5-1.0 |
| E-commerce | 25-45% | 5-15% | 1.5-2.5 |
| Professional Services | 30-50% | 10-20% | 1.0-2.0 |
| Manufacturing | 20-40% | 5-15% | 1.0-1.5 |
| Retail | 25-35% | 3-8% | 2.0-3.0 |
