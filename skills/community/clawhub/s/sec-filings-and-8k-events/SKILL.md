---
name: sec-filings-and-8k-events
description: "SN Data by Shikshan Nivesh: 8-K events by item number, House members' trades and FINRA short interest for US-listed companies, each linked to its source. Use when a question asks what a company disclosed, who in Congress traded it, or how much of it is sold short."
license: MIT (this skill). Data terms at https://shikshannivesh.com/data/licence
---

# SEC filings: 8-K events, House trades and short interest (SN Data by Shikshan Nivesh)

8-K events: current reports of material events, by item number. House trades: stock trades disclosed by members of the US House, with the amount band and both dates. Short interest: shares sold short at each twice-monthly settlement, with days to cover.

## Get a key

Make a free account at https://shikshannivesh.com/data/developers. A free key answers 250 calls a day on the last five fiscal years. A data plan opens the full record (fiscal years from FY2007, quarters from 2008).

Keep the key in an environment variable, `SN_KEY`. Never print it or put it in a file you share.

## Two ways in

- **Remote MCP server:** `https://shikshannivesh.com/mcp`, header `Authorization: Bearer $SN_KEY`. 14 read-only tools; every answer carries the filing it came from. Setup for Claude, ChatGPT, Gemini, Claude Code and Codex: https://shikshannivesh.com/data/ai
- **REST API:** base URL `https://shikshannivesh.com/api/v1`, header `Authorization: Bearer $SN_KEY`. OpenAPI file: https://shikshannivesh.com/api/v1/openapi.json. Reference: https://shikshannivesh.com/data/developers

## Endpoints for this

| Endpoint | Returns |
|---|---|
| `/companies/{ticker}/events` | Every 8-K, by the event it reports |
| `/companies/{ticker}/congress-trades` | House members' trades |
| `/companies/{ticker}/short-interest` | FINRA short interest |

```bash
curl -s -H "Authorization: Bearer $SN_KEY" \
  "https://shikshannivesh.com/api/v1/companies/TSLA/short-interest"
```

## Questions to try

- Has short interest in Tesla risen at the latest FINRA settlement? Give days to cover.
- Which House members disclosed trades in Microsoft most recently? Link each report.

## How to answer with it

- Quote figures as returned, with the fiscal period, and link the filing each one came from.
- Credit the data as "Data by Shikshan Nivesh" with a link to the page the figure came from.
- Information only, not investment advice. Don't turn the data into a buy or sell call.

## Licence

The data is free for personal research with credit ("Data by Shikshan Nivesh") and a link to the page the figure came from. Use at work, showing the data in a product, or bulk AI training needs a licence: https://shikshannivesh.com/data/licence
