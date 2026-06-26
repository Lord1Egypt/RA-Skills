---
name: related-works-report-from-paper-mds
description: Build a related-works report from one or more paper markdown files by extracting Related Works sections, resolving cited papers, deduplicating references, retrieving arXiv abstracts via Tavily plus local helpers, and assembling a final report inside a user-specified work folder. Use when the user points at paper_mds, wants a related-works survey report, or asks to turn several paper markdown files into a final_related_works_report.md.
argument-hint: [paper-md-paths --workdir path]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, Skill, call_mcp_tool, WebFetch
---

# Related Works Report Pipeline

Orchestrate a full related-works reporting workflow for: **$ARGUMENTS**

## Overview

This workflow turns a small set of paper markdown files into a reproducible report:

```text
paper md files
-> step1 extract Related Works + cited papers
-> step2 deduplicate cited papers
-> sequential Tavily abstract lookup + local arXiv fetch
-> normalized citation companion text
-> final_related_works_report.md
```

The output is not just the final report. Every intermediate artifact is written into the user-selected **work folder** so the process can be resumed, audited, or partially rerun.

## Required Inputs

Before running, collect or infer:

- **PAPER_MD_PATHS**: one or more paper markdown paths
- **WORKDIR**: a user-specified working folder

If `WORKDIR` is missing, ask the user for it before doing substantial work.

All process outputs and the final report must be written under `WORKDIR`. Do not write process artifacts elsewhere.

## Constants

- **TAVILY_ONLY = true** — Tavily is the only allowed search mechanism for title-to-arXiv matching
- **TAVILY_BATCH_MODE = sequential** — finish batch N before batch N+1
- **NO_SEARCH_FALLBACK = true** — if Tavily fails, record the failure; do not switch to arXiv search, arXiv API search, or another provider
- **LOW_CONTEXT_ABSTRACT_MODE = true** — write one JSON line per title, then render markdown from JSONL
- **CITATION_NORMALIZATION_REQUIRED = true** — the final workflow must consider a normalized-citation companion section so Part 1 can be aligned with dedup ids like `P001`
- **FINAL_REPORT_NAME = `final_related_works_report.md`**

## Work Folder Layout

Create and maintain these artifacts under `WORKDIR`:

| Artifact | Purpose |
|----------|---------|
| `step1_extracted_related_works_and_citations.md` | Per-source Related Works verbatim + citation tables |
| `step1_normalized_related_works.md` | Citation-normalized companion text using dedup ids like `P001` when replacement is unambiguous |
| `step2_deduplicated_paper_list.md` | Deduplicated paper list with source occurrences |
| `title_batches/batch_XX.md` | Abstract lookup batches |
| `abstract_batches/batch_XX_fetches.jsonl` | One JSON line per title after Tavily + local fetch |
| `abstract_batches/batch_XX_results.md` | Rendered markdown per abstract batch |
| `final_related_works_report.md` | Final assembled report |

## Execution Rule

Run phases in order. Do not stop after a checkpoint unless:

- the user explicitly says to stop, or
- an input is missing and must be confirmed, or
- Tavily failures are severe enough that the user should decide whether to continue with partial results

Parallelism rules:

- **Phase 1 extraction** may use one clean-context sub agent per source paper.
- **Phase 3 abstract lookup** must run batches sequentially, not in parallel.

## Phase 0: Initialize the Work Folder

1. Validate `PAPER_MD_PATHS`.
2. Create `WORKDIR`, `WORKDIR/title_batches`, and `WORKDIR/abstract_batches`.
3. Record the chosen source files in the first process artifact.

## Phase 1: Extract Related Works and cited papers

Use one clean-context sub agent per source markdown file.

Each sub agent must return:

- the verbatim Related Works section
- the papers cited inside that section
- enough citation metadata to later support normalization and deduplication:
  - citation token in the text (`[12]`, `Guo et al., 2017`, etc.)
  - year
  - title
  - authors
  - raw reference text

Merge all outputs into `WORKDIR/step1_extracted_related_works_and_citations.md`.

## Phase 2: Deduplicate cited papers

Build `WORKDIR/step2_deduplicated_paper_list.md`.

