---
name: best-practices-performance
description: Style correctness, debugging, and common pitfalls
---

# Best Practices and Troubleshooting

Practices that avoid React Native styling pitfalls and how to verify or debug NativeWind.

## Usage

**Explicit light and dark** — Avoid styles that apply only in one mode; React Native can misbehave with conditionally applied styles:

```tsx
<Text className="text-black dark:text-white" />
{/* Prefer both; avoid only dark:text-white */}
```

**Colors on the right element** — `color` does not cascade from `View` to `Text` on native. Put text color classes on `Text` (or the component that actually accepts `color`):

```tsx
<View>
  <Text className="text-red-500">Hello</Text>
</View>
{/* Not: <View className="text-red-500"><Text>Hello</Text></View> */}
```

**Modifiers require component support** — `hover:` needs `onHoverIn`/`onHoverOut`; `active:` needs `onPressIn`/`onPressOut`; `focus:` needs `onFocus`/`onBlur`. Use `Pressable` or `TextInput` where needed; plain `View`/`Text` don't support hover.

**Inline style precedence** — Inline `style` overrides `className`-derived styles when both are present (style specificity).

**Cache** — When something looks wrong, clear the Metro cache: `npx expo start --clear` (or framework equivalent). Ensure the correct `global.css` is used and that Tailwind CLI can compile it: `npx @tailwindcss/cli --input ./global.css --output output.css`; if the rule is missing in output, the issue is Tailwind/content, not NativeWind runtime.

**Debug** — Run with `DEBUG=nativewind` (Mac/Linux) or `set "DEBUG=nativewind" && <start-command>` (Windows) to get debug output; useful when reporting issues.

**Verify installation** — Call `verifyInstallation()` from `nativewind` inside a component (not globally) to confirm setup:

```tsx
import { verifyInstallation } from "nativewind";
function App() {
  verifyInstallation();
  return (/* ... */);
}
```

**Flex defaults** — React Native's default flex behavior differs from web; use `flex-1` or explicit `flex-direction` when layout doesn't match expectations.

## Key Points

- Always pair light and dark classes; put color utilities on the component that accepts `color` (e.g. `Text`).
- Clear cache and confirm Tailwind output before blaming the runtime; use `DEBUG=nativewind` and `verifyInstallation()` when debugging.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/dark-mode.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/style-specificity.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/getting-started/troubleshooting.mdx)
-->
