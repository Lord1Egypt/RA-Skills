---
name: Continuous Native Generation and Prebuild
description: Generate android/ios from app config and package.json with npx expo prebuild; when to use --clean and how it fits EAS Build.
---

# Continuous Native Generation (CNG) and Prebuild

CNG means native projects are generated on demand from app config and **package.json**, not maintained by hand. **Prebuild** is the command that generates **android** and **ios** from the Expo template + config plugins.

## Usage

**Generate native directories:**

```bash
npx expo prebuild
```

**Generate for one platform:**

```bash
npx expo prebuild --platform ios
```

**Clean regenerate (removes existing android/ios first):**

```bash
npx expo prebuild --clean
```

Use `--clean` when you change app config or add/remove native deps so that config plugins and autolinking produce a consistent result. Without `--clean`, prebuild layers changes on top of existing files, which can diverge.

**Skip dependency version updates (e.g. keep current react/react-native):**

```bash
npx expo prebuild --skip-dependency-update react-native,react
```

**Force package manager or skip install:**

```bash
npx expo prebuild --no-install
npx expo prebuild --pnpm
```

## Key points

- **Inputs:** app config, `npx expo prebuild` args, Expo SDK version (template), autolinking of native modules, config plugins. **Output:** **android** and **ios** directories.
- **EAS Build:** if **android** and **ios** are missing, EAS Build runs prebuild before compiling. If they exist, it does not run prebuild (so local customizations are preserved but may drift from config).
- **Do not edit generated native files** if you rely on CNG; edits are overwritten by the next `npx expo prebuild --clean`. Put native customizations in config plugins or Expo Modules API (e.g. lifecycle listeners).
- **Upgrades:** with CNG, upgrade = bump deps + update app config + run `npx expo prebuild --clean`. No manual native project merges.
- **Libraries:** native-only or config-plugin libraries work with prebuild; use development builds. Expo Go only supports a fixed set of SDK and third-party libs.

<!--
Source references:
- https://docs.expo.dev/workflow/continuous-native-generation/
- https://docs.expo.dev/workflow/prebuild/
-->
