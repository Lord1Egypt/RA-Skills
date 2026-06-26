# Privacy Requirements — Complete Reference

**Official URL:** https://developer.apple.com/app-store/user-privacy-and-data-use/

Privacy violations are the **#1 cause of App Store rejections**. This document covers all privacy requirements comprehensively.

---

## App Tracking Transparency (ATT)

**Required since iOS 14.5**

### When ATT Permission is REQUIRED

You **must** request permission via ATT if your app:

| Scenario | Example |
|----------|---------|
| **Targeted advertising** | Displaying ads based on data from other companies' apps/websites |
| **Data broker sharing** | Sharing device location or email lists with data brokers |
| **Ad network sharing** | Sharing advertising identifiers with ad networks for retargeting |
| **SDK data combining** | Using SDKs that combine user data across apps |
| **Fingerprinting** | Using device signals to uniquely identify users |

### When ATT is NOT Required

You **don't need** ATT permission if:

| Scenario | Details |
|----------|---------|
| **On-device only** | Data is linked only on-device and never sent off device |
| **Fraud prevention** | Data broker used solely for fraud detection/prevention |
| **Credit reporting** | Consumer reporting agency for credit purposes only |
| **First-party analytics** | Analytics without cross-site/cross-app linking |

### ATT Implementation Requirements

```swift
// Request permission
import AppTrackingTransparency

ATTrackingManager.requestTrackingAuthorization { status in
    switch status {
    case .authorized:
        // Tracking allowed
    case .denied, .restricted, .notDetermined:
        // Tracking not allowed
    }
}
```

**Critical Rules:**
- Cannot gate features on tracking consent
- Cannot incentivize users to allow tracking
- Can explain why you want permission (transparently)
- Cannot use fingerprinting as alternative
- Must respect user's choice in ATT prompt
- Must re-request only when status is `.notDetermined`

---

## Privacy Labels (App Privacy Details)

**Required for all app submissions**

### Data Categories

| Category | Data Types |
|----------|------------|
| **Contact Info** | Name, email address, phone number, physical address |
| **Health & Fitness** | Health data, fitness data |
| **Financial Info** | Payment info, credit info, salary, assets |
| **Location** | Precise location, coarse location |
| **Sensitive Info** | Racial/ethnic data, sexual orientation, political opinions, religious beliefs |
| **Contacts** | Contacts (address book) |
| **User Content** | Emails/messages, photos/videos, audio, gameplay content, customer support |
| **Browsing History** | Web browsing history |
| **Search History** | Search history in app |
| **Identifiers** | User ID, device ID, IDFA |
| **Purchases** | Purchase history |
| **Usage Data** | Product interaction, advertising data |
| **Diagnostics** | Crash data, performance data |

### Data Use Categories

For each data type, you must disclose:

| Use | Description |
|-----|-------------|
| **Third-Party Advertising** | Displaying ads or sharing with ad networks |
| **Developer's Advertising** | Displaying ads from your own ad network |
| **Analytics** | Analyzing user behavior, app performance |
| **Product Personalization** | Customizing what user sees |
| **App Functionality** | Core app features |
| **Other Purposes** | Any other use |

### Linking and Tracking

| Question | Meaning |
|----------|---------|
| **Linked to User** | Data is connected to user identity |
| **Used to Track User** | Data is used for cross-app/cross-site tracking |

### Accuracy Requirements

**Your privacy labels MUST match your actual data practices:**
- Review all code paths for data collection
- Review all third-party SDKs
- Update labels with every app update
- Inaccurate labels = rejection

---

## Privacy Manifests

**Required since May 2024**

### File: PrivacyInfo.xcprivacy

