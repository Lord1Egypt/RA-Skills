---
name: tablescribe
display_name: TableScribe 表格智取
display_name_en: TableScribe — Table Extraction & Verification
description: >-
  给需要把截图、扫描件、纸质表格照片变成数据的人：视觉读语义、OCR 读坐标、程序化校验做裁判三路互证，产出 Excel／CSV／JSON 与校验报告。
description_en: >-
  For anyone who must turn screenshots, scans, PDF captures, and phone photos of paper tables into usable data. A vision model reads semantics, OCR supplies coordinates, and programmatic cross-checks arbitrate, producing Excel, CSV, or JSON with a verification report.
version: 1.0.0
category: data-analysis
sub_categories:
  - key: pro-data
    name: 数据处理
tags: [表格识别, OCR 校验, 数据还原, Excel 导出, 合并单元格]
tags_en: [table extraction, OCR verification, data reconstruction, Excel export, merged cells]
icon: 📋
platforms: [WorkBuddy, QClaw, ima, Claude Code, Codex]
trigger_keywords: [表格转 Excel, 图片表格识别, 扫描件表格, 截图转表格, 合并单元格还原, 勾选列识别, 多页续表, 行列合计对不上, 数字串位, OCR 复核]
author: DeepCraft Studio
license: Commercial
pay_skill: true
price_cny: "2.99"
---

# TableScribe — Table Extraction & Verification

Turn screenshots, scans, PDF captures, and phone photos of paper tables into structured Excel, CSV, or JSON, with merged cells, checkbox columns, continued pages, and shifted digits handled by three-way cross-verification and a report you can audit.

## What This Is

- **The problem.** Generic optical character recognition (OCR) reads a page of text; it does not understand a table. Merged cell spans, checkbox column ownership, and the row and column address of every number are exactly where it fails, and one wrong cell invalidates the whole sheet.
- **What you get.** A main table, a column dictionary, a verification report, and a reconstruction note, delivered as `.xlsx`, `.csv`, or `.json`.
- **How it differs from asking a general model.** Asked to transcribe a table, a general model invents numbers and rows, and it invents them fluently. This skill never lets it transcribe freely: it answers structured questions only, and OCR coordinates plus arithmetic decide what is true.
- **Three channels in parallel.** The vision model supplies semantics (headers, column ownership, merge spans, units), OCR supplies coordinates (text-box positions, checkbox glyphs), and programmatic checks arbitrate (row and column totals, page continuity, magnitude and format).
- **The acceptance test.** Not "the model says it read it correctly", but "the cross-checks close and every value traces back to a text box in the source image".

## When to Use It

- "I have screenshots of a system export and need a workbook I can filter and pivot."
- "The scan runs to two pages, page two repeats the header, and rows at the seam went missing."
- "Merged cells break the columns the moment OCR dumps the page."
- "It is a phone photo of a paper form with glare and a slight tilt, and the numbers do not line up."
- "The table has checkbox columns, and I need to know which boxes each row ticks."
- "The totals are off by a little, and I need to know which row and which cell."
- "I have a batch of same-layout sheets to convert, and I need an auditable record of what changed."

## When NOT to Use

- Handwriting, heavy perspective distortion, or stamp occlusion: route to manual entry.
- Columns whose meaning needs business judgment: this skill reconstructs and verifies only.
- Scans below 800px or text under 12px: rescan first.
- Editing source values or imputing missing cells: mark gaps, never fabricate.

## Quick Reference

| Situation | Use |
|---|---|
| Poor image quality, preprocessing | `references/extraction-playbook.md` |
| Merged cells, multi-row headers | `references/cell-reconstruction.md` |
| Verify the extraction | `references/verification-rules.md` + `scripts/verify_table.py` |
| Truncation, column drift, garbled text | `references/failure-modes.md` |

## Inputs and Outputs

Inputs:

| Field | Required | Notes |
|---|---|---|
| Image files | Yes | PNG, JPEG, WebP, or TIFF, or a scanned PDF rendered page by page. Long edge ideally >= 1500 px, one page per image |
| Table type | No | Value table, checkbox table, or mixed; inferred from headers and data shape when omitted |
| Target column model | No | Supply an existing name and unit list to skip header semantics |
| Check rules | No | Which columns carry totals, which row is the total row, tolerance, key column |
| Export format | No | `xlsx` (default), `csv`, `json`, or several |
| Output language | No | Whether to add a header lookup table; the default reproduces the source verbatim, untranslated |

