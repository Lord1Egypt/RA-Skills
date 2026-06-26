---
name: Expo development workflow
description: Core development loop, development builds vs Expo Go, and when to use prebuild or EAS Build.
---

# Development workflow

Expo apps are React Native apps using Expo tooling. The core loop: write JS → update app config or native/config plugins → install native deps or change native code → create a development build when native changes are required.

## Usage

**Start dev server and run on device/simulator:**

```bash
npx expo start
```

**Run native build locally (generates android/ios if missing):**

```bash
npx expo run:android
npx expo run:ios
```

**When to create a new development build:**

- You changed **app.json** / app config in ways that affect native projects (e.g. permissions, plugins).
- You added or updated a library that has native code or a config plugin.
- You wrote or changed native code (e.g. via Expo Modules API or config plugin).

Use **development builds** (with `expo-dev-client`) for production-style development; **Expo Go** is a limited playground and not suitable for store-bound apps or custom native code.

## Key points

- **Development build:** debug build that includes `expo-dev-client`. You can use any native module and config plugins. Create via EAS Build (`eas build --profile development`) or locally (`npx expo run:android|ios` after prebuild).
- **Continuous Native Generation (CNG):** native projects are generated from app config + **package.json** (e.g. via `npx expo prebuild`). Default for `create-expo-app`; **android** and **ios** are often in **.gitignore** and regenerated on demand or in the cloud.
- **Cloud vs local:** EAS Build runs prebuild when **android**/**ios** are absent; local builds use `npx expo prebuild` (or `npx expo run`, which runs prebuild for the target platform if needed). Use `npx expo prebuild --clean` when config or native deps change to avoid stale native state.
- **Core activities:** (1) JS-only changes → no new build; (2) app config changes → prebuild/rebuild if they affect native; (3) native code or config plugin changes → development build; (4) new native dependency → development build, optionally via its config plugin.

<!--
Source references:
- https://docs.expo.dev/workflow/overview/
- https://docs.expo.dev/workflow/continuous-native-generation/
-->
