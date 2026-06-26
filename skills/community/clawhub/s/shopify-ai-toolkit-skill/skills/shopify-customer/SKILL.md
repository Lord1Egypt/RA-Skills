---
name: shopify-customer
description: Use for the Customer Accounts API — authentication, customer profiles, addresses, and account management. NOT for Admin API customer management (use shopify-admin). NOT for storefront cart/checkout (use shopify-storefront-graphql).
license: MIT
---

# Shopify Customer Accounts API Skill

Work with Shopify Customer Accounts — authentication, profiles, and addresses.

## What This Skill Covers

- **Customer authentication** — OAuth flows, session management
- **Customer profiles** — access and update customer data
- **Addresses** — manage customer shipping/billing addresses
- **Account management** — login, logout, password reset, registration

## Workflow

Use the `shopify-admin` skill for GraphQL operations, but first search the docs:

```bash
node skills/shopify-admin/scripts/search_docs.mjs "customerAccount mutation" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

## Environment Variables

```bash
OPT_OUT_INSTRUMENTATION=true
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```
