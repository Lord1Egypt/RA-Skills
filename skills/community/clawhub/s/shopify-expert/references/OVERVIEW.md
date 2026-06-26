# Shopify Expert – reference index

Skill id **`shopify-expert`**. Load this file first, then open the smallest reference that matches the task. Generated files are **`DOC_*.md`** (from the official LLM documentation snapshot). Regenerate with `./scripts/regenerate-shopify-skill-references.sh` (monorepo root).

## Hand-authored (OpenClaw + pointers)

| File | Content |
| ---- | ------- |
| [SOURCES_AND_VERSIONS.md](SOURCES_AND_VERSIONS.md) | Official URLs; snapshot / regeneration; attribution |
| [MERCHANT_USER_DOCS.md](MERCHANT_USER_DOCS.md) | Merchant Help Center vs developer docs |
| [CONNECTING.md](CONNECTING.md) | Gateway → Shopify HTTPS topology |
| [AUTH.md](AUTH.md) | Tokens, scopes, env vars |
| [TOOLING.md](TOOLING.md) | curl patterns, optional CLI |
| [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md) | `skills.entries`, tools |
| [SAFETY.md](SAFETY.md) | Data, rate limits, destructive ops |
| [WORKFLOWS.md](WORKFLOWS.md) | Pre-flight checklist |
| [ADMIN_REST_API.md](ADMIN_REST_API.md) | **Admin REST API** — `curl` resource reference, pagination, rate limits, REST webhooks (curated; snapshot API `2024-10` in examples). For GraphQL see [DOC_ADMIN_API.md](DOC_ADMIN_API.md). |

## Generated from Shopify LLM doc snapshot

| File | Topics (section titles preserved as H2 inside) |
| ---- | ------------------------------------------------ |
| [DOC_INTRO.md](DOC_INTRO.md) | Introduction / platform overview before first H3 |
| [DOC_APP_CONFIGURATION.md](DOC_APP_CONFIGURATION.md) | `shopify.app.toml`, app configuration |
| [DOC_ADMIN_API.md](DOC_ADMIN_API.md) | GraphQL Admin API only (not REST `*.json` routes) |
| [DOC_SHOPIFY_CLI.md](DOC_SHOPIFY_CLI.md) | Shopify CLI |
| [DOC_POLARIS.md](DOC_POLARIS.md) | Polaris Web Components + Polaris |
| [DOC_EMBEDDED_APP_BRIDGE.md](DOC_EMBEDDED_APP_BRIDGE.md) | Embedded apps, App Bridge |
| [DOC_CHECKOUT_UI_EXTENSIONS.md](DOC_CHECKOUT_UI_EXTENSIONS.md) | Checkout UI extensions |
| [DOC_ADMIN_UI_EXTENSIONS.md](DOC_ADMIN_UI_EXTENSIONS.md) | Admin UI extensions |
| [DOC_CUSTOMER_ACCOUNT_EXTENSIONS.md](DOC_CUSTOMER_ACCOUNT_EXTENSIONS.md) | Customer account extensions |
| [DOC_FUNCTIONS.md](DOC_FUNCTIONS.md) | Shopify Functions |
| [DOC_WEBHOOKS.md](DOC_WEBHOOKS.md) | Webhooks |
| [DOC_CUSTOM_DATA.md](DOC_CUSTOM_DATA.md) | Metafields, metaobjects |
| [DOC_PLATFORM_AUTHENTICATION.md](DOC_PLATFORM_AUTHENTICATION.md) | Platform auth / authorization (developer doc) |
| [DOC_DEPLOY.md](DOC_DEPLOY.md) | Hosting and deployment |
| [DOC_LIQUID.md](DOC_LIQUID.md) | Liquid |
| [DOC_THEME_APP_EXTENSIONS.md](DOC_THEME_APP_EXTENSIONS.md) | Theme app extensions |
| [DOC_HEADLESS_STOREFRONT.md](DOC_HEADLESS_STOREFRONT.md) | Hydrogen / headless storefronts |
| [DOC_POS_UI_EXTENSIONS.md](DOC_POS_UI_EXTENSIONS.md) | POS UI extensions |

**Maintainer:** taxonomy and manifests live under **`docs/openclaw-shopify/`** (not required on disk for end users who only install the packaged skill).
