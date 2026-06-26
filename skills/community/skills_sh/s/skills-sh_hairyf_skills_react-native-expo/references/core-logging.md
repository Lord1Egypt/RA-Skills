---
name: Logging and viewing logs
description: Console logs in terminal, native logs in Xcode/Android Studio, and system logs (log-android / log-ios).
---

# Logging

React Native apps can be inspected via console output in the Expo CLI terminal, native IDE logs, or system-wide device logs.

## Usage

**Console (JS):** When you run `npx expo start` and connect a device or simulator, `console.log` / `console.warn` / `console.error` appear in the terminal. Logs are sent over WebSockets, so fidelity is lower than attaching dev tools directly.

**High-fidelity JS logs:** Use a development build with [Hermes](https://docs.expo.dev/guides/using-hermes/) and the [JavaScript inspector](https://docs.expo.dev/guides/using-hermes/#javascript-inspector-for-hermes) for `console.table` and full dev tools.

**Native logs (Android):**

- Open the project in Android Studio (e.g. after `npx expo prebuild`), run the app, and use **Logcat**.
- Or from terminal: `npx react-native log-android` (wraps `adb logcat`).

**Native logs (iOS):**

- Open the project in Xcode, run the app, and use the console/debug area.
- Or from terminal: `npx react-native log-ios` (system logs for the device/simulator).

**System logs (all processes on device):**

```bash
# Android
npx react-native log-android

# iOS
npx react-native log-ios
```

Use these when you need logs from other apps or the OS, not just your app.

## Key points

- **Console:** Shown in the Expo CLI terminal when a device/simulator is connected; WebSocket-based, so not full fidelity. For full dev tools, use Hermes + inspector in a development build.
- **Native debugging:** Best done by building and running from Android Studio or Xcode and using their log/console UIs.
- **log-android / log-ios:** Convenient for terminal-only workflows; they show system-wide logs, so filter by your app if needed.

<!--
Source references:
- https://docs.expo.dev/workflow/logging/
- https://docs.expo.dev/debugging/runtime-issues/#native-debugging
-->
