## Description:

Generates a daily 15:30 market report covering index moves, sector rankings, bond-market updates, and fixed-income-plus track forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wesdaliang](https://clawhub.ai/user/wesdaliang)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and agent users use this skill after market close to prepare a Markdown market brief for China equity indexes, sector performance, bond yields, and fixed-income-plus product-track outlooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to use unscoped external memory and non-packaged STANDARD/ files for financial analysis.

Mitigation: Use it only in workspaces where MEMORY.md and the referenced STANDARD/ files are intended inputs for this report and do not contain unrelated private information or instructions.

Risk: The generated fixed-income-plus track outlooks are forecasts and may be wrong or incomplete.

Mitigation: Treat the report as informational commentary rather than investment advice, and review the market data and risk warnings before use.

## Reference(s):

- [Market Data Query Reference](references/market_data.md)
- [ClawHub Skill Page](https://clawhub.ai/wesdaliang/skills/xqant-daily-market-report)
- [Publisher Profile](https://clawhub.ai/user/wesdaliang)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown market report with concise analysis and risk warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current market data and referenced product lists when available; forecasts should be treated as informational commentary, not investment advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
