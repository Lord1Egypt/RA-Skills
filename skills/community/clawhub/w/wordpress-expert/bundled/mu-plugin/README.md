# OpenClaw Site Helper (must-use plugin)

PHP source for **WordPress**, not the OpenClaw gateway. Shipped with the skill; must live on the **target site** for the REST routes to exist.

**ClawHub-only skill bundle:** Often only this **README** (text)—**no** `.php` file, because ClawHub disallows non-text files in the bundle. Get **`openclaw-site-helper.php`** from the **full** git repository (`openclaw-wordpress-skill/bundled/mu-plugin/` in your project clone).

For **when** installation helps and how this differs from WP-CLI / `wordpress_plugin_files`: [references/MU_HELPER.md](../../references/MU_HELPER.md).

## Installation

1. Copy **`openclaw-site-helper.php`** to **`wp-content/mu-plugins/`** (or symlink). Create `mu-plugins/` if missing.
2. MU plugins load automatically—no activation in the Plugins screen.
3. **Requirement:** The OpenClaw gateway must have **write access** to that path **or** you copy manually (FTP, deploy, hosting panel).

## REST overview

**Namespace:** `openclaw-helper/v1` (in `wordpress_rest_request` use `path` **without** the `wp-json/` prefix, e.g. `openclaw-helper/v1/status`).

| Method | Path | Permission | Purpose |
|--------|------|------------|---------|
| GET | `openclaw-helper/v1/status` | `manage_options` | Short info: helper version, `features` list, WP/PHP version, `site_url` |
| GET | `openclaw-helper/v1/health` | `manage_options` | Runtime: memory, extensions (allowlist), cron backlog count, uploads dir writable?, locale, timezone—**no** plugin list, no paths to `wp-config` |
| GET | `openclaw-helper/v1/me/capabilities` | logged-in REST user | All **true** capabilities of the **current** user (application password); optional query `check=cap1,cap2` for yes/no map |

**Authentication:** As usual with application password / session against `WORDPRESS_SITE_URL` ([references/AUTH.md](../../references/AUTH.md)).

### Examples (`wordpress_rest_request`)

- **Status:** `method: GET`, `path: openclaw-helper/v1/status`
- **Health:** `method: GET`, `path: openclaw-helper/v1/health`
- **Capabilities:** `method: GET`, `path: openclaw-helper/v1/me/capabilities`
- **Capabilities with check:** `method: GET`, `path: openclaw-helper/v1/me/capabilities`, `query: { check: "install_plugins,edit_themes" }`

## When to install? (short)

| Scenario | Recommendation |
|----------|----------------|
| REST-only from gateway, no `exec` / WP-CLI on target | **Useful**—health/capabilities from WP’s perspective |
| Strict sandbox without shell | **Useful** for diagnostics with `wordpress_rest_request` |
| Local DDEV + `wordpress_wp_cli` / `exec` | **Optional** (convenience, one call vs several shell steps) |
| Read/write files under `wp-content/plugins/<slug>/` | **Not** via this MU plugin—use **`wordpress_plugin_files`** (with `WORDPRESS_PATH`) or deploy/workspace; see below |

## Deliberately not included

- **No** generic file read/write under `wp-content/plugins/...` via this REST API (duplicates **`wordpress_plugin_files`**, higher risk).
- **No** secrets, full plugin list, or sensitive `wp_options` dump.

## Security

Minimal, documented fields. Routes with `manage_options` only for admin-level application passwords or equivalent. `/me/capabilities` shows only the **logged-in** user’s rights—useful for least-privilege tests with **non-admin** application passwords.

If needed, remove the file or adjust `permission_callback` in a local fork (do not overwrite from skill sync blindly).

## Version

See plugin header and constant `OPENCLAW_SITE_HELPER_VERSION` in `openclaw-site-helper.php` (e.g. `0.2.0`). After updates: deploy the same file again.

## Future

Additional **read-only** routes only for clear operational gaps; see [references/MU_HELPER.md](../../references/MU_HELPER.md).
