# Layout And Spacing In Utilities

Tailwind's layout utilities encode opinions that plain CSS does not. These are the places where the utility behaves differently from the property you think you wrote. For the underlying mechanics — stacking contexts, flex sizing, margin collapse — use the `css` skill.

## Spacing Between Children

- `gap-*` is the default. It works in flex and grid, never collapses, and survives wrapping and reordering.
- `space-x-4` / `space-y-4` apply a margin to all-but-one child via a sibling selector. Consequences: it breaks on a wrapping row (the wrapped item gets no top margin), inverts under `flex-row-reverse`, and fights any child that sets its own margin.
- `divide-x` / `divide-y` use the same selector to draw borders between children — same wrapping caveat, plus it conflicts with `space-*` on the same element.
- Reach for `space-*` only when gap is unavailable: a non-flex, non-grid block container where you want rhythm between arbitrary children (`[&>*+*]:mt-4` does the same with clearer intent).

## Sizing

- `size-8` sets width and height together — half the length of most icon and avatar class lists.
- `w-screen` is `100vw`, which **includes the scrollbar** and causes horizontal overflow on desktop. Full-bleed uses `w-full` on a full-width parent, or `w-dvw`.
- `h-screen` is `100vh` and ignores mobile browser chrome that collapses on scroll. `h-dvh` tracks it; `h-svh` uses the smallest stable height when live resizing would be jumpy.
- `min-h-screen` on the page shell plus `flex-1` on the main region is the sticky-footer layout; `h-screen` on a scrolling page clips content instead.
- `max-w-*` comes from the container scale, not the breakpoint scale: `max-w-sm` = 24rem, `sm:` = 40rem (SKILL.md — Utility Scale Math).
- `max-w-prose` = 65ch, the readable-measure default; a text column wider than that is a recurring typographic defect in a Tailwind marketing page.

## Flex And Grid Specifics

- `grid-cols-2` compiles to `repeat(2, minmax(0, 1fr))`, so Tailwind already dodges the raw-CSS `1fr` overflow trap. Writing `grid-cols-[1fr_1fr]` by hand reintroduces it.
- Responsive card grid without breakpoints: `grid-cols-[repeat(auto-fit,minmax(min(16rem,100%),1fr))]` — the inner `min()` stops overflow below 16rem.
- `flex-1` is `1 1 0%` (all space split evenly); `flex-auto` is `1 1 auto` (only leftover space split, larger content keeps a larger track). Equal columns need `flex-1`.
- A flex child defaults to `min-width: min-content`: add `min-w-0` before expecting `truncate`, `overflow-hidden`, or shrinking to work. Column direction needs `min-h-0`.
- `items-center` can push content out of a scroll container's top; `items-center-safe` (v4) falls back to `start` when the content overflows.
- `order-*` changes paint order, never DOM order — keyboard and screen-reader order stay as written. Reordering visually past a couple of positions is an accessibility defect.

## Text Overflow

- `truncate` = `overflow:hidden; text-overflow:ellipsis; white-space:nowrap` and needs a resolvable width: a `max-w-*`, a grid track, or `min-w-0` inside flex.
- `line-clamp-3` handles multiple lines and needs no width constraint, but hides overflow in the block direction — a container with `overflow-visible` elsewhere will fight it.
- `break-words` for long words, `wrap-break-word`/`break-all` for URLs and hashes, `hyphens-auto` needs a `lang` attribute to do anything.
- `text-balance` on headings, `text-pretty` on body — both no-ops on very long text by design, so applying them broadly is safe.

## Positioning And Overflow

- `rounded-*` on a parent with absolutely positioned or image children needs `overflow-hidden`, or the child paints over the corner.
- `overflow-hidden` creates a scroll container: it breaks `sticky` descendants and clips focus rings and shadows. When the goal is only to stop horizontal scroll, `overflow-x-clip` creates no scroll container and sticky survives.
- `sticky top-0` does nothing if any ancestor has `overflow-hidden`, or if the element has no positioned space to move within.
- Tailwind's `z-*` scale stops at 50 by design. Needing `z-[9999]` means the element is trapped in a stacking context — diagnose with the `css` skill rather than escalating.
- `inset-0` + `absolute` + `m-auto` centers an element with an intrinsic size; `grid place-content-center` is the default for everything else.
- `isolate` on a component root caps its internal z-index so it cannot leak into the page.

## The Container Utility

- v3: `container` sets a max-width per breakpoint, is **not centered by default**, and takes `center`/`padding` options in the config.
- v4: those options are gone. Recreate them as a utility:

```css
@utility container {
  margin-inline: auto;
  padding-inline: 1.5rem;
}
```

- Modern alternative that needs no utility at all: `mx-auto max-w-7xl px-6` — explicit, greppable, and it doesn't jump at each breakpoint.

- Do not confuse `container` (a max-width utility) with `@container` (a container-query context) — different features, adjacent names.

