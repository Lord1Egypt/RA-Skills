---
name: shopify-library
description: Search Shopify stores and products with PPSPY. Use this skill as a general Shopify library and Shopify spy tool for store, product, theme, and category research.
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

# Shopify Library

Search Shopify stores, products, themes, and categories from one general-purpose Shopify intelligence skill.

Keywords: shopify library, shopify spy tool.

## Setup

1. Visit the official website at [ppspy.com](https://www.ppspy.com/) to view real-time dashboard data and product UI.
2. Visit the direct API site at [api.ppspy.com](https://api.ppspy.com/) to get your API key and manage billing/recharge.
3. Set the environment variable: `PPSPY_API_KEY`

## Available Tools (9 total)

### Shopify Stores (5 tools)
- `ppspy_shopify_store_list` — Search and filter Shopify stores by region, language, revenue, traffic, theme
- `ppspy_shopify_store_details` — Get detailed information for a specific Shopify store
- `ppspy_shopify_store_traffic_list` — Search Shopify stores with traffic data
- `ppspy_shopify_single_product_store_list` — Search single-product Shopify stores
- `ppspy_shopify_theme_store_list` — Search Shopify stores by theme

### Shopify Products (2 tools)
- `ppspy_shopify_product_list` — Search and filter Shopify products by price, sales, category, revenue
- `ppspy_shopify_bestselling_product_list` — Get bestselling products for a specific store

### Supplement (2 tools)
- `ppspy_product_category_list` — Get product categories
- `ppspy_shopify_theme_list` — Get Shopify themes

## Usage Examples

- "Use the Shopify spy tool to find high-revenue stores"
- "Search the Shopify library for products in the beauty category"
- "Show me bestselling products for this Shopify store"
- "Find single-product Shopify stores with strong traffic"
- "List Shopify stores using a specific theme"

## Credits

Each API call consumes credits from your PPSPY account:
- **Shopify Store/Product Search**: 1 credit per record
- **Detail/Supplement APIs**: Free
