---
name: skill-tailwind
description: >-
  Write, configure, migrate, and review modern Tailwind CSS v4 (CSS-first) in any stack or none —
  framework-agnostic, examples are plain HTML + CSS/SCSS. Use whenever setting up Tailwind, doing a
  v3->v4 migration (@tailwind->@import, JS config->@theme), defining a reusable design-token / color
  system + dark mode via @theme, choosing between the two organizing approaches — (A) utility-first
  classes in markup and (B) BEM + @apply in SCSS grouped by property type — wiring responsive @variant
  and states, debugging @apply / @reference in component styles, or reviewing Tailwind code. Not for:
  choosing brand color VALUES or palettes, JS theme libs, cn()/clsx/tailwind-merge glue, vanilla-JS
  component behavior, non-Tailwind CSS frameworks, general CSS Q&A, or build/CI and generic postcss tooling.
metadata:
  tags: tailwind, css, scss, v4, design-tokens, bem, utility-first
---

# skill-tailwind

Implementation layer for **Tailwind CSS v4 (CSS-first)**: how to correctly express a style with the
means of v4, framework-agnostically (plain HTML + CSS/SCSS). Teaches **two equal** approaches to
organizing styles — utility-first and BEM+`@apply` — and a deliberate choice between them.

> The skill is responsible for **Tailwind's technical correctness**, not for visual direction. If the
> project has a design system / `DESIGN.md` / ready-made tokens — we do **not** redefine them, we
> **map** them into `@theme`. All token values in the examples are **placeholders to be replaced**;
> only the **names** are stable.

## When to apply

Trigger: any request where Tailwind markup appears, CSS with `@import "tailwindcss"` / `@theme`
/ `@apply`, or a request to "make it look nice with Tailwind classes." Apply when you need to:

- write new markup/components in Tailwind (in any stack or none);
- configure v4: entry CSS, `@theme` tokens, custom utilities/variants, dark mode;
- migrate **v3 → v4** (`@tailwind` → `@import`, JS config → `@theme`, renamed utilities);
- set up/map **design tokens** via `@theme` (CSS variables);
- **choose an approach** for a component: utilities in markup vs BEM+`@apply` in SCSS;
- **review** Tailwind code (class detection, tokens vs arbitrary, states, anti-patterns).

## Scope and out-of-scope

**Does:** style implementation in Tailwind v4 — framework-agnostic (plain HTML + CSS/SCSS), both
approaches A/B, design tokens via `@theme`, states/accessibility, v3→v4 migration, review.

**Does not:**

- **Does not dictate visual design** (§3A): direction, palette, and typography are set by the
  project's design system; the skill **maps** it into `@theme`, it does not invent it. The skill is
  an implementation layer.
- **Does not cover JS-framework components** that need stateful JS: combobox/autocomplete,
  command palette (⌘K), a full-blown date-picker/calendar (native `<input type="date">` for the
  simple case — yes), a sortable/virtualized data table, a carousel with autoplay, charts,
  WYSIWYG, OTP input, resizable panels, tree view. Principle: **the native element if it exists;
  otherwise it is a JS layer** (for interactive primitives the skill shows a CSS-only basis and
  honestly marks where ~JS is needed — see `tabs`, `dropdown`, `toast`).

## Quick navigation (Quick reference)

Read as needed — progressive disclosure.

**References (`references/`)** — dense reference materials:

| Topic | File |
| --- | --- |
| v4 rules (Wrong→Correct→Why), the two "important"s | `references/v4-rules.md` |
| Subtle v4 gotchas (variant stack, `bg-(--var)`, `@reference`, `@source`, currentColor) | `references/gotchas.md` |
| Wiring Tailwind into a build (which plugin; the preprocessor-skips-`@apply` pitfall; per-unit `@reference`) | `references/build-integration.md` |
| Design tokens: semantic set, `.dark`, `@theme inline`, mapping a foreign system | `references/tokens.md` |
| Two approaches: abstraction ladder, "good/bad `@apply`", decision tree, grouping | `references/approaches.md` |
| Agnostic component patterns (inventory) | `references/components.md` |
| First-party plugins (`@tailwindcss/typography`, `@tailwindcss/forms`) | `references/plugins.md` |
| Editor/tooling setup (`prettier-plugin-tailwindcss`, IntelliSense) | `references/editor-setup.md` |
| Review checklist (12 items) | `references/review.md` |

