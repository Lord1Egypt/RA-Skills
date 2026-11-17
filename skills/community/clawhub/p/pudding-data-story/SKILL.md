---
name: pudding-data-story
description: Build or revise reader-first interactive data stories and visual essays in the spirit of The Pudding. Use for Pudding-style websites, scrollytelling, scroll-driven graphics, interactive data journalism, data-backed longform features, animated visual explanations, storyboards, or audits of work that feels like a dashboard or ordinary chart. Also trigger for 中文 requests mentioning 数据叙事、滚动叙事、交互可视化、动态数据故事、Pudding 水准, or “不要像普通图表”. Covers editorial framing, data receipts, visual form, meaningful interaction, motion, implementation architecture, accessibility, mobile behavior, and QA.
---

# Pudding Data Story

Create visual journalism in which the reader experiences an argument through evidence. Treat motion and interaction as explanatory grammar, not decoration.

Base new standalone work on The Pudding's official website starter when its stack fits. In an existing codebase, preserve the stack and port the starter's patterns instead of replacing the application.

## Start with the editorial gate

Do not begin with a chart type or animation. Establish:

- the driving question;
- a one-sentence thesis that the available data can support;
- what the reader should notice, understand, or reconsider;
- one concrete person, place, object, or event that can open the story;
- the data needed for every factual claim;
- why this story is better seen or experienced than merely written.

Reject or reframe a concept if it is only “a dashboard about X,” a tour of available metrics, or a generic trend recap. A strong story has an argument, human stakes, and a visual reason to exist.

Write to the reader. Never expose the design brief in published copy. Remove phrases such as “this visualization demonstrates,” “push the data,” “choose a lens,” “same group of particles,” “这里展示,” “推动数据,” or “观察镜头” unless the interface literally requires that instruction.

Read [references/editorial-workflow.md](references/editorial-workflow.md) before drafting the story structure.
For AI model, training-cost, benchmark, or capability stories, also read [references/ai-data-evidence.md](references/ai-data-evidence.md).

## Verify the evidence

Build a claim-to-source ledger before implementation:

| Claim or scene | Measure | Grain | Time range | Source | Transformation | Caveat |
|---|---|---|---|---|---|---|

For every derived value, preserve units, denominator, missing-value treatment, filters, and calculation. Label estimates and incomplete coverage in the same visual state where they appear. Keep methodology and data downloads accessible without interrupting the main narrative.

If data is missing, stale, contradictory, or too coarse for the proposed claim, stop and narrow the claim. Do not animate uncertainty away.

## Storyboard before coding

Use the sequence:

1. **Concrete opening** — begin with a specific example the reader can grasp.
2. **Reveal** — show the first surprising relationship with minimal annotation.
3. **Zoom out** — place the example inside the full dataset.
4. **Mechanism** — explain why the pattern happens.
5. **Agency** — let the reader search, compare, simulate, or contribute when that action answers a real question.
6. **Stakes** — connect the pattern to people or consequences.
7. **Resolution** — return to the thesis with limits and a useful next thought.

For every beat, specify:

| Beat | Reader-facing copy | Evidence | Visual state | Reader action | Transition meaning |
|---|---|---|---|---|---|

One scroll step should make one claim. Scrollytelling is not a slideshow of chart types.

## Match visual form to the argument

Choose encodings from the comparison the reader must make:

- change over time → line, connected position, or animated trajectory;
- distribution or uncertainty → dots, density, interval, or simulation;
- part-to-whole → aligned bars or area only when precise comparison is not central;
- flow or transformation → sankey, alluvial, or stable marks that move between states;
- geography → map only when location explains the pattern;
- sequence or conversation → synchronized timeline;
- friction or constraints → simulation or playable model when the interaction embodies the thesis;
- individual examples within a population → concrete-first small multiple, beeswarm, or searchable field.

Preserve object constancy only for the same semantic entities. Do not morph unrelated metrics into “the same particles.” Avoid chart carousels, gratuitous 3D, decorative network graphs, and motion that adds no meaning.

Read [references/interaction-patterns.md](references/interaction-patterns.md) when selecting a visual or interaction.

