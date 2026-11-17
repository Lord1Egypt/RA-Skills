# Optionals — Nil Safety Without Noise

An optional is a two-case enum, not a nullable pointer. Every trap below comes from treating it as the latter. The goal is not "zero optionals"; it is that each `Optional` in the code marks a real "this may legitimately be absent", and nothing else.

## Unwrapping — Choose By Intent

| Intent | Form | Note |
|---|---|---|
| Absence is normal, continue without it | `if let x { … }` | Shadowing shorthand `if let x` (`swift >=5.7`) |
| Absence means this function cannot proceed | `guard let x else { return }` | Keeps the happy path unindented; the reason lives in the `else` |
| Absence means the program is already broken | `guard let x else { fatalError("…") }` | Names the invariant in the crash log (SKILL.md rule 1) |
| Absence has a cheap substitute | `x ?? default` | Right side is `@autoclosure`: it is NOT evaluated when `x` is non-nil |
| Absence should become an error | `guard let x else { throw ParseError.missingField("x") }` | Preferred at API boundaries (`errors.md`) |
| Value exists but only after init | `let view: UIView!` | IBOutlets and two-phase init only |

- `??` is lazy on its right-hand side, so `x ?? expensiveDefault()` costs nothing when `x` is present. No closure trick is needed.
- Chained `??` associates right: `a ?? b ?? c` is `a ?? (b ?? c)`, which is what you want.
- `if let a, let b, a.count > 0` binds and conditions in one clause; splitting them into nested `if`s adds indentation and no clarity.

## The Traps

- **Interpolating an optional** prints `Optional("x")` into user-visible text. The compiler warns; silence it deliberately with `String(describing:)` or by unwrapping, never by adding `!`.
- **Optionals are not Comparable.** `<`, `>`, `<=`, `>=` were removed for `Optional` in Swift 3. Sorting by an optional field does not compile; decide explicitly where nils go: `sorted { ($0.date ?? .distantPast) < ($1.date ?? .distantPast) }`.
- **`dict[key] = nil` removes the key.** To store a genuine nil value in a `[String: Int?]`, use `dict.updateValue(nil, forKey: key)`. The difference is visible in `dict.count`.
- **Double optionals are real.** A `[String: Int?]` subscript returns `Int??`; `as?` on an optional and `try?` on an optional-returning throwing function used to nest too. `try?` flattens since Swift 5; dictionary subscripts do not. Flatten with `??` or pattern matching, do not `!!`.
- **`if optionalBool` does not compile**, and `if optionalBool == true` treats nil as false while `if optionalBool != false` treats nil as true. Pick the one that matches the requirement and write it down.
- **Optional chaining swallows the failure.** `user?.save()` does nothing when `user` is nil and reports nothing. If the call mattered, unwrap and handle the nil branch.
- **`as?` returns nil for a failed cast AND for a nil input** — a nil result does not tell you which. Split the checks when the difference matters.
- **IUO propagates.** `view.frame` where `view: UIView!` crashes exactly like `view!.frame`; the declaration moved the `!`, it did not remove it.

## Optional as a Value, Not a Branch

```swift
let name = user.flatMap(\.profile).map(\.displayName) ?? "Guest"
let ids  = rows.compactMap { Int($0.identifier) }        // drops nils
let sum  = optionalCount.map { $0 * 2 }                  // stays optional
```

- `map` keeps the optional; `flatMap` un-nests one level. `compactMap` on a sequence removes nils — this is the only member you want on collections of optionals.
- Pattern matching reads better than chained unwraps for enums with payloads: `if case let .success(value)? = result`.
- `Optional`'s `Equatable` conformance works: `x == nil`, `x == y`, and switching on `.some`/`.none` are all fine — it is only ordering that was removed.

## API Design With Optionals

- Do not return `[T]?`. Empty array already means "nothing"; the optional adds a case with no meaning and forces every caller to unwrap.
- Do not return `Bool?` from a predicate. Return `Bool`, or an enum with the third case named.
- Optional parameters with a nil default (`func f(limit: Int? = nil)`) are fine; optional parameters where nil means "use a different algorithm" should be an enum instead.
- A struct with six optional properties is usually two or three structs, or an enum with associated values. Optional-heavy models push the impossible-state check onto every reader.
- `throws` beats returning nil whenever the caller could reasonably ask "why?".

## Bridging and Objective-C

- Unaudited Objective-C headers import every object pointer as an IUO. A crash in Swift code calling an old framework often means the header lied about nullability — annotate it with `NS_ASSUME_NONNULL_BEGIN` and `_Nullable` rather than defending at every call site (`interop.md`).
- `NSNull` is not nil: JSON parsed through Foundation's `JSONSerialization` yields `NSNull` for JSON `null`, which is a non-nil object. `Codable` handles this correctly; dictionary-walking code does not.
- Objective-C collections cannot hold nil, so a bridged `[String?]` becomes an array of `NSNull` on the way out.
