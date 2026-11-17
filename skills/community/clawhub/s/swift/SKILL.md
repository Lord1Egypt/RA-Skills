---
name: Swift
slug: swift
version: 1.0.3
description: Writes, debugs, and optimizes Swift — concurrency, ARC leaks, optionals, generics, SwiftUI state, and packages. Use when writing or reviewing Swift code, when a build won't type-check or the compiler "is unable to type-check this expression in reasonable time", when an app crashes on a force unwrap, an unowned reference, or EXC_BAD_ACCESS, when Swift 6 raises Sendable / actor-isolated / data-race errors, when a retain cycle keeps objects alive, when JSON fails to decode, when async code hangs or deadlocks, when SwiftUI state resets or views redraw too often, when XCTest or Swift Testing tests are flaky, when a Swift package won't resolve, or when bridging to Objective-C, C, or Linux. Not for Xcode signing and IDE settings, or App Store submission and iOS app lifecycle.
homepage: https://clawic.com/skills/swift
changelog: "Display name shown correctly"
metadata:
  clawdbot:
    emoji: 🦅
    requires:
      bins:
      - swift
    os:
    - darwin
    - linux
    displayName: Swift
    configPaths:
    - ~/Clawic/data/swift/
---

User preferences and memory live in `~/Clawic/data/swift/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/swift/` or `~/clawic/swift/`), move it to `~/Clawic/data/swift/`.

## When To Use

- Writing, reviewing, or refactoring Swift: models, protocols, generics, async code, SwiftUI views, packages
- Diagnosing a crash from its message, or a hang with no message: nil unwrap, arithmetic overflow, unowned dangling, exclusivity violation, continuation never resumed
- Fixing Swift 6 data-race errors, `Sendable` conformance failures, and actor-isolation diagnostics during a language-mode migration
- Chasing memory: retain cycles, objects that never `deinit`, growth Instruments blames on nothing
- Making builds and binaries faster: type-check blowups, generic bloat, ARC traffic, existential boxing
- Shipping Swift off Apple platforms: Linux and server builds, static linking, Foundation gaps, C interop
- Not for Xcode project settings, signing, or provisioning (→ `xcode`), and not for App Store review, app lifecycle, or platform frameworks (→ `ios`)

## Quick Reference

| Situation | Play |
|---|---|
| Crash with a Swift message ("Unexpectedly found nil", "Index out of range") | Decode it in Crash Messages below, then `debugging.md` for the chain |
| Crash with no message (EXC_BAD_ACCESS, bare SIGTRAP) | Memory Graph, zombies, then sanitizers → `debugging.md` |
| Object never deallocates, `deinit` never runs | Retain cycle: closure, delegate, timer, or observer → `arc.md` |
| "Sending value of non-Sendable type", "actor-isolated property" | `concurrency.md` for the rule, `swift6-migration.md` for the order to fix them in |
| Async code hangs with no error and no CPU | Continuation never resumed, or a blocked cooperative thread (rule 4) → `concurrency.md` |
| Upgrading a codebase to Swift 6 language mode | Per-target ratchet, not a big bang → `swift6-migration.md` |
| Too many `!`, `try!`, or IUOs; nil handling is noisy | `optionals.md` |
| Designing the failure channel: `throws` vs `Result` vs optional, typed throws, retry, cancellation | `errors.md` |
| JSON decode throws, keys missing, dates rejected | `codable.md` (fractional-second ISO 8601 is the usual one) |
| `any` vs `some` vs generic; a protocol default never gets called | `types.md` |
| Unicode, string indices, substrings, regex, locale-sensitive compare | `strings.md` |
| Array/Dictionary/Set behavior, ordering, or an O(n²) blowup | `collections.md` |
| Arithmetic traps at runtime, a numeric conversion crashes, floats compare wrong, or money needs a type | `numerics.md` |
| SwiftUI state resets, views redraw constantly, layout fights back | `swiftui.md` |
| Tests flaky, async tests pass before the work finishes | `testing.md` |
| Package won't resolve, resources missing, plugin blocked | `packages.md` |
| Slow build, slow runtime, oversized binary | `performance.md` |
| Objective-C, C, or C++ bridging; unsafe pointers; C callbacks | `interop.md` |
| Builds on macOS, fails on Linux or in a container | `linux.md` |
| Designing public API: naming, access control, availability, ABI | `api-design.md` |
| Property wrappers, result builders, macros, key paths | `metaprogramming.md` |
| Anything else | Reduce to the smallest file that still reproduces, compile with `-Onone`, and read the FIRST compiler error — the rest is usually cascade noise |

