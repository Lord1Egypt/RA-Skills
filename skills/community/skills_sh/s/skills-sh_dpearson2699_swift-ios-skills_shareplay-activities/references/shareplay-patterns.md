# SharePlay Extended Patterns

Overflow reference for the `shareplay-activities` skill. Contains advanced
patterns that exceed the main skill file's scope.

## Contents

- [Collaborative Drawing Canvas](#collaborative-drawing-canvas)
- [Full SharePlay Manager](#full-shareplay-manager)
- [SwiftUI SharePlay Integration](#swiftui-shareplay-integration)
  - [ShareLink and AirDrop](#sharelink-and-airdrop)
- [Custom Activity with State Sync](#custom-activity-with-state-sync)
- [Participant Tracking](#participant-tracking)

## Collaborative Drawing Canvas

### Activity Definition

```swift
import GroupActivities

struct DrawTogetherActivity: GroupActivity {
    static let activityIdentifier = "com.example.draw-together"

    var metadata: GroupActivityMetadata {
        var meta = GroupActivityMetadata()
        meta.title = "Draw Together"
        meta.type = .createTogether
        return meta
    }
}
```

### Stroke Message

```swift
import Foundation

struct StrokeMessage: Codable, Sendable {
    let id: UUID
    let points: [CGPointCodable]
    let color: ColorCodable
    let lineWidth: Double

    struct CGPointCodable: Codable, Sendable {
        let x: Double
        let y: Double
    }

    struct ColorCodable: Codable, Sendable {
        let red: Double
        let green: Double
        let blue: Double
        let alpha: Double
    }
}

struct ClearCanvasMessage: Codable, Sendable {
    let timestamp: Date
}
```

### Drawing Manager

```swift
import GroupActivities

@Observable
@MainActor
final class DrawingManager {
    private var session: GroupSession<DrawTogetherActivity>?
    private var reliableMessenger: GroupSessionMessenger?
    private var unreliableMessenger: GroupSessionMessenger?
    private var tasks: [Task<Void, Never>] = []

    var strokes: [StrokeMessage] = []
    var isConnected = false

    func startObserving() {
        Task {
            for await session in DrawTogetherActivity.sessions() {
                configureSession(session)
            }
        }
    }

    private func configureSession(
        _ session: GroupSession<DrawTogetherActivity>
    ) {
        // Clean up previous session
        cleanUp()

        self.session = session
        self.reliableMessenger = GroupSessionMessenger(
            session: session,
            deliveryMode: .reliable
        )
        self.unreliableMessenger = GroupSessionMessenger(
            session: session,
            deliveryMode: .unreliable
        )

        // Observe state
        let stateTask = Task {
            for await state in session.$state.values {
                switch state {
                case .joined:
                    isConnected = true
                case .invalidated:
                    isConnected = false
                    cleanUp()
                default:
                    break
                }
            }
        }
        tasks.append(stateTask)

        // Observe strokes (unreliable for speed)
        let strokeTask = Task {
            guard let messenger = unreliableMessenger else { return }
            for await (stroke, _) in messenger.messages(of: StrokeMessage.self) {
                strokes.append(stroke)
            }
        }
        tasks.append(strokeTask)

        // Observe clear messages (reliable for correctness)
        let clearTask = Task {
            guard let messenger = reliableMessenger else { return }
            for await (_, _) in messenger.messages(of: ClearCanvasMessage.self) {
                strokes.removeAll()
            }
        }
        tasks.append(clearTask)

        session.join()
    }

    func sendStroke(_ stroke: StrokeMessage) async {
        strokes.append(stroke)
        try? await unreliableMessenger?.send(stroke, to: .all)
    }

    func clearCanvas() async {
        strokes.removeAll()
        try? await reliableMessenger?.send(
            ClearCanvasMessage(timestamp: Date()),
            to: .all
        )
    }

    func leave() {
        session?.leave()
        cleanUp()
    }

    private func cleanUp() {
        tasks.forEach { $0.cancel() }
        tasks.removeAll()
        session = nil
        reliableMessenger = nil
        unreliableMessenger = nil
        isConnected = false
    }
}
```

## Full SharePlay Manager

### Generic Activity Manager

```swift
import GroupActivities

@Observable
@MainActor
final class SharePlayManager<Activity: GroupActivity> {
    private(set) var session: GroupSession<Activity>?
    private(set) var messenger: GroupSessionMessenger?
    private(set) var journal: GroupSessionJournal?

    private(set) var activeParticipants: Set<Participant> = []
    private(set) var localParticipant: Participant?
    private(set) var isJoined = false

    private var tasks: [Task<Void, Never>] = []

    // GroupSessionJournal requires iOS/iPadOS/tvOS 17+, macOS 14+,
    // or visionOS 1+. Gate this property if your deployment target is older.

    func startObserving() {
        Task {
            for await session in Activity.sessions() {
                configure(session)
            }
        }
    }

    private func configure(_ session: GroupSession<Activity>) {
        reset()

        self.session = session
        self.messenger = GroupSessionMessenger(session: session)
        self.journal = GroupSessionJournal(session: session)
        self.localParticipant = session.localParticipant

        let stateTask = Task {
            for await state in session.$state.values {
                switch state {
                case .joined:
                    isJoined = true
                case .invalidated:
                    isJoined = false
                    reset()
                default:
                    break
                }
            }
        }
        tasks.append(stateTask)

        let participantTask = Task {
            for await participants in session.$activeParticipants.values {
                activeParticipants = participants
            }
        }
        tasks.append(participantTask)

        session.join()
    }

    func leave() {
        session?.leave()
        reset()
    }

    func end() {
        session?.end()
        reset()
    }

    private func reset() {
        tasks.forEach { $0.cancel() }
        tasks.removeAll()
        session = nil
        messenger = nil
        journal = nil
        isJoined = false
        activeParticipants = []
    }
}
```

### Type-Safe Message Handling

```swift
extension SharePlayManager {
    func send<T: Codable>(_ message: T) async throws {
        guard let messenger else {
            throw SharePlayError.notConnected
        }
        try await messenger.send(message, to: .all)
    }

    func send<T: Codable>(_ message: T, to participant: Participant) async throws {
        guard let messenger else {
            throw SharePlayError.notConnected
        }
        try await messenger.send(message, to: .only(participant))
    }

    func messages<T: Codable>(of type: T.Type) -> AsyncThrowingStream<(T, Participant), Error> {
        AsyncThrowingStream { continuation in
            let task = Task {
                guard let messenger else {
                    continuation.finish()
                    return
                }
                for await (message, context) in messenger.messages(of: type) {
                    continuation.yield((message, context.source))
                }
                continuation.finish()
            }
            continuation.onTermination = { _ in task.cancel() }
        }
    }
}

enum SharePlayError: Error {
    case notConnected
}
```

## SwiftUI SharePlay Integration

Use this section when surfacing activities through SwiftUI controls. A custom
button works best when a FaceTime call or Messages conversation is already
active. Use `ShareLink`, UIKit/AppKit share sheets, or
`GroupActivitySharingController` when the user needs to choose participants.

### ShareLink and AirDrop

SwiftUI `ShareLink`, SharePlay over AirDrop, and system share sheets require
the shared item or activity to conform to `Transferable`. Keep the transferable
payload small; share IDs and URLs, then load heavy content after joining.

```swift
import CoreTransferable
import GroupActivities
import SwiftUI

extension WatchTogetherActivity: Transferable {
    static var transferRepresentation: some TransferRepresentation {
        GroupActivityTransferRepresentation { activity in
            activity
        }
    }
}

ShareLink(
    item: WatchTogetherActivity(movieID: movieID, movieTitle: movieTitle),
    preview: SharePreview(movieTitle)
)
```

### SharePlay Button

```swift
import GroupActivities
import SwiftUI

struct SharePlayButton<Activity: GroupActivity>: View {
    let activity: Activity

    @State private var observer = GroupStateObserver()

    var body: some View {
        if observer.isEligibleForGroupSession {
            Button {
                Task {
                    try await startActivity()
                }
            } label: {
                Label("SharePlay", systemImage: "shareplay")
            }
        }
    }

    private func startActivity() async throws {
        switch await activity.prepareForActivation() {
        case .activationPreferred:
            _ = try await activity.activate()
        case .activationDisabled:
            break
        case .cancelled:
            break
        @unknown default:
            break
        }
    }
}
```

### SharePlay Status Indicator

```swift
struct SharePlayStatusView: View {
    let participantCount: Int
    let isConnected: Bool

    var body: some View {
        if isConnected {
            HStack {
                Image(systemName: "shareplay")
                    .foregroundStyle(.green)
                Text("\(participantCount) connected")
                    .font(.caption)
                    .foregroundStyle(.secondary)
            }
        }
    }
}
```

### Full Activity View

Create the session manager at an app, scene, or feature coordinator boundary and
inject it into SwiftUI. The content view should use the manager, not own the
`sessions()` observation lifecycle.

```swift
struct SharedMovieView: View {
    @Environment(SharePlayManager<WatchTogetherActivity>.self) private var manager

    let movieID: String
    let movieTitle: String

    var body: some View {
        VStack {
            // Movie content here

            HStack {
                SharePlayButton(
                    activity: WatchTogetherActivity(
                        movieID: movieID,
                        movieTitle: movieTitle
                    )
                )

                if manager.isJoined {
                    SharePlayStatusView(
                        participantCount: manager.activeParticipants.count,
                        isConnected: true
                    )
                }
            }
        }
        .task { manager.startObserving() }
        .onDisappear { manager.leave() }
    }
}
```

## Custom Activity with State Sync

### Quiz Game Example

```swift
import GroupActivities

struct QuizActivity: GroupActivity {
    let quizID: String

    var metadata: GroupActivityMetadata {
        var meta = GroupActivityMetadata()
        meta.title = "Quiz Time"
        meta.type = .generic
        return meta
    }
}

// Messages
struct QuizQuestion: Codable, Sendable {
    let questionID: String
    let text: String
    let options: [String]
}

struct QuizAnswer: Codable, Sendable {
    let questionID: String
    let selectedOption: Int
}

struct QuizState: Codable, Sendable {
    let currentQuestionIndex: Int
    let scores: [String: Int]  // participant ID -> score
}
```

### Quiz Manager

```swift
@Observable
@MainActor
final class QuizManager {
    private var session: GroupSession<QuizActivity>?
    private var messenger: GroupSessionMessenger?
    private var tasks: [Task<Void, Never>] = []

    var currentQuestion: QuizQuestion?
    var scores: [String: Int] = [:]
    var isHost = false

    func configureSession(_ session: GroupSession<QuizActivity>) {
        self.session = session
        self.messenger = GroupSessionMessenger(session: session)
        self.isHost = session.isLocallyInitiated

        let questionTask = Task {
            guard let messenger else { return }
            for await (question, _) in messenger.messages(of: QuizQuestion.self) {
                currentQuestion = question
            }
        }
        tasks.append(questionTask)

        let answerTask = Task {
            guard let messenger else { return }
            for await (answer, context) in messenger.messages(of: QuizAnswer.self) {
                processAnswer(answer, from: context.source)
            }
        }
        tasks.append(answerTask)

        // Send current state to late joiners
        let participantTask = Task {
            var known: Set<Participant> = []
            for await participants in session.$activeParticipants.values {
                let newJoiners = participants.subtracting(known)
                for joiner in newJoiners {
                    if isHost, let question = currentQuestion {
                        try? await messenger?.send(question, to: .only(joiner))
                    }
                    let state = QuizState(
                        currentQuestionIndex: 0,
                        scores: scores
                    )
                    try? await messenger?.send(state, to: .only(joiner))
                }
                known = participants
            }
        }
        tasks.append(participantTask)

        session.join()
    }

    func submitAnswer(option: Int) async {
        guard let question = currentQuestion else { return }
        let answer = QuizAnswer(
            questionID: question.questionID,
            selectedOption: option
        )
        try? await messenger?.send(answer, to: .all)
    }

    private func processAnswer(_ answer: QuizAnswer, from participant: Participant) {
        // Score the answer and update scores
        let key = participant.id.uuidString
        scores[key, default: 0] += 1
    }
}
```

## Participant Tracking

### Tracking Who Has Seen What

```swift
@Observable
@MainActor
final class ParticipantTracker {
    private var knownParticipants: Set<Participant> = []

    func handleParticipantUpdate(
        _ activeParticipants: Set<Participant>,
        sendStateTo: (Participant) async throws -> Void
    ) async {
        let joined = activeParticipants.subtracting(knownParticipants)
        let left = knownParticipants.subtracting(activeParticipants)

        for participant in joined {
            print("Participant joined: \(participant.id)")
            try? await sendStateTo(participant)
        }

        for participant in left {
            print("Participant left: \(participant.id)")
        }

        knownParticipants = activeParticipants
    }
}
```

### Nearby Participant Detection

On visionOS 26+, nearby Apple Vision Pro participants can join the same group
activity. The core session, messenger, and journal APIs treat nearby and
FaceTime participants the same; use `isNearbyWithLocalParticipant` only when UI
or spatial placement needs to distinguish them:

```swift
for participant in session.activeParticipants {
    if participant.isNearbyWithLocalParticipant {
        print("\(participant.id) is nearby")
    }
}
```

This is useful for visionOS spatial activities where you want to offer
different experiences for co-located vs. remote participants.
