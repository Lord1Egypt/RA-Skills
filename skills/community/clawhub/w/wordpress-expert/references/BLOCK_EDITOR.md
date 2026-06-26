# Block editor (Gutenberg) for agents

WordPress 6.x uses the block editor as the primary editing surface. This doc is **agent-oriented**: how to scaffold, what files matter, and when to use OpenClaw tools vs browser.

**Deep reference:** [Block Editor Handbook](https://developer.wordpress.org/block-editor/).

## When to load

- Custom blocks, block patterns, or block themes (FSE).
- Debugging “block not in inserter” or broken `block.json` dependencies.
- Deciding static vs dynamic blocks for a feature.

## Scaffold (host or CI)

From a machine with Node/npm (often **not** the WordPress server):

```bash
npx @wordpress/create-block my-namespace-my-block --namespace my-plugin
```

Common variants: `--variant dynamic`, or interactive templates from `@wordpress/scripts`. The scaffold produces:

- `block.json` (metadata, API version)
- `src/edit.js`, `src/save.js` or `render.php` for dynamic blocks
- `package.json` with `build` / `start` via `wp-scripts`

**Agent workflow:** edit files via **workspace** or **`wordpress_plugin_files`** under the plugin slug; run `npm install` / `npm run build` where the toolchain exists (local dev or documented CI)—the skill does not assume `npm` on the production server.

## Static vs dynamic

| Type | Output | Use when |
|------|--------|----------|
| **Static** | Saved HTML in post content | Simple presentational blocks |
| **Dynamic** | PHP `render_callback` or `render.php` | Lists, user-specific data, always-fresh output |

Prefer **dynamic** when data must reflect server state at render time.

## `block.json` essentials

- `apiVersion` (2 or 3 per project)
- `name`, `title`, `category`, `icon`
- `editorScript`, `editorStyle`, `style`—ensure built asset handles exist after `npm run build`
- `supports` for spacing, colors, etc.

Missing dependencies in the generated `*.asset.php` file often cause **white screen in editor**—verify `wp-blocks`, `wp-element`, `wp-components` (etc.) are listed.

## REST vs files vs browser

- **Content CRUD** (posts with blocks): prefer **`wordpress_rest_request`** (`wp/v2/posts`, …) with block HTML in `content.raw` / `content` as appropriate.
- **Plugin/block code:** **`wordpress_plugin_files`** or workspace; then build assets.
- **Visual builder-only flows** (some patterns, template parts in Site Editor): **`browser`** if REST/file tools cannot express the change—get user approval for writes.

## Patterns and FSE

- **Block patterns:** registered in PHP or `patterns/` in themes; document in theme `theme.json` where relevant.
- **Full site editing:** templates live under `templates/`, parts under `parts/`; see [THEME_AND_TEMPLATES.md](THEME_AND_TEMPLATES.md).

## Woo / Elementor overlap

WooCommerce blocks: [WOOCOMMERCE.md](WOOCOMMERCE.md). Elementor: [ELEMENTOR.md](ELEMENTOR.md). Do not replace Elementor widgets with raw HTML shortcuts.

## Pitfalls

- Editing only `build/` outputs while ignoring `src/`—changes get overwritten on next build.
- Forgetting `filemtime()` or proper `version` on enqueued block assets—cache issues.
- Assuming `is_cart()` for block-based cart pages—see [DOMAIN.md](DOMAIN.md) Woo note.
