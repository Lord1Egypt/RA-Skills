---
name: Expo SDK and third-party libraries
description: Use Expo SDK packages, React Native core, and third-party native libraries; determine compatibility and install with npx expo install.
---

# Expo SDK and third-party libraries

Use **React Native** core components/APIs from `react-native`, **Expo SDK** packages from the [API reference](https://docs.expo.dev/versions/latest/) for device and system features (camera, updates, maps, auth, etc.), and **third-party** npm packages. Compatibility depends on whether you use **Expo Go** or a **development build**.

## Usage

**Install Expo SDK or React Native–compatible packages (preferred):**

```bash
npx expo install expo-device
npx expo install @react-navigation/native
```

`npx expo install` picks versions that match your Expo SDK and warns about known incompatibilities.

**Expo SDK usage (example):**

```js
import Constants from 'expo-constants';
import * as Device from 'expo-device';
```

**Check compatibility before adding a library:**

- Does it ship **android** or **ios** directories or mention “linking”?
- Does it require changes to **AndroidManifest.xml**, **Info.plist**, or **Podfile**?
- Does it provide a [config plugin](https://docs.expo.dev/config-plugins/introduction/)?

If any is yes, use a **development build**; add the package, add its config plugin to app config if required, then create a new build.

**Exclude a package from Expo version checks:**

In **package.json**:

```json
{
  "expo": {
    "install": {
      "exclude": ["some-package"]
    }
  }
}
```

## Key points

- **Expo Go:** only supports the Expo SDK and a curated set of third-party libs (see “Expo Go” on [React Native Directory](https://reactnative.directory)). Not suitable for production or custom native code.
- **Development builds:** include your app’s native code and config; any React Native–compatible library can be used. Use [React Native Directory](https://reactnative.directory) and filter by “Expo Go” only when targeting Go.
- **Config plugins:** libraries that need native config often ship or document a config plugin; add it to the `plugins` array in app config so prebuild applies it. Out-of-tree plugins: [expo/config-plugins](https://github.com/expo/config-plugins).
- **Custom native code:** add via [Expo Modules API](https://docs.expo.dev/modules/overview/) (local module with `npx create-expo-module@latest --local`, or standalone module). Use config plugins for native project config; use lifecycle listeners instead of editing AppDelegate/MainApplication directly.

<!--
Source references:
- https://docs.expo.dev/workflow/using-libraries/
- https://docs.expo.dev/versions/latest/sdk/third-party-overview/
- https://docs.expo.dev/workflow/customizing/
-->
