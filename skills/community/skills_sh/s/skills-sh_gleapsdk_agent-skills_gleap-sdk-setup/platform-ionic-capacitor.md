# Ionic / Capacitor SDK

## Table of Contents
- [Installation](#installation)
- [Initialization](#initialization)
- [Required Permissions](#required-permissions)
- [Common API Usage](#common-api-usage)

## Installation

Install based on your Capacitor version:

### Capacitor v5+

```
npm install capacitor-gleap-plugin
```

### Capacitor v4

```
npm install GleapSDK/Capacitor-SDK#capacitor-v4 --save
```

### Capacitor v3

```
npm install capacitor-gleap-plugin@8.2.3
```

### Sync (all versions)

```
npx cap sync
```

## Initialization

In your `index.js`, `index.tsx`, or main component (call only once):

```typescript
import { Gleap } from 'capacitor-gleap-plugin';

Gleap.initialize({ token: "API_KEY" });
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

The Ionic/Capacitor SDK uses the same JavaScript-style API as the web SDK.

### Identify Users

```typescript
import { Gleap } from 'capacitor-gleap-plugin';

Gleap.identify({
  userId: "USER_ID",
  userProperties: {
    name: "Franz",
    email: "franz@example.com",
    plan: "Pro plan",
    companyName: "ACME inc.",
  },
});
```

Update contact:
```typescript
Gleap.updateContact({ userProperties: { plan: "Enterprise" } });
```

Clear identity on logout:
```typescript
Gleap.clearIdentity();
```

### Track Events

```typescript
Gleap.trackEvent({ name: "User signed in" });

// With data:
Gleap.trackEvent({ name: "Purchase completed", data: { amount: 49.99 } });
```

### Custom Data

```typescript
Gleap.attachCustomData({ data: { environment: "staging" } });
Gleap.setCustomData({ key: "key", value: "value" });
Gleap.removeCustomData({ key: "key" });
Gleap.clearCustomData();
```

### Widget Control

```typescript
Gleap.open();
Gleap.close();
const { isOpened } = await Gleap.isOpened();
```
