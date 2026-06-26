# Technical Requirements — Complete Reference

**Official URLs:**
- https://developer.apple.com/news/upcoming-requirements/
- https://developer.apple.com/support/third-party-SDK-requirements/

This document covers all technical requirements for App Store submission.

---

## Current SDK Requirements

### As of April 2025

| Requirement | Details |
|-------------|---------|
| **Xcode** | Version 16 or later |
| **iOS SDK** | iOS 18 |
| **iPadOS SDK** | iPadOS 18 |
| **tvOS SDK** | tvOS 18 |
| **visionOS SDK** | visionOS 2 |
| **watchOS SDK** | watchOS 11 |

### Verification

Check your build settings:
```bash
xcodebuild -showBuildSettings | grep -E "SDK|DEPLOYMENT"
```

Required in Xcode project:
- `IPHONEOS_DEPLOYMENT_TARGET` = Appropriate minimum iOS version
- Built with latest Xcode (16+)
- Using iOS 18 SDK

---

## Privacy Manifests (Required since May 2024)

### File Location

Create `PrivacyInfo.xcprivacy` at your app bundle root.

### Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyTracking</key>
    <false/>

    <key>NSPrivacyTrackingDomains</key>
    <array>
        <!-- Domains used for tracking, if NSPrivacyTracking is true -->
    </array>

    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <!-- All data types collected -->
    </array>

    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <!-- Required reason APIs used -->
    </array>
</dict>
</plist>
```

### Required Reason APIs

These APIs require justification in your privacy manifest:

| API Category | Examples | Reason Codes |
|--------------|----------|--------------|
| **File timestamp** | `getattrlist()`, `stat()` | DDA9.1, C617.1, etc. |
| **System boot time** | `sysctl()` KERN_BOOTTIME | 35F9.1, 8FFB.1, etc. |
| **Disk space** | `statfs()`, `statvfs()` | 85F4.1, E174.1, etc. |
| **User defaults** | `UserDefaults` | CA92.1, 1C8F.1, etc. |
| **Active keyboard** | `UITextInputMode` | 54BD.1, etc. |

### Example: User Defaults Reason

```xml
<dict>
    <key>NSPrivacyAccessedAPIType</key>
    <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
    <key>NSPrivacyAccessedAPITypeReasons</key>
    <array>
        <string>CA92.1</string>
    </array>
</dict>
```

**CA92.1:** Access user defaults to read and write data accessible only within the app.

---

## Third-Party SDK Requirements

### SDKs Requiring Privacy Manifests

Apple maintains a list of commonly used SDKs that must include privacy manifests:

**Analytics:**
- Firebase Analytics
- Google Analytics
- Amplitude
- Mixpanel
- Segment

**Advertising:**
- Google Mobile Ads SDK (AdMob)
- Facebook SDK
- AppLovin
- Unity Ads
- IronSource

**Others:**
- Firebase Crashlytics
- Sentry
- OneSignal
- Branch
- AppsFlyer

### Verification

Check if your SDKs are compliant:
1. Update to latest SDK versions
2. Verify SDK includes PrivacyInfo.xcprivacy
3. Check SDK documentation for compliance status

### What If SDK Not Compliant?

| Option | Action |
|--------|--------|
| **Update SDK** | Use latest version with manifest |
| **Replace SDK** | Find compliant alternative |
| **Remove SDK** | If not essential |
| **Contact vendor** | Request compliance update |

---

## SDK Signatures

### Requirement

All third-party SDKs must be signed.

### Verification

Xcode 15+ automatically verifies SDK signatures. Check in:
- Xcode → Project → Signing & Capabilities
- Build logs for signature validation

### Adding Signatures

For SDKs without signatures:
1. Contact SDK vendor for signed version
2. Use package managers (SPM, CocoaPods) with checksums
3. Manually verify and sign using `codesign`

---

## Performance Requirements

### Prohibited Activities

| Activity | Guideline | Consequence |
|----------|-----------|-------------|
| **Cryptocurrency mining** | 2.4.2 | Rejection |
| **Excessive battery drain** | 2.4 | Rejection |
| **Excessive heat generation** | 2.4 | Rejection |
| **Excessive storage writes** | 2.4 | Rejection |
| **Unrelated background processes** | 2.4 | Rejection |

### Performance Standards

| Metric | Requirement |
|--------|-------------|
| **Launch time** | <5 seconds warm launch |
| **Responsiveness** | No UI freezes |
| **Memory usage** | Reasonable for device |
| **Battery impact** | Minimal |
| **Network efficiency** | Reasonable data usage |

### Testing Performance

Use Xcode Instruments:
- **Time Profiler** — CPU usage
- **Allocations** — Memory usage
- **Energy Log** — Battery impact
- **Network** — Data usage
- **Core Animation** — UI performance

---

## Device Compatibility

### iPhone/iPad Requirements

| Rule | Details |
|------|---------|
| **Universal** | iPhone apps should run on iPad |
| **Orientation** | Support declared orientations |
| **Size classes** | Adapt to all screen sizes |
| **Safe areas** | Respect notch/Dynamic Island |

### Minimum iOS Version

| Consideration | Guidance |
|---------------|----------|
| **User reach** | Lower minimum = more users |
| **Feature availability** | Higher minimum = newer APIs |
| **Testing burden** | Each version needs testing |
| **Typical minimum** | iOS 15-17 for most apps |

### Device Capabilities

Declare required capabilities in Info.plist:
```xml
<key>UIRequiredDeviceCapabilities</key>
<array>
    <string>arm64</string>
    <string>metal</string>
