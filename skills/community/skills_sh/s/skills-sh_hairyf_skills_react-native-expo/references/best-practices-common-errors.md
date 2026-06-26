---
name: Common Expo development errors
description: Frequent errors when using Expo and how to resolve them (Metro, AppRegistry, SDK version, version mismatch, caches).
---

# Common development errors

Quick reference for frequent Expo/React Native errors and fixes.

## Usage

| Error / symptom | Likely cause | What to do |
|----------------|--------------|------------|
| **Metro ECONNREFUSED 127.0.0.1:19001** | Dev server not reachable | `rm -rf .expo` and check firewall/proxy; ensure nothing else is using the port. |
| **Module AppRegistry is not a registered callable module (calling runApplication)** | JS bundle failing at startup | Run `npx expo start --no-dev --minify` to test production bundle; check device logs in Android Studio/Xcode; check Babel and minifier config. |
| **npm ERR! No git binary found** | Git missing or not in PATH | Install Git and ensure it’s on PATH. |
| **XX.X.X is not a valid SDK version** | Deprecated or unsupported SDK | [Upgrade the project](https://docs.expo.dev/workflow/upgrading-expo-sdk-walkthrough/) to a supported SDK; if already on supported, update Expo Go. |
| **React Native version mismatch** | Different RN version in server vs app | Align versions: [troubleshoot version mismatch](https://docs.expo.dev/troubleshooting/react-native-version-mismatch) using **app.json** and **package.json**. |
| **Application has not been registered** | AppKey mismatch (native vs JS) | [Align AppKey](https://docs.expo.dev/troubleshooting/application-has-not-been-registered/) with the native project. |
| **App not behaving as expected / stale UI** | Caches | Clear caches: [macOS/Linux](https://docs.expo.dev/troubleshooting/clear-cache-macos-linux/), [Windows](https://docs.expo.dev/troubleshooting/clear-cache-windows/). |

When adding fixes (e.g. new deps or config), prefer `npx expo install` and run `npx expo-doctor` after big changes.

## Key points

- **AppRegistry / runApplication:** usually an exception during bundle load; production-like bundle and device logs narrow it down.
- **Version alignment:** use `npx expo install` for Expo/RN deps; keep **expo** and **react-native** in sync with the SDK and each other.
- **Caches:** Metro, Watchman, and build caches can cause stale behavior; clear them when behavior doesn’t match code changes.
- **Contributing:** if you hit an error that’s not documented, consider [opening a PR](https://github.com/expo/expo/pulls) to add it to the common errors list.

<!--
Source references:
- https://docs.expo.dev/workflow/common-development-errors/
- https://docs.expo.dev/troubleshooting/
-->
