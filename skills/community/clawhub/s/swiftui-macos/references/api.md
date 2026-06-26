# Modern API

## Deprecated SwiftUI API

- `foregroundColor()` → `foregroundStyle()`.
- `cornerRadius()` → `clipShape(.rect(cornerRadius:))`.
- `tabItem()` → `Tab` type with `TabView`.
- `overlay(content, alignment:)` → `overlay(alignment:) { content }`.
- `.navigationBarLeading`/`.navigationBarTrailing` → `.topBarLeading`/`.topBarTrailing`.
- `NavigationView` → `NavigationStack` or `NavigationSplitView`.
- `NavigationLink(destination:)` → `navigationDestination(for:)`.
- `PreviewProvider` → `#Preview`.
- `onChange(of:perform:)` (1-parameter) → `onChange(of:) { old, new in }` or `onChange(of:) { }`.
- `GeometryReader` → `containerRelativeFrame()`, `visualEffect()`, or `Layout` protocol when possible. `GeometryReader` is still correct for reading sizes for custom layouts or coordinate space conversions.
- `animation(_:)` without value → `.animation(.bouncy, value: score)`.
- `showsIndicators: false` in ScrollView init → `.scrollIndicators(.hidden)`.
- `Text("A") + Text("B")` concatenation → `Text("\(styledA)\(styledB)")` via interpolation.

## Preferred Modern Patterns

- `@Entry` macro for `EnvironmentValues`, `FocusValues`, `Transaction`, `ContainerValues` keys. Replaces the manual `EnvironmentKey` + `defaultValue` + computed property extension pattern.
- Fill and stroke on shapes can be chained directly — no overlay needed (macOS 14+).
- `ForEach(items.enumerated(), id: \.element.id)` — do not convert to array first.
- `ContentUnavailableView` for empty states. `ContentUnavailableView.search` auto-includes the search term.
- `Label` over `HStack { Image(...); Text(...) }` for icon-text pairs.
- System hierarchical styles (`.secondary`, `.tertiary`) over manual `.opacity()`.
- `bold()` over `fontWeight(.bold)` — lets the system choose the correct weight for context.
- `Image(.assetName)` (generated symbols) over `Image("assetName")` when the project supports it.
- Static member lookup: `.circle` over `Circle()`, `.borderedProminent` over `BorderedProminentButtonStyle()`.
- In `Form`, wrap controls in `LabeledContent` for correct title/control layout.
- `RoundedRectangle` defaults to `.continuous` corner style — no need to specify.
- `@Previewable` macro for using `@State` directly inside `#Preview` without wrapper views: `#Preview { @Previewable @State var count = 0; Stepper("Count: \(count)", value: $count) }`.

## Swift Modernisms