## Core Rules

1. **`!` is a deliberate crash, not a shortcut.** Recoverable nil → `guard let x else { return }`. Nil that means the program is already broken → `guard let x else { fatalError("config missing: \(key)") }`; the crash log then names the invariant instead of "Unexpectedly found nil while unwrapping an Optional value", which names nothing. Only IBOutlets and two-phase init justify an implicitly unwrapped `T!`.
2. **`weak` when the target can die first; `unowned` only when lifetimes are provably nested.** Test: can the referenced object deallocate while this reference exists? Yes → `weak` (becomes nil, no crash). Provably no, because it owns me → `unowned` (one less check, but a dangling read is an immediate crash rather than a nil). Escaping closures that touch `self`: `[weak self] in guard let self else { return }`. Non-escaping closures (`map`, `forEach`, `withLock`) never need a capture list — they cannot outlive the call.
3. **Reference type only for identity or lifecycle.** Default `struct`. Reach for `class`/`actor` when the thing has identity (two copies with equal fields are still different things), needs `deinit`, or is genuinely shared and mutated in place. Copy cost is not the tiebreaker: standard-library collections are copy-on-write, so a copy is a retain until someone writes (→ `types.md`).
4. **Never block a thread in the cooperative pool.** Swift concurrency runs one thread per active core, so on an 8-core machine 8 concurrent `DispatchSemaphore.wait()` calls inside `async` functions deadlock the whole process — no error, no timeout. Bridge blocking work out to a dedicated `DispatchQueue` or thread, and `await` everything else.
5. **Every `withCheckedContinuation` resumes exactly once on every path.** Twice = runtime trap ("SWIFT TASK CONTINUATION MISUSE"). Zero times = the awaiting task hangs forever with no error and no log. Audit every early return, every error branch, and every delegate callback that can fire more than once. Use the `Checked` variants everywhere except measured hot paths — the `Unsafe` ones diagnose nothing.
6. **Actor state is only consistent between `await`s.** Actors serialize access but are reentrant: any `await` inside an actor method lets other calls run and mutate state. Check-then-act across a suspension is a bug. Deduplicate in-flight work by storing the `Task` handle and returning it, not by flipping an `isLoading` flag around an `await`.
7. **`@unchecked Sendable` is a promise you must implement.** Legal only when every mutable stored property is reached through one lock (`Mutex`, `NSLock`, serial queue) with no path around it, and that lock is documented in the type. Otherwise the compiler stops checking and the race ships. Prefer making the type actually Sendable: `let` properties of Sendable types, or an `actor`.
8. **Budget the type-checker.** One unsolvable expression stalls its whole file. Build with `-Xfrontend -warn-long-expression-type-checking=500 -Xfrontend -warn-long-function-bodies=500` (milliseconds) and split whatever it flags — long `+` chains, mixed numeric literals, and large collection literals without type annotations are the repeat offenders. Annotating one intermediate `let` routinely takes a multi-second expression under the threshold.

## Crash Messages

Swift runtime traps surface as `EXC_BREAKPOINT` on arm64 and `EXC_BAD_INSTRUCTION` on x86_64; the human-readable line goes to stderr and lands in crash reports under Application Specific Information. No message at all means it is not a Swift trap — it is a memory error.

| Message | Means | First move |
|---|---|---|
| "Unexpectedly found nil while unwrapping an Optional value" | `!` or IUO on nil | Symbolicate to the line, then replace with `guard let` or a `fatalError` that names the invariant (rule 1) |
| "Index out of range" | Collection subscript past the end | Off-by-one, or an index captured before a mutation; `enumerated()` offsets are not slice indices (`collections.md`) |
| "Attempted to read an unowned reference but the object was already deallocated" | `unowned` outlived its target | Switch to `weak`; the lifetimes were not nested (rule 2) |
| "SWIFT TASK CONTINUATION MISUSE: … tried to resume its continuation more than once" | Continuation resumed twice | One-shot guard around the resume, or restructure the callback (rule 5) |
| "Simultaneous accesses to 0x…, but modification requires exclusive access" | Exclusivity violation | Two `inout` arguments aliasing one variable, or a mutating method re-entering itself; copy to a local first |
| "Fatal error: Duplicate keys of type 'X' were found in a Dictionary" | `==` and `hash(into:)` disagree, or duplicates in `uniqueKeysWithValues` | Hash exactly the fields `==` compares (`collections.md`) |
| "sort predicate is not a strict weak ordering" | Comparator inconsistent, or NaN in the data | Make `a<b`, `b<a`, and equality mutually exclusive; filter NaN before sorting |
| "Range requires lowerBound <= upperBound" | Computed range inverted | Clamp before constructing — empty ranges are legal, inverted ones trap |
| "Arithmetic operation '… + 1' (on type 'Int') results in an overflow" | Signed/unsigned overflow on `+`, `-`, `*`, or `<<` — traps in release too | Widen the accumulator or use `addingReportingOverflow`; `&+` only when wrapping IS the algorithm (`numerics.md`) |
| "Division by zero", "Division results in an overflow" | Integer `/` or `%` with a zero divisor, or `Int.min / -1` | Guard the divisor where it enters the system; floating-point division yields `.infinity` instead of trapping |
| "Negative value is not representable", "Double value cannot be converted to Int…" | Signed → unsigned, or a NaN/infinite/out-of-range `Double` → integer | `Int(exactly:)` for untrusted values, `Int(clamping:)` to saturate |
| EXC_BAD_ACCESS / KERN_INVALID_ADDRESS with no Swift message | Dangling pointer, over-release, `unowned(unsafe)`, or a C pointer escaping its `withUnsafe…` scope | Zombies first, then Address Sanitizer (`debugging.md`, `interop.md`) |
| Hang, low CPU, no message | Blocked cooperative thread (rule 4) or an unresumed continuation (rule 5) | Pause in the debugger, `bt all`, look for tasks parked on a semaphore or lock |

