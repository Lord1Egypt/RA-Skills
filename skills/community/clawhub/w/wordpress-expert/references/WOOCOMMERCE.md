# WooCommerce

Notes for OpenClaw with **REST**, **WP-CLI**, or **browser**—without dedicated in-WordPress agent tools. For **Elementor**, see [ELEMENTOR.md](ELEMENTOR.md).

## Guidelines

- Block-based cart/checkout behavior: see also [DOMAIN.md](DOMAIN.md) (block cart note) and [BLOCK_EDITOR.md](BLOCK_EDITOR.md) when touching Woo blocks.
- Product/order/coupon logic via **WooCommerce APIs** (REST `wc/v3` where possible) instead of ad-hoc PHP in third-party plugins.
- **OpenClaw:** prefer `wordpress_rest_request` with path under `wc/v3/...`; WP-CLI only with appropriate **`wpCliProfile`** ([WPCLI_PRESETS.md](WPCLI_PRESETS.md)). Do not run arbitrary PHP on the server instead of shop CRUD.
- **Variable products (order):** Create product (`variable`) → set attributes → create variations → verify with GET/list (REST or allowed WP-CLI).
- **Custom Woo-related plugin:** In plugin header `Requires Plugins: woocommerce`; admin notice if Woo is missing. **HPOS:** declare compatibility with custom order tables per [Woo docs](https://woocommerce.com/document/high-performance-order-storage/) when touching order plugins.
- No "shortcut" hacks that bypass shop data—CRUD through the official layer.

If REST is not enough: targeted **admin UI** (browser) or a **small custom plugin**—do not edit third-party plugin files. Scaffold hints: [PLUGIN_DEV_PLAYBOOK.md](PLUGIN_DEV_PLAYBOOK.md).

## Limits

No specialized **in-WordPress** helpers (e.g. dedicated admin tools) here. Decide per [TOOLING.md](TOOLING.md) whether REST, WP-CLI, browser, or a **small custom plugin** on the site is needed.

Future improvement: dedicated OpenClaw tools (track progress in maintainer source repo).
