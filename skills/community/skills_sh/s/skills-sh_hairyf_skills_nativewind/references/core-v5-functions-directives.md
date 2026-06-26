---
name: core-v5-functions-directives
description: NativeWind v5 CSS directives (@import, @theme, @utility, @source), CSS functions (var, calc, env, color-mix), and RN-specific functions
---

# v5 Functions & Directives

NativeWind v5 uses Tailwind CSS v4's CSS-first configuration. Directives live in your global CSS; CSS and React Native-specific functions are available in styles and theme.

## Usage

**Tailwind v4 directives:**

| Directive | Purpose |
|-----------|---------|
| `@import` | Import Tailwind layers and other CSS files |
| `@theme` | Define design tokens (colors, spacing, fonts) |
| `@utility` | Define custom utilities |
| `@custom-variant` | Define custom variants |
| `@source` | Specify content sources for class detection |
| `@plugin` | Load a Tailwind plugin |
| `@apply` | Inline utility classes inside custom CSS |

Example setup:

```css
@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/preflight.css" layer(base);
@import "tailwindcss/utilities.css";
@import "nativewind/theme";
```

`nativewind/theme` adds RN-specific theme (elevation, platform fonts, safe area) and variants `ios:`, `android:`, `native:`, `web:`, `tv:`.

**CSS functions (polyfilled on native by react-native-css):**

- **var()** — Use CSS custom properties; set in CSS or via `vars()` from JS.
- **calc()** — Arithmetic; supported for px, %, rem, em, and CSS variables. Do not mix unit types in one expression (e.g. `calc(100% - 20px)` not supported on native).
- **env()** — `env(safe-area-inset-top)`, `env(safe-area-inset-bottom)`, etc.
- **color-mix()** — e.g. `color-mix(in oklch, red 50%, blue)`.

**React Native–specific CSS functions** (use in CSS / `@theme`):

- `hairlineWidth()` — Thinnest visible line (maps to `StyleSheet.hairlineWidth`).
- `roundToNearestPixel(value)` — Round to nearest pixel.
- `getPixelSizeForLayoutSize(layoutSize)` — Layout size → pixel size.
- `platformColor(name)` — e.g. `platformColor(systemBlue)`.

## Key Points

- Use `@theme` in CSS for design tokens; use `vars()` in JS for runtime CSS variables.
- Keep `calc()` operands to a single unit type on native to avoid layout engine limits.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/functions-and-directives.mdx)
-->
