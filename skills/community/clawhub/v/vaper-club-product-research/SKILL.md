---
name: vaper-club-product-research
description: Research and compare vape products with Vaper.club data. Use when users want to find a product, identify its model, see prices and stock across shops, or compare offers of the same model.
---

# Vaper.club Product Research

Use the Vaper.club MCP server (`https://api.vaper.club/mcp`). For adults only; never give advice on circumventing age verification, purchase restrictions or other legal limits.

## Tools

- `search_products` – each result is **one shop's offer** with brand, model, category, shop, price range, stock status, variants, rating and `sourceUrl`.
- `compare_products` – finds the best-matching standardized model and returns offers of that same model from different shops, cheapest first.
- Helpers: `search_brands` (to confirm a brand name), `get_brand_details` (models under a brand), resource `vaper://site/categories`.

## Workflow

1. Understand the query: brand, model, category, country, shop.
2. Call `search_products` with `query` plus any known `brand_name`, `model_name`, `category_name`, `country`.
3. Check `meta.warnings` – a brand/model that was "not recognized" was only used as a keyword, so results may be broader.
4. To compare, call `compare_products` with the same filters. If it returns no products and a warning, ask the user for a more specific brand and model; do not compare unrelated products.
5. Summarize with price, currency, stock status and shop, and always include `sourceUrl`.

## Rules

- A brand is not a model. A shop offer is not a separate model. Several shops can offer the same model.
- Use the standardized `modelName`; do not guess a model from a product title.
- Only compare fields that actually exist in the response. Missing values are unknown, not zero.
- Prices and stock change; say that they should be confirmed on the shop website (`shopProductUrl`).
- Mixed currencies are not directly comparable unless the user asks for conversion.
- Internal product ids are never exposed; identify products by title, shop and `sourceUrl`.
