---
name: visual-dna
description: "Extract visual identity into reusable Design DNA JSON, then apply it to generate faithful UI from references."
metadata:
  version: "0.2.2"
---
# Design DNA

Extract visual identity from any reference. Apply it to any content. Reuse it everywhere.

Three phases — use any combination:

1. **Analyze** — screenshots, images, or URLs → Design DNA JSON
2. **Generate** — Design DNA JSON + your content → faithful implementation
3. **Structure** — show the full schema when asked

Read `references/schema.md` for the full field list.
Read `references/generation-guide.md` for generation rules.


## Activation Boundary

Use this skill only when the user explicitly asks for visual DNA extraction, style analysis, brand/design-system extraction, or generation from an existing Design DNA JSON. Do not activate it for generic UI tasks unless the user supplied references or asked to match a reference.

When URLs or assets are supplied, use the references the user provided or assets already present in the project. Report which references were used. Do not try to judge ownership, sensitivity, or permission to analyze a reference; that is a human decision. Ask only when the reference itself is ambiguous, unavailable, or requires credentials you do not have.

## The Three Dimensions

| Dimension | What it captures |
|-----------|-----------------|
| **design_system** | Measurable tokens: colour, typography, spacing, layout, shape, elevation, motion, components |
| **design_style** | Qualitative feel: mood, visual language, composition, brand voice, interaction personality |
| **visual_effects** | Special rendering: Canvas, WebGL, particles, shaders, scroll effects, SVG animation |

## Phase 1: Analyze

When the user provides screenshots, images, or URLs:

1. Read `references/schema.md` — know every field before starting
2. For each reference: analyze or fetch and analyze
3. Fill **every field** — no empty strings, no guesswork flagged as guesswork
4. When references conflict: note the dominant pattern, mention variants
5. Output complete Design DNA JSON
6. Ask: "Want to adjust any values before generating?"

**Key extraction rules:**
- Colour: sample dominant palette by area. Primary = largest area, accent = CTA usage
- Typography: identify font class visually (geometric, humanist, serif). Estimate scale ratios from heading/body relationships
- Spacing: assess density by element proximity. Measure section rhythm consistency
- Visual effects: scan for Canvas, WebGL, Three.js, GSAP, particles, shaders, custom cursors. Set `enabled: false` for anything not present

## Phase 2: Generate

When the user provides DNA JSON + content:

1. Read `references/generation-guide.md`
2. Build CSS custom properties from `design_system` tokens
3. Apply `design_style` qualitative fields to subjective decisions
4. Implement `visual_effects` at the appropriate tech tier (CSS → Canvas → WebGL)
5. Fetch real assets from original URLs when possible — don't recreate
6. Default output: self-contained HTML with inline CSS/JS

**Priority order:**
1. Colour & typography (80% of visual identity)
2. Spacing & layout
3. Shape & elevation
4. Design style qualitative fields
5. Visual effects
6. Motion & interaction

**Quality check before delivering:**
- Does it actually look like the reference?
- Are all design tokens applied (not just some)?
- Is the output self-contained (no external dependencies that could break)?
- Do visual effects degrade gracefully without JS?

## The DNA JSON as an Asset

The extracted JSON is the key output — not just the generated UI. Once extracted:
- Commit it to version control
- Share it across teams and projects
- Feed it to any agent for any future generation
- Refine it iteratively

This turns "make it look like that site" into a precise, reproducible spec.

## Pair with no-slop-ui

When generating UI from DNA:
- Apply `no-slop-ui` rules alongside DNA tokens
- DNA tells you WHAT the design is
- `no-slop-ui` tells you what NOT to do (no AI defaults slipping in)
- Together: faithful to reference, clean execution
