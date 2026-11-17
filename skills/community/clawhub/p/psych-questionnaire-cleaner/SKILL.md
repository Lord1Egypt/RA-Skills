---
name: psych-questionnaire-cleaner
description: Clean, score, and audit psychology questionnaire or survey datasets with reproducible rules, participant-level quality flags, privacy protection, Chinese-language outputs, and traceable reports. Use for 心理学问卷、量表、调查数据的缺失值、异常编码、重复记录、作答质量、反向计分和分量表清洗；do not use to diagnose participants or invent an instrument's scoring key.
metadata: {"openclaw":{"emoji":"🧹"}}
---

# Psychology Questionnaire Cleaner

Clean questionnaire data reproducibly while preserving the distinction between raw observations, mechanical corrections, quality flags, exclusions, and scale scores.

## Non-negotiable boundaries

- Preserve the source file unchanged. Write results to a new output directory and never overwrite raw data.
- Treat participant data as sensitive. Minimize identifiers in reports, avoid printing row-level sensitive answers, and do not upload data to external services without explicit authorization.
- Never invent item ranges, reverse-keyed items, subscales, missing-value codes, attention-check answers, exclusion thresholds, or scoring rules.
- Do not diagnose, label, or infer a participant's mental-health condition. This skill cleans research data; it does not provide clinical interpretation.
- Default to flagging questionable records rather than deleting or silently changing them. Apply exclusions only when the user or an approved cleaning plan supplies the rule.
- Keep observed values, cleaned values, derived flags, exclusion decisions, and scale scores distinguishable and traceable.
- Treat the response-time and attention-check exclusions below as user-approved rules. Remove excluded rows from the analytical dataset, but preserve them in a separate exclusion record and the audit log; never delete them from the source file.
- Produce all user-deliverable filenames, column names, rule descriptions, logs, and narrative reports in Simplified Chinese. Preserve the raw source file unchanged and provide a reversible original-to-Chinese column-name map whenever source fields are renamed in an output.

## Choose the operating mode

Use the least destructive mode that satisfies the request:

1. **Audit**: profile the data and produce flags and recommendations without changing analytical values.
2. **Clean**: normalize declared missing codes, types, and structural problems; retain all rows unless an exclusion policy is supplied.
3. **Score**: clean first, then compute declared reverse-scored items, subscales, and total scores.

If the user does not choose a mode, use **Audit + non-destructive Clean**. Do not score until an item dictionary or authoritative scoring key is available.

## Establish the cleaning plan

Look for a protocol, preregistration, codebook, questionnaire manual, item dictionary, or an existing cleaning configuration. When no plan exists, read [references/cleaning-plan-template.md](references/cleaning-plan-template.md) and create a draft plan from evidence in the supplied files.

Clearly separate:

- **Confirmed rules** from the user, protocol, or scoring key.
- **Safe structural rules** such as exact duplicate detection and type-parse failures.
- **Proposed rules** that require user approval, such as a response-time cutoff or participant exclusion.

The following user-approved rules are exceptions to the ordinary flag-only default:

- **Response time**: using all parseable, finite, positive durations in the declared analysis cohort before any quality exclusion, calculate one median `M`. Exclude a record from the analytical dataset when `duration < M / 3` or `duration > 3M`; both bounds are inclusive. Do not calculate a replacement median after exclusions. If no valid duration or no declared duration field exists, record the rule as not executable and do not infer one from incompatible timestamps.
- **Attention checks**: when an attention check has a declared expected answer, exclude a record when its non-missing response does not match any declared acceptable answer. Treat a missing or unparseable attention-check response as a separate flag unless the cleaning plan explicitly defines it as a mismatch.

Read [references/quality-indicators.md](references/quality-indicators.md) for the exact calculation, output fields, and the definition of regular-response flags.

Ask only for missing information that would materially change values or exclusions. Continue with an audit when scoring or exclusion details are unavailable.

## Inspect before transforming

Record enough provenance to reproduce the run:

- input filenames, file hashes when feasible, worksheet/table names, row and column counts;
- column names and a reversible rename map;
- participant/session identifiers and whether identifiers appear unique;
- item, metadata, timing, attention-check, and free-text columns;
- observed types, declared valid ranges, undeclared codes, and missing-value tokens;
- exact duplicate rows and duplicate identifier groups;
- missingness by variable and participant;
- transformations planned and their evidence source.

Do not expose raw participant responses in the narrative report. Use aggregate summaries and pseudonymous row keys.

## Apply structural cleaning

Perform only documented transformations and log each one:

- Trim accidental surrounding whitespace and normalize declared missing tokens without altering meaningful free text.
- Parse dates, durations, and numerics with explicit failure flags; do not coerce failures to valid-looking values.
- Flag values outside confirmed item ranges. Do not winsorize, clip, or replace questionnaire responses by default.
- Detect exact duplicate rows and duplicate participant/session identifiers separately. Resolve duplicates only with a declared policy; otherwise retain and flag them.
- Preserve original column names or write a reversible name map when names are normalized.
- Keep item nonresponse distinct from structural missingness, not-applicable values, skipped branches, and technical missingness whenever the source supports that distinction.

## Evaluate response quality

Read [references/quality-indicators.md](references/quality-indicators.md) when the request includes careless responding, low-quality responses, bots, speeders, straightlining, or participant exclusion.

Create one column per indicator and retain its underlying numeric value. Do not collapse unlike indicators into a single opaque judgment. Apply the approved response-time and attention-check exclusions above; use preregistered or user-approved cutoffs for any other exclusion, otherwise present sensitivity summaries and label cutoffs as proposals.

Flag regular response patterns, including declared longstrings, repeating cycles, and strictly monotonic runs, using the definition in [references/quality-indicators.md](references/quality-indicators.md). These are descriptive flags only and must not trigger exclusion unless the user later approves a separate rule. Do not run pattern detection across unrelated sections, different response ranges, attention checks, or free-text columns.

Never treat a long identical-response run, low within-person variability, multivariate outlier status, or a regular-response flag alone as proof of invalid responding. If a combined exclusion rule is approved, state its Boolean logic exactly and preserve all component flags.

## Score only from an authoritative key

Before scoring, confirm for every scale:

- included items and item-to-subscale mapping;
- valid minimum and maximum for each item;
- reverse-keyed items;
- sum versus mean scoring;
- allowed missingness and any prorating rule;
- whether attention checks or non-scale items are excluded.

For a reverse-keyed item with confirmed bounds `min` and `max`, compute:

```text
reversed = min + max - observed
```

Do not apply this formula to out-of-range or unresolved values. Name derived columns so they cannot be confused with raw items. Compute scores only when the confirmed completeness rule is met, and emit a score-status or score-missing-reason column.

Do not use internal consistency, factor loadings, correlations, or outcome associations to delete participants unless the user explicitly requests a documented psychometric analysis. Keep reliability and construct validation separate from routine data cleaning.

## Produce traceable outputs

Follow [references/output-contract.md](references/output-contract.md). At minimum, deliver:

- a Chinese-named analytical dataset that retains stable row identity and excludes only records covered by approved rules;
- a separate Chinese-named exclusion record containing every removed row, its rule, and its reason;
- Chinese participant/row-level flag columns and exclusion status;
- a Chinese machine-readable audit log of transformations and decisions;
- a Chinese resolved cleaning plan showing confirmed, proposed, and unused rules;
- a concise Chinese quality report with counts before and after each approved rule;
- a Chinese list of unresolved questions that could affect analysis.

Validate that row counts reconcile, identifiers remain traceable, raw values can be recovered, score formulas match the plan, and repeated runs with the same inputs and plan produce the same outputs.

## Communicate results

Lead with what changed and what did not. Report the number of records flagged and excluded separately. Distinguish data errors from plausible but unusual responses, and distinguish rule-based exclusions from exploratory sensitivity analyses. Warn when conclusions depend materially on an unapproved cutoff or missing scoring information.
