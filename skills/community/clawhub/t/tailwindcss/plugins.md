# Plugins — Official, Custom, And Third-Party

Most projects need two official plugins and zero custom ones. Write a plugin when you need a utility that must sort with utilities and accept variants; anything else is a component.

## The Official Plugins

| Plugin | Gives you | Load when |
|---|---|---|
| `@tailwindcss/typography` | `prose` — readable defaults for HTML you didn't write | Markdown, MDX, CMS body fields, changelogs |
| `@tailwindcss/forms` | Resets native form controls to a stylable baseline | Any real form; browser defaults are unstylable otherwise |
| `@tailwindcss/container-queries` | `@container` and `@md:` variants | v3 only — core in v4 |
| `@tailwindcss/aspect-ratio` | `aspect-w-*` | Legacy only — `aspect-video`/`aspect-square` are core since v3.0 |

```css
/* v4 */
@plugin "@tailwindcss/typography";
@plugin "@tailwindcss/forms";
```

```js
// v3
plugins: [require('@tailwindcss/typography'), require('@tailwindcss/forms')]
```

## `prose` In Practice

- `prose` sets sizes, spacing, and colors for descendant elements — it is the antidote to Preflight on content you don't author (SKILL.md rule 5).
- Size and theme modifiers: `prose prose-lg prose-slate dark:prose-invert`.
- Element overrides use the element modifier: `prose-headings:font-display prose-a:text-brand-600 prose-img:rounded-lg`.
- Escape a subtree with `not-prose` — the wrapper for an interactive widget or a code playground embedded in an article.
- `max-w-none` when the article already sits in a sized column; `prose` caps its own measure by default and the two caps fight.
- Code blocks: `prose` styles `pre`/`code` lightly; a syntax highlighter's own theme needs `prose-pre:bg-transparent prose-pre:p-0` or the two backgrounds stack.

## `forms` In Practice

- Default strategy resets every native control globally. `@plugin "@tailwindcss/forms" { strategy: class; }` (v4) or `require('@tailwindcss/forms')({ strategy: 'class' })` (v3) instead opts in per element with `form-input`, `form-select`, `form-checkbox`.
- Use `class` strategy in any app that already has form styling, or the plugin silently restyles the whole product on install.
- `accent-color` (`accent-brand-500`) brands checkboxes and radios without the plugin at all — the cheapest option when native controls are acceptable.
- After the reset, focus styling is yours: the plugin removes the browser ring and leaves you responsible for the canonical replacement (SKILL.md rule 8).

## Writing A Custom Utility (v4)

```css
@utility scrollbar-none {
  scrollbar-width: none;
  &::-webkit-scrollbar { display: none; }
}

/* functional — takes a value, so arbitrary syntax works: tab-4, tab-[7] */
@utility tab-* {
  tab-size: --value(integer);
}
```

- `@utility` output sorts inside the `utilities` layer, so variants (`md:`, `hover:`) and `@apply` both work on it. A rule written in `@layer components` gets neither.
- The `*` suffix plus `--value(...)` is what makes a utility accept values; a static `@utility` name never takes an argument.
- Name with the framework's grammar (`scrollbar-none`, not `noScrollbar`) or IntelliSense and `twMerge` grouping both miss it.

## Writing A Plugin (v3, or when you need JS)

```js
const plugin = require('tailwindcss/plugin');

module.exports = plugin(({ addUtilities, matchUtilities, addVariant, theme }) => {
  addUtilities({ '.scrollbar-none': { 'scrollbar-width': 'none' } });

  matchUtilities(
    { 'text-shadow': (value) => ({ textShadow: value }) },
    { values: theme('textShadow') },
  );

  addVariant('sidebar-open', '[data-sidebar="open"] &');
  addVariant('supports-backdrop', '@supports (backdrop-filter: blur(0))');
});
```

- `addUtilities` for static; `matchUtilities` for value-taking (it is what makes arbitrary values work on your utility).
- `addComponents` exists and is almost always the wrong choice — it emits into the components layer where utilities override it, which is right for a base style and wrong for anything you expected to win.
- `addBase` for element-level defaults; keep it to a handful of rules or you have written a reset nobody knows about.
- A plugin can be loaded into v4 with `@plugin "./my-plugin.js";` — the JS API still works, so a v3 plugin usually survives the upgrade unchanged.

## Third-Party Plugins

- Component libraries that ship classes (daisyUI, Flowbite) hand you a second design system inside Tailwind. Legitimate for internal tools and admin panels; costly when the design is bespoke, because every override fights the library's own layer.
- Check the plugin declares v4 support before an upgrade — plugins that reach into internal APIs (rather than the documented `plugin()` surface) are the usual thing that blocks a migration.
- Any plugin that ships class names must be in the scan path if it generates markup, and safelisted if it generates class names at runtime.
- Audit before adding: a plugin adding 5 utilities you could write in 10 lines of `@utility` is a dependency, a version constraint, and a migration risk.

