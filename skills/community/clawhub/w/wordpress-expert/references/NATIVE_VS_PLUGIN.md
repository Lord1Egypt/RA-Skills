# OpenClaw native vs. plugin `wordpress-site-tools`

Skill **`wordpress-expert`** must **not** build a parallel OpenClaw. Prefer WordPress-specific, policy-aware steps via the plugin; everything else via **built-in** OpenClaw tools (names depend on gateway version—see [OpenClaw Tools](https://docs.openclaw.ai/tools)).

## Quick overview

| Task | Preferred | Fallback |
|------|-----------|----------|
| Read/write WP data (REST) | **`wordpress_rest_request`** | Shell **`exec`** + `curl` (quoting/escaping, [SAFETY.md](SAFETY.md)) |
| WP-CLI with allowlist/profile | **`wordpress_wp_cli`** + `wpCliProfile` or `wpCliAllowPrefixes` | **`exec`** + `wp` ([SAFETY.md](SAFETY.md), [WPCLI_PRESETS.md](WPCLI_PRESETS.md)) |
| First contact / connectivity | **`wordpress_connection_check`** | Manual [CONNECTING.md](CONNECTING.md) |
| Media upload (multipart) | **`wordpress_media_upload`** (if allowed) | `curl` with `-F` / browser |
| Files under `wp-content/plugins/<slug>/` (list/read/write, limited) | **`wordpress_plugin_files`** (if allowed, `WORDPRESS_PATH` set) | Workspace file access / `exec` |
| **Inside-WP diagnostics** (extensions, cron backlog, REST user caps, health) | **`wordpress_rest_request`** to `openclaw-helper/v1/*` **if** MU helper is installed on site | WP-CLI/`exec` on gateway (if allowed)—see [MU_HELPER.md](MU_HELPER.md) |
| Composer, npm, git, Docker, systemd | **`exec`** | — |
| UI without API (Customizer, some plugins) | **`browser`** (only with clear user approval for writes) | — |
| Drafts / templates / no path to the site’s `wp-content` | Workspace **read** / **write** / **edit** | Site tree via **`wordpress_plugin_files`** or an explicit host path ([PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md)) |

## Notes

- **Plugin tools** need `tools.allow` (or plugin bundle name)—see [CONNECTING.md](CONNECTING.md). In **sandboxed** setups the global allowlist alone is often insufficient; sandbox policy and `group:openclaw`—see [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md).
- **Secrets** never in chat or Git; [AUTH.md](AUTH.md).
- **Browser** is slower and more fragile than REST/WP-CLI—only when necessary.

See also [TOOLING.md](TOOLING.md) (decision tree).
