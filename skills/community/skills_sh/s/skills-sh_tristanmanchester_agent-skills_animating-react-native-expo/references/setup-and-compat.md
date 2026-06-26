# Setup & compatibility (Expo-first)

## 1) Expo-managed projects

Install with Expo so versions match your SDK:

```bash
npx expo install react-native-reanimated react-native-worklets
npx expo install react-native-gesture-handler
```

Key points from the official docs:
- Expo’s Reanimated integration installs both `react-native-reanimated` and `react-native-worklets` via `expo install`.
  The Reanimated Babel plugin is configured automatically through Expo’s Babel preset when installed this way.
  See Expo’s Reanimated page.
  https://docs.expo.dev/versions/latest/sdk/reanimated/
- Expo’s Gesture Handler page recommends installing via `expo install react-native-gesture-handler`.
  https://docs.expo.dev/versions/latest/sdk/gesture-handler/

Debugging note (common gotcha):
- Reanimated relies on APIs incompatible with “Remote JS Debugging” (JSC). Use Hermes + the Hermes JavaScript Inspector instead.
  (Expo highlights this in its Reanimated docs.)
  https://docs.expo.dev/versions/latest/sdk/reanimated/

## 2) Reanimated 4 requirements (architecture + worklets)

Reanimated 4 is **New Architecture only** (Fabric / TurboModules). If your app is still on the legacy architecture, stay on Reanimated 3 or migrate the app to the New Architecture.

Official migration + compatibility pages:
- Migration guide: https://docs.swmansion.com/react-native-reanimated/docs/guides/migration-from-3.x/
- Compatibility table: https://docs.swmansion.com/react-native-reanimated/docs/guides/compatibility/

Reanimated 4 also:
- Adds a required dependency on `react-native-worklets`.
- Renames the Babel plugin from `react-native-reanimated/plugin` to `react-native-worklets/plugin` (bare RN).
  See the migration guide above.

## 3) Gesture Handler setup essentials

Wrap the app with `GestureHandlerRootView` as close to the root as possible.

From the official installation guide:
- `GestureHandlerRootView` defaults to `flex: 1`; if you provide a custom style, keep `flex: 1`.
- Gestures outside the root view won’t be recognised, and gesture relations only work under the same root view.
- If a dependency already renders a root view, it’s still safe to add one at the root; nested root views are ignored except for the top-most.
- If using gestures inside a React Native `Modal` on Android, wrap the Modal’s content with `GestureHandlerRootView`.

Docs:
- https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/installation/

Expo tutorial chapter (gesture + Reanimated together):
- https://docs.expo.dev/tutorial/gestures/
