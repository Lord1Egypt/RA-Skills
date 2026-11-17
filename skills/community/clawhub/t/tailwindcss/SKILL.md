---
name: tailwindcss
slug: tailwindcss
version: 1.0.1
description: >-
  Writes and debugs Tailwind CSS: utility classes, theme config, dark mode, variants, plugins, and build setup. Not for CSS mechanics themselves — stacking contexts, flex sizing, and cascade behavior belong to the `css` skill. Use when a class produces no CSS, when dynamically built names (`bg-${color}-500`) never render, when styles work in dev but vanish after deploy, when your own CSS beats a utility or can't override one, when `@apply` breaks inside a Vue, Svelte, or CSS-module file, when `hover:`, `group-hover:`, `peer-*`, `has-[…]`, or `dark:` won't fire, when upgrading v3 to v4 (`@tailwind` directives, `tailwind.config.js` → `@theme`, renamed utilities), when adding custom colors, spacing, breakpoints, fonts, or keyframes, when wiring Tailwind into Vite, Next.js, Astro, SvelteKit, Rails, or Laravel, when the CSS bundle is huge or rebuilds crawl, when Preflight flattens third-party widgets, or when choosing between `@apply`, a component, and `tailwind-merge`.
homepage: https://clawic.com/skills/tailwindcss
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: 🌊
    requires:
      bins:
      - npx
    os:
    - linux
    - darwin
    - win32
    displayName: Tailwind CSS
    configPaths:
    - ~/Clawic/data/tailwindcss/
---

User preferences and memory live in `~/Clawic/data/tailwindcss/` (see `setup.md` on first use, `memory-template.md` for the file format). If you have data at an old location (`~/tailwindcss/` or `~/clawic/tailwindcss/`), move it to `~/Clawic/data/tailwindcss/`.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/tailwindcss/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| tailwind_version | 3 \| 4 | 4 | Selects the config surface of every answer: `4` emits `@import "tailwindcss"`, `@theme`, `@source`, `@utility`, suffix `!`; `3` emits `tailwind.config.js`, `@tailwind` directives, `content`, `safelist`, prefix `!` |
| build_integration | vite \| postcss \| cli \| browser | vite | Which install steps and config files `installation.md` emits, and where the scan root sits |
| dark_mode_strategy | media \| class \| data-attribute | media | The variant definition emitted in CSS, and whether toggle code plus the paint-blocking script ships with it (`dark-mode.md`) |
| component_syntax | jsx \| vue-sfc \| svelte \| astro \| html | jsx | Markup language of every emitted example, and which `@apply`/`@reference` rules apply (`frameworks.md`) |
| merge_helper | cn \| clsx \| tailwind-merge \| none | cn | Helper wrapped around conditional or overridable class props in emitted components (`components.md`) |
| rem_base | number px (10-16) | 16 | Every px↔rem conversion for **utilities** in Utility Scale Math (`p-4` = 4 × 0.25rem = 1rem = rem_base px). Breakpoints are exempt — see that section |
| token_threshold | number (2-5) | 3 | Uses of the same value before it must become a theme token: gates Core Rule 2, the promotion rules in `arbitrary-values.md` and `variants.md`, and the second Output Gate |
| text_direction | ltr \| rtl \| both | ltr | `ltr` emits physical utilities (`ml-4`, `text-left`, `border-l`); `rtl` and `both` emit logical ones (`ms-4`, `text-start`, `border-s`) everywhere and add `dir` to example markup (`variants.md`) |
| a11y_target | aa \| aaa | aa | Which contrast and target-size rows gate output: AA = 4.5:1 body and `size-6`; AAA = 7:1 body and `size-11` (`accessibility.md`) |

Preference areas to record as the user reveals them:

