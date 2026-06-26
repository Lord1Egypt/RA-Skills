# CallKit + PushKit Extended Patterns

Overflow reference for the `callkit` skill. Contains advanced patterns that exceed the main skill file's scope.

## Contents

- [Full Call Manager](#full-call-manager)
- [Hold and Mute Actions](#hold-and-mute-actions)
- [Multiple Concurrent Calls](#multiple-concurrent-calls)
- [Call State Tracking](#call-state-tracking)
- [Encrypted VoIP Push Filtering](#encrypted-voip-push-filtering)
- [Call Directory Incremental Updates](#call-directory-incremental-updates)
- [Testing VoIP Locally](#testing-voip-locally)

## Full Call Manager

```swift
import CallKit
import AVFoundation
import PushKit

@Observable
@MainActor
final class VoIPCallManager: NSObject {
    let provider: CXProvider
    let callController = CXCallController()

    private(set) var activeCalls: [UUID: CallInfo] = [:]

    struct CallInfo {
        let uuid: UUID
        let handle: String
        let isOutgoing: Bool
        var isOnHold: Bool = false
        var isMuted: Bool = false
        var isConnected: Bool = false
    }

    override init() {
        let config = CXProviderConfiguration()
        config.localizedName = "My VoIP"
        config.supportsVideo = true
        config.maximumCallGroups = 2
        config.maximumCallsPerCallGroup = 1
        config.supportedHandleTypes = [.phoneNumber]
        config.includesCallsInRecents = true

        provider = CXProvider(configuration: config)
        super.init()
        provider.setDelegate(self, queue: nil)
    }

    // MARK: - Incoming

    func reportIncoming(
        uuid: UUID,
        handle: String,
        callerName: String,
        hasVideo: Bool
    ) async throws {
        let update = CXCallUpdate()
        update.remoteHandle = CXHandle(type: .phoneNumber, value: handle)
        update.localizedCallerName = callerName
        update.hasVideo = hasVideo
        update.supportsHolding = true
        update.supportsDTMF = true
        update.supportsGrouping = false
        update.supportsUngrouping = false

        try await withCheckedThrowingContinuation {
            (continuation: CheckedContinuation<Void, Error>) in
            provider.reportNewIncomingCall(
                with: uuid, update: update
            ) { error in
                if let error {
                    continuation.resume(throwing: error)
                } else {
                    continuation.resume()
                }
            }
        }

        activeCalls[uuid] = CallInfo(
            uuid: uuid, handle: handle, isOutgoing: false
        )
    }

    // MARK: - Outgoing

    func startCall(handle: String, hasVideo: Bool) {
        let uuid = UUID()
        let cxHandle = CXHandle(type: .phoneNumber, value: handle)
        let action = CXStartCallAction(call: uuid, handle: cxHandle)
        action.isVideo = hasVideo

        callController.request(
            CXTransaction(action: action)
        ) { error in
            if let error {
                print("Start call failed: \(error)")
            }
        }

        activeCalls[uuid] = CallInfo(
            uuid: uuid, handle: handle, isOutgoing: true
        )
    }

    // MARK: - Actions

    func endCall(uuid: UUID) {
        let action = CXEndCallAction(call: uuid)
        callController.request(CXTransaction(action: action)) { error in
            if let error { print("End call failed: \(error)") }
        }
    }

    func setHeld(uuid: UUID, onHold: Bool) {
        let action = CXSetHeldCallAction(call: uuid, onHold: onHold)
        callController.request(CXTransaction(action: action)) { error in
            if let error { print("Hold failed: \(error)") }
        }
    }

    func setMuted(uuid: UUID, muted: Bool) {
        let action = CXSetMutedCallAction(call: uuid, muted: muted)
        callController.request(CXTransaction(action: action)) { error in
            if let error { print("Mute failed: \(error)") }
        }
    }
}
```

## Hold and Mute Actions

```swift
extension VoIPCallManager: CXProviderDelegate {
    nonisolated func providerDidReset(_ provider: CXProvider) {
        Task { @MainActor in
            for uuid in activeCalls.keys {
                disconnectCall(uuid)
            }
            activeCalls.removeAll()
        }
    }

    nonisolated func provider(
        _ provider: CXProvider,
        perform action: CXSetHeldCallAction
    ) {
        Task { @MainActor in
            activeCalls[action.callUUID]?.isOnHold = action.isOnHold
            if action.isOnHold {
                pauseAudio(for: action.callUUID)
            } else {
                resumeAudio(for: action.callUUID)
            }
            action.fulfill()
        }
    }

    nonisolated func provider(
        _ provider: CXProvider,
        perform action: CXSetMutedCallAction
    ) {
        Task { @MainActor in
            activeCalls[action.callUUID]?.isMuted = action.isMuted
            // If call translation is active, mute app input without deactivating
            // upstream audio that translated audio may need.
            setMicrophoneMuted(action.isMuted)
            action.fulfill()
        }
    }

    nonisolated func provider(
        _ provider: CXProvider,
        perform action: CXAnswerCallAction
    ) {
        Task { @MainActor in
            configureAudioSession()
            connectToServer(callUUID: action.callUUID) { success in
                if success {
                    activeCalls[action.callUUID]?.isConnected = true
                    action.fulfill()
                } else {
                    provider.reportCall(
                        with: action.callUUID,
                        endedAt: Date(),
                        reason: .failed
                    )
                    action.fail()
                }
            }
        }
    }

    nonisolated func provider(
        _ provider: CXProvider,
        perform action: CXStartCallAction
    ) {
        Task { @MainActor in
            configureAudioSession()
            provider.reportOutgoingCall(
                with: action.callUUID,
                startedConnectingAt: Date()
            )
            connectToServer(callUUID: action.callUUID)
            provider.reportOutgoingCall(
                with: action.callUUID,
                connectedAt: Date()
            )
            activeCalls[action.callUUID]?.isConnected = true
            action.fulfill()
        }
    }

    nonisolated func provider(
        _ provider: CXProvider,
        perform action: CXEndCallAction
    ) {
        Task { @MainActor in
            disconnectCall(action.callUUID)
            activeCalls.removeValue(forKey: action.callUUID)
            action.fulfill()
        }
    }

    nonisolated func provider(
        _ provider: CXProvider,
        didActivate audioSession: AVAudioSession
    ) {
        Task { @MainActor in
            startAudioEngine()
        }
    }

    nonisolated func provider(
        _ provider: CXProvider,
        didDeactivate audioSession: AVAudioSession
    ) {
        Task { @MainActor in
            stopAudioEngine()
        }
    }
}
```

## Multiple Concurrent Calls

When a second call arrives while one is active, CallKit automatically puts
the first call on hold. Handle the hold action to pause your audio stream:

```swift
nonisolated func provider(
    _ provider: CXProvider,
    perform action: CXSetHeldCallAction
) {
    Task { @MainActor in
        if action.isOnHold {
            // Pause the RTP stream for this call
            pauseMediaStream(for: action.callUUID)
        } else {
            // Resume the RTP stream
            resumeMediaStream(for: action.callUUID)
        }
        activeCalls[action.callUUID]?.isOnHold = action.isOnHold
        action.fulfill()
    }
}
```

Configure `maximumCallGroups` and `maximumCallsPerCallGroup` in
`CXProviderConfiguration` to control how many concurrent calls your app
supports.

## Call State Tracking

Use `CXCallObserver` to monitor call state changes from outside the provider
delegate:

```swift
import CallKit

final class CallStateObserver: NSObject, CXCallObserverDelegate {
    let observer = CXCallObserver()

    override init() {
        super.init()
        observer.setDelegate(self, queue: nil)
    }

    func callObserver(
        _ callObserver: CXCallObserver,
        callChanged call: CXCall
    ) {
        if call.hasEnded {
            print("Call \(call.uuid) ended")
        } else if call.hasConnected {
            print("Call \(call.uuid) connected")
        } else if call.isOutgoing {
            print("Outgoing call \(call.uuid) ringing")
        } else {
            print("Incoming call \(call.uuid) ringing")
        }
    }
}
```

## Encrypted VoIP Push Filtering

Use a notification service extension with
`CXProvider.reportNewIncomingVoIPPushPayload` only when server-side metadata
encryption means the server cannot determine whether the outgoing notification
is a VoIP call request or some other data. If the server knows the content is
a VoIP call, send a normal PushKit VoIP push instead.

```swift
import UserNotifications
import CallKit

final class NotificationService: UNNotificationServiceExtension {
    override func didReceive(
        _ request: UNNotificationRequest,
        withContentHandler contentHandler:
            @escaping (UNNotificationContent) -> Void
    ) {
        guard let encryptedPayload = request.content
            .userInfo["encrypted"] as? [AnyHashable: Any] else {
            contentHandler(request.content)
            return
        }

        let decryptedPayload = decryptPayload(encryptedPayload)

        CXProvider.reportNewIncomingVoIPPushPayload(
            decryptedPayload
        ) { error in
            if let error {
                // Show a missed-call notification instead
                let content = UNMutableNotificationContent()
                content.title = "Missed Call"
                content.body = decryptedPayload["callerName"] as? String ?? ""
                contentHandler(content)
            } else {
                // Call was reported; suppress the notification
                contentHandler(UNNotificationContent())
            }
        }
    }
}
```

This requires the `com.apple.developer.usernotifications.filtering` entitlement.

## Call Directory Incremental Updates

After the first full load, use incremental updates to add or remove entries
without reloading the entire dataset:

```swift
private func addOrRemoveIncrementalEntries(
    to context: CXCallDirectoryExtensionContext
) {
    let removedNumbers: [CXCallDirectoryPhoneNumber] = fetchRemovedNumbers()
    for number in removedNumbers {
        context.removeBlockingEntry(withPhoneNumber: number)
        context.removeIdentificationEntry(withPhoneNumber: number)
    }

    let newBlocked: [CXCallDirectoryPhoneNumber] = fetchNewBlockedNumbers()
    for number in newBlocked.sorted() {
        context.addBlockingEntry(withNextSequentialPhoneNumber: number)
    }

    let newIdentified: [(CXCallDirectoryPhoneNumber, String)] = fetchNewIdentified()
    for (number, label) in newIdentified.sorted(by: { $0.0 < $1.0 }) {
        context.addIdentificationEntry(
            withNextSequentialPhoneNumber: number,
            label: label
        )
    }
}
```

Call Directory data is bulk data. The system calls `beginRequest(with:)` when
loading the extension, not for each individual incoming call, so keep web
lookups and dataset sync in the containing app before reloading the extension.

## Testing VoIP Locally

### Simulating VoIP Pushes

Use the Push Notifications Console or a command-line tool to send test pushes.
The payload must target the VoIP topic (`<bundle-id>.voip`):

```json
{
    "aps": {},
    "handle": "+15551234567",
    "callerName": "Test Caller",
    "hasVideo": false
}
```

### Testing Without a Server

For development, you can bypass PushKit and directly call the incoming call
reporting method:

```swift
#if DEBUG
func simulateIncomingCall() {
    let uuid = UUID()
    Task {
        try? await CallManager.shared.reportIncomingCall(
            uuid: uuid,
            handle: "+15551234567",
            hasVideo: false
        )
    }
}
#endif
```

### Checking Extension Status

Verify that the Call Directory extension is enabled:

```swift
CXCallDirectoryManager.sharedInstance.getEnabledStatusForExtension(
    withIdentifier: "com.example.app.CallDirectory"
) { status, error in
    switch status {
    case .enabled:
        print("Extension is enabled")
    case .disabled:
        print("Extension is disabled -- prompt user to enable in Settings")
    case .unknown:
        print("Status unknown")
    @unknown default:
        break
    }
}
```
