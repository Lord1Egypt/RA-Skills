# Publishing a Svelte Component Library

Shipping components to other apps is a different job from shipping an app: you distribute **source**, not a bundle, and every assumption you bake in becomes their problem.

## The Package Shape

```
my-lib/
├── src/lib/          # the package root — everything here is published
│   ├── index.js      # the entry: re-export the public surface
│   └── Button.svelte
├── src/routes/       # your demo/docs app — NOT published
├── package.json
└── svelte.config.js
```

```bash
npx sv create my-lib          # choose the library option
npm run package               # runs svelte-package → dist/
```

`@sveltejs/package` copies `src/lib` to `dist`, compiles TypeScript to `.d.ts` (and preprocesses `<script lang="ts">` into a `.svelte.d.ts` per component), and generates the `exports` map if you let it.

## package.json Rules

```json
{
  "name": "my-lib",
  "type": "module",
  "files": ["dist"],
  "svelte": "./dist/index.js",
  "exports": {
    ".": { "types": "./dist/index.d.ts", "svelte": "./dist/index.js", "default": "./dist/index.js" },
    "./styles.css": "./dist/styles.css"
  },
  "peerDependencies": { "svelte": "^5.0.0" }
}
```

- **`svelte` in `peerDependencies`, never `dependencies`.** A bundled second copy of Svelte means two reactivity systems, and context lookups silently miss across the boundary.
- The `svelte` export condition is what tells a consumer's bundler to compile your `.svelte` files with its own compiler version.
- `files: ["dist"]` keeps your demo app out of the tarball; check with `npm pack --dry-run` before publishing.
- Ship `.svelte` **source**, not precompiled output: the consumer's compiler handles SSR, hydration, dev warnings, and their Svelte version. Precompiling pins them to yours.
- Run `npx publint` and `npx svelte-check` before release — most broken Svelte packages fail on the `exports` map, not on the code.

## API Design That Survives Versions

- Props are your API: name them for the consumer's mental model, give every optional one a default, and accept `...rest` so they can pass `id`, `data-*`, and ARIA attributes through.
- Extend the native element types (`HTMLButtonAttributes`) so a wrapper behaves like the thing it wraps.
- Extension points as **snippets**, not as a dozen boolean props. `{#snippet icon()}` beats `showIcon` + `iconName` + `iconPosition`.
- Data out through callback props (`onselect`), and `$bindable` only where the consumer owns the value (inputs, editors).
- Do not import `$app/*`, `$env/*`, or `$lib/*` in library code: they exist only inside a SvelteKit app and instantly make your package Kit-only. Take a URL or a callback as a prop instead.
- Anything the consumer might need to style: expose CSS custom properties, and accept a `class` prop applied to the root. Scoped styles inside your components are unreachable from theirs by design.
- Breaking changes to watch: renaming a prop, changing a snippet's arguments, tightening a default, and moving a value from prop to context — all of them are major versions even though nothing in your build fails.

## Styles

| Strategy | Consumer does | Cost |
|---|---|---|
| Scoped styles inside components | Nothing | No theming without CSS variables |
| One `styles.css` in `exports` | Imports it once | They must remember; ordering matters |
| CSS custom properties + scoped styles | Sets variables on a wrapper | The best default: themeable, no import |
| Utility classes (Tailwind) in library markup | Must run the same setup | Ties your package to their build |

## Custom Elements

```svelte
<svelte:options customElement="my-widget" />
```

Compiles the component to a real custom element for use in any framework or plain HTML.

- Props become attributes and properties; attributes are strings, so declare types via `customElement: { props: { count: { type: 'Number' } } }`.
- Shadow DOM is on by default, which isolates your styles and blocks the page's — `shadow: 'none'` opts out and gives up encapsulation.
- Slotted content works, snippets do not cross the custom-element boundary.
- Custom elements do not server-render: the element upgrades on the client. Do not use this mode for the library's SvelteKit consumers, only for framework-agnostic distribution.

## Release Checklist

- `npm run package` clean, `dist` contains only `src/lib` output
- `npm pack --dry-run` shows no demo app, no source maps you did not intend
- `publint` and `svelte-check` pass
- `svelte` in peerDependencies, with the widest range you actually support
- No `$app/*` or `$env/*` import anywhere in `dist`
- README documents props, snippets, callback props, and CSS variables — the four surfaces consumers touch
- A consuming app installed from the tarball renders it server-side without a hydration warning
