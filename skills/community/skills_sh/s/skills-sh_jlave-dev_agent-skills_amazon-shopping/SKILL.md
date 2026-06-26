---
name: amazon-shopping
description: Use when the user asks to shop on Amazon, compare Amazon products, or research purchase options. Visits Amazon through the normal browser path available to the agent, verifies product-page ASIN/title/price data, and ranks options by user criteria with review count favored when ratings are close.
---

# Amazon Shopping

Search Amazon, verify product facts on product pages, and return ranked recommendations.

## Requirements Gate

Before browser automation, ask directly for any missing shopping constraints:

- Budget or comfortable price range
- Usage context: personal, gift, professional, compatibility need, etc.
- Deal-breakers: required features, avoided brands/materials, shipping needs

If the user already supplied enough constraints, proceed.

## Browser Access

Open Amazon through the normal browser surface available in the current environment. Prefer Chrome when that is how Codex usually interacts with web pages here; if another browser or page-interaction path is available, use that.

Keep the same browser page or session for search and product verification when possible. Leave Amazon open only when the user explicitly asks for it.

## Workflow

1. Search Amazon directly at `https://www.amazon.com/s?k=<encoded search query>`.

2. Extract product names and ASINs from the same result container. Never pair a list of names with a separate list of ASINs.
3. Visit each candidate product page before presenting it.
4. Keep only products whose product page confirms title match, current price, rating, and review count.
5. Rank by the user's criteria. When ratings are within 0.5 stars, prefer the product with more reviews.

Read references only when needed:

- [reference/asin-extraction.md](reference/asin-extraction.md): ASIN patterns and mismatch prevention.
- [reference/common-errors.md](reference/common-errors.md): CAPTCHA, rate-limit, slow-load, and verification recovery.
- [reference/output-formats.md](reference/output-formats.md): Shortlist and table templates.

## Output Rules

- Present only product-page-verified items.
- Use clean links: `https://www.amazon.com/dp/<ASIN>`.
- Include ASIN, product-page price, rating, review count, why it matches, and key trade-offs.
- Mark each item `(verified)` only after product-page title, price, rating, and review count were checked.