## Arithmetic Defaults

Swift traps on integer overflow and on impossible conversions in **release builds too** — arithmetic is a crash surface, not only a correctness one. Choose the operator that states the intent:

| Intent | Write | Not |
|---|---|---|
| Ordinary arithmetic on validated values | `+`, `-`, `*` | `&+` "to be safe": wrapping hides the bug the trap was reporting |
| Wrapping IS the algorithm (hash, checksum, PRNG, ring index) | `&+`, `&*`, `&<<` | `+`, which traps the first time real input wraps |
| Overflow is possible and recoverable | `let (v, o) = a.addingReportingOverflow(b)` | `do`/`catch` — arithmetic never throws, it traps |
| Convert a value that might not fit | `Int(exactly: x)` → nil, or `Int(clamping: x)` to saturate | `Int(x)`, which traps on out-of-range, NaN, and infinity |
| Money, prices, tax, invoice lines | Integer minor units, or `Decimal` built from a string | `Double` at any stage, including "only for display" |
| Compare two computed `Double`s | `abs(a - b) <= max(abs(a), abs(b)) * .ulpOfOne * 4` | `==`, which fails for `0.1 + 0.2` |
| Midpoint or average of two integers | `a + (b - a) / 2` | `(a + b) / 2`, which overflows near the bounds |
| Test evenness | `x.isMultiple(of: 2)` | `x % 2 == 1`, false for every negative odd number (`%` takes the dividend's sign) |
| Sort or reduce floats that may contain NaN | Filter on `isFinite` first | `sorted()`, which trips the strict-weak-ordering trap |

Overflow, conversion, floating-point and money depth: `numerics.md`.

## Output Gates

Before emitting Swift code, verify:

- No `!`, `try!`, `as!`, or IUO beyond what `force_unwrap_policy` allows, and each survivor has a reason a reviewer would accept
- Every escaping closure that touches `self` has a capture list; every `unowned` passes the nested-lifetime test (rule 2)
- Every `withCheckedContinuation` resumes exactly once on every path, thrown errors included
- Nothing blocking (`.wait()`, `Thread.sleep`, synchronous file or network I/O) inside an `async` function (rule 4)
- Mutable global or static state is `let`, actor-isolated, or explicitly justified — it is a data-race error in language mode 6
- Errors propagated or handled; no empty `catch {}`, and `CancellationError` rethrown rather than swallowed (`errors.md`)
- Every numeric conversion is `exactly:`/`clamping:` or provably in range, and no monetary value passes through `Double`
- New public API follows the naming rules and carries availability when `deployment_floor` is set (`api-design.md`)

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/swift/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| swift_language_mode | 5 \| 6 | 6 | Whether data-race diagnostics are errors or warnings; drives all advice in `concurrency.md` and whether `swift6-migration.md` is offered |
| build_tool | swiftpm \| xcode | swiftpm | Examples use `swift build`/`swift test` or a scheme-based invocation; changes where build settings are edited (`packages.md`) |
| test_framework | swift-testing \| xctest \| both | swift-testing | Syntax of generated tests and which half of `testing.md` applies |
| target_platforms | apple \| linux \| cross-platform | apple | Gates Foundation, `@objc`, and Dispatch assumptions; cross-platform forces `#if canImport` guards (`linux.md`) |
| deployment_floor | text (e.g. "iOS 17, macOS 14") | none | When set, every suggested API is checked against it and wrapped in `@available`/`#available` instead of assumed present (`api-design.md`) |
| force_unwrap_policy | forbidden \| tests-only \| allowed | tests-only | Whether emitted non-test code may contain `!`, `try!`, or IUO; `forbidden` also rejects `as!` |
| money_representation | minor-units \| decimal | minor-units | Which type the Arithmetic Defaults row for money resolves to when emitting a currency model |

Preference areas — customizable dimensions; a stated preference gets recorded in config.yaml and applied:

- **Tooling** — formatter and linter (swift-format vs SwiftLint) and its rule set, whether macro-based libraries are acceptable given their build cost (`metaprogramming.md`)
- **Conventions** — default access level, explicit `self.`, doc-comment expectations, one type per file, naming of async vs completion-handler variants
- **Platform** — toolchain version, OS floors, static vs dynamic linking on Linux, architectures built in CI
- **Safety posture** — tolerance for `try!`, `fatalError`, `@unchecked Sendable`, unsafe pointers, and wrapping operators, and whether to flag them unprompted or only on review
- **Dependencies** — Foundation-only vs swift-collections/algorithms/async-algorithms, Combine vs `AsyncSequence`, the vetted third-party list
- **Output format** — full files vs minimal diffs, comment density, whether every change ships with a test
- **Work order** — test-first vs implementation-first, and whether to build and run the suite before handing work back

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `[weak self]` on every closure | Non-escaping closures cannot outlive the call, so the capture list buys nothing and adds an unwrap on every line | Capture list only on escaping and stored closures (rule 2) |
| `DispatchQueue.main.async` inside an `async` function | Hops to main by hand, defeats actor isolation, and hides the requirement from the compiler | `@MainActor` on the function or type; `MainActor.assumeIsolated` when already provably on main |
| `Task { }` fired and forgotten | Unstructured tasks are not cancelled when their scope ends, and a thrown error inside vanishes silently | `async let`/`TaskGroup` for scoped work; store the handle and cancel it when it must stay unstructured |
| `@unchecked Sendable` to silence the compiler | Converts a compile error into a race that only appears under load | Fix the isolation, or implement the lock the annotation promises (rule 7) |
| Retry loop whose `catch` also catches cancellation | Swallowing `CancellationError` makes the task uncancellable and the loop immortal | Rethrow cancellation first, then handle domain errors (`errors.md`) |
| `print()` left in shipping code | The string is fully constructed even when nothing reads it, and stdout is synchronized | `os.Logger` or `#if DEBUG`; `Logger` interpolation is lazy and redacts by default |
| Storing a `Substring` | A Substring keeps its parent String's entire buffer alive — parse a 10 MB file, keep 20 short fields, keep 10 MB | `String(substring)` at the boundary (`strings.md`) |
| `Array(repeating: MyClass(), count: n)` | The initializer runs once; all n slots hold the SAME instance | `(0..<n).map { _ in MyClass() }` |
| Comparing optionals with `<` | Optional lost its comparison operators in Swift 3; code that "worked" was comparing something else | Unwrap first, or compare with an explicit default |
| Force-trying a decode to "see the error" | `try!` destroys the `DecodingError`, the only thing that names the offending key path | `do`/`catch` and print the error in full (`codable.md`) |

## Where Experts Disagree

- **`any` existentials vs generics.** Existential-first reads better and compiles faster; generic-first runs faster (no boxing, no witness-table lookups) and specializes. The honest boundary is measurement: `any` for heterogeneous storage and API surfaces, `some`/generics on hot paths and wherever the concrete type is already known.
- **Swift Testing vs XCTest.** Swift Testing is the better authoring experience (parameterized cases, `#expect` with expression capture, in-process parallelism). XCTest still owns UI automation and performance measurement, so mixed suites are normal rather than a smell. Migrating a green XCTest suite for style alone buys nothing.
- **How hard to fight for value semantics.** One camp makes everything a struct and threads state explicitly; the other accepts reference-typed models where persistence or an Objective-C framework already imposes identity. The line worth defending in either camp: no shared mutable reference type crosses a concurrency boundary without isolation.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/swift (install if the user confirms):
- `ios` — shipping iOS apps: lifecycle, frameworks, App Store
- `xcode` — signing, build settings, derived data, IDE-level failures
- `macos` — macOS system behavior and command-line differences

## Feedback

- If useful, star it: https://clawic.com/skills/swift
- Latest version: https://clawic.com/skills/swift

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/swift.
