# Authentication and secrets (Shopify)

## Principles

- **Never** paste access tokens, client secrets, or session tokens into chat or commit them to Git.
- Store credentials in **host environment variables** or `skills.entries["shopify-expert"].env` in `openclaw.json`.

## Eligibility env

- **`SHOPIFY_SHOP_DOMAIN`** — required for skill eligibility (see `SKILL.md` metadata). Example: `your-store.myshopify.com` (no scheme, no path).

### Env name aliases (REST examples vs this skill)

| Used in [ADMIN_REST_API.md](ADMIN_REST_API.md) | Same as in this skill / [.env.example](../.env.example) |
| ---------------------------------------------- | -------------------------------------------------------- |
| `SHOPIFY_STORE_DOMAIN` | **`SHOPIFY_SHOP_DOMAIN`** |
| `SHOPIFY_ACCESS_TOKEN` | **`SHOPIFY_ADMIN_API_ACCESS_TOKEN`** (convention) |

Set whichever names your scripts use; values are the same.

## Admin API access

- Send **`X-Shopify-Access-Token`** on Admin API requests (GraphQL or REST). Token type depends on app setup (custom app token, offline/online session, etc.).
- Typical variable name (convention, not enforced by the skill): **`SHOPIFY_ADMIN_API_ACCESS_TOKEN`**.

## API version

- Include a supported **`{version}`** segment in the URL (e.g. `2025-01`). Use a variable such as **`SHOPIFY_ADMIN_API_VERSION`** in your scripts if helpful.

## Scopes

- Your app must request the correct **access scopes** for the operations you perform; errors often surface as HTTP 403 — see live **shopify.dev** scope docs.

## OAuth (apps)

- Public/custom apps use OAuth flows documented on **shopify.dev**. The bundled **`DOC_PLATFORM_AUTHENTICATION.md`** summarizes methods from the snapshot; follow current docs for implementation details.
