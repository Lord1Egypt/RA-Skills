# Flutter SDK

## Table of Contents
- [Installation](#installation)
- [Platform Setup](#platform-setup)
- [Initialization](#initialization)
- [Required Permissions](#required-permissions)
- [Common API Usage](#common-api-usage)

## Installation

```
flutter pub add gleap_sdk
```

### Flutter v2 (< v3)

Add to `pubspec.yaml`:

```yaml
dependencies:
  gleap_sdk:
    git:
      url: https://github.com/GleapSDK/Flutter-SDK.git
      ref: flutter-v2
```

## Platform Setup

### iOS

```
cd ios && pod install
```

### Android

If version conflict occurs, add to `AndroidManifest.xml`:

```xml
<manifest ... xmlns:tools="http://schemas.android.com/tools">
  <uses-sdk android:minSdkVersion="21"
    tools:overrideLibrary="io.gleap.gleap_sdk"/>
  <application ... tools:overrideLibrary="io.gleap.gleap_sdk">
```

Do NOT set `android:hardwareAccelerated="false"` at the application level.

### Web

Add as the first element in the `<head>` of `web/index.html`:

```html
<script>
!function(){if(!(window.Gleap=window.Gleap||[]).invoked){window.GleapActions=[];var e=new Proxy({invoked:!0},{get:function(e,n){return"invoked"===n?e.invoked:function(){var e=Array.prototype.slice.call(arguments);window.GleapActions.push({e:n,a:e})}},set:function(e,n,t){return e[n]=t,!0}});window.Gleap=e;var n=document.getElementsByTagName("head")[0],t=document.createElement("script");t.type="text/javascript",t.async=!0,t.src="https://sdk.gleap.io/latest/index.js",n.appendChild(t)}}();
</script>
```

Then run `flutter clean && flutter pub get`.

## Initialization

In `main.dart`, ensure the binding is initialized first:

```dart
import 'package:gleap_sdk/gleap_sdk.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  Gleap.initialize(token: 'API_KEY');
  runApp(MyApp());
}
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

```dart
Gleap.identify(
  userId: 'USER_ID',
  userProperties: GleapUserProperty(
    name: 'Franz',
    email: 'franz@example.com',
    phone: '+1 (902) 123123',
    companyName: 'ACME inc.',
    companyId: '19283',
    plan: 'Pro plan',
    value: 199.95,
    customData: <String, dynamic>{
      'role': 'admin',
    },
  ),
);
```

With identity verification:
```dart
Gleap.identify(
  userId: 'USER_ID',
  userProperties: GleapUserProperty(name: 'Franz', email: 'franz@example.com'),
  userHash: 'GENERATED_USER_HASH',
);
```

Update contact (partial updates supported):
```dart
Gleap.updateContact(
  userProperties: GleapUserProperty(plan: 'Enterprise'),
);
```

Clear identity on logout:
```dart
Gleap.clearIdentity();
```

### Track Events

```dart
Gleap.trackEvent(name: 'User signed in');

// With data:
Gleap.trackEvent(
  name: 'Purchase completed',
  data: <String, dynamic>{'amount': 49.99, 'currency': 'USD'},
);
```

### Custom Data

```dart
Gleap.attachCustomData(customData: <String, dynamic>{'environment': 'staging'});

// Incremental:
Gleap.setCustomData(key: 'key', value: 'value');

// Remove:
Gleap.removeCustomDataForKey(key: 'key');

// Clear all:
Gleap.clearCustomData();
```

### Widget Control

```dart
Gleap.open();
Gleap.close();
Gleap.isOpened();
```
