# Schema Design Guidelines

Apply these rules when designing schemas in VLM mode (Step 3 of `vlm-workflow.md`).

# 1. Schema structure

## 1.1 Choose structure by meaning, not layout
Decide whether a field is a non-array field or an array field based on actual repetition, structural sameness, and semantic independence, not on visual grouping.

- If values are shown together in one box, section, or table-like layout but do not truly repeat as interchangeable records, define them as separate scalar fields.
- If values of the same semantic type array, define them as repeated even if the layout looks visually non-array.

# 2. Key design

## 2.1 Extraction scope
Design keys to capture all major business-relevant document information without omission or invention.

- Extract information that is useful for storage, retrieval, or downstream processing.
- Do not create keys for decorative text, boilerplate, page numbers, incidental notes, or other low-value noise.

## 2.2 Multi-document schema generalization
If more than one document is provided for schema design, create one unified schema that covers all documents in the set.

- Generalize keys and descriptions across documents; do not overfit to values, wording, or layout that appear only in a specific sample.
- Include fields based on stable business meaning shared across the document set, even if some fields are blank or absent in individual documents.
- Do not create document-specific keys unless the information has consistent semantic meaning across the documents.

## 2.3 Field prioritization
Maximize coverage of important information, and place the most important fields first.

- Important information is document-dependent,
such as customer and diagnosis details in insurance documents, transaction tables in financial or trade documents,
and key parties, dates, amounts, statuses, approvals, signatures, consent/check states, and classifications in formal records.
- After the most important fields, include additional relevant information that is useful for storage, retrieval, or downstream processing
- Preserve the original structure of tables and repeated records as much as possible, including the relationships between rows, columns, and associated values.

## 2.4 Cell-level decomposition
- Split one cell into multiple keys when it contains independently meaningful values with clear boundaries, even if they appear in a single line.

## 2.5 Row hierarchy preservation
- If row labels are implicit, unlabeled, or nested within the same column, preserve all meaningful hierarchy levels
  and assign stable field names consistently by hierarchy depth
  (e.g., row_header_level_1, row_header_level_2, row_header_level_3, row_item).
- Do not drop intermediate parent headers; propagate all applicable upper-level row headers
  into each row object so every row remains self-contained and interpretable on its own.

## 2.6 Key naming
Each key name must be self-explanatory even when viewed alone, while staying within 64 characters.

- Use the document's wording as much as possible.
- Include upper-level path/context in the key name as fully as needed: section titles, box titles,
  table titles, row headers, column headers, and multi-level header paths when they determine meaning.
- Do not omit upper headers for some sibling keys while keeping them for others.

## 2.7 Selection fields
Design checkbox/radio/selection fields by semantic choice group, not by visible box count.

- If options are mutually exclusive, use one `string` key and return the label text of the marked option.
- If multiple selections are allowed, use one `array_of_string` key and return only the marked labels in document order.
- If the checked state itself has independent business meaning, define separate `boolean` keys.

# 3. Description design

Descriptions must be defined unambiguously so that different annotators using the same template extract
the same single value consistently. Write descriptions as precise extraction rules
that leave no room for interpretation.

Descriptions must be written in a generalized, reusable way for all documents under the same template or document set, not tied to sample-specific wording, values, or exact source text.
Never include any sample-specific value from the provided documents in the description.
If an example is necessary to clarify the rule, use a generic or synthetic example that does not come from the provided documents.


## 3.1 What descriptions should specify when applicable

Descriptions should include as many of the following as applicable. Prefer rules that,
from the extraction user's perspective, 1) produce unambiguous and consistent values,
and 2) remove unnecessary elements so only the needed value is extracted.

### A. Path
Specify the target by semantic identifiers such as section names, field labels, and table/header names,
not by fixed layout, position, or line order. For table fields, use column or grouped header names.

### B. Boundary
Define exact extraction boundaries: where the value starts and ends.
Prefer boundaries that capture exactly the semantic value intended by the key.

### C. Inclusion / exclusion
State whether to include or exclude labels, numbering, notes, parentheses, postal codes, units, currency symbols, punctuation, footnote markers, or surrounding text.
Prefer atomic extraction: exclude non-essential attached elements unless they are part of the intended value.

### D. Output format
Specify whether to preserve original text or normalize it, and define the normalization rule if used.
Prefer fixed output formats for dates, amounts, units, IDs, and addresses, and explicit whitespace rules.

When relevant, descriptions should explicitly define:
- date format,
- number/amount formatting,
- negative number normalization,
- whether commas, percent signs, currency symbols, or decimals are preserved,
- whether IDs/business numbers preserve hyphens/original form,
- whitespace normalization,
- address joining/preservation rules,
- unit handling,
- parenthetical note handling,
- whether surrounding punctuation is preserved,
- whether original typos/errors must be preserved exactly.

### E. Blank handling
Never omit a key because the value is missing. Use type defaults.
If the document literally shows placeholder-like values such as `-`, `N/A`, `해당 없음`, or equivalent text, extract them exactly as written; do not treat them as blank.

### F. Duplicate handling
If the same extractable value may appear multiple times and all occurrences are meaningful, use an array and return all occurrences in document order without deduplication.

### G. Multiple candidates
If multiple candidates exist, define a stable selection rule in the description, such as by proximity, header priority, or first occurrence.
If no stable rule exists, use an array instead of a scalar.

# 4. Additional rules for `array_of_object`

When defining a repeated table/group as `array_of_object`, descriptions must make row construction unambiguous and each output row independently interpretable.

## 4.1 Merged cells
If a cell is merged across multiple rows, repeat the upper-row value into all applicable lower rows so every output row is independently interpretable.

## 4.2 Row types
Define row handling rules clearly when needed:
- SECTION row: grouping/header-only row with no actual data values. Do not create a separate output row for it; use it only as context for lower rows.
- CATEGORY row: subtotal/category row that has its own value. Explicitly decide how category/item fields are populated so the row remains independently interpretable.
- ITEM row: lowest-level regular data row.

## 4.3 Row order
Preserve original document row order exactly.
Do not renumber, fill gaps, or repair non-consecutive numbering.

## 4.4 Table scope
State whether totals, subtotals, notes, or differently scoped rows belong in the repeated table.
If not, extract them as separate scalar keys with the same table/section prefix.

# Final requirements

You must satisfy all of the following:
- Maximize coverage of important information, and place the most important fields first.
- Preserve document meaning and hierarchy in the key names using snake_case.
- Preserve all meaningful row hierarchy levels, and create explicit keys for omitted or unlabeled levels whenever rows differ in hierarchical depth.
- Use repetition semantics, not visual layout, to decide array vs non-array structure.
- Write precise descriptions that remove ambiguity and make extraction consistent across annotators.
- Descriptions must be written in a generalized, reusable way for all documents under the same template.
