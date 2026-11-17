# Tailwind CSS v4 Setup

Tailwind v4 is a ground-up rewrite: the Rust-based Oxide/Lightning CSS engine replaces the old PostCSS pipeline, `tailwind.config.js` is gone, and configuration lives in CSS via the `@theme` directive with automatic content detection (no `content` array to maintain). If you see a `tailwind.config.js` in a project, confirm whether it's a v3 project before applying anything below.

Sources: official Tailwind CSS v4 docs (tailwindcss.com/docs), Tailwind v4 release notes.

## Install — Next.js (App Router)

```bash
npx create-next-app@latest my-app --typescript --tailwind
# or, adding to an existing Next.js app:
npm install tailwindcss @tailwindcss/postcss postcss
```

`postcss.config.mjs`:

```js
export default {
  plugins: {
    "@tailwindcss/postcss": {},
  },
};
```

`app/globals.css`:

```css
@import "tailwindcss";
```

That's the entire config file requirement. Import `app/globals.css` once, in the root layout.

## Install — Vite (React, React Router, TanStack Start)

```bash
npm create vite@latest my-app -- --template react-ts
cd my-app
npm install tailwindcss @tailwindcss/vite
```

`vite.config.ts`:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

`src/index.css`:

```css
@import "tailwindcss";
```

Import `src/index.css` in `src/main.tsx`. No PostCSS config needed — the Vite plugin handles it directly and gives the fastest HMR.

## CSS-first configuration with `@theme`

All design tokens live in the CSS entrypoint. Every token you declare auto-generates the matching utilities:

```css
@import "tailwindcss";

@theme {
  --font-sans: "Inter", sans-serif;
  --font-display: "Geist", sans-serif;

  --color-primary: oklch(55% 0.22 265);
  --color-primary-foreground: oklch(98% 0 0);

  --radius-card: 1rem;
  --shadow-elevated: 0 8px 30px oklch(0% 0 0 / 0.12);
}
```

`--color-primary` generates `bg-primary`, `text-primary`, `border-primary`, `ring-primary`, etc. automatically. `--font-display` generates `font-display`. This is the mechanism — see `design-tokens.md` for what values to actually put in there.

## The dark-mode trap (read this before building components)

`@theme` values are compiled into the generated utility CSS at build time. If you put a *resolved* color directly in `@theme` and try to swap it at runtime via a `.dark` class, the utility class itself doesn't change — only works for build-time theme variants, not runtime toggling.

**Correct two-stage pattern** for a runtime-switchable theme (light/dark toggle):

```css
@import "tailwindcss";

:root {
  --background: oklch(100% 0 0);
  --foreground: oklch(15% 0 0);
  --primary: oklch(55% 0.22 265);
}

.dark {
  --background: oklch(12% 0 0);
  --foreground: oklch(96% 0 0);
  --primary: oklch(70% 0.18 265);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
}
```

`@theme inline` maps the utility to the CSS variable rather than baking in a value, so flipping the `.dark` class on `<html>` at runtime actually changes what `bg-background` resolves to. This is also exactly the pattern shadcn/ui's default theme CSS uses, which is why the two integrate cleanly — see `shadcn-setup.md`.

## Migrating an existing v3 project

1. Run the official upgrade tool: `npx @tailwindcss/upgrade`
2. It converts `tailwind.config.js` values into `@theme` CSS, updates imports, and flags renamed utilities.
3. Manually review: some v3 utility names changed (check the migration guide's rename table for anything project-specific, e.g. shadow scale renames), and any `@apply`-heavy custom CSS should be spot-checked since cascade layering changed.
4. Confirm `content` config isn't still being referenced anywhere — v4 auto-detects template files and the array is ignored/unnecessary.

## New capabilities worth using deliberately

- **Container queries** are built in, no plugin: `@container` on a parent, `@sm:`, `@lg:` variants on children — use for components that need to respond to their container's width, not the viewport's (card grids, sidebar-adjacent panels).
- **`@utility` directive** for custom utility classes that behave like first-class Tailwind utilities (participate in variants, ordering) instead of a raw CSS class.
- **Native cascade layers** (`@layer theme, base, components, utilities`) — if hand-written CSS needs to interoperate with Tailwind's specificity, put it in the right layer rather than fighting specificity with `!important`.

## Supported browsers

Tailwind v4 relies on modern CSS features (native cascade layers, `color-mix()`, registered custom properties). If the project must support Safari < 16.4 or Chrome < 111, either stay on v3 or verify each v4 feature you rely on against caniuse before shipping.
