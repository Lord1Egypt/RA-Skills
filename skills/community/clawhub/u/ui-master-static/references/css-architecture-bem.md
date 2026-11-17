# CSS Architecture: Tokens + BEM

No build-time config, no framework — the architecture has to be enforced by convention. This is the convention. Sources: BEM official methodology (getbem.com), MDN CSS Custom Properties, MDN `@property`.

## Design tokens as custom properties

Every reusable value — color, spacing, radius, shadow, type size, transition timing — is declared once in `:root` and referenced everywhere by `var()`. Never write a literal color or pixel value inside a component rule unless it is genuinely one-off and unrelated to the system (rare).

```css
:root {
  /* Color — name by role, not hue, same principle as any design system */
  --color-bg: #ffffff;
  --color-fg: #111114;
  --color-surface: #f7f7f8;
  --color-primary: #3a5fff;
  --color-primary-hover: #2c49d6;
  --color-muted: #6b6b76;
  --color-border: #e4e4e8;
  --color-danger: #e5484d;

  /* Spacing — 4px base unit, consistent scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;

  /* Radius */
  --radius-sm: 0.375rem;
  --radius-md: 0.625rem;
  --radius-lg: 1rem;
  --radius-full: 9999px;

  /* Shadow / elevation */
  --shadow-xs: 0 1px 2px rgb(0 0 0 / 0.05);
  --shadow-sm: 0 2px 8px rgb(0 0 0 / 0.08);
  --shadow-md: 0 4px 16px rgb(0 0 0 / 0.10);
  --shadow-lg: 0 8px 30px rgb(0 0 0 / 0.14);

  /* Type */
  --font-display: "Cal Sans", "Inter", sans-serif;
  --font-body: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-5xl: 3rem;

  /* Motion */
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --duration-fast: 150ms;
  --duration-base: 250ms;
  --duration-slow: 400ms;
}
```

## Runtime theme switching (light/dark) without a build step

Same principle as Tailwind v4's two-stage `@theme inline` pattern (see the `ui-master` skill), expressed in plain CSS: define raw values once per theme, reference them everywhere through a stable variable name.

```css
:root {
  color-scheme: light;
  --color-bg: #ffffff;
  --color-fg: #111114;
  --color-surface: #f7f7f8;
}

[data-theme="dark"] {
  color-scheme: dark;
  --color-bg: #121214;
  --color-fg: #f2f2f5;
  --color-surface: #1c1c20;
}
```

```js
// toggle: document.documentElement.dataset.theme = "dark" | "light"
const stored = localStorage.getItem("theme");
if (stored) document.documentElement.dataset.theme = stored;
```

Because components always reference `var(--color-bg)` rather than a hardcoded value, flipping `data-theme` on `<html>` re-themes the whole page with zero per-component changes.

## `@property` — typed, animatable custom properties

Plain custom properties are untyped strings — the browser can't interpolate between two color strings or two angle values smoothly. `@property` (excellent, near-universal support) registers a custom property with a real syntax, default, and inheritance behavior, which makes it animatable:

```css
@property --gradient-angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

.hero {
  background: conic-gradient(from var(--gradient-angle), #3a5fff, #7c3aed, #3a5fff);
  animation: rotate-gradient 8s linear infinite;
}

@keyframes rotate-gradient {
  to { --gradient-angle: 360deg; }
}
```

Without `@property`, animating a custom property used inside `conic-gradient()` simply doesn't interpolate — this is the mechanism that makes effects like animated gradient borders and rotating conic gradients possible in pure CSS.

## BEM naming

**B**lock, **E**lement, **M**odifier. One rule: a selector is exactly one class, never a combination of the block class plus a bare tag or a second unscoped class. This keeps every rule at the same specificity (0,1,0) — no cascade fights, no `!important` needed to override a more specific ancestor selector.

```
.card { }                 /* Block: a standalone, reusable component */
.card__title { }          /* Element: a part of the block, only meaningful inside it */
.card__body { }
.card--highlighted { }     /* Modifier: a variant/state of the block */
.card__title--large { }    /* Modifier on an element */
```

```html
<div class="card card--highlighted">
  <h3 class="card__title card__title--large">Title</h3>
  <div class="card__body">...</div>
</div>
```

### Rules that keep BEM from degrading

- **Never nest BEM selectors to reach descendants** (`.card .card__title` defeats the purpose — just use `.card__title` directly, it's already scoped by name).
- **Elements don't have their own elements.** `.card__title__icon` is wrong — flatten to `.card__icon` or make icon its own block if it's genuinely reusable outside `.card`.
- **Modifiers never appear alone** — always paired with the base block/element class in markup (`class="card card--highlighted"`, not `class="card--highlighted"` by itself), since the modifier class typically only sets the properties that *change*, inheriting the rest from the base class.
- **One modifier = one concern.** Prefer `.button--primary` and `.button--large` as two separate modifiers over a single `.button--primary-large`, so they combine freely.

## File organization (no build step required, but works with one)

```
styles/
  tokens.css          /* :root custom properties — colors, spacing, type, shadow */
  reset.css           /* modern CSS reset (box-sizing, margin removal, etc.) */
  base.css            /* element defaults: body, headings, links, focus-visible */
  layout/
    header.css
    dashboard-shell.css
    footer.css
  components/
    button.css
    card.css
    form.css
  utilities.css        /* small single-purpose helpers: .sr-only, .truncate */
  main.css              /* imports everything, in this exact order */
```

```css
/* main.css — order matters: tokens before anything that uses them,
   base before components so components can override element defaults */
@import "./tokens.css";
@import "./reset.css";
@import "./base.css";
@import "./layout/header.css";
@import "./layout/dashboard-shell.css";
@import "./layout/footer.css";
@import "./components/button.css";
@import "./components/card.css";
@import "./components/form.css";
@import "./utilities.css";
```

In a Vite project, native `@import` at the top of `main.css` is bundled and inlined at build time (no runtime waterfall) — this works out of the box with zero configuration.

## A minimal modern reset

```css
*, *::before, *::after { box-sizing: border-box; }
* { margin: 0; }
body { line-height: 1.5; -webkit-font-smoothing: antialiased; }
img, picture, video, canvas, svg { display: block; max-width: 100%; }
input, button, textarea, select { font: inherit; }
p, h1, h2, h3, h4, h5, h6 { overflow-wrap: break-word; }
#root, #__next { isolation: isolate; }
```

## Checklist before moving to components

- [ ] Every color, spacing, radius, shadow, and type value used has a corresponding token — none are literal in component files
- [ ] File structure separates tokens / base / layout / components, imported in that order
- [ ] Every new component follows `block__element--modifier`, no nested block selectors
- [ ] Dark mode (if needed) uses the `[data-theme]` + variable-reference pattern, not a duplicated stylesheet
