# Figure translation contract

Before the first raster edit, inspect the real accepted pair
`examples/heatmap_english_original.png` and
`examples/heatmap_image2_zh_accepted.png`, plus its audit record in
`examples/heatmap_image2_acceptance.json`. It demonstrates complete in-image
replacement, unchanged data values, and an unclipped color bar. This is an
acceptance pattern, not a paper-specific runtime test.

## Inventory before editing

For every figure and subfigure, record all visible text: panel letters, title, axes, tick categories, legend entries, color-bar labels, conditions, group names, callouts, node labels, arrows, process steps, footnotes, and significance notes. Create an English-to-Chinese label map and verify terminology against the paper ledger.

## Preferred reconstruction order

1. Recreate plots from supplied source data or vector objects when available.
2. Edit vector PDF/SVG objects when text remains selectable.
3. For every raster-only figure with semantic English, use the built-in Image 2 edit mode on the original complete figure crop. Supply an exact label map and invariants for data values, marks, colors, scales, geometry, panel boundaries, and aspect ratio. Forbid added translation panels, captions, cropping, invented content, and data redrawing. Inspect the result visually and retry until every semantic English label is replaced in-image.
4. Deterministic masking, an OCR overlay, or a manually redrawn substitute may be used only as a diagnostic aid; it never satisfies the required Image2 raster deliverable.

Never redraw data points, bars, error bars, distributions, brain maps, microscopy content, or other evidentiary marks from visual estimation. If a safe translation cannot be produced, flag the figure as blocked rather than shipping an untranslated figure.

The delivered figure itself must contain no untranslated semantic English. A Chinese caption, legend/key, or annotation panel added below the original does not satisfy this contract. Cover and replace the original English title, axes, tick categories, legend entries, callouts, node labels, process steps, and annotations at their original visual locations while preserving the underlying evidence.

## Non-negotiable acceptance test

Extract each translated image after DOCX assembly and inspect the pixels, not only the document text. Mark every inventoried label as `replaced`, `preserved mathematical/identifier`, or `blocked`. If any ordinary English semantic label remains visible, reject the image and rebuild it. Never ship a figure whose only Chinese content is outside the original plot/image bounds.

For Image 2 edits, compare the generated image side by side with the original before inserting it. Confirm every data value and evidentiary mark remains unchanged. A successful edit must show Chinese at the original label positions and no English duplicate elsewhere. Save the accepted generated image into the task workspace and embed that exact file; do not substitute an earlier deterministic mock-up.

## Typography and layout

- Use a readable Chinese sans-serif font and keep panel letters and mathematical notation intact.
- Match original hierarchy, alignment, color coding, line weight, and relative spacing.
- Expand label boxes or wrap Chinese text when necessary; do not shrink text below readable size.
- Keep units, variable names, statistical symbols, gene/protein names, and standard abbreviations exact.
- Translate categorical tick labels and legend entries; numeric ticks usually remain unchanged.

## Verification

Compare the translated figure with the original side by side. Check every label in the inventory. Confirm unchanged panel count, plot geometry, scales, colors, legend-to-mark mapping, sample sizes, error bars, significance marks, and notes. Render the figure at final DOCX size and inspect legibility.

