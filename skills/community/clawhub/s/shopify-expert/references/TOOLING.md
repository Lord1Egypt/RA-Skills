# Tooling (curl, CLI)

## Minimum (skill eligibility)

- **`curl`** against `https://{SHOPIFY_SHOP_DOMAIN}/admin/api/{version}/graphql.json` with POST body and `X-Shopify-Access-Token` header for GraphQL.

### Minimal GraphQL example (pattern only)

```bash
curl -sS "https://${SHOPIFY_SHOP_DOMAIN}/admin/api/${SHOPIFY_ADMIN_API_VERSION}/graphql.json" \
  -H "Content-Type: application/json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ADMIN_API_ACCESS_TOKEN}" \
  -d '{"query":"{ shop { name } }"}'
```

Replace env names with your gateway’s actual configuration.

**REST Admin JSON** endpoints (`orders.json`, `products.json`, …): examples and pagination/rate-limit notes — [ADMIN_REST_API.md](ADMIN_REST_API.md).

## Shopify CLI

- Local app development often uses **`shopify`** CLI (`app dev`, `app deploy`, etc.). That requires the CLI installed on a machine the agent can execute — usually **optional** and **policy-gated** on the gateway. See bundled **`DOC_SHOPIFY_CLI.md`**.

## Browser / workspace

- Only if explicitly allowed by your OpenClaw **tools.allow** configuration.
