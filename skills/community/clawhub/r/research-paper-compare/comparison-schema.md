# Comparison Schema

## Goal

Represent each paper with the same analytical fields before comparison.

## Required Paper Record

For each paper, extract the following fields:

- `title`
- `authors`
- `year`
- `venue`
- `pdf_source`
- `evidence_quality`
- `problem`
- `motivation`
- `core_method`
- `method_components`
- `assumptions`
- `training_or_construction_setup`
- `evaluation_setup`
- `datasets_or_benchmarks`
- `metrics`
- `main_results`
- `claimed_contributions`
- `strengths`
- `weaknesses`
- `limitations`
- `best_fit_scenarios`
- `notes_on_comparability`

## Extraction Guidance

### Problem

State the task or research question the paper addresses.

### Core method

Summarize the main method in 2-4 sentences using technical precision.

### Method components

List the main modules, mechanisms, or stages.

### Assumptions

Record modeling assumptions, data assumptions, or system assumptions that affect fairness of comparison.

### Evaluation setup

Record datasets, tasks, baselines, and protocol details needed for valid comparison.

### Main results

Summarize the most relevant quantitative and qualitative outcomes without overstating claims.

### Strengths / weaknesses / limitations

Separate author-claimed advantages from evidence-based critical assessment when possible.

### Notes on comparability

State whether direct comparison is valid, partially valid, or weak because of dataset or protocol mismatch.

## Cross-Paper Comparison Axes

Use these default axes unless the user asks for a more specific focus:

1. Problem setting
2. Core method
3. Key novelty
4. Experimental setting
5. Main strengths
6. Main weaknesses
7. Limitations
8. Best use scenarios
9. Comparability caveats
10. Evidence quality

## Minimum Quality Bar

Do not compare papers until all required fields are populated at least at a usable level.
If critical fields such as method, evaluation setup, or main results are missing, report insufficient evidence.
