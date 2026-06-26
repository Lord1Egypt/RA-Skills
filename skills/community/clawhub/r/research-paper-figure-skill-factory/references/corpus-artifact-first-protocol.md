# Corpus Artifact First Protocol — v1.11, retained and clarified in v1.13

## Purpose

The guide must make literature acquisition visible and auditable before taxonomy construction. B3 is complete for B4 only when the local corpus artifacts are created, or the inability to create them is recorded with a concrete fallback request.

## Required directory

Default path:

```text
/mnt/data/<target-skill-slug>-corpus/
  papers/
  metadata/
    retrieval_manifest.csv
    retrieval_manifest.json
    acquisition_report.md
    failed_or_blocked_items.md
    figure_inspection_queue.md
    corpus_coverage_report.md
```

## Manifest requirements

Each item should include: item id, title, authors, year, venue, presentation status, official oral evidence by default, with spotlight/award only as user-approved fallback, stable id, landing URL, PDF URL, source route, access basis, acquisition status, local PDF path, inspection level, inclusion reason, limitations, and next action.

## Full-feasible-corpus rule

When local PDFs, a paper index, or prior retrieval manifests already exist, B3 must enumerate the full relevant candidate set before extraction scope is chosen. The default scope is `all_accessible_relevant_pdfs`.

Do not stop at a small fixed sample when many relevant PDFs are available. A sample may be used only for a human contact sheet, a quick pilot explicitly requested by the user, or a resource-limited run. In those cases, B3 must record:

- total candidate PDF count;
- accessible PDF count;
- selected/processed count;
- skipped count;
- skipped reasons;
- whether the run can support `production_grade` or only `limited`, `pilot`, or `fallback`.

The acquisition report or `corpus_coverage_report.md` must state whether the corpus was full-feasible, chunked/resumable, or intentionally sampled.

## v1.13 gating

Do not proceed to B4 unless `local_corpus.ready_for_extraction: true`. This can be true because:

- open-access/user-authorized PDFs exist locally;
- user-uploaded PDFs exist locally;
- a mixed corpus is sufficient for extraction and limitations are recorded;
- the user explicitly accepts metadata-only or caption-only fallback.

If none of these applies, ask the user for PDFs/permitted links and keep the active step at B3.

`local_corpus.ready_for_extraction: true` does not by itself mean the corpus is production-grade. Production-grade skill generation additionally requires a coverage assessment showing that available relevant PDFs were processed as fully as feasible, or that any cap is explicitly justified and recorded.

`local_corpus.ready_for_taxonomy` is deprecated compatibility shorthand. It must not be used as the B4 or B5 gate. B5 uses `extracted_evidence.ready_for_taxonomy`.

## Honesty rule

Never claim that a paper was downloaded, opened, or visually inspected unless the state and manifest show it. Metadata-only discovery is useful, but must stay labeled as metadata-only.

## v1.0.0 Recent Two-Year CS Oral Corpus Artifact Requirements

For the default builder-time acquisition route, the corpus artifact must target recent two-year computer-science top-conference oral papers. The manifest must prove that every included default-corpus item is actually an oral paper.

Additional required manifest columns:

```text
year_window_rule,venue_family,venue_tier,is_cs_top_conference,presentation_filter_required,oral_status_verified,official_oral_evidence_source_type,official_oral_evidence_url,official_oral_evidence_local_path,fallback_reason_if_not_oral
```

The acquisition report must include:

- resolved year window;
- selected CS top-conference venue set;
- search routes used for official oral lists;
- count of verified oral papers;
- count of unverified oral candidates;
- count and reasons for fallback non-oral items, if user-approved.

Rows without official oral evidence cannot count toward `verified_oral_count` and must not be used to claim an oral corpus.
