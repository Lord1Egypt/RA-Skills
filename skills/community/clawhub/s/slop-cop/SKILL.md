---
name: slop-cop
description: Judges visual design assets and AI-generated images before they ship, including layout defects, hallucinated text, and semantic consistency between copy and visuals/data.
---

# slop-cop

A visual-design referee. Given one or more image assets plus a decision context, produce strict per-asset verdicts (`SHIP`, `FIX`, or `KILL`) and, when multiple candidates compete for one slot, a ranked recommendation with placement reasoning.

The goal: stop hallucinated text, melted hands, off-brand vibes, layout overflow, misleading chart/copy mismatches, and obvious AI artifacts from reaching production.

## When to invoke

- User has 1–N images and a decision to make ("which works best for hero?", "is this safe to ship?", "does this fit my brand?").
- User wants a second opinion on a visual choice before deploy.
- User asks to audit a landing page or compare AI-generated variants.
- User explicitly says "slop check" / "is this AI slop?"
- User asks whether a marketing creative, email preview, dashboard mock, chart, graph, or KPI visual is truthful/presentable.

## Inputs the skill needs

Before analysis, confirm or infer:

1. **Image paths** — 1 or more local file paths or URLs.
2. **Decision context** — what slot/role is this for? Examples: `"hero banner at 1200x600"`, `"square avatar 1024x1024"`, `"mobile card at 4:5"`, `"is this safe to ship anywhere?"`.
3. **Target render size / aspect ratio** — if relevant.
4. **Brand palette / style** — hex colors and a one-line style descriptor when available.
5. **Mode** — single-asset audit (`SHIP/FIX/KILL`) or comparative pick (rank + recommend one).

If the user does not provide brand context, proceed without brand-fit scoring and note it in the verdict. Do not ask for brand context if the primary question is about layout, artifacts, or semantic correctness.

## Workflow

### 1. Inspect the actual image first

Before trusting a vision model, open or render the image yourself using the available image/file preview path (`read` on image files in OpenClaw, screenshot preview, or equivalent). Look for obvious human-visible defects:

- Text outside boxes/buttons/cards.
- Text clipped by crop/canvas/card boundaries.
- Overlapping cards/squircles/buttons/graphs.
- Elements visually sitting on top of unrelated elements.
- Giant accidental whitespace or broken screenshot framing.
- CTA text not contained inside the CTA shape.
- Misaligned dashboard/chart/card layers.

If you can see a defect in the rendered image, the vision model is not allowed to overrule it.

### 2. Run the vision pass

For each image, call the OpenClaw `image` tool with the strict checklist prompt in [references/vision-prompt-template.md](references/vision-prompt-template.md). Pass one image per call when possible. Use multi-image calls only for explicit side-by-side comparison once each has been individually vetted.

The prompt forces the vision model to enumerate findings against a fixed checklist instead of writing vibes-based prose.

### 3. Score against the full checklist

The mandatory checklist lives in [references/checklist.md](references/checklist.md). Every asset must be scored on:

- **Hallucination scan** — gibberish text, misspellings, extra/melted fingers, broken anatomy, duplicated objects, watermarks, AI signatures, lighting contradictions.
- **Layout containment** — all text must stay inside its intended button/card/squircle/container; no overlaps; no clipping; no accidental giant whitespace.
- **Semantic consistency** — visible claims must match visible evidence. If copy says a metric is trending down, the chart line must visually trend down. If copy says growth, the graph/KPI/direction must support growth. If button says an action, surrounding context must not imply a different action. If a dashboard card labels CPL/ROAS/booked calls, the visual trend and numbers must not contradict the label.
- **Legibility at target size** — can any text on the asset be read at its actual render size?
- **Responsive safety** — will the focal subject survive cropping to 16:9, 4:5, 1:1, and 9:16? Identify the focal point in pixel/percent terms.
- **Cross-browser / format** — transparency needs (PNG/WEBP vs JPG), color profile concerns (sRGB vs P3), iOS Safari quirks.
- **Brand fit** — if palette/style provided, check coherence; flag major mismatches.
- **Format / size sanity** — actual dimensions, file size for web, aspect-ratio fit for the target slot.

### 4. Assign a verdict per asset

Use exactly one verdict word per asset, plus a one-sentence reason. No hedging, no "looks okay but...".

| Verdict | Meaning |
|---------|---------|
| `SHIP`  | Clean. Deploy as-is. |
| `FIX`   | Salvageable with a specific edit (crop, recolor, regenerate text region, swap to different aspect, change copy/chart). State the fix. |
| `KILL`  | Do not use. Hallucination, broken layout, misleading semantics, off-brand, or wrong-tool-for-the-job. |

**Hard kill triggers** (any one = automatic `KILL`):

- Visible hallucinated/gibberish text on a graphic shipping to prod.
- Extra/missing/melted fingers on a human or human-adjacent character.
- Visible watermark or AI-tool signature.
- Major brand-palette violation (when palette provided) that cannot be fixed by recolor.
- Text visibly overflowing outside its intended box/button/card/squircle.
- Cards/buttons/graphs visibly overlapping unrelated content.
- Copy contradicts the visible chart/data/graph direction. Example: copy says "Cost per lead trending down" while the plotted line trends sideways or upward.
- A dashboard/KPI mock communicates a false or internally inconsistent story.

See [references/anti-patterns.md](references/anti-patterns.md) and [references/semantic-consistency.md](references/semantic-consistency.md) for the full kill list and examples.

### 5. Comparative mode (multiple candidates, one slot)

When the user is choosing between assets for a single slot:

1. Verdict each candidate individually first.
2. Drop all `KILL` verdicts from the running.
3. Rank remaining `SHIP` and `FIX` candidates by: semantic truth > layout containment > brand match > focal-point survival > legibility > polish.
4. Recommend one. Name the file path, the slot, and one-sentence placement reasoning.
5. If every candidate is `KILL` or `FIX`, recommend regeneration with a brief brief.

### 6. Output format

Return a structured response:

```markdown
## Verdicts
- <filename> — VERDICT — one-sentence reason

## Defects caught
- Concrete visual/layout/semantic defects. Be specific: "CTA copy extends past the green rounded rectangle", "chart line slopes slightly upward while label says CPL trending down".

## Anti-patterns flagged
- Optional CSS/HTML/format gotchas.

## Recommendation
- Which file to use or what to fix/regenerate.

## Deploy notes
- Concrete file paths, target dimensions, format conversions, and any CSS/HTML lines that should change. Do not deploy unless asked.
```

Keep it tight. No filler.

## Failure modes

- **Vision tool unavailable / errors out** — Use direct rendered-image inspection plus metadata. Mark the verdict `BEST-EFFORT` only if no visual inspection is possible. If rendered-image inspection is possible, give a normal verdict.
- **Vision model misses obvious defects** — Trust the human-visible image, not the vision model. Call out that the vision pass missed the issue.
- **No brand context provided** — Proceed; note "no brand check performed." Do not downgrade semantic/layout defects just because brand context is missing.
- **Asset is a wordmark/logo** — Skip hallucination scan for stylized typography (intentional design ≠ gibberish), but still check legibility, format, layout containment, semantic consistency, and brand-palette match.
