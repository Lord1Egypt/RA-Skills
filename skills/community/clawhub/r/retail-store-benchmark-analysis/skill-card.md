## Description:

门店Benchmark分析 compares a retail store against group, regional, provincial, or city peers and reports rank, tier, rank change, and piece-price by attach-rate quadrant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail analysts, operations managers, and agents use this skill to benchmark an individual store against a selected comparison scope, identify its performance tier, track ranking changes, and understand its position in a piece-price and attach-rate matrix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports unsafe database query construction.

Mitigation: Run only with parameterized queries, strict validation for dates and comparison scope, and read-only database credentials.

Risk: The authoritative security summary reports an unaudited local module imported from a hard-coded user path.

Mitigation: Install and review a trusted api_client module in a controlled environment before enabling the skill.

Risk: The authoritative security guidance says documentation should be corrected to match the actual benchmark logic.

Mitigation: Review the benchmark formulas, ranking semantics, and quadrant labels against the deployed business logic before release.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON result data and plain-text benchmark report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns store performance metrics, ranking, matrix quadrant, top peer stores, and error messages when data is unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact version section)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
