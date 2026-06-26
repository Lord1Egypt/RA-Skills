---
name: api-styled
description: NativeWind v5 styled() for third-party components, nativeStyleToProp mapping
---

# styled() (v5 API)

`styled` is from `react-native-css` and re-exported by Nativewind. It creates a wrapper component with `className` support and optional prop/style mapping. Use it for **third-party** native components that do not accept or pass through `className`. For your own components, pass through `className`; no need for `styled`.

## Usage

**Basic:** Map `className` to the component's default style prop.

```tsx
import { styled } from "nativewind";
import { SomeNativeComponent } from "third-party-library";

const StyledComponent = styled(SomeNativeComponent);
<StyledComponent className="bg-blue-500 p-4" />
```

**Map styles to props:** When a component expects style values as direct props (e.g. SVG `fill`, `width`, `height`), use `nativeStyleToProp`:

```tsx
import { styled } from "nativewind";
import { Svg, Circle } from "react-native-svg";

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

<StyledSvg className="w-24 h-24" viewBox="0 0 100 100">
  <StyledCircle className="fill-green-500 stroke-blue-500 stroke-2" cx="50" cy="50" r="45" />
</StyledSvg>
```

**Multiple style props:** Map multiple className-like props (e.g. FlatList):

```tsx
const StyledFlatList = styled(FlatList, {
  className: "style",
  contentContainerClassName: "contentContainerStyle",
});
```

**remapProps-style behavior:** Use third parameter `{ passThrough: true }`. **Limit transform to returned component:** `{ global: false }`.

## Key Points

- Use `styled()` only for third-party components that don't support `className`. For custom components, accept and forward `className`.
- `nativeStyleToProp` extracts resolved style properties and passes them as props — required for SVG and similar components that take `fill`/`width`/`height` as props.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/styled.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/guides/third-party-components.mdx)
-->
