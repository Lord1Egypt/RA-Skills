---
name: shopify-polaris-extensions
description: Use for Polaris React UI components in Shopify app extensions — app home cards, checkout UI extensions, customer account sections, and POS UI extensions. Polaris is Shopify's design system. NOT for Liquid themes (use shopify-liquid). NOT for Admin API (use shopify-admin).
license: MIT
---

# Shopify Polaris Extensions Skill

Build admin UI extensions with Shopify Polaris React components.

## What This Skill Covers

- **App home cards** — dashboard cards for Shopify admin home
- **Checkout UI extensions** — add custom content to checkout
- **Customer account sections** — extend customer account pages
- **POS UI extensions** — add custom UI to Shopify POS
- **Polaris components** — Button, Card, Page, IndexTable, etc.

## Workflow

Use `shopify-admin` for the underlying API calls. When building UI:

1. Search docs for the right Polaris component pattern:
   ```bash
   node skills/shopify-admin/scripts/search_docs.mjs "polaris app home extension" \
     --model "${MODEL_NAME:-openai/gpt-5.4}" \
     --client-name openclaw \
     --client-version 1.0
   ```

2. Write React/TypeScript code using Polaris components

## Polaris Extension Types

| Extension Type | Use for |
|--------------|---------|
| `polaris-app-home` | Admin dashboard cards |
| `polaris-checkout-extensions` | Checkout custom UI |
| `polaris-customer-account-extensions` | Customer account pages |
| `polaris-app-extensions` | General admin UI |

## Environment Variables

```bash
OPT_OUT_INSTRUMENTATION=true
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```
