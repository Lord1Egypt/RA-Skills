---
name: features-v5-third-party-guide
description: Styling third-party components — when className is not passed, multiple style props, dynamic mapping
---

# v5 Styling Third-Party Components

Third-party components often "pick" props and don't pass `className` down. Prefer contributing a fix (pass `...props`); when that's not possible, use `styled()` (or legacy `cssInterop`/`remapProps`) and, for multiple similar props, the dynamic mapping modifier.

## Usage

**Components that don't pass className:** Use `styled(ThirdPartyComponent, { className: "style" })`. If the component expects style values as direct props (e.g. `backgroundColor`), use `nativeStyleToProp` in the config.

**Multiple style props:** e.g. FlatList has `style` and `contentContainerStyle`. Map multiple classNames:

```tsx
styled(FlatList, {
  className: "style",
  contentContainerClassName: "contentContainerStyle",
});
```

**Components that read `style` directly:** If a component derives values from `style` (e.g. `backgroundColor = style.color`), NativeWind still resolves `className` to a style object; use `styled()` so the component receives the resolved style.

**Multiple similar props (e.g. labelColor, inputColor):** Use the **dynamic mapping modifier** so one `className` can target different props. In v5 the syntax is `@prop-[propName]:utility` (v4 used `{}-[propName]:utility`):

- `@prop-[propName]` — Move resolved style to `propName` prop.
- `@prop-[propName]:style-property` — Map only that style property to `propName`.

Example (conceptual):

```tsx
// Nested: screenOptions.tabBarTintColor
className="@prop-[screenOptions.tabBarTintColor]/color:color-red-500"
```

**TypeScript:** Extend module declarations so custom className props are typed; the interface must match the third-party props (including extends/generics).

## Key Points

- Prefer fixing the library to pass through props; then `className` works without wrapper.
- `styled()` (and cssInterop) add runtime cost; use only where necessary.
- For multiple style-like props, use multiple keys in `styled()` config or the `@prop` dynamic mapping modifier.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/guides/third-party-components.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/css-interop.mdx)
-->