Outputs:

| Artifact | Form | Contents |
|---|---|---|
| Main table | `.xlsx`, `.csv`, `.json` | One record per row; merged cells flattened with a source-row marker |
| Column dictionary | Sheet or `.json` | Name, unit, type, confidence, inferred flag |
| Verification report | Sheet or `.json` | Check name, expected value, actual value, difference, verdict |
| Reconstruction note | Sheet or `.md` | Doubts, skipped items, inferred names, imbalances present in the source table |

## Workflow

### 1. Preprocess and partition

- **Do.** Read pixel size and glyph height to judge readability. Grayscale, adaptive binarize, denoise, and deskew anything over 1.5 degrees of skew. Upscale 2x with LANCZOS before OCR. Split the page into a header band, a data region, and a tail region (total row, notes, stamp). Slice the data region into strips of at most 15 rows or 300 px, with one overlapping row between strips as a stitching anchor.
- **Pass when.** The sum of strip rows minus overlapping rows equals the row-anchor count; stitching rows are identical in both strips; at least two horizontal rules are found in the header band.
- **If it fails.** No header band: classify the page first (value table, checkbox table, plain text, receipt) and decide whether to infer columns from data shape. Output truncated: shorten the strips, never lower the resolution. Lines still not level after deskew: report perspective distortion and fall back to a manual-entry recommendation.
- **Hard rule.** A thumbnail contact sheet (many images shrunk into one) may be used only to classify page types, never to read values. A region known to contain values must be read from the single original image, upscaled at least 1.8x and split top and bottom when long.

### 2. Detect headers and column anchors

- **Do.** Crop and upscale the header band and ask the vision model only for the full column names left to right, their units, and whether the header is multi-level. Keep it away from the data region. Collect the x center of each header text box from OCR as the column anchor, then validate against vertical-rule positions. The band between adjacent anchor midpoints is the column band.
- **Pass when.** Bands do not overlap; every header text center sits inside its own band; a multi-level header splits into parent and child levels whose child spans sum to the parent width.
- **If it fails.** Header will not split: build columns from the lowest level and store the parent name in the `group` field. No header at all: infer column types from data shape (digit density, checkbox glyph ratio, text length distribution) and mark the names as inferred in the reconstruction note.

### 3. Segment cells and run OCR

- **Do.** Extract horizontal and vertical rules with morphological opening to recover the grid; for borderless tables fall back to row anchors plus column bands. OCR each cell or row strip, keeping the box, text, and confidence of every text block. Cluster rows by y center with a tolerance of 0.4 row height. Extract numbers with a regular expression instead of casting the whole string: normalize full-width digits, strip thousands separators and currency symbols first.
- **Pass when.** Every row hits at least one anchor (index, name, or unique key); the anchor count matches the partition plan; low-confidence cells enter the review queue and are counted.
- **If it fails.** Grid detection fails (light dashed rules, no borders, broken merges): switch to row-strip segmentation. Anchor missing: mark the row unanchored and keep it out of the main table. No channel can read a cell: leave it empty with a flag; never guess.

### 4. Re-check semantics with the vision model

- **Do.** Never ask for a full transcription. One call per strip, restricted to three structured questions: column ownership (which column this text belongs to), merge span (how many rows and columns this cell covers), and unit consistency (header unit against cell content). Anchor the prompt on column letters (A, B, C) and require JSON only, with cell text copied verbatim and never summarized. Fix the call parameters at temperature 0, thinking disabled, and a generous output ceiling.
- **Pass when.** The returned row count equals the strip anchor count; every returned row maps to an anchor; the finish reason is normal rather than a length cutoff; the JSON parses.
- **If it fails.** Truncated output: split further and lower rows per call. More rows than anchors: treat as invented rows, drop the unanchored ones, and record the count. Semantics disagree with coordinates: coordinates win; vision only informs column ownership.

### 5. Handle values, checkboxes, and merged cells

