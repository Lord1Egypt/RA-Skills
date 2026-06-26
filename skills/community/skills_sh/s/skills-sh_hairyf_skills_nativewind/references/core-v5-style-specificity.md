---
name: core-v5-style-specificity
description: NativeWind v5 style specificity order, !important, merging className and style prop
---

# v5 Style Specificity

NativeWind uses a specificity model consistent with CSS, adapted for React Native's inline-style model. Order of application matters when the same property is set in multiple places.

## Usage

**Which class wins:** When multiple classes set the same property, the **last class in the stylesheet** (CSS source order) wins, not the order in `className`:

```tsx
<Text className="text-blue-500 text-red-500" />
// Winner: whichever of "blue" / "red" is declared later in CSS
```

**Specificity order (lowest → highest):**

1. Base utility classes (e.g. `text-red-500`)
2. Modifier styles (e.g. `hover:text-blue-500`)
3. Inline `style` prop — overrides `className`
4. `!important` — overrides everything including inline styles

```tsx
<Text className="text-white" style={{ color: "black" }} />
// Result: color is "black" (style wins)

<Text className="!text-white" style={{ color: "black" }} />
// Result: color is "#fff" (!important wins)
```

**Merging className and style:** NativeWind merges both. Same property: `style` wins unless the class uses `!important`. Different properties: both apply.

```tsx
<View className="p-4" style={{ backgroundColor: "red" }} />
// Result: { padding: 16, backgroundColor: "red" }
```

**Composing components:** Accept `className` and concatenate so CSS source order controls override:

```tsx
function MyText({ className, ...props }) {
  return <Text className={`text-base text-black ${className}`} {...props} />;
}
<MyText className="text-red-500" />
```

## Key Points

- Inline `style` overrides `className` for the same property; use `!` prefix in class for Tailwind's important to override inline.
- For custom components, pass through `className` and append; the last class in the final string wins by CSS order.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/style-specificity.mdx)
-->
