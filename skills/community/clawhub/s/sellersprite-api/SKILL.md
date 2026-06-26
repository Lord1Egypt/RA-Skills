---
name: sellersprite-api
description: "SellerSprite Product Research — Fetch Amazon market data via SellerSprite API: product research, keyword analysis, competitor lookup, ASIN details, Blue Ocean Index scoring. Triggers: product research, sellersprite, amazon product research, blue ocean, keyword research, competitor analysis, market analysis, asin research, amazon fba"
compatibility: darwin,linux
metadata:
  version: 1.0.0
  requires:
    bins:
      - bun
    env:
      - name: SELLERSPRITE_SECRET_KEY
        description: "SellerSprite Open API secret key (get at https://open.sellersprite.com)"
        required: false
        note: "Can also be set via: bunx @teamclaw/sellersprite-cli config set secretKey <key>"
    packages:
      - "@teamclaw/sellersprite-cli"
---

# SellerSprite Product Research

Fetch Amazon market data via SellerSprite API. Each command calls exactly one API endpoint — compose them as needed.

## Quick Start

```bash
# Set API key
export SELLERSPRITE_SECRET_KEY="your-secret-key"

# Browse top categories
bunx @teamclaw/sellersprite-cli market

# Research products by keyword
bunx @teamclaw/sellersprite-cli product --keyword "wireless earbuds"

# Get ASIN details
bunx @teamclaw/sellersprite-cli asin --asin B08N5WRWNW

# Check remaining quota
bunx @teamclaw/sellersprite-cli quota
```

## Commands

| Command | API Endpoint | Description |
|---|---|---|
| `market` | `/v1/market/research` | Market/category research |
| `product` | `/v1/product/research` | Product research by keyword |
| `competitor` | `/v1/product/competitor-lookup` | Competitor lookup by ASIN |
| `asin` | `/v1/asin/{market}/{asin}/with-coupon-trend` | ASIN details + coupon trend |
| `keyword` | `/v1/keyword-research` | Keyword research |
| `quota` | `/v1/visits` | Check API quota |
| `config` | — | Local config management |

## Options

| Option | Applies to | Description | Default |
|---|---|---|---|
| `--keyword <kw>` | product, keyword | Search keyword | (required) |
| `--asin <asin>` | competitor, asin | Target ASIN | (required) |
| `--marketplace <code>` | all data commands | Marketplace code | `US` |
| `--month <yyyyMM>` | product, competitor, keyword | Query month | latest |
| `--page <n>` | market | Page number | `1` |
| `--size <n>` | market, product, competitor, keyword | Results per page (max 100) | `20`/`50` |
| `--format <format>` | all commands | `text` or `json` | `text` |

## References

Detailed specs in `references/` directory:

- `references/api-endpoints.md` — API parameters, response fields, computed stats, rate limits
- `references/marketplace-codes.md` — Supported marketplaces with currencies
- `references/error-handling.md` — Error types, unauthorized quota tips, module mapping
