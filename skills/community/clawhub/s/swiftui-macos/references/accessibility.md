# Accessibility

## VoiceOver

**Icon-only buttons are invisible.** Always include a text label:

```swift
// Bad: VoiceOver can't describe this
Button(action: add) { Image(systemName: "plus") }

// Good
Button("Add Item", systemImage: "plus", action: add)
```

Same applies to `Menu`:

```swift
Menu("Options", systemImage: "ellipsis.circle") { ... }
```

**`onTapGesture` is not a button.** VoiceOver can't activate it. Use `Button` unless you specifically need tap location or count. If `onTapGesture` must be used, add `.accessibilityAddTraits(.isButton)`.

**Decorative images**: `Image(decorative:)` or `.accessibilityHidden(true)`. Flag images with meaningless generated labels like `Image(.newBanner2026)`.

**Complex button labels**: Use `accessibilityInputLabels()` for buttons with dynamic or frequently changing text. For example, a button showing "AAPL $271.68" should have an input label of "Apple" for Voice Control.

## Dynamic Type

- Never hard-code font sizes. Use semantic fonts: `.body`, `.headline`, `.caption`.
- `.caption2` is extremely small — avoid. Even `.caption` should be used carefully.
- Custom sizes: `@ScaledMetric` (macOS 14 and earlier) or `.font(.body.scaled(by:))` (macOS 26+).
- Avoid fixed frames that can't accommodate larger text sizes.

## Reduce Motion

Check `@Environment(\.accessibilityReduceMotion)` and replace motion-heavy animations with opacity crossfades:

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion

withAnimation(reduceMotion ? .none : .spring) {
    // state change
}
```

## Color Independence

When color conveys meaning, check `accessibilityDifferentiateWithoutColor` and add secondary differentiators — icons, patterns, strokes, text labels.

## Accessibility Grouping

Use `accessibilityElement(children:)` to control how VoiceOver navigates composite views:

```swift
// Bad: VoiceOver reads icon, title, subtitle as three separate elements
HStack {
    Image(systemName: "folder")
    VStack(alignment: .leading) {
        Text(item.title)
        Text(item.subtitle).foregroundStyle(.secondary)
    }
}

// Good: combined into one element with composed label
HStack {
    Image(systemName: "folder")
    VStack(alignment: .leading) {
        Text(item.title)
        Text(item.subtitle).foregroundStyle(.secondary)
    }
}
.accessibilityElement(children: .combine)
```

Options: `.combine` (merge children into one element), `.contain` (group as a container), `.ignore` (skip children, provide custom label).

## Custom Control Accessibility

Use `accessibilityRepresentation` to give custom controls standard VoiceOver behavior without restructuring their visual appearance:

```swift
struct StarRating: View {
    @Binding var rating: Int

    var body: some View {
        HStack {
            ForEach(1...5, id: \.self) { star in
                Image(systemName: star <= rating ? "star.fill" : "star")
                    .onTapGesture { rating = star }
            }
        }
        .accessibilityRepresentation {
            Slider(value: .init(get: { Double(rating) }, set: { rating = Int($0) }),
                   in: 1...5, step: 1)
        }
    }
}
```

VoiceOver exposes this as a slider (adjustable trait, increment/decrement) while the visual remains star icons.

## Accessibility Rotors

`accessibilityRotor` defines custom VoiceOver navigation landmarks within a view. Users swipe up/down to jump between matches — essential for long lists, tables, or content with semantic categories:

```swift
List(items) { item in
    ItemRow(item: item)
}
.accessibilityRotor("Pinned") {
    ForEach(items.filter(\.isPinned)) { item in
        AccessibilityRotorEntry(item.title, id: item.id)
    }
}
.accessibilityRotor("Unread") {
    ForEach(items.filter { !$0.isRead }) { item in
        AccessibilityRotorEntry(item.title, id: item.id)
    }
}
```

Without rotors, VoiceOver users must navigate every item linearly. With rotors, they jump directly between pinned items, unread items, or any semantic group you define.

## Programmatic VoiceOver Focus

`@AccessibilityFocusState` moves VoiceOver's cursor programmatically — use after inserting new content, completing async operations, or showing alerts that VoiceOver should announce:

```swift
@AccessibilityFocusState private var focusedItem: Item.ID?

var body: some View {
    List(items) { item in
        ItemRow(item: item)
            .accessibilityFocused($focusedItem, equals: item.id)
    }
}

func addItem() {
    let newItem = Item(...)
    items.append(newItem)
    focusedItem = newItem.id  // VoiceOver jumps to the new item
}
```

Without this, VoiceOver stays wherever it was before the mutation — the user doesn't know something was added.

## Drag and Drop Accessibility

Drag-and-drop is invisible to VoiceOver by default. Provide accessibility actions as alternatives:

```swift
ForEach(items) { item in
    ItemRow(item: item)
        .draggable(item)
        .accessibilityAction(named: "Move Up") {
            moveItem(item, direction: .up)
        }
        .accessibilityAction(named: "Move Down") {
            moveItem(item, direction: .down)
        }
}
.dropDestination(for: Item.self) { items, location in
    // visual drag and drop handling
}
```

Custom accessibility actions appear in VoiceOver's actions menu (swipe up/down with VO). Every reorderable list must provide these.

## macOS Keyboard Navigation

- Every interactive element must be reachable via Tab key.
- Focus rings must be visible — don't suppress or hide them.
- `@FocusState` for managing keyboard focus programmatically.
- Test with Full Keyboard Access enabled in System Settings > Accessibility > Keyboard.
- Add `.keyboardShortcut()` for frequently used actions.
- Ensure custom controls respond to Enter/Space for activation.

## Testing

- **Accessibility Inspector** (Xcode → Open Developer Tool): inspect any element's label, traits, and value. Use the audit feature to catch missing labels and low-contrast text.
- **VoiceOver** (Cmd+F5): navigate the entire interface. Every interactive element should be reachable and clearly described. Test rotors and custom actions.
- **Full Keyboard Access** (System Settings → Accessibility → Keyboard): verify tab order is logical and all actions are triggerable via keyboard.
- **Increase Contrast** and **Reduce Motion**: verify the app respects these preferences. Check `accessibilityReduceMotion`, `accessibilityIncreaseContrast`, `accessibilityDifferentiateWithoutColor` environment values.
