---
name: api-with-nativewind
description: withNativewind Metro wrapper options (globalClassNamePolyfill, typescriptEnvPath)
---

# withNativewind (Metro)

`withNativewind` wraps your Metro config to enable NativeWind. It is a thin wrapper around `react-native-css`'s `withReactNativeCSS` with NativeWind defaults.

## Usage

```js
// metro.config.js
const { getDefaultConfig } = require("expo/metro-config");
const { withNativewind } = require("nativewind/metro");

const config = getDefaultConfig(__dirname);
module.exports = withNativewind(config);
```

**Optional second argument** (same shape as `withReactNativeCSS` from `react-native-css/metro`):

| Option | Default | Description |
|--------|---------|-------------|
| `globalClassNamePolyfill` | `true` | Babel transform that rewrites imports to add `className` support to RN components |
| `typescriptEnvPath` | `"nativewind-env.d.ts"` | Path for generated TypeScript declaration file for `className` types |

Override example:

```js
module.exports = withNativewind(config, {
  globalClassNamePolyfill: false,
  typescriptEnvPath: "custom-env.d.ts",
});
```

## Key Points

- In v4 the function was named `withNativeWind` (capital W). Both spellings work in v5; `withNativewind` is preferred.
- No second argument is required in v5 (unlike v4's `input: './global.css'`).

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/with-nativewind.mdx)
-->
