# Design Quality Rubric

Use this rubric when a user asks for a high-design HTML deck, roadshow deck, polished presentation, or says the output feels ordinary.

The goal is not decoration. The goal is a presentation that looks authored, intentional, credible, and performable.

## How To Use

Before implementation:

1. Write the audience decision.
2. Write the story spine.
3. Write the deck-level visual thesis.
4. Choose 3-5 layout patterns from `layout-pattern-library.md`.
5. Define the evidence layer: screenshots, source pages, charts, videos, reports, or appendices.

After implementation:

1. Score the deck from 0-100.
2. Fix any gate failure before delivery.
3. If the score is below 80, revise the story, composition, or evidence treatment before tuning colors.

## Hard Gates

If any hard gate fails, the deck is not ready.

- **Information gate**: confirmed source facts, numbers, charts, or claims are omitted or silently changed with no appendix or source view.
- **Audience gate**: the deck does not make clear what the audience should believe or do next.
- **Layout gate**: most pages use the same title-plus-cards structure without a purposeful reason.
- **Evidence gate**: generated material is presented as real proof, or a simulated chart, fictional case, generated evidence-like artifact, or easily mistaken data lacks an adjacent `示意 / 模拟 / 待核实` label. Ordinary creative supplements disclosed in the delivery verification list do not fail this gate merely because the user did not supply them.
- **Handoff gate**: creative supplements are not covered by a structured `《待核实内容清单》`. This makes the full workflow conditional, while an otherwise usable HTML artifact may still pass its design and technical gates.
- **Operation gate**: live presentation flow depends on hover, tiny mouse targets, or interactions a clicker cannot operate.
- **Portability gate**: the HTML references absolute local files, temp files, WeChat cache files, or missing assets.
- **Overflow gate**: text overlaps, spills out of containers, or leaves the 16:9 canvas at 1600x900.

## 100-Point Score

### 1. Story And Persuasion - 20 points

- 0-5: The deck is a list of topics.
- 6-10: The deck has sections, but the order does not earn the conclusion.
- 11-15: The deck has a clear problem, proof, mechanism, method, and action.
- 16-20: The deck creates a controlled change in audience belief with strong section openings and closings.

Check:

- Does the opening begin with a concrete change, tension, or scene?
- Does the deck delay definition until the problem is visible?
- Does each section end with a "so what" that naturally opens the next section?
- Is the sales or CTA page earned by diagnosis, mechanism, and proof?

### 2. Slide Role Clarity - 12 points

- 0-3: Slides mix too many jobs.
- 4-6: Roles exist, but several pages still feel interchangeable.
- 7-9: Most pages have one clear job.
- 10-12: Every page has a distinct role and the sequence feels rehearsable.

Check:

- Can each page be named as opener, evidence, mechanism, framework, case, workflow, offer, or close?
- If two adjacent pages look similar, do they intentionally show a sequence?
- Is dense content split across staged reveals or multiple pages?

### 3. Visual Thesis And Originality - 15 points

- 0-4: The deck is decorated but has no visual idea.
- 5-8: A style exists, but it is mostly color and card styling.
- 9-12: A clear visual metaphor guides composition and motifs.
- 13-15: The subject has been turned into a memorable visual world.

Check:

- Can the visual thesis be stated in one sentence?
- Does the thesis fit the subject matter, not just the user's favorite palette?
- Do motifs repeat with purpose: grid, ruler, data panel, document slice, map, console, timeline, cutaway?
- Does the design avoid looking like a template?

### 4. Composition And Hierarchy - 15 points

- 0-4: Pages are evenly filled and low-risk.
- 5-8: Some pages have hierarchy, but many are still flat.
- 9-12: Most pages have strong focal points and controlled secondary information.
- 13-15: The deck uses confident scale, asymmetry, contrast, whitespace, and rhythm.

Check:

- Is there a dominant object or statement on each key page?
- Are titles large enough when they should carry the stage?
- Are labels small and disciplined instead of competing with the headline?
- Do dense evidence pages have guided attention through callouts or cropping?

### 5. Evidence Treatment - 12 points

- 0-3: Evidence is absent or rewritten into vague summaries.
- 4-6: Evidence appears, but is too small, dumped, or decorative.
- 7-9: Evidence is readable, cropped, framed, and interpreted.
- 10-12: Evidence feels like a live artifact: source view, modal, slice, zoom, scroll, or case teardown.

Check:

- Does the audience see the original proof when credibility matters?
- Are charts and screenshots large enough to inspect?
- Are original pages available through source buttons, appendix, or downloadable files?
- Are interpretation and source facts visually separated?

### 6. Motion And Presenter Flow - 10 points

- 0-3: Motion is absent where sequence matters, or decorative where it distracts.
- 4-6: Some reveals work, but the presenter flow is uneven.
- 7-8: Clicker-driven staging supports the explanation.
- 9-10: Motion creates tension, focus, comparison, or proof without hurting readability.

Check:

- Does each click reveal the next spoken point?
- Does a staged slide show its complete final state before moving on?
- Do slides preserve and restore their prior reveal state when returning?
- Do videos open only when the presenter chooses and stop when closed?

### 7. Visual Finish - 8 points

- 0-2: Inconsistent spacing, type, borders, colors, or shadows.
- 3-5: Mostly consistent but still rough in details.
- 6-7: Polished component system and spacing.
- 8: Production-level finish.

Check:

- Are margins, labels, page numbers, and controls consistent?
- Are buttons and controls styled as part of the deck?
- Are type sizes stable and not viewport-scaled?
- Are colors balanced rather than one-note?

### 8. Technical Reliability - 8 points

- 0-2: Navigation, assets, or layout break.
- 3-5: Main flow works, but packaging or QA is incomplete.
- 6-7: Local deck works, assets are portable, and core QA passes.
- 8: Deck is packaged, checked, and ready to run on another computer.

Check:

- Does it pass `check_assets.py`?
- Does it pass `check_html_deck.py` at 1600x900?
- Does the zip contain the HTML and all assets?
- Does the first page, a dense page, a media page, and the final page render correctly?

## Score Bands

- **90-100**: High-design roadshow quality. Use for paid presentations, launches, or important clients.
- **80-89**: Strong professional quality. Deliverable after small polish.
- **70-79**: Usable but not premium. Fix weak composition, evidence, or section rhythm.
- **60-69**: Ordinary report. Likely title + cards, weak visual thesis, or thin proof.
- **Below 60**: Rebuild the story spine and visual system before continuing.

## Fast Diagnosis

If the deck feels ordinary:

1. Stop tuning colors.
2. Re-name each page role.
3. Replace repeated card grids with different layout patterns.
4. Add real evidence or source view.
5. Create one oversized focal moment per section.
6. Re-run this rubric.

If the deck feels cluttered:

1. Split dense pages into opener, evidence, and implication.
2. Move source detail into modal or appendix.
3. Reduce body copy on the slide and move explanation into speaker notes.
4. Use staged reveals.

If the deck feels stylish but unconvincing:

1. Add original artifacts where credibility depends on source proof.
2. Add exact sourced numbers or explicitly tracked projected values.
3. Separate source proof, interpretation, and creative supplements.
4. Add boundary language before the offer and complete the delivery verification list.
