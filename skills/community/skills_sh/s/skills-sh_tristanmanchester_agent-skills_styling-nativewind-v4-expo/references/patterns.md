# Component + className patterns

## Default styles + className merge (simple)

Use when you are building app-level components (buttons, cards, typography).

```tsx
import { Text } from "react-native";

type Props = {
  className?: string;
  children: React.ReactNode;
};

export function Label({ className = "", children }: Props) {
  const defaults = "text-black dark:text-white";
  return <Text className={`${defaults} ${className}`}>{children}</Text>;
}
```

## Variants (manual mapping)

Use when you need a small number of variants and want zero dependencies.

```tsx
import { Pressable, Text } from "react-native";

const base = "rounded-md px-4 py-2";
const variants: Record<"primary" | "secondary", string> = {
  primary: "bg-blue-600 active:bg-blue-700",
  secondary: "bg-zinc-200 dark:bg-zinc-800",
};
const label: Record<"primary" | "secondary", string> = {
  primary: "text-white font-semibold",
  secondary: "text-zinc-900 dark:text-zinc-50 font-medium",
};

export function Button({
  variant = "primary",
  className = "",
  labelClassName = "",
  children,
  ...props
}: React.ComponentProps<typeof Pressable> & {
  variant?: "primary" | "secondary";
  labelClassName?: string;
}) {
  return (
    <Pressable className={`${base} ${variants[variant]} ${className}`} {...props}>
      <Text className={`${label[variant]} ${labelClassName}`}>{children}</Text>
    </Pressable>
  );
}
```

## Variants (recommended in larger apps)

If variants are growing complex, use a class name management library:
- `tailwind-variants`
- `cva`
- `clsx` / `classnames`

NativeWind v4 keeps `className` available inside components, so these libraries work well.
