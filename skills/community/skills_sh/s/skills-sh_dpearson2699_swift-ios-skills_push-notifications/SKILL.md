---
name: push-notifications
description: "Implement, review, or debug push notifications in iOS/macOS apps — local notifications, remote (APNs) notifications, rich notifications, notification actions, silent pushes, and notification service/content extensions. Use when working with UNUserNotificationCenter, registering for remote notifications, handling notification payloads, setting up notification categories and actions, creating rich notification content, or debugging notification delivery. Also use when working with alerts, badges, sounds, background pushes, or user notification permissions in Swift apps."
---

# Push Notifications

Implement, review, and debug local and remote notifications on iOS/macOS using `UserNotifications` and APNs. Covers permission flow, token registration, payload structure, foreground handling, notification actions, grouping, and rich notifications. Targets iOS 26+ with Swift 6.3, backward-compatible to iOS 16 unless noted.

Keep adjacent domains separate: Live Activity `content-state` payloads belong in `activitykit`; PushKit/VoIP call pushes belong in `callkit`; App Clip ephemeral notification setup belongs in `app-clips`; long-running or scheduled background work after a silent push belongs in `background-processing`.

## Contents

- [Correction Reviews](#correction-reviews)
- [Permission Flow](#permission-flow)
- [APNs Registration](#apns-registration)
- [Local Notifications](#local-notifications)
- [Remote Notification Payload](#remote-notification-payload)
- [Notification Handling](#notification-handling)
- [Notification Actions and Categories](#notification-actions-and-categories)
- [Notification Grouping](#notification-grouping)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Correction Reviews

When reviewing flawed notification proposals, explicitly name the violated contract. APNs token reviews must say token registration is independent from alert authorization, upload on every `didRegister` callback, avoid local-cache-as-truth logic, never assume token length, and treat Simulator registration failure as expected while noting `.apns` files or `simctl push` can simulate delivery. Background-push reviews must say `content-available` only, `apns-push-type: background`, `apns-priority: 5`, Remote notifications background mode, low priority, throttled, not guaranteed, not every few minutes, and bounded `didReceiveRemoteNotification` returning the correct `UIBackgroundFetchResult`. Rich-notification reviews must say service extensions require `mutable-content: 1` plus an alert payload, silent pushes do not trigger them, attachments are supported on-disk files that the system validates and stores, secrets use Keychain Sharing while App Groups are for shared files/UserDefaults, communication notifications require capability + `NSUserActivityTypes` + `INInteraction` donation + `content.updating(from:)`, and every service-extension path including attachment/download failures and `serviceExtensionTimeWillExpire()` must call the content handler exactly once with original, best-attempt, or updated content.

## Permission Flow

Request notification authorization before scheduling or displaying user-visible alerts, sounds, or badges. The system prompt appears only once; subsequent calls return the stored decision. APNs token registration is separate: call `registerForRemoteNotifications()` when the app needs a device token, even if the user hasn't granted alert authorization.

```swift
import UserNotifications

@MainActor
func requestNotificationPermission() async -> Bool {
    let center = UNUserNotificationCenter.current()
    do {
        let granted = try await center.requestAuthorization(
            options: [.alert, .sound, .badge]
        )
        return granted
    } catch {
        print("Authorization request failed: \(error)")
        return false
    }
}
```

### Checking Current Status

Always check status before assuming permissions. The user can change settings at any time.

```swift
@MainActor
func checkNotificationStatus() async -> UNAuthorizationStatus {
    let settings = await UNUserNotificationCenter.current().notificationSettings()
    return settings.authorizationStatus
    // .notDetermined, .denied, .authorized, .provisional, .ephemeral
}
```

### Provisional Notifications

Provisional notifications deliver quietly to the notification center without interrupting the user. The user can then choose to keep or turn them off. Use for onboarding flows where you want to demonstrate value before asking for full permission.

```swift
// Delivers silently -- no permission prompt shown to the user
try await center.requestAuthorization(options: [.alert, .sound, .badge, .provisional])
```

### Critical Alerts

Critical alerts bypass Do Not Disturb and the mute switch. Requires a special entitlement from Apple (request via developer portal). Use only for health, safety, or security scenarios.

```swift
// Requires com.apple.developer.usernotifications.critical-alerts entitlement
try await center.requestAuthorization(
    options: [.alert, .sound, .badge, .criticalAlert]
)
```

### Handling Denied Permissions

When the user has denied notifications, guide them to Settings with `UIApplication.openSettingsURLString`. Do not repeatedly prompt or nag.

## APNs Registration

Use `UIApplicationDelegateAdaptor` to receive the device token in a SwiftUI app. The AppDelegate callbacks are the only way to receive APNs tokens.

```swift
@main
struct MyApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) var appDelegate

    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        UNUserNotificationCenter.current().delegate = NotificationDelegate.shared
        return true
    }

    func application(
        _ application: UIApplication,
        didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data
    ) {
        let token = deviceToken.map { String(format: "%02x", $0) }.joined()
        print("APNs token: \(token)")
        // Send token to your server
        Task { await TokenService.shared.upload(token: token) }
    }

    func application(
        _ application: UIApplication,
        didFailToRegisterForRemoteNotificationsWithError error: Error
    ) {
        print("APNs registration failed: \(error.localizedDescription)")
        // Simulator can simulate pushes, but it does not register with APNs.
    }
}
```

### Registration Order

Configure delegates and categories at launch. Then request user-notification authorization in context for visible notifications, and register with APNs whenever the app needs a device token. Do not gate APNs registration on `.authorized`; without alert authorization, remote notifications are delivered silently.

```swift
@MainActor
func configureNotifications() async {
    let center = UNUserNotificationCenter.current()
    let settings = await center.notificationSettings()

    if settings.authorizationStatus == .notDetermined {
        _ = await requestNotificationPermission()
    }

    // Needed for APNs token delivery and silent remote notifications.
    UIApplication.shared.registerForRemoteNotifications()
}
```

### Token Handling

Device tokens change. Re-send the token to your server every time `didRegisterForRemoteNotificationsWithDeviceToken` fires, not just the first time. Do not persist tokens locally as a source of truth or assume a fixed token length.

## Local Notifications

Schedule notifications directly from the device without a server. Useful for reminders, timers, and location-based alerts.

### Creating Content

```swift
let content = UNMutableNotificationContent()
content.title = "Workout Reminder"
content.subtitle = "Time to move"
content.body = "You have a scheduled workout in 15 minutes."
content.sound = .default
content.badge = NSNumber(value: 1)
content.userInfo = ["workoutId": "abc123"]
content.threadIdentifier = "workouts"  // groups in notification center
```

### Trigger Types

```swift
// Fire after a time interval (minimum 60 seconds for repeating)
let timeTrigger = UNTimeIntervalNotificationTrigger(timeInterval: 300, repeats: false)

// Fire at a specific date/time
var dateComponents = DateComponents()
dateComponents.hour = 8
dateComponents.minute = 30
let calendarTrigger = UNCalendarNotificationTrigger(
    dateMatching: dateComponents, repeats: true  // daily at 8:30 AM
)

// Fire when entering a geographic region
let region = CLCircularRegion(
    center: CLLocationCoordinate2D(latitude: 37.33, longitude: -122.01),
    radius: 100,
    identifier: "gym"
)
region.notifyOnEntry = true
region.notifyOnExit = false
let locationTrigger = UNLocationNotificationTrigger(region: region, repeats: false)
// Requires "When In Use" location permission at minimum
```

### Scheduling and Managing

```swift
let request = UNNotificationRequest(
    identifier: "workout-reminder-abc123",
    content: content,
    trigger: timeTrigger
)

let center = UNUserNotificationCenter.current()
try await center.add(request)

// Remove specific pending notifications
center.removePendingNotificationRequests(withIdentifiers: ["workout-reminder-abc123"])

// Remove all pending
center.removeAllPendingNotificationRequests()

// Remove delivered notifications from notification center
center.removeDeliveredNotifications(withIdentifiers: ["workout-reminder-abc123"])
center.removeAllDeliveredNotifications()

// List all pending requests
let pending = await center.pendingNotificationRequests()
```

## Remote Notification Payload

### Standard APNs Payload

```json
{
    "aps": {
        "alert": {
            "title": "New Message",
            "subtitle": "From Alice",
            "body": "Hey, are you free for lunch?"
        },
        "badge": 3,
        "sound": "default",
        "thread-id": "chat-alice",
        "category": "MESSAGE_CATEGORY"
    },
    "messageId": "msg-789",
    "senderId": "user-alice"
}
```

### Silent / Background Push

Set `content-available: 1` with no alert, sound, or badge. Requires "Background Modes > Remote notifications" plus APNs headers `apns-push-type: background` and `apns-priority: 5`. The system treats these as low priority, throttled, and not guaranteed; do not send them every few minutes or rely on them for immediate freshness. In `didReceiveRemoteNotification`, do bounded work and return a `UIBackgroundFetchResult` promptly, within the background execution window.

```json
{
    "aps": {
        "content-available": 1
    },
    "updateType": "new-data"
}
```

Handle in AppDelegate:
```swift
func application(
    _ application: UIApplication,
    didReceiveRemoteNotification userInfo: [AnyHashable: Any]
) async -> UIBackgroundFetchResult {
    guard let updateType = userInfo["updateType"] as? String else {
        return .noData
    }
    do {
        try await DataSyncService.shared.sync(trigger: updateType)
        return .newData
    } catch {
        return .failed
    }
}
```

### Mutable Content

Set `mutable-content: 1` plus an `alert` dictionary to let a Notification Service Extension modify an alerting remote notification before display. Silent pushes do not trigger the service extension. Use service extensions for bounded work such as downloading supported on-disk attachments, decrypting display text, or configuring communication notifications; call the content handler on every success, failure, and timeout path. For communication notifications, enable the capability, add `NSUserActivityTypes`, donate the `INInteraction`, then call `content.updating(from:)`.

```json
{
    "aps": {
        "alert": { "title": "Photo", "body": "Alice sent a photo" },
        "mutable-content": 1
    },
    "imageUrl": "https://example.com/photo.jpg"
}
```

### Localized Notifications

Use localization keys so the notification displays in the user's language:

```json
{
    "aps": {
        "alert": {
            "title-loc-key": "NEW_MESSAGE_TITLE",
            "loc-key": "NEW_MESSAGE_BODY",
            "loc-args": ["Alice"]
        }
    }
}
```

## Notification Handling

### UNUserNotificationCenterDelegate

Implement the delegate to control foreground display and handle user taps. Set the delegate as early as possible -- in `application(_:didFinishLaunchingWithOptions:)` or `App.init`.

```swift
@MainActor
final class NotificationDelegate: NSObject, UNUserNotificationCenterDelegate {
    static let shared = NotificationDelegate()

    // Called when notification arrives while app is in FOREGROUND
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        willPresent notification: UNNotification
    ) async -> UNNotificationPresentationOptions {
        // Return which presentation elements to show
        // Without this, foreground notifications are silently suppressed
        return [.banner, .sound, .badge]
    }

    // Called when user TAPS the notification
    func userNotificationCenter(
        _ center: UNUserNotificationCenter,
        didReceive response: UNNotificationResponse
    ) async {
        let userInfo = response.notification.request.content.userInfo
        let actionIdentifier = response.actionIdentifier

        switch actionIdentifier {
        case UNNotificationDefaultActionIdentifier:
            // User tapped the notification body
            await handleNotificationTap(userInfo: userInfo)
        case UNNotificationDismissActionIdentifier:
            // User dismissed the notification
            break
        default:
            // Custom action button tapped
            await handleCustomAction(actionIdentifier, userInfo: userInfo)
        }
    }
}
```

### Deep Linking from Notifications

Route notification taps to the correct screen using a shared `@Observable` router. The delegate writes a pending destination; the SwiftUI view observes and consumes it.

```swift
@Observable @MainActor
final class DeepLinkRouter {
    static let shared = DeepLinkRouter()

    var pendingDestination: AppDestination?
}

// In NotificationDelegate:
func handleNotificationTap(userInfo: [AnyHashable: Any]) async {
    guard let id = userInfo["messageId"] as? String else { return }
    DeepLinkRouter.shared.pendingDestination = .chat(id: id)
}

// In SwiftUI -- observe and consume:
.onChange(of: router.pendingDestination) { _, destination in
    if let destination {
        path.append(destination)
        router.pendingDestination = nil
    }
}
```

See [references/notification-patterns.md](references/notification-patterns.md) for the full deep-linking handler with tab switching.

## Notification Actions and Categories

Define interactive actions that appear as buttons on the notification. Register categories at launch.

### Defining Categories and Actions

```swift
func registerNotificationCategories() {
    let replyAction = UNTextInputNotificationAction(
        identifier: "REPLY_ACTION",
        title: "Reply",
        options: [],
        textInputButtonTitle: "Send",
        textInputPlaceholder: "Type a reply..."
    )

    let likeAction = UNNotificationAction(
        identifier: "LIKE_ACTION",
        title: "Like",
        options: []
    )

    let deleteAction = UNNotificationAction(
        identifier: "DELETE_ACTION",
        title: "Delete",
        options: [.destructive, .authenticationRequired]
    )

    let messageCategory = UNNotificationCategory(
        identifier: "MESSAGE_CATEGORY",
        actions: [replyAction, likeAction, deleteAction],
        intentIdentifiers: [],
        options: [.customDismissAction]  // fires didReceive on dismiss too
    )

    UNUserNotificationCenter.current().setNotificationCategories([messageCategory])
}
```

### Handling Action Responses

```swift
func handleCustomAction(_ identifier: String, userInfo: [AnyHashable: Any]) async {
    switch identifier {
    case "REPLY_ACTION":
        // response is UNTextInputNotificationResponse for text input actions
        break
    case "LIKE_ACTION":
        guard let messageId = userInfo["messageId"] as? String else { return }
        await MessageService.shared.likeMessage(id: messageId)
    case "DELETE_ACTION":
        guard let messageId = userInfo["messageId"] as? String else { return }
        await MessageService.shared.deleteMessage(id: messageId)
    default:
        break
    }
}
```

Action options:
- `.authenticationRequired` -- device must be unlocked to perform the action
- `.destructive` -- displayed in red; use for delete/remove actions
- `.foreground` -- launches the app to the foreground when tapped

## Notification Grouping

Group related notifications with `threadIdentifier` (or `thread-id` in the APNs payload). Each unique thread becomes a separate group in Notification Center.

```swift
content.threadIdentifier = "chat-alice"  // all messages from Alice group together
content.summaryArgument = "Alice"
content.summaryArgumentCount = 3         // "3 more notifications from Alice"
```

Customize the summary format string in the category:

```swift
let category = UNNotificationCategory(
    identifier: "MESSAGE_CATEGORY",
    actions: [replyAction],
    intentIdentifiers: [],
    categorySummaryFormat: "%u more messages from %@",
    options: []
)
```

## Common Mistakes

**DON'T:** Gate APNs token registration on alert authorization when the app needs silent pushes or server token binding.
**DO:** Request authorization for alerts/sounds/badges, and register with APNs whenever a device token is needed.
**DON'T:** Convert device token with `String(data: deviceToken, encoding: .utf8)`.
**DO:** Use hex: `deviceToken.map { String(format: "%02x", $0) }.joined()`.
**DON'T:** Promise every-few-minutes silent refresh or immediate background delivery.
**DO:** Say background pushes are low priority, throttled, not guaranteed, limited to a few per hour in practice, and require bounded `didReceiveRemoteNotification` work that returns the correct `UIBackgroundFetchResult`.
**DON'T:** Expect a silent push to run a Notification Service Extension, or leave the extension without calling its content handler.
**DO:** Use `mutable-content: 1` with an alert payload, supported on-disk attachments that the system validates and stores, `INInteraction` donation plus `content.updating(from:)` for communication notifications, and original or best-attempt content on every success, failure, and timeout path.
**DON'T:** Forget foreground handling. Without `willPresent`, notifications are silently suppressed.
**DO:** Implement `willPresent` and return `.banner`, `.sound`, `.badge`.
**DON'T:** Set delegate too late or register from SwiftUI views without AppDelegate adaptor.
**DO:** Set delegate in `App.init`; use `UIApplicationDelegateAdaptor` for APNs.
**DON'T:** Upload APNs tokens only when they "change" or assume a fixed token length. **DO:** Upload on every `didRegister` callback and treat the token as opaque data converted to hex.
**DON'T:** Put Live Activity, VoIP, or App Clip-specific notification rules here. **DO:** Route those to `activitykit`, `callkit`, and `app-clips`.

## Review Checklist

- [ ] Authorization requested before visible alerts/sounds/badges; denied case handled (Settings link)
- [ ] APNs registration not incorrectly blocked by alert authorization status
- [ ] Device token converted to hex, uploaded on every callback, and not treated as a locally cached or fixed-length constant
- [ ] `UNUserNotificationCenterDelegate` set in `App.init` or `application(_:didFinishLaunching:)`
- [ ] Foreground (`willPresent`) and tap (`didReceive`) handling implemented
- [ ] Categories/actions registered at launch if interactive notifications needed
- [ ] Silent push uses `content-available: 1`, no alert/sound/badge, `apns-push-type: background`, `apns-priority: 5`, Background Modes > Remote notifications, throttling caveats, and correct `UIBackgroundFetchResult`

## References
- [references/notification-patterns.md](references/notification-patterns.md) — AppDelegate setup, APNs callbacks, deep-link router, silent push, debugging
- [references/rich-notifications.md](references/rich-notifications.md) — Service Extension, Content Extension, attachments, communication notifications
- Apple docs: [APNs registration](https://sosumi.ai/documentation/usernotifications/registering-your-app-with-apns), [permission](https://sosumi.ai/documentation/usernotifications/asking-permission-to-use-notifications), [payloads](https://sosumi.ai/documentation/usernotifications/generating-a-remote-notification), [background pushes](https://sosumi.ai/documentation/usernotifications/pushing-background-updates-to-your-app)
