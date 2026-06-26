# Performance

## View Identity

SwiftUI's attribute graph tracks views by their **type** and **position** in the view tree. Understanding this is fundamental to avoiding unnecessary view destruction and recreation.

**Structural identity** (`if`/`else`, `switch`) creates `_ConditionalContent<TrueContent, FalseContent>` — a generic enum with two distinct type parameters. When the branch changes, the attribute graph sees a different active type and destroys the old view's node entirely (including all `@State`, running `.task` modifiers, and platform backing views), then creates a new one. This is not a "re-render" — it's destruction and construction.

**Ternary for modifier values** preserves identity because the view type doesn't change — only a property value does:

```swift
// Good: same view, different opacity — identity preserved
.opacity(isVisible ? 1 : 0)

// Bad: two different views, recreated on every toggle
if isVisible {
    content
} else {
    content.opacity(0)
}
```

Use `if`/`else` only when branches are structurally different views that genuinely need different identities.

## Equatable Views

Conform views to `Equatable` when body is expensive and inputs are few value types:

```swift
struct ExpensiveChart: View, Equatable {
    let data: [DataPoint]
    let style: ChartStyle

    static func == (lhs: Self, rhs: Self) -> Bool {
        lhs.data == rhs.data && lhs.style == rhs.style
    }

    var body: some View { ... }
}
```

SwiftUI skips body re-evaluation when comparison returns `true`.

**Trap**: SwiftData `@Model` types are reference types. Comparing two references to the same object always returns `true`. Don't use `Equatable` on views that take `@Model` instances as direct input — or compare on value-type identifiers only.

## NSViewRepresentable + Equatable

Conform `NSViewRepresentable` types to `Equatable` to prevent unnecessary `updateNSView` calls. Without this, `updateNSView` runs on every parent body re-evaluation. See `references/platform.md`.

## The .id() Modifier

`.id()` overrides a view's structural identity. When the value changes, SwiftUI destroys the old view and creates a new one — all `@State` is reset, all `task()` modifiers restart.

```swift
// CATASTROPHIC: new UUID every render — view is recreated on every body call
ForEach(items) { item in
    ItemRow(item: item)
        .id(UUID())  // Destroys and recreates ItemRow every time
}

// Correct: stable identity from the item
ForEach(items) { item in
    ItemRow(item: item)
        .id(item.id)
}
```

Legitimate uses: forcing a view reset (e.g., `.id(selectedTab)` on a detail view to reset scroll position). But never use a value that changes on every body evaluation.

## AnyView

Avoid `AnyView`. It erases type information SwiftUI uses for efficient diffing. Use `@ViewBuilder`, `Group`, or generics instead.

## View Initializers

Must be trivial. No networking, no file I/O, no heavy computation. Move work to `.task { }`.

## Body Evaluation

`body` is called whenever any observed property changes — and the entire body is re-evaluated, not just the part that uses the changed property (observation scoping happens at the *view* level, not the *expression* level). Move expensive derivations out:

```swift
// Bad: sorts on every body evaluation
var body: some View {
    ForEach(items.sorted(by: { $0.date > $1.date })) { ... }
}

// Good: derive once per evaluation
var body: some View {
    let sorted = items.sorted(by: { $0.date > $1.date })
    ForEach(sorted) { ... }
}
```

For expensive derivations that change rarely, cache in `@State` with explicit invalidation via `onChange`.

## ForEach Optimization

Extract loop bodies into separate view structs. This gives each item its own observation scope — changes to item N only re-evaluate that item's body. See `references/observation.md` for details.

Avoid expensive inline transforms in `ForEach` initializers (e.g., `items.filter { ... }.sorted { ... }`) when repeated often.

For hot-path collection operations that don't need a materialized array, use lazy sequences:

```swift
// Allocates intermediate arrays
let minPosition = items.filter(\.isPinned).map(\.position).min()

// No intermediate allocations
let minPosition = items.lazy.filter(\.isPinned).map(\.position).min()
```

## Lazy Stacks

`LazyVStack` / `LazyHStack` inside `ScrollView` for large or dynamic collections. Eager stacks instantiate all children immediately.

