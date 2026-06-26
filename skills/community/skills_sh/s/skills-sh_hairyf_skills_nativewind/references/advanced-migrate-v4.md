---
name: advanced-migrate-v4
description: NativeWind v4 to v5 migration steps, breaking changes, deprecations
---

# Migrate from NativeWind v4 to v5

NativeWind v5 is built on Tailwind CSS v4 and react-native-css; it uses CSS-first config, Metro import rewrites instead of Babel JSX transform, and replaces `cssInterop`/`remapProps` with `styled()`. Follow the migration steps and note breaking changes before upgrading.

## Usage

**Prerequisites:** Tailwind CSS v4.1+, React Native 0.81+, New Architecture, React Native Reanimated v4+, and install `react-native-css` as a peer dependency.

**Steps:**

1. **Dependencies:**  
   `npx expo install nativewind@preview react-native-css react-native-reanimated react-native-safe-area-context`  
   Dev: `npx expo install --dev tailwindcss @tailwindcss/postcss postcss`

2. **CSS file:** Replace `@tailwind base/components/utilities` with:
   ```css
   @import "tailwindcss/theme.css" layer(theme);
   @import "tailwindcss/preflight.css" layer(base);
   @import "tailwindcss/utilities.css";
   @import "nativewind/theme";
   ```

3. **Babel:** Remove `nativewind` from babel presets (no `jsxImportSource`, no `nativewind/babel`).

4. **PostCSS:** Add `postcss.config.mjs` with `@tailwindcss/postcss` plugin.

5. **Metro:** Use `withNativewind(config)` (no second argument; name can be `withNativeWind` or `withNativewind`).

6. **Cache:** Run `npx expo start --clear`.

**Breaking / renames:**  
Tailwind v4 class renames apply (e.g. `elevation-sm` → `elevation-xs`, `elevation` → `elevation-sm`). Shadows use `boxShadow`; line-height numeric values parsed as `em`. `rem` no longer changeable at runtime — use CSS variables. Dynamic mapping modifier: `{}-[prop]:utility` → `@prop-[prop]:utility`. Native theme functions (`platformColor`, `hairlineWidth`, etc.) are now CSS functions in `@theme`; `platformSelect` → use `@media ios` / `@media android`. **Deprecated:** `useColorScheme` from nativewind → use React Native's `useColorScheme` and `Appearance.setColorScheme`; `cssInterop`/`remapProps` → use `styled()`.

## Key Points

- JSX transform is replaced by import rewrites (`react-native` → `react-native-css/react-native`); no config change required but may affect custom rewrites.
- Reanimated v4 is required; animation behavior may differ from v4's custom engine.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/guides/migrate-from-v4.mdx)
-->
