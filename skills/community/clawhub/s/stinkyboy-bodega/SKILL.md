---
name: stinkyboy-bodega
description: One integration, one wallet relationship. Thousands of callable tools, paid per call in USDC via x402. Charge on success only — errors and verification failures settle nothing.
---
# Stinkyboy Bodega

One integration, one wallet relationship. Thousands of callable tools, paid per call in USDC via x402. Charge on success only — errors and verification failures settle nothing.

## Install
Point your MCP client at https://mcp.stinkyboy.co/mcp (Streamable HTTP). No signup:
the first call answers 402 with x402 v2 payment requirements.

## The six tools
## catalog_search

Search all catalog tools. synthesize=true (default) compiles a missing tool on the spot instead of returning a miss.

Parameters: `query, filters, synthesize`

## tool_detail

Full detail for one tool: price, schema, quality score, health, status, changelog.

Parameters: `tool_id`

## call_tool

Execute any catalog tool by id. Payment is charged on success only.

Parameters: `tool_id, inputs`

## get_quote

Price quote for a call or a build before commitment. Free, no payment needed.

Parameters: `tool_id, inputs`

## my_spend

Spend report for a caller wallet: calls, builds, receipts.

Parameters: `wallet`

## create_and_call

State the desired outcome with real inputs; the immediate compiler builds the missing tool and runs it in the same session.

Parameters: `outcome, inputs, path_hint, callback_url`

## Pay
- USDC on Base and Solana via x402 v2 (Linux Foundation standard).
- Schemes: exact, upto, batch-settlement, auth-capture. Credit tokens supported.
- Charge on success only. Unfunded callers get a quote via `get_quote`.

## Trust
- Every call returns a hash-chained receipt (input hash, output hash,
  price, timestamp, previous hash).
- Per-tool public quality scores at https://stinkyboy.co/catalog.

## Docs
Full spec: https://stinkyboy.co/llms-full.txt
