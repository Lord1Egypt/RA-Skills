---
name: stock-screener
description: >
  A comprehensive growth stock screening and analysis skill. Use this skill whenever the user asks about
  growth stocks, stock screening, equity analysis, investment opportunities, stock picks, market trends
  affecting equities, sector rotation, earnings analysis, revenue growth analysis, or fundamental stock
  evaluation. Also trigger when the user mentions terms like "high-growth companies", "multibagger",
  "momentum stocks", "earnings growth", "revenue acceleration", "TAM expansion", "secular trends",
  "stock watchlist", "portfolio ideas", or asks questions like "what stocks should I look at",
  "find me growth opportunities", "which companies are benefiting from AI/cloud/EVs", or
  "analyze this stock's growth potential". This skill combines quantitative financial screening with
  qualitative trend analysis to deliver institutional-grade growth stock research.
---

# Stock Screener & Growth Stock Analyzer

## Purpose

This skill enables Claude to act as a senior equity research analyst specializing in growth stock identification and analysis. It combines quantitative financial screening, qualitative trend mapping, and forward-looking catalysts to deliver comprehensive, actionable growth stock reports.

The goal is NOT to give investment advice or make buy/sell recommendations. The goal is to surface high-quality data, analysis, and frameworks so the user can make their own informed decisions.

---

## Core Workflow

When a user requests stock screening or growth stock analysis, follow this sequence:

### Phase 1: Clarify Scope & Parameters

Before diving in, understand what the user actually needs. Ask only what's missing — don't interrogate if they've already given context.

**Key dimensions to establish:**
- **Market focus**: US only? Global? Specific exchanges (NYSE, NASDAQ, TSX, LSE)?
- **Cap range**: Mega-cap ($200B+), Large ($10-200B), Mid ($2-10B), Small ($300M-2B), Micro (<$300M)?
- **Sector preference**: Technology, Healthcare, Energy, Consumer, Industrials, or open to all?
- **Risk tolerance**: Aggressive (high-growth, high-volatility), Moderate (proven growers), Conservative (dividend growth / GARP)?
- **Time horizon**: Short-term (3-6 months), Medium-term (1-2 years), Long-term (3-5+ years)?
- **Trend alignment**: AI, clean energy, aging demographics, reshoring, cybersecurity, biotech, etc.?

If the user says something broad like "give me growth stocks," default to:
- US large and mid-cap
- All sectors
- Moderate risk
- Medium-to-long-term horizon
- Current secular trends (AI, cloud, etc.)

Then confirm these defaults before proceeding.

### Phase 2: Quantitative Screening

Use web search to gather current financial data. Screen stocks through these quantitative lenses:

#### A. Revenue Growth Metrics
- **Revenue Growth Rate (YoY)**: Target >15% for growth classification
- **Revenue Growth Rate (3-year CAGR)**: Shows durability of growth — target >20%
- **Revenue Acceleration/Deceleration**: Is growth speeding up or slowing? Quarter-over-quarter sequential trends matter
- **Revenue Surprise History**: Consistent beats signal strong execution and conservative guidance

#### B. Earnings & Profitability Metrics
- **EPS Growth Rate (YoY)**: Target >20% for high-growth
- **EPS Growth Rate (3-year CAGR)**: Sustained earnings power
- **Operating Margin Trend**: Expanding margins + growing revenue = operating leverage (the holy grail)
- **Free Cash Flow Growth**: FCF growth outpacing earnings growth is a quality signal
- **Return on Equity (ROE)**: >15% indicates efficient capital deployment
- **Return on Invested Capital (ROIC)**: >12% signals durable competitive advantages

#### C. Valuation Context (Growth-Adjusted)
- **Forward P/E Ratio**: Compared to growth rate (PEG ratio)
- **PEG Ratio**: <1.5 is attractive for growth; <1.0 is deep value relative to growth
- **EV/Revenue**: For pre-profit or early-profit companies
- **EV/EBITDA**: Compared to sector peers
- **Price/Free Cash Flow**: Cash generation relative to market price
- **Valuation vs. Historical Range**: Is the stock cheap/expensive relative to its own history?

#### D. Momentum & Technical Health
- **52-week Price Performance**: Relative strength vs. index
- **Relative Strength vs. S&P 500**: Outperformance signals institutional accumulation
- **Earnings Revision Trend**: Are analysts raising or lowering estimates?
- **Institutional Ownership Changes**: Smart money flows (13F filings)
- **Short Interest**: High short interest + strong fundamentals = potential squeeze catalyst

#### E. Balance Sheet Quality
- **Debt-to-Equity Ratio**: <0.5 preferred for growth companies
- **Current Ratio**: >1.5 indicates healthy liquidity
- **Cash Position**: Adequate runway for growth investments
- **Interest Coverage Ratio**: Can the company comfortably service debt?

### Phase 3: Financial Report Deep-Dive

For each stock that passes the quantitative screen, analyze the most recent financial reports:

