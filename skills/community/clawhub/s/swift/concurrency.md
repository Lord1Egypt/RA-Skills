# Concurrency — async/await, Actors, Sendable

Mental model: `await` is a **suspension point**, not a thread hop you control. At every `await` the current task may pause, other work on the same actor may run, and the code after it may resume on a different thread. Almost every concurrency bug in Swift is a wrong assumption about what survives a suspension.

## Structured vs Unstructured

| Form | Cancellation | Errors | Use |
|---|---|---|---|
| `async let` | Cancelled when the enclosing scope exits | Propagate at the `await` | 2-5 known parallel calls |
| `withTaskGroup` / `withThrowingTaskGroup` | Children cancelled with the group | Rethrown from `next()`/iteration | N dynamic parallel calls |
| `Task { }` | NOT cancelled by scope exit; you must hold and cancel it | Silently dropped unless you `await` the value | Bridging from sync code, stored work |
| `Task.detached { }` | Same as `Task`, plus inherits no actor, no priority, no task-locals | Same | Rare: genuinely unrelated background work |

- `async let` starts the child immediately at the declaration, not at the `await`. Declare three and await them in order for real parallelism; declare one and await it on the next line and you got none.
- An `async let` you never `await` is implicitly cancelled and awaited at scope exit — the runtime guarantees it (SE-0317), not a compiler diagnostic, so nothing warns you and the work may already have cost you.
- `TaskGroup` results arrive in completion order, not submission order. Need order? Return `(index, value)` and sort.
- Task groups do not limit concurrency by themselves. Cap it: add the first `n` tasks, then add one more each time `next()` returns.

## Cancellation Is Cooperative

- Cancellation sets a flag. Nothing stops on its own. `Task.isCancelled` to bail quietly, `try Task.checkCancellation()` to throw.
- `Task.sleep` throws on cancellation; `Thread.sleep` does not, and it blocks a pool thread besides (SKILL.md rule 4).
- A `catch` that swallows `CancellationError` makes the task uncancellable — rethrow it before handling domain errors (`errors.md`).
- Check cancellation between loop iterations and before expensive steps, not once at the top.
- `withTaskCancellationHandler` bridges to APIs with their own cancel (URLSession tasks, database handles). The handler can run on any thread and may run before the operation starts — keep it small and idempotent.

## Actors

- An actor serializes access to its own mutable state. It is not a thread, not a queue, and gives no ordering guarantee across suspensions.
- **Reentrancy** is the trap (SKILL.md rule 6): between your `await` and its resumption another call may have mutated everything you read. Re-read state after every suspension; never carry "the array still has 3 items" across one.
- Every access from outside is `await`, including reads — an actor property is not a cheap getter.
- Deduplicate concurrent work by caching the `Task`, not a boolean:

```swift
actor ImageLoader {
    private var inFlight: [URL: Task<Data, Error>] = [:]
    func load(_ url: URL) async throws -> Data {
        if let task = inFlight[url] { return try await task.value }
        let task = Task { try await URLSession.shared.data(from: url).0 }
        inFlight[url] = task
        defer { inFlight[url] = nil }
        return try await task.value
    }
}
```

- `nonisolated` members cannot touch isolated stored properties; use them for pure computation and for synchronous protocol conformances — `Hashable`, `Equatable`, `CustomStringConvertible` cannot be async, so on an actor they must be `nonisolated` over immutable data.
- Actor `deinit` is nonisolated and cannot touch isolated state. Clean up explicitly before the last reference goes.
- `@globalActor` gives a shared isolation domain (`@MainActor` is the built-in one). One custom global actor per subsystem beats scattered locks; ten of them recreate the queue spaghetti you left behind.

## MainActor

- `@MainActor` means "runs on the main executor", which is a hop, not an immediate call. Code after `await someMainActorCall()` is on main, but time has passed and state may have changed.
- Annotate the type, not each method, for UI types — one annotation, no isolation islands.
- `MainActor.assumeIsolated { }` asserts you are already on main and runs synchronously, trapping if you are not. It is the correct bridge from synchronous framework callbacks documented as main-thread; `DispatchQueue.main.async` from inside async code is not (SKILL.md Traps).
- A `@MainActor` closure handed to a non-isolated API must be `@Sendable` as well, or the compiler rejects the escape.

