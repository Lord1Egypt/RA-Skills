---
name: "shopify-runtime"
description: "Use when the user wants direct Shopify runtime access through one configured store: inspect setup status, search Shopify docs, or execute JavaScript against the configured store."
# prettier-ignore
metadata: {"openclaw":{"requires":{"env":["SHOPIFY_STORE_DOMAIN","SHOPIFY_CLIENT_ID","SHOPIFY_CLIENT_SECRET"]},"primaryEnv":"SHOPIFY_CLIENT_SECRET"}}
---

# Seller Runtime Toolkit

Use this skill when you need direct, scriptable access to one Shopify store from OpenClaw.

This skill complements `seller-api-workflow`. Keep the existing workflow skill for higher-level business asks. Use this skill when the task is explicitly about Shopify setup status, documentation search, script execution, or troubleshooting those surfaces.

This skill is self-contained. You can copy the entire `shopify-runtime/` folder into an OpenClaw `workspace/skills/` directory and run it there without the `seller-assistant` plugin repository beside it.

## Quick Start

- Configure the skill in OpenClaw instead of maintaining per-store profiles.
- Set this skill's `apiKey` in OpenClaw. Because the skill declares `primaryEnv: "SHOPIFY_CLIENT_SECRET"`, OpenClaw injects that value into `SHOPIFY_CLIENT_SECRET` for each agent run.
- Set `skills.entries."shopify-runtime".env.SHOPIFY_STORE_DOMAIN` to your `*.myshopify.com` domain.
- Set `skills.entries."shopify-runtime".env.SHOPIFY_CLIENT_ID` to your Shopify app client id.
- Optionally set `skills.entries."shopify-runtime".env.SHOPIFY_API_VERSION` to override the default API version.
- Run the bundled script with `node`.
- Read [references/shopify-provider.md](references/shopify-provider.md) when the request touches auth, scopes, orders, or write access.
- Read [references/runtime-contract.md](references/runtime-contract.md) when you need the output shape or command examples.

Example OpenClaw config:

```json5
{
  skills: {
    entries: {
      "shopify-runtime": {
        apiKey: { source: "env", provider: "default", id: "SHOPIFY_CLIENT_SECRET" },
        env: {
          SHOPIFY_STORE_DOMAIN: "your-store.myshopify.com",
          SHOPIFY_CLIENT_ID: "your_shopify_client_id",
          SHOPIFY_API_VERSION: "2026-01",
        },
      },
    },
  },
}
```

## Auth And Scope Notes

- This skill currently authenticates with Shopify by exchanging `SHOPIFY_CLIENT_ID + SHOPIFY_CLIENT_SECRET` for an Admin API access token. It does not use a pre-issued `SHOPIFY_ACCESS_TOKEN`.
- This flow is intended for a Shopify app owned by the same organization as the target store and installed on that same store.
- Read operations usually need matching Shopify Admin API scopes such as `read_products`, `read_inventory`, `read_orders`, or `read_customers`.
- Write operations usually need the matching write scopes such as `write_products`, `write_inventory`, or `write_orders`.
- Order access can still fail even with basic scopes. Older orders may require `read_all_orders`, and protected customer data access may still be required.

## Capability Boundaries

- Prefer Admin GraphQL for normal reads and writes. Use REST only when GraphQL is not the best fit.
- `--mode read` blocks local REST writes and GraphQL mutations before the request is sent.
- `--mode write` only removes the local read-only guard. Shopify still enforces the app's granted scopes.
- `status` confirms local skill readiness, not that Shopify token exchange will succeed.

## Commands

### Inspect current setup

Use this when the user asks whether the skill is ready, which store it is pointed at, or which API version it will use.

```bash
node skills/shopify-runtime/scripts/seller-runtime.mjs status
```

### Search provider and official docs

Use this before writing an API script from memory. Prefer provider notes and the narrowest matching official documentation entry.

```bash
node skills/shopify-runtime/scripts/seller-runtime.mjs search --query "orders graphql pagination"
```

Add `--limit` or `--refresh` when needed.

### Execute JavaScript

Use this after you know the request shape. Default to `--mode read`. Only use `--mode write` when the user clearly asked for a write operation and the Shopify token should allow it.

```bash
cat <<'EOF' | node skills/shopify-runtime/scripts/seller-runtime.mjs execute --mode read
return await provider.graphql(`
  query {
    shop {
      name
    }
  }
`)
EOF
```

The script body should use `provider.graphql(...)` or `provider.request(...)`. In this runtime, `provider.graphql(...)` returns the validated GraphQL `data` object directly. Prefer piping the script on `stdin` so you do not need temporary files. `--script-file` is still supported when a real file is more convenient.

## Working Rules

- This skill targets one configured Shopify store per agent run.
- Search docs before inventing request shapes or filters from memory.
- Keep execution scripts narrow and return concise structured objects instead of raw payloads when possible.
- Treat `requestSummary`, `rawResponses`, and `logs` as execution evidence when you explain the outcome.
- Read mode blocks REST write methods and GraphQL mutations locally. Write mode still depends on the Shopify token having matching Admin API access.
- The runtime reads `SHOPIFY_STORE_DOMAIN`, `SHOPIFY_CLIENT_ID`, `SHOPIFY_CLIENT_SECRET`, and optional `SHOPIFY_API_VERSION` from the environment that OpenClaw injects for the skill run.
