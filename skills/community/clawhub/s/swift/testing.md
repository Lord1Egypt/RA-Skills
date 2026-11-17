# Testing — Swift Testing, XCTest, and Killing Flakiness

Two frameworks coexist. **Swift Testing** (`@Test`, `#expect`, `#require`) is the default for new code; **XCTest** still owns UI automation and performance measurement, so most real projects run both. Which half of this file applies is set by `test_framework` (SKILL.md Configuration).

## Swift Testing

```swift
import Testing

@Suite("Cart") struct CartTests {
    @Test func emptyCartTotalsZero() {
        #expect(Cart().total == 0)
    }

    @Test(arguments: [(1, 10), (3, 30), (0, 0)])
    func totalScalesWithQuantity(qty: Int, expected: Int) {
        #expect(Cart(quantity: qty).total == expected)
    }

    @Test func loadsRemoteCart() async throws {
        let cart = try #require(await service.load(id: "abc"))
        #expect(cart.items.count == 2)
    }
}
```

- `#expect` records a failure and continues; `#require` throws and stops the test. Use `#require` for the preconditions the rest of the test depends on — the alternative is a cascade of confusing follow-on failures.
- `#expect` captures the sub-expressions, so a failure prints the actual operand values without you formatting anything.
- Parameterized tests run as separate cases with their own results; a table of cases beats a `for` loop inside one test, which stops at the first failure.
- `@Test(.disabled("reason"))`, `.enabled(if:)`, `.tags(...)`, `.timeLimit(...)` are traits; a disabled test with a reason survives review, a commented-out one does not.
- Errors: `#expect(throws: ParseError.self) { try parse(bad) }`. For the exact case, capture and compare.
- Suites run **in parallel in-process** by default, including within a type. Shared mutable global state that XCTest's process-level parallelism tolerated will now break; serialize a suite with `.serialized` while you fix it, not forever.
- Test types are structs by default and get a fresh instance per test, so `init`/`deinit` replace `setUp`/`tearDown`.

## XCTest, Where It Still Applies

- `async` test methods are supported: `func testX() async throws`. Prefer them to expectations wherever the API is async.
- Expectations for callback APIs: `wait(for:timeout:)` in sync tests, `await fulfillment(of:timeout:)` in async ones. A test with no wait and no `await` passes before the work finishes — the single most common false green.
- `expectation.expectedFulfillmentCount` for callbacks that fire n times; `assertForOverFulfill = true` to catch the ones that fire n+1.
- `setUpWithError`/`tearDownWithError` can throw; the non-throwing versions force you to swallow setup failures.
- `XCTUnwrap` over `!`: it fails the test with the file and line instead of crashing the whole test run.
- `XCTAssertEqual` on `Double` needs `accuracy:` — floating-point equality without a tolerance is a flake generator.
- XCTest parallelization runs test **classes** in separate processes on macOS and simulators; that hides shared-state bugs until the code moves to Swift Testing.

## The Flakiness Checklist

| Symptom | Cause | Fix |
|---|---|---|
| Passes locally, fails in CI, order-dependent | Hash-order dependence: `Set`/`Dictionary` iteration differs per process | Reproduce with `SWIFT_DETERMINISTIC_HASHING=1`, then sort before asserting |
| Passes alone, fails in a suite | Shared singleton or static mutable state | Inject the dependency; reset in `init`/`setUp`; `.serialized` only as a stopgap |
| Fails under load or on slow machines | A sleep standing in for synchronization | Await the actual signal (expectation, continuation, `AsyncStream`) — never `Task.sleep` as a barrier |
| Fails only on the first run of the day | A real date, timezone, or locale leaking in | Inject a clock and a fixed locale; assert on components, not formatted strings |
| Fails intermittently with no pattern | Genuine data race | Thread Sanitizer over the suite (`debugging.md`) |
| Async test that never fails, even when broken | No `await`, no expectation | Make the test `async` and await the result |

## Test Doubles Without a Mocking Framework

- Swift has no runtime mocking. Depend on a protocol, inject a stub struct that implements it. Two lines per method, zero magic, works on Linux.
- Closure-based stubs are lighter than a full type for one-off behavior: `struct StubLoader: Loading { var load: (URL) async throws -> Data }`.
- Spies record calls in an array; when the system under test is concurrent, that array needs isolation, or the spy itself races.
- `@testable import` exposes `internal` symbols and requires the target be built with testability (the debug default). It does **not** expose `private`; a test that needs `private` is a design signal.
- Time: inject a clock protocol rather than reading `Date()`. Swift's `Clock`/`ContinuousClock` makes this idiomatic, and a fake clock turns a 5-second retry test into a 5-millisecond one.

## What To Test in Swift Specifically

- Decoding against **captured real payloads** as fixtures, including the malformed ones you have seen in production (`codable.md`). A model test against handwritten JSON tests your imagination.
- Optional and error paths: the `else` branch of every `guard` that throws, and the retry predicate.
- Cancellation: start the operation, cancel it, assert it stopped and cleaned up. Almost nobody tests this, and it is where hangs are born.
- Concurrency invariants: run the operation N times concurrently in a task group and assert the final state. Combined with TSan this catches what unit tests never do.
- Equatable/Hashable consistency for types used as dictionary keys.

## Running and Diagnosing

- `swift test --filter CartTests` scopes a run; `--parallel`/`--no-parallel` toggles XCTest parallelism.
- A test that hangs shows nothing useful in the output. Attach and `bt all`, or add a `.timeLimit` trait so CI fails instead of stalling.
- Code coverage is a map of untested paths, not a score. Chasing the last 10% usually produces tests that assert the implementation instead of the behavior.
- Keep the suite under the threshold where people stop running it locally. Slow suites get skipped, and a skipped suite catches nothing.
