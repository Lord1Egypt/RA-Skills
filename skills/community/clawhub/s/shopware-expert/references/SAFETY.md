# Safety and defaults (Shopware via OpenClaw)

**Connecting:** [CONNECTING.md](CONNECTING.md). **Auth:** [AUTH.md](AUTH.md). **OpenClaw layers:** [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md).

## Destructive actions

Only after **explicit** user instruction:

- Deleting products, customers, orders, or media at scale.
- Running `bin/console` commands that **drop** or **migrate** production databases.
- Removing or disabling **payment** / **shipping** / **tax** configurations without rollback notes.
- Purging cache or reindexing **production** during peak traffic without agreement.

Prefer **staging** or a **copy** of data for experiments.

## API writes

- Use **idempotent** patterns where possible; confirm **sales channel** and **language** context before writes.
- **Read-after-write:** `GET` the entity after `POST`/`PATCH` to verify.

## Storefront / theme changes

- Do not break **checkout** or **legal** pages casually; keep reversibility (git branch, backup theme).
- Respect **cookie** / **consent** requirements for your jurisdiction (see developer docs and legal counsel).

## Injection and shell

- Never interpolate untrusted chat text into `curl` or shell without escaping/allowlisting.
- OpenClaw security overview: [Security](https://docs.openclaw.ai/gateway/security)

## Core, vendor, and third-party plugin sources

- **Never** edit **Shopware core** under `vendor/shopware/` (or other core Composer packages). Extend only via documented extension points (plugins, apps, events, config).
- **Never** edit **third-party / Store** plugin code under `custom/plugins/<VendorPlugin>` (or equivalent) as a "quick fix". Prefer upgrades, configuration, APIs, or a **first-party** plugin in your own path (often `custom/static-plugins/` - see [APPS_VS_PLUGINS_AND_PATHS.md](APPS_VS_PLUGINS_AND_PATHS.md)).
- Prefer configuration and documented APIs over editing anything under `vendor/` in general.

## Third-party extensions

- Prefer configuration and documented APIs over editing vendor code under `vendor/`.
- For commercial extensions (B2B, PaaS, etc.), read `PRODUCT_EXTENSIONS_OVERVIEW.md` and official product docs before changing behaviour.

## Communication

Report success only after **verification** (API response, page check, or test output).
