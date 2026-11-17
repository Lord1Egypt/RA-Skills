# Accessibility In Tailwind

Utilities make accessibility failures fast to write. These are the ones a Tailwind codebase produces specifically, and the utilities that fix them.

## Focus

- `focus:outline-none` with nothing after it is the classic Tailwind a11y regression: it removes the only affordance keyboard users have and passes every visual review.
- v4 separates two things: `outline-hidden` hides the outline but keeps it visible under Windows High Contrast / forced-colors mode; `outline-none` sets `outline-style: none` and removes it everywhere. Use `outline-hidden` when replacing the ring, `outline-none` almost never.
- The canonical replacement (SKILL.md rule 8): `focus-visible:outline-hidden focus-visible:ring-2 focus-visible:ring-offset-2`. Add a ring color when the inherited `currentColor` is wrong for the surface — `focus-visible:ring-brand-500`.
- `focus-visible:` on **both** halves, never `focus:` — a `focus:` prefix strips the native outline on mouse click too, so a button shows a ring after every click and the keyboard user's affordance is the only thing you were trying to keep.
- `ring-offset-*` paints the page background between element and ring. A fixed offset color goes invisible in the other theme: `ring-offset-white dark:ring-offset-gray-900`.
- Focus must reach every interactive element: a `<div onClick>` gets no focus and no keyboard activation regardless of styling. Use a real `button`/`a`.

## Contrast

Floor: **4.5:1** for body text, **3:1** for large text (≥24px, or ≥18.66px bold) and for UI components and focus indicators (WCAG 2.2 AA, 1.4.3 / 1.4.11). AAA raises body to 7:1 — `a11y_target: aaa` selects it.

Against white, in the default palette:

| Class | Approx. ratio | Verdict |
|---|---|---|
| `text-gray-400` | ≈2.5:1 | Fails everything |
| `text-gray-500` | ≈4.8:1 | Lightest gray that passes AA body text |
| `text-gray-600` | ≈7.6:1 | Passes AAA body text |

- `text-gray-400` on white is the default "muted text" instinct and it fails. Muted text is `text-gray-500`, or `text-gray-600` when the design must be safe in both themes.
- Placeholders inherit the same problem — the `forms` plugin sets a light gray, and a placeholder is text.
- The 500 shade of the colorful ramps (`bg-blue-500`, `bg-green-500`) does **not** reliably carry white text: `text-white` on `bg-yellow-500` or `bg-lime-500` fails badly. Check each brand pairing rather than assuming the shade number implies contrast.
- v4's palette is defined in OKLCH and renders wide-gamut on P3 displays, so re-measure brand pairings after the upgrade rather than trusting v3 audits.
- Disabled states (`disabled:opacity-50`) legitimately drop below the floor; disabled controls are exempt (1.4.3), but the text explaining *why* it is disabled is not.

## Target Size

- `size-6` = 24px = AA minimum (2.5.8). `size-11` = 44px = AAA and Apple HIG.
- A 16px icon in a 24px box passes; the same icon with `p-0` does not. Pad to the target rather than growing the glyph: `p-2.5` around a `size-6` icon gives 44px.
- Adjacent small targets need spacing as well as size — `gap-2` between icon buttons prevents mis-taps that size alone doesn't.

## Hiding Things — Five Different Meanings

| Utility | Effect | Use for |
|---|---|---|
| `hidden` | `display: none` — gone from the accessibility tree | Content nobody should reach in this state |
| `invisible` | Occupies space, unreachable | Layout placeholders |
| `sr-only` | Visually gone, still announced and still focusable | Labels, skip links, live-region text |
| `not-sr-only` | Reverses it at a breakpoint or on focus | `sr-only focus:not-sr-only` — the skip link pattern |
| `aria-hidden` (attribute) | Visible, not announced | Decorative icons beside a text label |

`hidden md:block` is a content decision, not a layout one: mobile users never receive that content. `opacity-0` is worse than all of these — invisible, still focusable, still announced.

## Motion, Colors, And System Preferences

- `motion-reduce:` / `motion-safe:` — an infinite animation needs an explicit off switch: `motion-reduce:animate-none` beside every `animate-spin` and `animate-pulse`.
- `forced-colors:` — Windows High Contrast replaces your palette with system colors. Check that borders and focus indicators still exist there; `forced-color-adjust-none` only on things like color swatches whose color *is* the content.
- `contrast-more:` — thicken borders and darken muted text for users who asked for it.
- `print:` — dark themes don't print; `print:bg-white print:text-black` on the root.
- Never encode meaning in color alone: a red border needs an icon or text too, and `aria-invalid` rather than a class.

## Forms

- Every input has a `<label>`; `sr-only` on the label text is fine, a placeholder as the only label is not (it disappears on typing).
- `:user-invalid` (`user-invalid:border-red-500`) instead of `:invalid`, which matches an untouched empty required field and paints the form red before the user types.
- Error text linked with `aria-describedby`, and announced with a live region if it appears after submit.
- The `forms` plugin removes the browser's own focus ring; supplying the replacement above is on you.

## Checks Before Shipping

- Tab through the whole component: every stop visible, order matches reading order (`order-*` changes paint order only; tab order stays as the DOM wrote it).
- Muted text measured, not eyeballed, against both light and dark backgrounds.
- Zoom to 200% and to a 320px viewport: content reflows without horizontal scroll (WCAG 1.4.10), nothing clipped.
- Reduced-motion and forced-colors modes toggled once.
- Every icon-only control has an accessible name (`sr-only` text or `aria-label`).
- No `outline-none` in the diff without a ring in the same class list.

