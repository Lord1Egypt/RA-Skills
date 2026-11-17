# Accessibility & Performance — Production Floor

Walk this before presenting any UI as finished. These are not "nice to have" — a UI that fails these is a prototype, not production software. Sources: WCAG 2.2 (w3.org/WAI/WCAG22/quickref), web.dev Core Web Vitals guidance.

## Keyboard and focus

- [ ] Every interactive element (button, link, input, custom control) is reachable via Tab in a logical order
- [ ] Focus is **visibly** indicated — use `focus-visible:` variants, not just `:hover` styling reused for focus. shadcn/ui components handle this by default via Radix; don't strip it when customizing
- [ ] Modals/dialogs trap focus while open and return focus to the trigger element on close (Radix-based `Dialog`/`Sheet` do this automatically — verify if you built a custom overlay instead)
- [ ] No keyboard traps: Escape closes overlays, Tab cycles predictably

## Color and contrast

- [ ] Body text vs. background: 4.5:1 minimum
- [ ] Large text (≥24px, or ≥19px bold) and meaningful icons: 3:1 minimum
- [ ] Color is never the *only* signal for state (error fields also get an icon/text, not just a red border; status also has a label, not just a colored dot)
- [ ] Check disabled and placeholder text specifically — these are the most common contrast failures because "muted" often gets pushed too light

## Responsive behavior

- [ ] Tested at real breakpoints: ~360px (small phone), ~768px (tablet), ~1024px+ (desktop) — not just a resized browser window
- [ ] No horizontal scroll at any width unless intentional (e.g. a data table with a deliberate scroll container)
- [ ] Touch targets ≥44×44px on mobile for anything tappable
- [ ] Text reflows rather than truncating important content — truncate secondary metadata, not primary content, and always provide the full value via `title` or a tooltip when truncating

## States beyond the happy path

- [ ] **Loading**: skeleton or spinner designed, not a blank region (shadcn `Skeleton` component)
- [ ] **Empty**: a real empty state with guidance on the next action, not an empty `<div>` or a stray "No data"
- [ ] **Error**: specific, actionable error messaging in the interface's voice ("Couldn't save changes — check your connection and try again," not "Error" or a raw stack trace)
- [ ] **Long content**: names, emails, and labels tested with realistically long real-world values, not just short seed data

## Motion

- [ ] Any animation respects `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

- [ ] Motion serves a purpose (state change feedback, spatial continuity) rather than being decorative on every interaction

## Semantic HTML and ARIA

- [ ] Headings form a real hierarchy (`h1` → `h2` → `h3`, no skipped levels for style reasons)
- [ ] Buttons are `<button>`, links are `<a>` — don't build clickable `<div>`s for anything that should be one or the other
- [ ] Form inputs have associated `<label>` elements (shadcn `Form` + `Label` handle this if wired correctly — check that `htmlFor`/`id` actually match)
- [ ] Images have meaningful `alt` text, or `alt=""` if purely decorative
- [ ] Custom components built without a shadcn/Radix primitive get correct ARIA roles/states manually — verify against the ARIA Authoring Practices Guide for that pattern

## Performance / Core Web Vitals baseline

- [ ] No layout shift from images: explicit `width`/`height` (or `aspect-ratio`) on every image, `next/image` used in Next.js projects
- [ ] Web fonts don't cause an invisible-text flash — `font-display: swap` or Next.js `next/font` (which self-hosts and inlines font-loading strategy automatically)
- [ ] Large client-side JS is code-split (dynamic import) for anything not needed on initial paint (heavy charts, rich text editors, modals with large dependencies)
- [ ] Images are served in a modern format (WebP/AVIF) and sized appropriately for their rendered dimensions, not full-resolution originals shrunk by CSS

## Final pass

Before calling a UI done, actually tab through it with no mouse, squint at it at 360px width, and read every error/empty state out loud. If any of those feels unfinished, it is.
