---
name: core-v5-tailwind-foundation
description: NativeWind v5 built on Tailwind CSS v4, CSS-first config, web vs native support
---

# v5 Built on Tailwind CSS

NativeWind v5 is built on **Tailwind CSS v4**, which uses a CSS-first configuration model. The full Tailwind language is available at build time; on native, NativeWind applies the subset supported by React Native's style engine.

## Usage

**Tailwind v4 vs v3:**

- **CSS-first configuration** — Theming via `@theme` in CSS, not `tailwind.config.js`.
- **New directives** — `@import`, `@theme`, `@utility`, `@custom-variant`, `@source` replace `@tailwind` / `@layer`.
- **No config file required** — `tailwind.config.js` is optional; use `@config` to point to one if needed.

**Web vs native:** NativeWind accepts all classes but only applies styles supported on the current platform. For example, `grid` works on web but not on native (RN has flexbox only). Use platform variants to provide both:

```tsx
<View className="flex native:flex-col web:grid web:grid-cols-3">
  {/* flexbox on native, CSS grid on web */}
</View>
```

Recommend reading Tailwind's guides: Utility-First Fundamentals, Reusing Styles, Adding Custom Styles. Configuration details: see [Configuration](references/core-config.md) and [Setup](references/core-setup.md).

## Key Points

- Use `native:` or `web:` when a utility is web-only so native gets a valid alternative.
- Theming and custom utilities are defined in CSS with `@theme` and `@utility`, not in JS config.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/tailwindcss.mdx)
-->