Rules:

- deduplicate conservatively by normalized title
- merge only when the works are clearly the same paper
- preserve source occurrences so every original citation can be traced back

## Phase 2B: Citation normalization companion text

Before final assembly, produce `WORKDIR/step1_normalized_related_works.md`.

Goal:

- keep the original Related Works text untouched in `step1_extracted_related_works_and_citations.md`
- create a companion version where in-text citations are rewritten to dedup ids like `P001`

Preferred format:

- numeric citations: `[12]` -> `[P052]`
- author-year citations: `(Guo et al., 2017)` -> `[P095]`
- grouped citations: rewrite each cited work individually when the mapping is unambiguous

Rules:

- only replace citations when the mapping from source citation token to dedup id is unambiguous
- if a citation is ambiguous, keep the original token and add a short note below that section
- do not overwrite the verbatim source text

This step exists because the final report should be easy to align with the deduplicated bibliography.

## Phase 3: arXiv abstracts via Tavily + local helper

Use the helper scripts stored inside this skill:

- `.cursor/skills/related-works-report-from-paper-mds/scripts/fetch_arxiv_abs.py`
- `.cursor/skills/related-works-report-from-paper-mds/scripts/jsonl_to_abstract_batch_md.py`

### Search rules

- Tavily MCP only
- query shape: `"<paper title>" arXiv`
- preferred matches: `abs`, then `html`, then `pdf`
- convert `html`/`pdf` to canonical `https://arxiv.org/abs/<id>`
- no fallback search provider

### Batch rules

- process batches sequentially
- inside a batch, process titles one by one
- if Tavily rate limits, wait and retry Tavily only
- if Tavily still fails, record the error in the JSONL and leave `arXiv URL` and `Abstract` empty

### Low-context pattern

For each processed title, immediately append one JSON line to:

- `WORKDIR/abstract_batches/batch_XX_fetches.jsonl`

Each line should include at least:

- `dedup_id`
- `input_title`
- `tavily_status`
- `tavily_error`
- `arxiv_url`
- `fetch`

After a batch completes, render markdown with:

```bash
python3 ".cursor/skills/related-works-report-from-paper-mds/scripts/jsonl_to_abstract_batch_md.py" \
  "WORKDIR/abstract_batches/batch_XX_fetches.jsonl" \
  "WORKDIR/abstract_batches/batch_XX_results.md"
```

## Phase 4: Final assembly

Use the final builder script stored inside this skill:

```bash
python3 ".cursor/skills/related-works-report-from-paper-mds/scripts/build_final_related_works_report.py" \
  "WORKDIR/step1_extracted_related_works_and_citations.md" \
  "WORKDIR/step2_deduplicated_paper_list.md" \
  "WORKDIR/abstract_batches" \
  "WORKDIR/final_related_works_report.md" \
  "WORKDIR/step1_normalized_related_works.md"
```

The final report should contain:

- **Summary**
- **Part 1**: Related Works original text
- **Part 1B**: citation-normalized companion text
- **Part 2**: BibTeX-style entries with retrieved abstracts when available

## Key Rules

- Never fabricate a paper match or abstract.
- Never use non-Tavily search when resolving titles to arXiv.
- Keep all process artifacts inside `WORKDIR`.
- Prefer scripts inside this skill over ad hoc in-message code.
- Preserve source-paper order in Part 1.
- Preserve dedup order from `step2` in Part 2.

## Utility Scripts

- `scripts/fetch_arxiv_abs.py` — compact metadata + abstract extraction from a known arXiv URL
- `scripts/jsonl_to_abstract_batch_md.py` — render one batch markdown from JSONL
- `scripts/build_final_related_works_report.py` — assemble the final report from workdir artifacts

## Additional Resources

- For copy-paste invocations and expected `WORKDIR` contents, see [examples.md](examples.md)

## Example Invocation

```text
/related-works-report-from-paper-mds \
  "0_refs/paper_mds/2025_ConfidenceVLA.md 0_refs/paper_mds/2025_SAFE.md 0_refs/paper_mds/2025_FAIL_Detect.md --workdir 0_docs/related_works_report_run_02"
```
