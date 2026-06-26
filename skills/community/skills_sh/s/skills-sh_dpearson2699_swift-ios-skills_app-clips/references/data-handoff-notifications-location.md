# App Clip Data Handoff, Notifications, and Location

Use this when implementing App Group/full-app migration, keychain or Sign in with Apple handoff, ephemeral notifications, notification relaunch routing, or physical location confirmation.

## Contents

- [Data Migration to Full App](#data-migration-to-full-app)
- [Keychain Sharing](#keychain-sharing)
- [Sign in with Apple](#sign-in-with-apple)
- [Ephemeral Notifications](#ephemeral-notifications)
- [Location Confirmation](#location-confirmation)
- [Lifecycle and Ephemeral State](#lifecycle-and-ephemeral-state)

## Data Migration to Full App

When a user installs the full app, it replaces the App Clip. Use a **shared App Group container** for non-secret data the full app needs:

```swift
// In both targets: add App Groups capability with the same group ID

// App Clip — write non-secret data
func savePendingOrder(_ order: PendingOrder) throws {
    guard let containerURL = FileManager.default.containerURL(
        forSecurityApplicationGroupIdentifier: "group.com.example.myapp.shared"
    ) else { return }

    let data = try JSONEncoder().encode(order)
    let fileURL = containerURL.appendingPathComponent("pending-order.json")
    try data.write(to: fileURL)
}

// Full app — read migrated data
func loadPendingOrder() throws -> PendingOrder? {
    guard let containerURL = FileManager.default.containerURL(
        forSecurityApplicationGroupIdentifier: "group.com.example.myapp.shared"
    ) else { return nil }

    let fileURL = containerURL.appendingPathComponent("pending-order.json")
    guard FileManager.default.fileExists(atPath: fileURL.path) else { return nil }
    let data = try Data(contentsOf: fileURL)
    return try JSONDecoder().decode(PendingOrder.self, from: data)
}
```

### Shared UserDefaults

Use shared defaults for small, non-secret state such as identifiers, timestamps, feature choices, or pending-cart metadata:

```swift
let shared = UserDefaults(suiteName: "group.com.example.myapp.shared")
shared?.set(orderID, forKey: "pendingOrderID")
```

Any app or extension target provisioned with the same App Group entitlement can read and write the shared container and shared defaults suite. Treat App Group storage as a convenience handoff channel, not a trust boundary. Do not put passwords, refresh tokens, payment credentials, or other secrets in shared containers or shared defaults.

## Keychain Sharing

Starting in iOS 15.4, the full app can access keychain items created by its corresponding App Clip when the App Clip and full app have the correct association entitlements. This is one-way: the App Clip cannot read keychain items created by the full app. Use labels, service names, or account naming to distinguish App Clip-created items before migration.

## Sign in with Apple

Store the `ASAuthorizationAppleIDCredential.user` identifier in the shared container so the full app can verify the account without re-prompting unnecessarily:

```swift
let provider = ASAuthorizationAppleIDProvider()
provider.getCredentialState(forUserID: userID) { state, error in
    if state == .authorized {
        // Continue full-app account migration.
    }
}
```

## Ephemeral Notifications

App Clips can request ephemeral notification authorization by setting `NSAppClipRequestEphemeralUserNotification` in the App Clip target's `NSAppClip` `Info.plist` dictionary. The authorization can last up to 8 hours after each launch, but users can disable it from the App Clip card. Before scheduling, check `UNUserNotificationCenter` settings and require `authorizationStatus == .ephemeral`.

A notification tap relaunches the App Clip without the original invocation URL. For multi-experience App Clips, include a target content identifier so the App Clip can route after notification relaunch. Use a URL matching the relevant App Store Connect advanced App Clip experience, not an arbitrary opaque ID:

- Remote notifications: APNs `target-content-id`
- Local notifications: `UNNotificationContent.targetContentIdentifier`

## Location Confirmation

Use `APActivationPayload` to verify a user's physical location without requesting full location access. The confirmation region can have a radius up to 500 meters:

```swift
import AppClip
import CoreLocation

func verifyLocation(from activity: NSUserActivity) {
    guard let payload = activity.appClipActivationPayload else { return }

    let center = CLLocationCoordinate2D(latitude: 37.334722, longitude: -122.008889)
    // Apple allows a confirmation region radius up to 500 meters.
    let region = CLCircularRegion(center: center, radius: 100, identifier: "store-42")

    payload.confirmAcquired(in: region) { inRegion, error in
        if let error = error as? APActivationPayloadError {
            switch error.code {
            case .doesNotMatch:
                break
            case .disallowed:
                break
            @unknown default:
                break
            }
            return
        }

        if inRegion {
            routeToInStoreExperience()
        }
    }
}
```

Enable location confirmation in the App Clip target's `Info.plist`, not the full app's:

```xml
<key>NSAppClip</key>
<dict>
    <key>NSAppClipRequestLocationConfirmation</key>
    <true/>
</dict>
```

This is lightweight: the system confirms whether the invocation is within your registered physical region without granting continuous location access. The App Clip card discloses that the clip can verify location. Available iOS 14.0+.

## Lifecycle and Ephemeral State

- **No Home Screen icon** — App Clips appear in the App Library and recent apps.
- **Automatic removal** — the system may remove unused App Clips and their data after a limited, system-determined period.
- **No persistent state guarantee** — treat App Clip local storage as ephemeral; migrate important non-secret data to the shared container or a server.
- **Relaunching** — returning from the App Library uses the last invocation URL; returning from the App Switcher launches without an invocation URL, so restore saved state.
- **Location access** — use when-in-use authorization only; App Clip location authorization is short-lived and resets.
