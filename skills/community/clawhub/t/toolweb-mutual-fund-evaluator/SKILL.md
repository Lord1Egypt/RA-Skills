---
name: Mutual Fund Evaluator
description: AI-powered mutual fund evaluation tool for Indian retail investors using web search and investor profiling.
---

# Overview

The Mutual Fund Evaluator is an AI-powered platform designed specifically for Indian retail investors to evaluate mutual fund investments against their unique financial profiles. By combining investor profiling, fund analysis, and real-time web search capabilities, this tool provides personalized investment recommendations that align with individual risk tolerance, time horizons, and financial goals.

The tool analyzes multiple dimensions of the investor's profile—including age, investment horizon, risk appetite, volatility preferences, and tax sensitivity—alongside the characteristics of specific mutual funds. This comprehensive evaluation helps investors make informed decisions whether they are entering the market for the first time, adding to existing portfolios, or deciding whether to hold or exit current positions.

Ideal users include individual retail investors in India, financial advisors seeking quick fund evaluation inputs, and anyone comparing mutual fund options across different life stages and financial scenarios.

## Usage

### Sample Request

```json
{
  "fund_name": "Axis Bluechip Fund Direct Plan",
  "investor_age": 35,
  "investment_goal": "Wealth creation",
  "investment_horizon": "10",
  "investment_mode": "SIP",
  "existing_portfolio": "Some equity funds",
  "risk_tolerance": "High",
  "volatility_preference": "Medium",
  "tax_sensitivity": "High",
  "entry_context": "Adding more"
}
```

### Sample Response

```json
{
  "fund_name": "Axis Bluechip Fund Direct Plan",
  "evaluation_summary": {
    "suitability_score": 8.2,
    "recommendation": "Suitable",
    "key_insights": [
      "Fund aligns well with 10-year horizon",
      "Low expense ratio in Direct plan benefits tax-sensitive investors",
      "Bluechip focus appropriate for medium volatility preference",
      "SIP mode reduces timing risk for volatile equities"
    ]
  },
  "profile_analysis": {
    "investor_age": "35 (prime accumulation phase)",
    "horizon_assessment": "10 years is adequate for equity exposure",
    "risk_match": "High risk tolerance matches equity fund exposure"
  },
  "fund_analysis": {
    "fund_type": "Large Cap Equity",
    "aum": "₹12,500 Cr",
    "expense_ratio": "0.40% (Direct)",
    "3yr_returns": "15.2% CAGR",
    "volatility": "12.5% (Medium)",
    "portfolio_concentration": "Top 10 holdings: 42%"
  },
  "tax_implications": {
    "holding_period": "Long-term capital gains (LTCG) after 1 year",
    "tax_efficiency": "Direct plan saves 0.5% annually vs Regular",
    "ltcg_tax_rate": "20% with indexation benefit"
  },
  "comparative_context": "Outperformer vs Nifty 50 over 5-year period",
  "recommendations": [
    "Start SIP to benefit from rupee-cost averaging",
    "Hold for minimum 3-5 years to absorb market cycles",
    "Rebalance portfolio if equity allocation exceeds 70%"
  ]
}
```

## Endpoints

### GET /
**Root Endpoint**

Returns the API welcome page in HTML format.

**Parameters:** None

**Response:**
- Status: 200
- Content-Type: text/html
- Body: HTML welcome page

---

### POST /evaluate
**Evaluate Mutual Fund**

Evaluates a mutual fund based on investor profile using AI analysis with web search integration. This is the primary endpoint for fund evaluation.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| fund_name | string | Yes | Full name of the mutual fund including Direct/Regular plan |
| investor_age | integer | Yes | Investor's current age |
| investment_goal | string | Yes | Investment goal (e.g., "Wealth creation", "Retirement planning", "Education") |
| investment_horizon | string | Yes | Investment horizon in years (e.g., "5", "10", "20") |
| investment_mode | string | Yes | Investment approach: "Lump sum", "SIP", or "Both" |
| existing_portfolio | string | Yes | Current portfolio status (e.g., "No existing funds", "Some equity funds", "Diversified portfolio") |
| risk_tolerance | string | Yes | Risk appetite level: "Low", "Medium", or "High" |
| volatility_preference | string | Yes | Preferred volatility level: "Low", "Medium", or "High" |
| tax_sensitivity | string | Yes | Tax bracket sensitivity (e.g., "High", "Medium", "Low") |
| entry_context | string | Yes | Investment decision context: "First-time", "Adding more", "Deciding to hold or exit", or "Comparing" |

**Response:**
- Status: 200
- Content-Type: application/json
- Body: Detailed evaluation report including suitability score, fund analysis, tax implications, and recommendations

**Error Response (422):**
- Status: 422
- Content-Type: application/json
- Body: Validation error details with field-level error messages

---

### GET /health
**Health Check**

Checks the operational status and availability of the API service.

**Parameters:** None

**Response:**
- Status: 200
- Content-Type: application/json
- Body: Health status indicator

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

- **Kong Route:** https://api.toolweb.in/tools/mutual-fund-evaluator
- **API Docs:** https://api.toolweb.in:8205/docs
