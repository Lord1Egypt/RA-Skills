---
name: ai-visibility
description: |
  Check whether AI assistants (ChatGPT, Perplexity, Gemini, Google AI Overviews) recommend a
  brand, product, or crypto token in its category — the AI-era version of search ranking (GEO).
  The only x402 source for AI-recommendation data.

  USE FOR:
  - "Does AI recommend [brand]?" — visibility score 0-100 + who AI names instead
  - Ranking a whole category by how often AI names each brand (share of voice)
  - Whether ChatGPT/Perplexity recommend a crypto token, protocol, or chain
  - Qualifying a sales prospect by its AI-visibility gap (HOT/WARM/COLD)
  - Monitoring which brands/categories are being checked right now

  TRIGGERS:
  - "does ChatGPT recommend", "does AI recommend", "AI visibility", "GEO", "AEO"
  - "share of voice in AI", "brand in AI answers", "who does AI suggest for"
  - "is [token] recommended by AI", "ai visibility score"
  - "qualify this lead", "geo audit", "ai search ranking"

  Use x402 GET calls. Never guess paths — use the exact URLs below or GET /samples first.
mcp:
  - agentcash
---

# AI-Visibility / GEO with the x402 Agent Store

> All endpoints are GET on `https://store.agentexchange.work`. Paid calls return HTTP 402;
> your x402 client signs USDC on Base and retries. Free preview: `GET /samples`.

The unique edge: nobody else in x402 sells "does AI recommend this." Use it for marketing,
GEO/SEO agencies, brand monitoring, sales qualification, and crypto narrative signals.

## Quick Reference

| Task | Endpoint | Price |
|------|----------|-------|
| Brand AI-visibility audit (flagship) | `https://store.agentexchange.work/brands/check?brand=Notion&category=project%20management%20software` | $0.95 |
| Category ranking (who AI recommends, ranked) | `https://store.agentexchange.work/category/ranking?category=CRM%20software` | $0.02 |
| Crypto/token AI-visibility | `https://store.agentexchange.work/crypto/ai-visibility?project=Arbitrum&category=Layer%202%20networks` | $0.05 |
| Sales lead qualifier (tier + opener) | `https://store.agentexchange.work/sales/qualify?brand=acme-roofing.com&category=roofing` | $0.95 |
| AI-Visibility Index (25 brands, 5 industries) | `https://store.agentexchange.work/brands/visibility-index` | $0.005 |
| Live demand signal (what's being checked) | `https://store.agentexchange.work/signal` | $0.005 |

## Notes
- `brand` + `category` are the two key params for `/brands/check` and `/sales/qualify`.
- Results name the competitors AI recommends instead — useful for positioning and outreach.
- Free catalog: `GET https://store.agentexchange.work/` · Free samples: `GET /samples`.
