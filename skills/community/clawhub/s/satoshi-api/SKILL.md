---
name: satoshi-api
description: "Bitcoin intelligence: fee recommendations, mempool status, price, block info, and address lookups via the Satoshi API. Zero config — no node required."
homepage: https://bitcoinsapi.com
metadata:
  {
    "openclaw":
      {
        "emoji": "₿",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Satoshi API — Bitcoin Intelligence

Query the Bitcoin network from any chat message. Powered by the [Satoshi API](https://bitcoinsapi.com) — fee intelligence that saves money on every Bitcoin transaction.

No Bitcoin node required. No API key required.

## What you can ask

- **Fees:** "What are Bitcoin fees right now?" / "Is it cheap to send Bitcoin?"
- **Mempool:** "How's the mempool looking?" / "How many transactions are pending?"
- **Price:** "What's the BTC price?" / "Bitcoin price in USD"
- **Block info:** "When was the last Bitcoin block?" / "What's the current block height?"
- **Address:** "Check Bitcoin address bc1q..." / "What's the balance of [address]?"
- **Halving:** "When's the next Bitcoin halving?"

## Usage

```
uv run satoshi_api.py fees
uv run satoshi_api.py mempool
uv run satoshi_api.py price
uv run satoshi_api.py block
uv run satoshi_api.py address <address>
uv run satoshi_api.py halving
```

## About

Data from [bitcoinsapi.com](https://bitcoinsapi.com) — a free Bitcoin API with real-time fee intelligence, mempool analysis, and 90+ endpoints.

Also available as an MCP server for Claude Code / Cursor: [bitcoin-mcp](https://github.com/Bortlesboat/bitcoin-mcp)
