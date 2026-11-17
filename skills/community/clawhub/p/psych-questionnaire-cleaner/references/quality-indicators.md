# Response-quality indicators

Use indicators as transparent evidence, not diagnoses of participant intent. Calculate each indicator only on the item set for which it makes sense and keep the numeric value alongside any threshold flag.

## Completion time

- Use the declared duration field. Derive duration from timestamps only when they are compatible and the plan explicitly permits it.
- Before applying any quality exclusion, select all parseable, finite, strictly positive durations in the declared analysis cohort and calculate their median `M` once.
- Keep a record in the analytical dataset exactly when `M / 3 <= duration <= 3M`. Exclude a record when its duration is below `M / 3` or above `3M`.
- Store `M`, the lower bound, upper bound, duration value, and the result of the range test in the resolved plan, audit log, and quality report. Do not recompute `M` after exclusions.
- Flag a missing, non-numeric, non-finite, zero, or negative duration as `作答时长无效`; do not silently classify it as fast or slow. If the plan does not define how invalid durations are handled, retain and flag them rather than excluding them.
- If the study has predeclared cohorts that must have separate medians, use those cohorts only when they are named in the plan; otherwise calculate one cohort-wide median.

## Missingness

- Calculate missingness by participant and by item.
- Separate ordinary item nonresponse, branch-induced structural missingness, not-applicable codes, and technical failures when possible.
- Apply scale-specific scoring completeness rules independently of whole-survey missingness.

## Longstring / straightlining

- Compute the longest run of identical responses only across the declared item order.
- Do not bridge unrelated sections, different response scales, reverse-coded transformations, or non-item columns.
- Preserve the longest-run length, item range, and threshold used.
- A long run can be a legitimate response pattern; combine it with other evidence only through an approved rule.

## Within-person response variability

- Calculate variability only across items with compatible response scales and interpretation.
- Record the exact statistic, item set, handling of missing values, and threshold.
- Low variability is not inherently invalid when the construct or sample plausibly produces homogeneous answers.

## Attention and instructed-response checks

- Use only checks declared in the instrument or protocol.
- Record the expected answer, accepted alternatives, and treatment of missingness.
- Exclude a record when any non-missing attention-check response fails to match its declared expected or acceptable answer. Record the failed item and expected/observed category in `排除原因` and the audit log.
- A missing or unparseable attention-check response is a separate `注意力检测缺失或无效` flag, not a mismatch, unless the plan explicitly says otherwise.
- Keep check failures separate by item even when the resulting action is exclusion.

## Regular response patterns

Flag patterns only within a declared ordered group of compatible questionnaire items. Use raw or mechanically cleaned item values before reverse scoring; never span unrelated sections, different response ranges, attention checks, metadata, or text fields. The flag is evidence for review, not an exclusion rule.

- **连续同值（longstring）**: the longest contiguous run of the same valid response.
- **重复循环**: an exact repeating cycle with length 2, 3, or 4 that completes at least twice, such as `1,2,1,2` or `1,2,3,1,2,3`.
- **严格单调序列**: at least four contiguous valid responses that strictly increase or strictly decrease, such as `1,2,3,4` or `5,4,3,2`.

For every flagged row, output these Chinese fields: `规律作答标记`, `规律作答类型`, `规律作答最长长度`, and `规律作答题目范围`. A row may have more than one type. Missing values break a run or cycle; do not bridge across them. Do not exclude on the basis of these flags without a later, explicitly approved exclusion rule.

## Logical consistency checks

- Use only item pairs or branching rules whose relationship is declared in the plan.
- Distinguish true logical impossibility from psychological inconsistency or change over time.
- Never create ad hoc consistency rules merely because two items correlate weakly.

## Duplicate and bot-like patterns

- Detect exact duplicates, repeated identifiers, repeated network/device metadata, and highly similar response vectors as separate signals.
- Treat shared devices, classrooms, households, and repeated-study designs as plausible explanations.
- Do not identify a person or a bot from a single technical signal.

## Outliers and advanced person-fit statistics

- Univariate or multivariate outlier status is not equivalent to careless responding.
- Use person-fit, Mahalanobis distance, response entropy, or model-based indicators only when the user requests them and the analysis assumptions are documented.
- Keep thresholds exploratory unless they are preregistered or otherwise approved.

## Combining indicators

Avoid an opaque quality score. Prefer explicit expressions such as:

```text
exclude = failed_attention_checks >= 2
       OR (duration_flag AND longstring_flag)
```

This is a syntax example, not a recommended rule. Report how many rows are flagged by each component and by the combined expression. The approved response-time and attention-check rules are applied independently; regular-response flags remain flag-only. When no other rule is approved, provide sensitivity counts across plausible thresholds without excluding rows.
