---
name: vaper-club-product-reviews
description: Summarize user reviews of a vape product from Vaper.club. Use when users ask what people think of a product, its rating, or common praise and complaints.
---

# Vaper.club Product Reviews

Use the Vaper.club MCP server (`https://api.vaper.club/mcp`). For adults only; reviews are shown as objective user feedback.

## Workflow

1. Call `get_product_reviews` with `query` (and `brand_name` / `model_name` when known). It uses the best-matching product; check `data.product` to confirm it is the product the user means, otherwise refine the query.
2. Read `data.summary` (all reviews: count, average, rating distribution) and `data.reviews` (latest sample, default 10, max 20).
3. Group the sample into common positive and negative themes.
4. Answer with sample size and source URL.

## Rules

- Clearly separate:
  - statistics over **all** reviews (`summary`),
  - the **latest N** reviews returned (`reviews`, N = `returnedReviewCount`),
  - tendencies observed **in that sample**.
- Never present the sample as the opinion of all users.
- Review sources can differ (`source`: VaperClub, Shop, third-party); mention when relevant.
- If `reviewCount` is 0 or small, say the evidence is limited.
- Do not quote reviewers' personal details; reviewer names are display names only.
