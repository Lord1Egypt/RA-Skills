---
name: features-states
description: Pseudo-classes, group modifiers, dark mode, and data attributes
---

# States, Pseudo-classes, and Dark Mode

NativeWind supports hover/focus/active, disabled/empty, selection/placeholder, group modifiers, dark mode, and data-attribute selectors.

## Usage

**Hover, focus, active** — Require the component to support the corresponding events (e.g. `Pressable`, `TextInput` support hover/press/focus):

```tsx
<Pressable className="bg-blue-500 active:bg-blue-700">
  <Text className="text-white">Press Me</Text>
</Pressable>
<TextInput className="hover:border-gray-400 focus:border-blue-500" />
```

Modifiers: `hover:` (onHoverIn/onHoverOut), `active:` (onPressIn/onPressOut), `focus:` (onFocus/onBlur). Combine as needed: `hover:active:focus:border-blue-500`.

**Disabled and empty** — `disabled:` when `disabled={true}`; `empty:` when the component has no children.

**Selection and placeholder** — `selection:*` and `placeholder:*` for text selection and placeholder styling.

**Group (parent state)** — Tag parent with `group/name`, children with `group-hover/name:`, `group-active/name:`, `group-focus/name:`:

```tsx
<Pressable className="group/card">
  <View className="group-active/card:bg-blue-100">
    <Text className="group-active/card:text-blue-700">Press the card</Text>
  </View>
</Pressable>
```

**Dark mode** — Use `dark:` with system preference (no config). For manual toggle use React Native's `Appearance.setColorScheme()` and `useColorScheme()` from `react-native` (NativeWind's `useColorScheme` is deprecated in v5):

```tsx
import { useColorScheme, Appearance } from "react-native";
const colorScheme = useColorScheme();
Appearance.setColorScheme(nextScheme);
```

Always provide both light and dark styles to avoid RN conditional-style issues: `className="text-black dark:text-white"` instead of only `dark:text-white`.

**Data attributes** — Use `[&[data-active]]:bg-green-500` and pass `dataSet={{ active: value }}` for state-driven styling.

**Direction** — `ltr:` and `rtl:` for direction-aware styles.

## Key Points

- `hover:`/`active:`/`focus:` only work on components that forward the matching event props (e.g. Pressable, TextInput); not on plain View/Text.
- Dark mode: use `dark:` plus system or `Appearance.setColorScheme`; always pair light and dark classes.
- Group names allow multiple groups in one tree: `group/card` and `group/item` with corresponding `group-*/card` and `group-*/item` modifiers.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/states.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/dark-mode.mdx)
- https://github.com/nativewind/website (sources/nativewind/content/v5/api/use-color-scheme.mdx)
-->
