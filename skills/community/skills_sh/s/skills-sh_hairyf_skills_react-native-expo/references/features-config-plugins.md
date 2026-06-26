---
name: Config plugins
description: Use and write config plugins to modify native project files during prebuild (AndroidManifest, Info.plist, etc.).
---

# Config plugins

**Config plugins** run during `npx expo prebuild` (or during EAS Build) and modify generated native projects. Use them when a library or feature requires changes to **AndroidManifest.xml**, **Info.plist**, or other native config that app config does not support by default. With CNG, prefer plugins over editing **android**/**ios** by hand so changes are reproducible.

## Using a config plugin

Add the plugin to the `plugins` array in app config. Many Expo SDK packages export a plugin; add the package name or `[packageName, options]`:

```json
{
  "expo": {
    "plugins": [
      "expo-camera",
      ["expo-secure-store", { "faceIDPermission": "Allow $(PRODUCT_NAME) to use Face ID." }]
    ]
  }
}
```

Plugins run in order. After adding or changing a plugin, run `npx expo prebuild --clean` (or trigger a new EAS Build) so native files are regenerated.

## Writing a config plugin

A plugin is a function that receives Expo config and returns modified config. Use **mods** from `expo/config-plugins` to mutate native files: `withAndroidManifest`, `withInfoPlist`, etc.

**Minimal example — add a string to Android and iOS:**

```js
// plugins/withMyPlugin.js
const { withAndroidManifest, withInfoPlist } = require('expo/config-plugins');

function withMyPlugin(config, options = {}) {
  const message = options.message ?? 'Default message';
  config = withAndroidManifest(config, (c) => {
    const app = c.modResults.manifest?.application?.[0];
    if (app && !app['meta-data']) app['meta-data'] = [];
    app?.['meta-data']?.push({
      $: { 'android:name': 'MyKey', 'android:value': message },
    });
    return c;
  });
  config = withInfoPlist(config, (c) => {
    c.modResults.MyKey = message;
    return c;
  });
  return config;
}

module.exports = withMyPlugin;
```

**In app.config.js:**

```js
module.exports = ({ config }) => ({
  ...config,
  plugins: [['./plugins/withMyPlugin.js', { message: 'Hello' }]],
});
```

**Conventions:** Name the top-level function `with<Name>`. Keep the function synchronous; mods are executed in the prebuild phase. For parameters, use the second argument to the plugin and pass it from app config as the second element of the tuple.

## Key points

- **Mods** are the low-level hooks (e.g. `mods.android.manifest`, `mods.ios.infoplist`). The `with*` helpers from `expo/config-plugins` wrap them and are the recommended way to edit native files.
- **Order:** Plugins run in array order; put plugins that others depend on first.
- **Dynamic config:** To pass options or use a local plugin path, use **app.config.js** or **app.config.ts** (with a loader like `tsx/cjs` for TypeScript).
- **CNG:** With Continuous Native Generation, native dirs are generated on prebuild; config plugin changes apply there. Do not rely on plugin logic running outside prebuild (e.g. in `expo start`).

<!--
Source references:
- https://docs.expo.dev/config-plugins/introduction/
- https://docs.expo.dev/config-plugins/plugins/
- https://docs.expo.dev/config-plugins/mods/
-->
