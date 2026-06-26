# Android SDK

## Table of Contents
- [Installation](#installation)
- [Initialization](#initialization)
- [Required Permissions](#required-permissions)
- [Common API Usage](#common-api-usage)

## Installation

Add to `build.gradle` (Module: app) dependencies:

```gradle
implementation group: 'io.gleap', name: 'gleap-android-sdk', version: 'LATEST_ANDROID_VERSION'
```

Replace `LATEST_ANDROID_VERSION` with the version from `get-latest-versions.sh`.

Sync Gradle after adding the dependency.

## Initialization

In your main Activity's `onCreate`:

```java
import io.gleap.Gleap;

@Override
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    Gleap.initialize("API_KEY", this);
}
```

## Required Permissions

Add to `AndroidManifest.xml`:

### Image attachments

```xml
<uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />
<uses-permission android:name="android.permission.READ_MEDIA_VISUAL_USER_SELECTED"/>
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" />
```

### Audio recordings

```xml
<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-feature android:name="android.hardware.audio.pro" android:required="false" />
<uses-feature android:name="android.hardware.microphone" android:required="false" />
```

### Video calls

```xml
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.INTERNET" />
<uses-feature android:name="android.hardware.audio.pro" android:required="false" />
<uses-feature android:name="android.hardware.microphone" android:required="false" />
<uses-feature android:name="android.hardware.camera" android:required="false" />
```

## Common API Usage

### Identify Users

```java
GleapSessionProperties sessionProperties = new GleapSessionProperties();
sessionProperties.setName("Franz");
sessionProperties.setEmail("franz@example.com");
sessionProperties.setPhone("+1 (902) 123123");
sessionProperties.setValue(199.95);
sessionProperties.setPlan("Pro plan");
sessionProperties.setCompanyId("29883");
sessionProperties.setCompanyName("ACME inc.");

JSONObject customData = new JSONObject();
customData.put("role", "admin");
sessionProperties.setCustomData(customData);

Gleap.getInstance().identifyContact("USER_ID", sessionProperties);
```

Update contact (partial updates supported):
```java
GleapSessionProperties props = new GleapSessionProperties();
props.setPlan("Enterprise");
Gleap.getInstance().updateContact(props);
```

Clear identity on logout:
```java
Gleap.getInstance().clearIdentity();
```

### Track Events

```java
Gleap.getInstance().trackEvent("User signed in");

// With data:
JSONObject data = new JSONObject();
data.put("amount", 49.99);
data.put("currency", "USD");
Gleap.getInstance().trackEvent("Purchase completed", data);
```

### Custom Data

```java
Gleap.getInstance().setCustomData("value", "key");

// Attach all at once:
JSONObject customData = new JSONObject();
customData.put("environment", "staging");
Gleap.getInstance().attachCustomData(customData);

// Remove:
Gleap.getInstance().removeCustomDataForKey("key");

// Clear all:
Gleap.getInstance().clearCustomData();
```

### Widget Control

```java
Gleap.getInstance().open();
Gleap.getInstance().close();
Gleap.getInstance().isOpened();
```
