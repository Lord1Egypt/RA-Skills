# Installation — Choosing And Wiring The Build

Four ways to compile Tailwind. Pick by what already builds your assets, not by what a tutorial used.

- [Choosing The Integration](#choosing-the-integration) — Vite plugin vs PostCSS vs CLI vs browser
- [v4 Setup](#v4-setup) — install, `@import`, and what to delete afterwards
- [v3 Setup](#v3-setup) — `tailwind.config.js` and the `content` contract
- [Browser Support Floor (v4)](#browser-support-floor-v4) — the one blocker with no workaround
- [Verify The Install In One Minute](#verify-the-install-in-one-minute) — red-box test and artifact size
- [Editor And Repo Tooling](#editor-and-repo-tooling) — IntelliSense, class sorting, lint, CI guard
- [Multiple Entrypoints And Monorepos](#multiple-entrypoints-and-monorepos)

## Choosing The Integration

| Integration | Use when | Cost |
|---|---|---|
| Vite plugin (`@tailwindcss/vite`) | The project already uses Vite (React, Vue, Svelte, Astro, Laravel, SolidJS) | None — fastest path, fewest moving parts |
| PostCSS (`@tailwindcss/postcss`) | The bundler owns PostCSS: Next.js, webpack, Rails with cssbundling, Parcel | One extra config file; slightly slower than the Vite plugin |
| CLI (`@tailwindcss/cli`) | No bundler at all: server-rendered templates, Go/Rails/PHP apps serving static CSS | You own the watch process and cache-busting |
| Browser build (`@tailwindcss/browser`) | Prototypes, CodePen-grade demos, a single throwaway HTML file | Compiles on every page load; never ship it (SKILL.md Traps) |

`build_integration` records the choice; every command below assumes it.

## v4 Setup

```bash
npm install tailwindcss @tailwindcss/vite      # or @tailwindcss/postcss / @tailwindcss/cli
```

```css
/* src/app.css — the whole configuration surface */
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(0.62 0.19 259);
  --font-display: "Satoshi", sans-serif;
}
```

```js
// vite.config.js
import tailwindcss from '@tailwindcss/vite';
export default { plugins: [tailwindcss()] };
```

```js
// postcss.config.mjs — PostCSS route only
export default { plugins: { '@tailwindcss/postcss': {} } };
```

```bash
# CLI route only
npx @tailwindcss/cli -i ./src/app.css -o ./dist/app.css --watch --minify
```

Then import the CSS once, at the app entry (`import './app.css'`) or via a `<link>` in the layout. Importing it in two places doubles the output.

**Remove after installing v4**: `autoprefixer` and `postcss-import` — Lightning CSS is bundled and handles both. Leaving them in produces duplicated or mangled rules.

## v3 Setup

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

```js
// tailwind.config.js
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx,vue,svelte}'],
  theme: { extend: { colors: { brand: { 500: '#1d4ed8' } } } },
  plugins: [],
};
```

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

The `content` array is the entire scanning contract in v3 — `./index.html` is the entry left out most often.

## Browser Support Floor (v4)

v4 output uses `@property`, `color-mix()`, and cascade layers, so it requires **Safari 16.4+, Chrome 111+, Firefox 128+**. Below that, utilities exist but colors, shadows, and transforms degrade or vanish. A project that must serve older engines stays on v3 — there is no flag that lowers the floor.

## Verify The Install In One Minute

1. Put `<div class="p-4 bg-red-500 text-white">ok</div>` in a page and load it.
2. Red box → generation and delivery both work.
3. Class present in devtools but unstyled → the CSS file isn't linked, or is the wrong one (two entrypoints).
4. Nothing at all → grep the built CSS for `bg-red-500`; absent means the scan root is wrong.
5. Check the artifact size: an app-sized project's minified CSS is typically single-digit to low-tens of KB gzipped. A few hundred bytes means nothing was scanned; hundreds of KB means a pattern safelist or a source glob that swept a dependency tree.

## Editor And Repo Tooling

- **IntelliSense** (VS Code / Cursor / Zed extension): needs the CSS entrypoint (v4) or `tailwind.config.js` (v3) discoverable. In a monorepo, set the path explicitly in workspace settings — a silent no-autocomplete is almost always a discovery failure, not a bug.
- Enable suggestions inside strings, or completion never appears in `className`:

```json
{
  "editor.quickSuggestions": { "strings": "on" },
  "tailwindCSS.classFunctions": ["cn", "cva", "clsx", "tw"]
}
```

- **Class sorting**: `prettier-plugin-tailwindcss` emits the canonical order, which kills reorder-only diffs forever. Run it once on the whole repo in its own commit; mixing it with feature work makes every review unreadable.
- **Linting**: rules worth turning on are duplicate/conflicting classes in one attribute and unknown class names; both catch the failures in SKILL.md Traps before review.
- **CI**: build the CSS as a CI step and fail on an artifact under a size floor you set — the cheapest possible guard against a scan-config regression shipping empty styles.

## Multiple Entrypoints And Monorepos

- One Tailwind entrypoint per rendered document. Two apps in one repo get two CSS files, each with its own `@source`/`content` scope.
- Shared UI package: the consuming app points a source at the package's **source** files, not its build output, so it also picks up classes the package author didn't compile.
- Deduplicate the version: two `tailwindcss` copies in the tree (one hoisted, one nested) is a silent split-brain — `npm ls tailwindcss` before debugging anything else.

