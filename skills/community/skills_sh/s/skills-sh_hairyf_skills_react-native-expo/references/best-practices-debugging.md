---
name: Debugging Expo apps
description: Debug development and production issues; console and native logs, native debuggers, and reproducing production errors locally.
---

# Debugging runtime issues

Split issues into development-time and production-time. Use stack traces, isolation, and native logs; for production, reproduce locally first and use crash reporting.

## Usage

**Console logs:** with `npx expo start`, console output appears in the terminal. For higher fidelity (e.g. `console.table`), use a development build with Hermes and the [JS inspector](https://docs.expo.dev/guides/using-hermes/#javascript-inspector-for-hermes).

**Native logs – Android:**

```bash
adb logcat
# or
npx react-native log-android
```

**Native logs – iOS:** Xcode → Window → Devices and Simulators → select device/simulator → Open Console.

**Reproduce production JS locally:**

```bash
npx expo start --no-dev --minify
```

**Native debugging (Android Studio):**

```bash
npx expo prebuild -p android
open -a "Android Studio" ./android
# Then build and attach debugger in Android Studio
```

**Native debugging (Xcode, macOS):**

```bash
npx expo prebuild -p ios
xed ios
# Build (Cmd+R) and use LLDB / Xcode debugging tools
```

Delete **android** / **ios** after native debugging if you rely on CNG so the project stays managed by Expo.

## Key points

- **Isolate the bug:** revert to a working state, re-apply changes in small steps, or reproduce in a minimal `create-expo-app` project. Use breakpoints or `console.log` to confirm code paths and values.
- **Production:** reproduce locally first, then follow development debugging. Use store crash reports (Play Console, Xcode Crashes), native logs on a device that reproduces the crash, and Sentry/BugSnag (or similar) for JS errors and stack traces.
- **Crashes on older devices:** often performance-related; use React Native DevTools profiler and native profiling to find bottlenecks.
- **Stuck:** search the error message, check [Expo forums](https://chat.expo.dev/), [GitHub issues](https://github.com/expo/expo/issues), and Stack Overflow.

<!--
Source references:
- https://docs.expo.dev/debugging/runtime-issues/
- https://docs.expo.dev/workflow/logging/
- https://docs.expo.dev/debugging/tools/
-->
