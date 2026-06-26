# Connect WordPress to OpenClaw (existing installation)

Guide for **existing** WordPress sites: no extra WordPress plugin from this repo is required. Connect via **HTTPS + application password** (REST) and optionally **WP-CLI** on the same machine as the **OpenClaw gateway**.

OpenClaw: [Skills](https://docs.openclaw.ai/tools/skills), [Skills config](https://docs.openclaw.ai/tools/skills-config), [Building Plugins](https://docs.openclaw.ai/plugins/building-plugins), [Agent Tools](https://docs.openclaw.ai/plugins/agent-tools).

### Privilege tiers (least access first)

| Tier | Goal | Typical setup |
|------|------|----------------|
| **0 – Guidance** | Explain WordPress without touching a site | No companion plugin; stock `SKILL.md` still expects REST env for **eligibility**—use a local metadata fork if you need tier 0 only. |
| **1 – REST** | Content/API via HTTPS | `WORDPRESS_SITE_URL`, `WORDPRESS_USER`, `WORDPRESS_APPLICATION_PASSWORD`; optional plugin tools for REST / connection check. |
| **2 – Host + site FS** | WP-CLI, plugin file I/O, MU helper | Tier 1 plus `WORDPRESS_PATH`, narrow `wordpress_wp_cli` / `wordpress_plugin_files` in `tools.allow`; MU PHP from full repo if needed. |

See [PRE_INSTALL_AND_TRUST.md](PRE_INSTALL_AND_TRUST.md) and [SAFETY.md](SAFETY.md).

---

## 1. Two valid topologies

| Topology | When | `WORDPRESS_SITE_URL` + app password | `WORDPRESS_PATH` / WP-CLI tool |
|----------|------|--------------------------------------|--------------------------------|
| **A – REST only (remote)** | Shared hosting, gateway elsewhere, no FS access to WP | **Yes** | **No** (tool `wordpress_wp_cli` unused or empty) |
| **B – REST + WP-CLI** | Gateway on host **with** same filesystem as WP (or mount) | **Yes** | **Yes** – directory where `wp core version` runs |

`WORDPRESS_PATH` is the **cwd** for `wp` on the **gateway host**, not a URL. Without server access: **REST** only.

**DDEV (local):** REST at `https://<project>.ddev.site`; for WP-CLI in the plugin use `wpCliRunner: "ddev"` and `WORDPRESS_PATH` = DDEV **project root** (with `.ddev/`). Details: [DDEV.md](DDEV.md).

---

## 2. WordPress site (one-time)

1. **HTTPS**
2. User with appropriate role
3. **Application password:** Users → Profile → Application Passwords → create and store securely (not the login password)
4. **Test REST:** browser `https://your-domain.tld/wp-json/` (subdirectory: `https://domain.tld/blog/wp-json/`)
5. Check security/firewall plugins if REST is blocked

`WORDPRESS_SITE_URL` = public base URL **without** trailing slash.

---

## 3. OpenClaw gateway

**Before plugin install or secrets:** [PRE_INSTALL_AND_TRUST.md](PRE_INSTALL_AND_TRUST.md).

**Important for tools:** Plugin tools and changes to `tools.allow` / `plugins.allow` are registered in the **gateway process**. After such changes: **`openclaw gateway restart`**. A **new chat (`/new`)** is **not** a substitute; use `/new` only if after restart the **UI** still shows a stale tool list.

### 3.1 Skill

```bash
cp -r /path/to/openclaw-wordpress-skill ~/.openclaw/workspace/skills/wordpress-expert
```

Then **`openclaw gateway restart`**, then check: `openclaw skills list --eligible`. Optional new chat if the UI does not show the skill.

**Skill from ClawHub:** If you installed the skill via the ClawHub CLI, the bundle contains **only** instructions and `bundled/`—**not** the OpenClaw plugin. Install plugin **`wordpress-site-tools`** separately—public repo: **[github.com/realM1lF/openclaw-wordpress-tool](https://github.com/realM1lF/openclaw-wordpress-tool)** (or local path / monorepo clone; see skill README).

### 3.2 Plugin

**Option A – clone plugin only (recommended with ClawHub skill):**

```bash
git clone https://github.com/realM1lF/openclaw-wordpress-tool.git
cd openclaw-wordpress-tool && npm install
openclaw plugins install -l "$(pwd)"
openclaw plugins enable wordpress-site-tools
openclaw gateway restart
```

**Option B – monorepo** `personal-ki-agents`, folder `openclaw-wordpress-tools/`:

```bash
cd /path/to/openclaw-wordpress-tools && npm install
openclaw plugins install /path/to/openclaw-wordpress-tools
openclaw plugins enable wordpress-site-tools
openclaw gateway restart
```

### 3.3 Plugin ID and `plugins.allow`

- **Manifest ID** (in `openclaw.plugin.json`): **`wordpress-site-tools`**. Under `plugins.entries` the key must be **exactly** `plugins.entries.wordpress-site-tools`—do not guess from npm package or folder name.
- OpenClaw may **warn** if **`plugins.allow`** is empty while plugins load from workspace/path. Optional entry:

```json5
plugins: {
  allow: ["wordpress-site-tools"],
```

**Note:** If `plugins.allow` is **non-empty**, depending on OpenClaw version typically only **listed** plugin IDs are active/allowed—add other plugins to the same list.

### 3.4 Allow agent tools (`tools.allow`)

WordPress tools are **optional** and need a **tool allowlist** ([Agent Tools](https://docs.openclaw.ai/plugins/agent-tools)):

```json5
{
  tools: {
    allow: [
      "wordpress_connection_check",
      "wordpress_rest_request",
      "wordpress_wp_cli",
      "wordpress_media_upload",
      "wordpress_plugin_files",
    ],
  },
}
```

Shorthand: `tools.allow: ["wordpress-site-tools"]` (all tools from this plugin).

### 3.5 `openclaw.json` example (skill + plugin + secrets)

```json5
{
  skills: {
    entries: {
      "wordpress-expert": {
        enabled: true,
        env: {
          WORDPRESS_SITE_URL: "https://your-site.tld",
          WORDPRESS_USER: "wp_user",
          WORDPRESS_APPLICATION_PASSWORD: "xxxx xxxx xxxx xxxx xxxx xxxx",
        },
      },
    },
  },
  plugins: {
    allow: ["wordpress-site-tools"],
    entries: {
      "wordpress-site-tools": {
        enabled: true,
        config: {},
      },
    },
  },
  tools: {
    allow: [
      "wordpress_connection_check",
      "wordpress_rest_request",
      "wordpress_wp_cli",
      "wordpress_media_upload",
      "wordpress_plugin_files",
    ],
  },
}
```

Add `WORDPRESS_PATH`, `wordpressPath`, `wpCliRunner`, `wpCliAllowPrefixes` in `env` / config as needed (see DDEV.md, WPCLI_PRESETS.md).

### 3.6 OpenClaw: policy, sandbox, groups, providers

Global **`tools.allow`/`tools.deny`** (deny wins), **`group:openclaw`** without plugin tools, **sandbox** allowlists (`tools.sandbox.tools.*`), **`tools.byProvider`**, env **host vs. container**: see **[OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md)**.

**Sandbox:** See **[OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md)** and [Skills config](https://docs.openclaw.ai/tools/skills-config).

### 3.7 Optional MU plugin (bundled in skill)

The skill includes **`bundled/mu-plugin/openclaw-site-helper.php`** (see [bundled/mu-plugin/README.md](../bundled/mu-plugin/README.md)). This is **WordPress PHP**—not OpenClaw gateway code.

- **Deploy:** copy to **`wp-content/mu-plugins/`**.
- **Routes** (via `wordpress_rest_request`, path without `wp-json/`): `GET openclaw-helper/v1/status`, `/health` (`manage_options`), `/me/capabilities` (logged in; optional `check=`).
- Not a replacement for **`wordpress_plugin_files`**—see **[MU_HELPER.md](MU_HELPER.md)**.

### 3.8 Optional tool: `wordpress_plugin_files`

With **`WORDPRESS_PATH`** / `wordpressPath` on the gateway host: list/read/write only under `wp-content/plugins/<pluginSlug>/`. After plugin update: **`openclaw gateway restart`**. Sandbox: see [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md).

---

## 4. Verification

If **`wordpress_connection_check`** is in `tools.allow`, run it first (anonymous `wp-json/`, authenticated `users/me`, optional WP-CLI version). No secrets in output.

Manual:

```bash
curl -sS -u "USER:APP_PASSWORD" "https://your-site.tld/wp-json/wp/v2/posts?per_page=1"
```

Topology B: `cd /path/to/wp && wp core version`.

---

## 5. Value: plugin vs. skill only

| | Skill only + exec/curl | With wordpress-site-tools |
|--|------------------------|---------------------------|
| REST | shell strings, quoting risk | `wordpress_rest_request` |
| WP-CLI | free-form `wp` | `wordpress_wp_cli`, allowlist + blocklist |
| Diagnostics | manual | `wordpress_connection_check` |

---

## 6. Operational profiles

`tools.allow` / `tools.deny` (deny wins), sandbox per [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md). See [SAFETY.md](SAFETY.md), [WPCLI_PRESETS.md](WPCLI_PRESETS.md) for `wpCliProfile` presets (`read-only`, `content-staging`, `staging-admin`, `dev-local`).

---

## 7. Links

- [AUTH.md](AUTH.md)
- [WPCLI_PRESETS.md](WPCLI_PRESETS.md)
- [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md)
- [Plugin README](../../openclaw-wordpress-tools/README.md)
