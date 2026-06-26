---
name: shopify-admin
description: Shopify Admin API SOP — product tags, inventory, and other write operations via GraphQL/REST. Works with any Shopify store using a Custom App access token.
required_secrets:
  - SHOPIFY_ACCESS_TOKEN
  - SHOPIFY_STORE_DOMAIN
---

# Shopify Admin API SOP

## Overview

Shopify has two distinct APIs — know which one to use:

| API | Purpose | Auth |
|---|---|---|
| **Storefront API / MCP** (`/api/mcp`) | Read product catalog, cart (read-only) | None required |
| **Admin API** (GraphQL/REST) | Write products, tags, inventory, etc. | `X-Shopify-Access-Token` |

> The Storefront MCP is read-only. For any write operation, use the Admin API directly via the `http` tool.

---

## Credentials

Stored as skill secrets (injected at runtime):

- `SHOPIFY_STORE_DOMAIN` — e.g. `your-store.myshopify.com`
- `SHOPIFY_ACCESS_TOKEN` — `shpat_xxx` token from a Custom App with required scopes

---

## How to Call the Admin API

Use the `http` tool with `X-Shopify-Access-Token` header.

### GraphQL (recommended)

```
POST https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-01/graphql.json
Headers:
  Content-Type: application/json
  X-Shopify-Access-Token: {SHOPIFY_ACCESS_TOKEN}
```

### REST

```
GET/PUT https://{SHOPIFY_STORE_DOMAIN}/admin/api/2024-01/products/{id}.json
Headers:
  X-Shopify-Access-Token: {SHOPIFY_ACCESS_TOKEN}
```

---

## Common Operations

### Add / update product tags (full overwrite — include all existing tags)

```graphql
mutation {
  productUpdate(input: {
    id: "gid://shopify/Product/{PRODUCT_ID}",
    tags: ["existing-tag1", "existing-tag2", "new-tag"]
  }) {
    product { id title tags }
    userErrors { field message }
  }
}
```

⚠️ `tags` is a full replacement. Always fetch current tags first, then merge.

### Read product tags

```graphql
{ product(id: "gid://shopify/Product/{PRODUCT_ID}") { id title tags } }
```

### ID formats

- Numeric: `15501243941233`
- GraphQL GID: `gid://shopify/Product/15501243941233`

---

## Token Scopes

For full product management, the token needs:
`read_products`, `write_products`

For broader operations add:
`read_orders`, `read_inventory`, `write_inventory`, `read_themes`, `write_themes`

---

## Getting a Token (Custom App)

1. Shopify Admin → Settings → Apps → Develop apps
2. Create or open a Custom App → Configure → Admin API scopes
3. Install the app → API credentials tab → copy the `shpat_xxx` token (shown once)
4. Store it via: `PUT /skills/shopify-admin/secrets` `{"SHOPIFY_ACCESS_TOKEN": "shpat_xxx", "SHOPIFY_STORE_DOMAIN": "your-store.myshopify.com"}`

> If you use a Dev Dashboard app (Partner App), the token is obtained via OAuth.
> See the OAuth Refresh SOP below.

---

## OAuth Token Refresh SOP (Dev Dashboard apps)

When a token expires (401) or needs new scopes:

### Step 1 — Verify redirect URL is configured

In `shopify.app.toml`:
```toml
[auth]
redirect_urls = [ "https://example.com" ]
```
If empty, add it and run: `shopify app deploy --force`

### Step 2 — Open the authorization URL

```
https://{SHOPIFY_STORE_DOMAIN}/admin/oauth/authorize?client_id={CLIENT_ID}&scope={SCOPES}&redirect_uri=https://example.com&state=refresh
```

### Step 3 — Extract the code from the redirect URL

Browser redirects to `https://example.com/?code=XXXXXX&...`
Extract the `code` value (valid for ~60 seconds).

### Step 4 — Exchange code for token

```
POST https://{SHOPIFY_STORE_DOMAIN}/admin/oauth/access_token
Body: {"client_id": "{CLIENT_ID}", "client_secret": "{CLIENT_SECRET}", "code": "{code}"}
```

Response contains the new `access_token`.

---

## Gotchas

1. **`shopify app dev` triggers APP_UNINSTALLED webhook** — avoid for production stores. Use `shopify app deploy` to update config only.
2. **Existing token scopes don't auto-update** after Dev Dashboard scope changes — must re-run OAuth.
3. **Storefront MCP** (`/api/mcp`) is already configured in Kocoro for product search. Admin write ops bypass MCP entirely.
