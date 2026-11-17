## Description:

A Chinese-language A-share stock diagnosis skill that uses Wyckoff 2.0 methods to fetch K-line data, calculate technical indicators, analyze trends, identify support and resistance, assess Wyckoff structure, and summarize risk-reward signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxarch1980](https://clawhub.ai/user/dxarch1980)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can use this skill to generate Chinese-language technical-analysis reports for A-share stock codes, including price structure, trend, volume, Wyckoff phase, historical signal statistics, and risk-reward context. Outputs are informational and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock analysis output may be mistaken for investment advice.

Mitigation: Treat reports as informational technical analysis only and review decisions with qualified financial judgment.

Risk: The skill depends on efinance to fetch market data at runtime.

Mitigation: Install efinance in an isolated virtual environment and pin the dependency version where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxarch1980/skills/wyckoff-stock)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Chinese-language console report and structured report object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script expects an A-share stock code and optionally analyzes the most recent K-line history available through efinance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
