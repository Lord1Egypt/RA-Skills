---
name: translate-academic-papers
description: "Translate complete English academic papers into polished Simplified Chinese while preserving structure, evidence, equations, tables, citation numbering, and the English reference list. Use for journal articles, conference papers, preprints, and scholarly PDFs; deliver two verified DOCX files by default: a Chinese full-text edition and a paragraph-aligned English-Chinese bilingual edition. Translate all semantic text inside figures and create WPS-compatible citation-to-reference jumps plus clickable DOI links."
version: 1.1.2
---

# Translate Academic Papers

Produce a faithful full-paper translation. Never silently replace the paper with a summary, reading note, or selective translation.

## Standard invocation (标准调用示例)

This is the canonical instruction a user pastes to start the skill. When an AI receives this instruction together with an English paper, it must begin the complete translation immediately and must not ask non-essential questions in between.

> 调用 translate-academic-papers 完整翻译这篇英文论文。直接开始，中间不要询问；生成“全文中文版”和“逐段中英对照版”两个 DOCX。所有图片必须调用 Image2 重新渲染，将图内英文覆盖为中文；保留公式和英文参考文献，并制作可在 WPS 中使用的引文跳转。

### Mandatory execution (执行要求)

Upon loading this skill and receiving an English paper, the AI must:

1. Read and parse the entire paper directly.
2. Completely translate the body, title, abstract, methods, results, discussion, appendix, and figure captions.
3. Generate two DOCX files: `全文中文版.docx` and `逐段中英对照版.docx`.
4. In the bilingual edition, place each complete Chinese paragraph immediately after its complete English paragraph; never merge multiple English paragraphs into one Chinese paragraph, and never split one English paragraph into unrelated Chinese paragraphs.
5. For every image containing semantic English, call Image 2 to edit the image, using the original as the edit target, overwriting the original English with Chinese at the same locations, and preserving all data, coordinates, scales, colors, shapes, error bars, significance marks, and layout. Do not merely add a translation note below the figure, substitute an untranslated original, or use a standalone legend table or blue annotation box instead of in-figure translation.
6. Keep in-text citation numbers unchanged.
7. Keep the reference list in English; do not translate authors, journal names, paper titles, or DOIs.
8. Build WPS-compatible internal jumps between in-text citations and the reference list using native OOXML `w:hyperlink`, activated with Ctrl+click in WPS; make DOIs clickable links.
9. Preserve formulas, variables, units, statistical symbols, numbers, and data formats.
10. After completion, run checks for content, images, citation jumps, paragraph correspondence, and DOCX rendering.

### Only blocking questions allowed (仅在以下情况才允许询问)

Ask the user only when: the file cannot be read; the file is corrupt or password-protected; key pages are missing; the output directory is not writable; or the current environment has no Image 2 / image-editing capability at all.

### Prohibited behaviors (禁止行为)

- Do not output only a translation plan.
- Do not output only a summary, reading notes, or a partial translation.
- Do not ask about model, terminology, filename, output directory, or image format before starting.
- Do not claim a "missing translation engine" and stop working.
- Do not use figure titles or captions to replace in-figure text translation.
- Do not build the bilingual edition as "all English + all Chinese".
- Do not claim delivery before completing the Image 2 image overlays.

## Default deliverables

Generate two DOCX files unless the user explicitly requests only one:

1. `<Chinese title>_Image2全文中文版.docx`: Chinese body, Image 2-translated figures and tables, original English reference list.
2. `<Chinese title>_Image2逐段中英对照版.docx`: each complete English source paragraph immediately followed by its Chinese translation; preserve the same headings, figures, equations, tables, citations, and reference list.

Use the exact paragraph pairing and styling contract in [references/output-variants.md](references/output-variants.md). Do not interpret “bilingual” as two columns unless the user explicitly requests columns.

## Immediate-start policy

When the user supplies a paper file (or a readable local path/attachment) and asks for translation, start the complete workflow immediately and deliver the two default DOCX files in the same response. Do **not** ask setup, formatting, terminology, output-name, output-folder, figure-style, reference-link, or confirmation questions: this skill already defines their defaults.

Infer the Chinese title from the paper title; use the source file's directory as the output directory unless the user specifies another location. Use the translation standard, terminology ledger, figure workflow, DOCX styling, bilingual layout, citation navigation, and QA rules in this skill without asking the user to select them.

