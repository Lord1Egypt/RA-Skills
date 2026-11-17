---
name: switch402
description: Web data for agents, paid per call in USDC on Base via x402 - page to markdown, site map, page metadata, screenshots, web search and PDF text from api.switch402.com. We built and run switch402.
version: 1.0.0
homepage: https://switch402.com
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# switch402

switch402 is a pay-per-call web data API for AI agents. We built it and we operate it at
`https://api.switch402.com`. There is no account and no API key: each paid call is a single x402
payment in USDC on Base (eip155:8453), and you are charged only when the call succeeds.

This skill contains instructions only. It holds no code, no keys and never pays by itself.

## When to use

- The user wants a public web page as clean markdown, a list of a site's URLs, a page's metadata,
  a screenshot, web search results, or the text of a public PDF.
- The user is fine paying a small USDC amount per call from their own x402-capable wallet.

## Tools and prices (USDC on Base, charged only on success)

| Endpoint (POST JSON) | MCP tool | What it returns | Price |
|---|---|---|---|
| `/v1/scrape` `{"url"}` | `scrape` | Page as clean markdown | $0.008 |
| `/v1/scrape/lite` `{"url"}` | `scrape_lite` | Markdown, lite tier for simple pages | $0.003 |
| `/v1/map` `{"url","limit"?}` | `map` | Same-site links + sitemap URLs | $0.001 |
| `/v1/metadata` `{"url"}` | `metadata` | Title, description, canonical, OpenGraph/Twitter, JSON-LD | $0.001 |
| `/v1/screenshot` `{"url"}` | `screenshot` | 1280x800 PNG (base64) | $0.008 |
| `/v1/screenshot/full` `{"url"}` | `screenshot_full` | Full-page PNG (base64) | $0.012 |
| `/v1/search` `{"query"}` | `search` | Up to 10 ranked results | $0.008 |
| `/v1/pdf` `{"url"}` | `pdf` | Text per page (text PDFs, up to 50 pages / 10 MB) | $0.008 |
| `/v1/quote?url=` (GET) | `quote` | Price, payment status, capacity | Free |

Authoritative, machine-readable prices: `https://api.switch402.com/.well-known/x402` and
`https://api.switch402.com/openapi.json`. The amount to sign always comes from the live 402 response.

## How to call

1. Free check first: `curl -s "https://api.switch402.com/v1/quote?url=https://example.com"`.
2. Make the request without payment, for example
   `curl -s -X POST https://api.switch402.com/v1/map -H 'content-type: application/json' -d '{"url":"https://example.com"}'`.
   It returns HTTP 402 with x402 payment requirements.
3. **Ask the user to approve the exact price before paying.** Never pay without explicit approval,
   and never pay more than the 402 response asks for.
4. Retry the same request with the signed x402 payment header, using the user's own x402 client or wallet
   tooling. With MCP, retry the tool call with `_meta["x402/payment"]`.

MCP (streamable HTTP): `https://api.switch402.com/mcp`.

## Safety

- Every input (URL or query) is sent to api.switch402.com, which we operate. Do not send private URLs or secrets.
- Use a separate wallet holding only a small amount of USDC. This skill never asks for or stores a private key.
- Free, fair-use limits apply to the free quote endpoint.

## Links

- Site: https://switch402.com
- Docs for agents: https://api.switch402.com/llms.txt
- Hermes Agent plugin (same API): https://github.com/Duffey234/switch402-hermes
