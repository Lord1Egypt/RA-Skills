# Errors — Throwing, Typed Throws, Result, Cancellation

Swift's error handling is a second return channel, not exceptions: `throws` is part of the signature, propagation is explicit at every call, and there is no stack unwinding to fear. Design errors as data the caller can act on — anything else is a log line pretending to be control flow.

## Choosing the Channel

| Situation | Channel |
|---|---|
| The caller can plausibly recover or explain the failure | `throws` |
| Failure is expected and one-of-two, and the caller always branches | Return an enum or `Result` |
| Absence is the only information | Optional (`optionals.md`) |
| The precondition was violated by the programmer | `precondition` / `fatalError` — not an error |
| The operation was cancelled | Rethrow `CancellationError`, never convert it to a domain error |

- `Result` is for **storing** a completed outcome (a cache entry, a callback payload, a per-element result in a batch). Do not use it as the return type of a function you can just make `throws`; the caller then writes `switch` where `try` would do.
- Bridge with `Result { try work() }` and `try result.get()`.

## Designing the Error Type

- One enum per subsystem, cases named for what happened, payloads carrying what the caller needs: `case rateLimited(retryAfter: Duration)` beats `case failure(String)`.
- Add `var isRetryable: Bool` (or a `RetryPolicy` computed property) on the enum instead of matching cases at every call site.
- `LocalizedError` supplies `errorDescription` for user-visible text; a raw `String(describing: error)` in the UI leaks type names.
- Every Swift `Error` bridges to `NSError` with a domain derived from the type and a code from the case index — so **reordering cases changes the code**. Pin the codes explicitly when anything persists or transmits them.
- Wrap, do not swallow: `case storage(underlying: any Error)` keeps the cause for the log while giving the caller a stable case to match.

## Typed Throws

`swift >=6.0` allows `func f() throws(ParseError)`. It is precise and lets exhaustive `catch` compile without a default clause.

- Good fit: leaf, self-contained operations (parsing, validation, a small state machine) where the error set is genuinely closed.
- Bad fit: anything that calls into other subsystems — you end up mapping every downstream error into your enum, which is churn without benefit.
- `throws` remains shorthand for `throws(any Error)`; `rethrows` is unchanged.
- Do not typed-throw a public API's errors unless the enum is frozen: adding a case is a source break for exhaustive catches.

## Propagation Mechanics

- `try` marks the call, not the failure: `try a(b(), c())` marks the whole expression even though only one of them throws.
- `try?` converts to optional and discards the error; acceptable only when the error genuinely carries nothing (a lookup you will retry anyway). `try?` on a function returning `T?` flattens to `T?` since Swift 5 — no double optional.
- `try!` is a crash with the error message lost. Test code and provably-impossible cases only, and subject to `force_unwrap_policy` (SKILL.md Configuration).
- `rethrows` propagates only when the caller's closure throws, so `map`-style helpers stay `try`-free for non-throwing closures. Write it on every higher-order function that takes a throwing closure.
- Throwing from a closure requires the closure type to be marked `throws`; `@escaping () throws -> Void` and `() -> Void` are different types and will not substitute.

## defer

- Runs on every exit from the scope: return, throw, break. LIFO when there are several.
- Inside a loop it runs at the end of **each iteration**, not at the end of the loop — the usual surprise when it is used for cleanup of an accumulated resource.
- A `defer` that itself can fail has nowhere to report; keep them infallible.
- Canonical use: pairing acquire/release where the release must survive early returns — continuation cleanup that must run on every exit path is the same shape.

## Errors and Concurrency

- `CancellationError` is the one error you must not treat as a domain failure. A `catch { return fallback }` around cancellable work makes the task uncancellable and every enclosing `TaskGroup` hang until it finishes anyway (SKILL.md Traps).

```swift
do { try await work() }
catch is CancellationError { throw CancellationError() }
catch { fallback() }
```

- An error thrown inside `Task { }` whose value nobody awaits disappears completely — no console output, no crash (`concurrency.md`).
- In a `TaskGroup`, the first thrown error cancels the siblings and propagates; results already produced are lost unless you collected them as you went.
- Errors crossing an actor boundary must be `Sendable`; an error enum with a non-Sendable payload will not compile in language mode 6.
- Retry loops need three things: a cap, a delay that respects cancellation (`try await Task.sleep`), and an "is this retryable" predicate on the error type. Retrying a 400 forever is the classic version of missing the third.

## Boundaries

- Convert at the boundary, once. Network layer throws `NetworkError`; the repository maps it to a domain error; the UI maps that to a message. Skipping a layer means `URLError` codes end up in view code.
- Log where you have context, handle where you have authority. Logging the same error at four layers produces four alerts for one incident.
- An empty `catch {}` is never acceptable in shipped code (SKILL.md Output Gates). If the error is genuinely ignorable, say so: `catch { logger.debug("ignored: \(error)") }`.
- Objective-C `NSError**` methods import as `throws`, and a method returning a `BOOL` plus error imports as a non-returning `throws` function. A bridged method that returns nil **and** no error throws a generic error — check both when the failure looks empty.
