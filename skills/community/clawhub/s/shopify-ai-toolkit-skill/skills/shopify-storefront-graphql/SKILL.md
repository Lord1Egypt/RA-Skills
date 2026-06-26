---
name: shopify-storefront-graphql
description: Use for custom storefronts requiring direct GraphQL queries/mutations for data fetching and cart operations. Choose this when you need full control over data fetching and rendering your own UI. NOT for Web Components - if the prompt mentions HTML tags like shopify-store, shopify-cart, use storefront-web-components instead. NOT for admin operations (use shopify-admin).
license: MIT
---

# Shopify Storefront GraphQL API Skill

Search Shopify's Storefront GraphQL API docs and validate your GraphQL before returning it.

## Required Workflow

### Step 1 — Search the docs (mandatory)
```bash
node skills/shopify-storefront-graphql/scripts/storefront_search_docs.mjs "<operation>" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

Search for the specific operation or resource (e.g., `cartCreate mutation`, `product variants query`).

### Step 2 — Write the GraphQL code
Use search results to write efficient queries/mutations. Storefront API prioritizes performance — only request fields you need.

### Step 3 — Validate before returning (mandatory)
```bash
node skills/shopify-storefront-graphql/scripts/storefront_validate.mjs \
  --code '<graphql code>' \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0 \
  --artifact-id "$(openssl rand -hex 8)" \
  --revision 1
```

### Step 4 — If validation fails
1. Read the error — identifies the exact wrong field/type
2. Search for correct values
3. Fix the error
4. Re-validate (max 3 retries)

### Step 5 — Return code only after validation passes
Wrap GraphQL in triple backticks with `graphql` language tag.

## What This Skill Does

- Searches [shopify.dev Storefront API docs](https://shopify.dev/docs/api/storefront) for Cart, Checkout, Product, and Customer operations
- Validates GraphQL against the live Storefront API schema
- Enforces performance best practices (minimal field selection for customer-facing experiences)

## Environment Variables

```bash
OPT_OUT_INSTRUMENTATION=true
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```

## Example

User asks: "Create a cart with a product variant"

**Search → Write → Validate → Return** (follow the required workflow above)
