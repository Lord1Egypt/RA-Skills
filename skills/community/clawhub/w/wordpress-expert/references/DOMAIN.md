# WordPress domain knowledge (compact)

Compact **checklists** for WP-CLI, REST, and manual development under `wp-content`.

For **plugin architecture, security, REST routes, WPCS links, and OpenClaw workflow:** [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md).

For block editor, themes, performance: [BLOCK_EDITOR.md](BLOCK_EDITOR.md), [THEME_AND_TEMPLATES.md](THEME_AND_TEMPLATES.md), [PERFORMANCE_AND_SECURITY.md](PERFORMANCE_AND_SECURITY.md).

## Documentation

For depth: official handbooks for block editor, REST, hooks, WP-CLI; WooCommerce and Elementor docs for shop/builder topics.

## REST

- Discovery: `GET /wp-json/` or `GET /wp-json/wp/v2/` for namespaces.
- WooCommerce admin API often under namespace `wc/v3` (watch auth).

## Plugin scaffolds (manual or generated)

When creating new plugins, use:

| Type | Essentials |
|------|------------|
| **plain** | Standard plugin header, `plugins_loaded`, own prefix |
| **block** | `block.json`, editor script for inserter, complete `index.asset.php` deps (`wp-blocks`, `wp-element`, …); `render.php` with `get_block_wrapper_attributes()` |
| **custom-post-type** | Register CPT, taxonomies before CPT, rewrite, `flush_rewrite_rules` on activation, `uninstall.php` |
| **shortcode** | `shortcode_atts()`, output buffering, conditional `wp_enqueue_style` |
| **woocommerce / elementor** | `Requires Plugins` in header, dependency checks in admin |

**Optional features** when scaffolding (separate files/folders): admin settings (Settings API etc.), frontend CSS/JS (`wp_enqueue_*`), custom REST under `rest_api_init`—see playbook.

Split admin settings, REST, frontend assets into files; split files **over ~300 lines**.

## Database in custom plugins

Do not create tables only in the activation hook (race on first write). Prefer: `admin_init` + option version + `dbDelta`; `uninstall.php` with `DROP TABLE` + `delete_option`.

## CSS / frontend

- Prefer theme **CSS variables** (block theme: `--wp--preset--*`).  
- No inline CSS in frontend output; `wp_enqueue_style` + `filemtime()` for cache busting.  
- Before large style changes: inspect existing site styles (your site via REST/HTML—no credential leaks).

## Common mistakes

- Unclosed brackets, inconsistent variable names, missing edge cases (null/empty).  
- After each file change: **re-read content** before saying done.

## z-index

Moderate values (often 1–10); do not escalate unnecessarily.

## WooCommerce block cart (short)

- Block cart is not the classic shortcode: `is_cart()` can be unreliable when enqueuing—check page ID from `wc_get_page_id('cart')`.  
- Classic template hooks often do not fire on block cart—check slots/Store API/`render_block`.  
- `WC()->cart` often unavailable in custom REST callbacks—fetch data on frontend request or extend Store API.

Details: WordPress Developer Resources, WooCommerce REST docs, Elementor developer docs.
