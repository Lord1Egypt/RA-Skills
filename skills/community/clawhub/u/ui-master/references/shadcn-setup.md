# shadcn/ui Setup and Theming

shadcn/ui is not a package you `npm install` and import from `node_modules`. The CLI copies component source (built on Radix primitives, styled with Tailwind) directly into the project under `components/ui`. This means every component is fully owned and editable — that ownership is the point, and it's why this skill treats shadcn components as a starting composition, not a black box.

Source: official shadcn/ui docs (ui.shadcn.com/docs).

## Check before installing

Look for `components.json` at the project root. If it exists, shadcn/ui is already initialized — **do not re-run `init`**, it will prompt to overwrite the theme CSS and config. Instead, jump straight to adding components.

## Install — Next.js (App Router)

Requires Tailwind already set up (see `tailwind-v4-setup.md`).

```bash
npx shadcn@latest init
```

The CLI will ask for:
- Base color (`neutral`, `zinc`, `slate`, etc. — the default palette shadcn's own tokens are built from before you override with `design-tokens.md`)
- Whether to use CSS variables for theming — **always yes**, this is what makes the two-stage dark-mode pattern work

This generates/updates `components.json` and writes the base theme into your CSS entrypoint (`app/globals.css`).

```bash
npx shadcn@latest add button card dialog form input
```

Import components directly:

```tsx
import { Button } from "@/components/ui/button";
```

## Install — Vite / React Router / TanStack Start

Same CLI, framework-specific template flag:

```bash
npx shadcn@latest init -t vite
```

Prerequisites the CLI checks for: a working `@/*` import alias in **both** `tsconfig.json` and `tsconfig.app.json` (Vite splits these — both need the `paths` entry), and Tailwind already importing correctly in the CSS entrypoint.

`vite.config.ts` needs the alias resolved outside TypeScript too:

```ts
import path from "path";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: { "@": path.resolve(__dirname, "./src") },
  },
});
```

## `components.json` reference

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

- `style`: `new-york` (denser, more opinionated) vs the classic default — pick once, don't mix mid-project since spacing/radius conventions differ between styles.
- `rsc: true` only for Next.js App Router (React Server Components); `false` for Vite/client-only apps.
- `cssVariables: true` is what enables theming through CSS custom properties instead of hard-coded Tailwind color classes baked into each component file — required for the dark-mode pattern in `tailwind-v4-setup.md`.

## Theming to match your design tokens

After `init`, the generated CSS block in your entrypoint looks like the two-stage pattern from `tailwind-v4-setup.md`:

```css
:root {
  --background: oklch(100% 0 0);
  --foreground: oklch(15% 0 0);
  --primary: oklch(21% 0.006 285);
  --primary-foreground: oklch(98% 0 0);
  --muted: oklch(97% 0 0);
  --muted-foreground: oklch(55% 0.01 285);
  --destructive: oklch(58% 0.24 27);
  --radius: 0.625rem;
  /* ...border, input, ring, card, popover, chart-*, sidebar-* */
}

.dark {
  /* dark equivalents */
}

@theme inline {
  --color-background: var(--background);
  --color-primary: var(--primary);
  /* ... */
}
```

**Do not hand-edit individual component files to change colors.** Replace the values in `:root` / `.dark` with the palette from `design-tokens.md` instead — every shadcn component already references these variable names (`bg-primary`, `text-muted-foreground`, `border-input`), so a token change propagates everywhere automatically. This is the entire value proposition of the CSS-variable theming mode.

## Adding and updating components

```bash
npx shadcn@latest add table data-table sheet command sidebar
npx shadcn@latest add button --overwrite   # re-pull latest source for one component
```

Common production components by use case:
- **Forms**: `form` (React Hook Form + Zod wrapper), `input`, `select`, `checkbox`, `radio-group`, `textarea`
- **Data display**: `table`, `data-table` (TanStack Table wrapper), `badge`, `avatar`, `card`
- **Navigation**: `sidebar`, `navigation-menu`, `breadcrumb`, `tabs`
- **Overlays**: `dialog`, `sheet`, `dropdown-menu`, `popover`, `tooltip`, `command` (command palette)
- **Feedback**: `sonner` (toast), `alert`, `skeleton` (loading state), `progress`

## Before hand-rolling anything

Check `components/ui/` for an existing primitive before building a modal, dropdown, or form field from scratch. shadcn/ui's Radix-based primitives already handle focus trapping, ARIA roles, and keyboard interaction correctly — reimplementing them from raw `<div>`s is both wasted effort and a common source of accessibility regressions.
