# Responsive — Breakpoints, Ranges, And Container Queries

Tailwind is mobile-first and that is not a style preference: it changes what every unprefixed utility means.

## The Mobile-First Contract

- Unprefixed applies at **every** width. `md:` applies at ≥768px and everything above.
- "Only at medium" needs two utilities: `md:flex lg:hidden` = 768–1023px.
- Or one upper-bound variant: `max-lg:flex` = below 1024px. Available in both majors.
- Combine both for a closed range in one place: `md:max-lg:flex`.
- Design the smallest layout first, then add prefixes that *add*. Writing the desktop layout unprefixed and overriding it with `sm:`-prefixed resets means every mobile page loads desktop styles first and undoes them.

Scale (identical in v3 and v4): sm 640px/40rem · md 768/48 · lg 1024/64 · xl 1280/80 · 2xl 1536/96. `rem_base` never moves a breakpoint — a media query resolves rem against the browser's initial 16px, whatever `html { font-size }` says. Full numeric table: SKILL.md — Utility Scale Math.

## Custom Breakpoints

```css
/* v4 — sorts by value automatically */
@theme {
  --breakpoint-xs: 30rem;
  --breakpoint-3xl: 120rem;
}
```

```js
// v3 — extend keeps the defaults; declaration order matters
theme: { extend: { screens: { xs: '480px', '3xl': '1920px' } } }
```

- v3 `screens` at the top level (not under `extend`) deletes the default breakpoints; every existing `md:` in the codebase stops working.
- v3 sorts by declaration order, so an `xs` added at the end of the object emits after `2xl` and loses the mobile-first cascade. v4 sorts by value and is immune.
- A one-off threshold does not need a breakpoint: `min-[900px]:grid-cols-3`.
- Removing a default: `--breakpoint-2xl: initial;` in v4.

## Choosing Breakpoints

- Break where the *content* breaks, not at device names. Resize until the layout looks wrong; that width is the breakpoint. Device-derived breakpoints age with the device catalogue.
- Three is usually enough for a page: one-column, two-column, wide. A component that needs five is a component that should be using container queries.
- Test at the boundaries (767/768, 1023/1024), not in the middle of each range — off-by-one prefixes only show there.
- `2xl:` exists but most designs cap the content width instead (`max-w-7xl mx-auto`) and let the page breathe.

## Container Queries — Component-Level Responsiveness

Use when the same component renders at different widths (sidebar vs main, card grid vs list). The viewport is the wrong signal there.

```html
<div class="@container">
  <article class="flex flex-col @md:flex-row @lg:gap-8">…</article>
</div>
```

- Core in v4; the `@tailwindcss/container-queries` plugin in v3.
- Sizes come from the `--container-*` scale, deliberately smaller than viewport breakpoints: `@xs` 20rem · `@sm` 24 · `@md` 28 · `@lg` 32 · `@xl` 36 · `@2xl` 42.
- Named containers when they nest: `@container/sidebar` then `@md/sidebar:flex-row`. Unnamed queries bind to the nearest `@container` ancestor.
- Upper bound with `@max-md:`, one-off sizes with `@min-[400px]:`.
- A container query cannot depend on the element it sizes: the `@container` must be an ancestor of the queried element, not the element itself.
- Container-query units (`cqw`, `cqi`) work in arbitrary values: `text-[clamp(1rem,4cqi,2rem)]`.

## Intrinsic Sizing Beats Breakpoints

Many layouts need no media query at all — fewer breakpoints means fewer states to test:

- `grid-cols-[repeat(auto-fit,minmax(min(16rem,100%),1fr))]` — a card grid that reflows on its own.
- `flex flex-wrap gap-4` — toolbars and tag lists that wrap when they must.
- `w-full max-w-md` — full width on small screens, capped above, one class pair.
- `text-[clamp(1.5rem,1rem+2.5vw,3rem)]` — fluid type; keep a rem term in the clamp or browser zoom and user font-size stop working.

## Mobile Viewport Units

- `h-dvh` tracks the browser chrome collapsing on scroll; `h-svh` uses the smallest stable height (no jump, some empty space); `h-lvh` the largest.
- `100vh` on mobile means the *largest* viewport, so a `h-screen` hero is taller than the visible area on first paint.
- `w-screen` includes the scrollbar width and causes horizontal overflow on desktop — `w-full` or `w-dvw`.
- `min-h-dvh` on the page shell rather than `h-dvh`, so content longer than the viewport still scrolls.

## Checks

- Read the page at 320px wide: content reflows without horizontal scroll (WCAG 1.4.10).
- Zoom to 200%: text-based sizes survive because they are rem, not vw.
- Every `hidden md:block` pair audited — content hidden on mobile is content mobile users never get, and screen readers still announce it unless it is truly removed.
- Boundary widths tested on both sides of each breakpoint.
- Landscape phone (short viewport): `h-dvh` sections with vertical centering are the usual casualty.

