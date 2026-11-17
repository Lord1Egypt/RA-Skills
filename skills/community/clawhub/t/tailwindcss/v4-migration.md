# Upgrading v3 to v4

v4 moved configuration from JavaScript into CSS and rebuilt the engine. Most markup survives untouched; the breakage is concentrated in config, build chain, and a list of renames that compile cleanly while changing the design.

## Run The Tool First, Read The Diff Second

```bash
git switch -c tailwind-v4        # clean branch, nothing uncommitted
npx @tailwindcss/upgrade
```

The codemod migrates the config, rewrites directives, and renames utilities across the repo. It is good, not omniscient: it cannot see classes built at runtime, classes in files it wasn't pointed at, or `@apply` inside framework style blocks. Review the diff, then walk the checklist below.

## Config Surface

| v3 | v4 |
|---|---|
| `@tailwind base/components/utilities` | `@import "tailwindcss";` |
| `tailwind.config.js` `theme.extend` | `@theme { --color-brand-500: … }` in CSS |
| `content: [...]` | Automatic scanning + `@source "…"` |
| `safelist: [...]` | `@source inline("…")` |
| `darkMode: 'class'` | `@custom-variant dark (&:where(.dark, .dark *));` |
| `plugins: [require('x')]` | `@plugin "x";` |
| `presets: [...]` | `@import "./preset.css";` |
| `addUtilities` in a plugin | `@utility name { … }` |
| `addVariant` in a plugin | `@custom-variant name (…);` |
| `theme('colors.gray.200')` in CSS | `var(--color-gray-200)` |
| `corePlugins: { preflight: false }` | Import the layers individually, or restore what you need in your own `@layer base` |
| `separator`, `corePlugins` | Removed — no replacement |
| `prefix: 'tw-'` → `tw-flex` | `@import "tailwindcss" prefix(tw);` → `tw:flex` |

Keeping a JS config is legitimate: `@config "./tailwind.config.js";` loads it for theme, plugins, and content. Generated token pipelines are the main reason to stay (SKILL.md — Where Experts Disagree).

## Build Chain

- PostCSS plugin moved: `tailwindcss` → `@tailwindcss/postcss`.
- Vite projects should switch to `@tailwindcss/vite` and drop PostCSS entirely.
- Delete `autoprefixer` and `postcss-import`; Lightning CSS is bundled and does both. Leaving them causes duplicated and reordered rules.
- Browser floor rises to Safari 16.4 / Chrome 111 / Firefox 128. This is the one blocker with no workaround.

## Renamed Utilities (compile fine, look different)

| v3 | v4 | What changes if you skip it |
|---|---|---|
| `shadow-sm` | `shadow-xs` | Every small shadow one step heavier |
| `shadow` | `shadow-sm` | Same, across the app |
| `blur`, `rounded`, `drop-shadow` (bare) | `blur-sm`, `rounded-sm`, `drop-shadow-sm` | Bare names now mean one step smaller |
| `rounded-sm` | `rounded-xs` | Corners subtly larger |
| `outline-none` | `outline-hidden` | v4's `outline-none` is a real `outline-style: none` — kills the focus ring under forced colors |
| `ring` (3px blue-500) | `ring-3` for the old look | Bare `ring` is now 1px `currentColor` |
| `bg-opacity-50`, `text-opacity-*` | `bg-black/50`, `text-white/70` | Opacity utilities removed outright |
| `flex-shrink-0`, `flex-grow` | `shrink-0`, `grow` | Old names removed |
| `overflow-ellipsis` | `text-ellipsis` | Old name removed |
| `decoration-slice` | `box-decoration-slice` | Old name removed |

## Silent Default Changes

- **Border color**: was `gray-200`, now `currentColor`. Borders inherit text color, so `border` on dark text draws a near-black line where a light gray used to be. Fix once in a base layer, or make the border color explicit everywhere.
- **Ring**: 3px `blue-500` → 1px `currentColor`.
- **Placeholder color**: derived from the current text color rather than a fixed gray.
- **`space-x-*` selector** changed to target all but the last child; the rules that leaned on the old `:not([hidden]) ~ :not([hidden])` behavior with hidden siblings shift.
- **Palette in OKLCH**: colors render wide-gamut on P3 displays. Screenshots will not match pixel-for-pixel; brand colors pinned as exact hex tokens will.
- **`container`** lost its `center` and `padding` config options; recreate with `@utility container { margin-inline: auto; padding-inline: 2rem; }`.
- **Variable syntax in arbitrary values**: `bg-[--brand]` no longer resolves; use `bg-(--brand)` or `bg-[var(--brand)]`.
- **Important modifier moved to the end**: `!bg-red-500` → `bg-red-500!`.

## Cascade Layers — The One That Surprises Everyone

v4 emits `@layer theme, base, components, utilities`. Any author CSS *outside* a layer now beats every utility regardless of specificity. A stylesheet that coexisted with v3 by relying on specificity ordering will start winning everywhere, and utilities appear struck through in devtools with no explanation (SKILL.md — Cascade And Conflicts). Move legacy CSS into `@layer base` and the relationship inverts back.

## `@apply` In Framework Style Blocks

v4 compiles each CSS file in its own context, so a Vue SFC `<style>`, a Svelte `<style>`, or a `.module.css` has no theme:

```css
/* Component.vue */
<style>
@reference "../app.css";
.btn { @apply bg-brand-500 text-white; }
</style>
```

`@reference` imports the theme for resolution without emitting any CSS. Without it, the build fails with "Cannot apply unknown utility class".

## Migration Order That Minimizes Pain

1. Branch, commit everything, run the upgrade tool.
2. Fix the build chain (PostCSS plugin, remove autoprefixer) until the app compiles.
3. Diff the rendered app against production screenshots for the silent-defaults list — borders and rings first.
4. Grep for the removed syntax the tool cannot see: `theme(`, `!` prefixes inside template strings, `[--` arbitrary variables, `@apply` in framework style blocks.
5. Re-check scanning: classes that lived in files outside the old `content` globs may now be picked up (harmless) — and gitignored generated views may now be missed.
6. Only then move `tailwind.config.js` into `@theme`. It is optional, and doing it during the upgrade doubles the surface of any bug.

## Staying On v3 Deliberately

Legitimate reasons: a browser support floor below Safari 16.4, a JS-generated theme with no CSS equivalent, or a plugin ecosystem dependency with no v4 build. v3 still works; what you give up is the engine's speed and every new variant. Record the decision so the next session doesn't re-litigate it, and set `tailwind_version: 3` in config.
