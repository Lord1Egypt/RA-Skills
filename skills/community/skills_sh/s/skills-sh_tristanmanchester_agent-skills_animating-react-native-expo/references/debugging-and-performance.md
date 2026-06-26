# Debugging & performance checklist

## Verify the basics

### 1) Reanimated 4 is New Architecture only

If you see native build/runtime issues after upgrading, verify your app is on the New Architecture.

Docs:
- https://docs.swmansion.com/react-native-reanimated/docs/guides/migration-from-3.x/
- https://docs.swmansion.com/react-native-reanimated/docs/guides/compatibility/

### 2) Avoid “Remote JS Debugging”

Expo notes Reanimated is incompatible with remote debugging on JSC; prefer Hermes + inspector.

Docs: https://docs.expo.dev/versions/latest/sdk/reanimated/

## Worklet-related issues

### “Failed to create a worklet”

Common causes:
- Wrong/missing Babel plugin.
  - Expo: generally auto-configured when installed via `expo install`.
  - Bare: use `react-native-worklets/plugin` (Reanimated 4 migration).

Migration guide: https://docs.swmansion.com/react-native-reanimated/docs/guides/migration-from-3.x/

### JS side-effects from worklets

Use `scheduleOnRN` (not `runOnJS`). Functions passed to `scheduleOnRN` must exist in JS scope.

Docs: https://docs.swmansion.com/react-native-reanimated/docs/guides/worklets/

### Closure capture

If a worklet “randomly” slows down, check whether it captured a large object.

Docs: https://docs.swmansion.com/react-native-reanimated/docs/guides/worklets/

## Gesture issues

### Gestures not recognised

- Ensure you wrapped the root with `GestureHandlerRootView`.
- For Android Modals, wrap Modal content with a root view.

Docs: https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/installation/

### Conflicts / undefined behaviour

From the GestureDetector docs:
- Don’t nest detectors using different API styles.
- Don’t reuse the same gesture instance across multiple detectors.

Docs: https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/gesture-detectors/

## CSS transition performance

Avoid `transitionProperty: 'all'` unless you absolutely need it.

Docs: https://docs.swmansion.com/react-native-reanimated/docs/css-transitions/transition-property/

## Layout animation gotchas on New Architecture

From the entering/exiting docs:
- Don’t overwrite `nativeID` on animated views.
- Some components overwrite `nativeID` for children; wrap animated children with a plain `View` if animations don’t run.
- View flattening can cause a removed parent not to wait for children’s exiting animations; mitigate with `collapsable={false}`.

Docs: https://docs.swmansion.com/react-native-reanimated/docs/layout-animations/entering-exiting-animations/
