## Description:

Historical Baseline Analysis helps agents compare retail store performance against multi-period baselines and quartile statistics from Agent API database views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operators, analysts, and agent developers use this skill to compare store sales, order count, unit price, and attach-rate metrics with historical weekday baselines and identify abnormal performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe database query construction can expose real store data workflows to injection or incorrect query behavior.

Mitigation: Use parameterized database queries, validate store and date inputs, and run the skill with read-only least-privilege database access.

Risk: A hard-coded local import path loads an external module that is not part of the reviewed artifact.

Mitigation: Remove the hard-coded path and package any required client dependency through a reviewed, documented dependency path.

Risk: Week and month analysis are described by the skill, but the artifact indicates those paths are not implemented yet.

Mitigation: Document the current weekday-only implementation or complete and test week and month analysis before relying on those modes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwyang7/skills/retail-store-poscore-baseline-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JSON-like Python dictionaries and Markdown-ready analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include baseline statistics, percentile ranks, outlier status, and attribution findings.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
