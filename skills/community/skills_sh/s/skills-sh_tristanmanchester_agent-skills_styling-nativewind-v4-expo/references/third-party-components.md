# Third‑party components (remapProps / cssInterop)

## Decision guide

- Prefer **plain `className`** when the component forwards `className` correctly.
- Use **`remapProps`** when a component has *multiple style props* and you want `*Class` props.
- Use **`cssInterop`** when you need to map a class prop to a style prop (and optionally extract style attributes into non-style props).

Avoid using these for your own app components; for your own components, accept `className` and merge it.

## remapProps (multiple style props)

```tsx
import { remapProps } from "nativewind";

/**
 * ThirdPartyButton has buttonStyle + labelStyle
 */
const StyledThirdPartyButton = remapProps(ThirdPartyButton, {
  buttonClass: "buttonStyle",
  labelClass: "labelStyle",
});

// Usage
<StyledThirdPartyButton buttonClass="bg-blue-500" labelClass="text-white" />;
```

Notes:
- `remapProps(component, { "new-prop": "existing-prop" })` creates a new prop and maps it.
- `remapProps(component, { prop: true })` overrides an existing prop.

## cssInterop (map className → style, extract attributes)

Example based on `TextInput` patterns:

```tsx
import { TextInput } from "react-native";
import { cssInterop } from "nativewind";

cssInterop(TextInput, {
  className: {
    target: "style",
    nativeStyleToProp: {
      textAlign: true,
    },
  },
  placeholderClassName: {
    target: false,
    nativeStyleToProp: {
      color: "placeholderTextColor",
    },
  },
  selectionClassName: {
    target: false,
    nativeStyleToProp: {
      color: "selectionColor",
    },
  },
});
```

Guidelines:
- Call `cssInterop(...)` once (at app entry) before the component is rendered.
- Keep mappings tiny and explicit; do not “globally interop everything”.

## Editor IntelliSense for custom props (VS Code)

If you introduce custom class props (e.g. `headerClassName`), extend Tailwind IntelliSense:

```json
{
  "tailwindCSS.classAttributes": ["class", "className", "headerClassName"]
}
```