Ask a single concise blocking question only when no paper can be accessed, the supplied file is unreadable/corrupt/password-protected, essential pages are missing, or a requested destination cannot be written. If any non-blocking ambiguity remains, make the best evidence-based choice, record it in the final report, and continue. Never pause merely to preview a plan or obtain permission to begin the translation.

## Executable agent contract

This file is an execution contract, not a request to look for a separate “translation engine.” Any AI that loads this skill must perform the work itself in the current session:

1. Resolve the supplied PDF path or attachment and extract the complete source into stable, paragraph-level records.
2. Translate those records in batches using its own language capability, retaining the records in working memory or a local source-map file. The model itself is the translation engine: never stop, defer, or report “no batch translation executor” merely because no script named `translate.py`, external translation API, or third-party translation plugin is installed. If the source exceeds one response or context window, continue in deterministic source-ID batches and write each completed batch into the same local build state until the complete paper is assembled.
3. Use the available document runtime (`python-docx` or an equivalent Office writer) to assemble both DOCX outputs. If a helper script is missing, write the small local builder needed for this paper; do not return only a plan or a text summary.
4. For every raster figure with semantic English, call the available Image 2/image-edit capability with the original figure as the edit target. If the capability is exposed under a different tool name, use that tool's image-edit mode; do not silently substitute a caption, label table, or unchanged figure. If no image-edit capability exists at all, report that specific hard blocker before delivery rather than claiming success.
5. Run the supplied citation-link and navigation validators, render the DOCX files with the available Office renderer, inspect the rendered pages, and repair failures before delivery.

The AI must not ask the user to choose a translation model, chunk size, filename, output folder, figure method, or validation sequence. These defaults are already fixed above. It must not answer “the skill only provides instructions,” “a batch translation executor is missing,” or “the paper is too long for this turn” after loading this skill. The loaded instructions authorize and require direct execution: maintain resumable local state and continue source-ID batches until both complete DOCX deliverables are written, linked, rendered, and checked.

### Capability fallback order

Use this order without asking the user: (a) bundled PDF/document/image tools; (b) installed local runtimes and libraries; (c) the model's own translation and structured document-generation ability. A missing optional helper is never a blocker. Only an inaccessible source, an unwritable destination, or a genuinely unavailable mandatory Image 2/image-edit capability may block delivery, and the final report must name the exact blocked artifact.

On Windows, absence of `soffice` is not a blocker when Microsoft Word or WPS is installed. Use `scripts/render_docx_windows.ps1`, which tries `Word.Application` first and `KWPS.Application` second, exports the DOCX to PDF, and rasterizes every page with Poppler. Do not incorrectly report that rendering is unavailable merely because a LibreOffice-only helper cannot find `soffice`.

### Resumable Windows pipeline

On Windows, prefer `scripts/run_pipeline.py` to create the page-aware source records, persist translations after every source ID, and assemble both DOCX variants. Run it with the bundled Python runtime. If `C:\at` contains the Argos runtime and English-Chinese model, the script may use that local model only as a deterministic first-pass draft. Machine-first output is never deliverable: the agent must replace or revise every cached Chinese record with its own academically accurate translation and mark it `ai_verified` before final assembly. The cache lives beside the paper in `<pdf-stem>_translation_work/translations.jsonl`, so interruption never requires restarting completed paragraphs.

```powershell
python scripts/run_pipeline.py paper.pdf --output-dir <paper-directory>
```

This default command deliberately writes machine-first files inside the work
directory with `机器初译草稿` in their names. It cannot create deceptively named
final deliverables. After the agent has revised every effective cache row and
marked it `ai_verified`, it may assemble human-verified **staging text** with:

```powershell
python scripts/run_pipeline.py paper.pdf --output-dir <paper-directory> --final --title-zh "<verified Chinese title>"
```

The command deliberately writes `AI校订文本_待Image2与链接` staging names rather than final names. Replace applicable figures through Image 2, then run `make_image2_manifest.py` to create a hash-aligned, deliberately pending audit manifest. Visually inspect every extracted embedded image and change a row to `accepted` only after its label audit passes; the helper never self-certifies Image2 output. Run `link_citations.py` and `validate_navigation.py`, then assign the two final `_Image2...` filenames and run `validate_delivery.py` on both documents, the completed manifest, and `--translation-cache translations.jsonl`. Follow [references/delivery-contract.md](references/delivery-contract.md). A successful draft or text assembly is not a successful skill invocation.

