# #Predicate Pitfalls

Common runtime crashes and build errors when using `#Predicate` with SwiftData.

## Unsupported Expressions

`#Predicate` compiles Swift expressions into a query representation. Only a subset of Swift is supported. Unsupported expressions compile but crash at runtime.

| Pattern | Crash? | Fix |
| --- | --- | --- |
| `$0.name.uppercased() == "PARIS"` | Runtime crash | Use `localizedStandardContains` or `caseInsensitiveCompare` |
| `$0.name.count > 5` | Runtime crash | Store length in a separate property or filter after fetch |
| `$0.tags.count == 0` | Runtime crash | Use `$0.tags.isEmpty` (iOS 17.4+) or a stored flag |
| `$0.name.isEmpty` on optional String | Runtime crash on some OS versions | Use `$0.name == nil \|\| $0.name == ""` |
| Custom computed property | Runtime crash | Only stored `@Attribute` properties work in predicates |
| `Date.now` captured by value | Stale predicate | Create a `let now = Date()` before the predicate and capture it |
| Enum raw value comparison | Runtime crash (pre-iOS 18) | Store the raw value as a separate property, or target iOS 18+ |
| Loops, declarations, mutation, or switch-heavy control flow | Build error or runtime failure | Use boolean logic, ternary expressions, optional chaining, or optional binding patterns supported by Foundation `Predicate` |
| Arbitrary method calls | Runtime crash | Only supported methods (see below) work |

## Supported Operations

**Comparisons:** `==`, `!=`, `<`, `<=`, `>`, `>=`

**Logic:** `&&`, `||`, `!`

**String:** `localizedStandardContains(_:)`, `contains(_:)`, `starts(with:)`, `caseInsensitiveCompare(_:)`

**Collections:** `contains(where:)`, `allSatisfy(_:)`, `filter(_:)`, `.isEmpty`

**Other:** optional chaining, nil coalescing (`??`), ternary (`? :`), arithmetic (`+`, `-`, `*`, `/`), type casting (`as?`, `is`)

## Safe Pattern: Build Predicates Dynamically

```swift
func tripPredicate(searchText: String, favoritesOnly: Bool) -> Predicate<Trip> {
    let now = Date()
    return #Predicate<Trip> { trip in
        (searchText.isEmpty || trip.destination.localizedStandardContains(searchText))
        && (!favoritesOnly || trip.isFavorite)
        && trip.startDate > now
    }
}
```

Capture all external values as `let` bindings outside the predicate closure. The predicate captures them by value at creation time.

## Debugging Predicate Crashes

When a predicate crashes at runtime with `SwiftData.PredicateError` or `NSInvalidArgumentException`:

1. Simplify the predicate to a single clause and add clauses back one at a time
2. Check each clause uses only supported operations on stored properties
3. Test on the minimum deployment target — some operations were added in later iOS versions
