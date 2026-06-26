---
name: features-v5-states-pseudo
description: v5 pseudo-classes (hover, focus, active, disabled, empty), selection/placeholder, group, ltr/rtl
---

# v5 States & Pseudo-classes

NativeWind v5 supports pseudo-class modifiers that map to React Native event props or component state. The component must support the corresponding event prop for hover/focus/active to work.

## Usage

**Hover, focus, active:**

| Modifier | Pseudo-class | Activating event | Deactivating event |
|----------|--------------|------------------|--------------------|
| `hover:` | :hover | onHoverIn | onHoverOut |
| `active:` | :active | onPressIn | onPressOut |
| `focus:` | :focus | onFocus | onBlur |

Available on components like `Pressable`, `TextInput` — not on `View` or `Text` alone.

```tsx
<Pressable className="bg-blue-500 active:bg-blue-700">
  <Text className="text-white">Press Me</Text>
</Pressable>
```

Combine: `hover:active:focus:border-blue-500` (all conditions must be met).

**Disabled & empty:**

| Modifier | Condition |
|----------|-----------|
| `disabled:` | Component has `disabled={true}` |
| `empty:` | Component has no children |

**Selection & placeholder:** `selection:` for text selection color; `placeholder:` for placeholder text (e.g. on TextInput).

**Data attributes:** Use `[data-*]` selectors with `dataSet`:

```tsx
<View
  className="[&[data-active]]:bg-green-500 [&[data-active='false']]:bg-gray-500"
  dataSet={{ active: active }}
/>
```

**Group (parent state):** Parent: `group/name`; children: `group-hover/name:`, `group-active/name:`, `group-focus/name:`:

```tsx
<Pressable className="group/card">
  <View className="group-active/card:bg-blue-100">
    <Text className="group-active/card:text-blue-700">Press the card</Text>
  </View>
</Pressable>
```

**LTR / RTL:** `ltr:` and `rtl:` for direction-aware styles.

## Key Points

- Hover/focus/active require the component to support the corresponding event props.
- Group names allow multiple groups on a page; use `group/{name}` and `group-{modifier}/{name}:`.

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/states.mdx)
-->
