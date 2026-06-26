# react-native-update integration playbook

## Contents
- Fast path
- Service choice
- App shape specifics
- JS wiring
- Strategy and hook options
- Native touchpoints
- Release baseline and publishing
- Verification
- Troubleshooting
- Examples

## 1) Fast path
1. In the app root, install the SDK and ensure the CLI is available:
   - `npm i react-native-update`
   - `npm i -g react-native-update-cli`
   - Use `yarn`, `pnpm`, or `bun` equivalents only when the project already uses that package manager.
2. For iOS, run `cd ios && pod install` after dependency changes.
3. Create or select app records per platform with the matching service CLI:
   - Pushy: `pushy createApp --platform ios|android|harmony` or `pushy selectApp --platform ...`
   - Cresc: `cresc createApp --platform ios|android|harmony` or `cresc selectApp --platform ...`
4. Commit the generated `update.json`. It is not a secret. Do not commit `.update`.
5. Configure native bundle loading for iOS/Android/Harmony.
6. Initialize one `Pushy` or `Cresc` client and wrap the app with `UpdateProvider`.
7. Build a release package, upload that exact package as the native baseline, then publish a `.ppk` hot update.

## 2) Service choice
- Pushy China service: use `Pushy` from `react-native-update`, `pushy` CLI, Pushy admin, RMB billing.
- Cresc global service: use `Cresc` from `react-native-update`, `cresc` CLI, Cresc admin, USD billing.
- `update.json` stores app IDs and app keys for whichever service created them. Keep the JS client class and CLI service aligned.
- The same SDK supports both services; most integration code differs only in the client class name and command prefix.

## 3) App shape specifics

### React Native CLI
- Standard install plus iOS pods.
- RN >= 0.60 normally autolinks. Very old RN, monorepos, brownfield, or custom native layouts may need manual linking.

### Expo
- Use Expo prebuild workflow: `npx expo prebuild`.
- Expo 50+ is the supported baseline. Expo New Architecture support before Expo 51 is incomplete; prefer the latest Expo available.
- Do not co-install `expo-updates`; it conflicts with update behavior.
- Expo 48+ with `react-native-update` >= 10.28.2 configures iOS bundle URL automatically. Still run pods after prebuild.

### HarmonyOS
- `update.json` can include a `harmony` entry. Do not rely on `Platform.OS` unless the app already normalizes it to `harmony`.
- Harmony needs native package/provider/bundle-provider wiring in addition to JS `UpdateProvider`.
- Keep the bundle file name `bundle.harmony.js` whether or not Hermes bytecode is used.

### Brownfield or monorepo
- Do not change host app inheritance just to integrate OTA.
- Wire the bundle URL at the runtime creation point:
  - iOS XCFramework: call `RCTPushy.bundleURL()` through the brownfield bundle URL override or bridge delegate.
  - Android AAR/new architecture: pass `UpdateContext.getBundleUrl(application, "assets://index.android.bundle")` into `ReactHost` / `getDefaultReactHost`.
- Ensure the final distributed package contains the exact embedded baseline bundle that is uploaded as the native baseline.

## 4) Minimum JS wiring
Read the platform app key from `update.json`.

For iOS/Android:

```tsx
import { Platform } from 'react-native';
import updateConfig from './update.json';

const { appKey } = updateConfig[Platform.OS as 'ios' | 'android'];
```

For Harmony:

```tsx
import updateConfig from './update.json';

const { appKey } = updateConfig.harmony;
```

Pushy:

```tsx
import { Pushy, UpdateProvider } from 'react-native-update';
import App from './App';

const updateClient = new Pushy({
  appKey,
});

export default function Root() {
  return (
    <UpdateProvider client={updateClient}>
      <App />
    </UpdateProvider>
  );
}
```

Cresc:

```tsx
import { Cresc, UpdateProvider } from 'react-native-update';
import App from './App';

const updateClient = new Cresc({
  appKey,
});

export default function Root() {
  return (
    <UpdateProvider client={updateClient}>
      <App />
    </UpdateProvider>
  );
}
```

Rules:
- Create the client outside the component so it is stable across renders.
- Do not call `useUpdate()` in the same component that renders `UpdateProvider`; call it in descendants.
- Prefer the functions returned from `useUpdate()` (`checkUpdate`, `downloadUpdate`, `switchVersion`, `switchVersionLater`, etc.) over direct `client` calls. Direct `client` access is an escape hatch for unusual low-level integrations, not the normal app API.
- Use `checkUpdate()` to start a check only. Do not write flow control against `await checkUpdate()`; read `updateInfo` and `lastError` from `useUpdate()` in a `useEffect` or render path. This keeps manual checks, automatic checks, deep links, and QR flows on the same state-driven path.
- For TypeScript JSON imports, enable `resolveJsonModule` or use the project's existing JSON-import pattern.

