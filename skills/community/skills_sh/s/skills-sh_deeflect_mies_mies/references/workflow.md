# Workflow

Load when: framing, composing, redesigning, or making a substantial design decision.

Mies work follows Interface Craft's sequence: notice, frame, explore range when needed, choose the simplest useful architecture, set the reusable foundation, compose the core surface, design states, reduce, tune, and verify in the real interface.

## Source Order

Before inventing a direction, inspect sources in this order:

1. Existing product design docs, tokens, components, screenshots, and shipped UI.
2. Platform and category conventions the user already expects.
3. Official design systems or packages when the brief maps to one.
4. Mies foundation choices for this product.
5. One-off exceptions, written down and scoped.

Do not recreate an official system by hand just to make it feel custom. Do not import a new system without checking the project dependencies and existing stack first.

## Frame

Use Frame when the task is open-ended, high-impact, new, or directionally ambiguous.

1. Establish context: product, user, task, emotional state, platform, constraints.
2. Name 3-5 facets of quality the result must be perceived to have.
3. Identify the register: brand or product.
4. State the anti-reference.
5. Write the scene: where, device, ambient context, urgency, and mood.
6. Run the divergence pass below before settling on a direction.
7. Decide scope: sketch, mid-fi, production-ready; one component, one screen, flow, or whole surface.
8. Choose the simplest useful architecture.
9. Decide whether the design foundation is new, inherited, or being revised.

### Divergence

The first design you picture for a brief is the statistically most likely one — the category default, the first-token answer. Building it produces competent slop. Width is a thinking discipline: generate broadly, then choose narrowly. Push off the default on purpose:

1. **State the default.** Write the design you would get from the category label alone: its hero, layout, palette, type, and motion. ("AI design tool" → near-black page, huge bold sans headline, terse manifesto copy.) This is the prediction to beat, and it is now banned.
2. **Name the clichés.** List the 2-3 category reflexes and AI-default looks specific to this exact brief. Don't match a fixed list; derive them from this subject.
3. **Generate structurally different directions** built from the actual scene, user state, subject materials, and brand character — not palette swaps. Vary architecture, density, media strategy, disclosure, interaction model, and emotional tone. Force range with these levers:
   - **Borrow a model from another domain** — a game, a physical product or tool, a Muji-like direction, a platform pattern, a real-world object or craft detail.
   - **Invert the job** — help the user eliminate, defer, compare, or confirm instead of create.
   - **Shift a constraint** — what if this were not a screen, happened automatically, or showed only the current step?
   - **Swap the structure** — list vs phases vs table vs contextual sheet vs dashboard vs direct-manipulation vs background process (see `patterns.md` for the moves each implies).
   - **Take a facet to its extreme** — what is the most calm, most durable, most expert, or most playful version?

   Generate a fixed count (2-3) before judging any of them.
4. **Choose what the brief earns** — not what is easiest to produce, and not novelty for its own sake. The simplest direction that serves the scene wins.

Do not anchor on a single external example up front; one reference becomes a template the model copies, which kills the divergence. Look at real work later, for craft-level calibration, never to set the direction.

**Optional — push to the less-obvious.** When the brief explicitly rewards surprise, or two directions are close and the safe one is the category default, deliberately take the less-expected direction and make it earn its place through craft. This is opt-in, not the default; restraint still governs the shipped result.

For unfamiliar interactions, build or describe a small isolated prototype before folding the idea into the product. Use rough fidelity when the question is mechanics; use higher fidelity only when the decision is visual trust or brand impression.

For clear work, use a compact frame:

```text
Frame: <what this is>, <who it serves>, <scene>, <facets>, <architecture>, <what gets removed or protected>.
```

If the user asked only for planning, stop after the frame and ask for confirmation. If the user asked to build and the frame is clear, proceed.

## Set

For new products, new visual systems, and redesigns, set the foundation before composing screens. Read `design-system.md`.

Lock:

- Vibe in 2-4 sentences.
- Character behind the design.
- Facets of quality.
- Tokens for color, type, spacing, radius, layout, depth, motion, and states.
- Copy voice: how the product sounds, person/tense/casing, and what it never says.
- First reusable primitives.

If an existing foundation exists, audit it and extend it. If none exists, create the smallest durable foundation needed for the current work.

## Compose

1. Inspect the existing project foundation before writing code. If the project is greenfield with no stack yet, choose the smallest stack that fits the surface — plain HTML/CSS for a static page or simple landing, the user's preferred framework or a minimal React/Vite setup for an app — and don't pull in heavy dependencies a single surface doesn't need.
2. Use the current framework, components, tokens, icon system, and vibe lock.
3. Check `package.json` before importing a new library.
4. Establish hierarchy before styling details.
5. Build the core state first.
6. Add the necessary states: empty, loading, error, success, disabled, focus, active, long content, and responsive behavior.
7. Add motion only when it clarifies state, continuity, or tactility.
8. Subtract anything that does not earn its place.
9. Write the copy as part of the surface, not after it — labels, actions, and every state's words, warm and clear with no AI tells (`copy.md`).
10. Tune spacing, type, color, alignment, and interaction.
11. Verify against your own eyes — this is a gate, not a nicety. Render it, screenshot desktop and mobile, and critique the result as if it were someone else's work (`critique.md`). If it reads generic, default, or like the banned category default, rework the structure — not the palette — and look again. Don't call the work done on an unrendered guess.

## Separate Concerns

Don't ask one pass to solve everything. Declare which question this pass answers — interaction model, interface architecture, information hierarchy, visual language, component design, motion, or polish — and match fidelity to it. A blank-card prototype can prove an interaction; a stakeholder review may need a shippable artifact. Resolving the wrong concern at high fidelity is wasted work.

## Depth

A working first pass is the floor, not the finish. Most work stops there; strong work keeps climbing quality levels.

- **Early depth:** fix obvious gaps, remove broken or redundant parts, resolve edge cases, establish hierarchy and basic interaction.
- **Later depth:** once the obvious fixes are handled, look for discovery, invention, and refinement — the move a merely competent version would not make. Compare variants side by side. Use real references to reveal gaps you have stopped seeing. Remove what is no longer earning its place.

Produce a deliberate refinement pass at the next quality level, not a rewrite.

## Redesign

Classify the redesign before changing anything:

- **Preserve**: modernize without breaking brand memory, routes, labels, legal copy, analytics-sensitive IDs, or accessibility wins.
- **Evolve**: keep the product and IA, but refine visual language, rhythm, components, and states.
- **Overhaul**: new visual language is allowed; content and user intent still need protection.

Audit first:

- Brand tokens and type.
- Design foundation and reusable primitives.
- Vibe and character already implied by the product.
- Existing IA and primary paths.
- Content that works.
- Patterns to preserve.
- Patterns to retire.
- Current density, expression, motion, familiarity, and warmth.
- SEO and analytics risk when relevant.

## Reduce

Refinement often means removal:

- Merge sibling cards into one stronger section.
- Remove repeated subtitles, labels, dividers, captions, and explanatory copy.
- Replace decorative containers with spacing and alignment.
- Hide complexity until needed.
- Make one interaction excellent instead of several interactions average.

## Final Care

Ask:

- Does this meet the industry bar?
- Does it express the chosen facets?
- Is anything generic, uncanny, or default-AI-looking?
- Could someone predict the result from the category name alone?
- Are overlooked states considered?
- Does the smallest detail feel intentional?
- Would a real user feel guided, respected, and confident?