## Load supporting instructions

- Load the available `pdf` skill for extraction, OCR, rendering, or PDF inspection.
- Load the available `documents` skill for DOCX creation and visual verification.
- Read [references/translation-standard.md](references/translation-standard.md) before translating.
- Read [references/figure-translation.md](references/figure-translation.md) before processing figures.
- Inspect the accepted Image2 before/after example referenced there before the first raster edit.
- Read [references/output-variants.md](references/output-variants.md) before building either DOCX.
- Read [references/qa-checklist.md](references/qa-checklist.md) before delivery.
- Read [references/delivery-contract.md](references/delivery-contract.md) before final assembly.

## Quality and efficiency policy

Prioritize a verified, complete translation. Work efficiently using one source parse, one shared source map, stable-ID translation batches, reusable hash-validated caches, one process for both DOCX variants, and targeted retries for failed units. These are efficiency practices, not delivery deadlines.

Never omit content, weaken paragraph alignment, skip figure-interior translation, bypass navigation, or avoid render QA in order to finish sooner. Continue until every hard quality gate passes or a genuine external blocker remains. A long paper, context-window boundary, absent translation script/API, or need for multiple continuation turns is not an external blocker. If an external service stalls, preserve valid work and report the specific blocker rather than shipping a falsely complete file.

## Workflow

### 1. Map the complete source

Determine whether the PDF has a usable text layer. OCR only image-only or damaged pages. Inspect every page and restore natural reading order in multi-column layouts.

Begin this step as soon as the source is available. Do not stop to ask for a title, translation preferences, an output filename, a glossary, image handling instructions, or whether to create both standard deliverables.

Build a page-aware source map before translating. Cover all headings, body paragraphs, figures, captions, tables, equations, footnotes, Methods, limitations, availability statements, declarations, acknowledgements, appendices, supplementary text supplied by the user, and references. Give each substantive paragraph a stable source ID so the bilingual edition can be checked one-to-one.

The source map is paragraph-granular: one extracted source paragraph is one translation unit. Never build the bilingual file by iterating over a loose stream of English text and a separate loose stream of Chinese blocks.

### 2. Lock terminology

Build a terminology ledger for technical concepts, model names, measures, brain regions, species, genes, datasets, abbreviations, and statistical notation. Use one canonical Chinese rendering throughout. At first use, provide the standard Chinese term followed by the established English abbreviation where useful.

### 3. Translate every substantive block

Translate for meaning while preserving claim strength, logical relations, uncertainty, qualifications, evidential scope, paragraph boundaries, and citation placement. Use natural academic Simplified Chinese rather than literal English syntax.

Preserve all numbers, units, sample sizes, confidence intervals, effect sizes, p values, symbols, subscripts, superscripts, equation numbers, identifiers, URLs, and searchable proper names. Do not add explanations, causal claims, examples, or conclusions absent from the source. Mark uncertain extraction instead of guessing.

### 4. Translate figures and tables completely

Follow [references/figure-translation.md](references/figure-translation.md). Translate every semantic English element inside each figure, including figure titles, panel headings, axis titles, tick-category labels, legends, callouts, arrows, node labels, process steps, condition labels, annotations, and explanatory notes. Keep mathematical symbols, variable names, units, gene/protein names, and established abbreviations unchanged unless a standard Chinese presentation is clearer.

Do not deliver an English figure with only a Chinese caption. Rebuild or edit the image itself so a Chinese reader can understand it without reading English labels. Preserve data geometry, colors, panel identity, scales, uncertainty marks, significance marks, and visual relationships exactly. Translate complete captions separately below the translated figure.

**Hard gate for figures:** A figure passes only when the translated PNG/SVG/PDF image itself contains the Chinese replacement at the original label location. A caption, a legend/key below the image, a blue annotation panel, or a bilingual translation table does not count. Before inserting the image into DOCX, extract the final embedded image and visually inspect it. Any residual English title, axis title, categorical tick, legend entry, callout, node label, process step, or annotation is a blocking failure, except mathematical notation, units, identifiers, and explicitly preserved standard abbreviations.

