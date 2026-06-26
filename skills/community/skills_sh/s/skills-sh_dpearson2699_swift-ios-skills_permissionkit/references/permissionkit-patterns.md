# PermissionKit Extended Patterns

Overflow reference for the `permissionkit` skill. Contains advanced patterns
that exceed the main skill file's scope.

## Contents

- [Full UIKit Integration](#full-uikit-integration)
- [Response Observer Manager](#response-observer-manager)
- [Multi-Contact Permission Flow](#multi-contact-permission-flow)
- [Communication Limits Checking Pattern](#communication-limits-checking-pattern)
- [SwiftUI Full-Screen Permission Flow](#swiftui-full-screen-permission-flow)
- [macOS Integration](#macos-integration)
- [Error Recovery Patterns](#error-recovery-patterns)

## Full UIKit Integration

Complete UIKit view controller with permission request and response handling.
Keep the pending state explicit: if the child cancels the iMessage send flow,
PermissionKit does not deliver a `PermissionResponse` for that question.

```swift
import UIKit
import PermissionKit

class ContactViewController: UIViewController {
    private var responseTask: Task<Void, Never>?

    override func viewDidLoad() {
        super.viewDidLoad()
        startObservingResponses()
    }

    deinit {
        responseTask?.cancel()
    }

    func requestPermissionToMessage(_ contact: Contact) {
        let personInfo = CommunicationTopic.PersonInformation(
            handle: CommunicationHandle(
                value: contact.phoneNumber,
                kind: .phoneNumber
            ),
            nameComponents: contact.nameComponents,
            avatarImage: contact.avatarCGImage
        )

        let topic = CommunicationTopic(
            personInformation: [personInfo],
            actions: [.message]
        )

        let question = PermissionQuestion<CommunicationTopic>(
            communicationTopic: topic
        )

        Task {
            do {
                try await AskCenter.shared.ask(question, in: self)
                showPendingState(for: contact)
                schedulePendingExpiration(for: question.id)
            } catch AskError.communicationLimitsNotEnabled {
                enableMessaging(for: contact)
            } catch AskError.notAvailable {
                showFeatureUnavailable()
            } catch {
                showError(error)
            }
        }
    }

    private func startObservingResponses() {
        responseTask = Task { [weak self] in
            let responses = AskCenter.shared.responses(
                for: CommunicationTopic.self
            )
            for await response in responses {
                await MainActor.run {
                    self?.handleResponse(response)
                }
            }
        }
    }

    @MainActor
    private func handleResponse(_ response: PermissionResponse<CommunicationTopic>) {
        switch response.choice.answer {
        case .approval:
            let handles = response.question.topic.personInformation
                .map(\.handle)
            for handle in handles {
                enableCommunication(for: handle)
            }
        case .denial:
            let handles = response.question.topic.personInformation
                .map(\.handle)
            for handle in handles {
                showDeniedState(for: handle)
            }
        @unknown default:
            break
        }
    }

    private func showPendingState(for contact: Contact) { }
    private func schedulePendingExpiration(for id: UUID) { }
    private func enableMessaging(for contact: Contact) { }
    private func enableCommunication(for handle: CommunicationHandle) { }
    private func showDeniedState(for handle: CommunicationHandle) { }
    private func showFeatureUnavailable() { }
    private func showError(_ error: Error) { }
}
```

## Response Observer Manager

Centralize response observation for apps with multiple permission flows.

```swift
import PermissionKit

@Observable
@MainActor
final class PermissionManager {
    static let shared = PermissionManager()

    var approvedHandles: Set<String> = []
    var deniedHandles: Set<String> = []
    var pendingHandleValues: Set<String> = []
    var pendingQuestionIDs: Set<UUID> = []

    private var observerTask: Task<Void, Never>?

    private init() {
        startObserving()
    }

    deinit {
        observerTask?.cancel()
    }

    func askPermission(
        for handles: [CommunicationHandle],
        actions: Set<CommunicationTopic.Action>,
        in viewController: UIViewController
    ) async throws {
        let personInfo = handles.map { handle in
            CommunicationTopic.PersonInformation(
                handle: handle,
                nameComponents: nil,
                avatarImage: nil
            )
        }

        let topic = CommunicationTopic(
            personInformation: personInfo,
            actions: actions
        )

        let question = PermissionQuestion<CommunicationTopic>(
            communicationTopic: topic
        )

        try await AskCenter.shared.ask(question, in: viewController)
        let handleValues = handles.map(\.value)
        pendingQuestionIDs.insert(question.id)
        pendingHandleValues.formUnion(handleValues)
        schedulePendingExpiration(
            for: question.id,
            handleValues: handleValues
        )
    }

    func isApproved(_ handleValue: String) -> Bool {
        approvedHandles.contains(handleValue)
    }

    func isDenied(_ handleValue: String) -> Bool {
        deniedHandles.contains(handleValue)
    }

    func isPending(_ handleValue: String) -> Bool {
        pendingHandleValues.contains(handleValue)
    }

    private func startObserving() {
        observerTask = Task { [weak self] in
            let responses = AskCenter.shared.responses(
                for: CommunicationTopic.self
            )
            for await response in responses {
                await MainActor.run {
                    self?.processResponse(response)
                }
            }
        }
    }

    private func processResponse(
        _ response: PermissionResponse<CommunicationTopic>
    ) {
        pendingQuestionIDs.remove(response.question.id)

        let handleValues = response.question.topic.personInformation
            .map(\.handle.value)
        for value in handleValues {
            pendingHandleValues.remove(value)
        }

        switch response.choice.answer {
        case .approval:
            for value in handleValues {
                approvedHandles.insert(value)
                deniedHandles.remove(value)
            }
        case .denial:
            for value in handleValues {
                deniedHandles.insert(value)
            }
        @unknown default:
            break
        }
    }

    private func schedulePendingExpiration(
        for id: UUID,
        handleValues: [String]
    ) {
        // Expire or offer retry if no response arrives after your product's
        // chosen pending window. Child cancellation produces no response.
    }
}
```

## Multi-Contact Permission Flow

Request permission for multiple contacts in a single question.

```swift
func requestGroupPermission(
    contacts: [Contact],
    in viewController: UIViewController
) async throws {
    let personInfoList = contacts.map { contact in
        CommunicationTopic.PersonInformation(
            handle: CommunicationHandle(
                value: contact.identifier,
                kind: .custom
            ),
            nameComponents: contact.nameComponents,
            avatarImage: contact.avatarCGImage
        )
    }

    let topic = CommunicationTopic(
        personInformation: personInfoList,
        actions: [.message, .audioCall, .videoCall]
    )

    let question = PermissionQuestion<CommunicationTopic>(
        communicationTopic: topic
    )

    // Check question properties
    print("Question ID: \(question.id)")
    print("Choices: \(question.choices.map(\.title))")
    print("Default choice: \(question.defaultChoice.title)")

    if let expiration = question.expirationDate {
        print("Expires: \(expiration)")
    }

    try await AskCenter.shared.ask(question, in: viewController)
}
```

## Communication Limits Checking Pattern

Check which handles are already known to the system before building the
permission UI. This does not prove communication limits are enabled; still
handle `AskError.communicationLimitsNotEnabled` when asking. `knownHandles(in:)`
requires a non-nil, nonempty app bundle identifier.

```swift
@Observable
@MainActor
final class ContactListViewModel {
    var contacts: [ContactItem] = []

    struct ContactItem: Identifiable {
        let id: String
        let name: String
        let handle: CommunicationHandle
        var isKnownBySystem: Bool = false
        var needsPermissionPrompt: Bool = false
    }

    func refreshContactStatus() async {
        guard Bundle.main.bundleIdentifier?.isEmpty == false else { return }

        let limits = CommunicationLimits.current
        let allHandles = Set(contacts.map(\.handle))
        let knownHandles = await limits.knownHandles(in: allHandles)

        for i in contacts.indices {
            contacts[i].isKnownBySystem = knownHandles.contains(
                contacts[i].handle
            )
            contacts[i].needsPermissionPrompt = !contacts[i].isKnownBySystem
        }
    }
}
```

## SwiftUI Full-Screen Permission Flow

Build a complete permission flow in SwiftUI.

```swift
import SwiftUI
import PermissionKit

struct ContactDetailView: View {
    let contact: Contact
    @State private var permissionState: PermissionState = .unknown
    @Environment(PermissionManager.self) private var permissionManager

    enum PermissionState {
        case unknown, checking, needsPermission, approved, denied
        case pending, error(String)
    }

    var body: some View {
        VStack {
            Text(contact.name)
                .font(.title)

            switch permissionState {
            case .unknown, .checking:
                ProgressView("Checking permissions...")

            case .needsPermission:
                let handle = CommunicationHandle(
                    value: contact.phoneNumber,
                    kind: .phoneNumber
                )
                let question = PermissionQuestion<CommunicationTopic>(
                    handle: handle
                )

                VStack {
                    Text("Permission needed to message this contact.")
                        .foregroundStyle(.secondary)
                    PermissionButton(question: question) {
                        Label("Ask to Message", systemImage: "message.badge.clock")
                    }
                    .buttonStyle(.borderedProminent)
                }

            case .pending:
                Label("Waiting for parent response", systemImage: "clock")
                    .foregroundStyle(.secondary)

            case .approved:
                Label("Messaging enabled", systemImage: "checkmark.circle.fill")
                    .foregroundStyle(.green)

            case .denied:
                Label("Permission denied", systemImage: "xmark.circle.fill")
                    .foregroundStyle(.red)

            case .error(let message):
                Label(message, systemImage: "exclamationmark.triangle")
                    .foregroundStyle(.orange)
            }
        }
        .task {
            await checkPermission()
        }
    }

    private func checkPermission() async {
        permissionState = .checking
        let handle = CommunicationHandle(
            value: contact.phoneNumber,
            kind: .phoneNumber
        )
        let limits = CommunicationLimits.current
        let isKnown = await limits.isKnownHandle(handle)

        if isKnown {
            permissionState = .approved
        } else if permissionManager.isApproved(contact.phoneNumber) {
            permissionState = .approved
        } else if permissionManager.isDenied(contact.phoneNumber) {
            permissionState = .denied
        } else if permissionManager.isPending(contact.phoneNumber) {
            permissionState = .pending
        } else {
            permissionState = .needsPermission
        }
    }
}
```

## macOS Integration

On macOS 26.2+, pass an `NSWindow` instead of `UIViewController`.

```swift
#if os(macOS)
import AppKit
import PermissionKit

func requestPermission(
    for question: PermissionQuestion<CommunicationTopic>,
    in window: NSWindow
) async throws {
    try await AskCenter.shared.ask(question, in: window)
}
#endif
```

## Error Recovery Patterns

Provide actionable recovery for each error type.

```swift
func handleAskError(_ error: AskError) -> (title: String, message: String, action: (() -> Void)?) {
    switch error {
    case .communicationLimitsNotEnabled:
        return (
            "No Restrictions",
            "Communication limits are not enabled. You can communicate freely.",
            nil
        )
    case .contactSyncNotSetup:
        return (
            "Contact Sync Required",
            "Please enable contact sync in Settings to use this feature.",
            { openContactSyncSettings() }
        )
    case .invalidQuestion:
        return (
            "Invalid Request",
            "The permission request could not be created. Please try again.",
            nil
        )
    case .notAvailable:
        return (
            "Not Available",
            "This feature is not available on this device.",
            nil
        )
    case .systemError(let underlying):
        return (
            "System Error",
            underlying.localizedDescription,
            nil
        )
    case .unknown:
        return (
            "Unknown Error",
            "An unexpected error occurred. Please try again later.",
            nil
        )
    @unknown default:
        return (
            "Error",
            "An error occurred.",
            nil
        )
    }
}
```
