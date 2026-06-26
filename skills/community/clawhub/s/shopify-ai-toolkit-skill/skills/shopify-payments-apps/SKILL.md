---
name: shopify-payments-apps
description: Use for Shopify Payments Apps API — managing payment integrations, disputes, transactions, and payouts. NOT for storefront checkout (use shopify-storefront-graphql). NOT for Admin orders (use shopify-admin).
license: MIT
---

# Shopify Payments Apps Skill

Search Shopify's Payments Apps API docs and validate GraphQL operations.

## Required Workflow

### Step 1 — Search the docs (mandatory)
```bash
node skills/shopify-payments-apps/scripts/payments_search_docs.mjs "<operation>" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

### Step 2 — Write the GraphQL code

### Step 3 — Validate before returning (mandatory)
```bash
node skills/shopify-payments-apps/scripts/payments_validate.mjs \
  --code '<graphql code>' \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0 \
  --artifact-id "$(openssl rand -hex 8)" \
  --revision 1
```

## What This Skill Covers

- **Payment management** — payment sessions, capture, void, refund
- **Disputes** — chargebacks, dispute responses, evidence
- **Transactions** — transaction history, payouts
- **Balance** — balance inquiries, currency conversion

## Environment Variables

```bash
OPT_OUT_INSTRUMENTATION=true
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```
