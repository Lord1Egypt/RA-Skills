# Mobile Test Environment Setup

## iOS

```bash
# XCTest (built-in)
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16'

# UI testing (XCUITest)
xcodebuild test -scheme MyAppUITests -destination 'platform=iOS Simulator,name=iPhone 16'
```

**Test types**: XCTest (unit + performance), XCUITest (UI interaction), Swift Testing (Swift 6+), snapshot testing (`ios-snapshot-test-case`).

## Android

```bash
# JUnit + Espresso (built-in Gradle support)
./gradlew test                     # Unit tests
./gradlew connectedAndroidTest     # Instrumented tests (requires emulator/device)
```

**Test types**: JUnit5 (unit), Espresso (UI), UI Automator (cross-app), Robolectric (off-device JVM).

## React Native

```bash
npm install --save-dev jest @testing-library/react-native
npm install --save-dev msw
npm install --save-dev detox               # E2E
detox build --configuration ios.sim.debug
detox test --configuration ios.sim.debug
```

## Flutter

```bash
flutter test                    # Unit + widget
flutter test --coverage
flutter test integration_test/app_test.dart  # E2E (integration_test package)
```

## Simulator vs Real Device

| Scenario | Preference |
|----------|-----------|
| Unit tests | No device needed |
| Component/Widget tests | Simulator (fast) |
| UI interaction tests | Simulator (recommended), real device (CI optional) |
| E2E smoke tests | Real device (CI), simulator (local) |
| Performance tests | Real device (simulator perf inaccurate) |

## CI Device Provisioning

- **iOS**: GitHub Actions macOS runner has Xcode + simulator
- **Android**: `reactivecircus/android-emulator-runner` for GitHub Actions
- **Cloud**: Firebase Test Lab, Sauce Labs, BrowserStack

## Fallback When No Device Available

If CI has no simulator or real device:
1. Unit and widget tests run on standard CI
2. UI/E2E tests marked as manual, run locally
3. Robolectric (Android) for off-device JVM testing
