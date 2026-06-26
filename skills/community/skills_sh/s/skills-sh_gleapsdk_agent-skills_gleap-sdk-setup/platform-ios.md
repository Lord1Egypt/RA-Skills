# iOS SDK

## Table of Contents
- [Installation](#installation)
- [Import](#import)
- [Initialization](#initialization)
- [Required Permissions](#required-permissions)
- [Common API Usage](#common-api-usage)

## Installation

### Option A: Swift Package Manager (recommended)

In Xcode: **File > Add Packages...** and enter:

```
https://github.com/GleapSDK/Gleap-iOS-SDK
```

Select the Gleap package and click **Add Package**.

### Option B: CocoaPods

Add to `Podfile`:

```ruby
pod 'Gleap', '>= LATEST_IOS_VERSION'
```

Replace `LATEST_IOS_VERSION` with the version from `get-latest-versions.sh`.

Then run:

```
pod install
```

Use the generated `.xcworkspace` file for all further development.

## Import

**Swift:**
```swift
import Gleap
```

**Objective-C (SPM):**
```objectivec
@import Gleap;
```

**Objective-C (CocoaPods):**
```objectivec
#import <Gleap/Gleap.h>
```

## Initialization

### UIKit (AppDelegate)

Add to `applicationDidFinishLaunchingWithOptions`:

**Swift:**
```swift
Gleap.initialize(withToken: "API_KEY")
```

**Objective-C:**
```objectivec
[Gleap initializeWithToken: @"API_KEY"];
```

### SwiftUI

Add to the `App` struct's `init()`:

```swift
init() {
    Gleap.initialize(withToken: "API_KEY")
}
```

## Required Permissions

Add to `Info.plist` for image/camera attachments:

```xml
<key>NSPhotoLibraryUsageDescription</key>
<string>Allow photo access for attachments</string>

<key>NSCameraUsageDescription</key>
<string>Allow camera access for screenshots</string>
```

For audio recording:

```xml
<key>NSMicrophoneUsageDescription</key>
<string>Allow microphone access for audio feedback</string>
```

## Common API Usage

### Identify Users

```swift
let userProperty = GleapUserProperty()
userProperty.name = "Franz"
userProperty.email = "franz@example.com"
userProperty.phone = "+1 (902) 123123"
userProperty.value = 199.95
userProperty.plan = "Pro plan"
userProperty.companyId = "29883"
userProperty.companyName = "ACME inc."
userProperty.customData = ["role": "admin"]

Gleap.identifyContact("USER_ID", andData: userProperty)
```

Update contact (partial updates supported):
```swift
let props = GleapUserProperty()
props.plan = "Enterprise"
Gleap.updateContact(props)
```

Clear identity on logout:
```swift
Gleap.clearIdentity()
```

### Track Events

```swift
Gleap.trackEvent("User signed in")

// With data:
Gleap.trackEvent("Purchase completed", withData: ["amount": 49.99, "currency": "USD"])
```

### Custom Data

```swift
Gleap.attachCustomData(["environment": "staging", "buildId": "abc123"])

// Incremental:
Gleap.setCustomData("value", forKey: "key")

// Remove:
Gleap.removeCustomData(forKey: "key")

// Clear all:
Gleap.clearCustomData()
```

### Widget Control

```swift
Gleap.open()
Gleap.close()
Gleap.isOpened()
```
