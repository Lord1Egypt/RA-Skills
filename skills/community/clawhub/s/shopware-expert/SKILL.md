---
name: shopware-expert
description: "Enable Shopware 6 superpowers for OpenClaw. Get a massive boost in knowledge about everything related to Shopware 6 in general and Shopware 6 development."
metadata:
  version: "1.0.5"
  openclaw:
    skillKey: shopware-expert
    homepage: "https://developer.shopware.com/"
    requires:
      anyBins:
        - curl
      env:
        - SHOPWARE_BASE_URL
---

Instructions in this file are plain Markdown (no hidden or encoded content).

**Bundle version:** 1.0.5

# Shopware Expert: User Guide

## What This Skill Is

This skill equips your OpenClaw agent with **instructions, checklists, and bundled excerpts** from the **Shopware Developer Documentation**, oriented toward **Shopware 6.7** (the export prefers newer versioned doc paths). It supports work on **Admin API**, **Store API**, **plugins**, **apps**, **Administration UI**, **classic Storefront (Twig/themes)**, **headless/composable frontends**, **hosting**, **upgrades**, and **commercial extensions** - with an **index of ADRs** for deeper architecture topics.

**Full copy-paste 6.7 examples** (neutral `Acme` vendor, verify against official docs): `{baseDir}/references/SHOPWARE_67_EXAMPLES_PLUGIN_DAL.md`, `{baseDir}/references/SHOPWARE_67_EXAMPLES_STOREFRONT_ADMIN_CMS.md`, `{baseDir}/references/SHOPWARE_67_PRACTICAL_NOTES.md`.

**Official code guidelines (short):** `{baseDir}/references/CODE_GUIDELINES_ESSENTIALS.md` (public API, backward compatibility, Storefront / Store API conventions). Longer excerpts: `TESTING_AND_QUALITY_PART2.md` (search `resources/guidelines`).

The AI usually reaches Shopware via **HTTPS** (`curl` or similar). **Gateway tool policy** (what your OpenClaw install allows beyond `curl`) is configured in your host config, not by this skill; see `{baseDir}/references/OPENCLAW_INTEGRATION.md` and `{baseDir}/references/SAFETY.md`.

