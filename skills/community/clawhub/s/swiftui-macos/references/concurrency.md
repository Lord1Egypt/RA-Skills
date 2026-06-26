# Swift Concurrency

## Scheduling Cost Hierarchy

From cheapest to most expensive:

| Pattern | Cost | Use when |
|---|---|---|
| `MainActor.assumeIsolated { }` | Near-zero (assertion + direct call) | Callbacks known to be on main (e.g., NotificationCenter with `queue: .main`, AppKit delegates) |
| `await MainActor.run { }` | No allocation, reuses existing task | Already in async context, need main actor access |
| `DispatchQueue.main.async { }` | ~64B block allocation | Fire-and-forget from `@Sendable` or `nonisolated` closures (e.g., `onTermination` handlers) |
| `Task.immediate { @MainActor in }` | ~300-500B Task, no hop if already correct | Need Task semantics (cancellation, priority) with predictable ordering |
| `Task { @MainActor in }` | ~300-500B Task + always enqueues | Intentionally deferred execution with Task semantics |

**Anti-pattern: `Task { @MainActor in }` for synchronous code.**

Why it's worse than `DispatchQueue.main.async`:
- Each call is a raw `malloc` (~300-500 bytes) with **no pooling or recycling** — compared to ~64B for a dispatch block
- The closure requires `sending`, forcing `Sendable` conformance on all captured values — compile-time friction for zero runtime benefit (`sending` has no runtime cost)
- Multiple rapid calls create **separate Task objects and separate dispatch enqueues** — there is no coalescing mechanism
- Both end up at the same `dispatch_async_f(dispatch_get_main_queue(), ...)` call

Use `DispatchQueue.main.async` for fire-and-forget main-thread dispatch. Use `Task { @MainActor in }` only when you need Task semantics (cancellation, priority, task-locals).

## Actor Isolation

Two independent project settings affect concurrency behavior. Check which are enabled before reviewing.

### Task Isolation Inheritance

`Task { }` inherits the **caller's** isolation context:

- Called from `@MainActor` code → runs on MainActor
- Called from a custom actor → runs on that actor
- Called from `nonisolated` code → inherits the caller's context, which may itself be MainActor (e.g., if the `nonisolated` function was called from MainActor with SE-0461 enabled)

This means `Task { }` does **not** guarantee background execution. When `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` is set, most code is implicitly MainActor-isolated, so `Task { }` almost always stays on MainActor.

**`Task.detached { }`** breaks inheritance entirely — always runs on the global concurrent pool regardless of where it's called from. Use for CPU-bound work that genuinely needs to leave the current actor.

`Task.detached` is not inherently bad — it's the correct tool for breaking actor inheritance. But don't use it just to "run in background" when a `nonisolated` function would suffice.

### nonisolated(nonsending) (SE-0461)

**Requires opt-in** via `SWIFT_UPCOMING_FEATURE_NONISOLATED_NONSENDING_BY_DEFAULT`. Not yet the language default. Independent of MainActor default isolation.

This changes where `nonisolated async` functions execute:

**Without SE-0461** (legacy behavior): `nonisolated async func fetch()` hops to the global concurrent pool — an arbitrary background thread — even when called from MainActor.

**With SE-0461 enabled**: `nonisolated` async functions are implicitly `nonisolated(nonsending)` — they run on the **caller's executor**, not the global pool:

```swift
nonisolated func fetchData() async -> Data {
    // Called from MainActor? Runs on MainActor. No thread hop.
    // Called from another actor? Runs on that actor.
    await URLSession.shared.data(from: url).0
}
```

With the feature enabled, `nonisolated` no longer means "runs on a background thread" — it means "not tied to any specific actor, runs wherever the caller is." Without it, `nonisolated async` functions still hop to the global pool.

### @concurrent

`@concurrent` explicitly opts a function into running on the global concurrent pool, regardless of the caller's isolation. It implicitly makes the function `nonisolated`:

```swift
@concurrent
func decode<T: Decodable>(_ data: Data) async throws -> T {
    // Always runs on the global pool — guaranteed off MainActor
}
```

