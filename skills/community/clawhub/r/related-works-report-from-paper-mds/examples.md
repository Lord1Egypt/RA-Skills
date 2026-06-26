# Related Works Report Examples

## Minimal invocation

Use when the paper markdown files are already known and the user has provided a work folder:

```text
/related-works-report-from-paper-mds "0_refs/paper_mds/2025_ConfidenceVLA.md 0_refs/paper_mds/2025_SAFE.md 0_refs/paper_mds/2025_FAIL_Detect.md --workdir 0_docs/related_works_report_run_02"
```

## Invocation with a new work folder

Use a fresh folder when you want to keep an older run untouched:

```text
/related-works-report-from-paper-mds "0_refs/paper_mds/2025_ConfidenceVLA.md 0_refs/paper_mds/2025_SAFE.md 0_refs/paper_mds/2025_FAIL_Detect.md --workdir 0_docs/related_works_report_run_03"
```

## Expected work folder layout

After a successful run, `WORKDIR` should look roughly like:

```text
WORKDIR/
├── step1_extracted_related_works_and_citations.md
├── step1_normalized_related_works.md
├── step2_deduplicated_paper_list.md
├── final_related_works_report.md
├── title_batches/
│   ├── batch_01.md
│   ├── batch_02.md
│   └── ...
└── abstract_batches/
    ├── batch_01_fetches.jsonl
    ├── batch_01_results.md
    ├── batch_02_fetches.jsonl
    ├── batch_02_results.md
    └── ...
```

## What each artifact is for

- `step1_extracted_related_works_and_citations.md`: verbatim Related Works text plus citation tables from each source paper.
- `step1_normalized_related_works.md`: companion version of Part 1 with citations rewritten to dedup ids like `P001` when the mapping is unambiguous.
- `step2_deduplicated_paper_list.md`: the canonical paper list used for abstract lookup and final ordering.
- `abstract_batches/batch_XX_fetches.jsonl`: one JSON line per title, written incrementally during Tavily + arXiv processing.
- `abstract_batches/batch_XX_results.md`: readable markdown rendered from the JSONL batch file.
- `final_related_works_report.md`: final merged report with summary, original Related Works text, normalized citation companion text, and BibTeX-style entries with abstracts.

## Interpreting partial runs

If a run is interrupted, the work folder should still be useful:

- finished `step1` and `step2` files allow abstract retrieval to resume later
- existing `batch_XX_fetches.jsonl` files preserve already processed titles
- existing `batch_XX_results.md` files can be regenerated from the JSONL if needed

## Tavily-only expectation

Abstract lookup should follow this rule:

- search is done with Tavily only
- if Tavily fails or rate limits, retry Tavily only
- do not switch to arXiv API search, guessed arXiv URLs, or another search provider

## Typical final report structure

`final_related_works_report.md` should contain:

1. `Summary`
2. `Part 1. Related Works Original Text`
3. `Part 1B. Related Works with Normalized Citations`
4. `Part 2. BibTeX with Abstracts`
