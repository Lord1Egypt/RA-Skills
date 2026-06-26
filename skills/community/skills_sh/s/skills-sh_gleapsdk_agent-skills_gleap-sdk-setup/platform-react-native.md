# React Native SDK

## Table of Contents
- [Installation](#installation)
- [Native Linking](#native-linking)
- [Initialization](#initialization)
- [Required Permissions](#required-permissions)
- [Common API Usage](#common-api-usage)

## Installation

```
npm install react-native-gleapsdk --save
```

React Native Expo is fully supported with the latest SDK.

## Native Linking

### iOS

```
cd ios && pod install
```

If errors occur, run `pod repo update` first.

### Android

Open Android Studio and sync the Gradle project.

For API level 30 projects, if build errors occur, add to the `react-native-gleapsdk/build.gradle`:

```gradle
dependencies {
    implementation "com.facebook.react:react-native:+"
    implementation group: 'io.gleap', name: 'gleap-android-sdk', version: 'LATEST_ANDROID_VERSION'
    implementation("androidx.appcompat:appcompat:1.3.0") { force = true }
    implementation("com.google.android.material:material:1.4.0") { force = true }
}
```

Replace `LATEST_ANDROID_VERSION` with the version from `get-latest-versions.sh`.

## Initialization

In `index.js` (call only once):

```javascript
import Gleap from 'react-native-gleapsdk';

Gleap.initialize("API_KEY");
```

## Required Permissions

### Android (`AndroidManifest.xml`)

Image attachments:
```xml
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
<uses-permission android:name="android.permission.READ_MEDIA_VISUAL_USER_SELECTED"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" />
```

Audio recordings:
```xml
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-feature android:name="android.hardware.audio.pro" android:required="false" />
<uses-feature android:name="android.hardware.microphone" android:required="false" />
```

### iOS (`Info.plist`)

```xml
<key>NSPhotoLibraryUsageDescription</key>
<string>Allow photo access for attachments</string>

<key>NSCameraUsageDescription</key>
<string>Allow camera access for screenshots</string>

<key>NSMicrophoneUsageDescription</key>
<string>Allow microphone access for audio feedback</string>
```

## Common API Usage

### Identify Users

```javascript
Gleap.identify("USER_ID", {
  name: "Franz",
  email: "franz@example.com",
  phone: "+1 (902) 123123",
  value: 199.95,
  plan: "Pro plan",
  companyId: "19382",
  companyName: "ACME inc.",
  customData: {
    role: "admin",
  },
});
```

With identity verification:
```javascript
Gleap.identifyWithUserHash("USER_ID", { name: "Franz", email: "franz@example.com" }, "GENERATED_USER_HASH");
```

Update contact (partial updates supported):
```javascript
Gleap.updateContact({ plan: "Enterprise" });
```

Clear identity on logout:
```javascript
Gleap.clearIdentity();
```

### Track Events

```javascript
Gleap.trackEvent("User signed in");

// With data:
Gleap.trackEvent("Purchase completed", {
  amount: 49.99,
  currency: "USD",
});
```

### Custom Data

```javascript
Gleap.attachCustomData({ environment: "staging", buildId: "abc123" });

// Incremental:
Gleap.setCustomData("key", "value");

// Remove:
Gleap.removeCustomData("key");

// Clear all:
Gleap.clearCustomData();
```

### Widget Control

```javascript
Gleap.open();
Gleap.close();
const isOpened = await Gleap.isOpened();
```
