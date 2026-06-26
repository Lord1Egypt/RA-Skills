---
name: core-config
description: CSS-first configuration, @theme, @source, and nativewind/theme
---

# NativeWind Configuration

NativeWind v5 follows Tailwind CSS v4's CSS-first configuration. No `tailwind.config.js` is required; configure in CSS.

## Usage

**Theme and content in CSS:**

```css
/* global.css */
@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/preflight.css" layer(base);
@import "tailwindcss/utilities.css";
@import "nativewind/theme";

@theme {
  --color-brand: #3b82f6;
  --font-display: "CustomFont";
  --spacing-18: 4.5rem;
}

@source "../components/**/*.tsx";
@source "../screens/**/*.tsx";
```

Optional JS config:

```css
@config "./tailwind.config.js";
```

**What `nativewind/theme` provides:**

- Elevation scale: `--elevation-xs` … `--elevation-2xl` → `elevation-*` utilities (Android shadow elevation).
- Platform font families on `:root` (e.g. iOS: System/Georgia/Menlo; Android: system defaults).
- Custom utilities: `elevation-*`, `tint-*`, `ripple-*`, `corner-*`, `color-*`.
- Custom variants: `ios:`, `android:`, `native:`, `web:`, `tv:`.
- Safe area utilities via `tailwindcss-safe-area`.
- `leading-*` override for unit-less line-height.

**Custom utilities and variants:**

```css
@utility my-shadow {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

@custom-variant dark (@media (prefers-color-scheme: dark));
@custom-variant landscape (@media (orientation: landscape));
```

Plugins:

```css
@plugin "./my-plugin.js";
@plugin "tailwindcss-safe-area";
```

## Key Points

- Prefer `@theme`, `@utility`, `@custom-variant`, and `@source` in CSS over a JS config.
- `@source` explicitly sets content paths if auto-detection isn't enough.
- NativeWind-specific tokens (elevation, platform fonts, variants) come from `@import "nativewind/theme"`.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/customization/configuration.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/customization/theme.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/tailwindcss.mdx)
-->
