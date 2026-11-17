## Description:

Calculate SAR indicator values for A-share stocks, analyze trend, price position, volume ratio, and momentum, and provide a four-dimensional technical-analysis score with a trading suggestion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohanyang92](https://clawhub.ai/user/haohanyang92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis users can use this skill to fetch A-share historical K-line data, calculate SAR-based indicators, and generate concise technical-analysis summaries for one or more stock codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill retrieves external market data through Baostock as part of normal operation.

Mitigation: Run it in a dedicated virtual environment with appropriate network controls, and expect outbound access to the market-data provider.

Risk: The generated bullish or bearish scores and recommendations could be mistaken for financial advice.

Mitigation: Treat the output as informational technical analysis and require independent review before making trading decisions.

Risk: Dependency changes could alter runtime behavior or results.

Mitigation: Pin dependency versions for baostock, pandas, and numpy when deploying the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown instructions and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language CLI output with SAR values, trend direction, volume ratio, component scores, total score, and bullish or bearish recommendation labels.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
