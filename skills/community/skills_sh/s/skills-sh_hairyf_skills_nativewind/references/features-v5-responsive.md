---
name: features-v5-responsive
description: NativeWind v5 responsive breakpoints, media queries on native, platform media, reactive updates
---

# v5 Responsive Design

NativeWind supports responsive design on native via Tailwind breakpoint variants and media queries keyed to window dimensions; updates are reactive (e.g. rotation, split screen) without re-renders.

## Usage

**Breakpoint variants:** `sm:`, `md:`, `lg:`, `xl:`, `2xl:` work on native using window-width–based media queries:

```tsx
<Text className="text-sm md:text-base lg:text-lg">Responsive text</Text>
```

**Media features supported on native:**

| Media feature | Example | Notes |
|---------------|---------|--------|
| `width` | `@media (width: 500px)` | Exact and range |
| `min-width` / `max-width` | `@media (min-width: 768px)` | |
| `prefers-color-scheme` | `@media (prefers-color-scheme: dark)` | Uses RN Appearance API |
| `resolution` | `@media (resolution: 2dppx)` | dppx, dpi |
| `min-resolution` / `max-resolution` | | |

**Platform media (NativeWind-specific):**

```css
@media ios { /* iOS only */ }
@media android { /* Android only */ }
@media native { /* All native */ }
```

Same as class variants: `ios:`, `android:`, `native:`, `web:`, `tv:`.

```tsx
<Text className="font-sans ios:font-[System] android:font-[Roboto]">
  Platform-specific font
</Text>
```

## Key Points

- Media queries on native are reactive; when window dimensions change, styles update automatically.
- Use platform variants when a utility is web-only (e.g. `grid`) so native gets a valid fallback (e.g. `flex`).

<!--
Source references:
- https://github.com/nativewind/website (sources/nativewind/content/v5/core-concepts/responsive-design.mdx)
-->
