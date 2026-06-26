# Workflows and pre-flight

Before non-trivial Shopify work, confirm:

1. **Shop domain** — `SHOPIFY_SHOP_DOMAIN` correct for the target store.
2. **API version** — stable, supported version for your integration.
3. **Token and scopes** — token valid; scopes cover planned queries/mutations.
4. **Environment** — custom app vs production app; **do not** mix credentials.
5. **Official check** — cross-check critical behaviour on [shopify.dev](https://shopify.dev/).

**Read → plan → execute → verify** with a small dry-run query when possible.
