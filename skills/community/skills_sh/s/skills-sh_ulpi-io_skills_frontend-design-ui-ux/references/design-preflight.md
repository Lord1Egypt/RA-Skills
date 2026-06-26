# Design Pre-Flight Gate

Run this BEFORE declaring a design spec done (Step 6). Several items are mechanical counts — count,
don't eyeball.

> If a single box cannot be honestly ticked, the design is not done. Fix it, then re-run.

## Identity lock (consistency)

- [ ] Every screen/component uses ONLY values from the locked `DESIGN.md` (palette, type, spacing,
      radius, motion). Off-system values: **0**.
- [ ] One accent, one radius scale, one icon family, one type pairing across the whole project.
- [ ] Identity-lock holds: all screens read as the SAME product placed side by side.
- [ ] (Multi-feature / multi-session) `DESIGN.md` was re-read first; no drift introduced.

## Anti-slop (distinctiveness)

- [ ] **0** banned fonts; **0** banned color clichés (purple glow, cream default, gradient text).
- [ ] **0** banned layout patterns (3 equal cards, nested cards, eyebrow numbering, default centered-dark hero).
- [ ] **0** buzzwords, **0** fake names, **0** fake-precise numbers, **0** em-dashes in any visible copy.
- [ ] The **slop test** passes: no one could say "AI made that" with certainty.
- [ ] The **counterfactual test** passed: this is not the look I'd produce for ANY similar brief.
- [ ] The **Signature** element is present and embodies the brief.
- [ ] If inspiration links were used: the output **synthesizes** them — it does not clone any single reference.

## State & flow coverage (our moat — keep it)

- [ ] Every interactive element specs loading / empty / error states, not just the happy path.
- [ ] Flows cover edge cases (refresh mid-flow, session expiry, back, offline) where relevant.

## Accessibility (our moat — keep it)

- [ ] Contrast ratios are listed and pass WCAG AA (4.5:1 text / 3:1 large text + UI).
- [ ] Visible keyboard focus; full keyboard path documented.
- [ ] `prefers-reduced-motion` handled; motion is motivated.
- [ ] ARIA roles / screen-reader announcements specified for non-trivial components.
- [ ] (Mobile) touch targets ≥ 44pt (iOS) / 48dp (Android); safe areas respected.

## Layout craft

- [ ] ≥ 3 distinct layout families across a multi-section page (no monotonous repetition).
- [ ] Clear hierarchy; whitespace used deliberately; one focal point per view.

## Cognitive load (working memory ≈ 4)

- [ ] Primary nav ≤ ~5 top-level items; a form group ≤ ~4 fields; pricing ≤ 3 tiers; choices per
      decision kept small. Chunk or progressively disclose anything larger.
- [ ] Exactly one primary action per view; secondary actions visibly subordinate.

## Scored self-critique (calibrate — don't rubber-stamp)

Score the design 0–4 on each axis. Be honest: a **4 means genuinely excellent**; most real work lands
2–3. Axes: distinctiveness · hierarchy & focus · consistency with `DESIGN.md` · accessibility ·
state/edge coverage · copy quality · restraint (no decoration without meaning) · motion motivation.

- [ ] Total recorded (max 32). Any axis **≤ 2 → name the specific fix, apply it, and re-score.**
- [ ] Revise-and-justify: for every change made at this gate, state in one line WHAT changed and WHY.
      Do not hand off with an un-actioned axis ≤ 2.
