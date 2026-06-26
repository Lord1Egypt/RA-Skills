---
name: advanced-theme
description: Theme tokens, CSS variables at runtime, and NativeWind color behavior
---

# Theming and Dynamic Colors

Define design tokens in `@theme`, use CSS variables for runtime values, and apply NativeWind-specific color behavior.

## Usage

**Theme tokens** — Define in CSS; use as utilities:

```css
@theme {
  --color-brand: #3b82f6;
  --color-brand-light: #93c5fd;
  --font-display: "CustomFont";
  --spacing-18: 4.5rem;
}
```

Use as `text-brand`, `bg-brand-light`, `font-display`, `p-18`, etc.

**Runtime CSS variables** — Use `vars()` from `nativewind` to set CSS variables on a wrapper; reference them in classes:

```tsx
import { vars } from "nativewind";

<View style={vars({ "--color-primary": userColor })}>
  <Text className="text-[--color-primary]">Dynamic color</Text>
</View>
```

Define the variable in CSS (e.g. `:root { --color-primary: #3b82f6; }`) and override per subtree with `vars()`.

**Special color values** — `transparent`, `currentColor`/`current`, `inherit` work; use `border-current` to inherit text color for borders. Opacity modifier: `bg-blue-500/50`. Color functions such as `color-mix()` and HSL/HSLA are supported; theme and CSS variables can be used inside them.

**Native-only theme helpers** — In `@theme` you can use CSS functions such as `platformColor(systemRed, red)`, `hairlineWidth()`, `pixelRatio()`, `fontScale()`, `getPixelSizeForLayoutSize()`, `roundToNearestPixel()`. Platform-specific values via media: `@media ios { :root { --my-color: red; } }` and `@media android { :root { --my-color: blue; } }`.

## Key Points

- Design tokens: `@theme { --color-*, --font-*, --spacing-* }` then use as utilities.
- For values that change at runtime, set CSS variables with `vars()` and reference them in classes with arbitrary value syntax (e.g. `text-[--color-primary]`).
- NativeWind's `nativewind/theme` adds elevation scale, platform fonts, and custom utilities/variants; extend with your own `@theme` and `@utility`/`@custom-variant`.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/customization/theme.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/customization/colors.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/index.mdx)
-->
