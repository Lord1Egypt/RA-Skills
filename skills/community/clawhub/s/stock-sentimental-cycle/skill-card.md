## Description:

Analyzes A-share speculative sentiment cycles by scoring limit-up counts, consecutive-board height, failed-board rate, premium, turnover, limit-down pressure, and market breadth to classify cycle stage and surface reversal signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuqp](https://clawhub.ai/user/qiuqp)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and market analysts use this skill to produce structured A-share sentiment-cycle reviews, including stage classification, trend assessment, reversal-signal checks, and position-reference guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated position guidance could be mistaken for investment advice.

Mitigation: Treat outputs as trading reference only and require human review before acting on them.

Risk: External market-data calls may have cost or data-sharing implications.

Mitigation: Confirm before relying on configured external API calls when cost, credentials, or data sharing matters.

Risk: Market-data APIs may be unavailable or incomplete.

Mitigation: Use the skill's manual data-completion path and mark missing dimensions clearly in the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiuqp/skills/stock-sentimental-cycle)
- [Eastmoney financial data API endpoint](https://mkapi2.dfcfs.com/finskillshub/api/claw/query)

## Skill Output:

**Output Type(s):** [analysis, text, markdown, guidance]

**Output Format:** [Markdown report with scoring tables, trend analysis, reversal-signal status, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call market-data tools or request manual data completion when automated data is unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-06-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
