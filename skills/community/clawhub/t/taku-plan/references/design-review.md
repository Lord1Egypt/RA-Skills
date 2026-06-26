---
name: taku-design-review
description: >
  Use when a plan has UI/UX components that need design quality scoring — aesthetic,
  typography, color, spacing, layout, motion, responsiveness, accessibility, and
  content hierarchy. Triggers on "design review", "does this look good", "rate the
  design", "design critique", or when plan-phase UI decisions need evaluation.
---

# taku-design-review — Design Dimension Scoring

A design review that scores, not opines. Each dimension gets a number, an explanation of what perfection looks like, and a specific fix to close the gap.

## Why This Matters

"Looks good" is not a design review. Neither is "I don't like the color." Design quality is measurable across specific dimensions. This skill forces that measurement, explains the gap between current and ideal, and produces actionable fixes the implementer can apply.

**Why score numerically:** Numbers create accountability. "The typography needs work" is forgettable. "Typography scores 4/10 because no type scale is defined" demands action. Numbers also enable comparison: the before-score vs. after-score shows whether the revision actually improved things.

## The 9 Dimensions

Rate each 0-10. For anything below 8, explain what a 10 looks like and write the specific fix into the plan.

### 1. Aesthetic (0-10)
Does the design have a coherent visual personality, or does it look like a template?

**What a 10 looks like:** Every visual choice serves the product's identity. No element feels generic or borrowed. The design is recognizable as THIS product, not "a SaaS app."

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 2. Typography (0-10)
Are type choices intentional? Hierarchy, weight, size, spacing, line height — all specified?

**What a 10 looks like:** Exact typeface named for primary and secondary. Size scale defined. Heading/body contrast ratio >= 1.5x. Line height specified for body (1.5-1.6) and headings (1.1-1.2). No default system fonts as identity font.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 3. Color (0-10)
Is the color system complete with tokens, dark mode, and WCAG AA contrast?

**What a 10 looks like:** All colors defined as CSS variables. Dark mode variants specified. Contrast ratios verified (4.5:1 for body text, 3:1 for large text). Accent color used sparingly, not everywhere. No purple-on-white defaults.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 4. Spacing (0-10)
Is there a consistent spacing scale, or are values arbitrary?

**What a 10 looks like:** Base unit defined (4px or 8px). Spacing scale: 4/8/12/16/24/32/48/64/96. All padding, margins, and gaps use values from this scale. No magic numbers like `margin: 17px`.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 5. Layout (0-10)
Does the layout have intentional structure, or is it "stuff on a page"?

**What a 10 looks like:** Grid system defined (columns, gutters, max-width). Each section has one clear purpose. Visual hierarchy guides the eye: primary content first, secondary second, tertiary third. No competing focal points.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 6. Motion (0-10)
Is animation intentional and performant, or absent/indiscriminate?

**What a 10 looks like:** Transition durations defined (150/300/500ms). Easing curves specified. Animations serve hierarchy (drawing attention, indicating state change), not decoration. `prefers-reduced-motion` respected. Nothing animates just because it can.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 7. Responsiveness (0-10)
Is each viewport intentionally designed, or is mobile just "stacked columns"?

**What a 10 looks like:** Breakpoints defined with layout behavior per breakpoint (not "responsive"). Mobile layout designed separately, not just desktop squished. Touch targets >= 44px. Navigation adapts (not just hamburger). Images resize appropriately.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 8. Accessibility (0-10)
Can everyone use this, or is it designed for one specific user profile?

**What a 10 looks like:** Keyboard navigation works for all interactions. ARIA landmarks defined. Screen reader tested (logical heading order, alt text, form labels). Color contrast meets WCAG AA. Focus states visible. No content conveyed by color alone.

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

### 9. Content Hierarchy (0-10)
Does the user know what to look at first, second, third?

**What a 10 looks like:** Every screen has clear visual hierarchy. One primary action per view. Headings are scannable without reading body text. Information is layered: essential first, details on demand. Empty states designed (warm, helpful, actionable).

**Score N because:** [specific observation]

**Fix:** [specific change to the plan]

## Output Format

```
DESIGN REVIEW SCORECARD
═══════════════════════════════════════════
Dimension          | Score | What 10 Looks Like           | Fix
───────────────────|───────|──────────────────────────────|─────────────
Aesthetic          |  N/10 | ...                          | ...
Typography         |  N/10 | ...                          | ...
Color              |  N/10 | ...                          | ...
Spacing            |  N/10 | ...                          | ...
Layout             |  N/10 | ...                          | ...
Motion             |  N/10 | ...                          | ...
Responsiveness     |  N/10 | ...                          | ...
Accessibility      |  N/10 | ...                          | ...
Content Hierarchy  |  N/10 | ...                          | ...
═══════════════════════════════════════════
OVERALL: N/10
```

For dimensions scoring 8+, a brief note is fine. For dimensions below 8, the fix must be specific enough for the implementer to act on without asking questions.

**Why the 8+ threshold:** Scoring 8+ means the dimension is solid enough that only minor polish could improve it. Below 8 means there's a meaningful gap that will be visible to users. The fix must be specific because vague guidance ("improve the spacing") produces vague implementation.

## Known Pitfalls

**Scoring everything 7-8 without genuine analysis.** All nine dimensions scored 7 or 8. The scorecard looks balanced but reveals nothing. No dimension was strong enough to praise, no dimension was weak enough to flag. This is the "Gentleman's C" of design reviews — it passes everyone without teaching anything.

*What went wrong:* The reviewer didn't want to be negative. Every dimension got a safe score with vague observations like "could be slightly more intentional." No actionable fixes were produced.

*Prevention:* For anything below 8, the "What a 10 looks like" and "Fix" fields must be specific enough that the implementer can act without asking questions. If you can't write a specific fix, you haven't understood the gap well enough to score it. Scores without specific observations are guesses, not evaluations.

**Reviewing without a design system to calibrate against.** The review scored Typography 6/10 with "no clear type hierarchy." But the project never defined a type hierarchy in the first place. The fix said "define a type hierarchy" — which is a design task, not a review finding.

*What went wrong:* Design review is meant to evaluate a plan against its own stated intentions. Scoring against an unstated ideal produces findings that are really new design requirements, not review feedback.

*Prevention:* If the plan doesn't specify typography choices, the correct finding is "Typography is undefined" with a fix that says "Define typeface, size scale, and heading hierarchy before implementation." Don't score what doesn't exist — flag the gap.

**Treating the scorecard as the final deliverable.** Nine scores were produced, the overall was 8.2, and the review was declared "done." But three dimensions had fixes that contradicted each other (Motion said "add transitions everywhere" while Accessibility said "respect reduced motion"). The implementer was left with conflicting instructions.

*What went wrong:* Dimensions were scored in isolation without cross-referencing fixes for conflicts.

*Prevention:* After scoring all nine dimensions, scan fixes for contradictions. If Motion recommends animations that Accessibility flags, note the tension and recommend a resolution. The scorecard is analysis; synthesis is the actual deliverable.

## Completion

Append a `## Design Review` section to `DESIGN.md` with the scorecard and all fixes. Do NOT put design review output in `PLAN.md` — the plan document is execution-only.

If overall score is 8+: "Design is implementation-ready."

If overall score is below 8: "Design needs revision. Address the fixes above before proceeding to build."

Status: DONE when all 9 dimensions are scored and fixes are written into the plan. DONE_WITH_CONCERNS if the user deferred fixes. BLOCKED if no design exists to review.
