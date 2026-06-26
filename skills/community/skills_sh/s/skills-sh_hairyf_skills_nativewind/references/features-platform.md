---
name: features-platform
description: Platform variants, units, responsive breakpoints, and safe area
---

# Platform Variants, Units, and Responsive Design

NativeWind adds platform-specific variants, supports a subset of units on native, reactive breakpoints, and safe-area utilities.

## Usage

**Platform variants** — Use modifiers to apply styles per platform:

```tsx
<View className="flex native:flex-col web:grid web:grid-cols-3" />
<Text className="ios:font-[System] android:font-[Roboto]" />
```

Variants: `ios:`, `android:`, `native:`, `web:`, `tv:`.

**Units on native** — Supported: `px` (density-independent on native), `%`, `vw`/`vh` (via window dimensions, reactive), `rem` (default 14 on native, 16 on web), `em`. Ratio values (e.g. `aspect-ratio: 16/9`) supported. Override root font size with `:root { font-size: 16px; }` if needed.

**Responsive breakpoints** — `sm:`, `md:`, `lg:`, `xl:`, `2xl:` work on native using window-width media queries; styles update when dimensions change (rotation, split screen) without extra re-renders.

```tsx
<Text className="text-sm md:text-base lg:text-lg">Responsive text</Text>
```

**Safe area** — From `nativewind/theme` (tailwindcss-safe-area). Use utilities such as `pt-safe`, `pb-safe`, `inset-safe`, `min-h-screen-safe`, `pb-safe-offset-{n}`, `pb-safe-or-{n}` so content respects notches and home indicators.

## Key Points

- Use `native:` or `web:` when a utility is web-only (e.g. `grid`) so native gets a valid alternative (e.g. `flex`).
- `px` in theme/CSS is treated as dp on native; no separate "dp" unit in class names.
- Media queries on native are reactive; no manual subscription needed for orientation or window size.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/tailwindcss.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/units.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/responsive-design.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/tailwind/new-concepts/safe-area-insets.mdx)
-->
