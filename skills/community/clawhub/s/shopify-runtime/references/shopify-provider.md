# Shopify Provider Notes

The current built-in provider in this standalone skill is Shopify.

## Connection Model For This Skill

This skill uses a single-store environment-driven setup instead of plugin profiles.

Expected runtime inputs:

- `storeDomain`
- `clientId`
- `apiKey`
- optional `apiVersion`

In OpenClaw terms, the recommended mapping is:

- `skills.entries."shopify-runtime".apiKey` -> `SHOPIFY_CLIENT_SECRET`
- `skills.entries."shopify-runtime".env.SHOPIFY_STORE_DOMAIN` -> store domain
- `skills.entries."shopify-runtime".env.SHOPIFY_CLIENT_ID` -> client id
- `skills.entries."shopify-runtime".env.SHOPIFY_API_VERSION` -> optional version override

Status output intentionally exposes only safe connection details. Secret values are never returned.

At runtime the skill exchanges `clientId + apiKey` for a Shopify Admin access token through Shopify's client-credentials flow, then uses that token for Admin API requests.

## Local Runtime Rules Versus Shopify Access

Two layers still matter:

1. The local runtime mode must allow it.
2. The Shopify token must have the matching Admin API scopes.

Local runtime behavior:

- `mode: "read"` blocks REST write methods and GraphQL mutations
- `mode: "write"` allows the script to attempt writes, but Shopify can still reject them

## Execution Constraints

- Use `provider.graphql(...)` for Admin GraphQL work when possible.
- `provider.graphql(...)` returns the validated GraphQL `data` object directly.
- Use `provider.request(...)` for HTTP endpoints when GraphQL is not the best fit.
- Read mode rejects write-style GraphQL mutations and non-read REST methods.

## Order Access Caveats

Shopify order access can still require extra approval beyond the basic scope pair:

- `read_all_orders` may be needed for older orders
- protected customer data access may still block order reads

GraphQL scope failures may appear as HTTP `200` responses with GraphQL errors in the response body.
