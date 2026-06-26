# MU helper (`openclaw-site-helper`): when to use

The **must-use plugin** in the skill under [bundled/mu-plugin/](../bundled/mu-plugin/) registers **custom** REST routes under **`openclaw-helper/v1`**. It runs **inside WordPress PHP** on the **target site**—not in the OpenClaw gateway.

**Technical reference** (routes, permissions, examples): [bundled/mu-plugin/README.md](../bundled/mu-plugin/README.md).

---

## Decision matrix

| Setup | MU helper |
|-------|-----------|
| **REST-only** (only `wordpress_rest_request`, no SSH/`exec`/`wp` on server) | **High value**—health/runtime from WordPress; capabilities for the **application-password user** |
| **Sandbox** without shell or without `wp`/`curl` in container, REST allowed | **High value**—diagnostics without WP-CLI |
| **Shared hosting**—REST with app password, no CLI | **Useful** |
| **Local DDEV** with `wordpress_wp_cli` and/or `exec` | **Optional**—much is available via `wp`/`php`; MU still saves **one** consolidated REST call (e.g. health) |
| **Plugin files** under `wp-content/plugins/<slug>/` read/write | **Not** via MU—use **`wordpress_plugin_files`** (gateway needs `WORDPRESS_PATH`) or workspace/deploy |

---

## Concrete triggers (agent)

**Use routes** when the MU plugin is **installed** on the site (otherwise 404) and at least one applies:

1. Check if the **configured application-password user** has specific rights → **`GET .../me/capabilities`** (optional `check=install_plugins,...`).
2. Need **PHP extensions / memory / cron backlog / uploads dir writable** from the **running** site → **`GET .../health`** (requires `manage_options` for that user).
3. Quick **helper version + which endpoints are active** → **`GET .../status`** (`features` array).

Always use **standard WordPress REST** (`wp/v2/...`, Woo `wc/v3/...`) **first** for content/shop—the helper is **not** a replacement.

---

## Anti-patterns

- Saying **“MU is useless”** when only **REST** is allowed—then health/capabilities may be the **only** clean path without shell.
- **Everything via WP-CLI locally**—MU is then **convenience**, not required; say so clearly.
- Inventing **file I/O** in plugin dirs via custom MU REST—use **`wordpress_plugin_files`** / WP-CLI / workspace per [NATIVE_VS_PLUGIN.md](NATIVE_VS_PLUGIN.md).

---

## Installation

Deploy [openclaw-site-helper.php](../bundled/mu-plugin/openclaw-site-helper.php) to **`wp-content/mu-plugins/`**—see [bundled/mu-plugin/README.md](../bundled/mu-plugin/README.md) and [CONNECTING.md](CONNECTING.md) §3.7.

---

## Optional (later)

OpenClaw plugin **`wordpress_connection_check`** could optionally probe `openclaw-helper/v1/status` (“helper installed?”)—not required for this skill; see repo `openclaw-wordpress-tools`.
