---
name: vaper-club-discovery
description: Search Vaper.club for vape industry posts, brands and retail shops. Use when users ask about industry news, articles, brand background or where shops are located.
---

# Vaper.club Discovery

Use the Vaper.club MCP server (`https://api.vaper.club/mcp`) as a structured source of vape industry information. For adults only; never give advice on circumventing age verification, purchase restrictions or other legal limits.

## Tools

- `get_latest_posts` – latest news/reviews/guides (summaries only).
- `search_posts` – keyword search over posts.
- `search_brands`, `get_brand_details` – brand search and profile.
- `search_shops`, `get_shop_details` – shop search (name and/or country) and profile.

Reference resources: `vaper://site/about`, `vaper://site/faq`, `vaper://site/categories`, `vaper://site/languages`.

## Instructions

1. Decide what the user needs: news (posts), a brand, or a shop.
2. Pick the matching tool and use specific terms. `search_brands` and `search_shops` need at least one filter (`query`, `category_name` or `country`); never call them empty.
3. For a brand or shop the user cares about, follow up with `get_brand_details` / `get_shop_details` using the returned `brandId` / `shopId`.
4. Use the `language` parameter matching the user's language when possible.
5. Always give the `sourceUrl` of the Vaper.club page you used.
6. Read `meta.warnings`; if present, tell the user about the limitation (for example unrecognized filters).
7. Do not invent missing data. Shop locations only have country and address; there is no region/city filter.

## Source attribution

Distinguish and label: verified Vaper.club data, third-party data (shop websites), inferred information, unknown information.
