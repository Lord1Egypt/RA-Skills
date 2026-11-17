---
name: translate-paper-zh
license: MIT-0
metadata:
  author: vittta
  version: "0.1.0"
description: Translate an entire academic paper into a searchable Chinese PDF while preserving its scholarly layout, equations, figures, tables, citations, footnotes and appendices. Use for full-paper Chinese translation, two-column PDF translation, or a Chinese edition closely matching the original paper; not for a summary alone.
---

# Translate an academic paper into Chinese

Produce a faithful, complete translation with verifiable coverage. Prefer the original paper's two-column class and visual hierarchy. Never call an abstract, selected sections, text-only extraction, or a figure-label-incomplete version a full translation.

## Establish source and scope

1. Read the current PDF/document and file-delivery skills applicable in the environment.
2. Identify the authoritative title, authors, version/date, page count, DOI/URL, license and permission basis. Prefer a user-provided PDF or a source whose license allows the requested transformation. Do not assume that free access implies permission. If full translation is not permitted, seek a user-provided authorized copy or deliver a permitted alternative; preserve useful work without claiming completion.
3. Keep the immutable source, SHA-256, retrieval/provenance notes and license evidence. When using separately obtained TeX, compare its text, sections, figures, tables and appendix to the requested PDF; resolve version differences before building.
4. Infer Simplified Chinese unless the user requests otherwise. Translate all prose, captions, table headers, diagram/axis/legend labels, footnotes, acknowledgements, ethics/limitations sections and appendices. Preserve mathematical meaning, numbers, units, citations and author identities. Keep standard bibliographic metadata and identifiers where translation would harm traceability, recording exceptions.

## Runtime

The bundled helpers need Python 3.10+ and the dependencies in `requirements.txt`. Use an existing compatible runtime, or create a task-local virtual environment and install with `python -m pip install -r "$SKILL_DIR/requirements.txt"`. Commands below assume `python` resolves to that runtime. Composition also needs an embeddable Simplified Chinese font; the TeX route needs an appropriate Unicode-capable TeX toolchain. The helpers do not call a translation API.

## Inventory before translation

Set `SKILL_DIR` to this skill's resolved directory and use a task-local working directory for artifacts. Run:

```bash
python "$SKILL_DIR/scripts/paper_inventory.py" source.pdf work/inventory \
  --source-url 'AUTHORITATIVE_URL' --rights-basis 'VERIFIED_LICENSE_OR_AUTHORIZATION'
```

Inspect every rendered source page. Extracted blocks are candidates, not guaranteed reading order or complete content: two columns can merge, math can split, and raster/vector labels may be absent. Use OCR only where needed, then compare to the page. Add otherwise invisible labels as `visual_units` in the plan and complete `source_reviews` honestly. Never mark these complete solely because an extractor ran.

Use [the manifest reference](references/manifest.md) for fields, coverage records and audit commands. Keep the original inventory immutable; reconcile IDs and checksum deliberately if repairing an extraction. Maintain a shared terminology table with first-use English expansions for important technical terms. Preserve hedging, limitations and distinctions such as training/test-time adaptation, online versus standard variants, loss functions and update rules.

## Translate and compose

Choose the least destructive approach in [layout and fidelity](references/layout.md):

- Prefer licensed original TeX/LaTeX source and its actual paper class. Translate content in place; build with an embedded Chinese font and a Unicode-capable engine. Keep two columns, hierarchy, floats, table values, equation environments and citation structure. Permit additional pages if Chinese expansion requires them; preserve source-to-output mappings.
- If source is unavailable, use explicit PDF text regions or reconstruct the paper layout. The optional `overlay_regions.py` replaces planned text units and preserves vector/image artwork, but does not translate, discover labels, protect mathematical meaning automatically, or edit raster labels. Use it only for suitable regions. For mixed prose/math, dense tables or crowded charts, prefer re-typesetting the affected component and compare against the source.
- Do not force the original page count by shrinking text below readable size, deleting details or covering art. Do not summarize to fit. Reflow or expand the page count while retaining the paper style.

Translate in section-sized chunks, giving workers the source pages/text, glossary, equations context and precise coverage. Keep a model-authored translation path; do not make completion depend on an unverified external translation API. Never transmit private manuscripts to a third-party service without appropriate authorization. Review each chunk against the source before marking `fidelity_checked`.

Preserve figures as vectors where possible. Translate labels, legends and panel annotations as well as captions; keep every tick value, color mapping, point, line and panel. Retain full tables and footnotes. Do not treat original English within a figure as translated because its caption is Chinese.

## Gate delivery

If embedded CJK fonts make the PDF unnecessarily large, optionally run `optimize_pdf_fonts.py input.pdf optimized.pdf` before final review. It uses a font-subsetting fallback and saves only when every page’s extracted text and rendered pixels remain identical. Keep the original if it rejects the optimization.

1. Populate every source unit and visual unit with its translation or narrowly justified retained identity/math/reference data. Map it to output pages. Do not omit bibliography pages or appendices.
2. Run `audit_translation.py` to render every output page, extract searchable Chinese, check font embedding, check coverage, detect remaining English and create review templates. Audit failure is expected before manual review.
3. Open and inspect every rendered page at readable scale, comparing with the source. Check clipping, overlaps, missing glyphs, two-column flow, tiny text, image quality, figure labels, equations, data, citations, page breaks and footnotes. Fix issues, rebuild, then inspect changed pages again. Bind recorded reviews to current output and render checksums.
4. Review every remaining-English item. Allow only explicit, page-scoped identifiers, names, math or bibliographic terms with a reason; never blanket-allow all words to get a green result. English embedded in images requires visual checking independently.
5. Re-run the audit. Deliver as complete only if all gates pass and the semantic/visual reviews were genuinely performed. A passing script is evidence of recorded checks, not an independent linguistic guarantee.
6. Deliver the final PDF as a native attachment, with title/version, attribution and a brief statement of scope. Keep manifests and intermediate files unless asked for them. If blocked or partial, identify the exact missing content and avoid “全文/完整版/全部完成.” Verify the recipient can open the delivered file.
