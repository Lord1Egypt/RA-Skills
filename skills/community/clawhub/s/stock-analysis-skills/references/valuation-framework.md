# Valuation Framework — Reference Guide

Methodology for Module 4: Valuation Analysis. Covers relative valuation multiples, DCF construction, and the valuation verdict framework.

---

## 1. Relative Valuation Multiples

### P/E (Price-to-Earnings)

**Formula**: Share Price / EPS (TTM)

**Best suited for**: Profitable companies. One of the most widely used valuation metrics across sectors.

**Limitations:**
- Not meaningful for loss-making companies
- Sensitive to non-cash items (depreciation, amortization, stock-based compensation)
- Sensitive to one-time gains/losses — confirm whether the basis is GAAP or non-GAAP (adjusted)

**Benchmarking**: Compare trailing P/E to:
1. Broad market index historical range (e.g., S&P 500 median P/E)
2. Sector median (data sources: Bloomberg, FactSet, Refinitiv, visible alpha sell-side consensus)
3. Company's own 5-year average P/E (or longer cycle depending on sector cyclicality)

If the stock trades at a significant premium to all three benchmarks, there must be clear and verifiable growth/moat justification.

---

### Forward P/E

**Formula**: Share Price / Next Twelve Months (NTM) Consensus EPS

**Why it often matters more than trailing P/E**: Markets are forward-looking. Forward P/E reflects the price investors are paying for future earnings expectations.

**PEG Ratio** = Forward P/E ÷ Expected EPS Growth Rate
- PEG < 1.0: May be undervalued relative to growth (validate growth quality and sustainability)
- PEG 1.0–2.0: Roughly fair to moderately expensive
- PEG > 2.0: Expensive — requires high confidence in growth delivery

---

### P/B (Price-to-Book)

**Formula**: Share Price / Book Value per Share (Equity / Shares Outstanding)

**Best suited for**: Banks, insurance companies, asset-heavy manufacturing, and REITs.

**Less meaningful for**: Asset-light businesses (software, services) where intangibles are significant but not fully reflected on the balance sheet.

| P/B Level | Interpretation |
|-----------|---------------|
| < 1.0x | Trading below book value — may be a value opportunity, or may reflect distress/asset quality issues |
| 1.0–2.0x | Common reasonable range for capital-intensive sectors |
| 2.0–5.0x | Quality premium; more justifiable if ROIC significantly exceeds cost of capital |
| > 5.0x | Significant premium; typically requires high ROIC and high growth to support |

---

### EV/EBITDA

**Formula**: Enterprise Value / EBITDA

**Enterprise Value (EV)** = Market Cap + Total Debt – Cash & Equivalents

**Why it's often superior to P/E for cross-company comparison:**
- More "capital structure neutral" — easier to compare companies with different leverage levels
- Less affected by differences in depreciation policy
- Widely used in M&A and LBO valuation discussions

**Sector benchmark ranges (indicative; highly cyclical, adjust for market stage and growth):**
| Sector | Typical EV/EBITDA Range |
|--------|------------------------|
| Technology / SaaS | 15–35x |
| Healthcare | 12–20x |
| Industrials | 8–14x |
| Consumer Staples | 10–16x |
| Energy | 5–10x |
| Banks / Financials | N/A (typically use P/B, P/E) |

---

### P/S (Price-to-Sales)

**Formula**: Market Cap / Annual Revenue (or Share Price / Revenue per Share)

**Best suited for**: Early-stage growth companies not yet profitable; or for comparing companies at different profitability stages.

**Limitations**: Does not reflect profitability differences — at 10x P/S, a company with 80% gross margin is fundamentally different from one with 20%.

**Alternative**: Some analysts use EV/Revenue for a more "capital structure neutral" comparison.

| P/S Level | Implication |
|-----------|-------------|
| < 1x | Very cheap — may signal distress or low growth |
| 1–3x | Common range for mature, profitable companies |
| 3–8x | Growth premium — requires margin expansion path to support |
| > 10x | High growth expectations priced in; vulnerable to multiple compression |

---

### Free Cash Flow Yield

**Formula**: FCF per Share / Share Price (or FCF / Market Cap × 100%)

Typically more reliable than P/E, as FCF is harder to "manage" than accounting earnings.