Flag eager stacks with more than ~20-30 static children or any dynamic collection of meaningful size.

## Async Work

Prefer `.task { }` over `.onAppear { }` for async work — `.task` cancels automatically when the view disappears.

## Cached Values for Animation

Store display values in `@State` when they need to persist through deletion animations:

```swift
@State private var cachedTitle: String = ""

var body: some View {
    Text(cachedTitle)
        .onChange(of: tab.title, initial: true) { _, new in
            cachedTitle = new
        }
}
```

Without caching, the title flashes to empty during removal animation as the underlying data is deleted before the animation completes.

## @State for Animated and Gestured Values

Continuous gestures (`DragGesture`, `MagnifyGesture`, `RotateGesture`) fire at up to 120Hz on ProMotion displays. Each mutation through `@Observable` goes through: `_modify` → `willSet` → `didSet` → observation notification → body re-evaluation → `access()` thread-local lookup → re-register tracking. **Every frame.**

`@State` skips the entire observation pipeline — SwiftUI owns the storage directly.

```swift
// Bad: 120 observation cycles per second during drag
@Observable class Model {
    var dragOffset: CGFloat = 0  // Don't put gesture values here
}

// Good: @State bypasses observation entirely
@State private var dragOffset: CGFloat = 0
```

**Rule**: `@State` for values driven by gestures or continuous animation (offset, scale, opacity, rotation). `@Observable` for data that changes infrequently (model state, configuration, user input).

Note: standard `withAnimation(.spring) { value = x }` does NOT cause per-frame body evaluation — Core Animation handles the interpolation. The overhead is specifically with **continuous gestures** that fire rapid mutations.

## Canvas — Imperative 2D Drawing

`Canvas` provides an immediate-mode drawing context for complex 2D rendering that would be expensive as a view tree. Unlike composing `Shape` and `Path` views, `Canvas` draws into a single backing store with no per-element view overhead.

```swift
Canvas { context, size in
    for particle in particles {
        let rect = CGRect(x: particle.x, y: particle.y, width: 4, height: 4)
        context.fill(Path(ellipseIn: rect), with: .color(particle.color))
    }
}
```

**When to use:**
- Particle systems, visualizations, custom charts with hundreds+ of elements
- Any rendering where the number of drawn elements is dynamic and potentially large
- Cases where you'd otherwise create hundreds of `Circle()` or `Rectangle()` views

**When NOT to use:**
- Interactive content that needs per-element hit testing (use views)
- Simple layouts with a few shapes (the view tree overhead is negligible)

`Canvas` supports symbols (resolved views), images, text, and gradients. It does not support animations or gestures on individual drawn elements — pair with `TimelineView` for animation.

## TimelineView — Continuous Rendering

`TimelineView` drives view updates on a schedule — use for animations that need per-frame control beyond what `withAnimation` provides.

```swift
TimelineView(.animation) { timeline in
    Canvas { context, size in
        let elapsed = timeline.date.timeIntervalSince(startDate)
        // Draw frame based on elapsed time
    }
}
```

**Schedules:**
- `.animation` — every frame (display link, ~60-120Hz). Use for smooth continuous animation.
- `.periodic(from:by:)` — fixed interval. Use for clocks, timers, periodic updates.
- `.everyMinute` — once per minute. Use for time displays.

`TimelineView` only re-evaluates its content closure on schedule ticks — it doesn't force the entire parent view tree to update. Combine with `Canvas` for efficient per-frame rendering without view tree overhead.

## drawingGroup()

For views with many overlapping layers (complex gradients, particle effects, layered shapes), `drawingGroup()` renders the entire subtree into a single Metal texture:

```swift
ComplexVisualization()
    .drawingGroup()  // Flattens into one GPU-composited layer
```

Use when Instruments shows excessive CA layer compositing. Don't use on views with interactive children — it disables hit testing within the group.

## Observation

See `references/observation.md` for observation tracking discipline — state capture, version counters, `@ObservationIgnored`, and scope minimization. Observation problems are the most common performance issue in non-trivial SwiftUI apps.
