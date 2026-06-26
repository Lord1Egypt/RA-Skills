# Elementor

Notes for OpenClaw with **REST**, **WP-CLI**, or **browser**—without dedicated in-WordPress agent tools. For **WooCommerce**, see [WOOCOMMERCE.md](WOOCOMMERCE.md).

## Guidelines

- Theme/layout integration: [THEME_AND_TEMPLATES.md](THEME_AND_TEMPLATES.md) for child themes and template overrides.
- **Custom Elementor-related plugin:** `Requires Plugins: elementor` in header; minimum version e.g. with `defined('ELEMENTOR_VERSION')` and `version_compare`; admin notice if Elementor is missing.
- **Existing** Elementor pages: understand structure, then change deliberately (editor, exports, or site-specific APIs—depending on access).
- **No professional design from scratch:** Point users to template kits / designers; you adjust content/structure.
- Use real **Elementor widgets**, not raw HTML in the text widget as a widget substitute.
- Before layout changes: read current structure/page layout (stale-data protection).
- Prefer new Elementor pages as **drafts**.
- Container model (nested containers) instead of legacy section/column where applicable.
- On tool/API errors: **no** silent HTML fallback—report errors.
- **Check frontend:** After visible changes load the affected URL (browser or allowed HTTP)—not only “code written”.

## Limits

No specialized **in-WordPress** helpers (e.g. dedicated admin tools) here. Decide per [TOOLING.md](TOOLING.md) whether REST, WP-CLI, browser, or a **small custom plugin** on the site is needed.

Future improvement: dedicated OpenClaw tools (track progress in maintainer source repo).
