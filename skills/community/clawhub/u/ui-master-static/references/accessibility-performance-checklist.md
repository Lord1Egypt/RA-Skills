# Accessibility & Performance — Production Floor (Native CSS)

Walk this before presenting any UI as finished. Without a framework catching mistakes, these are entirely on the CSS/markup you write. Sources: WCAG 2.2 (w3.org/WAI/WCAG22/quickref), web.dev Core Web Vitals guidance.

## Keyboard and focus

- [ ] Every interactive element is reachable via Tab in a logical order (DOM order matches visual order, or `tabindex` is used deliberately, never as a way to "fix" a bad DOM order)
- [ ] Focus is visibly indicated with `:focus-visible` (not `:focus`, which also fires on mouse click and creates a distracting outline for mouse users) — never `outline: none` without a replacement indicator
- [ ] Custom interactive elements (a `<div>` acting as a button, a custom dropdown) have the correct `role`, `tabindex="0"`, and keyboard handlers (`Enter`/`Space` to activate) — or better, use the native `<button>`/`<select>`/`<details>` instead, which get this for free
- [ ] Modals/custom overlays trap focus while open and restore it to the trigger on close — this must be hand-built in native CSS/JS since there's no Radix-equivalent doing it automatically

## Color and contrast

- [ ] Body text vs. background: 4.5:1 minimum; large text/icons: 3:1 minimum
- [ ] Color is never the only signal for state — pair with an icon, label, or pattern
- [ ] Glassmorphism and gradient-over-image text is checked for contrast specifically — translucent panels are a common place for text to silently fall below 4.5:1 against a busy background

## Responsive behavior

- [ ] Tested at ~360px, ~768px, ~1024px+ — real breakpoints, not just a resized browser window
- [ ] `clamp()`-based fluid type tested at its floor and ceiling, not just mid-viewport
- [ ] Touch targets ≥44×44px on mobile
- [ ] Container-query components tested in every context width they'll actually appear in (full page vs. sidebar-adjacent), not just one

## States beyond the happy path

- [ ] Loading, empty, and error states are designed, not left as a blank region
- [ ] Error messaging is specific and actionable, written in the interface's voice
- [ ] Long real-world content (names, labels) tested, not just short seed data

## Motion

- [ ] `prefers-reduced-motion: reduce` is respected globally, not just on the one animation you remembered:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

- [ ] Scroll-driven animations, parallax, and 3D tilt effects specifically re-checked against this — they're the highest-risk category (see `references/modern-effects.md`)

## Semantic HTML and ARIA

- [ ] Real heading hierarchy (`h1`→`h2`→`h3`, no skipped levels for visual-size reasons — use CSS to resize a heading rather than picking the wrong tag)
- [ ] Buttons are `<button>`, links are `<a href>` — never a styled `<div onclick>`
- [ ] Every form input has an associated `<label>` (via `for`/`id`, or wrapping)
- [ ] Images have meaningful `alt`, or `alt=""` for decorative ones
- [ ] Landmark elements used correctly (`<header>`, `<nav>`, `<main>`, `<footer>`) — one `<main>` per page

## Performance / Core Web Vitals baseline

- [ ] No layout shift: explicit `width`/`height` or `aspect-ratio` on every image, dimensions reserved for anything that loads asynchronously
- [ ] Web fonts use `font-display: swap` (or are self-hosted with `@font-face` + `swap`) to avoid invisible-text flash
- [ ] `backdrop-filter` and heavy `box-shadow` usage is bounded — profile with browser dev tools if used across many elements in a scrollable list, since each is a separate compositing cost
- [ ] `will-change` used sparingly and only on elements that are actually about to animate — leaving it on permanently forces the browser to keep an expensive compositing layer alive for no benefit
- [ ] CSS file split by the architecture in `css-architecture-bem.md` so unused component styles aren't all loaded/parsed on every page in a multi-page static site

## Final pass

Tab through the UI with no mouse. Toggle `prefers-reduced-motion` in dev tools and confirm nothing breaks or disappears. Squint at it at 360px. If a Houdini or scroll-timeline effect is present, test in a non-Chromium browser (or emulate via dev tools) to confirm the fallback actually looks intentional.
