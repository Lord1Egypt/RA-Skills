# Connecting OpenClaw to Shopify

## Topology

- The **OpenClaw gateway** runs outside Shopify and reaches Shopify via **HTTPS** (e.g. `curl`) to the shop’s Admin API or Storefront API endpoints.
- There is **no** requirement to run inside Shopify infrastructure for **read-only guidance** or HTTP-based automation.

## Shop host

- Admin API (GraphQL) URL pattern: `https://{shop}/admin/api/{version}/graphql.json` where `{shop}` is typically `{name}.myshopify.com`.
- Set **`SHOPIFY_SHOP_DOMAIN`** to that host (e.g. `example.myshopify.com`) — see [AUTH.md](AUTH.md) for tokens.

## App types (high level)

- **Custom apps** in the shop admin vs **public apps** in the Partner Dashboard affect OAuth and token issuance — the hand-off details are in bundled `DOC_PLATFORM_AUTHENTICATION.md` and live **shopify.dev**.

## Verification

- After configuring env vars, use a **small** GraphQL or REST call (e.g. `shop { name }`) with correct `X-Shopify-Access-Token` — see [TOOLING.md](TOOLING.md).
