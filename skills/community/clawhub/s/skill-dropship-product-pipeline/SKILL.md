---
name: skill-dropship-product-pipeline
version: 1.0.0
description: >
  End-to-end dropship product lifecycle pipeline. CJ Dropshipping sourcing → margin check
  → Flux Kontext AI hero image → WooCommerce publish → CJ supplier mapping for auto-fulfillment.
requires:
  env:
    - FAL_KEY
    - OPENAI_API_KEY
    - CJ_ACCESS_TOKEN
    - WOO_URL
    - WOO_KEY
    - WOO_SECRET
    - WP_URL
    - WP_USER
    - WP_APP_PASS
  bins:
    - node
---

# skill-dropship-product-pipeline v1.0.0

Full end-to-end dropship product lifecycle — from CJ Dropshipping search to a live WooCommerce listing with an AI-generated hero image.

## Pipeline Steps

1. **CJ Sourcing** — Keyword search or direct product ID. Margin check (min 40%). Variant extraction.
2. **Hero Image** — Flux Kontext Dev (`fal-ai/flux-kontext/dev`) using the real CJ product photo as reference. Lifestyle background, product in active use, warm mood, 1:1 square.
3. **WooCommerce Publish** — Upload hero + gallery images, create product, set price/SKU.
4. **CJ Mapping** — Add product to your `cj-supplier-selection.json` for auto-fulfillment via `skill-dropshipping-fulfillment`.

> **Pipeline ends at WooCommerce publish.** Video creation is a separate step — use [skill-tiktok-video-pipeline](https://clawhub.com/skills/skill-tiktok-video-pipeline).

## Usage

```bash
# Source by keyword — finds best margin product
node scripts/pipeline.js --keyword "ring light" --sell-price 89

# Source by CJ product ID — skip sourcing step
node scripts/pipeline.js --cj-pid 2603020206551636100 --sell-price 69

# Dry run — skip WooCommerce publish (test mode)
node scripts/pipeline.js --keyword "desk lamp" --sell-price 99 --dry-run
```

## Options

| Flag | Required | Description |
|---|---|---|
| `--keyword` | ✅ (or `--cj-pid`) | CJ search keyword |
| `--cj-pid` | ✅ (or `--keyword`) | Known CJ product ID, skips search |
| `--sell-price` | ✅ | Selling price in your local currency |
| `--dry-run` | ❌ | Skip WooCommerce publish |
| `--lang` | ❌ | Language: `en`, `ar`, `both` (default: `en`) |
| `--min-margin` | ❌ | Minimum margin % (default: 40) |

## Credentials Setup

Create credential files or use environment variables:

```bash
# CJ Dropshipping
export CJ_ACCESS_TOKEN="your-cj-token"

# WooCommerce
export WOO_URL="https://yourstore.com"
export WOO_KEY="ck_..."
export WOO_SECRET="cs_..."

# WordPress media upload
export WP_URL="https://yourstore.com"
export WP_USER="your-wp-username"
export WP_APP_PASS="your-app-password"

# AI services
export FAL_KEY="your-fal-key"        # Flux Kontext hero image
export OPENAI_API_KEY="your-key"     # GPT-4o fallback for hero
```

## Hero Image Standard

- **Model:** Flux Kontext Dev (`fal-ai/flux-kontext/dev`)
- **Method:** Real CJ product photo as `image_url` input — product appearance locked from frame 1
- **Style:** Lifestyle background, product in active use, shallow DOF, warm mood, 1:1 square
- **Fallback:** GPT-4o `images/edits` if Flux fails

## Output Files

- `hero-{slug}.jpg` — Product hero (Flux Kontext or GPT-4o fallback)
- `pipeline-result-{slug}.json` — WooCommerce product ID, CJ mapping, cost/margin breakdown

## Economics

- Min margin default: 40%
- Hero image cost: ~$0.05–0.10 per product (Flux Kontext)
- Total pipeline cost per product: under $0.20

## Recommended Stack

For the full dropship automation stack:

1. **This skill** — source + list products
2. [skill-tiktok-video-pipeline](https://clawhub.com/skills/skill-tiktok-video-pipeline) — create video ads
3. [skill-dropshipping-fulfillment](https://clawhub.com/skills/skill-dropshipping-fulfillment) — auto-fulfill orders via CJ
4. [skill-woocommerce-stock-monitor](https://clawhub.com/skills/skill-woocommerce-stock-monitor) — OOS alerts
