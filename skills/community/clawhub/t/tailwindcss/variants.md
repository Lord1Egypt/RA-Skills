# Variants — State, Relations, And Custom Conditions

A variant is a selector wrapper. Every "it won't fire" bug is the generated selector not matching the DOM you have.

## The Relational Variants

| Variant | Generated relationship | Requirement |
|---|---|---|
| `group-hover:` | `.group:hover &` | The literal class `group` on an **ancestor** |
| `peer-checked:` | `.peer:checked ~ &` | The peer is a **preceding sibling** — the combinator only looks forward |
| `has-[a]:` | `&:has(a)` | The condition element is a **descendant** |
| `group-has-[img]:` | `.group:has(img) &` | Condition anywhere inside the marked ancestor |
| `*:` | `& > *` | Styles direct children from the parent |
| `**:` | `& *` | All descendants (v4); expensive on large subtrees |

```html
<!-- Named groups when they nest, or the inner group hijacks the outer -->
<li class="group/row">
  <div class="group/actions">
    <button class="opacity-0 group-hover/row:opacity-100 group-hover/actions:text-brand-500">…</button>
  </div>
</li>
```

- Unnamed `group-hover:` binds to the **nearest** `group` ancestor. Nesting two groups without names is the classic relational bug.
- `peer` cannot reach backwards. A label before its input uses `peer` on the input and `peer-checked:` on a *following* label; a label that must precede the input needs `has-[:checked]` on a shared parent instead.
- `has-[…]` replaces most of the JS that used to mirror child state into a parent class.

## Attribute And ARIA Variants

```html
<div data-[state=open]:rotate-180 aria-[sort=ascending]:font-bold>
<button class="aria-expanded:bg-gray-100" aria-expanded="false">
<div class="data-loading:animate-pulse" data-loading>          <!-- boolean form, v4 -->
```

- Headless UI, Radix, and most unstyled component kits expose state as `data-state`, `data-side`, `data-disabled` — style those instead of mirroring state into React props.
- The attribute must be on the **same element** as the utility unless prefixed with `group-`/`peer-`: `group-data-[state=open]:opacity-100`.
- Prefer `aria-*` variants when the attribute is already there for accessibility; you get the styling free and cannot drift out of sync.

## Structural, Media, And Feature Variants

- Position: `first:`, `last:`, `only:`, `odd:`, `even:`, `nth-3:`, `nth-last-2:`, `empty:`.
- Pseudo-elements: `before:`, `after:` (Tailwind injects `content: ""` automatically — `content-['']` is only needed for a real value), `placeholder:`, `selection:`, `marker:`, `file:`, `backdrop:`, `first-letter:`.
- Media and environment: `motion-reduce:`, `motion-safe:`, `print:`, `forced-colors:`, `contrast-more:`, `portrait:`, `landscape:`, `pointer-coarse:`, `noscript:`.
- Direction: `rtl:`, `ltr:` — both need a `dir` attribute in the tree. Logical utilities (`ms-*`, `pe-*`, `text-start`, `border-s`) are better: they mirror with no variant at all. `text_direction` other than `ltr` makes the logical forms the default in every emitted example; reserve `rtl:` for the cases logical properties cannot express, such as a mirrored icon or a directional shadow.
- Support tests: `supports-[display:grid]:`, `not-supports-[…]:`.
- Negation: `not-hover:`, `not-first:` — wraps the selector in `:not()`, useful for "everything except" without redefining the base.
- Enter/exit: `starting:` pairs with `transition-discrete` for animating from `display: none`.

## Arbitrary And Custom Variants

```html
<!-- One-off selector, inline -->
<div class="[&>*+*]:mt-4 [&_a]:underline [@media(hover:hover)]:hover:bg-gray-100">
```

```css
/* Reusable — v4 */
@custom-variant sidebar-open (&:where([data-sidebar=open] *));
@custom-variant theme-acme (&:where([data-brand=acme] *));
```

```js
// v3
plugin(({ addVariant }) => {
  addVariant('sidebar-open', '[data-sidebar="open"] &');
});
```

- `&` is where the element's own selector lands. Forgetting it produces a rule that matches nothing and no error.
- Wrap the condition in `:where()` to keep specificity at zero — otherwise the custom variant starts beating plain utilities and reintroduces the specificity wars Tailwind exists to end.
- Promote an arbitrary variant to a custom variant at `token_threshold` uses (default 3). Before that the inline form is more readable than a name nobody remembers.

## Stacking Order

Variants apply outside-in, left to right: `dark:md:hover:bg-gray-700` = in dark mode, at ≥768px, on hover. For state combinations the order is irrelevant to the result; for pseudo-elements and relational variants it is not:

- `before:hover:` — hover on the pseudo-element (rarely what you mean).
- `hover:before:` — the pseudo-element while the parent is hovered (usually what you mean).
- `*:first:` vs `first:*:` — the first child's children vs the children of the first child.

When a stacked variant misbehaves, read the generated selector in devtools before rewriting it; the selector says exactly which nesting you got.

## Diagnosis

| Symptom | Cause |
|---|---|
| `group-hover:` fires on the wrong row | Nested groups, unnamed (→ named groups above) |
| `peer-*` never fires | Peer is after the target in the DOM |
| `hover:` dead on mobile | Touch has no hover; add `active:` and `focus-visible:` |
| Custom variant produces no CSS | Missing `&`, or defined after the CSS was last built |
| Variant works in dev, not in production | The class string is dynamic (SKILL.md — Class Detection) |
| `data-[state=open]:` never matches | Attribute is on the parent — prefix with `group-` |
| Variant applies but loses | Another utility sorts later, or unlayered CSS wins (SKILL.md — Cascade And Conflicts) |
| Anything else | Copy the generated selector from devtools and test it in `document.querySelectorAll` |

