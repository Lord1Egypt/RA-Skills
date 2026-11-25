> Subclip sandbox: use only pinned, validated imports and native Subclip tools. Package/skill installation, external CLI execution, provider API keys, and standalone project setup are unavailable. Verify managed resources before use; use a supported alternative when unavailable.

For local font files, use the `@remotion/fonts` package.

### Prerequisites

Use the dependency already provided by Subclip. If the import is unavailable, choose a supported alternative; do not install packages inside the layer.

Subclip manages dependencies and execution. Use the installed runtime and native Subclip tools; package installation and standalone CLI execution are unavailable inside a layer.


### Loading a local font

Place your font file in the `public/` folder and use `loadFont()`:

```tsx
import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

await loadFont({
  family: "MyFont",
  url: staticFile("MyFont-Regular.woff2"),
});

export const MyComposition = () => {
  return (
    <div style={{ fontFamily: "MyFont" }}>
      Hello World
    </div>
  );
};
```

### Loading multiple weights

Load each weight separately with the same family name:

```tsx
import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

await Promise.all([
  loadFont({
    family: "Inter",
    url: staticFile("Inter-Regular.woff2"),
    weight: "400",
  }),
  loadFont({
    family: "Inter",
    url: staticFile("Inter-Bold.woff2"),
    weight: "700",
  }),
]);
```

### Available options

```tsx
loadFont({
  family: "MyFont", // Required: name to use in CSS
  url: staticFile("font.woff2"), // Required: font file URL
  format: "woff2", // Optional: auto-detected from extension
  weight: "400", // Optional: font weight
  style: "normal", // Optional: normal or italic
  display: "block", // Optional: font-display behavior
});
```
