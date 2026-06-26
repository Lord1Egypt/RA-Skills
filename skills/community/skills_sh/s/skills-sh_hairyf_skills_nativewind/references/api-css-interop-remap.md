---
name: api-css-interop-remap
description: cssInterop and remapProps (v5 deprecated in favor of styled); multiple className props, nativeStyleToProp
---

# cssInterop & remapProps (Legacy / Deprecated in v5)

`cssInterop` and `remapProps` enable `className` (or custom prop) support on components that don't support it. In **v5 these are deprecated** in favor of the unified `styled()` API; prefer `styled()` for new code. This reference documents behavior for migration or when maintaining v4 code.

## Usage

**cssInterop** — Tag a component so NativeWind resolves `className` into styles. Use when a third-party component has a `style` prop but does not accept `className`:

```tsx
import { cssInterop } from "nativewind";
import { MapView } from "react-native-maps";

cssInterop(MapView, { className: "style" });
<MapView className="w-full h-64" />
```

Map to specific props and extract style properties as props (`nativeStyleToProp`):

```tsx
cssInterop(component, {
  className: {
    target: "style",
    nativeStyleToProp: { height: true, width: true },
  },
});
```

Multiple style props:

```tsx
cssInterop(FlatList, {
  className: "style",
  contentContainerClassName: "contentContainerStyle",
});
```

**remapProps** — Simpler prop renaming only:

```tsx
import { remapProps } from "nativewind";

const CustomButton = remapProps(ThirdPartyButton, {
  buttonClass: "buttonStyle",
  labelClass: "labelStyle",
});
```

Options: `remapProps(component, { newProp: "existingStyleProp" })` or `{ existingProp: true }` to accept className on existing prop.

## Key Points

- **v5:** Use `styled(Component, config)` instead of `cssInterop`; use `styled(Component, config, { passThrough: true })` instead of `remapProps`. Same options (e.g. `nativeStyleToProp`, multiple className keys) are supported.
- Enabling cssInterop/styled on a component has a performance cost (style resolution, event handlers, context).

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/css-interop.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/guides/migrate-from-v4.mdx)
-->
