---
name: review-engineering-docs
description: Review Chinese engineering and construction documents in DOCX, text-based PDF, XLSX, or XLSM format. Use when asked to extract project facts, contacts, schedules, quantities, safety measures, missing items, conflicting values, or review questions from construction plans, technical proposals, tender materials, supplier files, and similar project documents. Produces a local, traceable pre-review report and never invents missing engineering data.
---

# Review Engineering Docs

Pre-review Chinese engineering documents with deterministic local extraction, then use the extracted evidence to prepare a concise human-review checklist.

## Non-Negotiable Rules

- Treat the source files as the only authority for project-specific facts.
- Never fill a missing field with a plausible value, another project's value, or an internet result.
- Label uncertain, unreadable, or conflicting content as `待确认`.
- Do not claim regulatory compliance. A qualified human must review the final engineering deliverable.
- Keep customer files and extracted text local unless the user explicitly requests an upload.
- Preserve the original files. Write all generated artifacts to a separate output directory.

Read [review-rules.md](references/review-rules.md) before interpreting results from safety-critical or contract-facing documents.

## Workflow

### 1. Inventory The Inputs

List each source file and classify it as:

- Native DOCX
- Text-based PDF
- Scanned or image-only PDF
- XLSX/XLSM workbook
- Unsupported legacy or drawing format

The bundled script supports DOCX, text-based PDF, XLSX, and XLSM. Convert legacy `.doc` or `.xls` files first. Run OCR on scanned PDFs before review and state that OCR was used.

### 2. Run Local Extraction

Install dependencies once:

```bash
python -m pip install -r <skill-directory>/scripts/requirements.txt
```

Run one file at a time:

```bash
python <skill-directory>/scripts/review_engineering_doc.py "<input-file>" --output-dir "<output-directory>"
```

Use `--no-excel` when an Excel copy of extracted fields is unnecessary. Use `--skip-extracted-text` when the user only wants structured results and a report.

The script creates:

- `fields.json`: structured facts and automated checks
- `fields.xlsx`: a flat review table, unless disabled
- `review_report.md`: readable facts, extracts, missing items, conflicts, and warnings
- `extracted_text.md`: locally extracted source text, unless disabled

### 3. Verify Evidence

Read `review_report.md` and `fields.json`. For every material claim:

1. Confirm the value appears in the extracted source text.
2. Distinguish a total duration from a stage or discipline duration.
3. Keep names, phone numbers, and roles separate unless the source explicitly links them.
4. Check whether a value came from正文、表格、封面、修订说明, or an OCR result.
5. If two values disagree, show both values and their source context.

Follow the field meanings in [review-schema.md](references/review-schema.md).

### 4. Compare Multiple Files

When reviewing a document set, build a flat conflict table with:

| Field | File A | File B | Result |
|---|---|---|---|
| Project name | Extracted value | Extracted value | Match / conflict / missing |
| Total duration | Extracted value | Extracted value | Match / different scope / conflict |
| Contact and role | Extracted value | Extracted value | Confirmed / ambiguous |
| Main quantities | Extracted value | Extracted value | Match / conflict / not comparable |
| Safety requirement | Present / absent | Present / absent | Review needed |

Do not merge conflicting values automatically.

### 5. Deliver The Pre-Review

Return these sections in this order:

1. `资料清单`
2. `已确认事实`
3. `关键工期与数量`
4. `安全与应急摘录`
5. `冲突与缺项`
6. `需要甲方确认的问题`
7. `人工复核说明`

Keep questions short and actionable. Prefer “请确认项目经理与安全员分别对应哪位联系人” over a long explanation.

## Failure Handling

- If a PDF contains no extractable text, stop and request or run OCR.
- If a file is password-protected or damaged, report the exact file and error.
- If table structure is lost during extraction, cite the raw text and mark the row for manual review.
- If the script does not recognize a domain-specific field, inspect the text manually; do not alter the parser just to force a desired answer.
- If the user requests a complete construction plan, use this skill only for pre-review and source extraction. Drafting and professional approval are separate tasks.

## Bundled Resources

- `scripts/review_engineering_doc.py`: deterministic local parser and report generator
- `scripts/requirements.txt`: Python dependencies
- `references/review-rules.md`: evidence and safety rules
- `references/review-schema.md`: output schema and field interpretation
