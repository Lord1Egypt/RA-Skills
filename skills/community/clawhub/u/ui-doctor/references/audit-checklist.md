# UI Audit Checklist

Go through every category below on every audit, even if the user only reported one symptom in one category — the reported bug is frequently a symptom of a broader pattern repeated elsewhere in the same codebase.

## A. Layout & State Synchronization

- [ ] Any two or more components whose visual state must change together share one source of truth (see `layout-state-sync.md`) rather than independent local state.
- [ ] CSS values that must stay related (sidebar width ↔ content margin, modal z-index ↔ backdrop z-index) are derived from the same token/variable, not two hardcoded values maintained separately.
- [ ] Animations that must appear synchronized use matching duration/easing tokens.
- [ ] No manual re-sync patches (`setTimeout`, forced re-renders, imperative DOM queries to "fix" state after the fact) papering over a duplicated-state root cause.

## B. Responsive Breakpoint Behavior

- [ ] A defined, consistent breakpoint set is used project-wide (not ad hoc `@media` values scattered per component).
- [ ] Layout is verified at each defined breakpoint, not just assumed to "probably work" via `flex-wrap`/`grid` auto-behavior.
- [ ] Content doesn't overflow, get clipped, or become unreachable (e.g. a fixed-position element covering interactive content) at any defined breakpoint.
- [ ] Touch targets remain reachable and appropriately sized on narrow/mobile widths (see WCAG target size below) — not just visually present but shrunk below a tappable size.
- [ ] Text doesn't reflow into unreadable states (e.g. one-word-per-line columns) at intermediate widths between defined breakpoints.

## C. Accessibility (WCAG 2.2 AA baseline)

- [ ] **Focus visibility**: every interactive element has a clearly visible focus indicator (not just a border-radius change or subtle shadow that fails contrast) — WCAG 2.2 SC 2.4.11/2.4.13.
- [ ] **Target size**: interactive targets are at least 24×24 CSS px, or have adequate spacing from adjacent targets — WCAG 2.2 SC 2.5.8.
- [ ] **Disclosure state communicated to assistive tech**: any collapse/expand, accordion, or toggle component sets `aria-expanded` (and `aria-controls` where applicable) and updates it in sync with the actual visual state — this is the accessibility-layer version of the same state-sync bug class in section A.
- [ ] **Color contrast**: text and meaningful UI components meet at least 4.5:1 (normal text) / 3:1 (large text, UI component boundaries) contrast, checked against actual token values, not assumed from the palette's intent.
- [ ] **Error identification**: form errors are communicated both visually and programmatically (`aria-invalid`, associated `aria-describedby` error text), not by color alone.
- [ ] **Reduced motion respected**: `prefers-reduced-motion` is honored at the token/system level (see `design-system-architect`'s motion tokens), not left unhandled.

## D. Performance

- [ ] No unnecessary re-render storms: check for unmemoized callbacks/objects passed as props to components wrapped in `memo`/`PureComponent`-equivalents, which silently defeats the memoization.
- [ ] Large dependencies (icon libraries, date libraries, chart libraries) are imported per-icon/per-function, not as a full-library import, to avoid bundle bloat.
- [ ] Layout-triggering state (things that cause reflow, like measuring an element's size) isn't recalculated more often than necessary — check for measurement/reflow work happening on every render instead of only when relevant inputs change.
- [ ] Code splitting/lazy loading is used for heavy, non-critical-path UI (modals, rarely-used panels, large editors) rather than bundled into the initial load.
- [ ] Images/media use appropriate sizing/formats (no full-resolution images displayed at thumbnail size).

## E. Consistency

- [ ] Spacing/color/radius/shadow values trace back to defined tokens (see `design-system-architect` if present) rather than one-off hardcoded values introduced during implementation.
- [ ] The same interactive pattern (e.g. how a dropdown opens, how a destructive action is confirmed) behaves the same way everywhere it appears, not slightly differently per screen.
- [ ] Loading, error, and empty states exist and look intentional for every data-driven component — not just the happy path.