For every raster figure that contains semantic English requiring replacement, **must call Image 2** to edit the supplied figure image. Inspect the original crop, pass that crop as the Image 2 edit target, provide an exact English-to-Chinese label map, and explicitly require preservation of every data value, data mark, color, scale, panel boundary, uncertainty mark, significance mark, geometry, and aspect ratio. Explicitly forbid translation panels, added captions, invented labels, cropping, and data redrawing. View the Image 2 result and accept it only after confirming that the original English labels are removed and Chinese replacements appear at the same locations. If the image fails, revise the Image 2 prompt and regenerate before continuing. Do not substitute a caption, label table, ordinary redraw, OCR overlay, or untranslated original image for this required Image 2 edit.

When updating an already assembled DOCX, use `scripts/replace_docx_media.py` with the exact `word/media/...` member. Write to a new DOCX, then regenerate the Image2 manifest and rerender; never assume that replacing a filesystem image automatically updates the embedded DOCX copy.

Recreate editable tables in Chinese. Preserve equations as editable equations whenever possible.

### 5. Build both document variants

Build the Chinese-only and paragraph-aligned bilingual DOCX files from the same source map and terminology ledger. The two files must contain identical scientific content, figures, tables, equations, citations, and end matter; the bilingual version additionally retains every English paragraph directly before its Chinese partner.

In the bilingual edition, every figure location must contain both versions in this order: the untouched English source figure with its English caption, followed immediately by the Image 2-edited Chinese figure with its Chinese caption. The Chinese figure must cover and replace English semantic labels at their original locations; a caption, key, or translation panel alone is not acceptable. For every applicable raster figure, use the validated Image 2 image-editing workflow; do not replace it with direct deterministic editing.

For the bilingual file, emit each source-map record as one atomic pair: `[source_id, English block]` followed immediately by `[source_id, Chinese block]`. Do not merge adjacent English records, split Chinese records, or use page-level extracted text as a substitute for paragraph records. Captions, notes, Methods paragraphs, and short transitions each require their own pair.

Keep the English reference list in both files. Do not translate bibliographic entries, author names, journal titles, or paper titles in the reference list.

### 6. Add WPS-compatible reference navigation

Use numbered citations exactly as the source does. Do not renumber citations or convert them to author-date style.

After each DOCX is content-complete, run:

```powershell
python scripts/link_citations.py input.docx output.docx
python scripts/validate_navigation.py output.docx
```

The first script creates ASCII bookmark targets and native OOXML `w:hyperlink w:anchor="ref_N"` links, which WPS Writer recognizes as real internal hyperlinks. In WPS, activate them with Ctrl+click unless the user's WPS setting is configured for single-click. A blue underlined field result without a `w:hyperlink` anchor is not sufficient. The script also converts DOI strings to `https://doi.org/...` links. The validator fails on missing anchors or bookmark targets.

Use lawful DOI resolution and full-text routes only. Prefer publisher pages, PubMed Central, Unpaywall, institutional subscriptions, preprint servers, or author manuscripts.

### 7. Verify content, navigation, and rendering

Render both final DOCX files and inspect every page. Verify one-to-one paragraph pairing in the bilingual file, translated figure interiors in both files, references and citations in both files, and WPS-compatible hyperlink field instructions. Fix defects and rerender after any layout-sensitive or OOXML change.

On Windows run the installed Office backend directly:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/render_docx_windows.ps1 -InputDocx final.docx -OutputDir final_render
```

The command must report `status: pass`, identify the Word or WPS backend, and produce one PNG per PDF page. Inspect the complete PNG sequence; successful PDF creation alone is not visual QA.

For long documents, first build contact sheets with `scripts/make_contact_sheet.py` to scan every page for blank pages, overflow, broken figures, clipped tables, and abrupt paragraph loss. Then inspect full-resolution page PNGs around every figure/table and any suspicious contact-sheet page. Contact sheets accelerate inspection but never replace targeted full-resolution checks.

For every figure, extract the image from the final DOCX (`word/media/*`), compare it with the source, and record a label-by-label pass/fail result. Do not infer success from the surrounding caption or from a translation panel outside the plot area. If direct masking and redraw cannot preserve the data marks, stop and report the figure as blocked instead of shipping an English figure.

For the bilingual edition, extract the pair records and require a one-to-one count and adjacency audit before delivery. Any mismatch between English and Chinese block counts is a blocking defect.

## Required final report

Deliver both verified DOCX files. State whether the translation is complete or draft. Report unreadable source passages, uncertain figure reconstruction, omitted supplementary files, or unresolved citations. Do not deliver intermediates unless requested.
