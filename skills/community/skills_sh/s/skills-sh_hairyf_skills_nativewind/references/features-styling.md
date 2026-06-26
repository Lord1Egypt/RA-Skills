---
name: features-styling
description: className usage, custom components, and third-party styling with styled/cssInterop/remapProps
---

# Styling Components with NativeWind

Use `className` on core RN components; for custom components pass it through. For third-party components that don't support `className`, use `styled` (or the deprecated `cssInterop` / `remapProps`).

## Usage

**Core and custom components** — Use `className`; custom components should accept and merge it:

```tsx
function MyComponent({ className, ...props }) {
  return <Text className={`text-black dark:text-white ${className}`} {...props} />;
}
<MyComponent className="font-bold" />
```

For multiple style props (e.g. button + label), accept multiple classNames and pass to the right element:

```tsx
function Button({ className, textClassName, ...props }) {
  return (
    <View className={className}>
      <Text className={textClassName}>Label</Text>
    </View>
  );
}
```

**Third-party components** — Use `styled()` (preferred in v5). Maps `className` → `style` and can map style properties to specific props:

```tsx
import { styled } from "nativewind";
import { SomeNativeComponent } from "third-party-library";

const StyledComponent = styled(SomeNativeComponent);
<StyledComponent className="bg-blue-500 p-4" />
```

Map style properties to props (e.g. for SVG or components that expect `height`/`width`/`fill` as props):

```tsx
const StyledSvg = styled(Svg, {
  className: {
    target: "style",
    nativeStyleToProp: { height: true, width: true },
  },
});
const StyledCircle = styled(Circle, {
  className: {
    target: "style",
    nativeStyleToProp: { fill: true, stroke: true, strokeWidth: true },
  },
});
```

**Multiple style props on one component** — Use `remapProps`-style mapping via `styled`; the API supports multiple className-like props (e.g. `contentContainerClassName` → `contentContainerStyle`):

```tsx
remapProps(FlatList, {
  className: "style",
  contentContainerClassName: "contentContainerStyle",
  ListHeaderComponentClassName: "ListHeaderComponentStyle",
  ListFooterComponentClassName: "ListFooterComponentStyle",
  columnWrapperClassName: "columnWrapperStyle",
});
```

In v5, prefer `styled(FlatList, { className: "style", contentContainerClassName: "contentContainerStyle" })` (same idea). `styled(Component, config, { passThrough: true })` replicates `remapProps` behavior; `{ global: false }` limits the transform to the returned component.

## Key Points

- Your own components: only pass through and merge `className`; no `styled`/`cssInterop`/`remapProps` unless wrapping a native/third-party component that doesn't support `className`.
- Third-party: use `styled()` for a single or multiple `className` → style prop mappings and optional `nativeStyleToProp` for props like `fill`, `width`, `height`.
- NativeWind resolves `className` into style objects; third-party components receive a style object (or a special empty-looking object when using remap-style APIs so they don't break).

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/index.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/styled.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/css-interop.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/guides/custom-components.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/guides/third-party-components.mdx)
-->
