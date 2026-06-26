# Design Language Lock (`DESIGN.md`)

The consistency engine. At Step 3, **write this artifact once per project** to
`.ulpi/design/DESIGN.md`. Every later screen, component, and session BINDS to it. This is what makes
repeated outputs look like one product instead of a fresh guess each time.

## Lock rules (non-negotiable)

- Tokens are **normative**; prose is context. Never split or duplicate the source of truth.
- **Variation within identity, never between.** Screens may differ in composition — never in palette,
  type, radius, or voice.
- **One per project:** one accent, one radius scale, one icon family, one type pairing, one copy register.
- **Re-read `DESIGN.md` before** specifying any new screen or feature. Any value outside it is a defect.
- Write this identity-lock sentence verbatim into every spec: *"Every screen must read as the same
  product if placed side by side."*

## The register split (decide first)

- **brand** — design IS the product (landing, marketing, portfolio): bolder type, more signature, a
  larger motion budget, expressive layout.
- **product** — design SERVES the task (app, dashboard, tool): clarity and density discipline, one
  component vocabulary reused everywhere. *"If the Save button looks different in two places, one is wrong."*

The register flips many rules — set it before anything else.

**Design-system routing (product register).** Prefer an established component system over bespoke
re-creation: pick ONE and record it as `design_system:`. See `design-system-routing.md` for the
brief→system map and the honesty rule. (`brand` register may go fully bespoke.)

## `DESIGN.md` template

Frontmatter (the locked, machine-readable header):

```yaml
---
project: <name>
register: brand | product
aesthetic_direction: <one named direction from anti-slop.md menu>   # justified by the brief
color_strategy: restrained | committed | full-palette | drenched
design_system: <name or "bespoke">   # product register → pick one; see design-system-routing.md
design_variance: 1-10        # optional taste dials — how far to push from convention
motion_intensity: 1-10
visual_density: 1-10
---
```

Body sections:

**## Design Read** — one line: the feeling + the bet. e.g. "Premium, restrained, editorial — trust over novelty."

**## Signature** — the single element this product is remembered by, and why it fits the brief.
Spend boldness in ONE place — the Signature — and keep everything around it quiet and disciplined (the
"remove one accessory" rule). One memorable move beats five competing ones.

**## Inspiration** (if any links were given) — per source: `took: <DNA>` and `rejected: <what we did NOT inherit>`, plus a one-line synthesis note proving it is not a clone of any single reference.

**## Color (locked)** — a table of named roles → OKLCH + hex + use:

| role | OKLCH | hex | use |
|------|-------|-----|-----|
| background / surface / elevated | | | |
| text / muted / subtle | | | |
| accent (exactly one) | | | |
| success / warning / danger / info | | | |

- Neutrals are **tinted** toward the brand hue (+0.005–0.015 chroma). Distribute 60-30-10 by visual weight.
- Every text/UI pair passes WCAG AA — record the ratio.

**## Type (locked)** — roles, families, usage:

| role | family | use | notes |
|------|--------|-----|-------|
| display | | headlines | tracking floor, used with restraint |
| body | | reading | measure 65–75ch |
| utility | | captions / data | |

- Paired on a contrast axis (serif+sans / geometric+humanist) OR one family in multiple weights.

**## Scales (locked)** — `spacing:` one scale · `radius:` one scale · `motion:` durations 100/300/500,
named easing curve, no bounce/elastic for UI, `prefers-reduced-motion` honored.

**## Voice** — `register:` (e.g. plain, confident, technical) · `action vocabulary:` consistent names
through a flow ("Publish" → "Published").

## Cross-session consistency

On any later feature: Read `.ulpi/design/DESIGN.md` FIRST, design strictly within it, and flag (don't
silently introduce) anything the brief forces outside it — then update it deliberately, never drift.
