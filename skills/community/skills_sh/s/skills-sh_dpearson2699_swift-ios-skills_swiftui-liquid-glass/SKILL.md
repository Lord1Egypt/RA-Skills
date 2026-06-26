---
name: swiftui-liquid-glass
description: "Implement, review, or improve SwiftUI Liquid Glass effects for iOS 26+. Covers glassEffect modifier, GlassEffectContainer, glass button styles, glass toolbar/tab bar, static status badges vs interactive controls, morphing transitions, tinting, interactive glass, ToolbarSpacer, scrollEdgeEffectStyle, backgroundExtensionEffect, and availability gating. Use when asked about Liquid Glass, glass buttons, glassEffect, GlassEffectTransition, glassEffectID, glassEffectUnion, scroll edge effects, or adopting iOS 26 design."
---

# SwiftUI Liquid Glass

Liquid Glass is the dynamic translucent material introduced in iOS 26 (and iPadOS 26,
macOS 26, tvOS 26, watchOS 26). It blurs content behind it, reflects surrounding color
and light, and reacts to touch and pointer interactions. Standard SwiftUI components
(tab bars, toolbars, navigation bars, sheets) adopt Liquid Glass automatically when
built with the iOS 26 SDK. Treat custom Liquid Glass as a controls/navigation-layer
effect, not a general content background. Use the APIs below for custom views and
controls that need that functional layer.

See [references/liquid-glass.md](references/liquid-glass.md) for the full API reference with additional examples.

## Contents

