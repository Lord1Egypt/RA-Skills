# Metaprogramming — Property Wrappers, Result Builders, Macros, Key Paths

Four tools that generate or redirect code. Each buys real leverage and each costs something specific: property wrappers cost initialization complexity, result builders cost diagnostics, macros cost build time, key paths cost a little performance. Reach for them when the duplication they remove is measured in dozens of sites, not three.

## Property Wrappers

```swift
@propertyWrapper
struct Clamped<Value: Comparable> {
    private var value: Value
    let range: ClosedRange<Value>
    var wrappedValue: Value {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }
    init(wrappedValue: Value, _ range: ClosedRange<Value>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}
```

- `init(wrappedValue:)` is what makes `@Clamped(0...10) var level = 5` legal. Without it, the `= 5` form does not compile.
- The wrapper is initialized **before** `self` exists, so it cannot read other instance properties. That is the root of most "cannot use instance member within property initializer" errors.
- `projectedValue` (the `$` form) can be any type — a `Binding`, a publisher, the wrapper itself, or a validation result. Read the wrapper's definition rather than assuming it is a `Binding`.
- Wrappers break `Codable` synthesis unless the wrapper itself is `Codable` with the right `init(from:)`; otherwise write `CodingKeys` and a manual initializer (`codable.md`).
- A wrapper on a struct property makes the struct's memberwise initializer take the wrapper's type or its wrapped value depending on the initializers you declared — surprising callers is common; declare both if the type is public.
- Composition applies outside-in: `@A @B var x` means `A` wrapping `B`. Two wrappers that both intercept `set` need a stated order.
- Wrappers cannot be applied to computed properties, protocol requirements, or (with restrictions) `lazy` ones.

## Result Builders

- Required pieces: `buildBlock`. Then `buildOptional` for a bare `if`, `buildEither(first:)`+`buildEither(second:)` for `if`/`else`, `buildArray` for `for` loops, `buildExpression` to accept extra leaf types, `buildFinalResult` to transform the output, `buildLimitedAvailability` for `if #available`.
- Missing one of those is why "the `if` in my builder doesn't compile" — the DSL supports exactly the control flow you implemented.
- Diagnostics are the real cost: a type error inside a builder often surfaces as "unable to type-check in reasonable time" or a message pointing at the wrong line. Bisect by extracting sub-expressions into typed `let`s.
- `buildExpression` overloads decide which leaf types are accepted; adding one is how you make a builder accept `String` alongside your own type.
- SwiftUI's `ViewBuilder` had a ten-child limit in older SDKs before parameter packs; with an older `deployment_floor` the fix is still `Group` or extracting a subview.

## Macros

- Two shapes: freestanding (`#stringify(x)`) produce an expression or declarations; attached (`@Observable`, `@Test`) modify a declaration.
- Macros operate on **syntax**, not semantics. They cannot see types, resolve names, or inspect values — a macro that "checks the property's type" is checking the text you wrote.
- Build cost is the headline tradeoff: a macro package pulls in swift-syntax, which compiles from source on a cold build. One macro dependency can add minutes to a clean build, and it is the usual answer to "why did our build time double" (`performance.md`).
- The macro implementation runs as a separate compiler plugin process; a crash there surfaces as an opaque build failure rather than a Swift error.
- Diagnostics point at the **use site** while the bug is in the macro. Debug by reading the expansion: Xcode's Expand Macro action, or a unit test with `assertMacroExpansion` from SwiftSyntaxMacrosTestSupport, which is the only fast feedback loop that exists.
- Emit real diagnostics from the macro (`context.diagnose`) instead of generating code that fails to compile — otherwise users see errors in code they never wrote.
- Multiple attached macros on one declaration expand in an order tied to declaration order; two that both add members can collide.
- Choose the cheapest tool: a protocol extension beats a macro; a property wrapper beats a macro; a macro is right when you must generate declarations that cannot be written generically.

## Key Paths

- `\Person.name` is a `KeyPath`; writable variants are `WritableKeyPath` (value types) and `ReferenceWritableKeyPath` (classes). A `let` property yields a read-only key path, which is why "cannot assign through key path" appears at the wrong-looking line.
- Key paths as functions (`swift >=5.2`): `people.map(\.name)` — shorter and faster to type-check than a closure.
- Composition (`\Person.address.city`) and `appending(path:)` make generic accessors possible: a sort descriptor, a diffing helper, or a table column all reduce to storing a key path.
- They cost a small dynamic lookup versus a direct access; irrelevant except in tight loops.
- `@dynamicMemberLookup` with key paths gives type-safe forwarding to a wrapped value; with string subscripts it gives no safety at all — use the key-path form unless you are wrapping genuinely dynamic data.

## Reflection, and When To Stop

- `Mirror` walks a value's children by metadata. It is read-only, slow, and its output is not a stable contract — fine for logging and debug dumps (`dump(x)`), wrong for serialization (that is `Codable`) and wrong for anything on a hot path.
- There is no runtime type registry in pure Swift: "find all types conforming to P" needs either a macro that generates the list, a plugin, or the Objective-C runtime on Darwin.
- The escalation ladder, cheapest first: generics → protocol extension → key paths → property wrapper → result builder → macro → reflection. Stop at the first rung that solves the problem; every rung above costs diagnostics quality, build time, or both.
