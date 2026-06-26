---
name: shopify-expert
description: "Enable Shopify superpowers for OpenClaw. Get a massive boost in knowledge about everything related to Shopify in general and Shopify development."
metadata:
  version: "1.1.0"
  openclaw:
    skillKey: shopify-expert
    homepage: "https://shopify.dev/"
    requires:
      anyBins:
        - curl
      env:
        - SHOPIFY_SHOP_DOMAIN
---

Instructions in this file are plain Markdown (no hidden or encoded content).

**Bundle version:** 1.1.0

# Shopify Expert: User Guide

## What this skill is

This skill gives your OpenClaw agent **structured guidance** and **bundled excerpts** from **Shopify official LLM documentation snapshot** (regenerated into `references/DOC_*.md`), plus a hand-curated **Admin REST API** reference (`references/ADMIN_REST_API.md`). It covers **apps**, **GraphQL Admin API**, **REST Admin JSON endpoints**, **CLI**, **Polaris**, **checkout / admin / customer account / POS extensions**, **Functions**, **webhooks**, **metafields**, **Liquid**, **themes**, **Hydrogen / headless**, and **deployment** — at a **point in time**; always **verify** against live **[shopify.dev](https://shopify.dev/)** for your API version.

**Not exhaustive:** the bundle is **not** a full mirror of Shopify docs or every changelog. Treat it as **entry points + checklists**.

**Intended role:** **Knowledge and routing** — orient the agent, pick the smallest relevant `references/` file, and use bundled text as a **starting point**. This skill is **not** a complete offline substitute for **[shopify.dev](https://shopify.dev/)**; when payloads, fields, or versioning must be exact, use **live** developer docs (or web tools your gateway allows).

The AI usually talks to Shopify over **HTTPS** (`curl` or similar). Broader gateway tools follow your host policy; see `{baseDir}/references/OPENCLAW_INTEGRATION.md` and `{baseDir}/references/SAFETY.md`.

## No companion plugin (v1)

There is **no** OpenClaw plugin in v1 — only this skill and optional **`curl`**. Prefer **documented** Admin **GraphQL** (`DOC_ADMIN_API.md`), **REST** (`ADMIN_REST_API.md`), and CLI patterns; see `{baseDir}/references/TOOLING.md` and `{baseDir}/references/AUTH.md`.

## Installation (typical)

1. Install the skill (ClawHub or `skills/shopify-expert` on the gateway host).
2. Set **`SHOPIFY_SHOP_DOMAIN`** (e.g. `your-store.myshopify.com` — see `{baseDir}/references/AUTH.md`).
3. Allow **`curl`** (and other tools only if your policy permits).
4. Restart the gateway after skill or env changes if needed.

Details: `{baseDir}/README.md`, `{baseDir}/references/CONNECTING.md`, `{baseDir}/references/AUTH.md`.

## What you can expect from the AI

- Use **live [shopify.dev](https://shopify.dev/)** when API shape, versions, or compliance matter.
- **Confirm** the shop context, API version, and **access scopes** before writes.
- **No secrets in chat** — env and secret stores only; see `{baseDir}/references/AUTH.md`.

## Required setup (eligibility)

Per **`metadata.openclaw.requires`**:

1. **`SHOPIFY_SHOP_DOMAIN`** — Admin / API host suffix, e.g. `example.myshopify.com` (no `https://`, no trailing path).

Optional for real API calls: access token and API version — see `{baseDir}/references/AUTH.md`.

## When the agent should use this skill

Use for **Shopify** development: apps, extensions, Storefront API, Liquid/themes, Hydrogen, webhooks, Functions, metafields, deployment.

Load `{baseDir}/references/OVERVIEW.md` first, then the smallest matching `DOC_*.md`, **`ADMIN_REST_API.md`** (REST), or other hand-authored file.

## Rules for the assistant (summary)

1. **Version and context first** — shop domain, API version, app type (public/custom), and scopes.
2. Prefer **official** GraphQL Admin API, **REST Admin API** where applicable, and CLI docs over guessing payloads.
3. **Never** echo tokens; reference env **names** only.
4. After tool or env changes, gateway restart may be required.

**Where work runs:** on the **OpenClaw gateway** (HTTP to Shopify), not inside Shopify’s runtime unless the user’s setup allows it.
