# PMA-Web Routing And UI

## Table of Contents

- [Routing](#routing)
- [Provider Composition](#provider-composition)
- [Entry Point](#entry-point)
- [shadcn/ui](#shadcnui)
- [Tailwind CSS v4](#tailwind-css-v4)
- [Theming](#theming)
- [Fonts And Visual Tokens](#fonts-and-visual-tokens)


## Routing

- Use TanStack Router file-based routing under `src/app/routes/`.
- Keep `routeTree.gen.ts` generated and excluded from manual lint noise.
- Prefer route-level layouts via `__root.tsx` and nested route folders.
- Keep feature logic in `src/features/`; routes should compose features instead of absorbing all business logic.

## Provider Composition

Provider order:

```text
I18nextProvider (optional)
QueryClientProvider
ThemeProvider
RouterProvider
```

`RouterProvider` is rendered in `main.tsx`, outside the provider factory when that keeps startup clearer.

## Entry Point

Baseline shape:

```typescript
import { createRouter, RouterProvider } from "@tanstack/react-router";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { Providers } from "./app/providers";
import { routeTree } from "./app/routeTree.gen";
import "./index.css";

const router = createRouter({ routeTree });
```

Requirements:

- fail fast when `#root` is missing
- register router types for TanStack Router
- keep global CSS imports at the entry boundary

## shadcn/ui

Use shadcn as owned code, not copy-pasted snippets. shadcn/ui + `@base-ui/react` is the **only** allowed UI ecosystem in PMA-Web — no Radix, no MUI/Mantine/Chakra/AntD/Headless UI/Ariakit/NextUI/Park UI/etc. See *UI Library Policy* in `baseline.md` for the full constraint and rationale.

### Required init choices

- component library: `base-ui` (do **not** pick the Radix-based option)
- style: `base-nova`
- base color: `neutral`
- CSS variables: `yes`
- aliases aligned to the actual folder layout

### Component sourcing order

Walk the list in order; stop at the first match. Do **not** skip ahead to hand-writing.

1. existing project primitive under `src/shared/components/ui/` — reuse or extend it
2. shadcn/ui registry — `bunx shadcn@latest add <name>`
3. `@base-ui/react` primitive wrapped to match shadcn's API conventions and Tailwind classes, placed in `src/shared/components/ui/`
4. hand-written from scratch — only after steps 1–3 cannot satisfy the need, and only after the proposal explicitly justifies it

A PR that hand-writes a primitive with a shadcn or Base UI equivalent is a review blocker.

### Rules

- generate shared primitives into `src/shared/components/ui/`; keep business components (forms, page composites) inside features
- add new primitives through the shadcn CLI rather than copy-pasting from the docs, so `components.json` and aliases stay consistent
- treat generated files as owned code — commit, edit, and refactor them freely
- keep `components.json` consistent with repository aliases and Tailwind paths
- if a feature truly needs something neither shadcn nor Base UI ships (virtualized grid, charts, …), bring in a **headless** non-component lib (`@tanstack/react-table`, `@tanstack/react-virtual`, `recharts`, …) and render it through shadcn-styled wrappers; introduce it via the proposal

## Tailwind CSS v4

Tailwind v4 has no JS config; the theme lives entirely in CSS. Standard imports for a shadcn project (matches the official theming scaffold at <https://ui.shadcn.com/docs/theming>):

```css
@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn/tailwind.css";
```

`shadcn/tailwind.css` is the helper layer shadcn injects when initializing a Tailwind v4 project — keep it. The customisation you do happens in the `:root` / `.dark` / `@theme inline` blocks below it, not in that import.

### Color Token Layering

Colors live in **three places**, each with a distinct role. Do not collapse them.

#### 1. `src/index.css` — the single source of truth

This file owns every color token. It has three layered blocks:

```css
@import "tailwindcss";
@import "tw-animate-css";
@import "shadcn/tailwind.css";

@custom-variant dark (&:is(.dark *));

/* (a) Light-mode CSS variables */
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --border: oklch(0.922 0 0);
  --radius: 0.625rem;
  /* …rest of the shadcn token set… */
}

/* (b) Dark-mode overrides (same names, different values) */
.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --border: oklch(1 0 0 / 10%);
  /* …matching dark values… */
}

/* (c) Map CSS variables into Tailwind theme tokens */
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-border: var(--border);
  --radius-lg: var(--radius);
  --radius-md: calc(var(--radius) - 2px);
  --radius-sm: calc(var(--radius) - 4px);
}
```

Roles:

- **(a) `:root`** — light-theme palette in oklch.
- **(b) `.dark`** — dark-theme overrides for the *same* variable names. The `@custom-variant dark (&:is(.dark *))` line is what makes Tailwind's `dark:` variant follow the `.dark` class set by `ThemeProvider`.
- **(c) `@theme inline`** — turns the raw CSS variables into Tailwind theme tokens, which is what makes utilities like `bg-background`, `text-primary`, `border-border`, `rounded-lg` work. Without this block, the variables exist but Tailwind cannot see them.

When customising the palette, edit blocks (a) and (b) only. Block (c) stays as a stable mapping.

#### 2. `components.json` — initial-value selector, not a runtime config

`components.json` carries `tailwind.baseColor` (`neutral`, `slate`, `stone`, `gray`, `zinc`). It tells the shadcn CLI which preset to write into `index.css` on `init` / `add`. After init it has **no runtime effect**: changing the value here will not recolor the app, only change what future `shadcn add` commands generate. Keep it in sync with reality but treat `index.css` as authoritative.

#### 3. shadcn primitives — consume tokens, never literal colors

Files generated under `src/shared/components/ui/` must reference utilities (`bg-background`, `text-muted-foreground`, `border-border`, …). They must not contain hex codes, oklch literals, or hard-coded Tailwind palette colors (`bg-zinc-900`). Same rule applies to feature components.

### Rules

- Edit color values in `index.css` only; do not scatter overrides across feature CSS.
- Add a new semantic token by extending all three blocks: declare in `:root`, override in `.dark`, expose in `@theme inline`.
- Prefer oklch for all color values to stay consistent with the shadcn baseline and to get sane perceptual interpolation.
- Keep hardcoded colors out of deep feature components — if a one-off color is unavoidable, lift it into `index.css` as a token first.

## Theming

- ThemeProvider is the single source of truth.
- Support `light`, `dark`, and `system` when the product needs them.
- Persist the selected theme in `localStorage`.
- Do not duplicate theme state in Zustand.
- Prefer a `ModeToggle` that cycles predictably through available modes.

## Fonts And Visual Tokens

- Prefer self-hosted variable fonts when typography matters.
- Keep font and radius tokens in CSS variables.
- Centralize product tokens in `index.css` or a dedicated theme file rather than spreading them across feature components.
