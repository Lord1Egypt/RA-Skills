---
name: expo-constants
description: Read app manifest, build info, and system constants at runtime with expo-constants.
---

# expo-constants

**expo-constants** exposes values that stay constant for the lifetime of the app install: app config (manifest), native build info, and device/system info. Use it to read `app.json`/app config in JS, branch between environments, or get runtime identifiers.

## Usage

```bash
npx expo install expo-constants
```

```js
import Constants from 'expo-constants';

// App manifest (from app config)
Constants.expoConfig?.name;
Constants.expoConfig?.version;
Constants.expoConfig?.extra; // custom env / feature flags

// Build / runtime
Constants.manifest?.runtimeVersion; // for expo-updates compatibility
Constants.nativeBuildVersion;       // iOS build number / Android versionCode
Constants.nativeAppVersion;         // version string

// Device / system
Constants.deviceName;
Constants.systemVersion;
Constants.platform?.ios;
Constants.platform?.android;
```

**Typical use cases:** feature flags via `extra`, showing app version in settings, branching logic by channel or build type (e.g. `extra.channel === 'production'`).

## Key points

- **expoConfig:** In development and in Expo Go this is the evaluated app config. In a built app it is the embedded manifest (often a subset). Prefer `Constants.expoConfig` over deprecated `Constants.manifest` when available.
- **extra:** Set in app config (`expo.extra`) or in app.config.js from env (e.g. `extra: { apiUrl: process.env.API_URL }`). Available as `Constants.expoConfig?.extra`.
- **Updates:** `runtimeVersion` in app config is what expo-updates uses; you can read a similar value from constants for display or logging.

<!--
Source references:
- https://docs.expo.dev/versions/latest/sdk/constants/
-->
