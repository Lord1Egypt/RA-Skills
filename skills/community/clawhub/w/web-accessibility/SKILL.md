---
name: web-accessibility
description: Apply WCAG 2 Level AA accessibility standards to design systems, UI components, and web pages — contrast math with a runnable validator, design-token patterns that make color accessible by construction, typography and focus-state rules, and a semantics checklist. Use when building or reviewing UI, choosing colors or type for a brand/design system, setting up design tokens, wiring accessibility checks into a build, or when the user mentions accessibility, a11y, WCAG, contrast, or screen readers.
license: MIT
metadata:
  author: raunakkathuria
  version: "1.0"
---

# Web Accessibility (WCAG 2 AA)

Make interfaces conform to [WCAG 2 Level AA](https://www.w3.org/WAI/WCAG2AA-Conformance) by building
accessibility into the design system, not auditing it in afterwards. A color, text style, or
component that enters the system already passing AA scales to every page that uses it; one that
doesn't becomes a bug on every page at once.

Conformance target: WCAG 2.2 Level AA ([quick reference](https://www.w3.org/WAI/WCAG22/quickref/?currentsidebar=%23col_customize&levels=aaa)).

## The order of operations

1. **Tokens first** — validate the palette as fg/bg pairs before any component uses it.
2. **Components second** — states, focus, target size, semantics per component.
3. **Pages last** — structure, headings, alt text, keyboard walk-through.

Fixing a failing token fixes every component; fixing a failing page fixes one page. Work top-down.

## 1. Color contrast is math, not judgment

Never eyeball contrast. The thresholds (WCAG 2.2):

| What renders | Minimum | Success criterion |
|---|---|---|
| Normal text (below 24px / below 18.66px bold) | **4.5:1** | 1.4.3 |
| Large text (≥24px, or ≥18.66px bold) | **3:1** | 1.4.3 |
| Meaningful non-text (icons, chart marks, input borders, focus indicators) | **3:1** | 1.4.11 |
| Disabled controls, decorative elements, logos | exempt | — |

Run the bundled validator (no dependencies, Node ≥14):

```bash
# ad-hoc pairs: fg,bg,minimum,label
node scripts/check-contrast.mjs --pair "#0f766e,#ffffff,4.5,link on white"

# a whole palette from a JSON config (see script header for the format)
node scripts/check-contrast.mjs contrast-pairs.json
```

**Wire it into the build.** A contrast check that runs once is an audit; one that runs in
`npm run build` or CI and exits non-zero is a guarantee. Add every token pair that renders as text
or meaningful graphics, in every theme.

## 2. Token patterns that make color accessible by construction

Three patterns cover most real-world palette failures:

- **Split fill roles from text roles.** Vibrant brand colors (a teal, an orange, a mid-blue) usually
  pass as a *fill behind dark text* but fail as *text on a light background* — often by a factor of
  two. Define both and never let components cross them:
  ```css
  --color-primary:      #14b8a6;  /* fills, borders, focus rings — never text on light */
  --color-primary-text: #0f766e;  /* the same hue, dark enough to be text (≥4.5:1)   */
  ```
  Filled buttons then choose text *per theme*: dark text on a bright fill, or light text on a dark
  fill — whichever pair passes, verified by the script, not by taste.

- **Theme-tune semantic colors.** Success/warning/error values that read well on near-black
  (`#f59e0b` amber, `#ef4444` red) fail on white — amber is ~2.2:1 there. Map
  `--color-success/warning/error` per theme instead of sharing one set; keep the bright ramp for
  dark themes and a darker ramp (e.g. `#b45309`, `#dc2626`) for light.

- **Subtle text has a floor.** Placeholder, hint, and caption text is still text — 4.5:1 applies.
  Mid-grays like `#9ca3af` on white (~2.5:1) are the single most common violation on the web. The
  lightest AA gray on white is around `#767676`; pick your "subtle" token at or below that
  lightness.

## 3. Typography that scales

- **Relative units** (`rem`/`em`) for font sizes, line heights, and containers that hold text —
  browser zoom and text-resize must work to 200% without loss of content (SC 1.4.4).
- **Body text ≥ 1rem (16px)**; don't fight user font-size settings with `html { font-size: 62.5% }`
  tricks that bake in pixel assumptions.
- **Line height ≥ 1.5** for body copy; paragraph spacing larger than line spacing (SC 1.4.12 expects
  content to survive these being user-forced).
- **Don't convey meaning by color alone** (SC 1.4.1): pair color with an icon, weight, underline, or
  text label — links inside prose need more than a hue change.

## 4. Interactive states

- **`:focus-visible` on every interactive element** — a 2px+ outline with 3:1 contrast against the
  surrounding surface (SC 2.4.7, 2.4.13). Never `outline: none` without a replacement.
- **Hover/active recolors must also pass.** A link that darkens on hover passes twice; one that
  brightens toward the background fails exactly when the user is looking at it. Add state colors to
  the contrast config too.
- **Target size ≥ 24×24 CSS px** (SC 2.5.8) — buttons, nav links, icon buttons. 44px stays the
  comfortable default for primary controls.
- **Respect `prefers-reduced-motion`** — gate non-essential animation behind the media query.

## 5. Semantics checklist (the part tokens can't fix)

Run through this per component/page; details and fix patterns in
[references/wcag-checklist.md](references/wcag-checklist.md):

- Images: `alt` text that says what the image *does* here; `alt=""` for decorative (1.1.1)
- One `<h1>`, headings in order, no skipping levels for styling (1.3.1)
- Real elements: `<button>`, `<a href>`, `<label for>` — not styled `<div>`s (4.1.2)
- Every input labelled; errors identified in text, not color alone (3.3.1, 3.3.2)
- Full keyboard walk-through: reach, operate, and *leave* everything; logical tab order; skip link
  on page-level nav (2.1.1, 2.1.2, 2.4.1)
- Current page/state marked (`aria-current="page"`, `aria-expanded`, …)
- Page `lang` attribute and a descriptive `<title>` (3.1.1, 2.4.2)

## Honest boundaries

- Automated checks (this script, axe, Lighthouse) catch roughly a third to half of WCAG failures —
  the mechanical ones. Keyboard walk-throughs and a screen-reader pass (VoiceOver/NVDA) are still
  required for real conformance. Say "the token layer is AA-verified", not "the product is
  accessible", until both have happened.
- A design system guarantees the **visual layer**: contrast, focus visibility, scalable type,
  target sizes. Content semantics — alt text, heading order, labels, keyboard flows — live in each
  product and must be checked there.
- Contrast ratios apply to the colors *as rendered* — opacity, gradients, and text over images need
  checking at their worst point, not their average.
