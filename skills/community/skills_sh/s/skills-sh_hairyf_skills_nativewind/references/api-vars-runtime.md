---
name: api-vars-runtime
description: vars(), VariableContextProvider, useUnstableNativeVariable for runtime CSS variables
---

# vars() & Runtime CSS Variables

NativeWind provides `vars()` and `VariableContextProvider` to set CSS custom properties from JavaScript. Variables flow down the tree like CSS custom properties and can be consumed with `var(--name)` in class names or CSS.

## Usage

**vars()** — Takes an object of variable names and values; returns a style object. Apply to `style` so descendants can use `var(--name)`:

```tsx
import { View, Text } from "react-native";
import { vars } from "nativewind";

function ThemedSection({ brandColor }) {
  return (
    <View style={vars({ "--brand-color": brandColor })}>
      <Text className="text-[--brand-color]">Themed text</Text>
    </View>
  );
}
```

Combine with other styles by spreading:

```tsx
<View style={[{ padding: 16 }, vars({ "--accent": "blue" })]} />
```

**VariableContextProvider** — Sets variables via React context so they are available to components that are not direct style descendants:

```tsx
import { VariableContextProvider } from "nativewind";

function App() {
  return (
    <VariableContextProvider variables={{ "--theme-color": "#3b82f6" }}>
      <Text className="text-[--theme-color]">Blue text</Text>
    </VariableContextProvider>
  );
}
```

**useUnstableNativeVariable()** — (Unstable) Reads the current value of a CSS variable from the nearest variable context for use in JavaScript:

```tsx
import { useUnstableNativeVariable } from "nativewind";

function MyComponent() {
  const themeColor = useUnstableNativeVariable("--theme-color");
  // Use themeColor in JS logic
}
```

## Key Points

- Use `vars()` for scoped runtime theming; use `VariableContextProvider` when the consumer is not a style child.
- Variables set in CSS (`:root { --x: ... }`) or via `vars()`/provider are consumed the same way in class names: `className="text-[--x]"`.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/vars.mdx)
-->
