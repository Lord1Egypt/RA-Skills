---
name: shopify-custom-data
description: Use for metafields, custom data, and attributes on products, collections, orders, customers, and other Shopify resources. Covers metafield definitions, types, visibility, and Storefront rendering.
license: MIT
---

# Shopify Custom Data Skill

Work with metafields and custom data on Shopify resources.

## What This Skill Covers

- **Metafield definitions** — create and configure metafield schemas
- **Metafield types** — string, integer, JSON, file reference, date, boolean, etc.
- **Storefront rendering** — access metafields via Liquid, Storefront API, or Hydrogen
- **Validation** — ensure metafield data meets schema requirements

## Workflow

When working with metafields, use `shopify-admin` or `shopify-storefront-graphql` for the actual GraphQL queries, but first search the docs:

```bash
node skills/shopify-admin/scripts/search_docs.mjs "metafield definition" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

## Environment Variables

```bash
OPT_OUT_INSTRUMENTATION=true
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```
