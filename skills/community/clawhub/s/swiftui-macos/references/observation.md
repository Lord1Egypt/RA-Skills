# Observation Tracking Discipline

The `@Observable` macro makes every stored property a potential observation dependency. Any property read during a view's `body` evaluation registers a tracking dependency — when that property changes, `body` re-evaluates. This is powerful but creates performance traps in non-trivial apps.

## State Capture at Body Level

Each read of an observed property inside a `ForEach` registers a separate dependency per iteration. With 100 items, reading `manager.activeItemID` inside the loop body creates 100 identical observation registrations.

```swift
// Bad: N observation registrations for the same property
var body: some View {
    ForEach(items) { item in
        ItemRow(item: item, isActive: item.id == manager.activeItemID)
    }
}

// Good: capture once, use the value
var body: some View {
    let activeItemID = manager.activeItemID
    ForEach(items) { item in
        ItemRow(item: item, isActive: item.id == activeItemID)
    }
}
```

## Non-Equatable Types Always Notify

The `@Observable` macro generates `shouldNotifyObservers` overloads resolved at compile time. For **non-Equatable** types, the fallback always returns `true` — every `set` fires observation, even when the value hasn't changed:

```swift
// Generated overloads (simplified):
func shouldNotifyObservers<T>(_ old: T, _ new: T) -> Bool { true }                    // non-Equatable: ALWAYS notifies
func shouldNotifyObservers<T: Equatable>(_ old: T, _ new: T) -> Bool { old != new }   // Equatable: checks value
func shouldNotifyObservers<T: AnyObject>(_ old: T, _ new: T) -> Bool { old !== new }  // Reference: checks identity
```

```swift
struct Theme { var primary: Color; var secondary: Color }  // NOT Equatable

@Observable class Settings {
    var theme = Theme(...)  // Every set triggers observation — even `theme = theme`
}
```

**Fix**: conform all property types to `Equatable`. This is trivial (usually just adding `: Equatable`) and eliminates redundant notifications for every assignment.

## In-Place Mutations Always Notify

The `_modify` accessor (used by all in-place mutations) **skips equality checks entirely**. This is by design — checking equality would require copying the collection before yielding, which is O(n) even for an O(1) append:

```swift
@Observable class Model {
    var items: [String] = ["A", "B", "C"]
}

model.items.append("D")        // _modify → always notifies ✓ (actual change)
model.items[0] = model.items[0] // _modify → always notifies ✗ (no change, still notifies)
model.items.sort()              // _modify → always notifies (even if already sorted)
model.items = model.items       // set → equality check → NO notification ✓
```

**Any in-place mutation** — `append`, `removeAll`, `sort`, subscript assignment, `+=` — goes through `_modify` and always triggers observation. Only full property assignment (`=`) uses the `set` accessor with equality checking.

This is why version counters (below) are valuable: they decouple the notification from the collection mutation.

## Value vs Reference in Collections

This determines whether modifying an element re-renders the **entire list** or just **that element's row**:

```swift
// STRUCT: mutating items[0].name goes through _modify on the ARRAY
structModel.items[0].name = "New"
// → subscript _modify fires on items → ALL observers of \.items notified
// → the entire list view re-renders

// CLASS (@Observable): mutating items[0].name only touches the OBJECT
classModel.items[0].name = "New"
// → array still holds the same reference → \.items NOT notified
// → only observers of that specific item's \.name re-render
```

Use `@Observable` classes for entities in collections when you need granular updates. Use structs when you want cascade (parent knows about child changes without manual signaling).

## Version Counters

For complex data structures (arrays of models, nested dictionaries), observing the structure directly means SwiftUI tracks every field of every element. Instead, expose a simple counter that increments on mutation:

```swift
@Observable
class DataStore {
    private(set) var items: [Item] = []
    var itemsVersion: UInt64 = 0

    @ObservationIgnored
    private var itemIndex: [Item.ID: Item] = [:]

    func addItem(_ item: Item) {
        items.append(item)
        itemIndex[item.id] = item
        itemsVersion += 1
    }
}
```

Views observe `itemsVersion`, not `items` directly. When the counter changes, the view re-reads what it needs — but the observation dependency is on a single `UInt64`, not the entire structure.

## @ObservationIgnored

Mark properties that should never trigger view updates:

- **Internal indices and caches** — lookup dictionaries, computed caches
- **Callbacks and closures** — `onRemoval`, `onUpdate` handlers
- **Bookkeeping state** — task references, internal flags, debug counters

```swift
@Observable
class Manager {
    var visibleItems: [Item] = []  // Triggers updates

    @ObservationIgnored
    private var itemIndex: [Item.ID: Item] = [:]  // Internal cache

    @ObservationIgnored
    var onRemoval: ((Item.ID) -> Void)?  // Callback
}
```

Without `@ObservationIgnored`, accessing these properties during body evaluation creates observation dependencies on internal implementation details.

## ForEach Body Extraction

Each `ForEach` iteration can be its own observation scope — but only if the loop body is a separate `View` struct:

```swift
// Bad: all items share parent's observation scope
ForEach(items) { item in
    HStack {
        Text(item.name)
        if item.id == manager.activeID { Image(systemName: "checkmark") }
    }
}

// Good: each ItemRow has its own scope
ForEach(items) { item in
    ItemRow(item: item)
}
```

When `ItemRow` is a separate struct, changes to item N only re-evaluate `ItemRow` for item N.

