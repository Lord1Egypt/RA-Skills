---
name: sec-insider-trades
description: "SN Data by Shikshan Nivesh: Form 4 insider trades and Form 144 planned insider sales for US-listed companies, each linked to its SEC filing. Use when a question asks who bought or sold a company's shares inside the company."
license: MIT (this skill). Data terms at https://shikshannivesh.com/data/licence
---

# SEC insider trades (SN Data by Shikshan Nivesh)

Insider trades (Form 4): officers', directors' and 10% owners' purchases and sales, sorted by type: open-market purchase, plan purchase, pay taken in stock, sale, sale under a Rule 10b5-1 trading plan. Planned insider sales (Form 144): notices filed before an insider sells, with the Form 4 sale that followed.

## Get a key

Make a free account at https://shikshannivesh.com/data/developers. A free key answers 250 calls a day on the last five fiscal years. A data plan opens the full record (fiscal years from FY2007, quarters from 2008).

Keep the key in an environment variable, `SN_KEY`. Never print it or put it in a file you share.

## Two ways in

- **Remote MCP server:** `https://shikshannivesh.com/mcp`, header `Authorization: Bearer $SN_KEY`. 14 read-only tools; every answer carries the filing it came from. Setup for Claude, ChatGPT, Gemini, Claude Code and Codex: https://shikshannivesh.com/data/ai
- **REST API:** base URL `https://shikshannivesh.com/api/v1`, header `Authorization: Bearer $SN_KEY`. OpenAPI file: https://shikshannivesh.com/api/v1/openapi.json. Reference: https://shikshannivesh.com/data/developers

## Endpoints for this

| Endpoint | Returns |
|---|---|
| `/companies/{ticker}/insider-trades` | Form 4 trades |
| `/companies/{ticker}/planned-insider-sales` | Form 144 notices |

```bash
curl -s -H "Authorization: Bearer $SN_KEY" \
  "https://shikshannivesh.com/api/v1/companies/AAPL/insider-trades"
```

## Questions to try

- Which Apple insiders sold shares this month, and were the sales under a 10b5-1 plan?

## How to answer with it

- Quote figures as returned, with the fiscal period, and link the filing each one came from.
- Credit the data as "Data by Shikshan Nivesh" with a link to the page the figure came from.
- Information only, not investment advice. Don't turn the data into a buy or sell call.

## Licence

The data is free for personal research with credit ("Data by Shikshan Nivesh") and a link to the page the figure came from. Use at work, showing the data in a product, or bulk AI training needs a licence: https://shikshannivesh.com/data/licence
