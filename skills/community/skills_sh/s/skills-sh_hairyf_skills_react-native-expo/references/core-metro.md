---
name: Metro bundler configuration
description: Customize Metro (expo/metro-config), resolver, transformer, cache, and environment variables.
---

# Metro configuration

Expo uses [Metro](https://metrometro.org/) for bundling. Customize behavior via **metro.config.js** at the project root. Always extend Expo's default config so features like aliases and asset hashing keep working.

## Usage

**Minimal config (recommended baseline):**

```js metro.config.js
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

module.exports = config;
```

**With options (e.g. disable CSS):**

```js metro.config.js
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname, {
  isCSSEnabled: false,
});

module.exports = config;
```

**Custom resolver (e.g. mock a module on web):**

```js metro.config.js
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

config.resolver.resolveRequest = (context, moduleName, platform) => {
  if (platform === 'web' && moduleName === 'lodash') {
    return { type: 'empty' };
  }
  return context.resolveRequest(context, moduleName, platform);
};

module.exports = config;
```

**Custom Babel transformer (extend Expo's):**

```js
const upstreamTransformer = require('@expo/metro-config/babel-transformer');

module.exports.transform = async ({ src, filename, options }) => {
  // Custom handling, then:
  return upstreamTransformer.transform({ src, filename, options });
};
```

Use a custom file (e.g. **metro.transformer.js**) and set `config.transformer.babelTransformerPath` to it.

## Cache and env

**Clear Metro cache after config or dependency changes:**

```bash
npx expo start --clear
npx expo export --clear
```

**Disable dotenv loading:** set `EXPO_NO_DOTENV=1` before running Expo CLI.

**Disable inlining `EXPO_PUBLIC_*` in client:** set `EXPO_NO_CLIENT_ENV_VARS=1` before bundling.

## Key points

- **Always use `getDefaultConfig(__dirname)`** so Expo's resolver, transformer, and platform handling stay intact.
- **Resolver:** Use `config.resolver.resolveRequest` to redirect or return `{ type: 'empty' }` for mocks; always call the default resolver for other modules.
- **Transformer:** Extend `@expo/metro-config/babel-transformer`; use **babel.config.js** and caller info (platform, isDev, etc.) when possible instead of custom transformer logic.
- **Cache:** After changing Metro config, Babel, or PostCSS, run with `--clear` to avoid stale bundles.

<!--
Source references:
- https://docs.expo.dev/versions/latest/config/metro/
- https://docs.expo.dev/guides/customizing-metro/
-->
