# Theming — Tokens, Scales, And Custom Values

The config is a token system that happens to generate classes. Get the namespace right and the utilities appear for free; get it wrong and nothing happens with no error.

- [Namespaces Generate Utilities (v4)](#namespaces-generate-utilities-v4) — which prefix produces which classes
- [v3 Equivalent](#v3-equivalent) — `extend` vs replacing a whole scale
- [Multi-Brand And Runtime Theme Switching](#multi-brand-and-runtime-theme-switching) — `@theme inline` and the indirection
- [Spacing And Scale Decisions](#spacing-and-scale-decisions)
- [Fonts](#fonts) — fallbacks and framework font loaders
- [Reading Tokens At Runtime](#reading-tokens-at-runtime) — JS and canvas
- [Dead Ends Worth Naming](#dead-ends-worth-naming)

## Namespaces Generate Utilities (v4)

A variable only creates classes when it lives in `@theme` **and** uses a known namespace prefix.

| Namespace | Example | Utilities produced |
|---|---|---|
| `--color-*` | `--color-brand-500` | `bg-brand-500`, `text-brand-500`, `border-brand-500`, `ring-brand-500`, `fill-…`, `divide-…` |
| `--font-*` | `--font-display` | `font-display` |
| `--text-*` | `--text-hero` | `text-hero` (pair with `--text-hero--line-height`) |
| `--spacing` | `--spacing: 0.25rem` | The base for every `p-*`, `m-*`, `gap-*`, `w-*`, `size-*` step |
| `--breakpoint-*` | `--breakpoint-3xl: 120rem` | `3xl:` and `max-3xl:` variants |
| `--container-*` | `--container-prose: 65ch` | `max-w-prose`, `@prose:` container query variant |
| `--radius-*` | `--radius-card: 0.75rem` | `rounded-card` |
| `--shadow-*`, `--inset-shadow-*` | `--shadow-panel` | `shadow-panel` |
| `--animate-*` | `--animate-slide` | `animate-slide` (the matching `@keyframes` must ship too) |
| `--ease-*` | `--ease-snap` | `ease-snap` |
| `--tracking-*`, `--leading-*` | `--tracking-tight` | `tracking-tight`, `leading-*` |

```css
@theme {
  --color-brand-500: oklch(0.62 0.19 259);
  --font-display: "Satoshi", ui-sans-serif, system-ui;
  --radius-card: 0.75rem;
  --breakpoint-3xl: 120rem;
}
```

- A variable declared in `:root` instead of `@theme` sets a value and generates **nothing**. First thing to check when a token produces no utility.
- Wrong namespace, same outcome: `--brand: red` produces no utility; `--color-brand: red` produces the full family.
- Clear a default scale before replacing it: `--color-*: initial;` inside `@theme` wipes the built-in palette, then define only yours. Without it you ship both.
- `@theme inline { --color-surface: var(--surface); }` makes utilities emit `var(--surface)` rather than the resolved value — the mechanism behind runtime theme switching below.

## v3 Equivalent

```js
theme: {
  extend: {
    colors: { brand: { 500: '#1d4ed8' } },
    fontFamily: { display: ['Satoshi', 'sans-serif'] },
    borderRadius: { card: '0.75rem' },
    screens: { '3xl': '120rem' },
  },
}
```

`extend` adds; a top-level key **replaces the entire scale**. `colors: { brand: … }` at the top level deletes every default color in the project — the change compiles, and half the app goes unstyled.

## Multi-Brand And Runtime Theme Switching

Utilities must point at an indirection, or swapping does nothing at runtime.

```css
@theme inline {
  --color-surface: var(--surface);
  --color-ink: var(--ink);
}

:root            { --surface: oklch(1 0 0);    --ink: oklch(0.2 0 0); }
[data-brand=acme]{ --surface: oklch(0.98 0.01 250); --ink: oklch(0.25 0.05 250); }
```

Now `bg-surface` resolves through `var(--surface)`, and setting `data-brand` on any ancestor re-themes the subtree — no rebuild, no duplicate utility set.

v3 equivalent, with the alpha placeholder so opacity modifiers keep working:

```js
colors: { surface: 'rgb(var(--surface) / <alpha-value>)' }   // --surface: 255 255 255
```

Omit `<alpha-value>` and `bg-surface/50` silently produces an invalid color.

## Spacing And Scale Decisions

- v4 derives every step from `--spacing` (default `0.25rem`), so any multiple works: `p-13` = 3.25rem, `mt-17` = 4.25rem. Changing `--spacing` rescales the entire app in one line — powerful and irreversible-feeling; do it before, not after, a design is built.
- v3 ships a fixed step list; anything off-scale needs a config entry or arbitrary syntax.
- Full numeric reference: SKILL.md — Utility Scale Math.
- Resist per-component scale entries. A token named `--spacing-card-gap` that appears once is a variable pretending to be a design decision; use the numeric step and move on (SKILL.md rule 2).

## Fonts

- `--font-display: "Satoshi", ui-sans-serif, system-ui` — always keep a fallback stack in the token; a missing webfont with no fallback renders the browser default and looks like a build failure.
- Framework font loaders (`next/font`, `@fontsource`) expose a CSS variable; feed that variable into the token rather than naming the family twice: `--font-display: var(--font-satoshi)`.
- Variable-font axes and optical sizing belong in a base layer (`font-variation-settings`), not in a token — utilities can't reach axis values.

## Reading Tokens At Runtime

v4 exposes theme values as CSS custom properties, so JS and canvas code can read them:

```js
getComputedStyle(document.documentElement).getPropertyValue('--color-brand-500')
```

If a token is only consumed this way and no class references it, use `@theme static { … }` so it is emitted regardless of usage. v3 has no equivalent — expose the value manually in a base layer.

## Dead Ends Worth Naming

| Attempt | Result |
|---|---|
| `--color-brand: red` in `:root` | No utilities; the variable exists and does nothing |
| Two `@theme` blocks defining the same token | The last one wins silently across the whole app |
| Theme token holding a full shorthand (`--shadow-x: 0 1px 2px rgb(0 0 0 / .1), inset …`) | Fine for `--shadow-*`; other namespaces expect a single value and produce broken CSS |
| Defining `--breakpoint-xs: 30rem` expecting it to sort first | Breakpoints sort by value in v4, so it does — but in v3 `screens` order is declaration order, and an out-of-order entry breaks the mobile-first cascade |
| Naming a color token by usage (`--color-danger`) *and* by hue (`--color-red-500`) for the same value | Two names for one token; the rebrand updates one of them |

