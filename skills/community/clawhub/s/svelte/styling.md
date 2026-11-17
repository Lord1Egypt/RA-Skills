# Styling, Transitions, and Motion

## How Scoping Actually Works

Svelte hashes a class (`svelte-1a2b3c`) onto the elements a selector can match **in this component's own markup**, then adds it to the selector. Two consequences explain nearly every styling surprise:

1. **A selector that matches nothing here is deleted** with a `css_unused_selector` warning — including selectors that only match markup rendered by a child component, injected by `{@html}`, or created imperatively by a library.
2. **Child component internals are out of reach.** `.card p { }` in the parent does not reach the `<p>` inside `<Card />` because that `<p>` never got the parent's hash.

Fixes, in order of preference:

| Situation | Fix |
|---|---|
| Style a child's root element | Pass a `class` prop and apply it in the child on the root node |
| Style deep inside a child | `:global(.card p)` in the parent, or better, expose CSS custom properties from the child |
| Style `{@html}` output | Wrap it: `.prose :global(p) { }` |
| Theme a whole subtree | CSS custom properties on a wrapper — they inherit through component boundaries |
| Library-generated DOM (datepicker, editor) | `:global()` scoped under a wrapper class, or the library's own theme file in `app.css` |
| Keyframes used by a global selector | Name them `-global-fadein` |

`:global { … }` as a block applies to everything inside it, which is easier to read than repeating `:global()` on each selector.

## Class and Style Directives

- `class={['btn', { active: isActive, 'btn-lg': size === 'lg' }]}` — arrays and objects are supported directly (`svelte >=5.16`), no clsx import.
- `style:color={c}` and `style:--brand={brand}` set individual properties without string concatenation, and win over a `style` attribute.
- `<Comp --accent="tomato" />` passes a CSS variable into a component by wrapping it in an element with `display: contents`. That wrapper is real DOM: it breaks direct `>` child selectors and flex/grid parent-child relationships. Prefer a plain prop plus `style:` when layout matters.
- Global stylesheet: import `app.css` in the root layout. Everything there is unscoped by definition; keep it to resets, fonts, tokens.

## Transitions

```svelte
{#if visible}
  <div transition:fade={{ duration: 200 }}>…</div>
{/if}
```

- `transition:` is bidirectional; `in:` and `out:` are one-way and can differ. Put the directive on the element **inside** the `{#if}`, not on a wrapper — the wrapper is never added or removed, so nothing animates.
- **Transitions are local by default in Svelte 5**: a transition plays when its own block toggles, not when an ancestor block does. Add `|global` to play on ancestor changes too (the Svelte 4 default was the opposite — a classic migration surprise).
- Built-ins from `svelte/transition`: `fade`, `fly`, `slide`, `scale`, `blur`, `draw`, plus `crossfade` for send/receive pairs between lists.
- A custom transition returning a `css` function is compiled to a Web Animation and runs off the main thread; one returning `tick` runs JavaScript on every frame. Use `tick` only for things CSS cannot express (text scrambling, canvas), and never on a list of many nodes.
- `animate:flip` (from `svelte/animate`) moves surviving items when a **keyed** `{#each}` reorders. Unkeyed lists cannot animate reorders at all.
- Events: `onintrostart`, `onintroend`, `onoutrostart`, `onoutroend` for sequencing work around a transition.
- `{#key value}` around a block replays its transition when the value changes — the standard route-change fade.

## Motion Values

```js
import { Tween, Spring } from 'svelte/motion';

const progress = new Tween(0, { duration: 400, easing: cubicOut });
const pointer = new Spring({ x: 0, y: 0 }, { stiffness: 0.1, damping: 0.4 });

progress.target = 1;        // animates
progress.current;           // read in markup
Spring.of(() => value);     // follow a reactive source
```

`Tween` and `Spring` classes (`svelte >=5.8`) replace the `tweened` and `spring` stores; use them for values that should animate continuously (gauges, drag handles, physics), and CSS transitions for discrete state changes.

## Reduced Motion

```svelte
<script>
  import { MediaQuery } from 'svelte/reactivity';
  const reduced = new MediaQuery('prefers-reduced-motion: reduce');
</script>

<div transition:fade={{ duration: reduced.current ? 0 : 200 }}>…</div>
```

Duration zero, not "no transition": keeping the directive preserves the enter/leave logic while removing the motion. Apply the same rule to `Tween` durations and to any `animate:flip`.

## Tailwind and Utility CSS

- Install through `npx sv add tailwindcss` — it wires the Vite plugin and the stylesheet import correctly.
- Utility classes are global; the scoping rules above stop applying, and `class` props become the whole component API. Keep one convention per project (`styling` in the Configuration table).
- `{@html}` content still needs a typography plugin or explicit `:global` rules — utilities cannot reach markup that does not exist in your source.
- Conditional utilities: the array/object `class` form above, not string templates that Tailwind's scanner cannot see.

## Styling Checklist

- Component styles scoped, with `:global` used deliberately and scoped under a wrapper
- Child components styled through a `class` prop or CSS variables, never by reaching in
- Transitions on the conditional element, `|global` only where an ancestor toggle should animate
- Keyed `{#each}` wherever `animate:flip` is used
- Reduced-motion path checked for every `transition:`/`in:`/`out:`, every `Tween` and `Spring`, and every `animate:flip` in the component
