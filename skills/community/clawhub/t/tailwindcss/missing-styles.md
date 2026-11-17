# Missing Styles — The Class Is There, The CSS Is Not

The report that dominates Tailwind help channels, and almost never a Tailwind bug. Work the chain in order; every step is a check, not a guess.

## Triage In Four Checks

1. **Is the class in the built CSS?** `grep -c 'bg-brand-500' dist/**/*.css` (or your build output dir). Zero → scanning problem, continue here. Non-zero → the CSS exists and is losing: that is a cascade problem (SKILL.md — Cascade And Conflicts).
2. **Is the file scanned?** v4: is the file under the project root and not `.gitignore`d? v3: does it match a glob in `content`?
3. **Is the class a complete literal string in that file?** Search the source for the exact class text. If it only exists as a template expression, that's the bug.
4. **Is it the right stylesheet?** Two entrypoints, an old `output.css` committed to the repo, or a framework that imports a stale CSS file will all serve yesterday's build.

## Dynamic Class Names — Rule This Out First

The scanner extracts substrings; it never evaluates.

```jsx
// Broken — none of these strings exist in the file
<div className={`bg-${tone}-500`} />
<div className={'text-' + size} />
<div className={clsx('p-' + spacing)} />

// Works — every candidate is a literal
const TONE = { danger: 'bg-red-500', ok: 'bg-green-500', warn: 'bg-amber-500' };
<div className={TONE[tone]} />
```

- Partial literals do not help: `bg-red-` plus `500` is two strings, and neither is a utility.
- The same rule applies to CSS-in-template languages: `class="bg-{{ color }}-500"` in Blade, ERB, Jinja, or Go templates fails identically.
- Numeric interpolation for widths (`w-[${pct}%]`) fails too. Use an inline `style` for genuinely continuous values — that is what `style` is for, and it costs no CSS.

## Classes The Scanner Cannot Reach

| Source of the class | Why it's invisible | Fix |
|---|---|---|
| Database, CMS field, API response | Never appears in any source file | Force-generate the closed set: v4 `@source inline("…")`, v3 `safelist` |
| Compiled files inside a dependency | `node_modules` is excluded by default | v4 `@source "../../node_modules/@acme/ui/dist";` · v3 add the path to `content` |
| Sibling package in a monorepo | Outside the app's scan root | v4 `@source "../ui/src";` (paths resolve relative to the CSS file) · v3 add the glob |
| A new top-level directory | v3 only sees the globs it was given | Extend `content`; v4 needs nothing |
| Exotic file type (`.mdx`, `.erb`, `.templ`, `.php`) | v3 globs are extension-scoped | Add the extension to the glob; v4 reads any non-binary, non-ignored file |
| Anything gitignored (generated views, build output that is also source) | v4 respects `.gitignore` | `@source "./generated";` explicitly re-includes it |

## Forcing Generation Without Blowing Up The Bundle

```css
/* v4 — enumerate, do not pattern-match */
@source inline("bg-red-500 bg-green-500 bg-amber-500");
@source inline("{hover:,focus:,}bg-blue-{500,600,700}");  /* brace expansion */
```

```js
// v3
safelist: [
  'bg-red-500', 'bg-green-500',
  { pattern: /^bg-(red|green|amber)-(500|600)$/, variants: ['hover'] },
]
```

- Anchor every regex (`^…$`). `/bg-.*/` matches the entire color palette across every shade and variant, which is how a 12 KB stylesheet becomes 400 KB.
- A safelist entry is a permanent cost paid on every page. If the set of possible classes is open-ended, the design is wrong: map CMS values to a fixed set of component variants instead of letting content authors emit arbitrary utilities.

## Works In Dev, Missing In Production

Ordered by frequency:

1. **A different config or CSS entrypoint in the build.** Compare the dev command and the build command: separate PostCSS configs, a framework preset overriding yours, or `NODE_ENV`-gated config all produce this.
2. **v3 with a `content` glob that only matched the dev tree** — e.g. `./src/**/*` while production also renders from `./content/**/*.mdx`.
3. **A stale committed artifact.** A checked-in `output.css` or `public/build/*` from months ago that the production template links instead of the built asset.
4. **CDN or proxy cache** serving the previous CSS with a fresh HTML. Hard-reload with cache disabled before touching config.
5. **Two Tailwind versions in the dependency tree** (one hoisted, one nested) — the plugin resolves one, your CSS imports the other. `npm ls tailwindcss` shows both.

Bisect quickly: add a class no design uses (`outline-4 outline-fuchsia-500`) to the failing element, rebuild, and grep the artifact. Present → scanning is fine and the fault is cascade or the served file. Absent → scanning.

## Only Some Classes Missing

- Only the **new** ones → dev server didn't restart after a config change. v4 CSS-config edits hot-reload; `tailwind.config.js` and `@source` changes often need a restart.
- Only classes **with variants** (`md:`, `dark:`, `group-hover:`) → the variant is undefined (custom variant not declared) or the prefix is wrong for the major.
- Only classes in **one component** → that file is excluded (ignored path, wrong extension) or it holds a different quoting style your custom IntelliSense/extract regex breaks on.
- Only **custom theme** classes (`bg-brand`) → the token isn't in `@theme` (v4 requires `@theme`, a plain `:root` variable generates nothing) or is under the wrong namespace: `--color-brand` makes `bg-brand`, `--brand` makes nothing.