- **Do.** Do not read numeric columns row by row. Instead take the numeric blocks inside that column band, sort them by ascending y, and align the resulting ordered series with row positions, because within a column natural order is row order. For checkbox columns, assign each mark by the x center of its box and the distance between mark y and row y, and distinguish three states: marked, blank, and undetected. Merge cells according to the span matrix: text columns may fill down or across but must record the source row and span; numeric columns never fill automatically.
- **Pass when.** The rebuilt series length equals the data row count, with any difference explained by blank rows or non-numeric notes; the marked, blank, and undetected counts sum to the row count; every merged region has a span and a fill policy on record.
- **If it fails.** Series length mismatch: first check whether the band swallowed digits from a neighbouring column by printing every text box in that band with its coordinates. Zero marks in a whole column: never conclude "nothing is ticked"; verify the band and confirm key rows against the image. Span uncertain: keep the cell blank with a flag.

### 6. Cross-check totals and page continuity

- **Do.** Run three families of checks. Arithmetic: row totals, column totals, and grand totals against their parts, with a tolerance of half the smallest currency unit or 1e-6. Continuity: repeated headers and footers across continued pages, key-sequence gaps and duplicates, rows repeated at the seam. Shape: decimal-place consistency, minus signs and parenthesized negatives, unit consistency, and magnitude jumps above ten times between neighbours. Resolve differences back to a specific cell with "total minus everything else".
- **Pass when.** Every check closes; an item that does not close carries an explanation (the source table is itself unbalanced, tax basis differs, rounding) recorded in the reconstruction note; every check reports expected, actual, and difference.
- **If it fails.** Difference cannot be located: return to that cell's pixels and re-read at high magnification. Still unbalanced: mark as open for human review and never edit a value to force a balance. Rows lost at a seam: re-stitch using the overlapping rows.

### 7. Export Excel with a fixed format

- **Do.** Export four sheets: main table, column dictionary, verification report, reconstruction note. Store numbers as real numbers with a number format rather than text. Freeze the header, bold it, size columns to content, and compute each row height from its longest cell instead of a fixed height, which silently clips long text. Set the font explicitly instead of inheriting the theme default. Use ISO dates. Keep empty cells empty: no zero and no placeholder. Flatten merged cells into repeated values plus a source-row marker so filtering and pivoting work. Write through a temporary file and replace only after a read-back check.
- **Pass when.** Reading the file back gives the same row count, column count, and totals as the report; every font name is the explicit value; there are no formula errors; all four sheets exist; each row height fits its longest cell.
- **If it fails.** Target file locked: save under a new name and keep the temporary file. Read-back mismatch: stop delivery and print the difference list. Numbers read back as text: reset the cell type and number format, then read back again.

### 8. Run the human review pass

- **Do.** Before delivery, walk the review queue in risk order: total rows and grand total cells, checkbox columns, merged regions, page seams, units and dimensions, key gaps, unanchored rows, the difference between blank and zero, and imbalances already present in the source. For each item give page, row, column, a crop suggestion, two candidate values, and a recommendation.
- **Pass when.** Every queued item has a verdict (confirmed, corrected, accepted as in the source); accepted items carry a reason in the reconstruction note; the delivery summary states the check pass rate and the number of open items.
- **If it fails.** More than a fifth of the item count is in doubt: judge the batch unreadable, ask for a re-shoot or manual entry, and list exactly what failed the threshold.

## Output Format

```
1) Table: CSV (UTF-8) or Markdown, header row first, empty cells stay empty (never 0)
2) Verification report: dimensions, row/column totals delta, anomaly list
3) Confidence: high / medium / low, with low-confidence cells listed
```

## Quality Gates