## 5) Strategy and hook options
- `checkStrategy`: `both` / `onAppStart` / `onAppResume` / `null`
- `updateStrategy`: `alwaysAlert` / `alertUpdateAndIgnoreError` / `silentAndNow` / `silentAndLater` / `null`
- For custom UI: set `updateStrategy: null`, then use `useUpdate()`.
- `debug: true` can check/download in development but cannot apply patches. Applying updates requires release builds.
- `throwError: true` lets callers use `try/catch`; otherwise use `lastError`.
- `beforeCheckUpdate`, `beforeDownloadUpdate`, `afterDownloadUpdate`, and `onPackageExpired` are control hooks for custom gates.
- `afterCheckUpdate` is useful for analytics or observability after each check.
- `logger` can forward update events to analytics.
- Avoid passing the `client` object down through app code. Keep the client at provider setup and drive UI through `useUpdate()` state.

## 6) Native touchpoints

### iOS
- Import the native module outside debug/flipper conditionals:
  - Objective-C / Objective-C++: `#import "RCTPushy.h"`
  - Swift: `import react_native_update`
- In release mode, use `RCTPushy.bundleURL()` for the bundle URL.
- For RN >= 0.74, update `bundleURL`.
- For RN < 0.74, update `sourceURLForBridge`.
- Keep DEBUG bundle behavior unchanged.
- In mixed native/RN apps, initialize the bridge with a delegate and then create the root view with `initWithBridge`; do not pass a fixed release `bundleURL` directly to the root view.
- After any iOS native change, rebuild the app.

### Android
- Import `cn.reactnative.modules.update.UpdateContext`.
- RN 0.82+ / New Architecture `ReactHost`: pass `jsBundleFilePath = UpdateContext.getBundleUrl(this)` into `getDefaultReactHost(...)`.
- RN 0.81 or lower `DefaultReactNativeHost`: override `getJSBundleFile()` and return `UpdateContext.getBundleUrl(this@MainApplication)`.
- Java `DefaultReactNativeHost`: override `protected String getJSBundleFile()` and return `UpdateContext.getBundleUrl(MainApplication.this)`.
- Brownfield/custom `ReactInstanceManager`: call `.setJSBundleFile(UpdateContext.getBundleUrl(context, "assets://index.android.bundle"))` and do not also set `setBundleAssetName`.
- If `react-native-screens` is installed, register `RNScreensFragmentFactory` in `MainActivity.onCreate`; do not put it in `MainActivityDelegate`.
- Disable release PNG crunching with `crunchPngs false` to keep diffs predictable.
- For AAB resource splits, `react-native-update` >= 10.36.0 handles the known image issue. On older versions, disable density splitting.

### Harmony
Minimum native checklist:
- `harmony/entry/src/main/cpp/CMakeLists.txt`: include `react-native-update/harmony/pushy/src/main/cpp` and compile `PushyTurboModule.cpp`.
- `harmony/entry/src/main/cpp/PackageProvider.cpp`: add `PushyPackage`.
- `harmony/entry/oh-package.json5`: add the `pushy` HAR dependency.
- `harmony/hvigor/hvigor-config.json5`: point `pushy` to `node_modules/react-native-update/harmony`.
- `harmony/entry/hvigorfile.ts`: add `reactNativeUpdatePlugin()`.
- `harmony/entry/src/main/ets/RNPackagesFactory.ts`: return `new PushyPackage(ctx)`.
- `harmony/entry/src/main/ets/pages/Index.ets`: add `PushyFileJSBundleProvider` before the resource bundle provider fallback.

## 7) Release baseline and publishing
- Build the native release first and upload the exact distributed package as the baseline:
  - iOS: `pushy uploadIpa <file.ipa>` or `cresc uploadIpa <file.ipa>`
  - Android APK: `pushy uploadApk <file.apk>` or `cresc uploadApk <file.apk>`
  - Android AAB: `pushy uploadAab <file.aab>` or `cresc uploadAab <file.aab>`
  - Harmony APP: `pushy uploadApp <file.app>` or `cresc uploadApp <file.app>`
- The file uploaded to the server must be byte-for-byte equivalent to the one users install. Keep a copy and tag the native version.
- If native code/config changes or the app is rebuilt, bump the native version and upload a new baseline. Rebuilding the same version can create build-time mismatches and larger/fallback updates.
- If producing APK and AAB for the same version, build both in the same Gradle invocation, for example:

```json
{
  "scripts": {
    "package:android:release": "cd android && ./gradlew clean assembleRelease bundleRelease"
  }
}
```

- Publish JS/assets-only changes with:
  - `pushy bundle --platform ios|android|harmony`
  - `cresc bundle --platform ios|android|harmony`