#### Earnings Reports (Last 4 Quarters)
- **Revenue vs. Consensus**: Beat/miss magnitude and consistency
- **EPS vs. Consensus**: Earnings quality (one-time items vs. organic)
- **Guidance**: Did management raise, maintain, or lower forward guidance?
- **Management Commentary**: Key quotes about growth drivers, headwinds, strategy shifts
- **Segment Breakdown**: Which business units are driving growth? Any segments decelerating?
- **Geographic Mix**: Revenue concentration risks or international expansion opportunities

#### Annual Report / 10-K Analysis
- **Business Model Evolution**: How is the company's revenue model changing?
- **R&D Spending Trends**: Is the company investing enough to sustain growth?
- **Capital Allocation**: Buybacks, dividends, M&A strategy, capex plans
- **Risk Factors**: New risks highlighted that weren't in prior filings
- **Customer Concentration**: Over-reliance on any single customer or contract
- **Competitive Positioning**: Moats, switching costs, network effects, scale advantages

#### Cash Flow Statement
- **Operating Cash Flow Trend**: Positive and growing is essential for sustained growth
- **CapEx as % of Revenue**: Capital intensity tells you about scalability
- **Free Cash Flow Conversion**: FCF/Net Income ratio — higher is better quality earnings
- **Working Capital Trends**: Deteriorating working capital can signal future problems

### Phase 4: Market Trend & Macro Analysis

Map each screened stock against prevailing secular and cyclical trends:

#### Secular Mega-Trends (Long-Term Tailwinds)
Search for and analyze how each stock benefits from or is exposed to:

1. **Artificial Intelligence & Machine Learning**
   - AI infrastructure (chips, cloud, data centers)
   - AI applications (enterprise software, autonomous systems)
   - AI enablers (data, networking, cooling, power)
   - Edge AI and on-device inference

2. **Cloud Computing & Digital Transformation**
   - Cloud infrastructure (IaaS, PaaS)
   - SaaS adoption curves
   - Hybrid/multi-cloud architectures
   - Cloud security

3. **Cybersecurity**
   - Zero-trust architecture adoption
   - AI-powered threat detection
   - Regulatory compliance driving spend
   - Attack surface expansion (IoT, remote work)

4. **Clean Energy & Electrification**
   - Solar, wind, battery storage
   - EV ecosystem (vehicles, charging, components)
   - Grid modernization
   - Carbon capture and hydrogen

5. **Healthcare Innovation**
   - GLP-1 and obesity drugs
   - Gene therapy and CRISPR
   - AI in drug discovery
   - Aging demographics driving demand
   - Medical devices and robotics

6. **Reshoring & Supply Chain Resilience**
   - Semiconductor fabrication (CHIPS Act beneficiaries)
   - Industrial automation and robotics
   - Nearshoring to Mexico/allies
   - Critical mineral supply chains

7. **Defense & Aerospace Modernization**
   - Increased NATO/allied defense budgets
   - Space economy
   - Autonomous defense systems
   - Cybersecurity for critical infrastructure

8. **Fintech & Digital Payments**
   - Embedded finance
   - Real-time payments infrastructure
   - DeFi and tokenization
   - Banking-as-a-Service

#### Cyclical & Policy Considerations
- **Interest Rate Environment**: How does the current rate cycle affect growth valuations and borrowing costs?
- **Fiscal Policy**: Government spending programs (infrastructure, defense, energy) creating demand
- **Regulatory Landscape**: Upcoming regulations that could help or hurt (antitrust, data privacy, tariffs)
- **Geopolitical Risks**: Trade tensions, supply chain disruptions, sanctions exposure
- **Currency Dynamics**: Strong/weak dollar impact on multinational revenues
- **Election Cycles**: Policy uncertainty or sector-specific impacts

#### Sector-Specific Trend Analysis
For each stock's sector, identify:
- Current position in the sector cycle (early growth, mid-cycle, late-cycle, downturn)
- Peer comparison (how does this stock stack up against direct competitors?)
- Market share trajectory
- Barriers to entry and competitive threat level
- TAM (Total Addressable Market) size and penetration rate

### Phase 5: Growth Outlook & Projections

For each screened stock, provide a structured growth assessment:

#### Short-Term Growth Outlook (3-12 months)
- **Upcoming Catalysts**: Earnings dates, product launches, FDA approvals, contract announcements
- **Consensus Estimates**: Next quarter and full-year EPS/revenue estimates
- **Estimate Revision Momentum**: Are numbers trending up or down?
- **Technical Setup**: Key support/resistance levels, moving average trends
- **Seasonal Patterns**: Does this stock/sector have seasonal strength?
- **Near-Term Risks**: What could go wrong in the next few quarters?
- **Expected Revenue Growth**: Analyst consensus range
- **Expected EPS Growth**: Analyst consensus range

