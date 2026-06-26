---
name: expo-updates and EAS Update
description: Over-the-air JS updates with expo-updates; runtime version, EAS Update channels, and when updates apply vs when a new binary is required.
---

# expo-updates and EAS Update

**expo-updates** lets the app load remote JavaScript bundles (and assets) so you can ship fixes and content without a new store build. **EAS Update** is the hosted service that serves and manages those updates.

## Usage

**Install and configure with EAS:**

```bash
npx expo install expo-updates
eas update:configure
```

**Publish an update to a channel:**

```bash
eas update --channel production --message "Fix login button"
```

**Required app config (typically set by `eas update:configure`):**

- `updates.url` – update server URL (EAS or self-hosted).
- `runtimeVersion` – string or policy (`appVersion`, `nativeVersion`, `fingerprint`) so updates only go to compatible binaries.

**Manual check and reload in app:**

```js
import * as Updates from 'expo-updates';

async function checkAndReload() {
  const update = await Updates.checkForUpdateAsync();
  if (update.isAvailable) {
    await Updates.fetchUpdateAsync();
    await Updates.reloadAsync();
  }
}
```

Disable automatic check on launch via app config (`updates.checkAutomatically`: `ON_ERROR_RECOVERY` or `NEVER`) if you want full control from JS.

## Key points

- **What can be updated:** JS, styles, assets. **What cannot:** native code, native deps, permissions, Expo SDK version – those require a new binary (EAS Build) and possibly a new `runtimeVersion`.
- **Runtime version:** must match between the binary and the update. Use a policy (e.g. `fingerprint`) so EAS derives it from your project; or set a string manually and bump it when native changes.
- **Channels/branches:** EAS Update uses channels (e.g. `production`, `preview`); point builds to a channel so they receive the right updates. Use branches for more complex workflows.
- **Testing:** In dev builds the bundle usually comes from Metro. Test updates in a release build (or a build that loads from updates); use `eas update` then open the app to see the published update.

<!--
Source references:
- https://docs.expo.dev/versions/latest/sdk/updates/
- https://docs.expo.dev/eas-update/introduction/
- https://docs.expo.dev/build/updates/
-->