Every app must include a privacy manifest file at the bundle root.

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
        <string>tracking.example.com</string>
    </array>

    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <dict>
            <key>NSPrivacyCollectedDataType</key>
            <string>NSPrivacyCollectedDataTypeEmailAddress</string>
            <key>NSPrivacyCollectedDataTypeLinked</key>
            <true/>
            <key>NSPrivacyCollectedDataTypeTracking</key>
            <false/>
            <key>NSPrivacyCollectedDataTypePurposes</key>
            <array>
                <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
            </array>
        </dict>
    </array>

    <key>NSPrivacyAccessedAPITypes</key>
    <array>
        <dict>
            <key>NSPrivacyAccessedAPIType</key>
            <string>NSPrivacyAccessedAPICategoryUserDefaults</string>
            <key>NSPrivacyAccessedAPITypeReasons</key>
            <array>
                <string>CA92.1</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

### Required Reason APIs

These APIs require justification in your privacy manifest:

| API Category | Examples | Common Reasons |
|--------------|----------|----------------|
| **File timestamp APIs** | `getattrlist()`, `stat()` | Determine file modification dates |
| **System boot time APIs** | `sysctl()` with `KERN_BOOTTIME` | Calculate elapsed time |
| **Disk space APIs** | `statfs()`, `statvfs()` | Check available storage |
| **User defaults APIs** | `UserDefaults` | Store app preferences |
| **Active keyboard APIs** | `UITextInputMode` | Determine input language |

### Third-Party SDK Requirements

All third-party SDKs must:
1. Include their own privacy manifests
2. Be signed with valid signatures
3. Declare their data collection and API usage

**Apple maintains a list of SDKs requiring privacy manifests:**
https://developer.apple.com/support/third-party-SDK-requirements/

---

## Privacy Policy Requirements

**Required for ALL apps (Guideline 5.1.1)**

### Must Include

| Element | Requirement |
|---------|-------------|
| **Data identification** | Clearly identify what data is collected |
| **Collection method** | Describe how data is collected |
| **All uses** | Explain all uses of the data |
| **Third-party sharing** | Confirm third parties provide equal protection |
| **Retention** | Explain data retention/deletion policies |
| **User rights** | Describe how to revoke consent and delete data |
| **Contact info** | Provide way to contact about privacy concerns |

### Best Practices

- Write in plain language (not legalese)
- Keep updated with app changes
- Make easily accessible from app and App Store listing
- Include effective date
- Describe security measures
- Cover all platforms (iOS, web, etc.)

### Common Privacy Policy Failures

| Issue | Solution |
|-------|----------|
| Too vague | Specify exact data types |
| Missing sections | Cover all required elements |
| Outdated | Update with every release |
| Hard to find | Link prominently in app and settings |
| Legal jargon | Simplify language |

---

## Data Collection Categories (Complete List)

### NSPrivacyCollectedDataType Values

```
NSPrivacyCollectedDataTypeName
NSPrivacyCollectedDataTypeEmailAddress
NSPrivacyCollectedDataTypePhoneNumber
NSPrivacyCollectedDataTypePhysicalAddress
NSPrivacyCollectedDataTypeOtherUserContactInfo
NSPrivacyCollectedDataTypeHealth
NSPrivacyCollectedDataTypeFitness
NSPrivacyCollectedDataTypePaymentInfo
NSPrivacyCollectedDataTypeCreditInfo
NSPrivacyCollectedDataTypeOtherFinancialInfo
NSPrivacyCollectedDataTypePreciseLocation
NSPrivacyCollectedDataTypeCoarseLocation
NSPrivacyCollectedDataTypeSensitiveInfo
NSPrivacyCollectedDataTypeContacts
NSPrivacyCollectedDataTypeEmails
NSPrivacyCollectedDataTypeTextMessages
NSPrivacyCollectedDataTypePhotos
NSPrivacyCollectedDataTypeVideos
NSPrivacyCollectedDataTypeAudioData
NSPrivacyCollectedDataTypeGameplayContent
NSPrivacyCollectedDataTypeCustomerSupport
NSPrivacyCollectedDataTypeOtherUserContent
NSPrivacyCollectedDataTypeBrowsingHistory
NSPrivacyCollectedDataTypeSearchHistory
NSPrivacyCollectedDataTypeUserID
NSPrivacyCollectedDataTypeDeviceID
NSPrivacyCollectedDataTypePurchaseHistory
NSPrivacyCollectedDataTypeProductInteraction
NSPrivacyCollectedDataTypeAdvertisingData
NSPrivacyCollectedDataTypeOtherUsageData
NSPrivacyCollectedDataTypeCrashData
NSPrivacyCollectedDataTypePerformanceData
NSPrivacyCollectedDataTypeOtherDiagnosticData
NSPrivacyCollectedDataTypeEnvironmentScanning
NSPrivacyCollectedDataTypeHands
NSPrivacyCollectedDataTypeHead
```

