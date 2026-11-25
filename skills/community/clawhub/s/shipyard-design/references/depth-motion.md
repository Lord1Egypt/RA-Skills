# Depth, motion and after-effects

Use this after a look is applied. Small, consistent and calm beats flashy. Every rule must work in light AND dark.

## Shadows (depth)

- Use one scale of 3 or 4 levels as CSS variables inside each pack's `extra`, e.g. `--shadow-1` (cards at rest), `--shadow-2` (hover, dropdowns), `--shadow-3` (dialogs, sheets). Never write a one-off shadow in a component.
- Light mode: soft, low-opacity shadows tinted toward the page colour, two layers (a tight one plus a wide one), e.g. `0 1px 2px rgb(0 0 0/.06), 0 4px 12px rgb(0 0 0/.06)`.
- Dark mode: shadows barely show. Show depth with a slightly lighter surface for each level plus a 1px hairline border (`--border`). Optional: a faint top inner highlight `inset 0 1px 0 rgb(255 255 255/.04)`.
- Flat, editorial or "console" looks may use no shadows at all, only hairlines. That is a valid choice: say it in DESIGN.md.
- At most one glow per screen (e.g. the main action), and only if the look calls for it.

## Motion

- Durations: 120 to 160 ms for hover and press, 180 to 250 ms for things entering (menus, toasts, sheets), up to 300 ms for page-level changes. Nothing over 400 ms.
- Easing: ease-out (`cubic-bezier(.2,.8,.2,1)`) for entering, ease-in for leaving. No bounce unless the look is playful.
- Animate only `opacity` and `transform`. Never width, height, top or left (janky on phones).
- Good uses: press feedback (scale .98), a list item appearing (fade + 4px rise), a dialog opening, route cross-fade, a skeleton shimmer while loading.
- Put shared values in variables: `--ease-out`, `--dur-fast`, `--dur-base`.
- Always respect reduced motion:
  `@media (prefers-reduced-motion: reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}`

## After-effects (opt-in only)

Blur/glass, film grain, gradient meshes, parallax and animated backgrounds are off unless the student asks or the chosen direction is built on one. When used:
- Keep text on a solid or near-solid surface; check AA contrast over the effect, in both modes.
- Glass needs a fallback for browsers without `backdrop-filter` (a solid surface).
- One effect per look. Never stack glow + glass + grain.
- Turn heavy effects off on `prefers-reduced-motion` and on small screens if they cost performance.

## Check it

Look at light and dark screenshots on a phone width. If a card disappears into the page in dark mode, add a border, not a bigger shadow. If anything moves on first load for no reason, remove it.
