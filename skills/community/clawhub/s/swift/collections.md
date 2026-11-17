# Collections — Array, Dictionary, Set, Slices, Algorithms

Swift's collections are copy-on-write value types with strong performance contracts. Most collection bugs are one of three things: an accidental O(n²), an index that is not an offset, or a `Hashable` conformance that lies.

## Complexity You Are Expected To Know

| Operation | Array | Dictionary / Set |
|---|---|---|
| Subscript by index / key | O(1) | O(1) average |
| `append` | O(1) amortized (capacity doubles) | — |
| `insert(at:)` / `remove(at:)` | O(n) | — |
| `contains(_:)` | O(n) | O(1) average |
| `firstIndex(of:)` | O(n) | — |
| `sorted()` | O(n log n), **not guaranteed stable** | — |

- The O(n²) that shows up in real code: `contains` inside a loop over another array. Build a `Set` once (O(n)) and the loop drops to O(n).
- The second one: `reduce` that concatenates. `reduce([], +)` copies the accumulator every step; `reduce(into: []) { $0.append($1) }` mutates in place. Same for building strings and dictionaries.
- The third: `remove(at:)` inside a loop. `removeAll(where:)` is a single pass.
- `reserveCapacity(n)` before a known-size build avoids the reallocation ladder — measurable above a few thousand elements, noise below it.

## Indices Are Not Offsets

- `enumerated()` yields `(offset, element)`. On an `ArraySlice` the offsets start at 0 while the indices start wherever the slice began — indexing the slice with an enumerated offset is the classic out-of-range crash (SKILL.md Crash Messages).
- Use `zip(collection.indices, collection)` when you need real indices, or `collection.indices` alone.
- `ArraySlice` keeps the parent array's storage alive, exactly like `Substring` (`strings.md`). Convert with `Array(slice)` when storing.
- Mutating a collection while iterating it is a logic error; snapshot with `for x in Array(collection)` or collect the mutations and apply them after the loop.
- Removing by index inside a `for i in 0..<count` loop shifts everything after it. Iterate `reversed()` when removing by index, or use `removeAll(where:)`.

## Dictionary

- `dict[key, default: 0] += 1` performs one lookup and mutates in place; `dict[key] = (dict[key] ?? 0) + 1` performs two lookups and can trigger a COW copy.
- `dict[key] = nil` **removes** the key; storing a nil value in a `[K: V?]` needs `updateValue(nil, forKey:)`.
- Iteration order is unspecified and differs between runs: Swift seeds hashing per process. Tests that depend on it are flaky in CI and only there.
- `Dictionary(uniqueKeysWithValues:)` traps on a duplicate key. Use `Dictionary(_:uniquingKeysWith:)` whenever the input is data you did not generate.
- `Dictionary(grouping:by:)` replaces the manual "append to the array in the dictionary" pattern and does it in one pass.
- `merge(_:uniquingKeysWith:)` is the in-place merge; `merging` returns a copy.
- `mapValues` keeps the keys and skips rehashing; `map` on a dictionary gives you an array of tuples instead, which is almost never what was meant.

## Set and Hashable

- `hash(into:)` must hash exactly the fields `==` compares. Hashing more is a correctness bug (equal values land in different buckets); hashing less only costs performance.
- Never mutate a property that feeds the hash while the value lives in a `Set` or serves as a dictionary key — the element becomes unfindable and `Duplicate keys` traps appear later, far from the cause.
- Set algebra is the readable form of loop-and-check: `union`, `intersection`, `subtracting`, `symmetricDifference`, `isSubset(of:)`.
- `Set` has no order. If a "set" must round-trip in a stable order, it is an `OrderedSet` (swift-collections) or a sorted array.

## Sequence, Lazy, and Algorithms

- `lazy` avoids intermediate arrays in a chain: `arr.lazy.filter(p).map(f).first` stops at the first hit. The catch: a lazy sequence re-evaluates on every traversal, so materialize with `Array(...)` if you iterate twice.
- `first(where:)` beats `filter { }.first` — the second builds the whole array.
- `allSatisfy` on an empty collection is `true`, `contains(where:)` is `false`. Both are correct and both surprise people writing validation.
- `zip` truncates to the shorter sequence, silently. Assert the counts when a mismatch means a bug.
- `stride(from:to:by:)` for non-unit steps; `Range` requires `lowerBound <= upperBound` and traps otherwise (SKILL.md Crash Messages).
- `compactMap` drops nils; `flatMap` on a sequence of sequences concatenates. Using `flatMap` on optionals in a sequence context is deprecated precisely because the two got confused.
- `sorted(by:)` needs a strict weak ordering, and `sorted()` is not documented as stable — when ties must keep input order, sort by a `(key, originalIndex)` pair.
- swift-algorithms adds `chunked`, `windows`, `uniqued`, `product`, `adjacentPairs`; swift-collections adds `Deque` (O(1) at both ends), `OrderedDictionary`, and `Heap`. Reaching for either is a dependency decision — record it as a preference (SKILL.md Configuration).

## Array Construction Traps

- `Array(repeating: MyClass(), count: n)` evaluates the initializer once: n references to ONE instance (SKILL.md Traps). `(0..<n).map { _ in MyClass() }` for distinct objects.
- `Array(repeating: Array(repeating: 0, count: cols), count: rows)` is fine for value types — the inner arrays are copies with COW, and writing to one does not touch the others.
- `arr[i...]` on an empty array with `i == 0` is legal (an empty slice); `arr[0]` is not. `first`/`last` return optionals for that reason, and `removeFirst()` traps on empty while `popFirst()` returns nil.
- `Array(dictionary)` yields `[(key: K, value: V)]` in unspecified order — sort it before comparing in a test.
- Reference-typed elements make an array's COW misleading: copying the array copies the references, so mutating an element is visible through both copies (`types.md`).
