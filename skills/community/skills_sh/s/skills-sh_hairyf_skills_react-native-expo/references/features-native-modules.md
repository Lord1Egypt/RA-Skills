---
name: Native modules and Expo Modules API
description: Add custom native code with Expo Modules API: local modules, config plugins for native config, and lifecycle subscribers.
---

# Native modules and Expo Modules API

When you need custom native code (no existing library), use the **Expo Modules API** to write Swift and Kotlin modules that are consumed from JavaScript. Use **local** modules for app-specific code and **config plugins** for native project configuration; use **lifecycle subscribers** instead of editing AppDelegate/MainApplication directly.

## Creating a local module

Scaffold a module inside the project so it is linked automatically:

```bash
npx create-expo-module@latest --local
```

Provide a module name when prompted. This creates a **modules/<name>** directory with **android/** and **ios/** and an **expo-module.config.json**. Implement your API in Kotlin/Swift and export it via the generated JS interface.

**Use the module in the app:**

```js
import MyModule from '@/modules/my-module';
MyModule.someMethod();
```

After adding or changing native code, rebuild the app (`npx expo run:android` or `run:ios`). If you use CNG and had no **android**/**ios** dirs, run `npx expo prebuild` first (or let EAS Build do it).

## Config plugin for native configuration

If your module (or a third-party SDK) requires changes to **AndroidManifest.xml**, **Info.plist**, or other native project files, implement a **config plugin** and add it to the app config. Do not edit **android**/**ios** by hand when using CNG—prebuild will overwrite those edits. See [features-config-plugins](features-config-plugins.md) for how to write and register a plugin.

For modules created with `create-expo-module`, you can add a plugin to the module’s **expo-module.config.json** and document that the app must include the module’s plugin in its `plugins` array.

## Lifecycle and AppDelegate

To run code on app launch or in response to lifecycle events (e.g. push notification registration), use **Expo Modules API** lifecycle APIs instead of editing **AppDelegate** or **MainApplication**:

- **iOS:** [AppDelegate subscribers](/modules/appdelegate-subscribers/) — register in the module to run when the app finishes launching, opens a URL, etc.
- **Android:** [Android lifecycle listeners](/modules/android-lifecycle-listeners/) — register for activity/fragment lifecycle.

This keeps behavior composable when multiple libraries need to hook into the same events.

## Key points

- **Expo Modules API** uses Swift/Kotlin and supports the New Architecture; it is the recommended way to add native modules for most apps. Use Turbo Modules if you need heavy C++.
- **Local vs standalone:** `--local` creates a module inside the app repo. Omit `--local` to create a standalone package you can publish or use in a monorepo.
- **CNG:** With prebuild-only workflows, generate native dirs when developing the module (e.g. `npx expo prebuild`) so you can build and test; use `npx pod-install` after adding native files or changing **expo-module.config.json**.

<!--
Source references:
- https://docs.expo.dev/workflow/customizing/
- https://docs.expo.dev/modules/overview/
- https://docs.expo.dev/modules/get-started/
- https://docs.expo.dev/modules/config-plugin-and-native-module-tutorial/
- https://docs.expo.dev/modules/appdelegate-subscribers/
- https://docs.expo.dev/modules/android-lifecycle-listeners/
-->
