# Product Listing Image Pipeline

Replicate an existing canvas workflow chain for a new product. Applicable to any multi-stage image generation pipeline — not limited to specific module counts or product types.

## When to use

The canvas has a complete image pipeline for one product (from text specs to final composites), and you need to produce the same structure for a different product.

## Core Method: Clone by Reference

The fundamental approach is **"read one, replicate many"** — reverse-engineer one complete reference chain, extract the reusable pattern, then re-execute it with new inputs.

### Phase 1: Reverse-Engineer the Reference

Pick **one complete chain** from the reference product and trace every node from start to finish.

For each node, record:
- **Generation params**: model, aspect_ratio, resolution, prompt structure (via `get_asset_detail(artifact_version_id=...)`)
- **Layout geometry**: position, size, gap to next stage (compute offsets between stages)
- **Edge topology**: which upstream nodes feed into it (methodology? positioning? product photo? prior stage output?)
- **Text style** (for text nodes): fontSize, textAlign, verticalAlign

Key rule: `get_element` truncates text at ~200 chars. Always use `get_asset_detail(asset_id=...)` to read full content.

The goal is to extract a **stage template** — a repeatable recipe for each step in the chain.

### Phase 2: Identify Template vs. Variable

Separate what stays the same from what changes per product:

| Template (reuse as-is) | Variable (adapt per product) |
|------------------------|------------------------------|
| Pipeline stage sequence | Product photo asset_id |
| Generation model & params | Product-specific prompt content |
| Canvas layout offsets & sizing | Headlines, copy, selling points |
| Edge topology pattern | Scene descriptions, feature callouts |
| Typography style rules | Product name, certifications, specs |

### Phase 3: Execute Stage by Stage

Work through the pipeline left-to-right. Each stage depends on the previous stage's output, so they must be sequential. Within a stage, parallel execution across modules is fine (max 3 concurrent).

**After each stage completes:**
1. Verify outputs exist (`get_element` to check asset_id is populated)
2. Create edges to maintain the same topology as reference
3. Collect asset_ids needed for the next stage

---

## Stage Recipes

### Background Generation

- Input: text spec node containing an English prompt
- Action: `generate_image` with prompt extracted from spec
- Key params: match reference (model, aspect_ratio, resolution, size)
- Position: compute from spec position + reference offset
- Edge: spec → background

### Product Swap (Multi-Image Reference)

- Input: background image + product photo
- Action: `generate_image` with `asset_id` as **array** `[background_asset, product_photo_asset]`
- Prompt pattern: "Edit the existing image and replace only the [product type] with the exact [product type] shown in the product reference photo. Preserve the original composition, lighting, and all non-[product] details."
- The model sees both images — no need to describe the product in text
- Auto-edges created from both sources

### Text Overlay Plan

- Input: product positioning + methodology + product photo + swap image
- Action: `create_element` (text node) with layout/copy instructions
- Content derivation:
  - Read the product positioning fully (`get_asset_detail`)
  - Map positioning fields to copy: key message → headline, selling points → feature callouts, usage scenarios → scene labels, demographics → audience tags
  - Adapt layout instructions based on the image composition (which areas have negative space)
- Edges: 1 per upstream source (typically 4: methodology, positioning, product photo, swap image)

### Final Composite

- Input: swap image + overlay plan text
- Action: `generate_image` with swap image as `asset_id`, prompt derived from overlay plan
- Prompt construction: translate the overlay plan's layout instructions + exact copy into a single edit prompt
- Edges: auto-edge from asset_id + manual edge from overlay plan

**Prompt lessons learned:**
- For multi-panel images with bottom text bars: keep instructions simple — "semi-transparent dark bars at the bottom of each panel" works. Over-specifying (opacity %, height %, "flush", "pinned") causes unreliable results.
- For single-image overlays: specify placement zone ("right side", "top left") and list exact text lines.
- Always end with: "English only. No extra text. No logo. No other design changes."

---

## Operational Rules

1. **Read before write** — always read the full reference chain before creating anything
2. **Full text only** — use `get_asset_detail` for text content, never rely on `get_element` truncated text
3. **Consistent model** — use the same model for all modules within a stage
4. **Concurrency cap** — max 3 parallel `generate_image` calls; prefer `virse_call batch` for edge creation
5. **Stage gating** — complete one stage fully before starting the next; collect all asset_ids between stages
6. **Edge completeness** — replicate the exact edge topology from the reference; every output node should have the same number and type of incoming edges

## Common Pitfalls

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Product swap shows wrong/generic product | Only one image passed as asset_id | Use `asset_id` array: `[scene, product_photo]` |
| Text content incomplete or garbled | Read from `get_element` truncated field | Use `get_asset_detail(asset_id=...)` |
| Overlay copy doesn't fit the new product | Copied reference copy without adapting | Read full positioning text; derive copy from its selling points and key message |
| Generated text overlay floats or mispositions | Over-constrained placement in prompt | Simplify — match the sentence structure of a known-good prompt |
| Rate limit / batch failures | Too many parallel calls | Max 3 parallel, or use batch mode |
| Visual style inconsistent across modules | Mixed models between modules | Pick one model per stage, apply to all modules |
