# Slidev Styling

UnoCSS utilities, custom styles, dark mode, and build configuration.

## UnoCSS Integration

Slidev ships with UnoCSS using Tailwind-compatible utility classes. Use them directly in Markdown/HTML:
```html
<div class="grid grid-cols-2 gap-4">
  <div class="bg-blue-500 p-4 rounded">Column 1</div>
  <div class="bg-red-500 p-4 rounded">Column 2</div>
</div>
```

Common utilities: spacing (`p-4`, `m-2`, `gap-4`), fl/grid (`flex`, `grid`, `grid-cols-2`), color (`text-blue-500`, `bg-gray-100`), sizing (`w-full`, `h-40`, `max-w-md`), typography (`text-2xl`, `font-bold`).

## Custom Global Styles

Create `styles/index.css` for project-wide styles. `@apply` works with UnoCSS:
```css
/* styles/index.css */
.my-custom-class {
  @apply text-2xl font-bold text-blue-500;
}
```

## Slide-Scoped Styles

Add a `<style>` block inside a slide to style only that slide:
```md
# Slide Title

Content here

<style>
h1 {
  color: #3b82f6;
}
</style>
```

Use `<style scoped>` to limit styles strictly to the current slide's elements.

## Dark Mode

UnoCSS `dark:` variants adapt to the active theme:
```html
<div class="bg-white dark:bg-black text-black dark:text-white">
  Adapts to light/dark theme
</div>
```

To render entirely different content per theme, use the `<LightOrDark>` component (see `components.md`).

## UnoCSS Configuration

Create `uno.config.ts` to define shortcuts, theme tokens, and rules:
```ts
import { defineConfig } from 'unocss'

export default defineConfig({
  shortcuts: {
    'bg-main': 'bg-white text-[#181818] dark:(bg-[#121212] text-[#ddd])',
  },
})
```

Override theme CSS variables in `styles/index.css` without ejecting:
```css
:root {
  --slidev-theme-primary: #3b82f6;
}
```

## Vite Configuration

Extend the underlying Vite config in `vite.config.ts`:
```ts
import { defineConfig } from 'vite'

export default defineConfig({
  // your custom Vite plugins / options
})
```

## Fonts

Configure web fonts in headmatter (auto-loaded from Google Fonts):
```yaml
---
fonts:
  sans: Roboto
  serif: Merriweather
  mono: Fira Code
---
```

See `assets.md` for font weights, local fonts, and providers.