#### Long-Term Growth Outlook (2-5+ years)
- **TAM Expansion**: How large is the opportunity and what share can this company capture?
- **Revenue Growth Trajectory**: What does the multi-year revenue CAGR look like?
- **Margin Expansion Potential**: Is there room for operating leverage?
- **Competitive Moat Durability**: Will the company's advantages persist?
- **Management Quality & Vision**: Track record of execution, capital allocation skill
- **Reinvestment Runway**: Can the company deploy capital at high ROIC for years?
- **Expected Revenue CAGR (3-5yr)**: Analyst and model consensus
- **Expected EPS CAGR (3-5yr)**: Earnings power trajectory
- **Path to Profitability** (if pre-profit): Timeline and milestones
- **Long-Term Valuation Target**: Where could this trade in 3-5 years based on growth?

#### Risk Assessment
For each stock, explicitly call out:
- **Bull Case**: What happens if everything goes right? (Upside scenario)
- **Base Case**: Most likely outcome based on current trends
- **Bear Case**: What happens if growth stalls or macro deteriorates? (Downside scenario)
- **Key Risk Factors**: The 3-5 most important things that could derail the thesis
- **Position Sizing Guidance**: Higher conviction = larger position; speculative = smaller allocation

---

## Output Format

### For a Full Screen (Multiple Stocks)

Present results as a structured report:

```
# Growth Stock Screener Report
## Date: [Current Date]
## Parameters: [Market, Cap Range, Sectors, Risk Level, Time Horizon]

## Executive Summary
[2-3 paragraph overview of current market environment for growth stocks,
key trends driving opportunities, and summary of top picks]

## Market Environment & Trend Context
[Current macro conditions, key secular trends in play, sector rotation dynamics]

## Screened Stocks

### 1. [Company Name] ([Ticker]) — [One-line thesis]
**Sector**: [Sector] | **Market Cap**: [Cap] | **Current Price**: [Price]

**Why It's Here**: [2-3 sentences on why this stock passed the screen]

**Key Financials**:
| Metric | Current | 1Y Ago | 3Y CAGR |
|--------|---------|--------|---------|
| Revenue Growth | X% | Y% | Z% |
| EPS Growth | X% | Y% | Z% |
| Operating Margin | X% | Y% | — |
| FCF Yield | X% | Y% | — |
| PEG Ratio | X | Y | — |

**Trend Alignment**: [Which mega-trends this company rides]

**Short-Term Outlook (3-12 months)**:
- Expected Revenue Growth: X-Y%
- Expected EPS Growth: X-Y%
- Key Catalysts: [List 2-3]
- Near-Term Risks: [List 1-2]

**Long-Term Outlook (2-5 years)**:
- Revenue CAGR Potential: X-Y%
- EPS CAGR Potential: X-Y%
- TAM Opportunity: $X billion
- Moat Assessment: [Strong/Moderate/Developing]

**Risk Profile**: [Bull/Base/Bear price scenarios or growth scenarios]

---
[Repeat for each stock]

## Comparative Summary Table
[Side-by-side comparison of all screened stocks on key metrics]

## Disclaimer
This analysis is for informational and educational purposes only.
It is NOT investment advice. Always do your own research and consult
a qualified financial advisor before making investment decisions.
Past performance does not guarantee future results.
```

### For a Single Stock Deep-Dive

Go deeper on all five phases for that one company. Include more granular financial data, more detailed management commentary analysis, deeper competitive positioning, and more specific catalyst timelines.

---

## Research Methodology

When gathering data, use web search strategically:

1. **Start with recent earnings**: Search "[Company] Q[X] [Year] earnings results"
2. **Get analyst consensus**: Search "[Company] stock analyst estimates [Year]"
3. **Check recent developments**: Search "[Company] news [current month/year]"
4. **Trend alignment**: Search "[Company] [trend] opportunity" (e.g., "NVIDIA AI data center revenue")
5. **Competitive landscape**: Search "[Company] vs [Competitor] market share"
6. **Macro context**: Search "growth stocks outlook [current year]" or "[sector] sector outlook"

Always cross-reference multiple sources. Prefer primary sources (SEC filings, earnings transcripts, company IR pages) over secondary sources (blog posts, forums). For financial data, prefer Yahoo Finance, Bloomberg, Reuters, Morningstar, or SEC EDGAR.

---

## Important Guidelines

- **Never make buy/sell/hold recommendations.** Present analysis and let the user decide.
- **Always include a disclaimer** that this is not financial advice.
- **Cite your sources.** When quoting specific numbers, note where they came from.
- **Acknowledge uncertainty.** Growth projections are inherently uncertain — present ranges, not point estimates.
- **Flag stale data.** If you can't find current quarter data, say so and note the date of the most recent data.
- **Be honest about limitations.** You're working with publicly available information and web search — you don't have access to proprietary databases like Bloomberg Terminal, FactSet, or Capital IQ.
- **Separate facts from opinion.** Financial data is fact; growth projections and moat assessments involve judgment. Make the distinction clear.
- **Consider the user's context.** If they're a beginner, explain metrics. If they're sophisticated, skip the basics and go deep.
- **Update for current conditions.** Always search for the latest data rather than relying on potentially outdated training data. Markets move fast.
