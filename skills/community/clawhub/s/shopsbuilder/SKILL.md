---
name: shopsbuilder
description: Launch and run online stores through the ShopsBuilder MCP.
version: 1.23.0
metadata:
  openclaw:
    homepage: https://shopsbuilder.app/en/docs/connect-ai-agent/
    emoji: 🧺
---

# ShopsBuilder

ShopsBuilder lets you create an online store and manage it for the merchant: products, prices,
stock, shipping, orders, sales and payments. You work through the ShopsBuilder MCP server
(`https://mcp.shopsbuilder.app/mcp`). The merchant signs in with OAuth, and you only reach the
stores they own or are an admin of.

## One-time setup

Add the server with the ShopsBuilder client document, then sign in on the machine that runs
OpenClaw:

```bash
openclaw mcp set shopsbuilder '{"url":"https://mcp.shopsbuilder.app/mcp","transport":"streamable-http","auth":"oauth","oauth":{"clientMetadataUrl":"https://mcp.shopsbuilder.app/oauth/openclaw-client-metadata.json"}}'
openclaw mcp login shopsbuilder
openclaw mcp doctor shopsbuilder --probe
```

The merchant signs in (or creates an account) in the browser. Never ask for passwords, API keys,
secret keys or wallet details in chat, and don't add authorization headers.

## Pick a store

1. Call `list_stores`.
2. No stores: collect the store name, the owner's email, the currency and the countries it sells
   to. The currency can't change once the store has prices, so confirm it. Call `create_store`
   with `confirmed=false`, show the preview, and call it again with `confirmed=true` only after
   the merchant agrees.
3. One store: it is selected. Several: ask which one, then call `select_store`.
4. `current_store` shows the selection. If a tool says provisioning isn't ready, tell the merchant
   and retry the same tool shortly.

## Add and publish a product

Run these one at a time, in order, and follow each result's `nextStep`:

`create_product` → `update_product_category` → `create_product_variant` →
`publish_product_to_channel` → `set_variant_price` → `set_variant_stock` →
`add_product_image_from_url`

- A product needs a category before it is published.
- Descriptions are Editor.js JSON serialized as a string.
- Before creating variants, call `get_product_variant_options`. If a dimension such as size is
  missing, confirm it with the merchant, then call `create_variant_dimension`.

## Check sales

Call `sales_summary` with `days=7` (or `30`). It compares with the previous period and lists top
products. Use `orders` only to look at individual orders.

## Restock

Call `restock_assessment`. Explain the evidence it used and never invent a forecast. Propose
`set_variant_stock` changes and apply them only after the merchant approves.

## Payments

When the merchant asks how shoppers pay, call `payment_methods` and share each `connectUrl`. The
merchant connects card or crypto payments in the browser.

## Confirm writes

- Confirm consequential changes (prices, stock, publishing, new stores) before you make them.
- Delete tools return a preview and a `confirmation_token`. Show the preview and pass the token
  back only after the merchant explicitly confirms.
- If no tool does what the merchant asks, say so plainly, don't pretend it was done, and call
  `report_missing_capability` with a one-sentence summary.