**Concepts (`docs/`)** — in-depth explanations of "why it works this way":

| Topic | File |
| --- | --- |
| Getting started (the first 5 minutes: `@import` + `@theme` + first component) | `docs/getting-started.md` |
| CSS-first config (`@import`, `@theme`, `@config`) | `docs/css-first-config.md` |
| Design tokens (conceptually) | `docs/design-tokens.md` |
| Variants and states (hover/focus-visible/active/disabled, `not-*`, stack) | `docs/variants-and-states.md` |
| Accessibility (focus-visible, `sr-only`, `forced-colors:`, `user-invalid:`, contrast) | `docs/accessibility.md` |
| Responsive and container queries (`@container`, `@md:`) | `docs/responsive-and-container-queries.md` |
| Dark mode (class-based `@custom-variant`, `.dark` overrides) | `docs/dark-mode.md` |
| Custom utilities and layers (`@utility`, `@layer`, `@variant`) | `docs/custom-utilities-and-layers.md` |
| Performance and bundle (class detection, dynamic names, `@source`) | `docs/performance-and-bundle.md` |
| Visual effects v4.1 (`text-shadow-*`, `mask-*`, colored `drop-shadow`, shadow/inset-shadow/ring) | `docs/effects.md` |
| Animations and motion (built-in `animate-*`, custom `--animate-*`, `starting:`, reduced-motion) | `docs/animations-and-motion.md` |
| RTL and logical properties (`ps-`/`pe-`, `start-`/`end-`, `dir`, `rtl:`/`ltr:`) | `docs/rtl-and-logical-properties.md` |

**Examples (`examples/`)** — each component in both implementations (A utility-first + B BEM): `button`,
`card`, `input-field`, `badge`, `alert`, `navbar`, `modal`, `responsive-grid`, `accordion`,
`checkbox-radio-switch`, `select`, `textarea`, `tabs`, `tooltip`, `breadcrumb`, `pagination`, `table`,
`popover`, `dropdown`, `drawer`, `progress`, `spinner-skeleton`, `avatar`, `toast`, `list`, `media`.
Index — `examples/README.md`.

**Templates (`templates/`)** — `entry.css`, `theme.css`, `tailwind.config.js`, component skeletons:
`component.utility.html` (A) and `component.bem.html` + `component.bem.scss` (B).

