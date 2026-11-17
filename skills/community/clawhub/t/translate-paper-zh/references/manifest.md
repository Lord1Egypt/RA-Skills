# Coverage and review manifest

Dependencies: Python 3 and PyMuPDF (`fitz`). The scripts use no network and no external translation API. Use environment-provided packages, or install from an approved official package registry when allowed. Source/output text extraction and font checks are mechanical aids; linguistic and visual inspection remain mandatory.

## Files

`paper_inventory.py` writes immutable `inventory.json`, source page PNGs, and an initial `translation.json`. Re-running it will not overwrite an existing translation plan. Do not rebuild the inventory with changed options without reconciling its checksum and unit IDs.

`inventory.json` records source checksum/provenance, page geometry, image/drawing counts, OCR warnings and text blocks with exact spans/coordinates. IDs are page/block identifiers. They represent extracted content, not automatically reconstructed paragraph order.

`translation.json` uses:
- `schema: 1`, `source_sha256`, `inventory_sha256`
- `rights`: `verified`, `basis`, `evidence` (source license URL, attribution, or specific authorization evidence; do not invent permission)
- `units`: exactly one entry per inventory ID
- `visual_units`: additional content invisible to text extraction, such as outlined/raster figure labels
- `source_reviews`: one per original page, proving visual inventory/OCR checks
- `regions`: optional explicit layout plans for the overlay helper
- `allowed_english`: exact words/phrases scoped to an output page with a legitimate reason
- `output_sha256`, `page_reviews`: filled only for the built and inspected output

## Text units

Each plan unit has `id`, `status` (`pending`, `translated`, `retained`), `kind`, `target`, `output_pages`, `fidelity_checked` and `reason`. Use positive integer output page numbers. For translated prose, `target` is the full Chinese text; the audit requires it in the searchable output after Unicode/whitespace normalization. If extraction order splits a paragraph around a formula or page break, split that unit into smaller traceable pieces in a deliberately revised inventory, or correct the output text layer; do not claim a match without checking it.

For retained content, the audit permits only `math`, `identifier`, `citation`, `reference`, `author` or `number` with a reason, and checks that source text survives. Do not relabel prose as a reference. Bibliographic identity retention does not permit retaining ordinary body prose, captions, footnotes or appendix paragraphs. Use translated prose plus the unchanged original identity within it when a block mixes those categories.

The audit compares numeric-token multiplicities in each translated unit. If they differ, inspect `numeric_candidates.json`, fix unintended changes, or set that unit’s `numeric_review` to the specific justified formatting/numbering change (for example, an ordinal translated into Chinese). Never excuse a changed experimental value.

`fidelity_checked: true` attests that a reviewer actually compared meaning, math, numeric values and citations. An automatic word-count comparison cannot set it.

## Visual units and source reviews

A visual unit has `id`, `page`, `bbox`, `source_text`, `target`, `kind`, `status`, `output_pages`, `fidelity_checked` and `reason`. It supplements the text inventory; never use it to hide missing text units. Translated visual labels must also be searchable. If translation is baked into a raster, add a correctly aligned accessible/searchable text layer as part of composition.

Each `source_reviews` entry includes `source_page`, `visual_inventory_checked`, `ocr_checked` and `visual_unit_ids`. Review every source page, including references and appendices; list exactly its extra visual units. A visually inspected page may legitimately have no such units. Sparse-text pages need explicit OCR review even when legitimately mostly plots.

## Output audit

```bash
python "$SKILL_DIR/scripts/audit_translation.py" work/inventory/inventory.json \
  work/translation.json work/chinese.pdf work/qa
```

The first run normally exits 1. It writes:
- `audit.json`: source-unit coverage, font embedding information, issues and warnings
- `numeric_candidates.json`: per-unit numeric discrepancies requiring explicit review
- `remaining_english.json`: page-scoped Latin-word candidates; inspect them, since acronyms and names may be legitimate
- `page-NNN.png`: every output page rendered at the selected DPI (default 144)
- `qa-template.json`: current output checksum and per-page render hashes with all review flags false

Open all page PNGs before copying/setting review fields. In `page_reviews`, set a reviewer identifier, `passed`, `no_clipping`, `no_overlap`, `legible`, `figures_complete`, `math_data_citations_checked` and notes based on genuine inspection. Copy the current output hash. Do not automatically convert all template false values to true. Every rebuild invalidates output-bound review; re-render and inspect affected pages, validating the rest are unchanged.

For `allowed_english`, add `{ "page": 3, "text": "ResNet CIFAR", "reason": "Exact model and dataset identifiers" }` only after review. The scanner reports Latin words of four or more characters, so acronyms, one-letter symbols and rasterized English still need visual inspection. Explicitly justified retained units supply their original terms to the same page-scoped allowlist.

The audit also rejects normalizable CJK compatibility ideographs in output text (for example U+F967 instead of standard 不), because normalized coverage comparison can hide broken ordinary exact-text search. Repair the affected font’s ToUnicode mapping or use a correct embedding workflow; do not alter glyph artwork. Verify unchanged rendered pixels, semantically identical Unicode text and exact searches for the repaired characters, then re-run the audit. Never apply broad Unicode normalization to mathematical content or arbitrary CMap source codes.

If extractable replacement/null glyphs remain from an unchanged source formula, first try to repair the text layer. Only after inspecting the exact rendered glyphs may a `glyph_exceptions` entry retain them: specify `page`, `character`, exact `count`, `visual_checked: true` and a narrow `reason`. Do not allow missing Chinese glyphs or blanket exceptions.

Exit 0 means mechanical gates and current recorded reviews pass. It does not verify the truth of a reviewer flag or detect every bad translation. Never use a green report as a substitute for inspecting all content. Check the final native attachment after upload as well as the local PDF.