| FCF Yield | Interpretation |
|-----------|---------------|
| > 5% | Attractive yield; quality companies may be undervalued |
| 3–5% | Reasonable range for quality "compounders" |
| 1–3% | Growth premium reflected |
| < 1% | Expensive; requires very strong growth outlook to justify |

---

## 2. DCF Valuation Framework

DCF estimates intrinsic value by discounting future free cash flows to present value.

### Two-Stage DCF (Standard Form)

**Stage 1: Explicit Forecast Period (Years 1–5)**
- Project revenue growth rate year by year
- Project EBIT margin (or FCF margin) year by year
- Calculate FCF: FCF = EBIT(1-t) + D&A – CapEx – Changes in Working Capital

**Stage 2: Terminal Value**
- Apply a terminal growth rate (g) to Year 5 FCF
- Terminal Value = FCF₅ × (1 + g) / (WACC – g)
- g should generally not exceed long-term nominal GDP growth (US long-term nominal GDP growth ~4-5%; conservative terminal growth 2-3%)

**Intrinsic Value per Share:**
= (Sum of PV of Stage 1 FCFs + PV of Terminal Value – Net Debt) / Diluted Shares Outstanding

---

### WACC Estimation Guide

WACC = (E/V) × Re + (D/V) × Rd × (1–T)

Where:
- E = Market value of equity, D = Market value of debt, V = E + D
- Re = Cost of equity (typically estimated using CAPM)
- Rd = Cost of debt (pre-tax; reference corporate bond yields / bank borrowing rates)
- T = Corporate tax rate

**Estimating cost of equity using CAPM**: Re = Rf + β × (Rm – Rf)
- Rf = Risk-free rate (typically 10-year US Treasury yield for USD-denominated analysis)
- β = Company beta (sensitivity to market moves; specify benchmark index and sample period)
- Rm – Rf = Equity risk premium (use long-term estimate appropriate for the market; Damodaran's annual updates are a common reference)

**Sector WACC reference ranges (indicative; adjust for risk-free rate and risk appetite environment):**
| Sector | Typical WACC Range |
|--------|-------------------|
| Large-cap tech / software | 9–12% |
| Healthcare / pharma | 8–11% |
| Consumer staples / utilities | 6–9% |
| Industrials / manufacturing | 8–11% |
| High-growth / speculative | 12–16% |
| Financial services | Typically use cost of equity directly |

---

### DCF Sensitivity Analysis

Present a sensitivity table showing fair value under different WACC and terminal growth rate assumptions:

| | g = 1.5% | g = 2.0% | g = 2.5% | g = 3.0% |
|---------|----------|----------|----------|----------|
| **WACC = 9%** | $XX.XX | $XX.XX | $XX.XX | $XX.XX |
| **WACC = 10%** | $XX.XX | $XX.XX | $XX.XX | $XX.XX |
| **WACC = 11%** | $XX.XX | $XX.XX | $XX.XX | $XX.XX |
| **WACC = 12%** | $XX.XX | $XX.XX | $XX.XX | $XX.XX |

---

## 3. Valuation Verdict Framework

Synthesize multiples and DCF into a verdict:

**Undervalued**: Stock trades at a significant discount (>15–20%) to:
- DCF intrinsic value AND
- Sector median multiples AND
- Own historical average multiples
The discount is not fully explained by fundamental deterioration.

**Fairly Valued**: Stock trades within ±15% of estimated intrinsic value and is broadly in line with sector and historical multiples; neither a strong buy nor a forced sell.

**Overvalued**: Stock trades at a significant premium (>20%) to intrinsic value and sector comps; the premium requires a high degree of "optimistic scenario" delivery to justify.

**Contextual nuances:**
- High P/E may be supported by high ROIC, strong earnings growth, and low capital intensity → premium may be justified
- Low P/E may be a "value trap": declining earnings or weakening moat → discount may not be an opportunity
- For high-growth companies, compare using "growth-adjusted multiples" (e.g., PEG, P/E-to-growth)

---

## 4. Valuation Module Scoring Guidance

| Score | Condition |
|-------|-----------|
| 5 | Multiple metrics indicate clear undervaluation; adequate margin of safety |
| 4 | Some discount to intrinsic value; multiples reasonably aligned with growth |
| 3 | Valuation roughly fair; multiples broadly consistent with peers and history |
| 2 | Valuation elevated; premium not fully matched by growth outlook |
| 1 | Significantly overvalued; extreme premium; requires near-perfect delivery |
