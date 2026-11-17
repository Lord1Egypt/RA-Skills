---
name: vertical-spacing
description: Use when computing or fixing vertical spacing (margins, padding, Auto Layout gap) between text blocks or components against a grid base, accounting for vertical-trim state on any text layers involved. Grouping follows the Gestalt principle of proximity — what is read together sits closer than what is read apart.
triggers:
  use_when:
    - user asks to compute or fix margins/padding/gap
    - user asks for vertical rhythm or spacing between a heading and body text
    - user asks to review or fix Auto Layout spacing on a Figma frame
    - user asks for a spacing/layout framework tied to a grid base (8px, 4px)
  do_not_use_for:
    - line-height / letter-spacing within a single text style (see text-typesetting)
    - column width / measure (see line-length-optimizer)
    - full type scale generation (see type-scale-generator)
metadata:
  author: Monika Zapisek
  project: Design Engineering Playbook
  version: "1.2.0"
  status: accepted
---

# Vertical Spacing

## Purpose

Compute vertical spacing (margin, padding, Auto Layout `gap`) as clean multiples of a grid base, applying the proximity rule (elements that relate should sit closer together than elements that don't), and correcting for vertical-trim state so the *optical* gap matches the *set* gap.

## When To Use

- Reviewing or defining spacing for a card, section, article, or form.
- Fixing an Auto Layout frame in Figma where gap/padding look inconsistent or off-grid.
- Not for spacing within a single line of text (that's `text-typesetting`) or column width (`line-length-optimizer`).

## Inputs

- `grid-base`: default `8px` (or `4px` for denser UI); confirm which the project uses rather than assuming.
- `component-type`: card / page section / article / form.
- `hierarchy-level`: compact / standard / spacious.
- `base-line-height` (`LH`): the resolved `line-height` of the body text in the flow — required for Workflow step 5 (paragraph/list rhythm), since those gaps are defined as a fraction of it, not as fixed pixel values.
- If available: Figma Auto Layout properties (see Figma Node Integration) and the `leadingTrim` state of any text layers inside the frame.

## Outputs

- Spacing values, all multiples of `grid-base` (e.g. 8, 16, 24, 32, 48, 64, 96).
- CSS (flex/grid `gap`, margin) or Tailwind utility classes, matching whichever convention the project already uses.
- A note on any vertical-trim-driven adjustment (see Workflow step 3).
- For paragraph/list flow: `paragraphSpacing`, list-to-paragraph gap, and list-item gap, each shown as both the `LH`-fraction formula and the resulting pixel value (see Workflow step 5).

## Questions

This skill is an audit, not an interview. Work in this order: read what the file or the input already says, report, then ask.

- Ask only when a value can't be read and the answer would change the result. One question at a time.
- Don't ask for anything the request already states or the file shows — say what you took and where it came from.
- If the question can't be answered, state the assumption and carry on. Never stall the report on it.
- Always ask before writing to a file or a Figma node.

Questions this skill may need:

- The grid base (4px or 8px), when the frame's existing values and spacing variables don't show one.

## Workflow

1. **Snap every value to `grid-base`.** Reject or round any spacing value that isn't a clean multiple — flag existing off-grid values found in input CSS rather than silently leaving them.

2. **Apply the proximity rule.** Spacing above a heading (separating it from the previous, unrelated block) should be noticeably larger — roughly 2–3× — than the spacing below it (to the body text it introduces). E.g. `margin-top: 48px` / `margin-bottom: 16px` on a heading, not symmetric values on both sides.

2a. **Grouping check — internal ≤ external.** This is the Gestalt principle of proximity applied to spacing: elements placed close together are read as one group, elements spaced apart as separate ones, and proximity outweighs similarity of colour or shape. The working form of it: the space inside a group is never larger than the space around the group.

   | Pair that is read together | Its gap must be smaller than |
   |---|---|
   | Title and its description | the gap to the next title–description pair, and the container's padding |
   | Label and its field | the gap to the next label–field pair |
   | Field and its helper or error text | the gap between label and field |
   | Items of one list | the gap between the list and the surrounding blocks |
   | Icon and its label | the gap to the next icon–label pair |
   | Heading and the text it introduces | the gap between that heading and the text above it |

   - Walk the frame from the inside out and compare each gap with the one a level up. Flag a pair whose inner gap is larger than the outer one — the grouping reads reversed. Flag equal gaps where two levels should differ — the grouping is ambiguous.
   - Report which elements end up reading as one group at the current values, so the finding is about meaning, not numbers.
   - The sources give the principle, not a ratio. The "2–3×" in step 2 is this skill's working value for headings; don't present it as a published rule.

3. **Vertical-trim correction (critical when text is involved):**
   - If the text layers in this spacing context have vertical-trim **off** (default), the visually perceived gap can be smaller than the set `gap`/`margin` value because the font's built-in leading sits inside the text box. Do not invent a universal pixel correction: the difference depends on the font metrics, line-height, and adjacent glyphs. Either measure the rendered distance or recommend turning vertical-trim on so the spacing value maps to the trimmed text bounds.
   - If vertical-trim is **on**, the set spacing value is the true optical distance from baseline/cap-height to the next element — no compensation needed; this is the state to prefer for new work.
   - Always state which assumption is in effect — don't emit a spacing recommendation without saying whether it assumes trim on or off, since the correct pixel value differs between the two.

4. **Report, don't silently rewrite a stylesheet or Figma frame** unless asked to apply directly.

5. **Paragraph and list rhythm — all derived from `LH` (body text line-height), not fixed pixel guesses:**

   | Relationship | Formula | Example (LH = 24px) |
   |---|---|---|
   | Between paragraphs (`paragraphSpacing`) | `0.50–0.75 × LH` | 12–16px |
   | Between a list block and the surrounding paragraph (before and after) | same as `paragraphSpacing` — treat the whole list as one paragraph-equivalent unit | 12–16px |
   | Between items inside one list (`List_Item_To_Item_Gap`) | `0.25–0.33 × LH` — deliberately tighter than `paragraphSpacing`, so the list reads as one cohesive block (Gestalt proximity) rather than a series of unrelated paragraphs | 6–8px |
   | Bullet/number to item text (horizontal indent) | fixed optical distance, not an `LH` fraction — one `grid-base` step or `1ch` (the width of a "0" in the running font), whichever the project's existing spacing convention prefers | 8px |

   - **Don't apply `paragraphSpacing` and first-line paragraph indent (`1em` text-indent) together** — pick one convention per project. If the input already shows one in use, match it rather than introducing the other.
   - Snap the computed `LH`-fraction results to `grid-base` (step 1) where the two don't conflict; if `grid-base` and the `LH`-fraction range don't intersect cleanly (e.g. `LH = 22px` → 0.5–0.75× = 11–16.5px, and `grid-base = 8` only offers 8 or 16), prefer the value inside the `LH`-fraction range over forcing a grid-base multiple — state which constraint won when they conflict, rather than silently picking one.
   - This step depends on `text-typesetting`'s `line-height` output — if `base-line-height` isn't given, ask for it or compute it via that skill first rather than guessing a round number.

6. **Figma margin-collapse guard (a real Figma-specific gotcha, not a CSS concept):** Figma's `TextNode.paragraphSpacing` only adds space *below* a paragraph, not above the next one — there's no browser-style margin-collapse behavior reconciling two adjacent blocks' spacing. If a heading node (H2, say) directly follows a paragraph node, the paragraph's `paragraphSpacing` alone is usually too small a gap above a heading (it was sized for paragraph-to-paragraph rhythm, not paragraph-to-heading), and the heading will visually "stick" to the text above it.
   - Fix: don't rely on the paragraph's trailing `paragraphSpacing` for this transition. An Auto Layout frame has one `itemSpacing` for all of its children — there is no per-item gap override — so give the heading its own space above it: wrap the heading together with the body it introduces in a nested Auto Layout frame and set the larger gap on the parent, or set `paddingTop` on a frame that wraps the heading. Size that space to:
     ```
     Margin_top_heading = 1.5 × LH_body
     ```
   - This is larger than the standard heading proximity ratio in step 2 specifically to counteract the missing collapse behavior — don't also apply step 2's 2–3× ratio on top of this value; they solve the same problem, use the larger of the two, not both stacked.

## Figma Node Integration

When running with Figma access, work against the selected `FrameNode`:

- **Read:** `layoutMode` (must be `VERTICAL` or `HORIZONTAL` — if `NONE`, this isn't an Auto Layout frame and gap/padding don't apply the same way; report that first), `itemSpacing` (= `gap`), `paddingTop`/`paddingBottom`/`paddingLeft`/`paddingRight`.
- **Also read `leadingTrim`** on any child `TextNode`s — this is the input to Workflow step 3. Don't compute a spacing verdict for a frame containing text without checking it.
- **Paragraph/list frames:** read `TextNode.paragraphSpacing` and `TextNode.paragraphIndent` directly when the node is a body-copy text node with multiple paragraphs — Figma exposes these as native text-node properties, not just Auto Layout `itemSpacing`, so check which one the content actually uses before recommending a fix. For a native list inside one text node, the gap between items is `TextNode.listSpacing` (Workflow step 5, `List_Item_To_Item_Gap`), not `itemSpacing`.
- **Verdict:** if `itemSpacing`/padding aren't multiples of the confirmed `grid-base`, flag each offending value with the nearest clean multiple.
- **Bound values:** if `itemSpacing` or a padding is bound to a variable (`frameNode.boundVariables`), name the variable and the nearest on-grid variable in the report. Don't replace a binding with a raw number.
- **Alert pattern for missing trim:** "Vertical trim is off for text in this frame. The configured `gap: {itemSpacing}px` includes the font's internal leading, so the optical gap may be smaller. I can't derive an exact correction without measuring the rendered font metrics. For a precise {grid-base}px grid, enable Vertical Trim: Cap height or measure the visible distance." — use this concrete alert when trim is off and the frame is otherwise on-grid.
- **Action back to Figma:** set `itemSpacing`/padding, or `paragraphSpacing`/`paragraphIndent`/`listSpacing` for text-node-native rhythm, or `leadingTrim` (`"CAP_HEIGHT"` / `"NONE"`) on child text nodes, only on explicit request — never silently.

## Quality Checklist

- [ ] Every emitted spacing value is a stated multiple of `grid-base`.
- [ ] Grouping check done from the inside out: no inner gap larger than the gap around its group; reversed and ambiguous groupings named.
- [ ] Proximity rule applied asymmetrically around headings (top ≫ bottom), not symmetric padding by default.
- [ ] Vertical-trim state checked for any text-containing frame before giving a final gap value; assumption stated explicitly if unknown.
- [ ] Off-grid values found in existing input are flagged, not silently left or silently "fixed" without saying so.
- [ ] Paragraph/list rhythm values (step 5) shown as both the `LH`-fraction formula and the resulting px — never a bare pixel number with no derivation.
- [ ] List-item gap is visibly tighter than `paragraphSpacing` (0.25–0.33×LH vs. 0.5–0.75×LH) — never emitted equal or reversed.
- [ ] `paragraphSpacing` and first-line indent not both recommended together; matches whichever convention the input already shows.
- [ ] Figma writes (if any) only happen on explicit request.
- [ ] Cross-reference to `text-typesetting` noted when the fix is really "turn on vertical-trim" rather than a spacing-value change.

## References

- Latin, M. (2017). *Better Web Typography for a Better Web*. — mathematical treatment of vertical rhythm and grid-base spacing.
- Butterick, M. *Practical Typography*. — critique of rigid baseline-grid enforcement in favor of flexible, grid-base-multiple padding/gap.
- Harley, A. (2020). *Proximity Principle in Visual Design*. Nielsen Norman Group — items close together are perceived as a group; proximity can overpower similarity of colour or shape; a section's text sits closer to its own heading than the preceding section's text does.
- Romasheva (2023). *The rule of internal and external* — "internal ≤ external" as a special case of the law of proximity. Practitioner source.
- Butterick, M. *Practical Typography*, "Headings" and "Space between paragraphs" — the best way to emphasise a heading is space above and below; paragraph space of 50–100% of the body text size.
- Wertheimer, M. (1923). Gestalt principle of proximity — elements spaced closer together are perceived as grouped/related; the basis for list items sitting tighter than paragraphs.
- Bringhurst, R. (2012). *The Elements of Typographic Style* (4th ed.). Hartley & Marks — paragraph spacing and first-line indent as alternative (not combined) conventions, both derived from line-height rather than arbitrary pixel values.
- Figma Plugin API Docs: `FrameNode.layoutMode`, `FrameNode.itemSpacing`, `FrameNode.paddingTop/Right/Bottom/Left`, `TextNode.leadingTrim`, `TextNode.paragraphSpacing`, `TextNode.paragraphIndent`, `TextNode.listSpacing`.
- Related skills: [`text-typesetting`](../text-typesetting/README.md) (vertical-trim and line-height source of truth), [`line-length-optimizer`](../line-length-optimizer/README.md) (horizontal measure — different axis, same text blocks).
