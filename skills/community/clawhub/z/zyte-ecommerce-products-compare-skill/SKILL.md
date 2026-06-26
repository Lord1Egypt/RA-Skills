---
name: zyte-ecommerce-products-compare-skill
description: >
  Extract structured product data from e-commerce URLs using the Zyte API and generate
  side-by-side comparison tables with intelligent purchase recommendations. Use this skill
  whenever the user wants to compare products from different e-commerce websites, asks
  "which product should I buy", wants a product comparison table, needs help deciding
  between product options, or provides multiple product URLs and wants them analyzed.
  Also trigger when the user says things like "compare these products", "which is the
  better deal", "help me pick between these", "product showdown", or pastes 2+ e-commerce
  URLs. Requires ZYTE_API_KEY in the environment.
---

# Zyte E-Commerce Products Compare Skill

Compare products from any e-commerce site by extracting structured data via the
Zyte API, building a normalized comparison table, and recommending the best option.

## What it does
- Searches products across multiple e-commerce sources
- Extracts price, features, and availability
- Compares products side-by-side
- Recommends the best option

## Input
A natural language product query.

## Skill structure

```
zyte-ecommerce-products-compare-skill/
├── SKILL.md                         ← Workflow and instructions (you are here)
├── scripts/
│   ├── fetch_products.py            ← Parallel fetcher (2–20+ URLs, rate-limit aware)
│   └── parse_product.py             ← Response parser (handles edge cases in Zyte output)
└── references/
    └── zyte-api-notes.md            ← API reference notes and known gotchas
```

**When to read what:**

- `scripts/fetch_products.py` — always. This is the primary data fetching tool.
- `scripts/parse_product.py` — always. Run it on each fetched response file.
- `references/zyte-api-notes.md` — when you hit unexpected errors or need to
  understand a parsing edge case.

## Prerequisites

- `python3` (3.8+, stdlib only — no pip installs required)
- `ZYTE_API_KEY` set in the environment

## Input

Gather from the user:

| Field     | Required | Description                                             |
|-----------|----------|---------------------------------------------------------|
| `urls`    | Yes      | List of product page URLs (at least 1, ideally 2+)     |
| `intent`  | No       | What the user cares about (e.g. "best value", "most durable") |
| `api_key` | Yes      | Zyte API key (prefer `$ZYTE_API_KEY` from env)          |

---

## Workflow

### Step 1 — Validate inputs

1. Confirm at least one URL is provided. If only one URL is given, extract and
   present its data but note that comparison requires 2+.
2. Each URL must start with `http://` or `https://`.
3. Verify `ZYTE_API_KEY` is set:
   ```bash
   echo "$ZYTE_API_KEY" | head -c 4; echo "..."
   ```
   If empty, ask the user to export it.
4. If URLs span very different product categories (e.g. footwear and electronics),
   warn the user and ask for confirmation before proceeding.

### Step 2 — Fetch product data (parallel)

Use the bundled fetch script to call the Zyte API for all URLs in parallel:

```bash
python3 scripts/fetch_products.py "$ZYTE_API_KEY" \
  "https://example.com/products/item-a" \
  "https://example.com/products/item-b" \
  "https://example.com/products/item-c"
```

The script handles everything:
- Fetches all URLs concurrently (up to 5 workers by default).
- Writes each response to `/tmp/product_1_raw.json`, `/tmp/product_2_raw.json`, etc.
- Retries HTTP 429 (rate limit) with exponential backoff, up to 3 times per URL.
- Reports per-URL errors (401, 422, 520, network failures) without aborting others.
- Decompresses gzip responses automatically.
- Prints progress to stderr and a JSON summary to stdout.

**Performance:** Parallel fetching cuts wall-clock time significantly. For 3 URLs,
expect ~35s instead of ~90s sequential (roughly 60% faster). For 10+ URLs the
savings are even greater since most calls run concurrently.

**Read the summary output** to check which URLs succeeded:

```json
{
  "total": 3,
  "success": 3,
  "failed": 0,
  "total_elapsed": 35.0,
  "results": [
    {"index": 1, "url": "...", "status": "ok", "file_path": "/tmp/product_1_raw.json", "elapsed": 18.2},
    {"index": 2, "url": "...", "status": "ok", "file_path": "/tmp/product_2_raw.json", "elapsed": 34.9},
    {"index": 3, "url": "...", "status": "ok", "file_path": "/tmp/product_3_raw.json", "elapsed": 21.4}
  ]
}
```

**Exit codes:** 0 = all succeeded, 1 = partial success (some failed), 2 = all failed.

### Step 3 — Parse responses

For each successful result from Step 2, run the parse script:

```bash
python3 scripts/parse_product.py /tmp/product_1_raw.json
python3 scripts/parse_product.py /tmp/product_2_raw.json
python3 scripts/parse_product.py /tmp/product_3_raw.json
```

Skip any index where the fetch status was not `"ok"`.

The script outputs normalized JSON to stdout with: `name`, `price`, `currency`,
`currencyRaw`, `brand`, `sku`, `availability`, `rating`, `reviewCount`,
`bestRating`, `description`, `features`, `additionalProperties`, `breadcrumbs`,
`mainImage`, `url`, `regularPrice`.

