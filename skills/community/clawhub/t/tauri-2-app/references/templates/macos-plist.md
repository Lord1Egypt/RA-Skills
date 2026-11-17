# macOS `Info.plist` and `entitlements.plist`

Both files live at `src-tauri/Info.plist` and `src-tauri/entitlements.plist` and are referenced from `tauri.conf.json` `bundle.macOS`.

## `Info.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>{{bundle.identifier}}</string>

    <!-- Usage descriptions: REQUIRED for every OS permission the app requests. -->
    <!-- Without these, the permission prompt never shows and the call returns "denied". -->

    <!-- Microphone — required if the app uses cpal / AVFoundation audio input. -->
    <!-- <key>NSMicrophoneUsageDescription</key>
    <string>{{ProductName}} needs the microphone to record voice input.</string> -->

    <!-- Accessibility — required if the app sends synthetic keystrokes / reads UI. -->
    <!-- <key>NSAccessibilityUsageDescription</key>
    <string>{{ProductName}} needs Accessibility access to insert text into other apps.</string> -->

    <!-- AppleEvents — required if the app sends AppleScript to other apps. -->
    <!-- <key>NSAppleEventsUsageDescription</key>
    <string>{{ProductName}} needs AppleEvents to control other applications.</string> -->

    <!-- Camera, Location, Contacts, Calendar, Photos, etc. — add as needed. -->
</dict>
</plist>
```

**Uncomment only the permissions the app actually uses.** Apple's notarization process flags apps that request permissions they don't exercise.

## `entitlements.plist`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <!-- Start with an EMPTY dict and add entitlements only when needed. -->
    <!-- Each entitlement weakens the hardened runtime; the goal is minimum. -->

    <!-- Audio input — required for microphone capture under sandbox/hardened runtime. -->
    <!-- <key>com.apple.security.device.audio-input</key>
    <true/> -->

    <!-- AppleEvents — only if Info.plist also has NSAppleEventsUsageDescription. -->
    <!-- <key>com.apple.security.automation.apple-events</key>
    <true/> -->

    <!-- JIT — only if the app embeds a JIT VM (rare; e.g. some ML runtimes). -->
    <!-- <key>com.apple.security.cs.allow-jit</key>
    <true/> -->

    <!-- Unsigned executable memory — needed by some unsigned native libraries. -->
    <!-- AVOID if possible; it weakens code-signing protections. -->
    <!-- <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
    <true/> -->
</dict>
</plist>
```

## How to know which entitlements you need

Don't guess. Build the app, run it, and watch Console.app for messages like:

```
{{ProductName}} (12345) deny(1) device-microphone
```

That tells you the missing entitlement — in this case, `com.apple.security.device.audio-input`. Add it, rebuild, retest.

For network entitlements (`com.apple.security.network.client`, `com.apple.security.network.server`), only enable if running under the App Store sandbox. The hardened runtime by itself does not block network access.

## Why minimal entitlements matter

- **Notarization**: Apple's notarization service reviews entitlement lists. Over-broad entitlements (`com.apple.security.cs.disable-library-validation`, `com.apple.security.cs.allow-dyld-environment-variables`) may delay or block notarization.
- **App Store**: stricter still. Only specific entitlements are allowed for App Store apps.
- **Security audit surface**: if a CVE is found in a framework you don't use, an unused entitlement does not save you; if you weren't using `com.apple.security.cs.allow-jit`, you're not affected by JIT-related issues. Tight entitlements = tight blast radius.

## Why minimal usage descriptions matter

- Listing `NSCameraUsageDescription` when the app never accesses the camera misleads users about what the app does, and macOS may still prompt for the permission inappropriately.
- App Store reviewers reject apps that request permissions they don't use.
- The strings appear in System Settings → Privacy → Microphone (etc.). Make them descriptive ("X needs the microphone to transcribe voice notes" is better than "X needs microphone access").
