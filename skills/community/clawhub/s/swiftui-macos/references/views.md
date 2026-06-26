# View Composition and Animation

## View Decomposition

Not all decomposition requires separate `View` structs. Choose based on the subview's needs:

| Extract into `View` struct | Computed property is fine |
|---|---|
| Has its own `@State` | Pure readability split of parent body |
| Needs independent identity (animations, transitions) | Shares all parent state, no own lifecycle |
| Reused across multiple files | Used once, tightly coupled to parent context |
| Loop body in `ForEach` (for observation scoping) | Simple conditional content |

For large views, extension-based decomposition by functional domain is effective:

```swift
// MyView+Sidebar.swift
extension MyView {
    var sidebarContent: some View { ... }
}

// MyView+Toolbar.swift
extension MyView {
    var toolbarContent: some ToolbarContent { ... }
}
```

This keeps related logic colocated without creating separate types that need all the parent's state passed in.

## ViewBuilder Storage

Store built view values, not escaping closures:

```swift
// Anti-pattern: escaping closure stored on view
struct Card<Content: View>: View {
    let content: () -> Content
}

// Correct: stored value, synthesized init calls the builder
struct Card<Content: View>: View {
    @ViewBuilder let content: Content
}
```

## ViewModifier

Use `ViewModifier` when:
- The modifier has its own `@State` (e.g., hover tracking, delayed appearance, tooltip management)
- Multiple modifiers are always applied together as a unit
- The modifier needs coordinator-like lifecycle management

Keep stateless modifiers as simple `View` extensions.

## Button Actions

Extract actions into methods or pass them directly:

```swift
// Preferred forms
Button("Save", action: save)
Button("Add", systemImage: "plus", action: addItem)

// Acceptable for simple one-liners
Button("Toggle") { isExpanded.toggle() }
```

Never inline multi-line business logic in button closures or `task()` / `onAppear()` blocks.

## .task(id:) for Reactive Async Work

When async work should restart in response to a value change, use `.task(id:)` — not `onChange` + manual Task cancellation:

```swift
// Bad: manual cancellation boilerplate
@State private var loadTask: Task<Void, Never>?

.onChange(of: selectedUserID) { _, newID in
    loadTask?.cancel()
    loadTask = Task { await loadProfile(newID) }
}
.onDisappear { loadTask?.cancel() }

// Good: automatic cancellation and restart
.task(id: selectedUserID) {
    await loadProfile(selectedUserID)
}
```

`.task(id:)` cancels the previous task and starts a new one whenever the `id` value changes. It also cancels on disappear. This eliminates an entire class of Task lifecycle bugs.

## Preference Keys

Use `PreferenceKey` for child-to-parent data flow — the reverse of environment:

```swift
struct SizePreferenceKey: PreferenceKey {
    static var defaultValue: CGSize = .zero
    static func reduce(value: inout CGSize, nextValue: () -> CGSize) {
        value = nextValue()
    }
}

// Child reports its size
ChildView()
    .background(GeometryReader { geo in
        Color.clear.preference(key: SizePreferenceKey.self, value: geo.size)
    })

// Parent reads it
.onPreferenceChange(SizePreferenceKey.self) { size in
    childSize = size
}
```

Prefer preference keys over closures or bindings for size reporting, anchor propagation, or any data that flows upward in the view tree.

## Navigation

- `NavigationSplitView` for sidebar-detail patterns (most macOS apps).
- `NavigationStack` for linear push/pop flows.
- Never mix `navigationDestination(for:)` and `NavigationLink(destination:)` in the same hierarchy.
- `navigationDestination(for:)` must be registered once per type — flag duplicates.
- Attach `confirmationDialog()` to the trigger view for correct Liquid Glass source animations.
- `sheet(item:)` with `.init` shorthand: `sheet(item: $item, content: DetailView.init)`.
- Use enums for `TabView(selection:)` bindings, not integers or strings.

## Animation

- Never use `.animation(_:)` without a value parameter.
- Chain animations via `withAnimation` completion — never with `DispatchQueue.main.asyncAfter`:

```swift
withAnimation(.spring) {
    scale = 2
} completion: {
    withAnimation(.spring) {
        scale = 1
    }
}
```

- `@Animatable` macro over manual `animatableData`. Mark non-animatable properties `@AnimatableIgnored`.
- Ternary for toggling modifier values (`.opacity(isVisible ? 1 : 0)`) preserves structural identity. `if/else` creates `_ConditionalContent` — use only when branches are structurally different views.

## Custom Layout Protocol

Use the `Layout` protocol instead of `GeometryReader` when the goal is **arranging subviews** (not reading sizes for other purposes). `Layout` participates correctly in the sizing negotiation — `GeometryReader` greedily takes all proposed space.

```swift
struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let result = arrange(proposal: proposal, subviews: subviews)
        return result.size
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        let result = arrange(proposal: proposal, subviews: subviews)
        for (index, position) in result.positions.enumerated() {
            subviews[index].place(at: CGPoint(x: bounds.minX + position.x, y: bounds.minY + position.y), proposal: .unspecified)
        }
    }

    private func arrange(proposal: ProposedViewSize, subviews: Subviews) -> (size: CGSize, positions: [CGPoint]) {
        let maxWidth = proposal.width ?? .infinity
        var positions: [CGPoint] = []
        var x: CGFloat = 0, y: CGFloat = 0, lineHeight: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > maxWidth, x > 0 {
                x = 0; y += lineHeight + spacing; lineHeight = 0
            }
            positions.append(CGPoint(x: x, y: y))
            lineHeight = max(lineHeight, size.height)
            x += size.width + spacing
        }

        return (CGSize(width: maxWidth, height: y + lineHeight), positions)
    }
}
```

**When Layout > GeometryReader:**
- Arranging children in custom patterns (flow, masonry, centered-middle)
- Anything where you'd read `GeometryProxy.size` just to divide space among children
- Layouts that need to adapt to children's ideal sizes

**When GeometryReader is still correct:**
- Reading a view's size to communicate it elsewhere (via preference keys)
- Coordinate space conversions (`convert(_:to:)`)
- Layouts that depend on absolute container dimensions for non-arrangement purposes

**`Layout` cache**: For expensive layouts, implement `makeCache(subviews:)` to avoid recomputing across `sizeThatFits` and `placeSubviews` calls. The cache is invalidated automatically when subviews change.

## Design Patterns

- `ContentUnavailableView` for empty/missing data states.
- `Label` over `HStack { Image; Text }` for icon-text pairs.
- Hierarchical styles (`.secondary`, `.tertiary`) over manual opacity.
- `bold()` over `fontWeight(.bold)` — system chooses correct weight for context.
- In `Form`, wrap controls in `LabeledContent` for correct layout.
