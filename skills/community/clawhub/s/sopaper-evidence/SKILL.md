---
name: sopaper-evidence
description: Evidence-first research workflow for evidence discovery, source verification, and citation grounding. Use when the task requires searching, verifying, and organizing real papers, datasets, benchmarks, case studies, and project artifacts without fabricating results, citations, or claims.
---

# Sopaper Evidence

Sopaper Evidence is an evidence-first research skill. Its job is to build a reliable evidence pack before supporting any downstream paper outline, abstract, related work summary, experiment plan, or draft section.

Version: `v1.1.1`

## Upstream source

Canonical repository: `https://github.com/sheepxux/SoPaper-Evidence`

This published skill bundle includes the helper scripts it references under `scripts/`. The GitHub repository remains the public source of truth for releases, examples, and issue tracking.

## Use this skill when

- The user wants to turn a project into a paper without inventing evidence
- The task requires finding prior papers, datasets, benchmarks, baselines, or case studies
- The task requires mapping claims to verified sources
- The task requires identifying evidence gaps before writing
- The user wants related work or experiment planning grounded in real sources

## Hard rules

- Do not fabricate papers, authors, venues, dates, citations, datasets, benchmarks, experiments, or numerical results
- Prefer primary sources over summaries, reposts, or blog interpretations
- Reject non-public URLs before fetching external pages; do not fetch localhost, private-network, link-local, non-HTTP(S), or credential-bearing URLs
- Separate verified facts from inference and open questions
- If evidence is missing, say it is missing and recommend what to collect next
- Do not state that the user's method outperforms baselines unless there is explicit evidence
- Every writing-oriented output must be traceable to evidence items

## Source priority

Use the highest-quality source available for each claim.

1. User-provided project artifacts: experiment logs, tables, code, configs, internal notes
2. Primary external sources: papers, official docs, benchmark leaderboards, dataset pages, project repos
3. Secondary summaries: blogs, news posts, third-party explainers

Read [references/source-priority.md](references/source-priority.md) when source quality or conflicts matter.
Read [references/input-schemas.md](references/input-schemas.md) when stronger input structure is needed before running the workflow.

## Core workflow

### 1. Scope the task

Collect or infer:

- Project name
- Research topic
- Core problem
- Method summary
- Existing evidence and file paths
- Target venue or paper style if known

If the project scope is unclear, produce a short working scope and label assumptions.

### 2. Search for evidence

Search for:

- Prior work
- Benchmarks and datasets
- Baseline methods
- Comparable case studies
- Official metrics definitions
- Relevant project artifacts in the local repository

For each source, capture the title, URL or path, source type, and why it matters.

Use [references/prior-work-search-playbook.md](references/prior-work-search-playbook.md) for a repeatable search process.
For OpenClaw-specific work, use [references/openclaw-evidence-playbook.md](references/openclaw-evidence-playbook.md).

### 3. Verify and classify

For each evidence item, classify it as:

- `verified_fact`
- `project_evidence`
- `inference`
- `unverified`

Do not merge these labels. If a statement depends on inference, say so explicitly.

### 4. Extract structured evidence

Use the schema in [references/evidence-schema.md](references/evidence-schema.md).

At minimum, extract:

- Claim or observation
- Source
- Evidence type
- Scope and limitations
- Relevance to the user's paper

### 5. Build the evidence map

Organize findings into:

- `related_work`
- `datasets_and_benchmarks`
- `baselines`
- `case_studies`
- `project_results`
- `claim_to_evidence`
- `evidence_gaps`