## Use motion as a sentence

Every transition must answer one of:

- What changed?
- Where did this item go?
- How does this subset differ?
- What happens under this assumption?
- How does a specific example relate to the whole?

Prefer stable marks that move, sort, aggregate, split, or annotate. Use fades only as support. Avoid ambient loops after the reader has understood the state.

Scrolling backward must restore the prior state. Keep transitions interruptible. Respect `prefers-reduced-motion`; reduced motion must preserve the explanation through direct state changes, not remove content.

## Make interaction earn its place

An interaction belongs only if it lets the reader:

- find themselves or a meaningful example;
- compare alternatives;
- test a causal or policy mechanism;
- inspect evidence that would clutter the default view;
- contribute data to a clearly explained experiment.

Provide a meaningful default state. Label controls in audience language. Do not make readers click merely to continue reading, and do not hijack wheel, trackpad, touch, or keyboard behavior.

Search, filter, scrub, sort, and simulation controls must change real data dimensions. A control that only swaps decorative scenes should be removed or turned into authored scroll progression.

## Implement with the official-template model

For a new Svelte story, inspect the current state of [The Pudding website starter](https://github.com/the-pudding/website) before copying patterns; it is an active Svelte migration. Use its architecture as the default:

- preprocessed CSV/JSON/SVG imports;
- Svelte components and stores for viewport/scroll state;
- a reusable `Scrolly` component;
- CSS `position: sticky` for the graphic;
- IntersectionObserver or Scrollama for discrete steps;
- D3/LayerCake for custom marks, scales, and layout;
- static/SSR output where practical;
- ArchieML or an equivalent content workflow when editors need structured copy.

For React, Next.js, Sites, or another existing stack, reproduce the same separation of concerns:

1. normalized data;
2. derived story states;
3. a pure visual renderer;
4. scroll/interaction state;
5. reader-facing copy;
6. methods and sources.

Do not reproduce The Pudding's logo, house fonts, or visual identity. The official starter is MIT-licensed, but its README explicitly excludes brand assets.

Read [references/technical-template.md](references/technical-template.md) before implementation.

## Build mobile and accessibility in from the first state

- Use semantic headings and a linear reading order that works without animation.
- Provide keyboard access and visible focus for every control.
- Give SVG graphics an accessible name and a concise text takeaway.
- Use color plus another cue; never color alone.
- Make touch targets at least 44 CSS pixels.
- Avoid fixed `100vh` scrolly geometry on mobile browser chrome; prefer content-driven sizing and `svh`/`dvh` with fallbacks.
- Ensure sticky graphics do not cover text or trap interactive controls.
- Provide a static or step-based fallback when sticky positioning or observers fail.
- Test 320 px, 768 px, and wide desktop layouts, plus portrait and landscape.

## Quality gates

Before declaring the story complete:

1. Run `python scripts/audit_story.py <project-or-story-file>`.
2. Read every visible sentence as a reader; remove production language and design rationale.
3. Verify every displayed number against the source or transformation.
4. Scroll down and back up slowly and quickly; test refresh at a mid-story URL position.
5. Use every control with mouse, keyboard, and touch-size viewport.
6. Test reduced motion and a no-JavaScript or failed-observer fallback.
7. Check that the opening, central reveal, and ending remain understandable in screenshots.
8. Verify performance on a mid-range mobile profile; avoid per-frame DOM churn.

Use [references/pudding-examples.md](references/pudding-examples.md) as a pattern library, not a style catalog. Copy the editorial logic, not the surface.

## Required handoff

Deliver:

- `story-brief.md` — question, thesis, audience, human opening, visual reason;
- `data-notes.md` — sources, transformations, caveats, claim ledger;
- `storyboard.md` — beat-by-beat copy, evidence, state, interaction, transition;
- the implemented story;
- `qa-notes.md` — device, accessibility, interaction, and data checks.

Use the copy-ready structures in [references/deliverable-templates.md](references/deliverable-templates.md). Do not leave a template field blank without explaining why it does not apply.

When revising an existing story, diagnose it against these gates first, then make the smallest structural changes that materially improve the reader's experience.
