---
name: shopify-partner
description: Use for Shopify Partner API — app management, analytics, revenue, payouts, and partner organization management. NOT for store-level Admin API (use shopify-admin). NOT for storefront (use shopify-storefront-graphql).
license: MIT
---

# Shopify Partner API Skill

Search Shopify's Partner API docs and validate GraphQL operations.

## Required Workflow

### Step 1 — Search the docs (mandatory)
```bash
node skills/shopify-partner/scripts/partners_search_docs.mjs "<operation>" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

### Step 2 — Write the GraphQL code

### Step 3 — Validate before returning (mandatory)
```bash
node skills/shopify-partner/scripts/partners_validate.mjs \
  --code '<graphql code>' \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0 \
  --artifact-id "$(openssl rand -hex 8)" \
  --revision 1
```

## What This Skill Covers

- **App management** — create, update, configure apps
- **Analytics** — app metrics, installs, uninstalls
- **Revenue & payouts** — earnings, transactions, payouts
- **Organization management** — partner orgs, members, invitations

## Environment Variables

```bash
OPT_OUT_INSTRUMENTATION=true
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```