- If a framework such as modern Expo has no `index.js`, create one that imports the real entry, for example `import "expo-router/entry";`.
- After publishing the `.ppk`, bind it to one or more uploaded native baselines. Canary rollout can bind one partial rollout and one full rollout per native baseline; client support requires `react-native-update` >= 10.32.0.

## 8) Verification checklist
- [ ] Release build succeeds on target platform.
- [ ] Native package baseline is uploaded for the exact package distributed to users.
- [ ] `update.json` has the platform `appKey` used by the JS client.
- [ ] App can call check update and returns structured update state.
- [ ] Update package download succeeds.
- [ ] App can switch to new version (now/later behavior as expected).
- [ ] QR/deep-link test path works if used.
- [ ] Rollback behavior understood/tested for crash scenarios.

## 9) Common pitfalls
- Missing/incorrect `update.json` appKey by platform.
- Mixing Pushy CLI/app keys with `new Cresc(...)`, or Cresc app keys with `new Pushy(...)`.
- Calling `client.checkUpdate()` / `client.downloadUpdate()` directly in normal UI code instead of using `useUpdate()`.
- Reading `const info = await checkUpdate()` and branching on it. Trigger the check, then react to `updateInfo` changes from `useUpdate()`.
- Expecting real apply-update behavior in DEBUG builds.
- Expo project still carrying `expo-updates`.
- Expo project not prebuilt before native changes.
- iOS release still returning the embedded Metro bundle URL instead of `RCTPushy.bundleURL()`.
- Android native host still using `setBundleAssetName("index.android.bundle")` instead of `UpdateContext.getBundleUrl(...)`.
- `react-native-screens` blank screen after OTA restart because `RNScreensFragmentFactory` is missing.
- Native release package uploaded to the server differs from the package actually installed by users.
- Rebuilding the same native version and distributing it without uploading the new baseline.
- Android release PNG crunching or old AAB density split behavior changing asset bytes.
- iOS pods not installed after dependency update.
- Native file edits not followed by full rebuild.
- Treating `metaInfo` as an object. It is a string payload; parse JSON defensively.

## 10) Example: class component integration
Use this when the app root is still class-based.

```tsx
import React from 'react';
import { Platform } from 'react-native';
import { Pushy, UpdateProvider } from 'react-native-update';
import App from './App';
import updateConfig from './update.json';

const { appKey } = updateConfig[Platform.OS as 'ios' | 'android'];

const pushyClient = new Pushy({
  appKey,
  checkStrategy: 'onAppStart',
  updateStrategy: 'alertUpdateAndIgnoreError',
});

export default class Root extends React.Component {
  render() {
    return (
      <UpdateProvider client={pushyClient}>
        <App />
      </UpdateProvider>
    );
  }
}
```

For Cresc, replace `Pushy` with `Cresc`.

## 11) Example: custom whitelist (gray release)
Use `metaInfo` and your own user/device attributes to decide whether to apply update.

```tsx
import { useEffect, useRef } from 'react';
import { useUpdate } from 'react-native-update';

function useWhitelistGate(currentUserId: string) {
  const { checkUpdate, updateInfo, downloadUpdate, switchVersionLater } = useUpdate();
  const handledHashRef = useRef<string | null>(null);
  const inFlightHashRef = useRef<string | null>(null);

  useEffect(() => {
    void checkUpdate();
  }, [checkUpdate]);

  useEffect(() => {
    if (!currentUserId) return;
    if (!updateInfo?.update || !updateInfo.hash) return;
    if (handledHashRef.current === updateInfo.hash) return;
    if (inFlightHashRef.current === updateInfo.hash) return;

    let cancelled = false;
    (async () => {
      let meta: { allowUsers?: string[]; allowChannels?: string[] } = {};
      try {
        meta = updateInfo.metaInfo ? JSON.parse(updateInfo.metaInfo) : {};
      } catch {
        return;
      }

      const allowList = meta.allowUsers ?? [];
      if (!allowList.includes(currentUserId)) return;

      inFlightHashRef.current = updateInfo.hash!;
      try {
        const ok = await downloadUpdate();
        if (!cancelled && ok) {
          handledHashRef.current = updateInfo.hash!;
          switchVersionLater();
        }
      } finally {
        inFlightHashRef.current = null;
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [currentUserId, updateInfo, downloadUpdate, switchVersionLater]);
}
```

Notes:
- Keep server-side rollout rules as source of truth; client whitelist is an extra guard.
- Store small, explicit whitelist keys in `metaInfo` such as `allowUsers` or `allowChannels`.
- Prefer phased rollout: internal users -> small percent -> full rollout.
- Never crash on malformed `metaInfo`; wrap JSON parsing in `try/catch`.
