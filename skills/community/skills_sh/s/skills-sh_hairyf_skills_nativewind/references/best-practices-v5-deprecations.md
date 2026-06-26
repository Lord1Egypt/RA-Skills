---
name: best-practices-v5-deprecations
description: v5 deprecations — useColorScheme, cssInterop/remapProps → styled, dynamic mapping → @prop
---

# v5 Deprecations & Replacements

NativeWind v5 keeps most APIs but deprecates a few; replace them to avoid future breakage and to use the recommended patterns.

## Usage

**useColorScheme:** The `useColorScheme` hook from `nativewind` is **deprecated**. Use React Native's API instead:

```tsx
import { useColorScheme, Appearance } from "react-native";

const colorScheme = useColorScheme();
const setColorScheme = (scheme) => Appearance.setColorScheme(scheme);
const toggleColorScheme = () =>
  Appearance.setColorScheme(Appearance.getColorScheme() === "dark" ? "light" : "dark");
```

**cssInterop / remapProps:** Replaced by **styled()**. Same options (e.g. `className: "style"`, multiple props, `nativeStyleToProp`). remapProps-style: `styled(Component, config, { passThrough: true })`; limit transform: `{ global: false }`.

**Dynamic mapping modifier:** Old `{}-[propName]:utility` is **renamed** to `@prop-[propName]:utility`. Update class names when migrating from v4.

**Native theme / JS:** JavaScript theme helpers are removed; use CSS equivalents (e.g. `platformColor()`, `hairlineWidth()` in `@theme`). `platformSelect` → `@media ios` / `@media android` in CSS.

## Key Points

- Deprecated features still work in v5 but emit warnings; migrate to avoid removal in a future major.
- Prefer `styled()` for any new third-party component wrapping; use RN's `useColorScheme` and `Appearance` for theme toggling.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/use-color-scheme.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/guides/migrate-from-v4.mdx)
-->
