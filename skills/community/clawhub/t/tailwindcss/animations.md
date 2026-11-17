# Animations And Transitions

Four built-in animations, a transition system, and a set of traps that only appear on the second state change.

## Transitions

- `transition` alone covers the properties you usually animate (color, background, border, opacity, shadow, transform, filter) — not `height`, `width`, or `top`.
- Narrow it when you mean one thing: `transition-colors`, `transition-transform`, `transition-opacity`. `transition-all` animates properties added later, including layout ones, and turns a theme swap into a visible sweep.
- Defaults: `duration-150`, `ease-in-out` (`transition` sets both). Override with `duration-200 ease-out`.
- Duration is in milliseconds and arbitrary values work: `duration-[240ms]`.
- Frame budget: 60fps leaves ~16.7ms per frame for style, layout, paint, and your JS combined. Only `transform` and `opacity` skip layout and paint, which is why every other animated property risks jank on a mid-range phone.
- A transition needs two states. `transition` on an element whose class never changes is dead weight in the class list.

## Built-In Animations

`animate-spin` · `animate-ping` · `animate-pulse` · `animate-bounce` · `animate-none` to cancel one inherited from a parent's class list.

- `animate-pulse` on skeletons is the default loading affordance; `animate-spin` on an SVG spinner wants `motion-reduce:animate-none` beside it.
- `animate-bounce` uses a non-standard easing curve tuned for attention, not physics — fine for a scroll hint, wrong for UI feedback.

## Custom Keyframes

```css
/* v4 — token plus keyframes in the same stylesheet */
@theme {
  --animate-slide-up: slide-up 0.3s ease-out;
}
@keyframes slide-up {
  from { opacity: 0; transform: translateY(0.5rem); }
  to   { opacity: 1; transform: translateY(0); }
}
```

```js
// v3
theme: { extend: {
  keyframes: { 'slide-up': { from: { opacity: 0, transform: 'translateY(8px)' },
                             to:   { opacity: 1, transform: 'translateY(0)' } } },
  animation: { 'slide-up': 'slide-up 0.3s ease-out' },
} }
```

- The `--animate-*` token produces `animate-slide-up`; the `@keyframes` block must exist in CSS that ships (a keyframes rule in a file nothing imports generates a class that animates nothing).
- Animate `transform` and `opacity` only. `from { height: 0 }` runs layout on every frame.
- Custom easing lives in `--ease-*` tokens: `--ease-snap: cubic-bezier(0.2, 0, 0, 1)` → `ease-snap`.

## Enter And Exit Animations

The hard case: animating an element that is being added to or removed from the DOM.

```html
<!-- v4: transition from display:none without JS -->
<div popover class="opacity-0 transition-all transition-discrete
                    open:opacity-100 starting:open:opacity-0">
```

- `transition-discrete` allows discrete properties (`display`, `overlay`) to participate; `starting:` supplies the `@starting-style` origin. Without the starting state, the element appears at its final values and nothing animates.
- Exit animations need the element to stay mounted for the duration — that is a framework concern (React transition libraries, Vue `<Transition>`, Svelte `transition:`), not something classes can solve.
- Headless kits expose `data-state="open"`/`"closed"` for exactly this: `data-[state=open]:animate-in data-[state=closed]:animate-out` with a library that provides those utilities, or your own keyframe tokens.
- Height-to-auto is not animatable directly. The grid trick — `grid-rows-[0fr]` → `grid-rows-[1fr]` with an `overflow-hidden` child — animates cleanly and needs no measurement.

## Reduced Motion

- `motion-reduce:` and `motion-safe:` map to `prefers-reduced-motion`. Prefer the opt-in direction: write the animation under `motion-safe:` so the default is calm, rather than adding overrides after the fact.
- Vestibular triggers are large-area movement, parallax, and zoom — not fades. A reduced-motion path that replaces a slide with a fade is usually better than removing the transition entirely, because the state change still reads.
- Infinite animations (`animate-spin`, `animate-pulse`) need an explicit `motion-reduce:animate-none`; a loading spinner that never stops is the exact case the setting exists for.

## Performance

- `will-change-transform` only on elements actually animating, and only while they animate. Every promoted layer holds GPU memory; a list where every row is promoted is slower than one that isn't.
- Animating many elements at once: stagger with `delay-*` rather than starting fifty transitions in the same frame.
- `backdrop-blur` is expensive per frame; animating alongside it drops frames on integrated GPUs. Fade the backdrop in, then apply the blur at rest.
- Long lists: animate the container, not every child.

## Checks

- Reduced motion enabled: nothing spins, nothing slides more than a fade.
- Only `transform`/`opacity` in any loop or hover transition.
- Every `transition` on an element whose classes actually change.
- Exit animation tested by removing the element, not just adding it.
- Animation still readable at 200% zoom and on a 320px viewport.