- **tooling** — formatter and lint stack (`prettier-plugin-tailwindcss`, ESLint class rules), IntelliSense regex for custom helpers, how eagerly to adopt new majors
- **conventions** — theme namespace naming, CSS entrypoint layout, where component classes are allowed to live
- **design system** — palette source (default palette, brand tokens, an imported token pipeline), spacing and type scale overrides, multi-brand or white-label needs
- **integrations** — UI kit in play (shadcn/ui, Headless UI, Radix, daisyUI, Flowbite): decides the variant idiom (`data-[state=…]`) and the class-merging strategy
- **risk posture** — appetite for arbitrary values and the `!` modifier, whether Preflight may be dropped, tolerance for features above the v4 browser floor
- **constraints** — banned techniques (`@apply`, browser build, runtime class construction), legacy stylesheets that must keep winning, email or WebView targets
- **output** — whether to show the generated CSS, and whether to name the mechanism before giving the fix

## When To Use

- Writing or reviewing Tailwind markup, `@theme`/`tailwind.config.js`, custom utilities, or plugins
- Debugging: a class emits nothing, emits but loses, works in dev and not in production, or fires in the wrong state
- Setting up or migrating: first install, framework wiring, v3 → v4, adding Tailwind to a codebase that already has CSS
- Design-system work in Tailwind: tokens, dark mode, multi-brand theming, component variant APIs
- Build health: rebuild speed, CSS bundle size, monorepo and library scanning
- Not for CSS mechanics or taste — why a flex child overflows belongs to `css`, palette and scale choices to `design-system`

## Quick Reference

| Situation | Play |
|---|---|
| Class is in the markup, no CSS in the output | The scanner never saw the string (→ Class Detection); dynamic name or unscanned file → `missing-styles.md` |
| Works in dev, gone after `build` | Same scanner problem, plus config drift between dev and build → `missing-styles.md` |
| CSS is generated but the element ignores it | Cascade And Conflicts below, then `debugging.md` symptom chains |
| Your own CSS silently beats every utility | Unlayered author CSS outranks every cascade layer in v4 (→ Cascade And Conflicts) |
| Two utilities of the same property fight (`px-4 px-6`) | Sheet order decides, not attribute order; runtime merging → `components.md` |
| `hover:`, `group-hover:`, `peer-*`, `has-[…]`, `data-[…]` won't fire | `variants.md` |
| `dark:` does nothing, or the theme flashes on load | `dark-mode.md` |
| Custom color, spacing step, font, breakpoint, or keyframe | `theming.md` |
| A one-off value the theme has no token for | `arbitrary-values.md` |
| `space-x` gaps wrong, `truncate` won't truncate, `w-screen` overflows | `layout.md` |
| A breakpoint fires at the wrong width, a range needs both bounds, or one component must respond to its own width | `responsive.md` |
| The same 14 classes repeated in 30 places | `components.md` — component boundary, `cva`, `cn`, and where `@apply` is still correct |
| `prose`, form-control resets, or writing a custom utility/variant | `plugins.md` |
| Transitions, keyframes, enter/exit animation, reduced motion | `animations.md` |
| Focus rings, `sr-only`, contrast of the default palette | `accessibility.md` |
| Next.js, Nuxt, Astro, SvelteKit, Rails, Laravel, Storybook, email, React Native | `frameworks.md` |
| First install, Vite plugin vs PostCSS vs CLI, editor IntelliSense | `installation.md` |
| Slow rebuilds, huge CSS file, monorepo or library scanning | `performance.md` |
| Upgrading v3 → v4, or an error naming `@tailwind`, `content`, or `corePlugins` | `v4-migration.md` |
| Adding Tailwind to a codebase that already has CSS, Bootstrap, or a UI kit | `adoption.md` |
| Anything else | Put the single class on a bare `<div>` in isolation: if it works there the fault is scanning or cascade, not the utility |

## Core Rules

