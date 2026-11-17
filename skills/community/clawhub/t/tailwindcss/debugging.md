# Debugging — Symptom to Cause

Each chain is ordered by probability. Start with the split: is the CSS missing, or present and losing?

## The Universal First Three

1. **Inspect the element.** If the utility's rule doesn't appear in DevTools at all → generation problem: the scanner never saw that string (SKILL.md — Class Detection). If it appears struck through → cascade problem, continue below.
2. **Read the layer badge.** Browser devtools name the cascade layer next to each rule, which is how you see v4's layers. A rule with no layer badge beating one in `utilities` is the whole story (SKILL.md — Cascade And Conflicts).
3. **Reproduce in isolation.** Same class on a bare `<div>` at the top of `<body>`. Works → the problem is context (ancestor, layer, plugin), not the utility.

## Class Generated But Not Applied

1. Another utility of the same property is present and sorts later — `class="px-6 px-4"` renders 1.5rem (SKILL.md rule 3).
2. Unlayered author CSS is winning (v4) or higher-specificity CSS is winning (v3). Search the codebase for the property, not the class.
3. An inline `style` attribute is set by the framework or a UI library — inline beats everything short of `!important`.
4. The element isn't the one you think: check for a wrapper that receives `className` while the styled node is a child, the classic in Radix/Headless UI `asChild` composition.
5. A parent has `display: contents`, `overflow: hidden`, or a transform that makes the property meaningless (positioning, sticky). That is CSS mechanics — hand off to the `css` skill.

## Variant Never Fires

| Variant | First thing to check |
|---|---|
| `hover:` on touch | Hover doesn't exist there; pair with `active:` and `focus-visible:` |
| `group-hover:` | The ancestor has the literal `group` class, and it is an *ancestor*, not a sibling |
| `peer-checked:` | The peer element precedes the target in the DOM (sibling combinator only looks forward) |
| `dark:` | Strategy declared, class on `<html>` (not on a component), blocking script before first paint (SKILL.md rule 4) |
| `data-[state=open]:` | The attribute is on the same element the utility is on, unless prefixed with `group-`/`peer-` |
| `md:` | Viewport really is ≥768px — device toolbar zoom lies; and unprefixed still applies below |
| Custom variant | Declared with `@custom-variant` (v4) or `addVariant` (v3), and the CSS restarted |
| Anything with `[]` | Brackets survived the template engine and no unescaped quote broke the string |

Read the generated selector in devtools before rewriting a stacked variant: the selector says exactly which nesting you got.

## Theme Value Ignored

1. Wrong namespace: utilities come from a namespace, not from any variable. `--color-brand: red` → `bg-brand`, `text-brand`. `--brand: red` → nothing.
2. Declared in `:root` instead of `@theme` (v4): `:root` sets a variable, `@theme` sets a variable *and* registers utilities.
3. v3: added at the top level of `theme` instead of `theme.extend`, which replaced the whole default scale and broke every other utility of that namespace at the same time.
4. Value present, utility present, no effect → a later `@theme` block or an imported preset redefines the same token.
5. Reading the value at runtime: v4 exposes theme values as CSS variables (`var(--color-brand)`); v3 has no runtime variables unless you defined them yourself.

## Build Errors

- `Cannot apply unknown utility class` → v4 `@apply` in a file with no theme context (Vue `<style>`, CSS module, Svelte) — add `@reference "../app.css";` at the top of that block, or the class genuinely doesn't exist.
- `@tailwind` / `Unknown at rule` → v3 syntax in a v4 project.
- `It looks like you're trying to use tailwindcss directly as a PostCSS plugin` → v4 needs `@tailwindcss/postcss`, not `tailwindcss`, in the PostCSS chain.
- `Module not found: autoprefixer` after upgrading → v4 bundles Lightning CSS; remove `autoprefixer` and `postcss-import` from the chain and from `package.json`.
- Nested `@apply` of your own class → `@apply` only accepts Tailwind-generated classes; a class you wrote in `@layer components` isn't one. Extract the declarations, or define it with `@utility` (v4).
- Build passes, output is nearly empty (a few hundred bytes) → nothing was scanned; the scan root or `content` is wrong.

## Wrong Rendering, Right CSS

- Colors look duller or shifted after upgrading to v4 → the palette moved to OKLCH and renders wide-gamut on P3 displays. Real difference, not a bug; pin exact brand hexes as tokens.
- Borders became invisible → v4's default border color is `currentColor`, not `gray-200`. Set `--color-border` and use it, or restore the old default in a base layer.
- Rings look thin → v4 `ring` is 1px `currentColor` (v3: 3px blue). Use `ring-3` for the old look.
- Shadows one step too strong → the shadow scale shifted by one name in v4 (`shadow` → `shadow-sm`).
- Spacing subtly off across the app → a `rem_base` other than 16 in the host page's `html { font-size }`; every rem-based utility scales with it, while breakpoints do not (SKILL.md — Utility Scale Math).

## Editor And Tooling Lies

- No autocomplete → the IntelliSense extension can't find the CSS entrypoint (v4) or the config (v3); point it explicitly in workspace settings.
- Autocomplete inside `cva`/`cn` needs `tailwindCSS.classFunctions` (or an `experimental.classRegex` entry); otherwise the strings look like plain text to the editor.
- Prettier reorders classes and a diff explodes → expected on first run of `prettier-plugin-tailwindcss`; commit the reformat alone.
- "Unknown at rule @theme" squiggles in the editor with a green build → the editor's CSS language service, not Tailwind. Set the workspace CSS validation to ignore unknown at-rules.

## When You Are Truly Stuck

Build once with the CSS entrypoint reduced to `@import "tailwindcss";` and a single test element. Add back one thing at a time — plugin, preset, custom layer, framework integration. The step that breaks it names the file to open next.
