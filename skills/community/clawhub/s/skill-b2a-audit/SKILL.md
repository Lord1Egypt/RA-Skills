# Skill: B2A Agent-Discoverability Audit
Version: 1.0 | Created: 2026-03-30

---

## Purpose
Audit any e-commerce site (WooCommerce/Shopify/custom) for AI agent discoverability and shopping readiness.
Outputs a scored report with prioritized fixes to make products visible to AI shopping agents (Google AI Shopping, Perplexity Shopping, AppFunctions agents).

## When to Use
- Before launching a new product line
- When traffic is low despite active inventory
- As part of B2A (Business-to-Agent) commerce infrastructure setup
- Quarterly storefront health check

## Inputs
- `SITE_URL` — the storefront URL to audit (e.g., https://example.com)
- `STORE_TYPE` — WooCommerce | Shopify | Custom (default: WooCommerce)

## Outputs
- Scored report appended to a notes file
- 5-dimension score card (0–10 each)
- Prioritized fix list: 🔴 HIGH / 🟡 MEDIUM / 🟢 LOW

## Audit Dimensions

### 1. Structured Data (schema.org/Product)
Check for:
- `@type: Product` with `name`, `sku`, `url`, `image`, `description`
- `Offer` block: `price`, `priceCurrency`, `availability`
- `brand` with `@type: Brand`
- `gtin` / `gtin13` / `gtin8` — required by Google Shopping and AI agent catalogs
- `mpn` (manufacturer part number)
- `aggregateRating` + `reviewCount`
- `color`, `material`, `weight` product attributes

Tool: Fetch any product page, inspect JSON-LD blocks.

### 2. Machine-Readable Catalog API
WooCommerce: Test `GET /wp-json/wc/store/v1/products` (public, no auth)
Shopify: Test `GET /products.json` (public, no auth)
Check: HTTP status, fields returned (id, name, sku, prices, images, in_stock)

### 3. Google Merchant Center / Shopping Feed
Test common feed URLs:
- `/feed=products`
- `/google-shopping-feed/`
- WooCommerce: Google Listings & Ads plugin
- Shopify: native GMC integration

### 4. Agent Checkout Compatibility
WooCommerce: Test `POST /wp-json/wc/store/v1/cart/add-item` availability
Check for headless cart API, programmatic checkout support

### 5. Product Descriptions (AI Intent Matching)
Evaluate description quality:
- Length > 100 words with specs
- Includes: connection type, battery life, dimensions, weight, use cases
- No tagline-only descriptions

## Scoring Rubric
| Score | Meaning |
|-------|---------|
| 9–10  | Production-ready for AI agents |
| 7–8   | Good, minor fixes needed |
| 5–6   | Partial — key gaps present |
| 3–4   | Visible but not optimized |
| 0–2   | Invisible to AI shopping agents |

## Report Format
```
## [YYYY-MM-DD] B2A Agent-Discoverability Audit — {SITE_URL}

### Score Card
| Dimension | Score | Notes |
...

### 🔴 HIGH Priority
...

### 🟡 MEDIUM Priority  
...

### 🟢 LOW Priority (future)
...

Overall: X/10
```

## Key Insight (from production use)
The biggest gap most e-commerce sites have: WooCommerce/Shopify APIs are browsable by agents, but without GTIN identifiers and a Google Merchant Center feed, products are **invisible to Google AI Shopping, Perplexity Shopping, and Android AppFunctions agents**. The fix is a free WooCommerce plugin + 30 minutes of product data entry. High leverage, low effort.
