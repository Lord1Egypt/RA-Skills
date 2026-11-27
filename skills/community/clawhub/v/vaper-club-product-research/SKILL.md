---
name: vaper-club-product-research
description: Vape search and vape price compare using Vaper.club data. Use when users want to search for a vape product, identify its model, check prices and stock across online vape shops, or compare prices and offers of the same model.
---

# Vaper.club Product Research (Vape Search & Vape Price Compare)

Use the Vaper.club MCP server (`https://api.vaper.club/mcp`) for **vape search** and **vape price compare** across online vape retailers. For adults only; never give advice on circumventing age verification, purchase restrictions or other legal limits.

## Tools

- `search_products` – **vape search**: search shop product offers by keyword, brand, model, category, country or shop. Each result is **one shop's offer** with brand, model, category, shop, price range, stock status, variants, rating and `sourceUrl`.
- `compare_products` – **vape price compare**: finds the best-matching standardized model and compares prices and stock of that same model across different shops, cheapest first.
- Helpers: `search_brands` (to confirm a brand name), `get_brand_details` (models under a brand), resource `vaper://site/categories`.

## Workflow

1. Understand the query: brand, model, category, country, shop.
2. Run **vape search** via `search_products` with `query` plus any known `brand_name`, `model_name`, `category_name`, `country`.
3. Check `meta.warnings` – a brand/model that was "not recognized" was only used as a keyword, so results may be broader.
4. Run **vape price compare** via `compare_products` with the same filters to compare prices and stock across shops. If it returns no products and a warning, ask the user for a more specific brand and model; do not compare unrelated products.
5. Summarize with price, currency, stock status and shop, and always include `sourceUrl`.

## Rules

- A brand is not a model. A shop offer is not a separate model. Several shops can offer the same model.
- Use the standardized `modelName`; do not guess a model from a product title.
- Only compare fields that actually exist in the response. Missing values are unknown, not zero.
- Prices and stock change; say that they should be confirmed on the shop website (`shopProductUrl`).
- Mixed currencies are not directly comparable unless the user asks for conversion.
- Internal product ids are never exposed; identify products by title, shop and `sourceUrl`.