1. **A class only exists if its complete string exists in a scanned file.** The scanner is a text matcher, not a JS evaluator: `bg-${tone}-500`, `'text-' + size`, and `` `p-${n}` `` produce zero CSS and zero errors. Write a lookup of whole classes — `const tone = { danger: 'bg-red-500', ok: 'bg-green-500' }` — and index into it.
2. **Theme first, arbitrary second, `@apply` last.** A value used ≥ `token_threshold` times (default 3) becomes a token (`--color-brand-500: oklch(0.62 0.19 259)`); below that, `bg-[#1da1f2]`. **The legitimate uses of `@apply` are exactly three, and this list is closed**: third-party HTML, `::-webkit-*` pseudo-elements, print sheets. Anything else you were about to `@apply` is a component you haven't written yet.
3. **Conflicts resolve by generated-sheet order, never by attribute order.** Tailwind sorts by property group then by scale ascending, so `px-6` is emitted after `px-4` and wins — `class="px-6 px-4"` still renders 1.5rem. To resolve at runtime, `twMerge('px-4','px-6')` → `px-6`; string concatenation just ships both.
4. **A manual dark toggle needs three things or it fails silently.** Default `dark:` follows `prefers-color-scheme`. Manual toggling requires (a) the strategy — v4 `@custom-variant dark (&:where(.dark, .dark *));`, v3 `darkMode: 'class'`; (b) the class on `<html>`, not on a component; (c) a blocking inline script that sets it before first paint, or every reload flashes the wrong theme.
5. **Preflight is take-it-or-leave-it: never fork or edit the reset itself.** It removes heading sizes and list markers and makes `img` `display: block; max-width: 100%` — which is why CMS HTML and third-party widgets go flat the day Tailwind lands. Three sanctioned exits, in order: wrap unowned content in `prose` (typography plugin); **restore** the handful of defaults you need in your own `@layer base` (an explicit short list, never a copy of the old reset); or drop Preflight whole by importing the layers individually (`adoption.md`). What is forbidden is a patched Preflight — a vendored copy with rules commented out drifts from the framework on every upgrade with no error.
6. **Mobile-first: unprefixed applies everywhere, `md:` means ≥768px and up.** A range needs two utilities (`md:flex lg:hidden` = 768–1023px) or one `max-*` variant (`max-lg:flex`). "Only on tablets" written as `md:block` is the classic responsive bug in Tailwind markup.
7. **Repetition is a component problem, not an `@apply` problem.** A component with a variant map (`cva`) plus a mergeable `className` prop keeps variants, IntelliSense, and the scanner working. `@apply` does support variants (`@apply hover:bg-blue-500` compiles fine) — what it costs you is discoverability and override order, and inside a Vue `<style>` or CSS module it needs `@reference` to see the theme at all.
8. **Never remove a focus affordance without replacing it in the same rule.** `focus:outline-none` alone is the classic Tailwind accessibility regression. Canonical replacement, used verbatim everywhere in this skill: `focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-offset-2` (add a `focus-visible:ring-*` color where the default `currentColor` is wrong). Two reasons for every token in it: `outline-hidden` keeps the outline under forced colors where `outline-none` deletes it, and `focus-visible:` on **both** halves means a mouse click shows no ring while keyboard focus does — `focus:outline-hidden` would strip the native outline on click too.
9. **Read the rename list before bumping the major.** v4 renamed `shadow`→`shadow-sm`, `shadow-sm`→`shadow-xs`, `rounded`→`rounded-sm`, `outline-none`→`outline-hidden`, dropped `bg-opacity-*` for `bg-black/50`, and changed `ring` from 3px blue to 1px `currentColor`. The build succeeds and the design shifts quietly (`v4-migration.md`).

## Utility Scale Math

Canonical home for these numbers; other files point here.