**Not exhaustive:** bundled text is **not** a complete mirror of Shopware 6.7 or every patch release. Treat it as **guidance and entry points**. For **merchant "how to in the Admin"** (click paths, day-to-day operations), the skill points to **[docs.shopware.com](https://docs.shopware.com/)** - see `{baseDir}/references/MERCHANT_USER_DOCS.md`.

## No companion plugin (v1)

Unlike **wordpress-expert**, this skill does **not** ship a dedicated OpenClaw plugin yet.

- **Minimal setup:** **`curl`** + **`SHOPWARE_BASE_URL`** only. That is enough for eligibility and for HTTP/API-style tasks when you keep other tools disabled.
- **Broader gateway capabilities:** If your host policy already allows additional tools, `{baseDir}/references/TOOLING.md` describes common Shopware dev workflows (e.g. `bin/console`). Keep allowlists **narrow**; see `{baseDir}/references/OPENCLAW_INTEGRATION.md`.
- **Benefit of a future plugin:** Typed Shopware tools would be easier to audit and allowlist than ad-hoc shell/curl. Until then, follow **narrow allowlists** and **verify** API calls against **official docs**.

## Installation Steps (Typical Flow)

On your OpenClaw gateway machine:

1. **Install the skill** (e.g. ClawHub or `skills/shopware-expert` on the gateway host).
2. **Set environment variables** - at minimum **`SHOPWARE_BASE_URL`** (host env or `skills.entries["shopware-expert"].env`). For Admin API work, add OAuth-related vars as documented in `{baseDir}/references/AUTH.md` and `.env.example`.
3. **Grant tools:** Your gateway must allow **`curl`** for HTTPS API use. Further tool access follows your **`tools.allow`** / sandbox policy - see `{baseDir}/references/OPENCLAW_INTEGRATION.md`.
4. **`openclaw gateway restart`** after plugin, allowlist, or env changes (when applicable).

Full detail: `{baseDir}/README.md`, `{baseDir}/references/CONNECTING.md`, `{baseDir}/references/AUTH.md`.

## What You Can Expect from the AI

- **API and integration tasks:** e.g. search or update entities via **Admin API** / **Store API** - the AI should use **fresh HTTP responses** and **documented** routes, not invented URLs or request bodies.
- **Extension and theme work:** expects a **project clone** on the gateway (or clear remote workflow); may use **`bin/console`**, Composer, and file edits **only** when your gateway policy permits those actions.
- **Merchant-style questions:** the AI should steer you to **user documentation** links when the task is "how to use the Admin," not code.
- **Version awareness:** the AI should **confirm the Shopware version** and **reconcile** bundled excerpts with **[developer.shopware.com](https://developer.shopware.com/)** and, when needed, **[shopware/platform](https://github.com/shopware/platform)** (including **ADRs** via `{baseDir}/references/ADR_OVERVIEW.md`).
- **Security:** use **staging**, least privilege, and explicit approval for destructive work. The AI must not echo **secrets** - only **set/unset** or **masked** env hints.

## Required Setup (Environment Variables)

**Required** for skill eligibility (see **`metadata.openclaw.requires`**):

1. **`SHOPWARE_BASE_URL`** - HTTPS base URL the gateway can reach (no trailing slash), e.g. `https://shop.example.com`.

**Common additions** for Admin API automation (optional; see **`{baseDir}/references/AUTH.md`**):

- OAuth client credentials and token URL (names may vary by your scripts), e.g. **`SHOPWARE_ADMIN_API_CLIENT_ID`**, **`SHOPWARE_ADMIN_API_CLIENT_SECRET`**, **`SHOPWARE_OAUTH_TOKEN_URL`**.

Store all secrets in **env** or **`skills.entries["shopware-expert"].env`**, never in chat or Git.

## Important Rules for People and the AI

- **No secrets in chat or Git** - see `{baseDir}/references/AUTH.md`.
- **Confirm Shopware version and context** before non-trivial advice - see `{baseDir}/references/WORKFLOWS.md` (pre-flight checklist).
- **Deeper topics** load from `{baseDir}/references/` as needed (progressive disclosure); large topics may be split across **`_PART2.md`**, **`_PART3.md`**, etc.

---

## When the agent should use this skill

Use for **Shopware-related** work: APIs, plugins, apps, Administration UI, Storefront, headless frontends, hosting, upgrades, extensions, architecture. Do **not** use for unrelated stacks unless the user asks for comparison.

Load **`{baseDir}/references/`** files when the task matches (examples: **`CONNECTING.md`**, **`AUTH.md`**, **`TOOLING.md`**, **`APPS_VS_PLUGINS_AND_PATHS.md`**, **`CODE_GUIDELINES_ESSENTIALS.md`**, **`SHOPWARE_67_EXAMPLES_PLUGIN_DAL.md`**, **`SHOPWARE_67_EXAMPLES_STOREFRONT_ADMIN_CMS.md`**, **`SHOPWARE_67_PRACTICAL_NOTES.md`**, **`ADMIN_API.md`**, **`STORE_API.md`**, **`PLUGIN_SYSTEM.md`**, **`APP_SYSTEM.md`**, **`HEADLESS_FRONTENDS.md`**, **`INSTALLATION_AND_HOSTING.md`**, **`MERCHANT_USER_DOCS.md`**, **`SOURCES_AND_VERSIONS.md`**, **`SAFETY.md`**, **`WORKFLOWS.md`**). Full index: **`{baseDir}/references/OVERVIEW.md`**.

## Rules for the assistant (summary)

1. **Version and environment first** - Before non-trivial advice or writes, establish the **target Shopware version** (ask the user, or infer from `composer.lock` / `bin/console` / project files when those files are readable on the gateway). Confirm **relevant env vars** are set **without printing secrets** - only names, set/unset, or masked placeholders (`{baseDir}/references/WORKFLOWS.md`).
2. **6.7-oriented, not complete** - Bundled excerpts favour **6.7-era** docs; they may lag **patch releases** or omit **new changelog** items. Do **not** assume full coverage.
3. **Verify via official sources** - For breaking, security-sensitive, or API-shape-critical work, follow **links in the reference files**, then **developer.shopware.com** and **shopware/platform** (ADRs) as needed; reconcile with the **user's actual version**.
4. Use **fresh data** from tools/API before writes; **do not invent** Admin API or Store API behaviour. For **apps vs plugins** and **where first-party vs third-party code lives** (`custom/static-plugins/` vs `custom/plugins/`), and rules **not to edit core or Store plugins**, read **`{baseDir}/references/APPS_VS_PLUGINS_AND_PATHS.md`** and **`{baseDir}/references/SAFETY.md`** before proposing file edits.
5. **Never** echo secrets; store credentials in host env or `openclaw.json` skill env - not chat.
6. Prefer **documented** HTTP patterns in **`{baseDir}/references/TOOLING.md`**. Do not assume tools beyond what the session policy allows.
7. For **pure merchant Admin usage** (where to click), use **`{baseDir}/references/MERCHANT_USER_DOCS.md`** and **docs.shopware.com** - not developer-only excerpts alone.
8. After **`tools.allow`**, plugin, or env changes, **`openclaw gateway restart`** is often required - see **`{baseDir}/references/CONNECTING.md`** and OpenClaw docs.

**Where work runs:** On the **OpenClaw gateway** (typically HTTP to Shopware) - not inside Shopware's PHP process unless the user's setup explicitly allows it.
