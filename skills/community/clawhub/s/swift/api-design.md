# API Design — Naming, Access Control, Availability, Evolution

Swift's API Design Guidelines optimize for **clarity at the point of use**, not brevity at the point of definition. Everything below follows from that, plus one operational fact: once an API is public and someone depends on it, changing it costs them a version bump.

## Naming

- Read the call site aloud; it should form a phrase: `list.insert(item, at: 0)`, not `list.insert(item, 0)`.
- The mutating/non-mutating pair is grammatical: verb-based operations are `sort()` / `sorted()`, `reverse()` / `reversed()`; noun-based results use `formUnion` / `union`. Inventing a third pattern makes readers check the docs every time.
- Omit needless words: `remove(at:)` not `removeElement(atIndex:)`. The types already say what the parameters are.
- Boolean properties read as assertions about the receiver: `isEmpty`, `hasSuffix`, `canSend`.
- Argument labels are for the call site's grammar. Use `_` when the first argument continues the method name (`min(a, b)`); label it when it needs a preposition (`move(from:to:)`).
- Name by role, not by type: `var delegate: Delegate` beats `var delegateProtocol: DelegateProtocol`; `body: Data` beats `data: Data`.
- Protocols describing capability end in `-able`/`-ible` (`Equatable`, `Codable`); protocols describing a thing are nouns (`Collection`, `Sequence`).
- Document the non-obvious with `///` and use the parameter/returns/throws sections. A doc comment that repeats the signature is noise; one that states the precondition and the failure modes is the reason the next reader stops guessing.

## Access Control

| Level | Visible | Subclass/override outside module | Use |
|---|---|---|---|
| `private` | Enclosing declaration and its extensions in the same file | — | Default for implementation detail |
| `fileprivate` | Whole file | — | Two types in one file that genuinely cooperate |
| `internal` | The module | — | Default; leave it implicit |
| `package` | All targets in the same package (`swift >=5.9`) | — | Sharing across your own targets without a public API |
| `public` | Any importer | No | Your API surface |
| `open` | Any importer | Yes | Class/method you intend to be subclassed |

- Default to the narrowest that compiles. Every `public` is a maintenance promise; every `open` is a promise about behavior under subclassing.
- Splitting a target for build reasons forces internal symbols public — that is exactly what `package` prevents (`packages.md`).
- `private` reaches into extensions of the same type in the same file, so the "make it fileprivate to use it from an extension" habit is usually unnecessary.
- `@testable import` sees `internal`, never `private`.

## Availability

- `@available(iOS 17, macOS 14, *)` on the declaration; `if #available(iOS 17, *) { } else { }` at the call site. The trailing `*` covers platforms you did not list and is required.
- With `deployment_floor` set (SKILL.md Configuration), every suggested API gets checked against it rather than assumed present.
- `@available(*, deprecated, renamed: "newName")` gives callers a fix-it; deprecating without `renamed:` or a message makes the warning useless.
- `@available(*, unavailable)` on a superclass initializer is how you close off an inherited init you cannot support.
- `@backDeployed` (`swift >=5.9`) ships a function's body with the client so a new API works on older OSes — only for additive, self-contained functions.
- Availability is per-declaration, not per-file: an extension can carry it for everything inside, which is the tidiest way to gate a feature.

## Evolution and ABI

- Source compatibility is what most packages owe their users; ABI stability only matters for binaries shipped separately from their clients (Apple's OS libraries; your XCFramework).
- With library evolution enabled, structs and enums become **resilient**: layout is not fixed, so consumers cannot switch exhaustively over your enum without `@unknown default`, and adding a stored property is not a break. `@frozen` opts out for speed and gives up that freedom permanently.
- Adding a case to a non-frozen public enum is source-compatible only because of `@unknown default`. Adding one to a frozen enum is a break. Decide which you are before the first release.
- Adding a protocol requirement is a break unless it has a default implementation. Adding a member to a protocol you expect others to conform to always needs one.
- Renaming anything public is a break; ship the new name plus a deprecated alias, then remove it a major later.
- Gate it in CI: `swift package diagnose-api-breaking-changes <ref>` catches the accidental break before the release note has to explain it.

## Designing the Surface

- Make illegal states unrepresentable: an enum with associated values beats a struct with five optionals whose valid combinations live in a comment.
- Return concrete types or `some P`; return `any P` only when the concrete type genuinely varies. The opaque return keeps callers fast and you free to change the implementation (`types.md`).
- Prefer a small number of orthogonal parameters over a boolean flag that switches behavior; `func fetch(refreshing: Bool)` is two functions wearing a trench coat.
- Default arguments beat overload families: one function with three defaults documents better than four overloads.
- Async and throwing are part of the signature and thus part of the contract. Adding `throws` later is a break; adding `async` is a bigger one. Decide early whether an operation can fail.
- Sendability is API too: a public type that should cross isolation boundaries must declare `Sendable` explicitly, and adding it later can break conformances downstream.
- Libraries depend on API packages (swift-log, swift-metrics), never on a specific backend — that choice belongs to the executable.
