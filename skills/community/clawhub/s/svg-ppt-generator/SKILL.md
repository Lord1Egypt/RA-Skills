---
name: ppt-generator
description: SVG-based PPT generator with 9 themes, 8 layouts, 30+ charts, and 600+ icons
---

# PPT Generator Skill

Professional presentation engine. Generates SVG pages and converts them to native editable PPTX via svg_to_pptx.
Includes 8 layout templates covering dark, light, consulting, tech, and more.

## When to Use

- User asks to create a PPT / presentation / slides
- User provides content, outline, or data that needs to become a PPTX
- User mentions "make a PPT", "generate slides", "presentation", etc.

## Interaction Flow (must follow)

After receiving a PPT request, **do not generate immediately**. Guide the user step by step:

### Step 1: Confirm Topic and Duration

> Got it, I'll make this PPT for you.
> Topic: "{extracted from user message}" — correct?
> How long is the presentation? This determines page count:
> - 10 min → 10-12 pages
> - 20 min → 15-18 pages
> - 30 min → 22-25 pages
> - 45 min → 28-35 pages

**Duration is required** — do not skip this. Page count directly depends on it.

If the user already provided a detailed outline, skip topic confirmation but still ask duration.

### Step 2: Pick a Style

> Pick a style (just reply with the number):
>
> 1. **dark_warm** (default) — dark warm tone, AI/tech feel
>
> 2. **consultant** — white + blue, consulting style
>
> 3. **cloud_orange** — deep navy + orange, cloud/tech architecture
>
> 4. **ai_ops** — full dark, ops/DevOps style
>
> 5. **tech_blue** — blue tech, formal business
>
> 6. **smart_red** — red business
>
> 7. **exhibit** — light showcase, data-heavy
>
> 8. **pixel_retro** — pixel retro, creative/fun

### Step 3: Confirm Outline

Propose a structure based on the topic and style:

> Based on your needs, here's a suggested structure ({N} pages):
>
> P1 — Cover: {title}
>
> P2 — Table of Contents
>
> P3 — {Section 1 title}
>
> ...
>
> P{N} — Closing: {key takeaway / CTA}
>
> Want to adjust anything, or shall I start generating?

### Step 4: Generate

Only start after user confirms. Send a status message:

> Starting generation, estimated X minutes.

Then execute the Technical Flow below.

### Step 5: Deliver and Iterate

Send the final PPTX with a brief note:

> PPT is ready, {N} pages total.
> Want changes? Just say:
> - "Update the data on page 3"
> - "Add a page about XX"
> - "Make the colors darker"

---

## Technical Flow (executed in Step 4)

```
Read design_spec.md + reference SVGs → Write SVG files → svg_to_pptx → Deliver
```

### Phase 1: Read Design Spec

Load the target style's design spec and reference templates:

```
ppt-master-assets/templates/layouts/{style}/design_spec.md   ← colors, fonts, layout rules
ppt-master-assets/templates/layouts/{style}/01_cover.svg      ← cover reference
ppt-master-assets/templates/layouts/{style}/02_chapter.svg    ← chapter page reference
ppt-master-assets/templates/layouts/{style}/03_content.svg    ← content page reference
ppt-master-assets/templates/layouts/{style}/04_ending.svg     ← ending page reference
```

### Phase 2: Generate SVG Files

Use the `write` tool to create SVG files page by page in `/tmp/ppt_svgs/{style}/`.

**SVG Rules:**
1. `viewBox` must be `0 0 1280 720` (16:9)
2. Strictly follow design_spec.md for colors, fonts, and layout
3. **Do not use**: foreignObject, clipPath, mask, `<style>`, class
4. File naming: `01_cover.svg`, `02_toc.svg`, `03_chapter1.svg`... in order
5. All text uses `<text>` elements with `font-family`, `font-size`, `fill`
6. Background: full-coverage `<rect>`. Decorations: `<rect>`/`<circle>`/`<line>`/`<path>`
7. Tables: manual `<rect>` + `<text>` layout (no HTML tables)
8. Fill the page — avoid large empty areas
9. Titles should state insights, not category labels

**Suggested order:**
- Cover and ending first (set the tone)
- Chapter dividers next (consistent style)
- Content pages last (data-heavy, one at a time)

### Phase 3: SVG → PPTX Conversion

svg_to_pptx converts SVG elements into **native DrawingML shapes** (not images):
- `<text>` → editable text boxes (double-click to edit)
- `<rect>` → native rectangles (drag, recolor)
- `<circle>` / `<ellipse>` → native circles
- `<line>` / `<path>` → native lines/paths
- Tables (rect + text combos) → editable shape groups

The output PPTX is fully editable in PowerPoint, just like a manually created file.

```python
import sys, os
sys.path.insert(0, os.path.expanduser(
    "~/.openclaw/workspace/skills/ppt-generator/ppt-master-assets/scripts"))
from svg_to_pptx import create_pptx_with_native_svg
from pathlib import Path

svgs = sorted(Path("/tmp/ppt_svgs/{style}").glob("*.svg"))
create_pptx_with_native_svg(svgs, Path("/tmp/output.pptx"),
                            canvas_format="ppt169",
                            use_native_shapes=True,  # required! otherwise SVG is embedded as image
                            verbose=True)
```

### Phase 4: Cross Review (optional, requires user confirmation)

After generating the first draft, ask the user:

> First draft is ready. Want to run a cross-review? Multiple reviewers check in parallel — more thorough but takes a few minutes.

If the user agrees and the agent supports subagents, run a review-fix cycle:

1. **Round 1 (full review)**: Launch 5 reviewer subagents in parallel
   - 🎤 Presentation Coach — narrative arc, flow, pacing
   - 👥 Target Audience — simulated audience reaction, comprehension
   - 🔬 Domain Expert — factual accuracy, technical depth
   - 📋 Content Auditor — structure, typos, data consistency
   - 👁️ Visual Inspector — layout, alignment, readability

2. **Fix**: Aggregate all issues, fix by priority (🔴 before ⚠️)

3. **Round 2 (regression)**: 3 reviewers verify the fixes

4. **Exit criteria**: 🔴=0 and ⚠️≤3, or round≥4 force exit

Skip if user says "no review" or "just a quick draft".

### Phase 5: Deliver

Only send the final version. Do not send intermediate versions unless the user asks.

---

## Style Directory Mapping

| # | Style | Directory | Background |
|---|-------|-----------|------------|
| 1 | Dark Warm | dark_warm | Dark cover + light content |
| 2 | Consultant | consultant | White + blue |
| 3 | Cloud Orange | cloud_orange | Deep navy + orange |
| 4 | AI Ops | ai_ops | Dark |
| 5 | Tech Blue | 科技蓝商务 | Blue |
| 6 | Smart Red | smart_red | Red |
| 7 | Exhibit | exhibit | Light |
| 8 | Pixel Retro | pixel_retro | Dark |

Default recommendation: dark_warm.

### Design Spec Location

Each template in `ppt-master-assets/templates/layouts/{directory}/` contains:
- `design_spec.md` — full design parameters
- `01_cover.svg` — cover template
- `02_chapter.svg` / `02_toc.svg` — chapter/TOC page
- `03_content.svg` — content page
- `04_ending.svg` — ending page

### Reference Documents

Key docs in `ppt-master-assets/references/`:
- `strategist.md` — strategist role
- `executor-consultant-top.md` — top-tier consulting executor
- `shared-standards.md` — SVG technical constraints

---
