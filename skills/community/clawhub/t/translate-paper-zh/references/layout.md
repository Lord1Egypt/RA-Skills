# Layout and fidelity procedures

## Source-led composition (preferred)

Use the actual conference/journal class when available and permitted. Keep a clean copy of source and assets; translate only a working copy. Preserve equation environments, labels, references, numeric values, tables and citation keys byte-for-byte where feasible. Translate macro arguments that contain prose (section titles, captions, table cells, algorithm comments, footnotes and appendix headings). Inspect custom macros that hide content. A successful compiler run does not mean all included files were translated.

Use XeLaTeX or LuaLaTeX plus an available CJK package/font. Inspect the actual TeX installation first; binaries may exist without formats, package databases or CJK packages. Resolve dependencies from official distribution sources under the task's allowed permissions. Match CJK package releases to the installed LaTeX kernel: the newest package can require a newer kernel than the available engine. Prefer an official compatible tagged release rather than silently upgrading unrelated tooling. If format/search indexes are missing, use explicit local TEXMF/TEXINPUTS paths and build a task-local format when permitted; check the resulting log and package versions. Do not replace the paper class with an unrelated report template merely to get a build. Use a legible CJK font with confirmed embedding permission, configured consistently for regular/bold text. For Simplified Chinese, select the SC face explicitly: font collections can default to Japanese glyph forms even when Chinese characters render. Check the configured collection face/index and representative glyphs, not only the font-file name. TTC faces can share an internal PostScript name containing “jp” even when the selected index and cmap are SC; do not infer the wrong face from that name alone. Avoid font paths or TeX package names that were never checked locally.

Check class-specific running-header height constraints for taller CJK glyphs; adjust the measured header space without changing the paper’s overall hierarchy. Some conference classes emit a whole PDF warning page when layout checks fail: inspect the first page and all generated pages, and fix the triggering configuration instead of delivering or merely hiding the warning. Inspect original hard page breaks after translation and remove only those that now cause artificial blank space, maintaining all content and section boundaries.

Perform a source-versus-translated structure comparison: included files, sections, equations, figure/table/caption counts, bibliography entries, footnotes and appendix boundaries. Review equation/citation compilation warnings. Translate references' surrounding headings and explanatory prose while preserving author names, original publication titles, venue/year/DOI and citation links for traceability. Translate titles too only when desired, keeping the original metadata alongside them.

## Region-led PDF composition

The bundled overlay helper needs PyMuPDF with `Page.insert_htmlbox`, an embeddable local CJK font, immutable inventory and an explicit plan. It redacts only original text, keeping images and graphics. It deliberately rejects target-region overlap with untouched text, duplicated source units, unreadably small type and overflow. It is appropriate for paragraph/title/caption blocks with room for Chinese.

```bash
python "$SKILL_DIR/scripts/overlay_regions.py" source.pdf work/inventory/inventory.json \
  work/translation.json work/chinese.pdf --font /verified/local/CJK-font.otf
```

Each region lists `page`, `bbox`, `source_ids`, `target`, optional `font_size` (default 9.5pt) and `line_height` (default 1.2). Coordinates are PDF points in the original page space. Its target must contain all corresponding unit translations. Redaction is permanent in the output, so never overwrite the source.

Inline mathematics can share a block with prose. The helper cannot protect its semantics: translate the paragraph while faithfully reproducing each variable and relation, or use source-led re-typesetting. Do not run a whole-page mask or obscure equations/lines to cover prose. If the helper refuses an overlap, inspect and replan; do not remove its checks or shrink text below the readability floor to force a result. Keep source columns and prevent captions from drifting to another figure.

## Figures and tables

Prefer original editable/vector assets. Inventory title, axis names, legend terms, panel labels, in-plot prose, annotations, notes and captions. Text extraction will miss glyph outlines and embedded rasters. Use exact figure data/source when redrawing; do not estimate points from an image or regenerate charts with an image model. For PDF diagram/plot text replacement, preserve nontext paths and crop bounds, then verify ticks and data marks before/after.

For raster-only labels, choose a precise document/image editing method allowed by the environment or recreate the labels around untouched data regions. Do not invent new experimental data. If a label cannot be edited reliably, document the limitation rather than silently leaving it English. Complete translation requires checking such labels visually even if the automated English report is empty.

## Font size and safe optimization

Full CJK font collections may add tens of megabytes. Premature external font subsetting can break CID/glyph mappings even when a PDF builds. Prefer `scripts/optimize_pdf_fonts.py` after composition; it uses PyMuPDF’s FontTools fallback, checks exact extracted text and per-page rendered pixels before/after, and writes only a smaller equivalent PDF. The default MuPDF subsetter can fail on some CFF collections; do not treat an optimization command’s successful exit as proof of correct glyphs. Re-run final audit with the optimized output checksum.

## Fidelity review checklist

Compare at least these against the source on every relevant page:
- Negation, quantifiers, statistical claims, confidence/uncertainty, and the direction of comparisons
- Loss symbols, gradients, update steps, subscripts/superscripts and equation numbering
- Values, percentages, signs, decimal places, sample sizes, units and table row/column alignment
- Figure-panel order, axis scales, tick labels, colors, legend mapping and caption cross-references
- Citation identity and numbering; definition at first use; consistent terminology thereafter
- Footnote markers, appendix content and all table/figure notes

Keep translator additions visibly separate and minimal. Label the work an unofficial Chinese translation unless officially authorized; retain source authorship and license attribution.