## Sendable

- `Sendable` = safe to hand across isolation domains. Structs and enums of Sendable members conform automatically when they are non-public; **public types must state the conformance explicitly** — the omission is the usual "why won't my library's type cross?".
- Final classes with only immutable `let` properties of Sendable types can conform. Non-final classes cannot: a subclass could add mutable state.
- Closures: `@Sendable` forbids capturing non-Sendable state and captures by value. A `@Sendable` closure capturing a `var` copies it at creation — later changes are invisible inside.
- `@unchecked Sendable` rules: SKILL.md rule 7.
- Global and static `var` is a data race by definition. Preference order: make it `let`; put it on an actor or `@MainActor`; wrap it in `Mutex` (Synchronization module, `swift >=6.0`); last resort `nonisolated(unsafe)` with a comment naming who guarantees safety.
- `sending` parameters (`swift >=6.0`) transfer a non-Sendable value across an isolation boundary when the compiler can prove the sender gives up every reference — the escape hatch that replaces most `@unchecked`.

## Continuations — Bridging Callback APIs

```swift
func fetch() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        legacyFetch { data, error in
            if let data { continuation.resume(returning: data) }
            else { continuation.resume(throwing: error ?? URLError(.unknown)) }
        }
    }
}
```

- Exactly one resume on every path (SKILL.md rule 5). Delegate-style callbacks that can fire twice need a `hasResumed` flag under a lock.
- A continuation is not cancellable on its own. Pair it with `withTaskCancellationHandler` and cancel the underlying operation there.
- Never `await` inside the continuation body — that closure is synchronous by design.

## AsyncSequence and AsyncStream

- `AsyncStream`'s default buffering is unbounded: a fast producer with a slow consumer grows memory without limit. Choose explicitly — `.bufferingNewest(n)` for state, `.bufferingOldest(n)` for events that must not reorder.
- Always set `continuation.onTermination` to tear down the underlying source; omitting it is the standard "the observer keeps firing after the screen closed" leak.
- A `for await` loop owns the task until the sequence finishes. If it never finishes, neither does the task — cancel it, or use SwiftUI's `.task`, which cancels on disappear.
- `AsyncSequence` has no built-in `debounce`, `merge`, or `zip`; those live in swift-async-algorithms. Hand-rolling them is where subtle cancellation bugs are born.

## Performance and Threads

- The pool runs one thread per active core; blocking any of them is rule 4. Backtrace signatures: `debugging.md`.
- Actor hops are cheap but not free. A loop that calls an actor per element serializes on that actor — batch it (`await store.add(contentsOf: chunk)`) instead of awaiting per item.
- A `Task` inherits the caller's priority; `Task.detached` starts at default. Priority escalation exists across structured relationships, not across detached ones.
- `Task.yield()` inside a long compute loop lets other tasks in — the async equivalent of not hogging the runloop.
- Task creation costs an allocation: one task per element of a 100k array is slower than a task group with a bounded width.

## Value vs Reference Under Concurrency

- Structs cross isolation boundaries by copy and are Sendable when their members are — the cheapest way to make a type concurrency-safe is to stop making it a class.
- `array[0].mutate()` does not compile through a computed subscript on a non-mutable path; extract, mutate, reassign.
- `inout` is not a reference across concurrency: the write-back happens when the function returns, and passing the same variable as two `inout` arguments is an exclusivity trap.

## Migration From GCD and Combine

- `DispatchQueue.main.async` → `@MainActor`. Serial queue as a lock → `actor`. Concurrent queue with barriers → `actor`, or `Mutex` when the critical sections are tiny and non-async.
- `DispatchSemaphore` has no place in async code; in sync code it stays a blocking primitive that must never wait on async work.
- Combine `Publisher` → `AsyncSequence` via `.values`. Cancellation maps to task cancellation; `AnyCancellable`'s cancel-on-deinit behavior does not.
- Migrate leaves first: convert one callback API to async at its boundary, leave the callers alone, and let the async surface grow inward.
