---
name: shopify-admin
description: Use for Admin GraphQL API — products, orders, customers, inventory, fulfillment, price rules, and all store management operations. NOT for storefront cart/checkout (use shopify-storefront-graphql). NOT for Liquid/theme code (use shopify-liquid).
license: MIT
---

# Shopify Admin API Skill

Search Shopify's Admin GraphQL API docs and validate your GraphQL before returning it.

## Required Workflow

**Every response must follow this exact sequence:**

### Step 1 — Search the docs (mandatory)
```bash
node skills/shopify-admin/scripts/search_docs.mjs "<operation>" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

Search for the **mutation or query name** (e.g., `productCreate mutation`, `inventoryAdjustQuantities mutation`).

### Step 2 — Write the GraphQL code
Use the search results to write the correct query/mutation with proper field names and arguments.

### Step 3 — Validate before returning (mandatory)
```bash
node skills/shopify-admin/scripts/validate.mjs \
  --code '<graphql code>' \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0 \
  --artifact-id "$(openssl rand -hex 8)" \
  --revision 1
```

### Step 4 — If validation fails
1. Read the error message — it names the exact wrong field/type
2. Search docs for the correct value:
   ```bash
   node skills/shopify-admin/scripts/search_docs.mjs "<correct type or field>" \
     --model "${MODEL_NAME:-openai/gpt-5.4}" \
     --client-name openclaw \
     --client-version 1.0
   ```
3. Fix the error
4. Re-validate (max 3 retries)
5. After 3 failures: return best attempt + explanation

### Step 5 — Return code only after validation passes
Always wrap GraphQL in triple backticks with `graphql` language tag.

## What This Skill Does

- Searches [shopify.dev Admin API docs](https://shopify.dev/docs/api/admin-graphql) for the right operation
- Validates GraphQL against the live Admin API schema
- Enforces best practices (field selection limits, proper input types, pagination)

## Environment Variables

```bash
# Optional: disable Shopify telemetry
OPT_OUT_INSTRUMENTATION=true

# Optional: custom Shopify dev URL
SHOPIFY_DEV_INSTRUMENTATION_URL=https://shopify.dev/
```

## Example

User asks: "Create a mutation to publish a product"

**Step 1 — Search:**
```bash
node skills/shopify-admin/scripts/search_docs.mjs "productPublish mutation" \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0
```

**Step 2 — Write:**
```graphql
mutation ProductPublish($id: ID!, $input: [PublicationInput!]!) {
  productPublish(id: $id, input: $input) {
    product {
      id
      title
      publishedAt
    }
    userErrors {
      field
      message
    }
  }
}
```

**Step 3 — Validate:**
```bash
node skills/shopify-admin/scripts/validate.mjs \
  --code 'mutation ProductPublish($id: ID!, $input: [PublicationInput!]!) { productPublish(id: $id, input: $input) { product { id title publishedAt } userErrors { field message } } }' \
  --model "${MODEL_NAME:-openai/gpt-5.4}" \
  --client-name openclaw \
  --client-version 1.0 \
  --artifact-id "abc12345" \
  --revision 1
```

**Step 4 — Return validated code**
