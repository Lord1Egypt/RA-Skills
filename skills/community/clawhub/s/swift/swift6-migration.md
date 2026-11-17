# Swift 6 Migration — Turning a Warning Wall Into a Ratchet

Swift 6 language mode makes data-race safety a compile-time error instead of a runtime maybe. The migration fails when it is attempted as one flag flip on a whole app; it succeeds as a per-target ratchet where each step is independently shippable.

## The Order That Works

1. **Upgrade the toolchain, stay in language mode 5.** Fix ordinary source breakage first; do not mix compiler upgrade with isolation work.
2. **Turn on `-strict-concurrency=targeted`** (warnings only). Fix what it says. This covers code that already uses async/actors and leaves the rest alone.
3. **Move to `-strict-concurrency=complete`**, still warnings. This is the real workload and where the warning count peaks.
4. **Flip one leaf target to language mode 6.** Leaf = a target nothing else in your graph depends on, usually a model or utility module. Its warnings became errors; nothing above it changed.
5. **Walk up the dependency graph**, one target per pull request, until the app target flips last.
6. **Lock the ratchet**: once a target is in mode 6 it never goes back, and new targets start in mode 6.

Per-target mode in SwiftPM (`swift-tools-version: 6.0` or later):

```swift
.target(name: "Core", swiftSettings: [.swiftLanguageMode(.v6)])
```

Under tools 5.x the equivalent knob is `.enableExperimentalFeature`/`.unsafeFlags` for strict concurrency, and `unsafeFlags` bars the package from being used as a versioned dependency (`packages.md`) — another reason to raise tools-version before starting.

## Triage: Which Warning Class Is This

| Diagnostic | Root cause | Cheapest correct fix |
|---|---|---|
| "Var 'x' is not concurrency-safe because it is nonisolated global shared mutable state" | Global/static `var` | `let` if it never changes; `@MainActor` if UI-adjacent; `Mutex` if hot; `nonisolated(unsafe)` only with a documented owner |
| "Type 'X' does not conform to the 'Sendable' protocol" | Value crossing a boundary | Add the conformance if the members are already safe; make stored refs immutable; otherwise isolate the type |
| "Non-sendable type 'X' … cannot cross actor boundary" | Passing a class instance in or out | Pass a Sendable snapshot struct instead of the object |
| "Main actor-isolated property 'y' can not be referenced from a nonisolated context" | Caller lacks isolation | Annotate the caller `@MainActor`, or `await` it |
| "Call to main actor-isolated initializer in a synchronous nonisolated context" | Type is `@MainActor`, construction is not | `MainActor.assumeIsolated` at a proven-main callback, else make the call async |
| "Capture of 'self' with non-sendable type in a `@Sendable` closure" | Escaping closure crossing domains | Capture the fields you need, not `self` |
| "Sending value of non-Sendable type … risks causing data races" | Ownership transfer the compiler can't prove | Mark the parameter `sending`, or hand over a copy |

## The Five Refactors That Clear Most of the Wall

- **Snapshot at the boundary.** Convert reference-typed models into Sendable structs where they cross isolation. Most "make this Sendable" tickets are really "stop sharing this object".
- **Isolate the type, not each member.** One `@MainActor` on a view model removes dozens of per-property diagnostics and prevents the half-isolated state that generates new ones.
- **Delete the ambient singleton.** `static var shared` that everything mutates is the largest single source of errors; inject the dependency, or make the singleton an actor.
- **Retire `DispatchQueue`-as-lock.** A serial queue guarding state maps one-to-one to an actor; keeping it forces `@unchecked Sendable` forever.
- **Give completion handlers `@Sendable`** and audit what they capture. Old callback APIs are where non-Sendable captures hide.

## Third-Party and Objective-C Code You Cannot Change

- Objective-C headers can be annotated for Swift concurrency without touching implementation: `NS_SWIFT_UI_ACTOR` for main-thread types, `NS_SWIFT_SENDABLE` for types that are safe. Auditing the header is cheaper than wrapping the type.
- A dependency compiled in language mode 5 keeps working: its types are seen as non-Sendable unless declared. Wrap them in your own Sendable facade rather than sprinkling `@unchecked` at every use site.
- `@preconcurrency import` silences Sendable diagnostics coming from one module — a scoped, reversible suppression. Use it to isolate a blocker; grep for it before each release so it does not become permanent.
- `@retroactive` (`swift >=6.0`) is required when you conform someone else's type to someone else's protocol; the warning exists because a future upstream conformance would collide.

## What NOT To Do

- Do not scatter `@unchecked Sendable` to make the build green — you converted compile-time proof back into a production race (SKILL.md rule 7).
- Do not annotate everything `@MainActor` to end the fight: the app compiles and then runs single-threaded, and the regression looks like "the new version is slower".
- Do not migrate tests last. Test targets surface isolation problems in setup and shared fixtures that production code hides; migrate them alongside their target.
- Do not mix a language-mode flip with a feature branch. The diff must be reviewable as "isolation only".

## Verifying the Migration Actually Bought Something

- Warning count is a progress metric, not a success metric. The success metric is that races the old build had are now impossible: pick two historical race bugs and confirm the new mode would have rejected them.
- Keep Thread Sanitizer in CI even after the flip — it still covers Objective-C, C, and any `@unchecked`/`nonisolated(unsafe)` you kept (`debugging.md`).
- Track main-thread time before and after. An over-isolated migration shows up as a jump there, not in any diagnostic.
- `swift >=6.2` moves in the opposite direction with an approachable-concurrency setting that makes unannotated code main-actor-isolated by default, so single-threaded code stops fighting the checker. Confirm what your toolchain supports before designing around it; the ratchet above works with or without it.