- `FormatStyle` over `String(format:)`: `Text(value, format: .number.precision(.fractionLength(2)))`.
- `localizedStandardContains()` for user-input text filtering — not `contains()` or `localizedCaseInsensitiveContains()`.
- `Double` over `CGFloat` everywhere except optionals and `inout` parameters (bridging doesn't work there).
- Date formatting for display: use `"y"` not `"yyyy"` for correct localization. Prefer `FormatStyle` over manual format strings entirely.
- `Date(string, strategy: .iso8601)` over manual `DateFormatter` for parsing.
- `ObservableObject` requires explicit `import Combine` — no longer re-exported by SwiftUI.
- `URL.documentsDirectory` over `FileManager` directory lookups. `url.appending(path:)` to append.
- `replacing("a", with: "b")` over Foundation's `replacingOccurrences(of:with:)`.

## Apple's Open-Source Swift Packages

These are maintained by Apple's Swift team, follow Swift Evolution, and cover non-trivial algorithms and data structures that should not be reimplemented. Prefer them over hand-rolled alternatives.

### swift-collections

Efficient, well-tested data structures missing from the standard library.

| Type | Use instead of | Why |
|---|---|---|
| `OrderedDictionary` | `[Key: Value]` + separate `[Key]` for ordering | Maintains insertion order with O(1) key lookup. Eliminates the common pattern of keeping a dictionary and array in sync. |
| `OrderedSet` | `Array` with manual uniqueness checks or `Set` + order tracking | O(1) membership test with stable ordering. Correct `Hashable`, `Equatable`, `Codable`. |
| `Deque` | `Array` used as a queue (removing from front) | O(1) amortized prepend and append. `Array.removeFirst()` is O(n). Essential for FIFO queues, ring buffers, sliding windows. |
| `Heap` | Sorted array with manual insertion | O(log n) insert/remove-min. Use for priority queues, top-K tracking, scheduling. |
| `TreeDictionary` | `Dictionary` in persistent/functional patterns | Hash array mapped trie (HAMT). Efficient structural sharing for copy-on-write snapshots — useful for undo stacks or diffing state. |

```swift
// Maintaining unique recently-visited items in order:
var recentURLs = OrderedSet<URL>()
recentURLs.append(url)           // O(1), no-op if already present
recentURLs.move(url, to: 0)     // Move to front if exists

// Priority queue for download scheduling:
var pending = Heap<Download>()   // Downloads comparable by priority
pending.insert(download)
let next = pending.removeMin()
```

### swift-algorithms

Sequence and collection algorithms from the Swift Algorithms package. These cover operations that are error-prone to implement correctly or are repetitive boilerplate.

| Algorithm | Use instead of | Example |
|---|---|---|
| `uniqued(on:)` | Manual `Set`-based dedup loop | `items.uniqued(on: \.id)` |
| `chunks(ofCount:)` | Manual stride-based slicing | `data.chunks(ofCount: 50)` for batch processing |
| `windows(ofCount:)` | Manual index arithmetic for sliding windows | `values.windows(ofCount: 3)` for moving averages |
| `adjacentPairs()` | `zip(array, array.dropFirst())` | `path.adjacentPairs()` for edge iteration |
| `compacted()` | `.compactMap { $0 }` | `optionals.compacted()` — clearer intent |
| `indexed()` | `.enumerated()` when you need true collection indices | `items.indexed()` for index-based access |
| `partitioned(by:)` | Two separate `filter` passes | `items.partitioned(by: \.isActive)` — single pass |
| `minAndMax()` | Separate `.min()` and `.max()` calls | Single-pass min/max extraction |

### swift-async-algorithms

Async sequence operators for combining, transforming, and timing async streams. These handle edge cases (backpressure, cancellation, buffering) that hand-rolled versions typically get wrong.

| Algorithm | Use instead of | When to use |
|---|---|---|
| `merge(_:_:)` | Manual `TaskGroup` + `AsyncStream` fan-in | Interleaving events from multiple independent sources (e.g., keyboard events + mouse events + notification stream) |
| `combineLatest(_:_:)` | Multiple `Observations {}` streams combined manually | Reacting to the latest value from two+ streams simultaneously (e.g., filter text + sort order) |
| `debounce(for:)` | Manual `Task.sleep` + cancellation | Search-as-you-type, window resize handlers, any rapid-fire event that should coalesce |
| `throttle(for:)` | Manual timestamp tracking | Rate-limiting updates (e.g., progress reporting, scroll position syncing) |
| `chain(_:_:)` | Wrapping sequences in `AsyncStream` to concatenate | Playing async sequences in order (e.g., cached results then network results) |
| `zip(_:_:)` | Manual coordination with continuations | Pairing elements from two streams 1:1 |

```swift
// Debounce search input from an async stream of keystrokes:
for await query in searchTerms.debounce(for: .milliseconds(300)) {
    await performSearch(query)
}

// Merge independent event sources:
for await event in merge(keyboardEvents, mouseEvents, systemNotifications) {
    handleEvent(event)
}

// React to latest from two streams:
for await (filter, sortOrder) in combineLatest(filterChanges, sortChanges) {
    updateResults(filter: filter, sort: sortOrder)
}
```

### When to add these packages

- **Do not reimplement** `OrderedSet`, `OrderedDictionary`, `Deque`, `Heap`, or any async sequence combinator. The correct implementations handle edge cases (hash collision strategies, COW optimization, cancellation propagation, backpressure) that ad-hoc versions miss.
- **Add the package** when the first use case arises — don't preemptively add all three. Each is an independent SPM dependency.
- These are **not third-party dependencies** in the usual sense — they're maintained by the Swift project under the `apple/` GitHub organization, follow Swift Evolution, and are considered the staging ground for eventual standard library inclusion.
