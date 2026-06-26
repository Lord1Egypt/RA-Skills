---
name: trueprofit
description: >
  TrueProfit profit analytics expert. Use this skill whenever working with TrueProfit MCP tools
  to analyze store performance, query profit data, orders, products, ad costs, or customer metrics.
  Trigger automatically when the user asks about profit, ROAS, COGS, net margin, orders, revenue,
  ad spend, shipping costs, or any e-commerce analytics question involving their TrueProfit store.
  Also use when the user connects a new MCP server at mcp.trueprofit.io.
---

# TrueProfit MCP — Usage Guide

TrueProfit is a profit analytics platform for e-commerce merchants (Shopify, etc.). This skill
teaches you how to use TrueProfit MCP tools effectively to answer business analytics questions.

## Key Business Concepts

### Profit Metrics
- **Revenue**: Gross sales before any deductions
- **Net Revenue**: Revenue after refunds and discounts
- **COGS (Cost of Goods Sold)**: Product cost per unit — must be set manually or imported
- **Gross Profit** = Net Revenue − COGS
- **Net Profit** = Gross Profit − Ad Costs − Shipping − Transaction Fees − Custom Costs − Taxes
- **Net Margin** = Net Profit / Net Revenue × 100%
- **Contribution Margin** = Revenue − Variable Costs (excludes fixed overhead)

### Advertising Metrics
- **Ad Spend**: Total spend across all connected platforms (Facebook, Google, TikTok, etc.)
- **ROAS** = Revenue / Ad Spend (per channel)
- **Blended ROAS** = Total Revenue / Total Ad Spend (all channels combined)
- **MER (Marketing Efficiency Ratio)** = Revenue / Total Marketing Cost

### Key Ratios
- **AOV (Average Order Value)** = Revenue / Number of Orders
- **Refund Rate** = Refunded Amount / Gross Revenue × 100%
- **CAC (Customer Acquisition Cost)** = Total Ad Spend / New Customers
- **LTV (Lifetime Value)** = AOV × Purchase Frequency × Customer Lifespan
- **Break-even ROAS** = 1 / (1 − COGS%) where COGS% = COGS / Revenue

## Workflow Patterns

### Step 1: Always establish shop context

Most tools require a `shop_id`. Start every session with:
```
list_shops → identify the right shop → use shop_id for all subsequent calls
```

Single-shop users: `list_shops` returns one item — use its `shop_id` directly.
Multi-shop / agency users: confirm with the user which shop before proceeding, or loop across all shops.

### Step 2: Use the correct date range format

All dates use `YYYY-MM-DD` format in the shop's local timezone.

| User says | date_from | date_to |
|-----------|-----------|---------|
| "today" | today | today |
| "this month" | first day of current month | today |
| "last month" | first day of previous month | last day of previous month |
| "last 30 days" | today − 30 | today |
| "last 7 days" | today − 7 | today |
| "yesterday" | yesterday | yesterday |
| "Q1 2025" | 2025-01-01 | 2025-03-31 |

Check the shop's timezone via `get_shop_details` if date precision matters.

### Step 3: Pick the right tool

| User question | Tool |
|---------------|------|
| "What's my profit this month?" | `get_profit_summary` |
| "Show daily profit trend / chart" | `get_profit_by_date` |
| "Which products make the most profit?" | `get_profit_by_product` |
| "Show my recent orders" | `list_orders` |
| "Find order #1234 / search orders" | `list_orders` with `search` param |
| "Details on a specific order" | `get_order_insights` |
| "Orders summary / total count" | `get_orders_summary` |
| "How much did I spend on ads?" | `get_ad_costs` |
| "ROAS by UTM / campaign / source" | `get_revenue_by_utm` |
| "What custom costs do I have?" | `get_custom_costs` |
| "Show my products and COGS" | `list_products` |
| "Details on a specific product" | `get_product` |
| "Update COGS for a product" | `update_product_cogs` |
| "Customer retention / total customers" | `get_customer_overview` |
| "Details on a specific customer" | `get_customer_details` |
| "Shipping cost for specific orders" | `get_shipping_cost` |
| "Which ad platforms are connected?" | `get_connected_platforms` |
| "What shop am I looking at?" | `get_shop_details` |

## Important Tool Parameters

These non-obvious parameters unlock significant functionality:

**`list_orders`**
- `financial_status`: filter by `paid`, `pending`, `refunded`, `partially_refunded`, `authorized`, `partially_paid`, `unpaid`, `voided` (comma-separated for multiple)
- `search`: find orders by name or number (e.g., `"#1234"`)
- `order_by`: sort by `created_at`, `total_price`, or `profit`
- `page` / `page_size`: paginate large result sets (default page_size=20)

**`list_products`**
- `search`: filter by product title
- `page` / `page_size`: paginate large catalogs

**`update_product_cogs`**
- `variant_id`: omit or set to `0` to update **all variants** of a product at once
- `zone_name`: pricing zone, defaults to `"global"` — leave empty unless the shop uses regional COGS zones
- Changes take effect retroactively across all historical orders for that product

**`get_shipping_cost`**
- Requires specific **order IDs** (not a date range) — get them from `list_orders` first
- Max 100 order IDs per request

**`get_customer_details`**
- Requires a Shopify **customer ID** (numeric) — not name or email
- Get customer IDs from order data in `list_orders` or `get_order_insights`

## Common Workflows

### "How was my performance last month?"
1. `list_shops` → get `shop_id`
2. `get_profit_summary` with last month's date range
3. `get_ad_costs` for ad spend breakdown by platform
4. Present as: Revenue, Net Profit, Net Margin %, ROAS, AOV — with period-over-period change if available

