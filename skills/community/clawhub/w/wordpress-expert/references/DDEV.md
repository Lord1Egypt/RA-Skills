# Local WordPress with DDEV + OpenClaw

DDEV runs WordPress in containers. The **OpenClaw gateway** runs on your **host** (Linux/macOS/WSL). This skill/plugin is designed for that.

**Layout:** The WordPress tree may sit under a **docroot subdirectory** (common: `web/`) while **`WORDPRESS_PATH`** is the **project root** (with `.ddev/`). Plugin files must live under the **`wp-content/plugins/…`** that **that** installation actually uses—confirm if unsure ([PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md)).

## REST (no special case)

- **URL:** `https://<projectname>.ddev.site` (no trailing slash) → `WORDPRESS_SITE_URL`
- **Auth:** application password on the WordPress user as usual ([AUTH.md](AUTH.md))
- **Tools:** `wordpress_rest_request`, `wordpress_connection_check`, `wordpress_media_upload` use `fetch` on the host. If the browser opens the DDEV URL without certificate warnings, Node/OpenClaw usually works too. On TLS errors: DDEV/mkcert docs (trust CA on host) or `NODE_EXTRA_CA_CERTS`—project-specific.

## WP-CLI via plugin (`wordpress_wp_cli`)

On the host there is often **no** direct `wp` on PATH; use **`ddev wp`** from the **DDEV project root** (folder with `.ddev/`).

In the plugin:

- **`WORDPRESS_PATH`** (or `wordpressPath` in config) = **absolute path to that project root**, not necessarily `web/`.
- **`wpCliRunner`:** `ddev` in `plugins.entries.wordpress-site-tools.config`, **or** environment:

```bash
export WORDPRESS_WP_CLI_RUNNER=ddev
```

`WORDPRESS_WP_CLI_RUNNER` **overrides** config when set to `wp` or `ddev`.

- **`ddev`** must be installed on the **same machine as the OpenClaw gateway** and on PATH.

Implementation: the plugin runs `spawn("ddev", ["wp", ...args], { cwd: WORDPRESS_PATH })`—same allowlist/blocklist as direct `wp`.

## Connection check

`wordpress_connection_check` uses the **same** runner logic for the “WP-CLI core version” step.

## Quick standard setup

1. DDEV project running (`ddev start`).
2. `WORDPRESS_SITE_URL=https://your-project.ddev.site`
3. `WORDPRESS_PATH=/absolute/path/to/ddev-project-root`
4. `WORDPRESS_WP_CLI_RUNNER=ddev` **or** `wpCliRunner: "ddev"` in plugin config
5. Restart gateway after config changes.

See also [CONNECTING.md](CONNECTING.md), [TOOLING.md](TOOLING.md).
