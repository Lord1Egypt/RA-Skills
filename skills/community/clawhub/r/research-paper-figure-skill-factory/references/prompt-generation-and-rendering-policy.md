# Prompt Generation and Rendering Policy

Version: 1.0.1

## Prompt Construction Order

1. Figure thesis
2. Paper slot and audience
3. Canvas and layout
4. Panel choreography
5. Required objects, modules, stages, or evidence elements
6. Label strategy
7. Visual rhetoric
8. Style family
9. Color semantics
10. Sample/reference-image transfer rules
11. Negative constraints
12. Candidate count and varied axis

## Candidate-Board Prompt Boundary

Generated skills must distinguish two prompt types:

- **P4 candidate-board brief:** low-commitment visual comparison for choosing direction after text candidates.
- **P7 final image brief:** formal prompt for the selected direction after the user has reviewed and locked/revised a visual candidate.

Do not use the final image brief as a substitute for the candidate-board step. After 4-6 text candidates, the generated skill must set up and then generate/display candidate images before direction lock unless the user explicitly skips image candidates.

## Candidate-Board Setup Template

```text
Board purpose:
Generate candidate images or schematic candidates for choosing a figure direction, not a final figure.

Candidate count:
<4/5/6; default 6>

Hold fixed:
<paper thesis, target slot, required modules, exact labels, color semantics, sample-image transfer rules>

Vary only:
<subtype / scheme / layout / style / metaphor / density / prompt framing>

Compare:
<what the user should choose by looking at the images>

Rendering route:
ChatGPT web: Create image through ChatGPT Images 2.0.
Codex: $imagegen first; if unavailable, ChatGPT Images 2.0 API or another approved image-generation API.
```

The setup turn is `TEXT_ONLY` and must stop before generation.

## Final Image Brief Template

```text
Create a publication-ready scientific figure for a research paper.

Goal / figure thesis:
<one sentence>

Paper slot and audience:
<introduction / method / results / appendix / rebuttal / slides>

Canvas and layout:
<aspect ratio, panel count, reading order>

Panel content:
Panel A: ...
Panel B: ...
Panel C: ...

Labels:
Use only these exact short labels: <list>.

Sample-image transfer:
<per-image attributes to borrow, or none>

Style and color semantics:
<style family, palette role, what each color means>

Candidate variation:
Generate <4/5/6> candidates, usually 6. Vary only <axis>.

Avoid:
long paragraphs, unreadable labels, fake metrics, logos, watermarks, decorative clutter, SVG/Mermaid/TikZ/Graphviz/code-rendered diagram instructions.
```

## Rendering Route

Candidate boards, draft candidates, final visuals, and revisions must use native image generation:

1. ChatGPT web: Create image through ChatGPT Images 2.0.
2. Codex: `$imagegen` first.
3. Codex fallback: ChatGPT Images 2.0 API or another approved image-generation API.

Allowed bitmap outputs from that route: PNG, JPG, JPEG, WebP.

Forbidden visual outputs/fallbacks: SVG, Mermaid, TikZ, Graphviz, HTML/CSS diagrams, canvas diagrams, matplotlib/code-generated figures, filesystem image exports produced by local code or scripts.

If image generation is unavailable, stop and provide a prompt handoff. Do not substitute code-rendered figures.

## Turn-Level Separation

- P4 and P7 are `TEXT_ONLY`; they may prepare prompts but must not generate images.
- P5 and P8 are `IMAGE_ONLY`; they must contain image generation only.
- The next text reply after P5 or P8 must record the image batch in state.
- The first/startup reply must never generate images.
