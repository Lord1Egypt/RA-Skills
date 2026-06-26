# Tools: decision tree

OpenClaw typically provides **`exec`** (shell), **`browser`**, and workspace file access—exact tool names depend on your gateway version ([Tools](https://docs.openclaw.ai/tools)). Plugin **`wordpress-site-tools`** may register **`wordpress_connection_check`**, **`wordpress_rest_request`**, **`wordpress_wp_cli`**, optional **`wordpress_media_upload`**, optional **`wordpress_plugin_files`** (see repo README / `openclaw-wordpress-tools`).

**Plugin vs. native:** [NATIVE_VS_PLUGIN.md](NATIVE_VS_PLUGIN.md).

## Order (default)

1. **WP-CLI**—in this order:  
   - **a)** Agent tool **`wordpress_wp_cli`** when installed, in **`tools.allow`**, and **`WORDPRESS_PATH`** (or plugin config `wordpressPath`) is set—arguments as array after `wp`; only allowed prefixes (defaults read-heavy; preset **`wpCliProfile`** or **`wpCliAllowPrefixes`**). For **DDEV:** `wpCliRunner: "ddev"` or `WORDPRESS_WP_CLI_RUNNER=ddev`, path = DDEV project root; see [DDEV.md](DDEV.md).  
   - **b)** Else **`wp`** (or e.g. **`ddev wp`**) via **`exec`** if available and you have a valid **`--path=<wp-root>`** (or `@alias`).  
   - Never `eval` / unsafe shell chains; see [SAFETY.md](SAFETY.md).

2. **WordPress REST API**—in this order:  
   - **a)** Agent tool **`wordpress_rest_request`** when installed, enabled, in **`tools.allow`**—parameters `method`, `path` (under `/wp-json`), optional `query` / `body`; auth from env/plugin config ([AUTH.md](AUTH.md)).  
   - **b)** **Media file upload:** **`wordpress_media_upload`** when allowed (local file under gateway `cwd`, see plugin README); else **`curl`** with `-F` via **`exec`**.  
   - **c)** Else **`curl`** (or equivalent) via **`exec`** when **`WORDPRESS_SITE_URL`** + valid auth are set.  
   - Good for: content CRUD, media metadata, many read-only endpoints.  
   - WooCommerce: often namespace `wc/v3` (app password or appropriate role).
   - **Optional verify:** Core **Plugins** REST (`/wp/v2/plugins`, when available for the authenticated user) follows WordPress’s documented routes and identifiers—use the [REST reference](https://developer.wordpress.org/rest-api/reference/plugins/) if you rely on it; **correct files on disk** under the site’s `wp-content` remain authoritative.

2b. **OpenClaw MU helper REST** (`openclaw-helper/v1/...`)—**only** if the MU plugin is on the **WordPress site** ([bundled/mu-plugin/README.md](../bundled/mu-plugin/README.md)) and you need it (REST-only, sandbox without shell, app-password user capabilities, consolidated health). **Always first** use normal WP core/plugin REST (`wp/v2`, Woo, …) for domain tasks; not for plugin file I/O—see [MU_HELPER.md](MU_HELPER.md).

3. **Browser**, only when CLI/REST are not enough (e.g. Customizer-only flow, plugin with no API).  
   - More fragile and slower; only with clear user approval for writes.

## Operator limits (often not or only partly automatable)

Without extra in-WP helpers (e.g. custom MU plugin), many tasks are **not** cleanly solvable via REST or conservative WP-CLI:

| Area | Typical issue | Recommended path |
|------|---------------|------------------|
| **Customizer** | No stable REST replacement | **Browser** with user approval or manual |
| **Nav menus** | REST/CLI gaps depending on setup | WP-CLI only if in **allowlist preset**; else browser/admin |
| **Some page builders** | Data in builder format, not classic posts | Builder docs, **browser**, or **small custom plugin** |
| **Admin-only plugins** | No public API | Browser or manual |
| **Complex Woo setup** | Partly admin-only | Prefer REST `wc/v3`; else [WOOCOMMERCE.md](WOOCOMMERCE.md) |

Do **not** let users believe “everything” works via chat—name gaps clearly. Post-install verification: [CONNECTING.md](CONNECTING.md).

## Scope

The agent works on the **host** with shell, HTTP (plugin tool or shell), and optionally browser—not as embedded PHP inside WordPress.

## Sandbox (OpenClaw)

In a **sandboxed** session (e.g. Docker), `wp` or `curl` are often missing in the container (host PATH does not apply automatically), and the container does **not** inherit `skills.entries.*.env` from the host. OpenClaw also applies **separate** sandbox tool allowlists (`tools.sandbox.tools.allow` / `deny`)—global `tools.allow` alone is not always enough for plugin tools like `wordpress_rest_request`. Diagnose: `openclaw sandbox explain` (official docs). **Details, links, WordPress checklist:** [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md).