- **Utilities — px = rem × `rem_base`.** Step `n` = n × 0.25rem. `p-4` = 1rem = 16px at the default `rem_base` 16, and 10px at `rem_base` 10, because a utility's rem resolves against `html { font-size }`. Fractional steps 0.5/1.5/2.5/3.5 exist; `px` = 1px. v4 derives every step from `--spacing: 0.25rem`, so any multiple works (`p-13` = 3.25rem); v3 only ships the listed steps.
- **Breakpoints — `rem_base` does not apply.** sm 640px/40rem · md 768/48 · lg 1024/64 · xl 1280/80 · 2xl 1536/96, identical in both majors. A media query resolves `rem` against the browser's **initial** font-size, always 16px, ignoring `html { font-size }` (CSS Media Queries Level 4, "Evaluating Media Features"). So `sm:` is 640px even in a project with `rem_base: 10` — computing 40 × 10 = 400px there is wrong. This is the one exception to the row above.
- **Container scale is not the breakpoint scale.** `max-w-*` and container-query sizes share `--container-*`: xs 20rem · sm 24 · md 28 · lg 32 · xl 36 · 2xl 42 · 3xl 48 · 4xl 56 · 5xl 64 · 6xl 72 · 7xl 80. So `max-w-sm` = 24rem while `sm:` = 40rem — the pair most often misread in the framework.
- **Type** (size/line-height, rem): `text-sm` 0.875/1.25 · `text-base` 1/1.5 · `text-lg` 1.125/1.75 · `text-xl` 1.25/1.75 · `text-2xl` 1.5/2.
- **Target sizes**: `size-6` = 1.5rem = 24px = WCAG 2.2 AA floor (2.5.8); `size-11` = 2.75rem = 44px = AAA and Apple HIG. `a11y_target` picks the row. The floor is specified in CSS px, so under `rem_base` 10 those same classes render 15px and 27.5px and fail it — size hit areas in px or raise the step.
- **Opacity modifier**: `bg-blue-500/50` is the color at 50% alpha. v4 computes it with `color-mix()`, so it also works on `currentColor` and on a CSS variable; v3 required a color defined with the `<alpha-value>` placeholder.

## Class Detection

The mental model that explains most Tailwind bugs: the build reads your source files as **plain text** and extracts every substring shaped like a utility. It does not parse, does not resolve imports, and does not run your code.

- A class inside a comment or a dead branch is generated. A class assembled at runtime is not. A class that lives only in a database row, CMS field, or API response is never seen.
- v4 scans from the project root automatically, skipping `.gitignore`d paths, binaries, and `node_modules`. Widen with `@source "../packages/ui/src";`, narrow with `@source not "./legacy";`, force with `@source inline("bg-red-500 bg-green-500");`.
- v3 scans exactly the `content` globs and nothing else. A new top-level directory, or an `index.html` missing from the array, yields silence — not an error.
- Classes shipped inside a dependency's compiled files are invisible in both majors until you point a source at them (`missing-styles.md`).
- Verify, don't hope: after a production build, `grep -c 'bg-brand-500' dist/**/*.css`. Either the class is in the artifact or the scan configuration is wrong.

## Cascade And Conflicts

- **v4 emits into cascade layers** (`theme, base, components, utilities`). Author CSS written *outside* any layer beats every layer regardless of specificity — one stray unlayered `.card { padding: 0 }` disables `p-4` on every card, and DevTools shows the utility struck through with no specificity explanation. Move that rule into `@layer base` and the utility wins again.
- **v3 output has no layers**: plain specificity and source order decide, so `.card p { margin: 0 }` (0,2,0) beats `mt-4` (0,1,0). Same symptom, opposite mechanism — check `tailwind_version` before diagnosing.
- Same-property utilities never "override" each other in the attribute; both are generated and the sheet decides (→ Core Rule 3).
- Override across a component boundary with `twMerge`, which knows the conflict groups. Custom utilities need `extendTailwindMerge` or the merge silently keeps both (`components.md`).
- Escape hatch: the important modifier — v4 suffix `bg-red-500!`, v3 prefix `!bg-red-500`. Reserve it for CSS you don't own; `important: true` project-wide trades one problem for a permanent one.
- Custom CSS placement: `@layer components` for anything a utility should be able to override, `@utility` (v4) for anything that must sort with utilities and accept variants.

## Output Gates

Before emitting Tailwind markup or config, verify:

- Every class a complete literal string in a scanned file — no interpolation, no concatenation?
- Any value repeated ≥ `token_threshold` times (default 3) promoted to a theme token instead of repeated arbitrary syntax?
- Interactive elements carry the canonical `focus-visible` ring of rule 8 and meet the target-size row?
- Directional utilities match `text_direction` — logical (`ms-*`, `text-start`) whenever it is not `ltr`?
- Every color set has its `dark:` counterpart, if the project themes?
- Layout read at the smallest width first — unprefixed is mobile, not desktop?
- Text colors pass the contrast floor (`text-gray-400` on white is ≈2.5:1 and fails)?
- Syntax matches `tailwind_version` — no `@tailwind` directive in a v4 project, no `@theme` block in a v3 one?

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `bg-${color}-500`, `'text-' + size` | The scanner is a text matcher; that string never exists in the source | Lookup map of complete classes (→ Class Detection) |
| `class="px-4 px-6"` to override | Both are generated; the stylesheet decides, not the attribute | `twMerge`, or don't emit both (→ Cascade And Conflicts) |
| `focus:outline-none` with nothing after it | Deletes the only affordance keyboard users have | `focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-offset-2` (→ Core Rule 8) |
| `important: true` in the config | Every utility becomes `!important`: third-party CSS dies and your own overrides need escalation | Per-class `!` on the few that need it; layer your CSS instead (→ adoption.md) |
| `@apply` in a Vue `<style>` or a CSS module | That file compiles in its own context with no theme loaded | v4 `@reference "../app.css";` first — better, move the classes to the markup (→ frameworks.md) |
| `h-screen` for a full-height mobile section | `100vh` ignores the browser chrome that collapses on scroll | `h-dvh`, or `h-svh` when live resizing would be jumpy |
| `w-screen` for a full-bleed row | `100vw` includes the scrollbar width → horizontal scroll on desktop | `w-full`, or `w-dvw` |
| `space-x-4` on a wrapping or reversed row | The sibling selector skips wrapped rows and inverts under `flex-row-reverse` | `gap-4` (→ layout.md) |
| `truncate` with no width constraint | `text-overflow` needs a resolvable width; a flex child defaults to `min-width: min-content` | `min-w-0` on the flex child, or an explicit `max-w-*` |
| `safelist: [{ pattern: /bg-.*/ }]` | Emits the whole palette across every variant — bundle explodes, tree-shaking gone | Enumerate the real classes (→ missing-styles.md) |
| Adding `dark:` to background only | Half the component follows the theme; the bug is invisible in the mode you develop in | Set foreground and background as a pair, every time |
| Browser build (`<script src=…tailwindcss">`) in production | Compiles on every page load, no scanning discipline, no plugin parity | A real build step (→ installation.md) |
| Pasting v3 snippets into a v4 project | `@tailwind`, `content`, `corePlugins`, and `safelist` are gone; the error names the directive, never the cause | Mapping table in `v4-migration.md` |
| `rounded-full` on an element without `overflow-hidden` | Absolutely positioned children paint over the rounded corner | `overflow-hidden` on the rounded parent (→ layout.md) |

## Where Experts Disagree

- **`@apply`.** Tailwind's own maintainers argue against it; design-system teams shipping a class API to templates they don't control use it deliberately. Boundary: `@apply` is right when the markup isn't yours to edit — otherwise it's a component you haven't written yet.
- **Arbitrary values vs a closed theme.** One camp treats `[...]` as a design-system leak; the other as the reason Tailwind survives real designs. Boundary: escapes are fine at the leaf, harmful in shared components — those pull from tokens so a rebrand is one file.
- **CSS config (`@theme`) vs JS config (`@config`).** JS is programmable — loops, imports from a token package, generated scales — and v4 still loads it. Boundary: generated token pipelines stay in JS; hand-maintained themes move to `@theme` and get CSS variables for free.
- **Class sorting.** Automated (`prettier-plugin-tailwindcss`, canonical order, zero diff noise) vs hand-grouped by concern (layout, then color, then state) for readability. Boundary: any repo with more than one author takes the automated order; the argument only survives in solo codebases.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/tailwindcss (install if the user confirms):
- `css` — the mechanics underneath the utilities: stacking contexts, flex sizing, cascade
- `react` — component architecture, props, and state around the class strings
- `nextjs` — App Router, fonts, and build integration specifics
- `design-system` — tokens, scales, and multi-product theming above the config file
- `accessibility-audit` — full WCAG review beyond the floor enforced here

## Feedback

- If useful, star it: https://clawic.com/skills/tailwindcss
- Latest version: https://clawic.com/skills/tailwindcss

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/tailwindcss.
