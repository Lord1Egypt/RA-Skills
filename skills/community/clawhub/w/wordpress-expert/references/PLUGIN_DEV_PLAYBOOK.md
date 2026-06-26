# Plugin development under OpenClaw (playbook)

Curated guardrails for **your own** plugins and **addon** plugins (do not patch third-party code). **Depth** comes from the [WordPress Developer Handbook](https://developer.wordpress.org/) and [Coding Standards](https://developer.wordpress.org/coding-standards/)—here: order, security, and OpenClaw-specific workflow.

**When to load:** Tasks with **PHP/JS under `wp-content/plugins/`** or **custom REST routes**—together with `{baseDir}/references/DOMAIN.md`, `{baseDir}/references/WORKFLOWS.md`, and for blocks/themes/perf: [BLOCK_EDITOR.md](BLOCK_EDITOR.md), [THEME_AND_TEMPLATES.md](THEME_AND_TEMPLATES.md), [PERFORMANCE_AND_SECURITY.md](PERFORMANCE_AND_SECURITY.md).

## Where OpenClaw should write new plugin code

OpenClaw’s **workspace** is the agent’s general file area ([Tools](https://docs.openclaw.ai/tools))—**not** the implied install location for “a plugin for **my** WordPress site.”

**Default order for site-specific plugins:**

1. **`wordpress_plugin_files`** when allowed and it maps to that site’s `wp-content/plugins/<slug>/` ([CONNECTING.md](CONNECTING.md) §3.8, [NATIVE_VS_PLUGIN.md](NATIVE_VS_PLUGIN.md)).
2. Otherwise a **host path** the user stated or that matches the same WordPress tree as **`WORDPRESS_PATH`** / the running site—if ambiguous, verify with WP-CLI, a directory check, or ask.
3. **Workspace** for drafts, reusable templates, or when **no** filesystem path to the target site exists.

## OpenClaw vs. in-WordPress agent

`wordpress-site-tools` does **not** offer `patch_plugin_file` or a dedicated grep tool. Workflow:

- **Read:** Workspace files or `wordpress_wp_cli` / `exec` only within allowlist; optionally `wordpress_rest_request` for site data.
- **Write:** Prefer the **site plugin directory** (section above) or **`wordpress_plugin_files`**; else workspace or another path the user approves. **Always read the full file** before large overwrites (do not replace whole files blindly without read).
- **Verify:** Read-after-write, `wordpress_connection_check` for config topics, PHP log only if access is allowed and safe.

**Forbidden as strategy:** Running arbitrary PHP on the server just to change Woo/content—use **REST** (`wc/v3`, …) or **WP-CLI** with an appropriate `wpCliProfile` ([WPCLI_PRESETS.md](WPCLI_PRESETS.md)).

## MUST / MUST NOT (development)

Aligned with [SAFETY.md](SAFETY.md)—WordPress-specific habits:

**MUST**

- Follow [WordPress Coding Standards](https://developer.wordpress.org/coding-standards/).
- Use nonces for admin forms and AJAX where applicable.
- Sanitize input; escape output (`esc_html`, `esc_url`, `esc_attr`, `wp_kses_post` as appropriate).
- Use prepared statements for `$wpdb`; no string-concat SQL with untrusted input.
- Use capability checks (`current_user_can`) in admin code.
- Enqueue scripts/styles with `wp_enqueue_*` and proper dependencies.
- Prefer hooks over editing WordPress core or vendor plugin files.
- Use a text domain for translatable strings.

**MUST NOT**

- Modify WordPress core.
- Trust user input without sanitization or output without escaping.
- Hardcode `$wpdb` table names without `$wpdb->prefix` for custom tables.
- Register write-capable REST routes with `permission_callback` that always returns true without a clear model.
- Patch third-party plugin files in place—use addons and hooks ([USER_EXPECTATIONS.md](USER_EXPECTATIONS.md) §2.1).

## Architecture: extension points (hooks)

- **Actions** (`do_action`): events; callbacks are not expected to return values to core.
- **Filters** (`apply_filters`): transform values; always **return** the (possibly modified) value.
- **Priority:** default `10`; same priority = registration order.
- **Bootstrap:** Own plugin: main file with plugin header, `ABSPATH` check, then typically `plugins_loaded` or earlier only if needed (constants).
- **Admin:** `admin_menu`, `admin_init` for settings; always check **capabilities** (`current_user_can`).

**Useful hook order (mental model, not exhaustive):** `muplugins_loaded` → `plugins_loaded` → `init` → `wp_loaded` → `admin_init` / `rest_api_init` → `wp_enqueue_scripts` → `template_redirect` → `wp` → `shutdown`. Register where your code’s dependencies exist—see [Plugin API / Hooks](https://developer.wordpress.org/plugins/hooks/), [add_action](https://developer.wordpress.org/reference/functions/add_action/), [add_filter](https://developer.wordpress.org/reference/functions/add_filter/).

## Suggested plugin layout (orientation)

Not mandatory—adapt to project size. Split files over ~**300 lines** for reviewability.

**Minimal**

- `my-plugin.php` (header, bootstrap, hooks)
- `uninstall.php` if you persist options/tables
- `includes/` for classes if logic grows

**Layered (larger plugins)**

- Main plugin file + `includes/` (loader, services), `admin/` (settings UI), `public/` (frontend), `languages/`, optional `tests/`.
- Keep REST registration in a dedicated include loaded on `rest_api_init`.

Use **`wordpress_plugin_files`** (with `WORDPRESS_PATH`) or workspace sync to edit these paths—no path traversal.

## Custom REST API

- `register_rest_route` with namespace and route; **always** `permission_callback` (never `__return_true` for sensitive writes without a design).
- Validate arguments (`validate_callback`); escape output per context.
- See [REST API Handbook](https://developer.wordpress.org/rest-api/).

## Security and data

- **Nonces** for admin forms and AJAX; **capabilities** not only “is logged in”.
- **Sanitize** input, **escape** output.
- **Prepared statements** for `$wpdb`.
- **Prefix** options, meta keys, function names to avoid collisions.

## Lifecycle and structure

- **Activation/deactivation:** `register_activation_hook` / `register_deactivation_hook`; for CPT **rewrite:** `flush_rewrite_rules` on activation/deactivation ([DOMAIN.md](DOMAIN.md)).
- **uninstall.php:** cleanup for real tables/options; do not ship an empty stub only.
- **i18n:** text domain, `load_plugin_textdomain`; keep strings translatable—[Internationalization](https://developer.wordpress.org/plugins/internationalization/).

## Scaffold checklist

Addition to the table in [DOMAIN.md](DOMAIN.md):

| Feature idea | Typical building blocks |
|--------------|-------------------------|
| Admin settings | Settings API or options page, capability, nonce |
| Frontend CSS/JS | `wp_enqueue_style` / `wp_enqueue_script`, `filemtime` for version |
| REST endpoints | separate file, `rest_api_init`, `permission_callback` |
| Woo-related | `Requires Plugins: woocommerce`, dependency check, HPOS declaration where needed ([WOOCOMMERCE.md](WOOCOMMERCE.md)) |
| Elementor-related | `Requires Plugins: elementor`, version check ([ELEMENTOR.md](ELEMENTOR.md)) |

## Quality (on the user’s machine)

- **WPCS / PHPCS:** set up as dev dependency; the skill **does not** run PHPCS.
- **POT:** `wp i18n make-pot` (WP-CLI if allowed by preset).
- **Tests:** PHPUnit optional; for changes: read-after-write ([WORKFLOWS.md](WORKFLOWS.md)) and project manual tests (maintainer docs in source repo).

## Extending third-party plugins

- **Addon plugin** using documented hooks/filters of the target plugin; **no** permanent edits to vendor files.
- See [USER_EXPECTATIONS.md](USER_EXPECTATIONS.md) §2.1.

## Typical PHP pitfalls

| Pitfall | Hint |
|---------|------|
| `the_content()` inside `the_content` filter | Possible infinite loop—use `$content` parameter |
| `is_cart()` on block cart | May be false—check page ID with Woo helpers |
| Guessing meta keys | Copy from code that stores the value |
| `wp_redirect()` after output | Headers already sent—redirect early + `exit` |
| Block frontends | Much UI is client-side—not only PHP templates |

## Canonical links

- [Plugin Handbook](https://developer.wordpress.org/plugins/)
- [REST API Handbook](https://developer.wordpress.org/rest-api/)
- [Coding Standards](https://developer.wordpress.org/coding-standards/)
- [Security](https://developer.wordpress.org/apis/security/)

**Optional MU helper on the site:** Source in skill under `bundled/mu-plugin/`—deploy to `wp-content/mu-plugins/`. For **operations and diagnostics** (REST `openclaw-helper/v1/status`, `/health`, `/me/capabilities`)—**not** for generating/deploying plugin code from chat; development stays workspace/WP-CLI/file tools. When useful: [MU_HELPER.md](MU_HELPER.md); routes: [bundled/mu-plugin/README.md](../bundled/mu-plugin/README.md).
