---
name: wordpress-expert
description: "Enable WordPress superpowers for OpenClaw. Your Developer, Content Manager, Author, Security Specialists, Contributor, Subscriber and Admin and more."
metadata: {"version":"1.1.1","openclaw":{"skillKey":"wordpress-expert","homepage":"https://github.com/realM1lF/openclaw-wordpress-tool","requires":{"anyBins":["wp","curl"],"env":["WORDPRESS_SITE_URL","WORDPRESS_USER","WORDPRESS_APPLICATION_PASSWORD"]}}}
---

# WordPress Expert: User Guide

## What This Skill Is

This skill equips your OpenClaw agent with the necessary instructions and checklists to manage your existing WordPress website. It empowers the AI to perform tasks related to content, settings, media, plugins, themes, and extensions like WooCommerce or Elementor.

The AI typically communicates with your site via secure web interfaces (HTTPS/REST). If configured accordingly, it can also work directly via the terminal (WP-CLI) or at the file level.

## Urgent Recommendation: The Companion Plugin

For the AI to work precisely and safely, you should install the companion plugin **`wordpress-site-tools`** on the computer/server where your OpenClaw gateway runs: **[github.com/realM1lF/openclaw-wordpress-tool](https://github.com/realM1lF/openclaw-wordpress-tool)**.

- **Why?** This plugin provides typed tools (e.g. `wordpress_rest_request`, `wordpress_wp_cli`, `wordpress_connection_check`, optional media and plugin file access).
- **Benefit:** Clearer, easier to audit, and easier to allowlist than ad-hoc `exec`/`curl`. Without it, the skill still documents fallbacks—more manual and error-prone.

## Installation Steps (Typical Flow)

On your OpenClaw gateway machine:

1. **Install the skill** (e.g. ClawHub or `skills/wordpress-expert` in the workspace).
2. **Clone** the `wordpress-site-tools` repo, run **`npm install`**, then **`openclaw plugins install`** / **`enable`** (see plugin README).
3. **Grant tools:** Add WordPress tools to **`tools.allow`** in `openclaw.json`.
4. **Environment variables:** Set the three required variables below (host env or `skills.entries["wordpress-expert"].env`). Optional: **`WORDPRESS_PATH`** if you use WP-CLI or `wordpress_plugin_files`—see `{baseDir}/references/CONNECTING.md`.
5. **`openclaw gateway restart`** after plugin, allowlist, or env changes.

Full detail: `{baseDir}/README.md`, `{baseDir}/references/CONNECTING.md`, `{baseDir}/references/PRE_INSTALL_AND_TRUST.md`.

## What You Can Expect from the AI

- **Everyday tasks:** e.g. “Create a draft post” or “Upload an image” via REST—with **`wordpress-site-tools`**, prefer **`wordpress_rest_request`** and related tools.
- **Advanced tasks:** WP-CLI or plugin file edits need **`WORDPRESS_PATH`**, narrow allowlists, and explicit configuration—see `{baseDir}/references/CONNECTING.md` and `{baseDir}/references/WPCLI_PRESETS.md`.
- **Security:** The AI is not an omnipotent admin by default; use staging, least-privilege users, and approval for destructive work. The AI should use fresh tool/API data, not guesses.

## Required Setup (Environment Variables)

These three are **required** (see **`metadata.openclaw.requires`**):

1. **`WORDPRESS_SITE_URL`** — Base URL of the site (HTTPS, no trailing slash), e.g. `https://yoursite.com`.
2. **`WORDPRESS_USER`** — WordPress username for the application password.
3. **`WORDPRESS_APPLICATION_PASSWORD`** — From **Users → Profile → Application Passwords** in WordPress (not the login password). Store in env/config, never in chat or Git.

Optional: **`WORDPRESS_PATH`** — Directory on the gateway where `wp` runs, if you use WP-CLI or plugin file tools. Details: `{baseDir}/references/AUTH.md`, `{baseDir}/references/CONNECTING.md`.

## Important Rules for People and the AI

- **No secrets in chat or Git** — see `{baseDir}/references/AUTH.md`.
- **Deeper topics** load from `{baseDir}/references/` as needed (progressive disclosure).

---

## When the agent should use this skill

Use for **WordPress-related** work: content, media, plugins, themes, WooCommerce, Elementor, REST, code under `wp-content`. Do **not** use for unrelated tasks.

Load **`{baseDir}/references/`** files when the task matches (examples: **`CONNECTING.md`**, **`PLUGIN_DEV_PLAYBOOK.md`**, **`DOMAIN.md`**, **`WOOCOMMERCE.md`**, **`ELEMENTOR.md`**, **`BLOCK_EDITOR.md`**, **`THEME_AND_TEMPLATES.md`**, **`PERFORMANCE_AND_SECURITY.md`**, **`SAFETY.md`**, **`WORKFLOWS.md`**). Full index: **`{baseDir}/references/OVERVIEW.md`**.

## Rules for the assistant (summary)

1. Use **fresh data** from tools/API before writes; do not invent site state.
2. **Never** echo secrets; store credentials in host env or `openclaw.json` skill env—not chat.
3. Prefer **`wordpress_rest_request`** / **`wordpress_wp_cli`** / **`wordpress_connection_check`** (and related plugin tools) when in **`tools.allow`**; see `{baseDir}/references/NATIVE_VS_PLUGIN.md` and `{baseDir}/references/TOOLING.md`.
4. For **new site-specific plugin files**, prefer the **real** `wp-content/plugins/…` tree or **`wordpress_plugin_files`**—not the generic OpenClaw workspace by default; see `{baseDir}/references/PLUGIN_DEV_PLAYBOOK.md` (**“Where OpenClaw should write”**).
5. After plugin or **`tools.allow`** changes, **`openclaw gateway restart`** is usually required—see `{baseDir}/references/CONNECTING.md`.
6. Do not patch third-party plugins in place—addon approach in `{baseDir}/references/PLUGIN_DEV_PLAYBOOK.md` and `{baseDir}/references/USER_EXPECTATIONS.md`.

**Where work runs:** On the **OpenClaw gateway** (REST, shell, browser, workspace). Optional MU helper on the WordPress server is documented under `{baseDir}/bundled/mu-plugin/README.md` and `{baseDir}/references/MU_HELPER.md`.