### "Which products should I focus on?"
1. `get_profit_by_product` for a meaningful date range (e.g., last 30 days)
2. Sort by **net profit** (not revenue) — high-revenue products can have negative profit
3. Flag products with COGS = 0 — profit data is unreliable until COGS is set
4. Recommend: double down on high-margin, investigate high-volume low-margin

### "Find a specific order"
1. `list_orders` with `search="#1234"` (order name/number) and a date range
2. Or filter by `financial_status="refunded"` to find refunded orders
3. Then `get_order_insights` with the order ID for full line-item breakdown

### "Why did my profit drop this week?"
1. `get_profit_by_date` → find which specific day(s) caused the drop
2. `get_ad_costs` → check for ad spend spike or platform attribution issues
3. `list_orders` with `financial_status="refunded"` → look for refund spike
4. `get_connected_platforms` → verify all ad platforms still connected

### "Set up COGS for my products"
1. `list_products` → identify products with COGS = 0 or null
2. Ask user to confirm cost per product/variant
3. `update_product_cogs` — use `variant_id=0` to update all variants at once if cost is the same
4. `get_product` → verify the update was applied
5. Note: this retroactively recalculates profit for all past orders

### "Show shipping costs for my orders"
1. `list_orders` → get order IDs for the date range (up to 100 at a time)
2. Extract the order IDs
3. `get_shipping_cost` with the order ID list

### "Compare my shops" (multi-shop / agency)
1. `list_shops` → get all shop IDs
2. For each shop: `get_profit_summary` with same date range
3. Build comparison: Revenue, Net Profit, Net Margin, ROAS per shop
4. Note: currencies may differ — confirm before converting

### "How many customers do I have?"
- `get_customer_overview` → total customers, new customers (no date range needed — shop-level metric)
- For individual customer history: need their Shopify customer ID from order data

## Presenting Results to Users

When sharing analytics data, lead with the most actionable insight:

- **Profit summary**: Revenue → Net Profit → Net Margin % → ROAS → AOV (in that order)
- **Product analysis**: present as a ranked table with Revenue, Profit, Margin columns
- **Date trends**: describe the trend direction first, then call out notable peaks/drops
- **Ad costs**: show spend by platform + total ROAS, flag platforms with low ROAS
- **COGS gaps**: prominently warn if products have COGS = 0 before showing profit numbers

## Formulas Reference

```
Net Profit = Revenue - COGS - Ad Spend - Shipping - Transaction Fees - Refunds - Custom Costs
ROAS = Ad Revenue / Ad Spend
Blended ROAS = Total Revenue / Total Ad Spend
Net Margin % = (Net Profit / Revenue) × 100
AOV = Revenue / Number of Orders
CAC = Total Ad Spend / New Customers
LTV = AOV × Purchase Frequency × Customer Lifespan
Refund Rate = Refunded Amount / Gross Revenue × 100
Break-even ROAS = 1 / (1 - COGS%) where COGS% = COGS / Revenue
```

## Tips & Gotchas

1. **COGS = 0 means unreliable profit**: If any products lack COGS, net profit is overstated for
   those products. Always warn the user before presenting profit data.

2. **Ad platform reporting lag**: Facebook, Google, and TikTok can have 1–3 day attribution delay.
   For very recent dates, ad costs may appear lower than actual spend.

3. **Currency per shop**: Each shop reports in its own currency. Never mix currencies across shops
   without explicit user confirmation and conversion.

4. **UTM data is incomplete by nature**: `get_revenue_by_utm` only captures orders where UTM
   parameters were tracked. Direct/organic traffic won't appear — always note this caveat.

5. **`get_customer_overview` has no date range**: It returns shop-level lifetime totals, not
   a filtered period. Don't pass date params to this tool.

6. **`get_shipping_cost` needs order IDs, not dates**: First use `list_orders` to get IDs,
   then pass them to `get_shipping_cost` (max 100 per call).

7. **COGS updates are retroactive**: Updating COGS via `update_product_cogs` recalculates profit
   for all historical orders — confirm with the user before bulk updates.

8. **Auth is automatic**: This MCP uses Account-level OAuth. The server automatically exchanges
   it for a Shop token when needed — don't try to manage tokens manually.

9. **Refunds inflate cost ratios**: A refund spike makes ad spend look higher as % of revenue.
   Check `list_orders` with `financial_status="refunded"` to assess refund impact.

## Connected Ad Platforms

Check which platforms are active via `get_connected_platforms`:

| Platform | Notes |
|----------|-------|
| Facebook Ads | Most common, 1-3 day attribution delay |
| Google Ads | Includes Shopping, Search, YouTube |
| TikTok Ads | |
| Snapchat Ads | |
| Pinterest Ads | |

Disconnected platforms = spend tracked as custom costs, or not tracked at all.

## Keeping the Skill Up to Date

TrueProfit MCP is actively developed — new tools and workflows are added regularly. To get the
latest version of this skill, call the `get_skill` tool from the TrueProfit MCP server:

```
get_skill → copy the returned SKILL.md content → overwrite ~/.claude/skills/trueprofit/SKILL.md
```

Do this periodically (e.g., once a month) or whenever you notice a tool behaving differently
than documented here.

## MCP Server Info

- **Server URL**: https://mcp.trueprofit.io/mcp
- **Auth**: OAuth 2.0 — sign in with your TrueProfit Account at app.trueprofit.io
- **Tools**: 20 tools covering profit, orders, products, ads, customers, shipping
- **Download skill**: https://mcp.trueprofit.io/skill
