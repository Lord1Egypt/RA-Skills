---
name: Indian Stock Fundamental Analyser
description: AI-powered fundamental analysis for Indian stocks (NSE/BSE) designed for long-term investors seeking data-driven investment insights.
---

# Overview

The Indian Stock Fundamental Analyser is an AI-powered API that delivers comprehensive fundamental analysis for stocks listed on the National Stock Exchange (NSE) and Bombay Stock Exchange (BSE). Built for long-term investors, this tool leverages artificial intelligence and real-time web search to evaluate company health, financial metrics, growth potential, and investment suitability across different time horizons.

The analyser processes stock tickers or company names and generates detailed assessments tailored to your investment timeline, whether you're planning a 3-year, 5-year, or 10-year investment strategy. By combining fundamental financial analysis with current market intelligence, the API removes guesswork from equity research and helps investors make informed decisions backed by quantitative and qualitative data.

Ideal users include retail investors, financial advisors, portfolio managers, and fintech platforms integrating stock analysis into their offerings. Whether you're evaluating blue-chip stocks like TCS and RELIANCE or exploring mid-cap opportunities, this tool provides institutional-grade analysis accessible through a simple API interface.

## Usage

**Analyze a stock for a 5-year investment horizon:**

```json
POST /analyze
Content-Type: application/json

{
  "stock_ticker": "TCS",
  "investment_horizon": "5 Years"
}
```

**Sample Response:**

```json
{
  "stock_ticker": "TCS",
  "investment_horizon": "5 Years",
  "company_name": "Tata Consultancy Services Limited",
  "sector": "Information Technology",
  "market_cap": "14.2 Trillion INR",
  "pe_ratio": 28.5,
  "dividend_yield": 2.3,
  "revenue_growth_3y": "8.2%",
  "profit_margin": "21.5%",
  "roe": "34.2%",
  "debt_to_equity": 0.12,
  "current_price": "3845.50",
  "52_week_high": "4150.00",
  "52_week_low": "3200.75",
  "recommendation": "BUY",
  "confidence_score": 8.2,
  "key_strengths": [
    "Strong market leadership in IT services",
    "Consistent revenue growth and profitability",
    "Robust return on equity exceeding 30%",
    "Low debt levels indicating financial stability"
  ],
  "key_risks": [
    "Currency fluctuation impact on exports",
    "Competition from global IT service providers",
    "Moderate valuation at current levels"
  ],
  "analyst_summary": "TCS presents a solid long-term investment opportunity for 5-year investors. The company's dominant market position, consistent execution, and strong financial metrics support capital appreciation and dividend income. Current valuation is reasonable given growth prospects.",
  "fair_value_estimate": "4200-4500",
  "upside_potential": "12-15%",
  "analysis_date": "2025-01-15"
}
```

## Endpoints

### GET /
**Root endpoint**

Returns the API welcome page in HTML format.

**Parameters:** None

**Response:** HTML content (text/html)

---

### POST /analyze
**Analyze Stock Fundamentals**

Performs comprehensive AI-driven fundamental analysis of an Indian stock using web search and financial metrics evaluation.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `stock_ticker` | string | Yes | NSE/BSE stock ticker symbol or company name (e.g., TCS, RELIANCE, HDFCBANK) |
| `investment_horizon` | string | Yes | Investment timeframe in years (e.g., 3 Years, 5 Years, 10 Years) |

**Response Shape:**

The response returns a comprehensive analysis object containing:
- Stock identification fields (ticker, company name, sector)
- Current market data (price, market cap, 52-week range)
- Financial metrics (P/E ratio, dividend yield, ROE, debt-to-equity)
- Growth metrics (3-year revenue growth, profit margins)
- AI-generated recommendation with confidence score
- Key strengths and risk factors
- Fair value estimation and upside potential
- Analyst summary tailored to investment horizon

**Status Codes:**
- `200`: Successful analysis
- `422`: Validation error (missing or invalid parameters)

---

### GET /health
**Health Check**

Returns the health status of the API service.

**Parameters:** None

**Response:** JSON object indicating service status

---

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.toolweb.in/tools/indian-stock-fundamental-analyzer
- **API Docs:** https://api.toolweb.in:8204/docs
