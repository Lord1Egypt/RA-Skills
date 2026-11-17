# WCAG 2.2 AA checklist with fix patterns

Companion to the main skill. Organized by what you're reviewing. Success criteria in parentheses;
full definitions: https://www.w3.org/WAI/WCAG22/quickref/

## Images and media

- **Informative image** → `alt` describes its function in context, not its appearance.
  A magnifier icon inside a search button: `alt="Search"`, not `alt="magnifying glass"`. (1.1.1)
- **Decorative image** → `alt=""` (empty, present) or CSS background, so screen readers skip it. (1.1.1)
- **SVG icons** → `aria-hidden="true"` when a text label sits beside them; `role="img"` +
  `<title>` when they stand alone. (1.1.1)
- **Video** → captions (1.2.2); prerecorded audio → transcript (1.2.1).
- **Autoplaying audio > 3s** → must be pausable or muteable. (1.4.2)

## Structure and semantics

- Exactly one `<h1>`; heading levels descend without skipping. Style with CSS, never by picking a
  smaller heading tag. (1.3.1)
- Native elements first: `<button>` for actions, `<a href>` for navigation, `<ul>` for lists,
  `<table>` with `<th scope>` for data. A `<div onclick>` needs `role`, `tabindex`, and key
  handlers to equal a free `<button>`. (4.1.2)
- Landmarks: one `<main>`, `<nav>` labelled if there are several
  (`aria-label="Primary"`/`"Footer"`). (1.3.1)
- Reading order in the DOM matches visual order — don't reorder purely with CSS grid/flex `order`
  when the sequence carries meaning. (1.3.2)
- `<html lang="en">` (or the page's language); parts in another language get their own `lang`. (3.1.1, 3.1.2)
- Descriptive, unique `<title>` per page. (2.4.2)

## Forms

- Every control has a programmatic label: `<label for>`, wrapping `<label>`, or `aria-label` as a
  last resort. Placeholder text is not a label. (3.3.2, 1.3.1)
- Errors: identified in text next to the field, associated via `aria-describedby`; never color
  alone. Keep the user's input; say how to fix it. (3.3.1, 3.3.3)
- Autocomplete attributes on common fields (`autocomplete="email"` …). (1.3.5)
- No context change on focus or on input — submitting happens on an explicit action. (3.2.1, 3.2.2)
- Don't ask for the same information twice in one process (2.2.x/3.3.7 — redundant entry).

## Keyboard and focus

- Walk the whole page with Tab / Shift-Tab / Enter / Space / Esc / arrows: everything reachable,
  operable, and leavable. (2.1.1, 2.1.2)
- Tab order follows the visual/logical flow; avoid positive `tabindex`. (2.4.3)
- Visible focus on everything interactive (2.4.7); the focused element must not be fully hidden
  behind sticky headers/footers (2.4.11).
- Skip link as the first focusable element on pages with repeated navigation. (2.4.1)
- Custom widgets (menus, dialogs, tabs) follow the
  [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/patterns/) keyboard contract; dialogs
  trap and restore focus.
- Anything a pointer can drag must have a single-pointer alternative. (2.5.7)

## Color and appearance

- Contrast minimums — see the main skill and run its `scripts/check-contrast.mjs`. (1.4.3, 1.4.11)
- Color is never the only signal: links in prose get underlines; chart series get patterns or
  labels; required fields get a symbol plus text. (1.4.1, 1.4.1 for charts too)
- Content survives 200% zoom and 320px-wide reflow without horizontal scrolling or loss. (1.4.4, 1.4.10)
- Text spacing override-proof: no clipping when users force line-height 1.5 / letter-spacing 0.12em.
  (1.4.12)
- Content that appears on hover/focus (tooltips, previews) is dismissible (Esc), hoverable, and
  persistent. (1.4.13)

## Motion and time

- `prefers-reduced-motion: reduce` disables non-essential animation and parallax.
- Nothing flashes more than 3 times per second. (2.3.1)
- Moving/auto-updating content can be paused, stopped, or hidden. (2.2.2)
- Time limits are adjustable or extendable. (2.2.1)

## Status and dynamic updates

- Async results, toasts, and validation summaries announce via `role="status"` /
  `aria-live="polite"` (assertive only for errors that block). (4.1.3)
- State on controls: `aria-expanded`, `aria-current="page"`, `aria-selected`, `aria-pressed`
  reflect reality and update.

## Testing pass (per release)

1. Run the contrast script over the token pairs (build already does, if wired).
2. Automated sweep: axe DevTools or Lighthouse accessibility — fix everything it can see.
3. Keyboard-only walk-through of the critical flows.
4. Screen-reader pass on those flows: VoiceOver (Safari) or NVDA (Firefox/Chrome) — listen for
   unlabelled buttons, unannounced updates, and focus jumps.
5. Zoom to 200% and a 320px viewport; force text-spacing overrides.

Automated tools catch roughly a third to half of failures. Steps 3–5 are what make the conformance
claim honest.
