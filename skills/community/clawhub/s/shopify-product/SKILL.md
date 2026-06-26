---
name: shopify-product
description: Search Shopify products and analyze winning items with PPSPY. Filter products by price, category, sales, and revenue, and inspect bestselling products by store.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - PPSPY_API_KEY
      bins:
        - npm
    install:
      command: npm
      args:
        - install
        - -g
        - "ppspy-mcp-server@1.0.1"
    primaryEnv: PPSPY_API_KEY
    emoji: "🔍"
    homepage: https://www.ppspy.com
    mcpServers:
      ppspy:
        command: ppspy-mcp-server
        env:
          PPSPY_API_KEY: "{{PPSPY_API_KEY}}"
---

# Shopify Product

Search Shopify products, explore winning product ideas, and inspect bestselling products by store.

Keywords: shopify product.

## Setup

1. Visit the official website at [ppspy.com](https://www.ppspy.com/) to view real-time dashboard data and product UI.
2. Visit the direct API site at [api.ppspy.com](https://api.ppspy.com/) to get your API key and manage billing/recharge.
3. Set the environment variable: `PPSPY_API_KEY`

## Available Tools (3 total)

### Shopify Product Research (3 tools)
- `ppspy_shopify_product_list` — Search and filter Shopify products by price, sales, category, revenue
- `ppspy_shopify_bestselling_product_list` — Get bestselling products for a specific store
- `ppspy_product_category_list` — Get product categories

## Usage Examples

- "Search Shopify products under $50 with high monthly sales"
- "Show bestselling products for this Shopify store"
- "Find winning Shopify products in this category"
- "List product categories before I search"

## Credits

Each API call consumes credits from your PPSPY account:
- **Shopify Product Search**: 1 credit per record
- **Supplement APIs**: Free
