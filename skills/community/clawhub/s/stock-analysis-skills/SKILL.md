---
name: stock-analysis
description: >
  This skill should be used when the user asks to "analyze a stock", "research a company",
  "give me a research report on [ticker]", "run stock analysis on [company]",
  "do fundamental analysis of [ticker]", "evaluate [company] for investment",
  "what do you think of [ticker]", "analyze [AAPL / TSLA / NVDA / etc.]",
  "deep dive on [company]", or any request for structured equity research,
  investment thesis, or financial analysis of a publicly traded company.
version: 0.1.0
---

# Stock Analysis Pro — Analytical Framework

This skill provides the methodology, analytical standards, and scoring logic for producing institutional-quality equity research reports across 10 structured modules. It is loaded automatically whenever a stock or company analysis is requested.

---

## Core Analytical Principles

Apply these principles across every module of every report:

- **Data-first**: Ground every assertion in current financial data, market data, or explicitly sourced intelligence. Do not make claims without evidence.
- **Multi-dimensional**: No single factor determines an investment case. Integrate macro, technical, fundamental, valuation, and sentiment signals before forming a view.
- **Balanced**: Present both bull and bear cases within each module. Avoid confirmation bias — if the data contradicts the prevailing narrative, say so.
- **Transparent**: Explicitly flag data gaps, estimation uncertainty, and the limits of web-sourced information. Use ⚠️ where data is unavailable or estimated.
- **Actionable**: Every module ends with a Key Takeaway. The final scorecard delivers a clear, justified investment stance — not "it depends."

---

## The 10-Module Framework

Each module addresses a distinct analytical dimension and contributes to the overall investment verdict:

| # | Module | Core Question |
|---|--------|---------------|
| 1 | Macro Analysis | Is the external environment a tailwind or headwind? |
| 2 | Stock Trend Analysis | What is price action signaling about near-term direction? |
| 3 | Company Competency | Is the business fundamentally strong with a durable moat? |
| 4 | Valuation Analysis | Is the stock priced fairly relative to intrinsic value and peers? |
| 5 | Earnings & Analyst Forecast | Are earnings growing and consistently beating expectations? |
| 6 | Competitor Benchmarking | How does the company rank against its direct peers? |
| 7 | Risk Analysis | What could go wrong and how severe are the consequences? |
| 8 | ESG & Governance | Is the company sustainable and well-governed for the long run? |
| 9 | Catalyst & Event Tracker | What near-term events could move the stock materially? |
| 10 | Investment Summary | What is the bottom-line investment verdict with full rationale? |

---

## Scoring Logic (Module Scorecard)

Rate each module from 1 to 5 based on the analytical findings:

| Score | Meaning |
|-------|---------|
| 5 | Strongly positive signal — clear tailwind or outstanding quality |
| 4 | Moderately positive — good, with minor concerns |
| 3 | Neutral — mixed signals or insufficient differentiation |
| 2 | Moderately negative — notable headwinds or weaknesses |
| 1 | Strongly negative — significant concern, major red flag |

**Risk Profile (Module 7) is scored inversely**: 5 = very low risk, 1 = very high risk.

The **Overall Score** is a simple average of the 9 module scores (excluding the summary module). Weighting guidance:
- For **short-term theses**: weight Technical Trend and Catalysts more heavily
- For **long-term theses**: weight Macro, Company Competency, Valuation, and ESG more heavily

---

## Investment Stance Thresholds

Map the overall module scorecard average to a recommended analyst stance:

| Overall Score | Analyst Stance |
|--------------|----------------|
| 4.5 – 5.0 | ⭐⭐⭐⭐⭐ Strong Buy |
| 3.5 – 4.4 | ⭐⭐⭐⭐ Buy |
| 2.5 – 3.4 | ⭐⭐⭐ Hold |
| 1.5 – 2.4 | ⭐⭐ Reduce |
| 1.0 – 1.4 | ⭐ Avoid |

Always articulate what would need to change for the stance to upgrade or downgrade by one level.

---

## Data Source Hierarchy

Prioritize higher-quality sources when gathering data. Prefer recency over breadth.

1. Company SEC filings: 10-K (annual), 10-Q (quarterly), 8-K (material events)
2. Company investor relations pages and official earnings press releases
3. Analyst consensus platforms: FactSet, Bloomberg, Refinitiv, LSEG (via web search)
4. Financial data aggregators: Morningstar, Yahoo Finance, Macrotrends, Wisesheets
5. Investment research platforms: Seeking Alpha, The Motley Fool, GuruFocus
6. ESG rating agencies: MSCI ESG Ratings, Sustainalytics, S&P Global ESG
7. Industry and macro data: IMF, World Bank, Federal Reserve, OECD, industry associations
8. News and events: Reuters, Bloomberg, Financial Times, Wall Street Journal

---

## Key Analytical Standards

Apply these standards consistently across all modules:

**Financial metrics:**
- Use trailing twelve months (TTM) for income statement metrics unless forward estimates are more relevant
- Compare multiples to both sector median and 3–5 year historical average for the same company
- When multiples are not meaningful (e.g., negative P/E due to losses), use EV/Sales or note the limitation
- Free cash flow yield (FCF / Market Cap) is often a more reliable signal than reported earnings multiples

**Technical analysis:**
- Treat indicators as confirming or diverging signals — not standalone buy/sell triggers
- RSI interpretation: >70 = overbought territory; <30 = oversold territory; divergence with price direction is more informative than absolute level alone
- MACD: focus on signal line crossovers and histogram trend (expanding vs. contracting momentum)
- Golden Cross (50-day MA crossing above 200-day MA) and Death Cross (crossing below) are significant trend signals
- Volume confirmation: price moves on high relative volume are more reliable than low-volume moves

**Valuation (DCF guidance):**
- Use a 2-stage or 3-stage model: near-term explicit forecast period (5 years) + terminal value
- WACC should reflect sector risk: typically 8–10% for large-cap defensive, 10–14% for growth/tech, 12–16% for speculative/small-cap
- Terminal growth rate: 2–3% for stable businesses, aligned with long-run nominal GDP growth; avoid rates above 4% without explicit justification
- Sensitivity-test the DCF on WACC ± 1% and terminal growth rate ± 0.5% to show the fair value range

**Risk assessment:**
- Assign risk levels (Low / Medium / High) based on both likelihood and severity of impact
- A High risk designation requires at least one of: (a) high probability of occurrence, (b) potentially company-threatening consequence, or (c) a clear near-term trigger
- ESG risk should consider both the direct financial impact of ESG failings and the reputational/regulatory overhang

---

## Reference Files

Load these reference files for deeper methodology when needed:

- **`references/macro-framework.md`** — Detailed macro analysis methodology: GDP, rates, inflation, regulatory landscape
- **`references/technical-analysis.md`** — Technical indicator interpretation guide with signal tables
- **`references/fundamental-framework.md`** — Company competency and earnings analysis methodology
- **`references/valuation-framework.md`** — Valuation methodology including DCF construction and relative valuation
- **`references/risk-esg-framework.md`** — Risk rating criteria and ESG/governance assessment standards
