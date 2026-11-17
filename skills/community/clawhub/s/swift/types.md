# Types — Structs, Classes, Protocols, Generics, Enums

The decisions here fix a codebase's shape for years. Two questions settle most of them: **does this thing have identity?** (value vs reference) and **does the caller need to know the concrete type?** (generic vs existential).

## Value or Reference

| Signal | Choose |
|---|---|
| Two instances with identical fields are the same thing | `struct` |
| Two instances with identical fields are different things (a user session, a connection) | `class`/`actor` |
| Needs `deinit` to release something | `class`/`actor` |
| Shared and mutated from several places by design | `class`/`actor`, with isolation (`concurrency.md`) |
| Crosses a concurrency boundary | `struct` of Sendable members (cheapest path to safety) |
| Framework requires a class (NSObject, ObservableObject, Core Data) | `class`, and keep it thin |

- Copy cost is rarely the deciding factor: `Array`, `String`, `Dictionary`, `Set` and `Data` are copy-on-write, so a copy is a retain until someone writes.
- COW in your own type: hold a class box and branch on `isKnownUniquelyReferenced(&storage)` before mutating; copy only when it returns false. Worth it for types wrapping a large buffer, nothing else.
- Large structs of many stored properties are copied by value on every assignment. "Large" here means many words of inline storage, not "many lines of code" — measure before restructuring.
- Mutating a struct inside a collection: `array[0].mutate()` works through `Array`'s mutable subscript, but the same expression through a computed property or a dictionary value does not. When it does not compile, extract, mutate, reassign.

## Protocols: Requirement vs Extension

- A method declared in the protocol AND implemented in an extension is dynamically dispatched through the witness table — overriding works.
- A method that exists **only** in the extension is statically dispatched on the static type. Calling it through `any P` runs the extension's version even when the concrete type declares its own. That is the whole "protocol extensions don't override" surprise, and the fix is always the same: add the member to the protocol requirements.
- Witness matching is exact on parameter types: `func f(_ x: Int)` does not satisfy `func f(_ x: some Numeric)`.
- `Self` requirements and associated types make a protocol usable as a constraint but restrict it as a type; `any P` works for many of these (`swift >=5.7`) but not where `Self` appears in a parameter position.
- Class-only protocols need `: AnyObject` — required before a conforming reference can be `weak`.
- Optional requirements need `@objc optional`, which drags the whole protocol into the Objective-C runtime. A protocol extension with a default implementation is the Swift-native answer.
- Composition (`some Shape & Codable`) beats inheritance hierarchies of protocols; deep protocol trees make diagnostics unreadable.

## `some` vs `any` vs Generic

| Form | Dispatch | Cost | Use |
|---|---|---|---|
| `<T: P>` generic | Static after specialization | Cheapest; specialization needs visibility (`performance.md`) | Hot paths, algorithms |
| `some P` (opaque) | Static, one concrete type per call site | Same as generic, nicer syntax | Return types that must not leak the concrete type |
| `any P` (existential) | Dynamic via witness table | Boxing: values larger than three words heap-allocate | Heterogeneous storage, plugin boundaries |

- `some P` in a parameter position is sugar for a generic parameter (`swift >=5.7`). In a return position it is a promise that the type is always the same one, which a generic cannot express.
- `any P` in a `var` means every access pays a witness lookup and possibly a retain. An array of `any Shape` where all elements happen to be `Circle` still pays it.
- Primary associated types let existentials carry a type: `any Collection<Int>` (`swift >=5.7`).
- Type erasure by hand (`AnyShape` wrapping closures) is now rarely necessary; reach for `any P` first and hand-roll only when you need to erase an associated type that has no primary slot.

## Generics That Compile Fast and Read Well

- Constrain with `where` clauses on the declaration rather than casting inside the body. A `where Element: Equatable` beats an `as?` at every call.
- Conditional conformance (`extension Array: Drawable where Element: Drawable`) expresses "this holds when the contents hold" without a wrapper type.
- Parameter packs (`swift >=5.9`) remove the family of `func zip2/zip3/zip4` overloads; use them instead of arity ladders.
- Retroactive conformance — conforming a type you don't own to a protocol you don't own — needs `@retroactive` (`swift >=6.0`), because upstream adding the same conformance later would be an ambiguity you cannot fix.
- Generic code that never gets specialized costs unspecialized dispatch and code size; specialization needs the generic body visible to the caller's module — `@inlinable`, `@usableFromInline`, or whole-module optimization.

## Enums

- Exhaustive `switch` is the point. Resist `default:` in your own enums — adding a case should break every site that must handle it.
- Enums from a resilient library (built with library evolution) can gain cases between versions, so switching over them requires `@unknown default:`. That clause warns on new cases while still compiling — different from `default:`, which silently absorbs them.
- `indirect` is required for recursive payloads; put it on the single recursive case rather than the whole enum when only one case needs it.
- Size = largest payload plus a discriminator, and Swift packs the tag into spare bits when it can. An enum with one huge case makes every instance that big — box it (`indirect` or a class) if the case is rare.
- `CaseIterable` synthesis works only for enums with no associated values.
- Raw values are for serialization boundaries. Give them explicit strings; auto-derived names change when someone renames a case, and the rename is invisible at the wire.

## Equatable, Hashable, Comparable

- Synthesis works when every stored property conforms; write it by hand only to exclude a field (a cache, a timestamp) — and then `hash(into:)` must hash **exactly** the fields `==` compares, or dictionaries and sets corrupt (SKILL.md Crash Messages).
- Never mutate a property that participates in a hash while the value sits in a `Set` or is a dictionary key.
- `Comparable` must be a strict weak ordering: `a < b`, `b < a`, and "equivalent" must be mutually exclusive and transitive. NaN violates this, which is why sorting Doubles with NaN can trap.
- `Identifiable` is not `Equatable`. SwiftUI diffing uses `id` for identity and `Equatable` (when present) to skip redraws — they answer different questions.

## Classes: Initialization and Inheritance

- Two-phase init: all stored properties of the class and its superclasses get values (phase 1) before anything may use `self` (phase 2). This is why a property wrapper or a closure referencing `self` cannot be a default value — use `lazy var` or set it in the initializer.
- Designated initializers delegate up; convenience initializers delegate across. A subclass inherits its superclass's initializers only when it adds no uninitialized stored properties or overrides all designated ones.
- `required init` propagates to subclasses; `init?` failability propagates to callers.
- `final` on classes and members removes dynamic dispatch and enables inlining. Apply it by default and drop it when subclassing is designed for, not the reverse.
- `deinit` order: subclass first, then superclass. Nothing in `deinit` may resurrect `self`.

## Noncopyable and Ownership

- `~Copyable` types (`swift >=5.9`) cannot be copied, so a file handle or a lock token can be modeled as a value that is provably used once. `consuming` takes ownership and ends the caller's use; `borrowing` reads without a retain.
- Use them for resources with a real "closed after this" state. Applying them to ordinary models produces friction with no benefit — everything must then be threaded explicitly.

## Casting

- `as` for guaranteed upcasts and bridging; `as?` for conditional; `as!` only where a failure is a programming error and `force_unwrap_policy` allows it.
- `is`/`as?` chains over a closed set of types are an enum wearing a disguise. Model the set as an enum and let the compiler check exhaustiveness.
- Dynamic casts cost a runtime metadata lookup and are much slower across the Objective-C bridge; in a hot loop, hoist the cast out.
- `Any` erases everything, including whether the value was an optional. Avoid it in stored properties; if a boundary forces it, convert immediately at the edge.
