# Behavior spec — WIP Computer Homepage

Authoritative description of every interactive and animated piece. Use this
when porting to the production stack.

---

## On load (first 6.5 seconds)

- Page renders at scroll-top against pure white.
- Header is fully transparent. Only the WIP logo (top-left) is visible. The
  top-right "Demo Kaleidoscope" button is at 0% opacity.
- Hero displays the resolved headline as a static, fully-rendered DOM string:
  - **Top line:** Every AI. (Georgia regular)
  - **Bottom line:** *One experience.* (Georgia italic)
  - No caret. Holds completely still for ~6.5s. This is intentional — SSR /
    JS-off / crawlers see the resolved line, not a typing animation.
- Beneath the headline:
  - Subhead in muted color.
  - Two CTAs side by side: blue pill button "Demo Kaleidoscope ↗" (opens
    https://wip.computer/login?next=/demo in new tab) and quiet text link
    "Read the letter" (anchors to #letter).
- A single random Buckminster Fuller patent drawing (1 of 5 GIFs) sits behind
  the hero at 7% opacity. Position randomized from a curated BUCKY_PRESETS
  list (13 hand-tuned img/rotation/offset combinations).

---

## After the 6.5s hold — typewriter cycle starts

- A 1px blinking caret appears at the end of "One experience."
- Bottom line erases char-by-char (~53ms/char) until empty.
- Top line erases "Every AI." → "" and types "Your AIs:" char-by-char (~95ms/char).
- Three payoff lines cycle on the bottom line. Each is typed, held ~2.2s,
  erased back to empty, brief breath, then the next:

  **Group 1:** remember you. / remember everything. / forget when you say.
  **Group 2:** know who does what. / talk to each other. / work together.
  **Group 3:** go where you go. / live on every device. / never start over.
  **Group 4:** ask before they act. / wait for your yes. / work for you.

- After each group's 3rd payoff, top retypes back to "Every AI." and bottom
  retypes "One experience." Resolution holds for 5s with a calm-pulsing caret,
  then the next group begins.
- Cycle is infinite. The top line is the stem and never re-renders — only its
  trailing punctuation morphs between "." (resolved) and ":" (during cycle).
- Each line uses an invisible "ghost" sibling that reserves slot width at the
  target's final dimensions. Typing grows from the geometric center of the
  slot, so text stays horizontally centered relative to the line above it
  even mid-typing. This is what fixes the "know who does what" centering bug.

### Caret states

- **Blinking** (during typing/erasing): 1.2s on/off cycle.
- **Calm pulse** (during resolved holds): 2.6s ease-in-out fade.
- 1px wide, current text color, height: 0.85em.
- Position switches between top and bottom line in sync with the active line.
- The Caret element is declared *outside* the HeroTitle component so its
  identity is stable across re-renders — otherwise the CSS animation restarts
  on every typewriter tick (50–95ms) and never makes it past frame 0.
- `prefers-reduced-motion: reduce` → entire typewriter loop is disabled;
  page just shows the resolved headline statically. No caret.

---

## Bucky background

- Initial image picked from BUCKY_PRESETS at random (no immediate repeat).
- Every 50s, the bg fades out (700ms), swaps to a different preset, fades back in (700ms).
- An ambient slow Y-axis drift (~1.2 px/sec) plays continuously, random direction.
- No scroll-parallax, no mouse-parallax, no drag in the shipping version.
- (Debug only: clicking the WIP logo toggles a presets panel in the top-right
  that lets the designer manually jump to any image/rotation combination and
  capture new presets via clipboard. Strip this for production — see
  Strip-for-prod section below.)

---

## Header on scroll

- Header is `position: fixed`. Fully transparent at scroll-top.
- As soon as user scrolls past 8px:
  - A translucent white backdrop fades in (blur(10px) + rgba(255,255,255,0.78)).
  - A 6%-black hairline bottom border fades in.
- The header's "Demo Kaleidoscope" CTA opacity is *directly* tied to scroll
  position relative to the hero's own CTA:
  - 0% while the hero CTA is fully below the header line
  - linear ramp 0 → 100% as the hero CTA slides up through the header's
    vertical band (the height of the hero CTA itself)
  - 100% the moment the hero CTA is fully scrolled past
- Net effect: hero button disappears upward while header button takes its
  place pixel-by-pixel.

---

## Letter section

- Anchor: `#letter`. Read by "Read the letter" link in hero.
- Italicized eyebrow: "A letter from the founder · May 2026"
- Title: "Transmuting Command C + Command V" (sans-serif, 600).
- Body: first-person founder letter explaining the problem, naming the
  solution (Kaleidoscope / Lēsa / LDM OS), and inviting alpha use.
- Bulleted list of 6 open questions.
- Inline IKB-blue underlined link to github.com/wipcomputer.
- Sign-off: "Parker Todd Brooks / Founder, WIP Computer."
- Final CTA row: "Demo Kaleidoscope ↗" button + "Explore the architecture ↓"
  text link.

---

## Architecture section (hidden by default)

- Always present in the DOM as a `<div id="explore">` with `display: none`.
- Triggered by clicking "Explore the architecture ↓" in the letter CTA.
- On click:
  - Section sets `display: block`, fades to opacity 1 (280ms).
  - `scrollIntoView({ behavior: 'smooth', block: 'start' })` anchors the
    section's title just below the header (24px scroll-margin-top).
  - The "Explore the architecture" link in the letter CTA disappears.
- The section has a small × button in the top-right of its header, aligned
  to the cap-line of the title (not the visual middle). Rotates 90° on hover.
- Clicking × closes the section (`display: none`, opacity fade) and smooth-
  scrolls back to the letter's CTA row. The "Explore the architecture" link
  reappears in the letter.
- Content: title "WIP Computer Architecture" + a subtitle that spans the
  full grid width, then a 2-column grid of 8 product cards (name + one-line
  description, no icons, no images): Kaleidoscope, LDM OS, Memory Crystal,
  Remote Control, Bridge, Sapien ID, Dream Weaver, Agent Pay.
- Shared state: `_archState` + `useArchOpen()` hook. One open/close source
  of truth used by both Letter (to hide the trigger link) and Products (to
  render the section).

---

## Footer

3-column grid + bottom row.

- **Brand col** (wide, left): "WIP Computer, Inc." / "Learning Dreaming
  Machines" / "Made in California."
- **Tools col:** "Are you an AI agent?" (links to wip.computer/agent.txt,
  new tab) + a clickable "Local passkeys on/off" pill with a red→green
  status dot. Local React state; resets on reload. (See note in
  Strip-for-prod about wiring this to the real passkeys API.)
- **Connect col:** GitHub @wipcomputer + X @wipcomputer, each with its
  inline-SVG icon.
- **Bottom row:** copyright on left, Privacy Policy + Terms of Use on right,
  both linking to wip.computer/legal/… URLs in new tab.
- Hairlines above the columns and above the copyright line are inset at the
  same column width.

---

## Color and type system

- Background: pure white `#ffffff`.
- Body text: `#444` muted gray.
- Headings: `#111`.
- Accent (buttons, inline letter link): International Klein Blue family —
  `#1f4ec2` default → `#0033ff` (electric IKB) on hover. The exact hex
  comes from sampling https://wip.computer/demo/ — keep it consistent.
- Type stack:
  - Display (hero, letter title): Georgia, regular + italic
  - Body / UI: Inter Tight, weights 400/500/600
  - No monospace, no system-sans, no third typeface
- All corners squared (border-radius: 0) **except** pill-shaped CTA
  buttons which are fully rounded (border-radius: 999px).
- Layout: max-width 680px for body content (the letter), 1040px wide for
  product grid. Generous vertical spacing between sections.

---

## Strip-for-production

These are debug affordances and should be removed before ship:

1. **Bucky readout panel.** In Hero(), the `<div className="bucky-readout">`
   block (rows of img/rot/y/dx/dy values + the 0°/90°/180° grids of 1–15).
   Triggered by clicking the WIP logo. The whole `readoutOn` state and the
   logo's onClick handler should be removed.
2. **Easter-egg snapshot copy.** In Hero's mousedown/up handlers, the
   block that copies snapshot text to the clipboard via `navigator.clipboard`
   when a non-drag click happens. Remove the click branch entirely.
3. **Bucky drag.** Same handlers. Production should not allow dragging the
   bg around.
4. **Local passkeys toggle.** Currently dumb local state. Either wire to
   the real passkeys API the demo site already uses, or remove the toggle
   and just show a static indicator.

Everything else ships as-is.

---

## Accessibility notes

- `aria-label="Every AI. One experience."` on the `<h1>` and all animated
  text marked `aria-hidden="true"` — screen readers always get the canonical
  line, never mid-typing fragments.
- `aria-pressed` on the passkeys button.
- `aria-label` on the architecture close button.
- All external links carry `target="_blank" rel="noopener"`.
- `prefers-reduced-motion: reduce` disables: typewriter loop, caret
  animation, bucky bg drift + cross-fade transitions (transitions become
  instant; bg still swaps but without motion).
- One known gap: the architecture reveal uses `display: none ↔ block`
  rather than `inert` + ARIA — fine for now but a screen reader could
  potentially announce the hidden content during the in-between frame.
  Worth tightening in production.

---

## Tech

- Single static HTML page (`Homepage.html`) loading React 18 + ReactDOM +
  Babel Standalone from unpkg. JSX transpiled in-browser at load time.
- Component split: `components.jsx` (Header, Hero, HeroTitle, Letter,
  Products, Footer), styles in vanilla `styles.css`.
- The prototype is the design reference; production port will likely be
  vanilla JS to match a "no React, no build step, no framework runtime"
  deliverable spec from the wip-websites-private brief.

---

## Deploy notes (from earlier conversation)

> The brief from the local agent says explicitly:
> "No React, no JSX, no build step, no framework runtime."
>
> But it also says:
> "If you prototype in a framework, also export a plain static version,
> and the static version is the deliverable."

This export is the framework prototype. The vanilla static port still has
to happen separately. All component logic is small enough to translate
piece-by-piece — the typewriter and the header crossfade are the only
non-trivial bits.
