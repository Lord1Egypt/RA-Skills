# Refine

Load when: subtracting, tuning, proving production readiness, or doing a final pass.

If the work has a design foundation, judge against it. If it does not and the task is larger than a small fix, stop and create or request the foundation first.

## Subtract

The subtraction pass asks what can leave.

Audit:

- Redundant headings, subtitles, captions, labels, helper text.
- Repeated cards, repeated containers, repeated section layouts.
- Borders, dividers, shadows, and backgrounds that do not clarify grouping.
- Secondary actions competing with the primary action.
- Options that can become defaults.
- Content that can move behind progressive disclosure.
- Decoration pretending to be structure.
- Category-default furniture: repeated tiny labels, fake metrics, ornamental status dots, generic cards, and placeholder visuals.

Keep:

- What helps the user understand, decide, act, recover, or trust.
- What creates the necessary impression for brand work.
- What establishes useful rhythm or hierarchy.
- What makes an edge state humane.

Do not remove information users need to make a decision. Mystery is not minimalism.

Subtraction should increase clarity, not just lower object count. If removing something makes the user less confident, replace it with a better structure instead of pretending absence is elegance.

## Tune

After subtraction, tune what remains.

### Proportion And Spacing

- Use a small spacing scale.
- Use foundation spacing tokens instead of invented gaps.
- Make sibling spacing consistent unless hierarchy demands contrast.
- Check optical alignment, not just numeric alignment.
- Reserve weight for the primary subject/action.
- Make hover/focus/active states stable so layout does not shift.

### Type

- Reduce type roles.
- Use foundation type roles instead of new local styles.
- Make hierarchy readable in 3 seconds.
- Keep line length and line height humane.
- Prevent widows, cramped labels, clipped italics, and overlong buttons.

### Color And Material

- Give every color a job.
- Use foundation color roles instead of new hex values.
- Use one radius system or a documented radius rule.
- Use one icon family.
- Shadows and strokes should separate layers, not decorate them.
- Remove muddy depth and low-contrast text.
- Verify button text contrast, focus visibility, semantic color contrast, and disabled-state legibility.

### States

Every meaningful interactive element needs relevant:

- Default.
- Hover.
- Focus-visible.
- Active.
- Disabled.
- Loading.
- Empty.
- Error.
- Success.

Do not ship only the perfect happy path.

### Copy

- Cut throat-clearing, hedges, and words that restate what the UI shows.
- Replace AI-default marketing words and fake-warm microcopy with the plain, specific thing.
- Make errors and empty states name the specific situation and the next step.
- Keep one term per concept and consistent casing, tense, and person across the surface.
- For anything larger than a label tweak, run Word's full pass (`copy.md`).

## Precision

The standard is exact, not approximate. The imagined hand treats a one-pixel drift or a stray hardcoded value as a defect, verifies at high zoom instead of trusting a glance, and refuses "close enough."

### Pixel-level

- Optical alignment over numeric: align to what the eye reads — cap height, glyph edges, icon mass — not just bounding boxes.
- Every spacing, size, and radius comes from the scale; no arbitrary 13px or 7px drift.
- Nested radius stays concentric: inner radius = outer radius − padding.
- Hairlines render as true 1px at the device pixel ratio; no blurred half-pixel borders or shadows.
- Icons share optical size, stroke width, and baseline; align icon to text by optical center, not box.
- Text baselines align across columns; no widows, no clipped descenders or italics, no off-by-one in line-height rhythm.
- Use even dimensions where centering must stay crisp; avoid fractional sizes that soften edges.
- Assets are crisp at 1x and 2x; no upscaled raster, no SVG smeared by non-integer transforms.

### Code-level

- Values come from tokens, not magic numbers inlined at the call site.
- One unit system; don't mix px/rem/em without reason; round to device pixels where crispness matters.
- No dead styles, no redundant wrappers, no z-index soup, no `!important` patches.
- Animate transform and opacity; never animate layout properties that cause reflow.
- Semantic HTML and stable layout: reserve space so nothing jumps as state or data loads.
- Hover, focus, and active states change paint, not layout — no one-pixel nudge on hover.
- Consistent naming and structure; the next reader should not have to reverse-engineer intent.

## Prove

A design is not finished until it survives reality.

Check:

- Long text, short text, missing text.
- Many items, one item, no items.
- Large numbers and weird-but-real values.
- Mobile widths, tablet widths, desktop widths.
- First viewport fit for brand pages and primary task visibility for product pages.
- Navigation wrapping, table overflow, long button labels, and clipped display type.
- Keyboard navigation and focus order.
- Touch targets.
- Contrast.
- Reduced motion.
- Slow network and failed network.
- Permission errors and validation errors.
- Localization expansion and RTL risk when relevant.

Use semantic HTML, labels, alt text, landmarks, and accessible names. Restraint never excuses inaccessible UI.

## Mies Preflight

Before final, answer:

- What was removed?
- What survived, and why?
- What is the primary action or subject?
- Does visual weight match importance?
- Does the register fit?
- Is there one coherent type, color, icon, radius, and spacing system?
- Does every new value come from the foundation, or is the exception documented?
- Does the result still match the vibe and character lock?
- Does anything look like AI filler, in pixels or in words?
- Is the copy warm, clear, specific, and free of AI tells, with every state's words written?
- Is it pixel- and code-exact: aligned to the scale, crisp at the device pixel ratio, no magic numbers, no layout shift?
- Did the category-reflex check pass?
- What small detail proves a human thought about actual use?
- What was verified in build, browser, screenshot, or targeted review?
