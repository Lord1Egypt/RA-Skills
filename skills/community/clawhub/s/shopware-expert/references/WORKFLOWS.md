# Workflows (OpenClaw + Shopware)

## Before you advise or change anything (checklist)

Work through this **unless** the user only wants generic Shopware theory with no instance.

1. **Shopware version** – Confirm the **exact** version (e.g. `6.7.x`): ask the user, or read from the **project** (`composer.lock` / `composer.json` for `shopware/core`, or `bin/console --version` if you may run it). If unknown, **state the assumption** and recommend verifying.
2. **Environment variables** – For API work, confirm **which** vars are configured (**not** their values): e.g. `SHOPWARE_BASE_URL` set; OAuth vars present if using Admin API (see [AUTH.md](AUTH.md)). Reply with **set/unset** or **masked** values only; **never** paste secrets into chat.
3. **Sales channel & context** – For Store API / storefront behaviour, clarify **sales channel**, **language**, and **currency** when relevant; wrong context causes confusing bugs.
4. **Edition / scope** – Note if the shop uses **commercial extensions**, **B2B**, **PaaS**, etc.; do not assume OSS-only features.
5. **Target environment** – Distinguish **staging vs production** before destructive API calls, `bin/console` writes, or bulk data changes.
6. **Verify critical facts** – For breaking changes, new endpoints, or security: follow **links in the reference file** you used, then **[developer.shopware.com](https://developer.shopware.com/)** and, if needed, **[shopware/platform](https://github.com/shopware/platform)** (ADRs, source). The bundled text may lag **6.7** patch releases.

Then proceed with **Read → Plan → Write → Verify** below.

## Read → Plan → Write → Verify

1. **Read** – Load current state: API `GET`, `bin/console` info commands, or files in a cloned project.
2. **Plan** – For multi-step or risky work, state a short plan; cite the **official doc section** you rely on.
3. **Write** – Apply the smallest change (API patch, file edit, config update).
4. **Verify** – Re-fetch the resource, run targeted tests, or check the Admin/Storefront as appropriate. Only then report **done**.

## Stale data

- Do not trust earlier chat turns for **IDs**, **versions**, or **stock**—re-query before writes.

## Complexity

- Simple reads: execute directly.
- Large refactors: checkpoint every few steps; keep the user informed.

## When to load which reference

| Task type | Start here |
| --------- | ---------- |
| Merchant “how to in Admin” | [MERCHANT_USER_DOCS.md](MERCHANT_USER_DOCS.md) |
| Admin API integration | `ADMIN_API.md`, [AUTH.md](AUTH.md) |
| Storefront / headless | `STORE_API.md`, `HEADLESS_FRONTENDS.md` |
| Plugins / apps | [APPS_VS_PLUGINS_AND_PATHS.md](APPS_VS_PLUGINS_AND_PATHS.md), `PLUGIN_SYSTEM.md`, `APP_SYSTEM.md` |
| Architecture, public API, backward compatibility, Storefront/Store API rules | [CODE_GUIDELINES_ESSENTIALS.md](CODE_GUIDELINES_ESSENTIALS.md), `TESTING_AND_QUALITY_PART2.md` (guidelines sections) |
| Storefront plugin JS, `theme:compile`, shipping `dist/` | [SHOPWARE_67_PRACTICAL_NOTES.md](SHOPWARE_67_PRACTICAL_NOTES.md) (section 13), `STOREFRONT_THEMES_TWIG.md` |
| Hosting / updates | `INSTALLATION_AND_HOSTING.md`, `RELEASE_AND_UPGRADES.md` |

## Debugging

1. Capture **HTTP status**, **response body**, and **Shopware version**.
2. Identify **sales channel** / **language** mismatches early.
3. Apply the **minimal** fix; avoid unrelated refactors.