### Purpose Values

```
NSPrivacyCollectedDataTypePurposeThirdPartyAdvertising
NSPrivacyCollectedDataTypePurposeDeveloperAdvertising
NSPrivacyCollectedDataTypePurposeAnalytics
NSPrivacyCollectedDataTypePurposeProductPersonalization
NSPrivacyCollectedDataTypePurposeAppFunctionality
NSPrivacyCollectedDataTypePurposeOther
```

---

## Permission Requests

### System Permissions

| Permission | Key | When to Request |
|------------|-----|-----------------|
| **Camera** | `NSCameraUsageDescription` | When user taps camera feature |
| **Microphone** | `NSMicrophoneUsageDescription` | When user needs audio input |
| **Location** | `NSLocationWhenInUseUsageDescription` | When app needs location |
| **Location (Always)** | `NSLocationAlwaysUsageDescription` | Only if truly needed |
| **Photos** | `NSPhotoLibraryUsageDescription` | When user accesses photos |
| **Contacts** | `NSContactsUsageDescription` | When user shares contacts |
| **Calendars** | `NSCalendarsUsageDescription` | When user accesses calendar |
| **Reminders** | `NSRemindersUsageDescription` | When user accesses reminders |
| **Health** | `NSHealthShareUsageDescription` | When reading health data |
| **Bluetooth** | `NSBluetoothAlwaysUsageDescription` | When using Bluetooth |
| **Motion** | `NSMotionUsageDescription` | When using accelerometer/gyroscope |

### Request Best Practices

- Request in context (when user performs related action)
- Explain why permission is needed (before system prompt)
- Provide alternative if permission denied
- Don't request all permissions at launch
- Re-request gracefully if previously denied

---

## Data Security Requirements (Guideline 1.6)

### Required Measures

| Requirement | Implementation |
|-------------|----------------|
| **Secure transmission** | HTTPS for all network calls |
| **Secure storage** | Keychain for sensitive data |
| **Encryption** | Encrypt sensitive local data |
| **Access control** | Prevent unauthorized access |
| **Session management** | Secure token handling |

### Common Security Issues

| Issue | Fix |
|-------|-----|
| HTTP connections | Switch to HTTPS |
| Hardcoded secrets | Use environment variables or Keychain |
| Unencrypted storage | Use encrypted Core Data or Keychain |
| Logging sensitive data | Remove sensitive data from logs |

---

## Privacy Checklist Before Submission

### Privacy Manifest
- [ ] PrivacyInfo.xcprivacy file exists at bundle root
- [ ] All collected data types declared
- [ ] All required reason APIs justified
- [ ] Tracking domains listed (if tracking)
- [ ] Third-party SDK manifests included

### Privacy Labels
- [ ] All data types identified in App Store Connect
- [ ] Uses accurately described
- [ ] Linked to user correctly marked
- [ ] Used to track correctly marked
- [ ] Labels match actual app behavior

### ATT
- [ ] ATT prompt implemented (if tracking)
- [ ] User choice respected
- [ ] No tracking before consent
- [ ] Fallback if user declines

### Privacy Policy
- [ ] Link in App Store listing
- [ ] Link in app (Settings or About)
- [ ] Covers all data collection
- [ ] Explains user rights
- [ ] Contact information included

### Permissions
- [ ] All permission strings in Info.plist
- [ ] Strings explain why permission needed
- [ ] Permissions requested in context
- [ ] Graceful handling if denied

---

*Privacy requirements evolve. Always verify against current Apple documentation.*