</array>
```

Common capabilities:
- `arm64` — 64-bit processor
- `metal` — Metal graphics
- `nfc` — NFC support
- `arkit` — ARKit support
- `gamekit` — Game Center

---

## Background Modes

### Allowed Background Modes

| Mode | Use Case | Key |
|------|----------|-----|
| **Audio** | Music, podcasts | `audio` |
| **Location** | Navigation | `location` |
| **VoIP** | Voice calls | `voip` |
| **External accessory** | Bluetooth LE | `external-accessory` |
| **Bluetooth LE** | BLE accessories | `bluetooth-central`, `bluetooth-peripheral` |
| **Background fetch** | Content updates | `fetch` |
| **Remote notifications** | Silent push | `remote-notification` |
| **Processing** | Long tasks | `processing` |

### Requirements

- Only request modes you actually use
- Must provide clear user benefit
- Excessive background activity = rejection
- Battery impact must be reasonable

---

## App Size

### Limits

| Limit | Details |
|-------|---------|
| **Cellular download** | 200 MB (users can bypass) |
| **App Store package** | 4 GB maximum |
| **On-device** | Varies by device storage |

### Size Optimization

| Technique | Impact |
|-----------|--------|
| **Asset catalogs** | Automatic app thinning |
| **On-demand resources** | Download content as needed |
| **Image optimization** | Compress images |
| **Remove unused** | Delete unused assets |
| **Symbol stripping** | Enable in release builds |

---

## Code Signing

### Requirements

| Requirement | Details |
|-------------|---------|
| **Valid certificate** | Active Apple Developer Program |
| **Provisioning profile** | Matches Bundle ID |
| **Entitlements** | Only request needed entitlements |
| **Hardened runtime** | Required for macOS |

### Common Issues

| Issue | Fix |
|-------|-----|
| **Expired certificate** | Renew in Developer Portal |
| **Wrong profile** | Select correct provisioning profile |
| **Bundle ID mismatch** | Match App Store Connect |
| **Missing entitlements** | Add required entitlements |

---

## API Usage

### Deprecated APIs

| Action | Consequence |
|--------|-------------|
| **Using deprecated** | Warning now, rejection later |
| **Private APIs** | Immediate rejection |
| **Undocumented APIs** | Rejection |

Check for deprecated APIs:
```bash
xcodebuild -showBuildWarnings
```

### Private API Detection

Apple scans for private API usage:
- Static analysis of binary
- Runtime behavior analysis
- Symbol table inspection

---

## Archive and Upload

### Pre-Upload Checklist

| Check | Details |
|-------|---------|
| **Build configuration** | Release, not Debug |
| **Architecture** | arm64 (remove simulator slices) |
| **Symbols** | Upload dSYM files |
| **Validation** | Run Xcode validation |

### Xcode Validation

Before upload, validate archive:
1. Product → Archive
2. Distribute App → App Store Connect
3. Click Validate App
4. Review and fix any issues

### Common Validation Errors

| Error | Fix |
|-------|-----|
| **Missing icon** | Add 1024×1024 icon |
| **Invalid binary** | Remove simulator architectures |
| **Signing issues** | Check certificate/profile |
| **Info.plist missing keys** | Add required keys |

---

## Info.plist Requirements

### Required Keys

| Key | Purpose |
|-----|---------|
| **CFBundleDisplayName** | App name on home screen |
| **CFBundleIdentifier** | Bundle ID |
| **CFBundleVersion** | Build number |
| **CFBundleShortVersionString** | Version number |
| **UILaunchStoryboardName** | Launch screen |
| **UISupportedInterfaceOrientations** | Supported orientations |

### Permission Descriptions

All permission requests require usage descriptions:

| Permission | Key |
|------------|-----|
| Camera | `NSCameraUsageDescription` |
| Microphone | `NSMicrophoneUsageDescription` |
| Photos | `NSPhotoLibraryUsageDescription` |
| Location (when in use) | `NSLocationWhenInUseUsageDescription` |
| Location (always) | `NSLocationAlwaysUsageDescription` |
| Contacts | `NSContactsUsageDescription` |
| Calendars | `NSCalendarsUsageDescription` |
| Reminders | `NSRemindersUsageDescription` |
| Health | `NSHealthShareUsageDescription` |
| Bluetooth | `NSBluetoothAlwaysUsageDescription` |
| Motion | `NSMotionUsageDescription` |
| FaceID | `NSFaceIDUsageDescription` |
| Speech Recognition | `NSSpeechRecognitionUsageDescription` |
| Tracking | `NSUserTrackingUsageDescription` |

---

## TestFlight Requirements

### Before TestFlight

| Requirement | Details |
|-------------|---------|
| **Beta App Description** | Describe what testers should focus on |
| **Contact Information** | Valid contact for testers |
| **Privacy Policy** | Required for TestFlight |
| **Export Compliance** | Answer encryption questions |

### TestFlight vs App Store

| Aspect | TestFlight | App Store |
|--------|------------|-----------|
| Review time | 24-48 hours | Same |
| Review depth | Lighter | Full |
| Billing | Not charged | Charged |
| Distribution | Invited testers | Public |

---

## Export Compliance

### Encryption Questions

When uploading, answer:
1. Does your app use encryption?
2. Does it qualify for exemptions?
3. Do you have required documentation?

### Common Exemptions

| Exemption | Applies To |
|-----------|------------|
| **Standard encryption** | HTTPS for networking |
| **Authentication only** | Password hashing |
| **Ancillary** | Encryption not primary function |

For standard HTTPS:
- Answer YES to using encryption
- Qualify for exemption
- No additional documentation needed

---

## Technical Checklist

### Before Submission

#### Build Requirements
- [ ] Built with Xcode 16+
- [ ] Using iOS 18 SDK
- [ ] Release configuration
- [ ] Symbols uploaded (dSYM)
- [ ] arm64 architecture only

#### Privacy
- [ ] PrivacyInfo.xcprivacy included
- [ ] Required reason APIs declared
- [ ] Third-party SDKs have manifests
- [ ] SDKs are signed
- [ ] All permission descriptions

#### Performance
- [ ] No crashes on supported devices
- [ ] Acceptable launch time
- [ ] Reasonable battery usage
- [ ] No memory leaks
- [ ] Works offline (if applicable)

#### Compatibility
- [ ] Tested on oldest supported iOS
- [ ] Tested on current iOS
- [ ] Tested on multiple device sizes
- [ ] iPad compatibility (if applicable)
- [ ] Dark Mode support

#### Code Quality
- [ ] No deprecated API warnings
- [ ] No private APIs
- [ ] All validation checks pass
- [ ] Export compliance answered

---

*Technical requirements evolve. Always verify against current Apple documentation.*
