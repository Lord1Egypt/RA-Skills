# Theming + dark mode (NativeWind v4)

## Dark mode: system vs manual

- Read system preference via `useColorScheme()`.
- Allow user override via `colorScheme.set("light" | "dark" | "system")`.

Expo note: to follow system appearance, set `userInterfaceStyle` to `automatic` in `app.json`.

### Minimal toggle

```tsx
import { useState } from "react";
import { Pressable, Text, View } from "react-native";
import { colorScheme } from "nativewind";

export function ThemeToggle() {
  const [current, setCurrent] = useState<"light" | "dark">("light");
  return (
    <View className="items-center">
      <Pressable
        onPress={() => {
          const next = current === "light" ? "dark" : "light";
          setCurrent(next);
          colorScheme.set(next);
        }}
      >
        <Text className="font-semibold">{current}</Text>
      </Pressable>
    </View>
  );
}
```

## Dynamic themes with CSS variables

### 1) Define colours in tailwind.config.js

Create theme colours that point at CSS variables:

```js
module.exports = {
  theme: {
    colors: {
      primary: "rgb(var(--color-primary) / <alpha-value>)",
      secondary: "rgb(var(--color-secondary) / <alpha-value>)",
    },
  },
};
```

Set defaults on `:root` (via Tailwind `addBase`) if you want stable defaults:

```js
plugins: [
  ({ addBase }) =>
    addBase({
      ":root": {
        "--color-primary": "0 0 0",
        "--color-secondary": "255 255 255",
      },
    }),
];
```

### 2) Override variables at runtime with vars()

```tsx
import { vars, useColorScheme } from "nativewind";
import { Text, View } from "react-native";

const themes = {
  brand: {
    light: vars({ "--color-primary": "0 0 0", "--color-secondary": "255 255 255" }),
    dark: vars({ "--color-primary": "255 255 255", "--color-secondary": "24 24 27" }),
  },
};

export function ThemedCard({ children }: { children: React.ReactNode }) {
  const { colorScheme } = useColorScheme();
  return (
    <View style={themes.brand[colorScheme]} className="rounded-xl bg-secondary p-4">
      <Text className="text-primary">{children}</Text>
    </View>
  );
}
```

Guideline: keep your “theme contract” small (a handful of variables), then build design tokens around it.
