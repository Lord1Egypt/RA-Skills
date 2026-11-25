---
name: vaper-club-brand-research
description: Build a brand profile from Vaper.club data. Use when users ask about a vape brand's background, official website, company, aliases, product categories or models.
---

# Vaper.club Brand Research

Use the Vaper.club MCP server (`https://api.vaper.club/mcp`). For adults only.

## Workflow

1. `search_brands` with the brand name (names and aliases are matched). Pick the correct `brandId`; check `aliases` because similar names, sub-brands and series names are easy to confuse.
2. `get_brand_details` with `brand_id` (or `brand_name`).
3. Present: description, official website, company name, categories, models (with how many shop offers each has), average rating and review count.
4. Verify the official website is the one returned in `officialWebsite`; do not substitute a shop website.
5. Include the brand `sourceUrl`.

## Rules

- Label information: verified (Vaper.club data), third-party, inferred, unknown. Do not fill gaps from memory.
- Sub-brands and series are not automatically separate brands; only state relationships that appear in the data.
- Model lists only include models with currently published shop offers.
- For brand news, follow up with `search_posts` using the brand name.