Most useful with SE-0461 enabled (where `nonisolated` alone would stay on the caller's executor). Without SE-0461, plain `nonisolated` already runs on the global pool — but `@concurrent` makes intent explicit and future-proofs the code.

Can be applied to functions on isolated types to opt specific methods out:

```swift
@MainActor
class ViewModel {
    @concurrent
    func heavyComputation(_ input: Data) async -> Result {
        // Runs on global pool despite the class being @MainActor
    }
}
```

Cannot be combined with explicit isolation (`@concurrent @MainActor` or `@concurrent nonisolated(nonsending)` are errors — conflicting isolation).

### sending (SE-0430)

`sending` is a parameter convention for transferring exclusive ownership across isolation boundaries. It's **purely compile-time** — zero runtime cost, no copies, no reference counting.

You encounter it when:
- `Task.init`'s closure parameter requires `sending` — all captured values must be `Sendable` or exclusively owned by the closure
- Functions that cross actor boundaries may require `sending` parameters

```swift
// Task.init signature (simplified):
init(operation: sending @escaping @isolated(any) () async -> Success)

// This means captures must be Sendable:
let nonSendable = MyNonSendableType()
Task { use(nonSendable) }  // Error: captured value is not Sendable

// The compile-time check prevents data races:
var mutable = [1, 2, 3]
Task { @MainActor in mutable.append(4) }
print(mutable)  // Error: 'mutable' used after being sent
```

`sending` prevents the caller from using the value after passing it — eliminating data races at compile time with no runtime overhead.

This is why `Task { @MainActor in }` creates friction with non-Sendable captures. `DispatchQueue.main.async` uses `@Sendable @convention(block)` (with `@preconcurrency` for backwards compatibility) — a different mechanism with its own constraints. For cases where Sendable enforcement is genuinely too restrictive, `DispatchQueue.asyncUnsafe` (macOS 14+) relaxes it entirely — but correctness is then your responsibility.

## Modern Task Patterns

**Named tasks** (SE-0469) for debuggability:

```swift
Task("Fetch User Profile") {
    let profile = try await api.fetchProfile(userID)
    self.profile = profile
}
```

**Caller isolation inheritance** (SE-0420) with **`#isolation`**:

`#isolation` captures the caller's actor isolation context at the call site. Combined with an `isolated (any Actor)?` parameter, it lets functions run on whatever actor the caller is on — no hop:

```swift
func processItems(
    isolation: isolated (any Actor)? = #isolation
) async -> [Result] {
    // Called from MainActor? Runs on MainActor.
    // Called from a custom actor? Runs on that actor.
    // No thread hop in either case.
    items.map { process($0) }
}
```

This is critical for library code that shouldn't assume or force a specific isolation context. Without it, the function would either require `@MainActor` annotation (too restrictive) or hop to the global pool (unnecessary overhead).

**Task.immediate** (SE-0472) — synchronous start, no dispatch hop:

```swift
Task.immediate { @MainActor in
    updateUI()
}
```

Key semantics:
- If already on the target executor: **runs synchronously inline** up to the first suspension point, then falls back to normal scheduling. This means mutations are visible immediately after the call — unlike `Task { }` which always enqueues (subsequent code runs *before* the task body).
- If not on the target executor: falls back to normal enqueue (same as `Task { }`).
- Full Task allocation (~300-500B) happens either way — the savings are in avoiding the dispatch hop, not the allocation.

```swift
// Task { } — always deferred, ordering not guaranteed
print("1")
Task { @MainActor in print("2") }
print("3")
// Output: 1, 3, 2

// Task.immediate — synchronous when isolation matches
print("1")
Task.immediate { @MainActor in print("2") }  // already on MainActor
print("3")
// Output: 1, 2, 3
```

Use `Task.immediate` when you need Task semantics (cancellation, task-locals) but want predictable execution ordering and avoid unnecessary hops.

**Isolated deinit** (SE-0471):

Without `isolated deinit`, the deinitializer of an actor-isolated class runs in a `nonisolated` context — you cannot access any of the class's isolated stored properties, call isolated methods, or perform cleanup that requires the actor. This forces workarounds like fire-and-forget `Task` blocks (which may never execute if the process is shutting down) or simply skipping cleanup with a comment like "the Task will be cancelled when its reference is dropped."

`isolated deinit` runs the deinitializer **on the type's actor**. For `@MainActor` types, this means the deinit body executes on the main thread with full access to all isolated state:

```swift
@MainActor
final class ResourceOwner {
    private var observationTasks: [Task<Void, Never>] = []
    private var notificationObserver: Any?
    let connection: NonSendableConnection

    isolated deinit {
        // All of these are MainActor-isolated — safe to access here
        for task in observationTasks {
            task.cancel()
        }
        if let observer = notificationObserver {
            NotificationCenter.default.removeObserver(observer)
        }
        connection.close()
    }
}
```

**When to use:**
- Cancelling stored `Task` references that would otherwise leak
- Closing non-Sendable connections, file handles, or resources
- Removing notification observers or KVO registrations
- Any cleanup that accesses `@MainActor`-isolated stored properties

**When NOT needed:**
- Types with no cleanup requirements (most SwiftUI views, simple data containers)
- Types where all resources are automatically managed (ARC handles reference cleanup, `deinit` of child objects handles their own teardown)
- Actors (custom actors already run `deinit` on their own executor — `isolated deinit` is for classes with *inherited* isolation like `@MainActor`)

**Runtime behavior**: The runtime schedules the deinit body on the appropriate executor. If the last reference is dropped from the correct actor, the deinit runs synchronously inline (no hop). If dropped from a different context, the runtime enqueues it — the object's deallocation is deferred until the deinit body completes on the correct actor. This means the object may live slightly longer than expected when dropped off-actor.

## Periodic Background Work

**Do not use polling Task loops for periodic work.** A `while !Task.isCancelled { await work(); try await Task.sleep(for: .minutes(15)) }` loop wakes the CPU on a fixed schedule, cannot be coalesced with other system activity, and ignores Low Power Mode.

Use `NSBackgroundActivityScheduler` instead — the system chooses optimal execution times:

```swift
let activity = NSBackgroundActivityScheduler(identifier: "com.myapp.sync")
activity.repeats = true
activity.interval = 15 * 60  // 15 minutes
activity.tolerance = 5 * 60  // system can shift ±5 min for coalescing
activity.qualityOfService = .utility

activity.schedule { completion in
    Task {
        await performSync()
        completion(.finished)
    }
}
```

Benefits over polling loops:
- System coalesces with other scheduled activities (fewer wake-ups)
- Defers work during high system load or Low Power Mode
- `tolerance` enables timer coalescing at the kernel level
- Respects App Nap when the app is not visible

Reserve polling `Task.sleep` loops for work that must happen at precise intervals regardless of system state (e.g., UI timers, keep-alive pings for active connections).

## Task Cancellation

Always track tasks for cancellation and clean up:

```swift
@State private var pollingTask: Task<Void, Never>?

var body: some View {
    content
        .task { await load() }  // Preferred: auto-cancels on disappear
}

// When .task isn't sufficient (user-triggered, needs restart):
func startPolling() {
    pollingTask?.cancel()
    pollingTask = Task {
        while !Task.isCancelled {
            await poll()
            try? await Task.sleep(for: .seconds(30))
        }
    }
}
```

Always check `Task.isCancelled` after `await` or `sleep` before continuing work.

## AsyncStream Bridging

Use `AsyncStream` to bridge delegate/callback-based AppKit APIs into structured concurrency. This is the correct pattern for converting imperative AppKit callbacks into values a SwiftUI view or manager can consume.

```swift
@Observable @MainActor
final class DownloadManager {
    private(set) var downloads: [Download] = []

    func observeDownloads(session: URLSession) -> AsyncStream<URLSessionDownloadTask> {
        AsyncStream { continuation in
            let delegate = DownloadDelegate(continuation: continuation)
            // Store delegate strongly — the stream owns its lifetime
            self.sessionDelegate = delegate
            session.delegate = delegate

            continuation.onTermination = { @Sendable _ in
                // Fires on an ARBITRARY thread — use DispatchQueue, not Task
                DispatchQueue.main.async {
                    session.invalidateAndCancel()
                }
            }
        }
    }
}
```

**`onTermination` isolation**: `AsyncStream.onTermination` fires on whichever thread cancels the task or drops the last reference — it's explicitly `@Sendable`, not actor-isolated. Use `DispatchQueue.main.async` for MainActor cleanup, not `Task { @MainActor in }` (more overhead for the same `dispatch_async_f` call) and not `MainActor.assumeIsolated` (will crash if not already on main).

For observing `@Observable` property changes in non-view contexts, use `Observations {}` (see `references/observation.md`) instead of building manual AsyncStream wrappers.

## Rules

- Prefer `async`/`await` APIs over closure-based variants.
- Never use `Task.sleep(nanoseconds:)` — use `Task.sleep(for:)`.
- Flag mutable shared state not protected by an actor (unless MainActor default isolation covers it).
- `DispatchQueue.main.async` is acceptable for fire-and-forget from `@Sendable` contexts — don't dogmatically replace with `Task { @MainActor in }`, which costs more.
- For periodic background work, prefer `NSBackgroundActivityScheduler` over polling Task loops. See "Periodic Background Work" section above.
