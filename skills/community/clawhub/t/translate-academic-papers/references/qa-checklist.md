# Final QA checklist

## Completeness and pairing

- Compare the source map with both DOCX files and account for every substantive block.
- Confirm that Methods, limitations, availability statements, declarations, acknowledgements, appendices, figures, tables, equations, captions, notes, and references are present when supplied.
- In the bilingual edition, confirm every English source ID has exactly one adjacent Chinese partner and every Chinese partner maps back to one English source block.
- Confirm the bilingual edition has equal English/Chinese source-block counts, with no merged English paragraphs, split Chinese paragraphs, or unmatched short paragraphs/captions/notes.
- In the Chinese edition, search for residual English body paragraphs outside proper names, identifiers, references, and intentionally preserved equations.

## Accuracy

- Spot-check the abstract, every major section, every numerical result paragraph, all captions, and all tables against the source.
- Verify sample sizes, units, signs, decimal places, ranges, confidence intervals, effect sizes, p values, equation symbols, and citation numbers.
- Confirm consistent terminology and matching evidential strength in both versions.

## Figure interiors

- Maintain a label inventory for every figure and mark each item translated or intentionally preserved.
- Reject figures with untranslated semantic English in titles, axes, tick categories, legends, callouts, nodes, or annotations.
- Compare original and translated figures side by side; confirm unchanged data geometry, scales, colors, mappings, panel letters, units, uncertainty marks, and significance marks.
- Inspect every translated figure at its final DOCX display size.
- Extract the embedded image from the final DOCX and inspect the pixels. Reject any figure where Chinese appears only in the caption or in an added panel outside the original image, or where ordinary English semantic labels remain visible.
- In the bilingual edition, verify every figure occurs twice: first the untouched English source image, then the independently embedded Chinese image with labels covered/replaced in-image. Confirm both captions are adjacent to their corresponding image.
- For every Image 2 edit, record the accepted output path and visually compare it with the original. Confirm the DOCX relationship embeds that accepted file rather than an older placeholder or translation-panel image.

## WPS-compatible navigation

- Run `scripts/link_citations.py` separately on both content-complete DOCX files.
- Run `scripts/validate_navigation.py` on both linked files and require a zero exit code.
- Confirm every numbered reference has a unique ASCII `ref_<number>` bookmark.
- Confirm each internal citation is represented by a native `w:hyperlink w:anchor="ref_<number>"` element and a matching bookmark.
- Test representative single, range, and comma-separated citations in WPS Writer from early, middle, and late sections, using Ctrl+click when required by WPS settings.
- Confirm every hyperlink field target exists and each visible DOI opens an `https://doi.org/` target.
- Treat missing targets, duplicate reference numbers, malformed DOI values, or ambiguous citations as blocking defects.

## Visual layout

- Render both latest DOCX files and inspect every page.
- Check title hierarchy, paragraph pairing, page breaks, figure resolution, caption attachment, table wrapping, equation clipping, fonts, and reference indentation.
- Ensure no text, image, table, or equation is clipped, overlapped, missing, or stranded.
- Rerender after every layout-sensitive or OOXML change.