Use [assets/claim-evidence-map-template.md](assets/claim-evidence-map-template.md) when the user needs a reusable deliverable.
Use [assets/related-work-matrix-template.md](assets/related-work-matrix-template.md) when comparing papers, baselines, and benchmark coverage.
Use [assets/experiment-gap-report-template.md](assets/experiment-gap-report-template.md) when the task requires prioritizing missing experiments before drafting.
Use bundled `scripts/build_evidence_ledger.py` when the user already has markdown notes or source lists and needs a first-pass evidence ledger.
Use bundled `scripts/generate_search_plan.py` when the user starts only with a topic and needs a first-pass evidence search plan.
Use bundled `scripts/generate_topic_claims.py` when the user starts only with a topic and needs a cautious structured claims draft.
Use bundled `scripts/search_external_sources.py` when the user needs a first-pass source list from a topic or search plan.
Use bundled `scripts/fetch_external_sources.py` when raw URLs should be converted into structured source-note drafts before review.
Use bundled `scripts/verify_source_notes.py` when fetched notes should be conservatively upgraded into page-level verified facts or reviewed primary-source summaries before entering the ledger.
Use bundled `scripts/run_evidence_pipeline.py` when the user already has source files, claims, and optional result artifacts and wants one end-to-end draft pack. Result artifacts may be structured markdown, `.csv`, `.tsv`, or `.json`, and multiple result artifacts can be fused into aggregate project evidence. Use its `--result-dir` option when the user has an experiment directory and wants raw result files discovered recursively.
Use bundled `scripts/bootstrap_claim_map.py` when the user already has a claims list and a ledger draft and needs a first-pass claim map.
Use bundled `scripts/triage_evidence_gaps.py` when the user needs a first-pass blocker/major/minor gap report from the current claims and evidence ledger.
Use bundled `scripts/review_comparison_fairness.py` when the user needs a dedicated fairness check on comparative claims, baseline breadth, metric grounding, and scope alignment.
Use bundled `scripts/run_topic_evidence_pipeline.py` when the user wants the full topic-driven workflow from theme to search plan, source list, fetched notes, optional result-directory ingestion, ledger, claim map, gap report, and fairness review.
Use bundled `scripts/validate_input_bundle.py` when the user has partially structured inputs and needs a quick schema check before running the pipeline.

### 6. Support writing

Only after the evidence map is complete, support tasks such as:

- contribution candidates
- related work summary
- abstract support points
- experiment plan
- paper outline

Before writing, run the checks in [references/claim-audit-rules.md](references/claim-audit-rules.md).
Use [assets/paper-outline-from-evidence-template.md](assets/paper-outline-from-evidence-template.md) when the user needs a draft-safe paper structure.

## Output requirements

Unless the user asks for something else, default to this output shape:

1. `Evidence brief`
2. `Key sources`
3. `Claim-to-evidence map`
4. `Evidence gaps`
5. `Safe writing notes`
6. `Experiment gap report` when blocker gaps exist

See the example set in:

- [examples/openclaw-input.md](examples/openclaw-input.md)
- [examples/openclaw-search-plan.md](examples/openclaw-search-plan.md)
- [examples/openclaw-evidence-brief.md](examples/openclaw-evidence-brief.md)
- [examples/openclaw-claim-map.md](examples/openclaw-claim-map.md)
- [examples/openclaw-gap-report.md](examples/openclaw-gap-report.md)
- [examples/openclaw-source-note.md](examples/openclaw-source-note.md)
- [examples/openclaw-source-list.md](examples/openclaw-source-list.md)
- [examples/openclaw-ledger-draft.md](examples/openclaw-ledger-draft.md)
- [examples/openclaw-claims.md](examples/openclaw-claims.md)
- [examples/openclaw-claims-structured.md](examples/openclaw-claims-structured.md)
- [examples/openclaw-claim-map-draft.md](examples/openclaw-claim-map-draft.md)
- [examples/openclaw-gap-report-draft.md](examples/openclaw-gap-report-draft.md)
- [examples/openclaw-paper-outline.md](examples/openclaw-paper-outline.md)

## Writing constraints

When supporting downstream paper writing:

- Tie each major claim to one or more evidence items
- Avoid precise quantitative wording unless the number is verified
- Mark missing comparisons, missing ablations, and missing real-world validation
- Prefer conservative wording over overstated conclusions

## OpenClaw-specific guidance

When the user is working on OpenClaw or a similar embodied AI / robotics project, prioritize:

- manipulation benchmarks
- long-horizon task evidence
- policy or planner comparisons
- real-world versus simulation evidence
- ablations on perception, planning, or control components

Do not assume OpenClaw has capabilities, datasets, or benchmark wins unless they are present in project artifacts or verified sources.
Use [references/benchmark-baseline-checklist.md](references/benchmark-baseline-checklist.md) before accepting benchmark-fit or baseline coverage claims.
Use [references/evidence-gap-triage.md](references/evidence-gap-triage.md) when deciding whether to keep drafting or stop and report blockers.
