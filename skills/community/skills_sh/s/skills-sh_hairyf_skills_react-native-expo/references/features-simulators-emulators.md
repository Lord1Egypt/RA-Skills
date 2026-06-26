---
name: iOS Simulator and Android Studio emulator
description: Using iOS Simulator and Android emulator with Expo: launch from CLI, limitations, and troubleshooting.
---

# iOS Simulator and Android Studio emulator

Developing on simulators/emulators avoids constant use of physical devices. Expo CLI can launch the iOS Simulator or Android emulator and install the app.

## Usage

**Start dev server and open iOS Simulator:**

```bash
npx expo start
# Then press `i` to open iOS Simulator
# Or `shift + i` to choose a specific simulator
```

**Start and open Android emulator:**

```bash
npx expo start
# Then press `a` to open Android emulator (device must be running)
```

**Prerequisites:**

- **iOS:** macOS with Xcode and iOS Simulator. Install Xcode from the App Store; accept the license (`sudo xcodebuild -license accept`) if the CLI warns you. Watchman is recommended.
- **Android:** Android Studio with SDK and at least one AVD (Android Virtual Device). Ensure `ANDROID_HOME` (or `ANDROID_SDK_ROOT`) points to the SDK; `adb` should be on PATH (typically `$ANDROID_HOME/platform-tools`).

Development builds (`npx expo run:ios` / `npx expo run:android`) will build and run on the booted simulator/emulator. For Expo Go, run the app in the simulator/emulator first so the correct Expo Go build is installed.

## iOS Simulator limitations

- **macOS only.** On Windows/Linux you need a physical iOS device or a remote Mac.
- Unavailable in Simulator: audio input, barometer, camera, motion (accelerometer/gyroscope). Use a real device to test those.
- Background apps are suspended (iOS 11+). Expo CLI targets the **most recently opened** simulator if multiple are open.

## Troubleshooting

**iOS: CLI stuck when opening Simulator**

- Open Simulator manually: `open -a Simulator`, then **File → Open Simulator** and pick device/OS. Then press `i` again in Expo CLI.

**iOS: Expo Go not opening in Simulator**

- First install may require interacting with the Simulator (click/drag) before the “Open Expo Go?” prompt appears; tap OK.

**iOS: xcrun or Expo Go errors**

- Uninstall Expo Go in the Simulator, then press `shift + i` in Expo CLI and select the simulator to reinstall.
- If still broken: **Device → Erase All Content and Settings...** in Simulator to reset it (helps when the Simulator is in a bad state or low on memory).

**Android: adb version mismatch**

- Error like `adb server version (xx) doesn't match this client (xx)`. Fix by using the same `adb` everywhere: e.g. run `$ANDROID_HOME/platform-tools/adb version` and, if needed, replace the system `adb` with that binary or ensure PATH prefers `platform-tools`.

## Key points

- **iOS:** `i` / `shift + i` in Expo CLI; requires Xcode and macOS; Simulator has no camera/mic/motion.
- **Android:** Start an AVD first (or use “Cold Boot” from CLI); ensure one `adb` version system-wide to avoid server/client mismatch.
- **Expo Orbit:** Can manage simulators and launch builds from the menu bar (see Expo docs).

<!--
Source references:
- https://docs.expo.dev/workflow/ios-simulator/
- https://docs.expo.dev/workflow/android-studio-emulator/
-->
