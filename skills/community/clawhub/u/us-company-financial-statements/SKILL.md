---
name: us-company-financial-statements
description: "SN Data by Shikshan Nivesh: income statement, balance sheet and cash flow of US-listed companies from each 10-K and 10-Q, by quarter and fiscal year, with ratios and revenue by segment. Use when a question needs a reported financial figure for a US company."
license: MIT (this skill). Data terms at https://shikshannivesh.com/data/licence
---

# US company financial statements (SN Data by Shikshan Nivesh)

Financial statements: income statement, balance sheet and cash flow from each 10-K and 10-Q, by quarter and fiscal year, with ratios worked out the same way for every company. Revenue by segment: by business, product and region, from each 10-K.

## Get a key

Make a free account at https://shikshannivesh.com/data/developers. A free key answers 250 calls a day on the last five fiscal years. A data plan opens the full record (fiscal years from FY2007, quarters from 2008).

Keep the key in an environment variable, `SN_KEY`. Never print it or put it in a file you share.

## Two ways in

- **Remote MCP server:** `https://shikshannivesh.com/mcp`, header `Authorization: Bearer $SN_KEY`. 14 read-only tools; every answer carries the filing it came from. Setup for Claude, ChatGPT, Gemini, Claude Code and Codex: https://shikshannivesh.com/data/ai
- **REST API:** base URL `https://shikshannivesh.com/api/v1`, header `Authorization: Bearer $SN_KEY`. OpenAPI file: https://shikshannivesh.com/api/v1/openapi.json. Reference: https://shikshannivesh.com/data/developers

## Endpoints for this

| Endpoint | Returns |
|---|---|
| `/companies` | Every company covered |
| `/companies/{ticker}` | One company and its latest figures |
| `/companies/{ticker}/financials` | Income statement, balance sheet, cash flow (`period=annual` or `quarterly`) |
| `/companies/{ticker}/figures` | Revenue, margins, returns, growth, per-share figures (`ids=revenue,net_income,roic`) |
| `/companies/{ticker}/segments` | Revenue by business, product and region |

```bash
curl -s -H "Authorization: Bearer $SN_KEY" \
  "https://shikshannivesh.com/api/v1/companies/AAPL/financials?period=annual"
```

## Questions to try

- Compare Apple's revenue over its last three fiscal years with NVIDIA's and cite the 10-Ks.

## How to answer with it

- Quote figures as returned, with the fiscal period, and link the filing each one came from.
- Credit the data as "Data by Shikshan Nivesh" with a link to the page the figure came from.
- Information only, not investment advice. Don't turn the data into a buy or sell call.

## Licence

The data is free for personal research with credit ("Data by Shikshan Nivesh") and a link to the page the figure came from. Use at work, showing the data in a product, or bulk AI training needs a licence: https://shikshannivesh.com/data/licence
