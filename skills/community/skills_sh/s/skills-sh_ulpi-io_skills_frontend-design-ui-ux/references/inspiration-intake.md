# Inspiration Intake (via the `browse` skill)

When the user provides reference links, do NOT guess from the URL — **actually visit each** with the
`browse` skill, extract its design DNA, and synthesize (never clone) into the locked `DESIGN.md`. None
of this writes code; it produces design understanding.

## When to run

Step 1, only if the user gave 1–4 inspiration URLs. Ask once in Step 0: *"Any reference sites or
designs you admire? Paste 1–4 URLs."* Optional — skip cleanly if none.

## Requires

The `browse` skill (`@ulpi/browse`). If browse is not installed, or a link is unreachable: say so, ask
the user to describe the vibe or paste screenshots, and proceed from the brief. **Never block on it.**

## Procedure per link (use the `browse` skill)

1. `browse goto <url>`.
2. Screenshots: full page + the hero + 1–2 key sections (composition, density, rhythm).
3. Extract computed design values via `browse` JS eval — sample real elements:
   - **Type:** `getComputedStyle(h1).fontFamily / fontSize / fontWeight / letterSpacing`; body font.
   - **Color:** computed `background-color` & `color` of body, sections, and the primary button → assemble the real palette.
   - **Shape / depth:** `borderRadius` and `boxShadow` of cards and buttons.
   - **Spacing:** section padding / margin rhythm.
   - **Layout:** column count, grid usage, hero pattern, nav style (`browse snapshot` for structure).
4. Distill into a one-line **DNA note** per site, e.g.:
   "Linear — tight tracking, near-mono palette, restrained motion, generous whitespace."

## Synthesize — do NOT clone (critical)

- Cross-blend 2–4 references into something **distinct**. If the output looks like a single reference
  reskinned, it failed.
- **The brief beats the references.** Anti-slop (`anti-slop.md`) still applies — if a reference uses a
  banned tell (purple glow, em-dash, 3 equal cards), do NOT inherit it.
- Never lift proprietary assets, logos, or copy. Take principles, not pixels.

## Record provenance

Write the `Inspiration` block into `.ulpi/design/DESIGN.md`: per source, what you **took** and what you
**rejected**, plus a one-line synthesis note. This makes the identity auditable and repeatable across the project.
