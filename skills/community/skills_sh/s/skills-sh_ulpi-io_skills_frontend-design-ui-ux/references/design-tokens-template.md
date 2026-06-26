# Design Tokens — Derivation Method

Tokens are **derived per brief and locked in `DESIGN.md`** (see `design-language-lock.md`). This file is
the **method** for deriving them plus a set of **neutral structural scales** — it is NOT a ready-made
palette to paste. There is deliberately no default brand color or default font here: shipping a default
identity is what produces generic, "AI slop" output.

> Color and type are IDENTITY — derive them. Spacing, radius, shadow, z-index, breakpoints are
> STRUCTURE — start from the neutral scales below, then pick ONE of each and lock it.

---

## Color — derive, never default

1. **Seed from the subject** — the brand, product domain, mood words, and any inspiration DNA
   (`inspiration-intake.md`). Not from a default palette.
2. **Pick a color strategy** (record in `DESIGN.md`):
   - `restrained` — tinted neutrals + one accent ≤ ~10% of surface.
   - `committed` — one saturated color carries 30–60%.
   - `full-palette` — 3–4 named roles.
   - `drenched` — the surface itself IS the color.
3. **Work in OKLCH** for perceptually even ramps; export hex alongside.
4. **Tint the neutrals** toward the brand hue (+0.005–0.015 chroma) — pure grays read as generic.
5. **Distribute 60-30-10** by visual weight (dominant / secondary / accent).
6. **Define semantic states** (success / warning / danger / info) within the same chroma language.
7. **Verify WCAG AA** for every text/UI pairing (4.5:1 text, 3:1 large text + UI) and record the ratio.

Role set to fill (named, not numbered-only): `background` / `surface` / `elevated`, `text` / `muted` /
`subtle`, `border`, exactly **one** `accent`, and the four semantic states. Dark mode: re-derive
(don't just invert) — keep the tint and the contrast guarantees.

## Type — derive, never default

1. **Choose roles:** a `display` face (characterful, used with restraint), a `body` face (quiet,
   readable), and a `utility`/`mono` face for captions or data if needed.
2. **Pair on a contrast axis** — serif+sans, geometric+humanist, or one family in multiple weights.
   Avoid the reflex defaults in `anti-slop.md`.
3. **Scale:** a modular scale sized to the register (brand can go large/expressive; product stays tight).
4. **Craft details:** body measure 65–75ch; a display letter-spacing floor (≈ ≤ −0.02em at large sizes);
   `text-wrap: balance`/`pretty` for headings; metric-matched fallback fonts to avoid layout shift.

---

## Neutral structural scales (pick ONE of each, then lock)

These carry little identity, so a sensible default is fine — but lock a single choice per project.

**Spacing** (4px base rhythm): `0, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128` (px). Keep the
rhythm consistent; don't mix step systems within a project.

**Radius** — pick ONE scale and use it everywhere: e.g. `{ sm: 4, md: 8, lg: 12, xl: 16, full: 9999 }`.
A single radius language is a strong, cheap consistency signal.

**Shadow / elevation** — a small set tied to z-layers (`sm`, `default`, `md`, `lg`, `xl`). Prefer soft,
low-opacity shadows; avoid the harsh default drop-shadow look.

**Z-index layers** (named, not magic numbers): `base 0, dropdown 20, sticky 30, fixed 40,
modalBackdrop 45, modal 50, popover/tooltip 60, toast 70, skipLink 80`.

**Breakpoints:** `sm 640 · md 768 · lg 1024 · xl 1280 · 2xl 1536` (px). Container max widths a touch
narrower than the breakpoint for readability.

**Motion:** durations `fast 100–150 · base 300 · emphasis 500`; one named easing curve (e.g.
`cubic-bezier(0.16, 1, 0.3, 1)`); **no bounce/elastic for UI**; exit ≈ 75% of enter; honor
`prefers-reduced-motion`. Motion must be motivated (see `anti-slop.md`).

---

## Handoff notes (for engineering agents)

- Use **semantic** token names in components (`bg-surface`, `text-muted`) — never raw values.
- Map tokens to the project's system (Tailwind theme / CSS variables) — but `DESIGN.md` stays the
  source of truth; the implementation derives from it, not the reverse.
- Test every component in light and dark; verify contrast and focus states.
- This skill produces the **token spec**, not the implementation — hand the locked values to the engineer.
