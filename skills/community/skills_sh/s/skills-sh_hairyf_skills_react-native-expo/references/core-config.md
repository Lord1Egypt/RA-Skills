---
name: Expo app config
description: Configure Expo projects with app.json, app.config.js, or app.config.ts for prebuild, Expo Go, and OTA updates.
---

# App config (app.json / app.config.js / app.config.ts)

The app config is the single source for project configuration used by Prebuild, Expo Go, and the OTA update manifest. It must live at the project root next to **package.json**.

## Usage

**Static config (app.json):** minimal example:

```json
{
  "name": "My app",
  "slug": "my-app"
}
```

**Dynamic config (app.config.js):** use for environment-specific values, env vars, or merging with app.json:

```js
module.exports = ({ config }) => ({
  ...config,
  name: process.env.APP_NAME || config.name,
  version: process.env.MY_VERSION || '1.0.0',
  extra: { apiUrl: process.env.API_URL },
});
```

**TypeScript (app.config.ts):** use `ConfigContext` and return `ExpoConfig`:

```ts
import { ExpoConfig, ConfigContext } from 'expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  slug: 'my-app',
  name: 'My App',
});
```

**Reading config in app code:** use `expo-constants`; do not import app.json/app.config.js directly (you get the raw file, not the processed manifest):

```js
import Constants from 'expo-constants';

Constants.expoConfig?.extra?.apiUrl;
```

Sensitive fields (e.g. `hooks`, `ios.config`, `android.config`, `updates.codeSigningCertificate`) are filtered from the public config. Verify public config with:

```bash
npx expo config --type public
```

## Key points

- Config drives Prebuild generation, Expo Go compatibility, and the updates manifest. Full schema: app config reference in docs.
- Prefer **app.config.js** or **app.config.ts** when you need env-based or dynamic values; use **extra** to pass custom data into the app.
- Library authors extend config via [Config plugins](/config-plugins/introduction/); config plugins are applied during `npx expo prebuild`.
- Resolution order: static (app.config.json or app.json) is read first; if a dynamic config (app.config.ts or app.config.js) exists and exports a function, the static config is passed in as `config`; the function’s return value is the final config (no Promises).

<!--
Source references:
- https://docs.expo.dev/workflow/configuration/
- https://docs.expo.dev/versions/latest/config/app/
-->
