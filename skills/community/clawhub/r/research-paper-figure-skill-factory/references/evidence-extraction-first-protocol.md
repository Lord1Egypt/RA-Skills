# Evidence Extraction First Protocol — v1.12, tightened in v1.13

## Purpose

B3 downloads or organizes a lawful local corpus. B4 must transform that corpus into structured evidence. B5 taxonomy and B6-B7 specialized skill generation must be grounded in that evidence.

## Core rule

A retrieval manifest is not evidence by itself. It only records what was acquired. Evidence for taxonomy requires at least one of:

- full PDF and figure image inspection;
- PDF text and figure caption inspection;
- caption-only inspection with explicit label;
- metadata-only inference with explicit user-approved fallback;
- user-provided reference figure analysis.

## Required B4 artifact directory

```text
<local_corpus.root_dir>/extracted/
  paper_cards.csv
  paper_cards.json
  figure_inventory.csv
  figure_inventory.json
  caption_inventory.csv
  caption_inventory.json
  label_summary.csv
  panel_structure_notes.md
  visual_pattern_observations.md
  evidence_map.json
  extraction_report.md
  extraction_summary.json
  representative_rendered_pages/
```

## Gate sequence

1. B3 sets `local_corpus.ready_for_extraction`.
2. B4 sets `extracted_evidence.ready_for_taxonomy`.
3. B5 builds taxonomy from `evidence_map.json` and related extraction files.
4. B6-B7 generate the specialized skill only after evidence lineage is complete or fallback is explicitly recorded.

## Minimum evidence for a full taxonomy

For a full, non-fallback specialized skill, prefer:

- multiple source papers from the target domain;
- multiple inspected figures per major figure subtype;
- at least one evidence-backed claim per taxonomy axis;
- documented limitations for caption-only or metadata-only items.

If many relevant local PDFs are available, these minimums are only a floor, not permission to stop early. B4 must process all accessible relevant PDFs where feasible, or use chunked/resumable extraction and record any cap. A taxonomy built from a small sample while a much larger relevant local corpus was available must be labeled `pilot`, `thin`, or `fallback` unless the user explicitly accepts the limitation.

Multi-label classification is required whenever a figure can serve multiple roles. A single PDF or diagram may count toward method framework, architecture, pipeline, mechanism, evidence board, case walkthrough, taxonomy, failure/limitation, or other categories. Store label counts and multi-label counts when the figure class taxonomy has more than one applicable angle.

When evidence is thin, label the taxonomy as `pilot`, `thin`, or `fallback` and keep `generated_skill.known_limitations` updated.

## v1.13 Evidence sufficiency labels

During B5 taxonomy drafting, before B5 taxonomy finalization, label the evidence level:

- `full_taxonomy`: enough papers/figures/panels/captions to support a reusable class-specific skill. Default target: at least 8-12 relevant papers and 12-20 inspected figures, unless the user-defined domain is narrower.
- `thin_taxonomy`: useful but partial evidence. It can guide a draft skill, but cannot be represented as production-grade without explicit limitation notes.
- `pilot_taxonomy`: exploratory first pass for planning or corpus expansion.
- `fallback_taxonomy`: based mainly on generic scaffolds, caption-only, metadata-only, or user-approved substitutes.

Every taxonomy claim must be represented in `evidence_map.json` or recorded as a `generic_fallback_claim`. Unsupported core claims prevent `evidence_lineage.evidence_lineage_complete` from becoming true.


## v1.15 lock-grade clarification

Evidence sufficiency may be assessed during B5 taxonomy drafting, but it must be finalized before B5 taxonomy finalization and re-checked before B7 skill package locking. Only `full_taxonomy` can support `generated_skill.lock_grade: production_grade`. Thin, pilot, or fallback evidence can only support `limited`, `pilot`, or `fallback` lock grades after explicit user acceptance and limitation recording.

## v1.16 builder-time extraction rule

For specialized skill generation, B4 evidence extraction belongs to the builder run. The guide must create the first `extracted/` evidence artifacts before generating a production-grade specialized skill. The generated specialized skill may include future corpus refresh logic, but it should not be responsible for the initial extraction that justifies its taxonomy.
