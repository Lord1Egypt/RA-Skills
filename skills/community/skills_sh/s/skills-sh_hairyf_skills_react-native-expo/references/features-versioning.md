---
name: Upgrading Expo SDK
description: Upgrade Expo SDK incrementally; npx expo install --fix, expo-doctor, and when to regenerate native projects.
---

# Upgrading Expo SDK

Upgrade one SDK version at a time to isolate breakages. Expo Go supports only the latest (and sometimes previous) SDK; production apps on EAS typically have longer support via development builds.

## Usage

**Upgrade to a target SDK (example: 54):**

```bash
npm install expo@^54.0.0
npx expo install --fix
npx expo-doctor
```

**Then update native projects:**

- **CNG (no android/ios in repo):** delete local **android** and **ios** if present; they are regenerated on next `npx expo run`, `npx expo prebuild`, or EAS Build.
- **Bare/managed native dirs:** run `npx pod-install` in **ios** if applicable; apply changes from the [Native project upgrade helper](https://docs.expo.dev/bare/upgrade/). Consider [adopting prebuild](https://docs.expo.dev/guides/adopting-prebuild/) for easier upgrades.

**Check release notes** for the target SDK (e.g. “Upgrading your app” and breaking changes) before and after upgrading.

## Key points

- **npx expo install --fix** aligns Expo-related dependencies to versions compatible with the installed **expo** package; prefer it over raw `npm install` for Expo/React Native deps.
- **expo-doctor** checks for common misconfigurations and version mismatches; run after upgrading.
- **CNG** keeps upgrades mostly in dependency and config space; avoid manual native edits so prebuild stays the source of truth.
- **Deprecated SDKs:** old Expo Go builds may not work; use development builds for production and for testing older SDKs where supported by EAS.

<!--
Source references:
- https://docs.expo.dev/workflow/upgrading-expo-sdk-walkthrough/
-->
