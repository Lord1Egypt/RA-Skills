# Registers

Load when: choosing visual direction, color, typography, layout, density, imagery, or tone.

For new products and redesigns, registers inform the design foundation. Do not let each screen reinterpret the register differently.

## Brand Register

Brand surfaces create the impression: landing pages, marketing sites, portfolios, campaigns, product stories, venue pages, long-form editorial, about pages.

Brand can be distinctive, but every distinctive move must earn attention.

Before choosing an aesthetic, name the reference lane and the category reflex. A landing page should not become editorial-serif restraint, purple AI gloss, brutalist utility, the severe black manifesto dev-tool page, or centered hero plus three cards unless the brief actually earns that lane.

Use:

- Stronger first-view composition.
- Real imagery, product shots, objects, scenes, or generated visual assets when the subject demands it.
- More expressive typography when it fits the voice.
- Committed color when color is the brand.
- Pacing, silence, and contrast.
- A small number of memorable details.

Avoid:

- Safe but invisible restraint.
- Editorial aesthetics by reflex.
- Monospace as fake technical personality.
- Repeated labels, pills, tiny uppercase scaffolding, or section-number theater.
- Text-only pages when the subject is physical, visual, spatial, or product-led.
- Stock-looking visuals used where the actual product, place, person, or state should be inspectable.
- Manifesto headlines that announce the brand's taste or values instead of a design that proves them.

Brand test:

```text
Would this feel intentional if the logo were removed?
```

If not, the design is leaning on category defaults.

Brand foundation:

- Lock the vibe before selecting fonts or colors.
- Choose imagery and type as part of character, not decoration.
- Give the brand one or two memorable moves, then protect the rest with restraint.
- Document what counts as too generic, too cold, and too loud.
- Decide the visual asset strategy early: real assets, generated raster assets, product screenshots, canvas/WebGL, or a deliberate text-only treatment that the brief can defend.

## Product Register

Product surfaces serve a task: app UI, dashboards, settings, admin panels, editors, authenticated tools, forms, onboarding, checkout, command surfaces.

Product restraint is not plainness. It is earned familiarity plus exact craft.

The product bar is trust in motion: a fluent user should keep moving because the interface behaves like a serious tool in its category. Surprise is expensive and must pay for itself.

Use:

- Platform and category defaults as the baseline.
- Predictable navigation, forms, tables, filters, tabs, sidebars, and command affordances.
- Dense scanning when users need repeated use.
- State-rich components.
- Consistent tokens, components, labels, and icon semantics.
- Motion for state and continuity only.
- Existing component libraries and official packages when they already define the expected behavior.

Avoid:

- Brand-page drama in operational tools.
- Decorative motion.
- Display fonts in labels, buttons, or data.
- Inconsistent component vocabulary.
- Invented affordances for standard tasks.
- Decorative brand-page composition in repeated operational surfaces.

Product test:

```text
Would a fluent user trust this and keep moving, or pause at every subtly-off decision?
```

Product foundation:

- Lock component vocabulary before building many screens.
- Define dense and comfortable spacing variants.
- Define state colors, focus rules, skeletons, empty states, and error behavior.
- Preserve familiarity unless a deviation has a clear user benefit.
- Define table, form, filter, navigation, and command patterns before multiplying screens.

## Color

Pick a strategy before picking values:

- **Restrained**: tinted neutrals and one small accent. Product default.
- **Committed**: one color carries much of the surface. Useful for strong brand moments.
- **Full palette**: several named roles, each with a job. Useful for data, campaigns, or rich identity systems.
- **Drenched**: the surface is the color. Rare, brand-led, and high-commitment.

Rules:

- Avoid pure black and pure white when softer tinted neutrals give more depth.
- Do not drift between warm and cool neutral systems without a reason.
- Accent color marks action, selection, state, or identity. It is not confetti.
- Serious contexts usually need lower chroma and cleaner hierarchy, not less care.
- For brand surfaces, color strategy may carry voice. For product surfaces, color usually carries action and state.

## Typography

- Product UI can use system fonts when native familiarity matters.
- Brand surfaces may need a more specific type voice, but not a reflex font.
- Use fewer roles: display, heading, body, label, data is often enough.
- Hierarchy comes from size, weight, spacing, and contrast, not decoration.
- Keep body text readable, usually 65-75 characters per line.
- Do not use letter spacing as a substitute for composition.

## Layout

- Prefer a clear structure over decorative framing.
- Use whitespace as structure.
- Align edges deliberately; optical alignment beats mechanical equality.
- Break the grid only when the break creates emphasis.
- Cards are not the default layout unit.
- Page sections should not all share the same family.
- Mobile behavior must be designed, not assumed.
- First viewport composition must expose the primary subject or action quickly. If a nav wraps, a hero pushes the CTA below the fold, or text cannot fit, the composition is not done.

## Warmth

Warmth is the guardrail against sterile minimalism.

Add warmth through:

- Specific, humane copy.
- Thoughtful defaults.
- A better empty state.
- A recovery path that reduces anxiety.
- Small tactile feedback.
- A visual detail that rewards attention without demanding it.
- Preserving useful familiarity instead of stripping it away.

Do not add warmth through random decoration.
