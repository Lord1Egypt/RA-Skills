# Themes, templates, and FSE

**Agent goal:** pick the **right file** to edit (classic theme vs block theme) and avoid breaking the template hierarchy.

**Handbooks:** [Theme Handbook](https://developer.wordpress.org/themes/), [Block themes](https://developer.wordpress.org/themes/block-themes/).

## When to load

- Changing how archives, singles, or the homepage render.
- Child themes vs parent edits.
- Full Site Editing (`theme.json`, templates, template parts).

## Classic template hierarchy (summary)

WordPress picks the **most specific** template it finds, then falls back:

- **Single post:** `single-{post-type}-{slug}.php` then `single-{post-type}.php` then `single.php` then `singular.php` then `index.php`
- **Page:** custom template then `page-{slug}.php` then `page-{id}.php` then `page.php` then `singular.php` then `index.php`
- **Archive:** `archive-{post-type}.php` then `archive.php` then `index.php`
- **Home:** `front-page.php` / `home.php` vs `index.php` depending on Reading settings

If the wrong template wins, check **parent vs child** load order and filename typos.

## Block themes (FSE)

- **`theme.json`:** global styles, settings, layout. Validate JSON.
- **`templates/`:** HTML templates (block markup).
- **`parts/`:** header/footer and reusable parts.
- **Patterns:** may live under `patterns/` with metadata headers.

Changes often need **no PHP** for layout. Prefer `theme.json` plus templates. Use **workspace** or allowed deploy paths under the **active theme directory** (child theme preferred).

## Decision table: where to edit

| Goal | Prefer |
|------|--------|
| One-off layout for a **classic** theme | Child theme copy of the specific template file |
| Global colors/fonts in **block** theme | `theme.json` |
| Homepage structure in **block** theme | `templates/front-page.html` or `home.html` as appropriate |
| Add hooks without touching templates | Small **custom plugin** ([PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md)) |
| WooCommerce cart/checkout look | Woo template overrides in child theme or documented hooks ([WOOCOMMERCE.md](WOOCOMMERCE.md)) |

## Child themes

- **Prefer child theme** for third-party parent updates.
- `style.css` must declare `Template:` parent slug.
- `functions.php` for enqueue and `add_action` only. Avoid duplicating entire parent trees unless necessary.

## OpenClaw tools

- **`wordpress_plugin_files`** is for **plugins** under `wp-content/plugins/<slug>/` only. Theme files on the server often need **workspace** deploy or `exec`/SFTP your environment allows.
- **REST:** read posts/pages; not a substitute for editing PHP/HTML theme files on disk.
- **Browser:** Customizer or Site Editor when file access is missing. User approval for writes.

## Pitfalls

- Editing the **parent** theme directly (lost on update).
- Wrong template for CPT: check `single-{post_type}.php`.
- Mixing classic PHP templates with FSE expectations without knowing which is active.
