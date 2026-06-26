---
name: shopify-functions
description: Use for Shopify Functions — cart validators, discounts (percentage, fixed amount, buy X get Y), delivery customizers, and fulfillment constraints. NOT for Liquid themes (use shopify-liquid) or GraphQL API calls (use shopify-admin).
license: MIT
---

# Shopify Functions Skill

Search Shopify Functions documentation and validate your function code before returning it.

## Required Workflow

### Step 1 — Search the docs (mandatory)
```bash
node skills/shopify-functions/scripts/functions_search_docs.mjs "<function type or API>" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

Examples: `cart_checkout_validation`, `discount type:Percentage`, `delivery_customization`.

### Step 2 — Write the function code
Use search results to write correct Shopify Functions in your chosen language (TypeScript, Rust, etc.).

### Step 3 — Validate before returning (mandatory)
```bash
node skills/shopify-functions/scripts/functions_validate.mjs \
  --code '<graphql or function code>' \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0 \
  --artifact-id "$(openssl rand -hex 8)" \
  --revision 1
```

### Step 4 — If validation fails
1. Read the error
2. Search for correct values
3. Fix the error
4. Re-validate (max 3 retries)

### Step 5 — Return code only after validation passes

## Function Types

| Function Type | Description |
|--------------|-------------|
| `cart_checkout_validation` | Validate cart before checkout |
| `cart_transform` | Modify cart at checkout |
| `delivery_customization` | Customize delivery options |
| `discount` | Percentage, fixed amount, buy X get Y |
| `fulfillment_constraints` | Control where orders can be fulfilled |

## Environment Variables

```bash
OPT_OUT_INSTRUMENTATION=true
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```
