# Design Foundation

Load when: starting a new product, creating a new visual direction, redesigning, or whenever the work needs reusable coherence before screens are built.

Mies design work should not make up new values screen by screen. Establish the foundation first, then compose from it.

Lockable decisions must be written in templates, tables, token files, or component specs. Do not leave reusable rules as freeform prose the next agent has to reinterpret.

## Purpose

The foundation is the source of truth for:

- Vibe.
- Character.
- Quality facets.
- Color.
- Type.
- Spacing.
- Radius.
- Layout grid.
- Containers and elevation.
- Icons.
- Motion.
- Component states.
- Copy voice.

If the project already has a design system, read it and extend it. If it does not, create the smallest useful foundation before building screens.

## Discovery Order

Look for these before creating new values:

- `PRODUCT.md`, `DESIGN.md`, brand docs, component docs, or equivalent project notes.
- Theme files, CSS variables, Tailwind config, design tokens, native platform styles.
- Existing primitives: buttons, inputs, dialogs, panels, empty states, tables, navigation.
- `package.json` and lockfiles, so imports match installed libraries.
- Screenshots or live surfaces that show the real design language.

If a foundation exists, preserve its vocabulary unless it is the thing being redesigned. If the project has no foundation, create only the smallest durable slice needed for the current work.

## Foundation Output

For new products and redesigns, produce or update a durable artifact in the project-appropriate place:

- `DESIGN.md` when the project has no better design doc.
- Existing design docs when they exist.
- Theme files, token files, Tailwind config, CSS variables, or component primitives when implementation is part of the task.

Do not scatter decisions across one-off components.

## System Choice

Use one system per product surface.

- If the brief maps clearly to an official design system, use the official package and tokens when practical.
- If the project already uses shadcn, Radix, Material, Carbon, Fluent, Polaris, Primer, or a native platform system, extend that system instead of replacing it.
- If the brief is an aesthetic rather than a system, say so internally and build the aesthetic from tokens, primitives, and real assets. Do not pretend an aesthetic has an official package.
- If a new dependency is useful, verify it is installed or provide the install step before importing it.
- Do not override 90 percent of a system and still call it that system. At that point, define a local foundation.

## Required Templates

Use the bundled templates as scaffolds whenever the foundation is created or materially changed. They are not rigid forms; keep the repeatable decisions, remove irrelevant rows, and rename tokens to match the project's stack and conventions.

- `templates/design-foundation.md`: the main durable foundation document.
- `templates/token-table.md`: structured token lock for colors, type, spacing, radius, shadows, layout, and motion.
- `templates/primitive-spec.md`: reusable component primitive contract.
- `templates/exception-record.md`: required for any one-off value or rule deviation.

If the project already has its own equivalent templates, use those instead and preserve their structure. Do not force the bundled template over a better local system.

## Vibe Lock

Write 2-4 sentences using the `Vibe Lock` shape in `templates/design-foundation.md`. This is the atmosphere contract.

Include:

- What the product should feel like.
- What it must not feel like.
- How restraint should behave.
- Where warmth comes from.

Example shape:

```text
The interface should feel quiet, exact, and expensive, like a tool built by someone who removes before adding. It should never feel empty, cold, decorative, or template-made. Warmth comes from clear recovery paths, thoughtful defaults, calm language, and small details that reward attention without asking for it.
```

## Character Lock

Write a short paragraph using the `Character Lock` shape in `templates/design-foundation.md`. This helps the agent act consistently.

Include:

- What this designer notices first.
- What they refuse to tolerate.
- What details they obsess over.
- How they treat real users.

Example shape:

```text
The character behind this system is a precise editor with human instincts who works with autistic, literal precision — exhaustive, never approximate. They notice a one-pixel misalignment, a radius that doesn't nest, a hardcoded value that should be a token, noisy containers, weak states, careless copy, and buttons that feel accidental. They verify at high zoom, reject "close enough," and treat exactness as respect rather than fuss. They protect the user's focus, remove anything performative, and leave behind one small sign that someone thought about the person using it.
```

## Voice Lock

Copy is part of the foundation, not a per-screen afterthought. Lock the voice once so every surface sounds like one product. Write 2-3 sentences plus the rails in the `Voice Lock` row of `templates/design-foundation.md`:

- How the product sounds (warm, plain, exact — match the vibe).
- Person, tense, and casing for labels and actions (usually second person, present tense, sentence case).
- What the voice never does (no hype words, no fake-warm exclamations, no overexplaining).
- One term per concept for the core nouns and actions.

Word writes and audits against this lock (`copy.md`). If no voice exists and the work is larger than a small fix, set it before composing.

## Token Lock

Define a small system before building. Use `templates/token-table.md` or the project's existing token structure. Every repeated value needs enough structure to be reused: name, value, role, and usage boundary.

### Color

- Neutral base: background, surface, elevated surface, border, muted text, body text, strong text.
- Accent: primary action and selected state.
- Semantic: success, warning, error, info only when needed.
- Rules: when each color may be used and what is banned.
- Prefer perceptual color spaces such as OKLCH when the stack supports them.
- Avoid pure black and pure white as defaults; lightly tinted neutrals usually age better.
- Lock warm or cool neutrality for the surface. Do not drift between them by accident.
- Check contrast for text, buttons, focus rings, charts, disabled states, and semantic states.

### Type

- Font family or families.
- Display, heading, body, label, data roles.
- Size scale.
- Weight scale.
- Line height rules.
- Maximum line lengths.

### Spacing

- Base unit.
- Section spacing.
- Component padding.
- Inline gaps.
- Stack gaps.
- Dense variants for product UI.

### Shape And Depth

- Radius system.
- Border rules.
- Shadow/elevation rules.
- Container rules: when to use cards, panels, dividers, or whitespace only.

### Layout

- Page max width.
- Grid columns.
- Breakpoints.
- Mobile collapse rules.
- Standard section rhythms.
- Rules for hero fit, navigation wrapping, tables, long forms, and first-viewport priority when relevant.

### Interaction And States

- Default, hover, focus-visible, active, disabled, loading, empty, error, success.
- Motion duration and easing.
- Touch target minimums.
- Keyboard/focus rules.
- Reduced motion and reduced transparency behavior when the visual system uses motion, blur, or layered material.

## Component Seed

For implementation work, define the first reusable primitives before composing full screens:

- Button.
- Input/select/textarea.
- Label/help/error text.
- Card or panel only if the system needs one.
- Badge/status.
- Empty state.
- Loading skeleton.
- Page shell.

Each primitive should use foundation tokens. If a primitive needs a new value, add it to the foundation instead of hard-coding it.

Use `templates/primitive-spec.md` as a scaffold for primitives that become part of the reusable system. Keep only the sections that clarify repeatable behavior.

## Exceptions

One-off values are allowed only when:

- The exception is tied to a named product moment.
- It cannot be expressed by the existing system.
- The reason is written with the shape of `templates/exception-record.md` or the project's equivalent exception log.

Otherwise, the value belongs in the foundation or should not exist.

## No Guessing Rule

When a value is lockable, choose one of these paths:

1. Use an existing token or component rule.
2. Add a new token or component rule to the foundation template.
3. Record a named exception with scope and expiration.
4. Ask the user if the choice changes the product's visual identity.

Never invent a local value in a component and move on.
