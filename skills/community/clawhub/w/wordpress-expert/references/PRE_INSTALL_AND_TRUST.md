# Before install: trust, credentials, and blast radius

Read this **before** enabling the companion OpenClaw plugin, setting WordPress credentials, or deploying optional code to a site. Skill id: **`wordpress-expert`** (ClawHub display name **WordPress Expert**).

## 1. What you are trusting

| Component | What it is | Your action |
|-----------|------------|-------------|
| **This skill** | Text instructions and references in the skill bundle | Review `SKILL.md` and `references/` if you do not trust the publisher. |
| **OpenClaw plugin `wordpress-site-tools`** | Separate Node package from **[github.com/realM1lF/openclaw-wordpress-tool](https://github.com/realM1lF/openclaw-wordpress-tool)**—registers REST/WP-CLI/file tools on the **gateway** | Read that repo’s source before `npm install` / `openclaw plugins install`. |
| **Optional MU helper** | PHP copied to the WordPress site’s `wp-content/mu-plugins/` | Source is **`openclaw-site-helper.php`** in the **full** skill git repo under `bundled/mu-plugin/`. **ClawHub text bundles often omit `.php`**—copy from a full clone or monorepo, not from a text-only upload. |

## 2. Credentials (least privilege)

- Use **WordPress Application Passwords**, not the account login password.
- Prefer a **dedicated user** with the **minimum role** needed (often not full admin on production).
- Use **staging** first; do **not** reuse production admin credentials for experiments.
- Store values in **`openclaw.json`** `skills.entries["wordpress-expert"].env` or host env—**never** in chat, Git, or the skill bundle.

## 3. Gateway and tools

- Installing/enabling the plugin and changing **`tools.allow`** / **`plugins.allow`** changes what the agent can do—**restart the gateway** after changes.
- **Restrict** optional tools (`wordpress_plugin_files`, `wordpress_media_upload`, broad WP-CLI allowlists) to environments where that risk is acceptable.
- Respect **sandbox** and **deny** rules—see [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md).

## 4. Site filesystem

- **`WORDPRESS_PATH`** and **`wordpress_plugin_files`** imply the gateway can read/write under `wp-content/plugins/<slug>/` when configured—only enable where intended.
- **Back up** the site before destructive or wide-ranging operations.

## 5. If anything above is unacceptable

You can still use **generic** OpenClaw tools (`exec`, browser, workspace) with the skill’s docs as guidance—but do **not** install the companion plugin or set WordPress env vars unless you accept the model above. See [CONNECTING.md](CONNECTING.md) **Privilege tiers** and [NATIVE_VS_PLUGIN.md](NATIVE_VS_PLUGIN.md).

## 6. ClawHub / registry notes

Registries and security scanners may flag skills that mention credentials, shell install steps, or third-party repos. This skill declares **expected** REST configuration via **`metadata.openclaw.requires.env`** in `SKILL.md` (the YAML **`description`** may be marketing-only; requirements are not duplicated there). If you believe a flag is a **false positive**, contact ClawHub maintainers with links to this file and the public plugin repo.

**VirusTotal (on ClawHub):** ClawHub may show a **VirusTotal** integration (e.g. scan status **Pending** or occasional detections). That is a **third-party** heuristic on archives or metadata—it is **not** proof of malware in this skill. The maintainer’s ClawHub package is **text-only** (Markdown and references; the packaging script strips non-text files such as `.php` from the upload bundle). The full source is in **git** for review. If a result looks wrong, use ClawHub / OpenClaw support channels; you may also use VirusTotal’s community or dispute flows where applicable—outcomes are not guaranteed.
