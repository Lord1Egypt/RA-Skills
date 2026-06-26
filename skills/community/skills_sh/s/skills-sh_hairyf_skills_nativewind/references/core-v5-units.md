---
name: core-v5-units
description: NativeWind v5 supported CSS units on native (px, %, vw/vh, rem, em), dp vs px, rem sizing
---

# v5 Units

NativeWind v5 supports a subset of CSS units on native; behavior differs from web where needed for React Native's layout engine.

## Usage

**Supported units:**

| Unit | Name | Native behavior |
|------|------|-----------------|
| `px` | Pixels | Treated as density-independent pixels (dp). `10px` → `10` in RN style. |
| `%` | Percentage | Relative to parent, same as CSS. |
| `vw` | Viewport width | Polyfilled with `Dimensions.get('window').width`; reactive to window size. |
| `vh` | Viewport height | Polyfilled with `Dimensions.get('window').height`; reactive. |
| `rem` | Root EM | Relative to root font size. Default **14** on native, **16** on web. |
| `em` | EM | Relative to current element's font size. |

**Ratio values** (e.g. `aspect-ratio: 16/9`) are supported on native.

**Override rem:**

```css
:root {
  font-size: 16px;
}
```

Or set via CSS variable on a parent. React Native `<Text />` defaults to `fontSize: 14`; NativeWind uses `rem` 14 on native and 16 on web to align with Tailwind's spacing scale.

## Key Points

- React Native uses dp; web uses px. NativeWind treats `px` in CSS as dp on native — use `px` in theme/CSS and conversion is automatic.
- Do not mix numerical and percentage units in `calc()` on native (e.g. `calc(100% - 20px)` is not supported by RN layout).

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/units.mdx)
-->