- [ ] **Row conservation.** Main-table rows equal the anchor count; for multi-page input they equal the sum of page rows with seam duplicates removed and recorded.
- [ ] **Column conservation.** Column count equals the column model; no empty column name and no all-empty column; inferred names are flagged.
- [ ] **Arithmetic closure.** Every declared total closes within tolerance, and every check carries expected, actual, and difference.
- [ ] **Value traceability.** Every value points back to an OCR text box or a vision answer at a fixed location; the count of untraceable values is zero.
- [ ] **Checkbox tri-state.** Each checkbox column reports marked, blank, and undetected counts that sum to the row count.
- [ ] **Merge record.** Every merged region records span, fill policy, and source row; numeric columns are never auto-filled.
- [ ] **No invented rows.** Every row has an anchor; unanchored rows are zero or are all listed and excluded from the main table.
- [ ] **Read-back verified.** Export passes read-back: explicit fonts, computed row heights, real numbers, all four sheets present.
- [ ] **No silent doubts.** Every failed check appears in the reconstruction note; nothing is dropped silently and no value is edited to force a balance.
- [ ] **No contact-sheet reads.** Every value traces to a magnified crop of a single original image; no thumbnail mosaic participated in reading values.

## Scope and Limits

1. **Structured tables only.** Headerless free text, contract clauses, and pure receipt fields (amounts in words, stamp text) are out of scope.
2. **No handwriting or stamp guarantees.** With handwriting, stamp overlap, or strong perspective distortion the skill degrades to a structural recommendation plus manual entry, and states the reason.
3. **No business judgement.** The skill does not decide what a value "should" be and does not edit numbers to make totals agree; it reconstructs and verifies.
4. **No detached accuracy figures.** Acceptance is the cross-check pass rate and the list of open items, not a self-reported score.
5. **No translation.** Foreign-language tables are reproduced verbatim; header translation is a separate optional lookup.
6. **Refusal below the readability floor.** If the long edge is under 800 px or glyph height under 12 px, the skill refuses and states the re-shoot requirements: square-on, no glare, one page per image, glyph height at least one fortieth of the screen width.

## Common Traps

- **Reading only the bottom header row**: rebuild the header tree first.
- **Thousand separators vs decimal points**: infer the convention from the rest of the column.
- **Treating total rows as data**: flag them out of the detail set.
- **Units only in the caption**: every numeric column must carry its unit field.

## Delivery Example

```text
Input
- 3 phone photos of a paper table: index / name / quantity / unit price / amount, total row at the end
- Export xlsx plus a verification report

Output skeleton
main.xlsx
  sheet1 main       5 columns x N rows (merges flattened, source_row column added)
  sheet2 dictionary index int / name text / quantity num / unit price num / amount num
                    (unit, confidence, inferred flag per column)
  sheet3 report     check / expected / actual / difference / verdict
      row_product   amount = quantity * unit price      diff 0.00   pass
      column_sum    amount column vs printed total      diff 0.00   pass
      sequence      index continuity                    gaps 0      pass
      decimals      unit price keeps two places         mismatches 0 pass
      continuity    seam rows vs anchors                diff 0      pass
  sheet4 note       inferred names 0 / unanchored rows 0 / doubts 2 (both reviewed, crops attached)
main.csv           plain-text copy of the main table
crop/              review crops named page-row-column
```

## Related Skills

- **ChartAtelier (paid)**: chart the cleaned table.
- **PriceLens (paid)**: normalise multi-channel quotes into a table first.

## Reference Files

| File | Purpose |
|---|---|
| references/extraction-playbook.md | Step parameters: preprocessing, slice sizes, OCR and vision call settings, column-model JSON, stitching and de-duplication |
| references/cell-reconstruction.md | Multi-column and merged-cell recovery: band rebuilding, ordered series, span matrix, checkbox tri-state |
| references/verification-rules.md | Cross-check rules: three check families, tolerances, difference localisation, page continuity, report fields |
| references/failure-modes.md | Failure taxonomy and fallbacks across capture, structure, glyph, semantics, and assembly |
| scripts/verify_table.py | Parameterised checks for totals, decimals, magnitude jumps, key continuity (standard library) |
| scripts/merge_continuation.py | Continuation merge: repeated headers, footers, seam duplicates, key gaps (standard library) |
| scripts/build_xlsx.py | Four-sheet export from the column model (requires openpyxl) |

`scripts/verify_table.py` and `scripts/merge_continuation.py` use the Python standard library only. `scripts/build_xlsx.py` requires `openpyxl` (`pip install openpyxl`) and exits with code 3 when it is missing; the two check scripts and the verification flow are unaffected.
