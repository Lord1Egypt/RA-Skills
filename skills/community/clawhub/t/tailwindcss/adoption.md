# Adoption — Adding Tailwind To A Codebase That Already Has CSS

The greenfield story is easy. Introducing Tailwind next to an existing stylesheet, a component library, or Bootstrap is where projects stall. Two decisions decide the outcome: what to do about Preflight, and who wins the cascade.

## Preflight — The First Blast Radius

`@import "tailwindcss"` includes a reset that removes heading sizes, list markers, and default button styling, and makes `img` `display: block; max-width: 100%`. On an existing site the visible result is that content pages go flat the day Tailwind lands.

Three sanctioned exits, in order of preference (SKILL.md rule 5). All three leave the reset itself untouched: a vendored Preflight with rules commented out is the one handling that is always wrong, because it drifts from the framework on every upgrade with no error.

1. **Keep Preflight, wrap unowned content in `prose`.** Correct for a product where Tailwind is becoming the system. CMS bodies, Markdown, and changelogs get `prose` from the typography plugin (`@plugin "@tailwindcss/typography";`).
2. **Keep Preflight, restore what you need in your own `@layer base`.** Additive, not a patch: Preflight still ships intact and your layer puts back an explicit short list — heading sizes, list markers, whatever the content pages actually lost. Restore deliberately, around five rules, never a copy of the old reset.
3. **Drop Preflight whole** by importing the layers individually:

```css
@layer theme, base, components, utilities;
@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/utilities.css" layer(utilities);
/* preflight.css deliberately omitted */
```

v3 equivalent: `corePlugins: { preflight: false }`.

Dropping it is right when Tailwind is a guest in someone else's design system, and wrong when it is going to become the design system — you inherit every browser default inconsistency you were about to stop fighting.

## Who Wins The Cascade

- **v4**: utilities live in `@layer utilities`. Any legacy CSS **outside** a layer beats every utility regardless of specificity. So on day one your old stylesheet wins everywhere, silently, and utilities show struck through in devtools.
  - To make utilities win: move legacy CSS into a layer declared before Tailwind's — `@layer legacy, theme, base, components, utilities;` then `@import "./legacy.css" layer(legacy);`.
  - To keep legacy winning during a transition: leave it unlayered and reach for the `!` modifier only where a utility must override.
- **v3**: no layers in the output, so plain specificity and source order decide. `.card p { margin: 0 }` (0,2,0) beats `mt-4` (0,1,0). Load Tailwind's CSS **after** the legacy sheet, and expect specificity fights on anything with a descendant selector.
- Either way, decide this once and write it down; a codebase where half the overrides use `!` and half rely on load order has no rule at all.

## Coexisting With A CSS Framework

| Neighbor | Main conflict | Handling |
|---|---|---|
| Bootstrap | Both define `.container`, `.row`, `.btn`; both ship a reset | Prefix Tailwind (`@import "tailwindcss" prefix(tw);` → `tw:flex`) and drop Preflight |
| Material / MUI | Runtime-injected styles land unlayered and win in v4 | Layer your own CSS; use the library's own theming for its components and Tailwind only outside them |
| Legacy BEM stylesheet | Descendant selectors beat utilities in v3 | Layer it (v4) or migrate component by component (below) |
| daisyUI / Flowbite | Second design system *inside* Tailwind, own component layer | Fine for admin tools; costly for bespoke design |
| A scoped-CSS framework (Vue/Svelte SFC) | Scoping raises specificity above utilities | Keep utilities in markup: the scoping data attribute outranks anything you write in a scoped block |

## Prefixing And Scoping

- `@import "tailwindcss" prefix(tw);` in v4 makes every utility `tw:flex`, `tw:hover:bg-red-500`. v3's `prefix: 'tw-'` produced `tw-flex` — a different shape, so the two are not interchangeable in migrated markup.
- Prefix when class-name collisions are real (an old sheet already defines `.flex` or `.hidden`). Skip it otherwise: it makes every class longer forever, and IntelliSense hides the cost only until someone greps.
- v3 could scope importance to a selector (`important: '#app'`) so utilities beat outside CSS inside one subtree. Under v4 the equivalent lever is layer ordering, which is cleaner and does not weaponize `!important`.

## Incremental Migration That Actually Finishes

1. **Install without deleting anything.** Tailwind's presence changes nothing until classes are used — except Preflight, which is why that decision comes first.
2. **Pick a leaf component**, not the shell. Convert it fully; delete the CSS it used in the same commit. A half-converted component is the state that never gets finished.
3. **Extract tokens before markup.** Port the palette, spacing, and type scale into `@theme` up front — otherwise the first fifty converted components hardcode arbitrary values and the rebrand becomes a repo-wide replace.
4. **Track the old stylesheet's size** in CI. It should only ever go down; a migration that doesn't shrink it is adding a second system rather than replacing one.
5. **Convert utilities-only rules first** (`.mt-lg { margin-top: 24px }`) — mechanical, low-risk, and it deletes the largest share of lines.
6. **Leave animations, print, and email rules for last.** They are the least utility-shaped CSS and often correctly stay hand-written.

## Signals The Migration Is Going Wrong

- New `@apply` blocks appearing faster than old CSS disappears — the old system is being renamed, not replaced.
- `!` modifiers accumulating in feature code: the layer decision was never made.
- Both `.btn` and a `Button` component in use, with different visuals.
- The legacy stylesheet's size flat for a month.
- Arbitrary values repeating the same hex — tokens were skipped at step 3.

