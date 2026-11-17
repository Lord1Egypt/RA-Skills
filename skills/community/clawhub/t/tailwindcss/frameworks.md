# Framework Integration — Per-Stack Gotchas

This is what each stack does differently once Tailwind is already installed — the gotchas, not the setup commands.

## Next.js

- PostCSS route: `@tailwindcss/postcss` in `postcss.config.mjs`; import the CSS once in the root layout.
- App Router: the CSS import belongs in `app/layout.tsx`, not in a page — importing it per-page ships duplicate stylesheets and flashes between navigations.
- `next/font` exposes a CSS variable; feed it into the token rather than repeating the family name: `--font-sans: var(--font-inter)` in `@theme`, and the font's `variable` class on `<html>`.
- Dark mode: the paint-blocking script goes in the layout's `<head>` as a raw `<script dangerouslySetInnerHTML>`; a client component effect runs after hydration and flashes.
- Reading `localStorage` or `matchMedia` during render is the standard hydration-mismatch source. Render both variants and hide one with `dark:hidden`.
- Server components can hold Tailwind classes freely — the scanner reads the source file, so RSC/client boundaries are irrelevant to it.
- MDX and content collections: those files are scanned like any other source in v4; in v3 add the extension to `content`.

## Vue And Nuxt

- `@apply` inside an SFC `<style>` block compiles in its own context. v4 requires `@reference "@/assets/app.css";` at the top of the block or the build fails with "Cannot apply unknown utility class".
- `<style scoped>` adds a data attribute to every selector, which raises specificity above plain utilities — scoped rules quietly beat the classes in your template.
- Dynamic classes via `:class="`bg-${tone}-500`"` fail exactly as in JSX; use an object or a lookup map of complete class strings.
- Nuxt: the CSS entry goes in `nuxt.config` `css: []`; the Vite plugin is preferred over the PostCSS route.
- Transition classes (`v-enter-active`) can hold utilities, but they are class *names* Vue generates — the utilities inside them are literal and scanned normally.

## Svelte And SvelteKit

- Same `@reference` requirement for `@apply` inside `<style>` blocks in v4.
- Svelte's `<style>` is scoped and unused-selector-pruned: a rule that only applies via a dynamic class gets removed at compile time with a warning. Keep utilities in the markup.
- `class:name={cond}` directives hold literal class names and are scanned fine; `class={`p-${n}`}` is not.
- SvelteKit: import the CSS in the root `+layout.svelte`.

## Astro

- Use the Vite plugin for v4; the `@astrojs/tailwind` integration targets v3.
- Import the global stylesheet once in a base layout. Astro's per-component `<style>` is scoped and hoisted; `@apply` there needs `@reference`.
- Content collections and Markdown render outside your components — `prose` from the typography plugin is the answer for those bodies.
- Islands share the global stylesheet; nothing extra is needed for a hydrated island's classes.

## Template Languages (Rails, Laravel, Django, Go, PHP)

- v4 scans any non-binary, non-gitignored file, so `.erb`, `.blade.php`, `.html.twig`, `.templ`, and `.j2` are picked up with zero config. v3 needs each extension in the `content` globs — this is the usual "nothing renders" report in these stacks.
- Class names built in the backend (`"bg-#{status}-500"` in Ruby, `"bg-".$color."-500"` in PHP) fail identically to JS interpolation. Map statuses to complete classes in a constant.
- Rails: `tailwindcss-rails` wraps the CLI and wires the watch process into `bin/dev`.
- Laravel: the Vite plugin, with the CSS entry registered in `vite.config.js`.
- Django/Flask: the CLI in watch mode alongside the dev server, output into `static/`; add a cache-busting query or hash in production.
- Server-rendered HTML from a database (CMS pages, rich text) is never scanned — that content gets `prose` and a safelist for any utility the editors may emit.

## Storybook

- Import the global stylesheet in `.storybook/preview.ts`, or every story renders unstyled while the app looks fine.
- `.stories.*` files must be in the scan path: v4 picks them up automatically; v3 needs them in `content`, and a story-only variant class is otherwise missing.
- A dark-mode decorator toggles the `dark` class on the preview root, matching whatever `dark_mode_strategy` the app uses.

## React Native

- Tailwind does not run on React Native; NativeWind maps a subset of utilities to style objects. Check which Tailwind major your NativeWind version targets before copying v4 syntax — the two release lines are not in lockstep.
- No cascade, no pseudo-classes, no media queries in the platform: variants that depend on them either don't exist or are re-implemented differently.

## Email

- Email clients strip or ignore cascade layers, CSS custom properties, and `color-mix()` — all of which v4's output relies on. Utilities that render perfectly in a browser render as nothing in Outlook.
- Use a pipeline that resolves variables and inlines the result (Maizzle, react-email) rather than linking a Tailwind stylesheet; verify the produced HTML has literal values, not `var(--color-brand-500)`.
- Layout in email is tables and inline styles; the utilities buy you a consistent scale, not the layout model.

## Cross-Stack Rules

- **One stylesheet per rendered document.** Two imports mean two copies of the utility layer.
- **Scoped style blocks raise specificity** in Vue and Svelte; anything you write there beats plain utilities.
- **`@reference`, not `@import`,** inside component style blocks in v4 — `@import "tailwindcss"` there emits the entire framework into that component's CSS.
- **Framework class helpers** (`clsx`, `cva`, `tw`) need registering with IntelliSense and with the Prettier plugin, or autocomplete and sorting stop at the function boundary.