- [Workflow](#workflow)
- [Core API Summary](#core-api-summary)
- [Code Examples](#code-examples)
- [Common Mistakes](#common-mistakes)
- [Review Checklist](#review-checklist)
- [References](#references)

## Workflow

Choose the path that matches the request:

### 1. Implement a new feature with Liquid Glass

1. Identify target surfaces (floating controls, custom bars, transient controls).
2. Decide shape, prominence, and whether each element is a real control or static status.
3. Wrap grouped glass elements in a `GlassEffectContainer`.
4. Apply `.glassEffect()` **after** layout and appearance modifiers.
5. Add `.interactive()` only to tappable/focusable elements.
6. Add morphing transitions with `glassEffectID(_:in:)` where the view hierarchy
   changes with animation. Put `glassEffectTransition(_:)` on the inserted or
   removed glass child, not on the always-present container. Name the transition
   choice: `.matchedGeometry` for nearby effects inside container spacing;
   `.materialize` for distant insertion/removal or no geometry match.
7. Gate with `if #available(iOS 26, *)` and provide a fallback for earlier versions.

### 2. Improve an existing feature with Liquid Glass

1. Find custom control or navigation backgrounds that can be replaced with `.glassEffect()`.
2. Wrap sibling glass elements in `GlassEffectContainer` for blending and performance.
3. Replace custom glass-like buttons with `.buttonStyle(.glass)`, `.buttonStyle(.glassProminent)`, or configurable styles such as `.buttonStyle(.glass(.clear))`. Use `.glass(_:)` when the button needs a specific tint or variant; reserve `.glassProminent` for high-emphasis primary actions.
4. Add morphing transitions where animated insertion/removal occurs.

### 3. Review existing Liquid Glass usage

Run through the Review Checklist below and verify each item.

## Core API Summary

### glassEffect(_:in:)

Applies Liquid Glass behind a view. Default: `.regular` variant in a `Capsule` shape.

```swift
nonisolated func glassEffect(
    _ glass: Glass = .regular,
    in shape: some Shape = DefaultGlassEffectShape()
) -> some View
```

### Glass struct

| Property / Method | Purpose |
|---|---|
| `.regular` | Standard glass material |
| `.clear` | Clear variant; add dimming/contrast treatment when legibility needs it |
| `.identity` | No visual effect (pass-through) |
| `.tint(_:)` | Add a color tint for prominence |
| `.interactive(_:)` | React to touch and pointer interactions |

Chain them: `.regular.tint(.blue).interactive()`

### GlassEffectContainer

Wraps multiple glass views for shared rendering, blending, and morphing.

```swift
GlassEffectContainer(spacing: 24) {
    // child views with .glassEffect()
}
```

The `spacing` controls when nearby glass shapes begin to blend. Match or exceed
the interior layout spacing so shapes merge during animated transitions but remain
separate at rest.

### Morphing & Transitions

| Modifier | Purpose |
|---|---|
| `glassEffectID(_:in:)` | Stable identity for morphing during view hierarchy changes |
| `glassEffectUnion(id:namespace:)` | Merge multiple views into one glass shape |
| `glassEffectTransition(_:)` | Control how glass appears/disappears |

Transition decision: use `.matchedGeometry` for nearby effects inside the container's
spacing; use `.materialize` for distant insertion/removal or when no geometry match
should occur; use `.identity` only when no transition animation is wanted.

### Button Styles

```swift
Button("Action") { }
    .buttonStyle(.glass)           // standard glass button

Button("Primary") { }
    .buttonStyle(.glassProminent)  // prominent glass button

Button("Media") { }
    .buttonStyle(.glass(.clear))    // configurable variant; verify contrast
```

### Scroll Edge Effects and Background Extension (iOS 26+)

These complement Liquid Glass when building custom toolbars and scroll views:

```swift
ScrollView {
    content
}
.scrollEdgeEffectStyle(.soft, for: .top)  // Configures edge effect at scroll boundaries

// Duplicate view into mirrored copies at safe area edges with blur (e.g., under sidebars)
content
    .backgroundExtensionEffect()
```

### ToolbarSpacer (iOS 26+)

Creates a visual break between items in toolbars:

```swift
.toolbar {
    ToolbarItem { Button("Edit") { } }
    ToolbarSpacer(.fixed)
    ToolbarItem { Button("Share") { } }
}
```

## Code Examples

### Glass button with availability gate

```swift
if #available(iOS 26, *) {
    Button("Show Status") { showStatusDetails() }
        .buttonStyle(.glass)
} else {
    Button("Show Status") { showStatusDetails() }
        .buttonStyle(.bordered)
}
```

### Grouped glass shapes in a container

```swift
let symbols = ["pencil", "eraser.fill", "lasso"]

GlassEffectContainer(spacing: 24) {
    HStack(spacing: 24) {
        ForEach(symbols, id: \.self) { symbol in
            Image(systemName: symbol)
                .frame(width: 56, height: 56)
                .glassEffect()
        }
    }
}
```

### Nearby morphing transition

```swift
@State private var isExpanded = false
@Namespace private var ns

var body: some View {
    GlassEffectContainer(spacing: 40) {
        HStack(spacing: 40) {
            Image(systemName: "pencil")
                .frame(width: 80, height: 80)
                .glassEffect()
                .glassEffectID("pencil", in: ns)

            if isExpanded {
                Image(systemName: "eraser.fill")
                    .frame(width: 80, height: 80)
                    .glassEffect()
                    .glassEffectID("eraser", in: ns)
                    .glassEffectTransition(.matchedGeometry)
            }
        }
    }

    Button("Toggle") {
        withAnimation { isExpanded.toggle() }
    }
    .buttonStyle(.glass)
}
```

For distant inserted or removed glass that should not morph from a nearby control,
use `.glassEffectTransition(.materialize)` on the conditional child instead.

### Unioning views into a single glass shape

```swift
@Namespace private var ns

GlassEffectContainer(spacing: 20) {
    HStack(spacing: 20) {
        ForEach(items.indices, id: \.self) { i in
            Image(systemName: items[i])
                .frame(width: 80, height: 80)
                .glassEffect()
                .glassEffectUnion(id: i < 2 ? "group1" : "group2", namespace: ns)
        }
    }
}
```

### Tinted glass icon control

```swift
struct GlassIconControl: View {
    let icon: String
    let tint: Color
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Image(systemName: icon)
                .font(.title2)
                .padding()
        }
        .buttonStyle(.glass(.regular.tint(tint)))
    }
}
```

### Clear glass action over bright content

```swift
if #available(iOS 26, *) {
    ZStack {
        Capsule()
            .fill(.black.opacity(0.28))

        Button {
            playRecap()
        } label: {
            Label("Play", systemImage: "play.fill")
                .font(.headline)
                .padding(.horizontal, 8)
        }
        .buttonStyle(.glass(.clear))
    }
    .fixedSize()
} else {
    Button("Play", systemImage: "play.fill") { playRecap() }
        .buttonStyle(.borderedProminent)
}
```

Use clear glass only when the background still leaves labels and symbols readable.
On bright or busy backgrounds, add a subtle dimming layer or choose a more opaque
button style.

### Static status count, not a toolbar control

```swift
VStack(spacing: 8) {
    Text("24")
        .font(.headline.monospacedDigit())
        .accessibilityLabel("24 options expiring")

    Text("Options Expiring")
        .font(.subheadline)
        .foregroundStyle(.secondary)
}
// Keep read-only status out of toolbar control slots and do not add .interactive().
```

## Common Mistakes

### DON'T: Apply Liquid Glass to every surface

Overuse distracts from content. Liquid Glass belongs in the controls/navigation layer;
do not use it to decorate static content containers.

```swift
// WRONG: Glass on everything
VStack {
    Text("Title").glassEffect()
    Text("Subtitle").glassEffect()
    Divider().glassEffect()
    Text("Body").glassEffect()
}

// CORRECT: Static content stays in the content layer
VStack {
    Text("Title").font(.title)
    Text("Subtitle").font(.subheadline)
    Divider()
    Text("Body")
}

Button("Add") { addItem() }
    .buttonStyle(.glass)
```

### DON'T: Make static status look tappable

Counts, badges, summaries, and read-only status chips should not live in toolbar
action slots or use `.interactive()` unless they initiate an immediate action. If a
badge belongs to a real toolbar action, make the action one accessible control and
keep the badge subordinate to that control.

### DON'T: Nest GlassEffectContainer for one related group

Use one container for the related glass group so rendering, blending, and morphing
scope stay predictable.

```swift
// WRONG
GlassEffectContainer {
    GlassEffectContainer {
        content.glassEffect()
    }
}

// CORRECT: Single container wrapping all glass views
GlassEffectContainer {
    content.glassEffect()
}
```

### DON'T: Add .interactive() to non-interactive elements

`.interactive()` adds visual affordance suggesting tappability. Using it on decorative
or read-only status glass misleads users.

### DON'T: Apply .glassEffect() before layout modifiers

Glass calculates its shape from the final frame. Applying it before padding/frame produces incorrect bounds.

```swift
// WRONG: Glass applied before padding
Text("Label").glassEffect().padding()

// CORRECT: Glass applied after layout
Text("Label").padding().glassEffect()
```

### DON'T: Forget accessibility testing

Always test with Reduce Transparency and Reduce Motion enabled. System settings can
remove or modify translucency and motion, so verify custom glass content remains readable.

### DON'T: Skip availability checks

Liquid Glass requires iOS 26+. Gate with `if #available(iOS 26, *)` and provide a fallback.

## Review Checklist

- [ ] **Availability**: `if #available(iOS 26, *)` present with fallback UI.
- [ ] **Container**: Multiple glass views wrapped in `GlassEffectContainer`.
- [ ] **Modifier order**: `.glassEffect()` applied after layout/appearance modifiers.
- [ ] **Interactivity**: `.interactive()` used only where user interaction exists.
- [ ] **Status vs action**: Static counts/status are not toolbar controls and do not expose press/hover affordance.
- [ ] **Transitions**: `glassEffectID` used with `@Namespace` for morphing animations.
- [ ] **Transition type**: `.matchedGeometry` for nearby effects; `.materialize` for distant ones, applied to the conditional glass child.
- [ ] **Consistency**: Shapes, tints, and spacing are uniform across related elements.
- [ ] **Performance**: Glass effects are limited in number; container used for grouping.
- [ ] **Accessibility**: Tested with Reduce Transparency and Reduce Motion enabled.
- [ ] **Button styles**: Standard `.glass`, `.glassProminent`, or configurable `.glass(_:)` used for buttons; `.glass(_:)` is primary when a tint or clear variant is required.
- [ ] **Clear glass contrast**: Clear glass over bright content has a dimming/contrast treatment or uses a more legible style.
- [ ] **Concurrency**: IDs passed to `glassEffectID` / `glassEffectUnion` are `Sendable`; MainActor-annotated Liquid Glass APIs stay in SwiftUI UI code.

## References

- Full API guide: [references/liquid-glass.md](references/liquid-glass.md)
- Apple docs: [Applying Liquid Glass to custom views](https://sosumi.ai/documentation/swiftui/Applying-Liquid-Glass-to-custom-views)
- Apple docs: [Adopting Liquid Glass](https://sosumi.ai/documentation/technologyoverviews/adopting-liquid-glass)