**Exit codes:** 0 = success, 1 = no product data in response, 2 = file/JSON error.

### Step 4 — Normalize data

Make the extracted data comparable:

1. **Prices** — parse string values (e.g. `"2999.0"`) to floats. Note each
   product's currency. If currencies differ, flag it — don't auto-convert.

2. **Ratings** — normalize to 0–5 scale if `bestRating` differs across products.
   Formula: `normalized = (ratingValue / bestRating) * 5`. If a product has no
   rating, show `—` and don't penalize it in ranking.

3. **Availability** — map Zyte values to readable labels: `InStock` → "In Stock",
   `OutOfStock` → "Out of Stock", `PreOrder` → "Pre-Order".

4. **Specs** — merge `features` and `additionalProperties` into one key-value map.
   Filter out junk entries (seller addresses, numeric-only keys, metadata like
   "net quantity" or "item count"). See `references/zyte-api-notes.md` for
   known junk patterns.

5. **Common fields** — identify fields present across all products for the table
   columns. Product-specific fields go in a "Unique Features" section.

### Step 5 — Build comparison table

Generate a markdown table adapted to the product category:

```
| Attribute      | Product A          | Product B          |
|----------------|--------------------|--------------------|
| Name           | ...                | ...                |
| Price          | $29.99             | $34.99             |
| Regular Price  | $39.99             | —                  |
| Brand          | Brand X            | Brand Y            |
| Rating         | 4.5/5 (120 reviews)| —                  |
| Availability   | In Stock           | In Stock           |
| Key Features   | feature1, feature2 | feature3, feature4 |
```

Rules:
- Use `—` for missing values, never leave cells blank.
- Show discounts: `$29.99 (was $39.99)`.
- Cap "Key Features" at 5 items per product.
- For 4+ products, consider vertical layout if the table gets too wide.

### Step 6 — Key differences

List 3–5 bullet points focused on what would influence a purchase decision:

```
- Product A is 70% cheaper
- Only Product B has customer ratings
- Product C is the only one with detailed material specs
- Product A has the steepest discount (40% off)
```

### Step 7 — Recommendation

**With user intent** — map intent keywords to relevant attributes:

| Keywords                      | Prioritize                                          |
|-------------------------------|-----------------------------------------------------|
| budget / cheap / value        | lowest price, price-to-rating ratio                 |
| best / premium / top          | highest rating, most reviews, brand reputation      |
| comfort / walking / running   | cushioning, weight, sole tech, material             |
| sport / court / outdoor       | support, traction, durability, construction         |
| durability / lasting          | material quality, warranty, build                   |

Produce up to 3 recommendations:

```
🏆 **Best Overall:** [Name] — [1-sentence reason]
💰 **Best Value:** [Name] — [1-sentence reason]
⭐ **Best Premium:** [Name] — [1-sentence reason]
```

Only include categories that make sense for the product set.

**Be honest about product-intent mismatch.** If none of the products actually match
the user's stated need (e.g. user wants running shoes but all products are casual
sneakers), say so clearly and suggest what to look for instead.

**Without intent** — rank by value score:

```
value_score = (rating / 5) * 0.6 + (1 - normalized_price) * 0.4
```

Where `normalized_price = (price - min) / (max - min)` across the set. If a product
has no rating, use the average of the other products as a stand-in.

### Step 8 — Final output

Structure the response as:

```
## Product Comparison
[Table from Step 5]

### Key Differences
[Bullets from Step 6]

### Recommendation
[From Step 7]

### Data Notes
- Source: Zyte API automatic product extraction
- [List any failed URLs with reasons]
- [Note if currencies differ across products]
- [Note if any data was incomplete]
- [Total fetch time and number of parallel workers used]
```

---

## Error handling

Most errors are handled automatically by `scripts/fetch_products.py`. Check
the JSON summary output to see per-URL status.

| Error                      | Handled by                                            |
|----------------------------|-------------------------------------------------------|
| Missing ZYTE_API_KEY       | You (Step 1) — stop and ask user to export it.        |
| Invalid URL format         | `fetch_products.py` — skipped, reported in summary.   |
| HTTP 401                   | `fetch_products.py` — reported as `auth_error`.       |
| HTTP 422                   | `fetch_products.py` — reported as `payload_error`.    |
| HTTP 429 (rate limit)      | `fetch_products.py` — auto-retries 3× with backoff.   |
| HTTP 520/521               | `fetch_products.py` — reported as `http_error`.       |
| No `.product` in response  | `fetch_products.py` — reported as `no_product_data`.  |
| JSON control characters    | `parse_product.py` — handled via `strict=False`.      |
| Missing individual fields  | You (Step 5) — show `—` in table, never crash.        |
| All URLs failed            | Report errors from summary, suggest manual URL check. |
| Mixed currencies           | You (Step 4) — show both, don't convert, flag it.     |

## DNS note

If network calls fail with DNS resolution errors in sandboxed environments,
force a public DNS resolver before running:

```bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```