## Computed Property Observation

Computed properties on `@Observable` classes propagate observation to every stored property they read. Accessing a computed property in `body` registers dependencies on ALL its underlying stored properties:

```swift
@Observable
class Manager {
    var firstName: String = ""
    var lastName: String = ""
    var avatar: NSImage?

    // Accessing fullName registers deps on BOTH firstName AND lastName
    var fullName: String { firstName + " " + lastName }
}

// Bad: body re-evaluates when avatar changes because
// it also reads firstName/lastName through fullName
var body: some View {
    VStack {
        Text(manager.fullName)    // tracks firstName + lastName
        AvatarView(manager.avatar) // tracks avatar
    }
}
```

This is correct behavior, but becomes expensive when computed properties aggregate many stored properties (e.g., a `filteredItems` that reads `items`, `filter`, `sortOrder`). Split into subviews so each tracks only what it displays.

### Manual Tracking for Ignored Backing Stores

The macro only instruments stored properties. Computed properties that read from `@ObservationIgnored` backing stores (KVO bridges, throttled values, derived state) need manual `access()` and registrar calls:

```swift
@Observable class KVOBridge {
    @ObservationIgnored private var _progress: Double = 0

    var progress: Double {
        access(keyPath: \.progress)     // Register for tracking
        return _progress
    }

    // When the backing store changes (e.g., from KVO callback):
    func updateProgress(_ value: Double) {
        guard _progress != value else { return }  // Manual equality check!
        _$observationRegistrar.willSet(self, keyPath: \.progress)
        _progress = value
        _$observationRegistrar.didSet(self, keyPath: \.progress)
    }
}
```

Key rules: always pair `willSet` with `didSet` (unpaired calls corrupt observation state). Add your own equality check — calling the registrar directly bypasses `shouldNotifyObservers`.

## Observation Scope Narrowing

All property reads during a single `body` evaluation share one observation scope. If a view reads `manager.items.count` for a badge AND `manager.activeItem` for detail display, changing either triggers re-evaluation of the entire body — even though count and detail are unrelated.

```swift
// Bad: both properties tracked in same scope
var body: some View {
    VStack {
        Text("Items: \(manager.items.count)")  // tracks items
        DetailView(item: manager.activeItem)    // tracks activeItem
    }
    // Changing activeItem re-evaluates the count text too
}
```

Fix: extract into subviews where each reads only what it needs:

```swift
struct ItemCounter: View {
    @Environment(\.manager) var manager
    var body: some View {
        Text("Items: \(manager.items.count)")  // only tracks items
    }
}

struct ActiveDetail: View {
    @Environment(\.manager) var manager
    var body: some View {
        DetailView(item: manager.activeItem)  // only tracks activeItem
    }
}
```

This is the same principle as ForEach body extraction, but applied to sibling views that depend on different slices of state.

## Observations {} — Reactive Observation Streams

`Observations {}` (macOS 26+) creates an `AsyncSequence` that yields whenever any `@Observable` property read inside the closure changes. This is the correct way to bridge observation into async contexts — replacing manual `withObservationTracking` loops.

```swift
// Track a single property — yields the value on each change
let activeTabChanges = Observations {
    self.windowState.activeTabID
}

let task = Task { @MainActor [weak self] in
    for await activeTabID in activeTabChanges {
        self?.handleTabChange(activeTabID)
    }
}
```

```swift
// Track multiple properties — yields a tuple, use `_` if you only care about the trigger
let settingsChanges = Observations {
    (
        self.settings.backgroundColorHex,
        self.settings.backgroundOpacity,
        self.settings.enableTheming,
    )
}

let task = Task { @MainActor [weak self] in
    for await _ in settingsChanges {
        self?.updateAppearance()
    }
}
```

This replaces the anti-pattern of wrapping `withObservationTracking` in a recursive loop. `Observations {}` handles the re-registration automatically, supports backpressure, and integrates with structured concurrency (the stream terminates when the task is cancelled).

**Key patterns:**
- **Store tasks for cancellation** — observation tasks should be tracked and cancelled during cleanup (e.g., in `deinit` or when observation scope changes).
- **Use `[weak self]` in the task closure** — the `Observations {}` stream can outlive the object if not cancelled. Without `weak self`, the observation keeps the object alive.
- **Read properties inside the `for await` body, not just in the `Observations` closure** — the closure determines *what to track*, but you may need to read additional state when reacting.

**When to use:**
- AppKit ↔ SwiftUI bridging in `NSWindowController`, `NSViewController`, or coordinator objects
- Reactive side effects in managers that aren't SwiftUI views (views should use `.onChange(of:)` or `.task(id:)` instead)
- Monitoring state changes that need to trigger imperative AppKit updates (window chrome, toolbar state, cursor management)

## Traps

- **@AppStorage inside @Observable**: Does not trigger view updates. `@AppStorage` only works inside `View` structs.
- **SwiftData @Model + Equatable**: `@Model` types are reference types. If a view's `Equatable` conformance compares model properties, both `lhs` and `rhs` read from the same object — comparison always returns `true`, and SwiftUI never detects changes. Don't conform model-displaying views to `Equatable`, or compare on value-type IDs only.
- **Observation in `nonisolated` contexts**: `Observations {}` captures the isolation context of where it's created. If you create it in a `nonisolated` context, the yielded values arrive without actor isolation — be explicit about isolation in the consuming `Task`.
