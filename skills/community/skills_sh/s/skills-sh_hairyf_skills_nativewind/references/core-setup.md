---
name: core-setup
description: NativeWind v5 setup — CSS file, Metro, PostCSS, and app entry
---

# NativeWind Setup

Minimal setup for NativeWind v5 (Tailwind CSS v4, React Native). Focus on what agents need to add or verify.

## Usage

**1. Main CSS file** — Use Tailwind v4 imports and NativeWind theme:

```css
/* global.css */
@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/preflight.css" layer(base);
@import "tailwindcss/utilities.css";
@import "nativewind/theme";
```

Use the relative path to this file when configuring Metro if needed.

**2. PostCSS** — Ensure `@tailwindcss/postcss` is in use:

```js
// postcss.config.mjs
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

**3. Metro** — Wrap config with `withNativewind`:

```js
// metro.config.js
const { getDefaultConfig } = require("expo/metro-config");
const { withNativewind } = require("nativewind/metro");

const config = getDefaultConfig(__dirname);
module.exports = withNativewind(config);
```

**4. App entry** — Import the CSS in the same file as the root component (not in the file that calls `AppRegistry.registerComponent`) for correct Fast Refresh:

```js
import "./global.css";

export default function App() {
  return (/* ... */);
}
```

**5. Optional overrides** — Pin `lightningcss` to avoid deserialization issues (e.g. in `package.json`):

```json
"overrides": { "lightningcss": "1.30.1" }
```

`withNativewind(config, options)` supports: `globalClassNamePolyfill` (default `true`), `typescriptEnvPath` (default `"nativewind-env.d.ts"`). No Babel config is required in v5; the Metro wrapper applies the transform.

## Key Points

- NativeWind v5 uses Tailwind v4: CSS-first config, no `@tailwind`; use `@import` + `@import "nativewind/theme"`.
- Import CSS in the root component file, not the registration file.
- Use `npx expo start --clear` (or equivalent cache clear) when troubleshooting.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/customization/configuration.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/with-nativewind.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/getting-started/installation/index.mdx)
-->
