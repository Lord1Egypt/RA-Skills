# Building the store apps

Do the work on a branch, open a pull request, and do not merge without the student's yes.

## Capacitor 7 wrapper

- Install `@capacitor/core`, `@capacitor/cli`, `@capacitor/ios`, `@capacitor/android` (version 7), plus the plugins the app uses: `@capacitor/app` (deep links, back button), `@capacitor/browser` (OAuth in the system browser), `@capacitor/splash-screen`, `@capacitor/status-bar`, and others only when used.
- `capacitor.config.ts`: `appId`, `appName`, `webDir` pointing at a tiny local folder (for example `native/www/index.html` with an offline message), and `server.url` set to the live HTTPS address so the app loads the real site. Keep `server.cleartext` off.
- A small client component (for example `NativeBridge`) that only runs inside the native app: listens for `appUrlOpen`, finishes sign-in, handles the Android back button, sets the status bar.
- Exclude `android/` and `ios/` from the web deploy (`.vercelignore`) so the web build stays fast.
- Icons and splash: put a 1024x1024 icon and a splash image in `assets/` and run `npx @capacitor/assets generate`.
- Then `npx cap add android`, `npx cap add ios` (iOS needs a Mac), and `npx cap sync` after every change.

## Android on Linux

- Needs a JDK 21 and the Android command-line tools (`sdkmanager "platforms;android-36" "build-tools;36.0.0"`).
- Google Play requires a recent target SDK: set `compileSdkVersion` and `targetSdkVersion` to 36 in `android/variables.gradle`.
- Upload key: create it once with `keytool -genkeypair -v -keystore <app>-upload.jks -alias upload -keyalg RSA -keysize 2048 -validity 10000`. Keep the `.jks` and a `keystore.properties` (store file, alias, passwords) outside the repo, `chmod 600`, and backed up somewhere safe. Never print or commit the passwords; read them from the properties file in `android/app/build.gradle` `signingConfigs`. Use Play App Signing so a lost upload key can be reset.
- Build: `cd android && ./gradlew bundleRelease`, which writes `app/build/outputs/bundle/release/app-release.aab`. Check the signature with `jarsigner -verify`.
- Bump `versionCode` for every upload.
- An Android emulator often does not start on a headless server; test on a real phone or say plainly it was not run.

## iOS on a Mac

- Needs Xcode and the paid Apple account. `npx cap open ios`, set the team, bundle id and version, then Product > Archive and upload to App Store Connect (or `xcodebuild archive` and `xcrun altool`/Transporter).
- Screenshots: Apple requires the 6.9 inch size, 1320x2868. Boot an iPhone Pro Max simulator, clean the status bar first with `xcrun simctl status_bar booted override --time 9:41 --batteryLevel 100 --batteryState charged --cellularBars 4 --wifiBars 3`, sign in with the demo account, then `xcrun simctl io booted screenshot shot1.png`.
- Test on TestFlight before submitting.
