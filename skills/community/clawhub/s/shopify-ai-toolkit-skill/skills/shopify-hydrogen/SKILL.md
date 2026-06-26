---
name: shopify-hydrogen
description: Use for Shopify Hydrogen — the React-based framework for building custom storefronts on Shopify Oxygen. Covers Hydrogen components, hooks, routes, server functions, caching, and Oxygen deployment. NOT for Liquid themes (use shopify-liquid) or Admin API (use shopify-admin).
license: MIT
---

# Shopify Hydrogen Skill

Search Hydrogen documentation and validate TypeScript/React code before returning it.

## Required Workflow

### Step 1 — Search the docs (mandatory)
```bash
node skills/shopify-hydrogen/scripts/hydrogen_search_docs.mjs "<component, hook, or concept>" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

### Step 2 — Write the code
Use search results to write correct Hydrogen components, hooks, or routes.

### Step 3 — Validate before returning (mandatory)
```bash
node skills/shopify-hydrogen/scripts/hydrogen_validate.mjs \
  --code '<typescript/react code>' \
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

## What This Skill Covers

- Hydrogen components (`useCart`, `useShop`, `CartForm`, etc.)
- Hydrogen routes and loaders
- Server functions and actions
- Oxygen deployment configuration
- Shopify Storefront API integration patterns

## Environment Variables

```bash
OPT_OUT_INSTRUMENTATION=true
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```