**Cheat sheets (`resources/`)** — flat scannable tables/trees (not prose): `v3-to-v4-cheatsheet.md`,
`tokens-table.md`, `property-order.md`, `apply-grouping.md`, `gotchas-list.md`. Aggregators for a
quick glance: `decision-trees.md` (all of the skill's forks as one list of ASCII trees),
`anti-patterns.md` (a "before → after" gallery for each NEVER), `checklist.md` (master checklist "is my
v4 correct?" — the entry point, consolidating review/evals/component-invariant checks).

**Workflows (`workflows/`)** — step-by-step playbooks:

| Task | File |
| --- | --- |
| v3 → v4 migration (syntax: `@tailwind`→`@import`, JS config→`@theme`, renames) | `workflows/migrate-v3-to-v4.md` |
| Refactor-to-tokens (second pass: arbitrary/hex → semantic tokens, clearing the "utility soup") | `workflows/refactor-to-tokens.md` |
| Introducing design tokens "from scratch" | `workflows/introduce-design-tokens.md` |
| Tailwind review | `workflows/review-tailwind.md` |
| Choosing approach A vs B | `workflows/choose-approach.md` |
| Diagnosing "it compiled but doesn't work" (Symptom → Cause → Check → Fix) | `workflows/troubleshoot.md` |

**Scripts (`scripts/`)** — optional offline checks: `scripts/check-v3-antipatterns.mjs`,
`scripts/lint-dynamic-classes.mjs` (index — `scripts/README.md`).

**Evals (`evals/`)** — skill checks: `evals/cases.md`, `evals/fixtures/*`, a static harness with no
dependencies `evals/harness.mjs` (`node evals/harness.mjs <files>`) and an optional real-compilation
verifier `evals/compile-check.mjs` (Tailwind v4 + Sass) — index `evals/README.md`.

## Core: the v4 stance

- Inclusion — `@import "tailwindcss"` (expands into the layers theme→base→utilities). `@tailwind
  base/components/utilities` — dead.
- Config — **CSS-first** via `@theme` (CSS variables). JS config only for dynamics, via
  `@config "..."`. Custom utilities — `@utility name { ... }`; custom variants — `@custom-variant`.
- Colors — **oklch**; spacing — a single `--spacing` (values are computed, not a static scale).
- Slash opacity `bg-primary/90` (not `bg-opacity-*`); gradients `bg-linear-to-r` (not
  `bg-gradient-to-r`); renames: `shadow-sm`→`shadow-xs`, `rounded-sm`→`rounded-xs`, etc.
- Container queries (`@container` + `@md:`), enter animations `starting:`, the negator `not-*`.
- Class detection is **literal**: concatenating names (`text-${c}-500`) is not found → safelist `@source
  inline(...)`. `border`/`ring` default to `currentColor`. The variant stack reads left-to-right.
- The two "important"s are **different** things: the global `@import "tailwindcss" important;` ≠ the
  suffix on a class `bg-danger!`. CSS variables in arbitrary values — `bg-(--brand)` (not `bg-[--brand]`).

## Abstraction ladder

Six rungs — from low abstraction to high. Climb **only when necessary**, but BEM+
`@apply` (rungs 4–6) is a **deliberate choice**, not a "failure of the utility-first approach."

1. **Utilities in markup** — the starting point for everything. Co-location, minimal bundle.
2. **Extract repeated markup** into a reusable block/partial/fragment (rather than hiding it in CSS).
3. **`@theme` tokens** — a repeated value (color/radius/spacing) becomes a named token.
4. **Custom `@utility`** — a repeated low-level property pattern that Tailwind lacks.
5. **Component class in `@layer components`** — a semantic class for a component.
6. **`@apply` as a narrow adapter** — inlining utilities into a component class / into foreign generated markup.

> Approach B = a conscious stop at rungs 4–6 for the sake of readability and reuse. Approach A = a
> stop at rungs 1–3 for the sake of co-location and a thin bundle. **The benefit of both is equal.** Details and
> the "good/bad `@apply`" rule — `references/approaches.md`.

## Decision trees

### 1. Utility-first (A) vs BEM+`@apply` (B) for this component

```
Markup repeats and is NOT extractable into a partial/fragment (generated by a CMS, third-party DOM)?
├── Yes → B (BEM+@apply): give the style a name without touching the markup.
└── No → Is one of the approaches already adopted in the repository?
    ├── Yes → follow the adopted one (consistency beats taste).
    └── No → Is the component one-off / simple / is the markup easy to extract?
        ├── Yes → A (utilities in markup).
        └── No → Many states/variants, "readability at a glance" matters?
            ├── Yes → B (BEM+@apply, grouped).
            └── No → A.
```

### 2. Where the color / token should live

```
Is this a one-off value, occurring exactly once and carrying no meaning?
├── Yes → arbitrary, sparingly: bg-[oklch(...)] or bg-(--brand) for a ready-made variable.
└── No → Does it have semantics (primary, muted, danger, border...)?
    ├── Yes → a semantic token in @theme (--color-primary, ...). This is the norm.
    └── No → Does the value come from an external design system / DESIGN.md?
        ├── Yes → MAP it into @theme (do not redefine) and use it by name.
        └── No → promote it on the very first repeat: arbitrary-first → token on repeat/meaning.
```

> These two trees are canonical here (on divergence, SKILL.md wins). All of the skill's forks as one
> scannable list, plus two more trees — #3 "arbitrary vs token (promotion)" and #4 "which
> component / native element vs JS" — `resources/decision-trees.md`.

## v4 vs v3 (summary)

The full list with rationale — `references/v4-rules.md`.

| Topic | v3 (before / anti-pattern) | v4 (correct) |
| --- | --- | --- |
| Inclusion | `@tailwind base/components/utilities;` | `@import "tailwindcss";` |
| Config | `tailwind.config.js` → `theme.extend` | `@theme { --color-...: ...; }` (CSS-first) |
| Custom utility | `@layer utilities { .x {...} }` | `@utility x { ... }` |
| Opacity | `bg-red-500 bg-opacity-50` | `bg-red-500/50` |
| Gradient | `bg-gradient-to-r` | `bg-linear-to-r` |
| Shadows/radii | `shadow-sm`, `rounded-sm` (old meaning) | `shadow-xs`, `rounded-xs` (shift by one size) |
| Important | `important: true` in config | `@import "tailwindcss" important;` **or** `bg-danger!` |
| CSS var in arbitrary | `bg-[--brand]` | `bg-(--brand)` |
| Arbitrary component | a custom PostCSS plugin | `@config "..."` only on real dynamics |

## Approach A: utility-first

Classes are written directly in the markup. Pros: **co-location** (the style is visible next to the
element), a smaller final bundle (no duplicated CSS), the absence of "stale" overrides. This is the
starting position of the ladder (rungs 1–3).

- Promote repeated values into `@theme` tokens and use them by name: `bg-primary`,
  `text-muted-foreground`, `rounded-lg`.
- Solve repeated **markup** by extracting it into a partial/fragment, not by collecting utilities into one class.
- A full set of interactive states is mandatory: `hover:`, `focus-visible:`, `active:`,
  `disabled:`; visible focus via `outline-ring`/`ring-ring`.
- **Reduced motion is part of the contract:** every transform/opacity transition and every
  `animate-*` carries a `motion-reduce:` fallback (`motion-reduce:transition-none` /
  `motion-reduce:animate-none`; in SCSS: `@media (prefers-reduced-motion: reduce) { @apply transition-none; }`).

```html
<button
  class="inline-flex items-center justify-center gap-2 h-10 px-4
         rounded-md bg-primary text-primary-foreground
         text-sm font-medium
         transition-colors
         hover:bg-primary/90 focus-visible:outline-2 focus-visible:outline-ring
         active:bg-primary/80 disabled:opacity-50 disabled:pointer-events-none">
  Save
</button>
```

Selection criteria and nuances — `references/approaches.md`.

## Approach B: BEM + `@apply`

A semantic component class into which utilities are inlined via `@apply`, **grouped by property
type**. Pros: readability, "clear at a glance", reuse, convenience with many states/variants. This is
a conscious choice of the upper rungs of the ladder (4–6).

The default BEM convention (camelCase for multi-word parts, lowercase-first):

- block — `cardList`; block modifier — `cardList_compact`; key-value modifier — `cardList_size_lg`;
- element — `cardList-item`; element modifier — `cardList-item_active`.
- Separators: element = single hyphen `-`, modifier = single underscore `_`, modifier-value = `_`.
- One block per component; elements always derive from the block, flat (no `-a-b` chains).
- **Configurable, not dogma:** this is the default. If the project already declares a scheme
  (classic `block__elem_mod`, Two Dashes `--`, React, or its own), **follow that** — consistency
  beats the default. The invariants the skill always enforces regardless of scheme: names must be
  programmatically separable into block/element/modifier; a modifier never stands alone
  (`block block_mod`, never bare `block_mod`); no elements of elements. The scheme catalog and the
  A vs B decision — `references/approaches.md`.
- A thing that **navigates is `<a>`**, a thing that **acts is `<button>`** — pick the tag by
  behavior and put the same `button` block classes on whichever tag is correct (a "link-button" is
  the right classes on the right tag, never a tag swap).

Inside a `<style>`/CSS module, `@apply` requires `@reference`. Group `@apply` by property category in
the canonical order — one `@apply` line per group — and do **not** add per-group label comments; the
line order conveys the grouping. The canonical order: layout → sizing → spacing →
background/borders/shape → typography → effects/motion → interaction, then states, then modifiers.
Within a block body, order: (1) base property groups 1–7, (2) base states, (3) elements in DOM order,
(4) block modifiers last (the engine re-sorts — this is for readability, not cascade).

```scss
@reference "../assets/css/main.css"; /* the entry CSS that defines your @theme tokens — NOT "tailwindcss" */

.button {
  @apply inline-flex items-center justify-center gap-2;
  @apply h-10;
  @apply px-4;
  @apply rounded-md bg-primary;
  @apply text-sm font-medium text-primary-foreground;
  @apply transition-colors motion-reduce:transition-none;

  &:hover            { @apply bg-primary/90; }
  &:focus-visible    { @apply outline-2 outline-ring; }
  &:active           { @apply bg-primary/80; }
  &:disabled         { @apply opacity-50 pointer-events-none; }

  /* block modifier */
  &_compact { @apply h-8 px-3 text-xs; }
}
```

> `@reference` must point at the **entry CSS that defines your `@theme` tokens** (path is relative to
> the source file). `@reference "tailwindcss"` exposes only the **default** theme and silently drops
> your custom tokens — use it only when the component touches no custom tokens.

The grouping canon, the A vs B decision tree, and the "good/bad `@apply`" rule — `references/approaches.md`.

## Anti-patterns (NEVER)

- **NEVER** `@tailwind base/components/utilities;` — only `@import "tailwindcss";`.
- **NEVER** introduce `tailwind.config.js` if there is no real JS dynamics (otherwise — `@theme`).
- **NEVER** `bg-opacity-*` / `text-opacity-*` — only the slash modifier (`bg-primary/90`).
- **NEVER** `bg-gradient-to-*` — it is `bg-linear-to-*` (and `bg-radial-*`/`bg-conic-*`).
- **NEVER** `@layer utilities { .x {} }` for a custom utility — it is `@utility x { ... }`.
- **NEVER** `bg-[--brand]` — the v4 syntax for a CSS variable is `bg-(--brand)`.
- **NEVER** concatenate class names with strings (`text-${color}-500`) — detection is literal; use
  full names or the safelist `@source inline(...)`.
- **NEVER** `@apply` inside `@keyframes`; inside a `<style>`/CSS module without `@reference`.
- **NEVER** `@screen md { @apply ... }` — it is v3 and was **removed** in v4 (the compiler passes it
  through unrecognized and silently drops the wrapped rules). To apply a breakpoint inside CSS use
  `@variant md { @apply ... }` (or the codemod's `@media (width >= theme(--breakpoint-md)) { ... }`).
- **NEVER** hide a "soup" of dozens of utilities in one semantic class for the sake of "clean markup" —
  that is bad `@apply`. Nesting `@apply` within `@apply` is also a no.
- **NEVER** model one-off **page** layout as an Approach-B block. Approach B is for REPEATED named
  primitives (button/card/badge/field); a non-reused page wrapped in a block with 20+ single-use
  elements is utility-soup relocated to SCSS — keep one-off page layout in markup utilities, even on
  a B project.
- **NEVER** nest an `<a>`/link inside a styled `<button>` to reuse button styles (invalid HTML, two
  focus stops, conflicting roles) — put the `button` block classes directly on the navigating `<a>`.
- **NEVER** hardcode design values (colors/radii) instead of mapping the external design system into
  `@theme`; **NEVER** drag in AI-slop defaults (purple-blue gradients, excessive roundings,
  decorative blobs). **NEVER** any translucent surface (`bg-*/<alpha>`) + `backdrop-blur` used for
  effect — including sticky headers/navbars and overlays, not just "glass cards" (a modal scrim may
  be translucent, but do not add `backdrop-blur` to it).
- **NEVER** confuse the two "important"s: the global `@import "tailwindcss" important;` ≠ the suffix `bg-danger!`.
- **NEVER** client-side validation via `invalid:`/`:invalid` — it colors an empty required field right away;
  only `user-invalid:` (after interaction). See `docs/accessibility.md`.
- **NEVER** invent an `inert:` variant — it does not exist; for non-interactivity use the native attribute
  `inert` (+ if needed `opacity-50`/`pointer-events-none`).

> The positive "before → after" pair for each NEVER (clear recognition + canon) —
> `resources/anti-patterns.md`; rationale and subtleties — `references/v4-rules.md` and `references/gotchas.md`.

## Review

Quick self-check before submitting — the master checklist `resources/checklist.md` (a flat summary by
topic, the entry point: consolidates review checks, eval axes, and component invariants). The full
checklist with the "why" (12 items: class detection, tokens vs arbitrary, the set of states, correct
`@apply` grouping, v4 syntax, dark mode, etc.) — `references/review.md`; step-by-step workflow — `workflows/review-tailwind.md`.
Diagnosing "it compiled but doesn't work" (Symptom → Cause → Check → Fix) — `workflows/troubleshoot.md`.
